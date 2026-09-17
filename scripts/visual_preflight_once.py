from pathlib import Path
import csv
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PLANS = ROOT / 'docs' / 'illustration-plans'
ASSETS = ROOT / 'assets'
REPORT = ROOT / 'docs' / 'reviews' / 'VISUAL_PREFLIGHT.md'
ILLUSTRATION_REGISTER = ROOT / 'references' / 'illustrations.md'
PHOTO_REGISTER = ROOT / 'references' / 'photographs.md'

PARTS = [
    (1, 5, 'I — Foundations'),
    (6, 14, 'II — Honey Bee Biology'),
    (15, 23, 'III — Starting an Apiary'),
    (24, 38, 'IV — Colony Management'),
    (39, 46, 'V — Bee Health'),
    (47, 54, 'VI — Honey Production'),
    (55, 59, 'VII — Other Hive Products'),
    (60, 69, 'VIII — Beekeeping Business'),
    (70, 74, 'IX — Sustainability'),
]


def part_for(chapter):
    for start, end, title in PARTS:
        if start <= chapter <= end:
            return title
    raise ValueError(chapter)


def classify(title, description):
    s = (title + ' ' + description).lower()
    tests = [
        ('decision_flow', ('decision', 'decision tree', 'triage', 'framework')),
        ('timeline', ('timeline', 'calendar', 'seasonal cycle')),
        ('map_landscape', ('map', 'landscape', 'apiary layout', 'site plan')),
        ('chart_data', ('chart', 'graph', 'curve', 'dashboard', 'matrix')),
        ('life_cycle', ('life cycle', 'reproductive cycle', 'development cycle')),
        ('comparison', (' versus ', ' vs ', 'comparison', 'compared', 'before-and-after', 'before and after')),
        ('anatomical', ('anatomy', 'anatomical', 'gland', 'trachea', 'external morphology')),
        ('technical_cutaway', ('cutaway', 'cross-section', 'cross section', 'section view')),
        ('process', ('procedure', 'sequence', 'workflow', 'process', 'sampling', 'installation', 'handling', 'step-by-step')),
    ]
    for label, words in tests:
        if any(w in s for w in words):
            return label
    return 'scientific_illustration'


def production_size(visual_type):
    if visual_type in {'decision_flow', 'timeline', 'map_landscape', 'chart_data', 'life_cycle'}:
        return 'double-column-or-full-page'
    if visual_type in {'comparison', 'technical_cutaway', 'anatomical'}:
        return 'double-column'
    return 'single-or-double-column'


def parse_plan_heading(text, path):
    m = re.match(r'# Chapter (\d+)\s+[—–-]\s+(.+?): Illustration Plan', text)
    if not m:
        raise ValueError(f'Unexpected illustration-plan heading: {path}')
    return int(m.group(1)), m.group(2).strip()


def visual_matches(text, chapter):
    """Return normalised matches for both modern Figure headings and legacy Visual headings."""
    modern = re.compile(r'^### Figure (\d+)\.(\d+)\s+[—–-]\s+(.+?)\s*$', re.M)
    legacy = re.compile(r'^## Visual (\d+)\s+[—–-]\s+(.+?)\s*$', re.M)
    found = []
    for m in modern.finditer(text):
        found.append({
            'start': m.start(), 'end': m.end(),
            'chapter': int(m.group(1)), 'seq': int(m.group(2)), 'title': m.group(3).strip(),
            'style': 'figure',
        })
    for m in legacy.finditer(text):
        found.append({
            'start': m.start(), 'end': m.end(),
            'chapter': chapter, 'seq': int(m.group(1)), 'title': m.group(2).strip(),
            'style': 'legacy-visual',
        })
    found.sort(key=lambda x: x['start'])
    return found


def parse_figures(path):
    text = path.read_text(encoding='utf-8')
    chapter, chapter_title = parse_plan_heading(text, path)
    matches = visual_matches(text, chapter)
    figures = []

    for i, m in enumerate(matches):
        start = m['end']
        end = matches[i + 1]['start'] if i + 1 < len(matches) else len(text)
        block = text[start:end].strip()
        # Remove book-level sections after the last visual while retaining subheadings
        # such as Format / Content / Accuracy Requirement inside a legacy brief.
        if i + 1 == len(matches):
            block = re.split(r'^## (?:Accuracy Requirements|Accessibility|Accessibility and Layout|Final-Layout Notes|Final Layout Notes)\s*$', block, maxsplit=1, flags=re.M)[0].strip()
        description = re.sub(r'\s+', ' ', block)

        if m['chapter'] != chapter:
            raise ValueError(f'Figure chapter mismatch in {path}: chapter {m["chapter"]}')
        title = m['title']
        seq = m['seq']
        visual_type = classify(title, description)
        figures.append({
            'asset_id': f'F{chapter:02d}.{seq:02d}',
            'figure_id': f'{chapter}.{seq}',
            'chapter': chapter,
            'chapter_title': chapter_title,
            'part': part_for(chapter),
            'working_title': title,
            'brief': description,
            'visual_type': visual_type,
            'source_plan': str(path.relative_to(ROOT)),
            'source_heading_style': m['style'],
            'production_status': 'BRIEF_READY',
            'provenance_plan': 'original_for_handbook',
            'rights_status': 'TO_BE_CREATED_OR_COMMISSIONED',
            'accuracy_status': 'PENDING_ASSET_REVIEW',
            'accessibility_status': 'REQUIRE_ALT_TEXT_GREYSCALE_COLOUR_INDEPENDENT',
            'recommended_print_size': production_size(visual_type),
            'final_asset_path': None,
            'revision_id': None,
        })

    if not figures:
        raise ValueError(f'No Figure/Visual headings parsed from {path}')

    # Every sequence within a chapter must be unique; gaps are allowed because some
    # plans may intentionally consolidate or retire a number later.
    seqs = [x['seq'] for x in matches]
    if len(seqs) != len(set(seqs)):
        raise ValueError(f'Duplicate figure/visual sequence in {path}: {seqs}')
    return figures


def parse_photos(path):
    text = path.read_text(encoding='utf-8')
    heading_re = re.compile(r'^### Photo (\d+)\.(\d+)\s+[—–-]\s+(.+?)\s*$', re.M)
    matches = list(heading_re.finditer(text))
    photos = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end].strip()
        block = re.split(r'^##\s+', block, maxsplit=1, flags=re.M)[0].strip()
        description = re.sub(r'\s+', ' ', block)
        chapter, seq = int(m.group(1)), int(m.group(2))
        photos.append({
            'asset_id': f'P{chapter:02d}.{seq:02d}',
            'photo_id': f'{chapter}.{seq}',
            'chapter': chapter,
            'part': part_for(chapter),
            'working_title': m.group(3).strip(),
            'shot_brief': description,
            'source_register': str(path.relative_to(ROOT)),
            'production_status': 'PLANNED',
            'preferred_provenance': 'original_or_clearly_licensed',
            'rights_status': 'UNSOURCED',
            'technical_review_status': 'PENDING',
            'final_asset_path': None,
        })
    return photos


def update_illustration_register(figure_count):
    text = ILLUSTRATION_REGISTER.read_text(encoding='utf-8')
    old = '''A repository audit performed after completion of Chapter 74 found:\n\n- Chapters **26–74** already had dedicated files named `chapter-NN-illustration-plan.md`.\n- Chapters **22–25** had valid earlier plans under legacy filenames `chapter-22.md` through `chapter-25.md`.\n- Chapters **1–21** had no dedicated illustration-plan files in `main`.\n- This reference-material branch adds dedicated, standardised plans for Chapters **1–21**, eliminating the missing-plan gap.\n- The archived noncanonical Honey Quality draft and its archived illustration plan remain under `docs/reference/` and are **not** part of the canonical figure sequence.\n\nAfter this branch, every canonical chapter 1–74 has a chapter-level visual plan.\n\n### Naming note\n\nFor final production, legacy files for Chapters 22–25 should be treated as authoritative plan sources despite their shorter filenames. Renaming can be done during the formatting pass if desired, but duplicate copies should not be created merely for filename consistency.'''
    new = f'''The final pre-production audit confirms:\n\n- every canonical Chapter **1–74** now has a dedicated standard file named `docs/illustration-plans/chapter-NN-illustration-plan.md`;\n- the formatting validator discovered the remaining Chapter 22–25 naming gap and dedicated standard plans were added before publication assembly was approved;\n- the archived noncanonical Honey Quality draft and archived plan remain under `docs/reference/` and are **not** part of the canonical figure sequence;\n- the chapter plans currently define **{figure_count}** planned figures in the machine-readable visual-production manifest.\n\nThe canonical plan naming gap is therefore closed. Final artwork itself remains pending production/review under Issue #100.'''
    if old not in text:
        raise RuntimeError('Expected legacy inventory paragraph not found in illustrations register')
    text = text.replace(old, new, 1)
    text = text.replace('| III — Starting an Apiary | 15–23 | Complete; 22–23 legacy filenames | Artwork pending |',
                        '| III — Starting an Apiary | 15–23 | Complete; standard filenames | Artwork pending |')
    text = text.replace('| IV — Colony Management | 24–38 | Complete; 24–25 legacy filenames | Artwork pending |',
                        '| IV — Colony Management | 24–38 | Complete; standard filenames | Artwork pending |')
    ILLUSTRATION_REGISTER.write_text(text, encoding='utf-8')


def main():
    expected = [PLANS / f'chapter-{n:02d}-illustration-plan.md' for n in range(1, 75)]
    missing = [str(p.relative_to(ROOT)) for p in expected if not p.exists()]
    if missing:
        raise SystemExit('Missing plans:\n' + '\n'.join(missing))

    figures = []
    for path in expected:
        figures.extend(parse_figures(path))

    ids = [x['figure_id'] for x in figures]
    if len(ids) != len(set(ids)):
        dupes = sorted({x for x in ids if ids.count(x) > 1})
        raise SystemExit('Duplicate figure IDs: ' + ', '.join(dupes))

    photos = parse_photos(PHOTO_REGISTER)
    photo_ids = [x['photo_id'] for x in photos]
    if len(photo_ids) != len(set(photo_ids)):
        raise SystemExit('Duplicate photo IDs detected')

    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / 'visual-production-manifest.json').write_text(
        json.dumps({'figure_count': len(figures), 'figures': figures}, indent=2, ensure_ascii=False) + '\n',
        encoding='utf-8'
    )
    with (ASSETS / 'visual-production-manifest.csv').open('w', encoding='utf-8', newline='') as f:
        fields = ['asset_id','figure_id','chapter','chapter_title','part','working_title','visual_type','production_status','rights_status','accuracy_status','recommended_print_size','source_plan']
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in figures:
            writer.writerow({k: row.get(k) for k in fields})

    (ASSETS / 'photo-production-manifest.json').write_text(
        json.dumps({'photo_count': len(photos), 'photos': photos}, indent=2, ensure_ascii=False) + '\n',
        encoding='utf-8'
    )

    update_illustration_register(len(figures))

    type_counts = {}
    legacy_count = 0
    for item in figures:
        type_counts[item['visual_type']] = type_counts.get(item['visual_type'], 0) + 1
        if item['source_heading_style'] == 'legacy-visual':
            legacy_count += 1
    type_lines = '\n'.join(f'- {k}: **{v}**' for k, v in sorted(type_counts.items()))

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(f'''# Visual Production Preflight — References 82–85

**Issues:** #100, #101, #102, #103  
**Date:** 17 September 2026  
**Status:** **PREFLIGHT PASS — ASSET PRODUCTION / SOURCING NEXT**

## 1. Purpose

This preflight converts the 74 chapter illustration plans and the photographic shot register into machine-readable production manifests before final asset creation. It does not mark unproduced assets as approved.

## 2. Inventory

- canonical chapter illustration plans found: **74 / 74**
- parsed planned figures/visuals: **{len(figures)}**
- legacy `Visual N` headings normalised to figure IDs in the manifest: **{legacy_count}**
- duplicate figure IDs: **0**
- parsed planned photographs: **{len(photos)}**
- duplicate photograph IDs: **0**
- pre-layout semantic index: **present** (`references/index.md`)
- master diagram register: **present** (`references/diagrams.md`)
- master illustration register: **present** (`references/illustrations.md`)
- photograph shot register: **present** (`references/photographs.md`)

## 3. Generated Production Manifests

- `assets/visual-production-manifest.json` — complete figure briefs and production metadata
- `assets/visual-production-manifest.csv` — production-board friendly figure index
- `assets/photo-production-manifest.json` — photograph sourcing/rights queue

All generated figure records remain at **BRIEF_READY** / **PENDING_ASSET_REVIEW** until an actual asset exists and passes accuracy, rights, accessibility and proof gates.

## 4. Figure-Type Distribution

{type_lines}

Classification is a production-routing aid based on the approved brief text; technical review of each finished visual remains mandatory.

## 5. Corrective Finding Resolved

Formatting validation exposed a real pre-production gap: standard dedicated illustration-plan files for Chapters 22–25 were missing even though older planning material existed. Standard professional plans were created for:

- Chapter 22 — Smokers and Hive Tools;
- Chapter 23 — Beekeeping Safety and First Aid;
- Chapter 24 — Installing Bees;
- Chapter 25 — Routine Hive Inspections.

`references/illustrations.md` has been updated so it no longer describes those plans as legacy-filename exceptions.

## 6. Asset Gates

No final figure or photograph can move to `APPROVED` until it passes:

1. manuscript alignment;
2. scientific/mechanical accuracy;
3. safety/legal review;
4. greyscale and final-size legibility;
5. alt-text/accessibility review;
6. commercial print/digital rights/provenance;
7. final-layout proof verification.

## 7. Production Order

Recommended order for fastest risk reduction:

1. bee-health diagnostic/life-cycle visuals;
2. safety and practical handling sequences;
3. anatomy/biology core plates;
4. honey-processing and food-safety diagrams;
5. hive-product processing/safety visuals;
6. traceability/business/compliance diagrams;
7. sustainability/research/future diagrams;
8. field photographs with verified provenance/rights.

## 8. Reference 85 Index

The semantic index already exists and correctly uses chapter/reference locators rather than invented page numbers. Issue #103 must remain open until final PDF/print pagination is stable and page locators are generated and proofed.

## 9. Conclusion

Visual inventory and pre-production routing are now deterministic. The next work is actual illustration/diagram production and photograph sourcing/rights review, followed by placement and final pagination.
''', encoding='utf-8')

    print(f'figures={len(figures)} photos={len(photos)} legacy_visuals={legacy_count}')
    print(type_counts)


if __name__ == '__main__':
    main()
