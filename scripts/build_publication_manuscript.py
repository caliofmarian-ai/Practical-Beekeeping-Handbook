from pathlib import Path
import json
import re
import hashlib

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / 'exports' / 'publication'
OUT_MD = OUT_DIR / 'Practical-Beekeeping-Handbook.md'
OUT_MANIFEST = OUT_DIR / 'manifest.json'

PARTS = [
    ('Part I', 'Foundations', 1, 5),
    ('Part II', 'Honey Bee Biology', 6, 14),
    ('Part III', 'Starting an Apiary', 15, 23),
    ('Part IV', 'Colony Management', 24, 38),
    ('Part V', 'Bee Health', 39, 46),
    ('Part VI', 'Honey Production', 47, 54),
    ('Part VII', 'Other Hive Products', 55, 59),
    ('Part VIII', 'Beekeeping Business', 60, 69),
    ('Part IX', 'Sustainability', 70, 74),
]

REFERENCE_SOURCES = [
    (75, 'Glossary', 'glossary/glossary.md'),
    (76, 'Bibliography', 'bibliography/bibliography.md'),
    (77, 'Recommended Books', 'references/recommended-books.md'),
    (78, 'Beekeeping Organizations', 'references/beekeeping-organizations.md'),
    (79, 'Useful Websites', 'references/useful-websites.md'),
    (80, 'Appendices', 'appendices/appendices.md'),
    (81, 'Tables', 'references/tables.md'),
    (82, 'Illustrations', 'references/illustrations.md'),
    (83, 'Diagrams', 'references/diagrams.md'),
    (84, 'Photographs', 'references/photographs.md'),
    (85, 'Index', 'references/index.md'),
]


def chapter_path(n: int) -> Path:
    return ROOT / 'chapters' / f'chapter-{n:02d}.md'


def plan_path(n: int) -> Path:
    return ROOT / 'docs' / 'illustration-plans' / f'chapter-{n:02d}-illustration-plan.md'


def normalise_chapter_heading(text: str, n: int) -> str:
    lines = text.splitlines()
    if not lines:
        raise ValueError(f'Chapter {n} is empty')
    first = lines[0].strip()
    m = re.match(r'^#\s+Chapter\s+(\d+)\s+[—–-]\s+(.+?)\s*$', first)
    if not m:
        raise ValueError(f'Unexpected chapter heading in chapter {n}: {first!r}')
    if int(m.group(1)) != n:
        raise ValueError(f'Chapter number mismatch: file {n}, heading {m.group(1)}')
    lines[0] = f'# Chapter {n} — {m.group(2)}'
    return '\n'.join(lines).rstrip() + '\n'


def chapter_title(text: str) -> str:
    first = text.splitlines()[0].strip()
    return first.removeprefix('# ').strip()


def validate_sources():
    missing = []
    for n in range(1, 75):
        if not chapter_path(n).is_file():
            missing.append(str(chapter_path(n).relative_to(ROOT)))
        if not plan_path(n).is_file():
            missing.append(str(plan_path(n).relative_to(ROOT)))
    for _, _, rel in REFERENCE_SOURCES:
        if not (ROOT / rel).is_file():
            missing.append(rel)
    if missing:
        raise SystemExit('Missing required publication sources:\n' + '\n'.join(missing))


def part_for_chapter(n: int):
    for part_no, title, start, end in PARTS:
        if start <= n <= end:
            return part_no, title, start, end
    raise ValueError(n)


def source_hash(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assemble():
    validate_sources()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    chunks = []
    chunks.append('# Practical Beekeeping Handbook\n')
    chunks.append('**Publication manuscript — 2026 edition**  \n')
    chunks.append('**Author:** Marian Caliof  \n')
    chunks.append('**Build status:** pre-release; final visual assets and pagination pending.\n')
    chunks.append('\n<!-- TOC -->\n')

    manifest = {
        'edition': '2026',
        'author': 'Marian Caliof',
        'chapters': [],
        'references': [],
        'parts': [],
    }

    current_part = None
    for n in range(1, 75):
        part_no, part_title, start, end = part_for_chapter(n)
        if current_part != part_no:
            current_part = part_no
            chunks.append('\n<!-- PAGEBREAK: PART -->\n')
            chunks.append(f'# {part_no} — {part_title}\n')
            chunks.append(f'*Chapters {start}–{end}*\n')
            manifest['parts'].append({
                'part': part_no,
                'title': part_title,
                'chapters': [start, end],
            })

        path = chapter_path(n)
        raw = path.read_text(encoding='utf-8')
        text = normalise_chapter_heading(raw, n)
        title = chapter_title(text)

        chunks.append('\n<!-- PAGEBREAK: CHAPTER -->\n')
        chunks.append(text)
        chunks.append(f'\n<!-- ASSET-PLAN: docs/illustration-plans/chapter-{n:02d}-illustration-plan.md -->\n')

        manifest['chapters'].append({
            'number': n,
            'title': title,
            'source': str(path.relative_to(ROOT)),
            'source_sha256': source_hash(path),
            'asset_plan': str(plan_path(n).relative_to(ROOT)),
        })

    chunks.append('\n<!-- PAGEBREAK: REFERENCE-MATERIAL -->\n')
    chunks.append('# Reference Material\n')

    for number, title, rel in REFERENCE_SOURCES:
        path = ROOT / rel
        text = path.read_text(encoding='utf-8').strip() + '\n'
        chunks.append('\n<!-- PAGEBREAK: REFERENCE -->\n')
        chunks.append(f'# Reference {number} — {title}\n\n')
        # Avoid duplicate level-1 title from source by demoting only its first heading.
        lines = text.splitlines()
        if lines and lines[0].startswith('# '):
            lines[0] = '## ' + lines[0][2:]
        chunks.append('\n'.join(lines).rstrip() + '\n')
        manifest['references'].append({
            'number': number,
            'title': title,
            'source': rel,
            'source_sha256': source_hash(path),
        })

    output = '\n'.join(chunks).rstrip() + '\n'
    if len(output) < 100000:
        raise SystemExit('Generated manuscript unexpectedly small')

    # Structural validation of generated output.
    found = [int(x) for x in re.findall(r'^# Chapter (\d+) — ', output, flags=re.M)]
    if found != list(range(1, 75)):
        raise SystemExit(f'Generated chapter order invalid: {found[:10]} ... {found[-10:]}')
    refs = [int(x) for x in re.findall(r'^# Reference (\d+) — ', output, flags=re.M)]
    if refs != list(range(75, 86)):
        raise SystemExit(f'Generated reference order invalid: {refs}')

    OUT_MD.write_text(output, encoding='utf-8')
    manifest['generated_file'] = str(OUT_MD.relative_to(ROOT))
    manifest['generated_sha256'] = hashlib.sha256(output.encode('utf-8')).hexdigest()
    manifest['chapter_count'] = 74
    manifest['reference_count'] = 11
    manifest['asset_plan_count'] = 74
    OUT_MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    print(f'Generated {OUT_MD.relative_to(ROOT)}')
    print(f'Characters: {len(output)}')
    print('Chapters: 74')
    print('References: 11')
    print('Asset plans: 74')


if __name__ == '__main__':
    assemble()
