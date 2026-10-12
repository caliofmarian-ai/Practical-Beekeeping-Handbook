from pathlib import Path
import argparse
import hashlib
import json
import os
import re
from urllib.parse import quote, unquote, urlsplit, urlunsplit

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



# Editorial planning belongs in the source repository, not the reader edition.
# Section bodies are excluded only in the assembled publication manuscript.
INTERNAL_SECTION_HEADERS = {'Review Notes', 'Figure Placeholders'}
MARKDOWN_LINK = re.compile(
    r'''(?P<opening>!?\[[^\]\n]*\]\()(?P<target>[^)\s]+)(?P<closing>(?:\s+["'][^"']*["'])?\))'''
)


def strip_internal_sections(markdown: str):
    """Exclude exact H2 editorial headings and their children, retaining source files."""
    result = []
    removed = []
    lines = markdown.splitlines(keepends=True)
    skip = False
    for line in lines:
        heading = re.match(r'^##\s+(.+?)\s*    return ROOT / 'chapters' / f'chapter-{n:02d}.md'


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


def assemble(check: bool = False):
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
    excluded_sections = []
    link_rebase_count = 0
    embedded_images = 0
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
        text, excluded = strip_internal_sections(text)
        text, rebased, images = rebase_local_links(text, path)
        link_rebase_count += rebased
        embedded_images += images
        excluded_sections.extend([f'Chapter {n}: {item}' for item in excluded])
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
        text, excluded = strip_internal_sections(text)
        text, rebased, images = rebase_local_links(text, path)
        link_rebase_count += rebased
        embedded_images += images
        excluded_sections.extend([f'Reference {number}: {item}' for item in excluded])
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

    verified_images = validate_output_images(output)
    if verified_images != embedded_images:
        raise SystemExit(f'Image accounting mismatch: {verified_images} != {embedded_images}')

    manifest['reader_only_sections_excluded'] = excluded_sections
    manifest['local_links_rebased_count'] = link_rebase_count
    manifest['local_images_verified_count'] = verified_images
    manifest['generated_file'] = str(OUT_MD.relative_to(ROOT))
    manifest['generated_sha256'] = hashlib.sha256(output.encode('utf-8')).hexdigest()
    manifest['chapter_count'] = 74
    manifest['reference_count'] = 11
    manifest['asset_plan_count'] = 74
    manifest_text = json.dumps(manifest, indent=2, ensure_ascii=False) + '\n'
    if check:
        if not OUT_MD.is_file() or not OUT_MANIFEST.is_file():
            raise SystemExit('Publication files missing; run builder without --check')
        if OUT_MD.read_text(encoding='utf-8') != output:
            raise SystemExit('Publication manuscript is stale; rebuild it from current source')
        if OUT_MANIFEST.read_text(encoding='utf-8') != manifest_text:
            raise SystemExit('Publication manifest is stale; rebuild it from current source')
        print('CHECK PASSED: committed publication manuscript and manifest are current')
    else:
        OUT_MD.write_text(output, encoding='utf-8')
        OUT_MANIFEST.write_text(manifest_text, encoding='utf-8')

    print(f'Generated {OUT_MD.relative_to(ROOT)}')
    print(f'Characters: {len(output)}')
    print('Chapters: 74')
    print('References: 11')
    print('Asset plans: 74')
    print(f'Local links rebased: {link_rebase_count}')
    print(f'Local images verified: {verified_images}')
    print(f'Internal editorial sections excluded: {len(excluded_sections)}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build/validate the canonical publication manuscript')
    parser.add_argument('--check', action='store_true', help='Fail if the committed assembled source is stale')
    args = parser.parse_args()
    assemble(check=args.check)
, line.strip())
        if heading:
            name = heading.group(1).strip()
            if name in INTERNAL_SECTION_HEADERS:
                removed.append(name)
                skip = True
                continue
            skip = False
        elif re.match(r'^#\s+', line):
            skip = False
        if not skip:
            result.append(line)
    return ''.join(result).rstrip() + '\n', removed


def rebase_local_links(markdown: str, source: Path):
    """Rebase local Markdown links for the publication directory and reject missing files."""
    links_rebased = 0
    embedded_images = 0
    source_parent = source.resolve().parent
    root = ROOT.resolve()
    destination = OUT_DIR.resolve()
    in_fence = False
    result = []

    def rewrite(match):
        nonlocal links_rebased, embedded_images
        raw = match.group('target')
        url = urlsplit(raw)
        if url.scheme or url.netloc or not url.path or url.path.startswith('/'):
            return match.group(0)

        candidate = (source_parent / unquote(url.path)).resolve()
        if not candidate.is_relative_to(root):
            raise ValueError(f'Link escapes repository: {source.relative_to(ROOT)}: {raw}')
        if not candidate.is_file():
            raise ValueError(f'Missing local link target: {source.relative_to(ROOT)}: {raw}')

        rebased_path = os.path.relpath(candidate, destination).replace(os.sep, '/')
        updated = urlunsplit(('', '', quote(rebased_path, safe='/._~-'), url.query, url.fragment))
        links_rebased += 1
        if match.group('opening').startswith('!'):
            embedded_images += 1
        return match.group('opening') + updated + match.group('closing')

    for line in markdown.splitlines(keepends=True):
        # Do not modify or validate examples inside fenced code blocks.
        if re.match(r'^\s*(?:\x60{3,}|~{3,})', line):
            in_fence = not in_fence
            result.append(line)
        elif in_fence:
            result.append(line)
        else:
            result.append(MARKDOWN_LINK.sub(rewrite, line))

    return ''.join(result), links_rebased, embedded_images


def validate_output_images(markdown: str):
    """Verify every local Markdown image is readable from the generated file's directory."""
    total = 0
    for match in MARKDOWN_LINK.finditer(markdown):
        if not match.group('opening').startswith('!'):
            continue
        url = urlsplit(match.group('target'))
        if url.scheme or url.netloc:
            continue
        if not url.path or url.path.startswith('/'):
            raise ValueError(f'Unexpected absolute/empty image link in publication: {match.group("target")}')
        target = (OUT_DIR / unquote(url.path)).resolve()
        if not target.is_relative_to(ROOT.resolve()) or not target.is_file():
            raise ValueError(f'Broken publication image link: {match.group("target")}')
        total += 1
    return total


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
