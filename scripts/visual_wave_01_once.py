from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'assets' / 'visual-production-priority.json'
OUT_DIR = ROOT / 'assets' / 'production-briefs'
OUT_JSON = OUT_DIR / 'wave-01-bee-health-safety.json'
OUT_CSV = OUT_DIR / 'wave-01-bee-health-safety.csv'
OUT_MD = OUT_DIR / 'wave-01-bee-health-safety.md'
REPORT = ROOT / 'docs' / 'reviews' / 'VISUAL_WAVE_01_READINESS.md'

TARGET_CHAPTERS = set([21, 22, 23, 24, 25, 33, 38, 39, 40, 41, 42, 43, 44, 45, 46])


def main():
    data = json.loads(SRC.read_text(encoding='utf-8'))
    figures = [
        x for x in data['figures']
        if x['editorial_priority'] == 'A_CORE' and x['chapter'] in TARGET_CHAPTERS
    ]
    figures.sort(key=lambda x: (x['chapter'], int(x['figure_id'].split('.')[1])))
    if not figures:
        raise SystemExit('No Wave 01 A_CORE figures found')

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    queue = []
    for index, item in enumerate(figures, start=1):
        q = {
            'wave': 1,
            'production_order': index,
            'asset_id': item['asset_id'],
            'figure_id': item['figure_id'],
            'chapter': item['chapter'],
            'chapter_title': item['chapter_title'],
            'working_title': item['working_title'],
            'visual_type': item['visual_type'],
            'brief': item.get('brief', ''),
            'reuse_family': item.get('reuse_family'),
            'recommended_print_size': item.get('recommended_print_size'),
            'source_plan': item.get('source_plan'),
            'production_status': 'READY_FOR_ASSET_CREATION',
            'required_review_gates': [
                'manuscript_alignment',
                'scientific_or_mechanical_accuracy',
                'safety_and_legal_review',
                'greyscale_and_final_size_legibility',
                'alt_text_and_accessibility',
                'commercial_rights_and_provenance',
                'final_layout_proof',
            ],
            'rights_plan': 'ORIGINAL_ASSET_FOR_HANDBOOK',
            'final_asset_path': None,
            'technical_review_status': 'PENDING_AFTER_ASSET_CREATION',
        }
        queue.append(q)

    OUT_JSON.write_text(json.dumps({'wave': 1, 'asset_count': len(queue), 'assets': queue}, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    fields = ['production_order','asset_id','figure_id','chapter','chapter_title','working_title','visual_type','reuse_family','recommended_print_size','production_status','source_plan']
    with OUT_CSV.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in queue:
            writer.writerow({k: row.get(k) for k in fields})

    sections = []
    current = None
    for item in queue:
        if current != item['chapter']:
            current = item['chapter']
            sections.append(f'\n## Chapter {current} — {item["chapter_title"]}\n')
        sections.append(
            f'''### {item['asset_id']} — Figure {item['figure_id']} — {item['working_title']}\n\n'''
            f'''**Production order:** {item['production_order']}  \n'''
            f'''**Type:** `{item['visual_type']}`  \n'''
            f'''**Recommended print size:** `{item['recommended_print_size']}`  \n'''
            f'''**Reuse family:** `{item['reuse_family'] or 'none'}`  \n'''
            f'''**Source plan:** `{item['source_plan']}`  \n\n'''
            f'''**Approved source brief:**  \n{item['brief']}\n\n'''
            f'''**Required production gates:** manuscript alignment; scientific/mechanical accuracy; safety/legal review; greyscale and final-size legibility; alt text/accessibility; commercial rights/provenance; final-layout proof.\n'''
        )

    OUT_MD.write_text(f'''# Visual Production Wave 01 — Safety and Bee Health\n\n'''
                      f'''**Status:** READY FOR ASSET CREATION  \n'''
                      f'''**Asset count:** {len(queue)}  \n'''
                      f'''**Scope:** A_CORE visuals from Chapters 21–25, 33, and 38–46.\n\n'''
                      f'''This wave contains the highest-risk visual material: PPE/safety, bee installation/inspection/transport, emergency triage, disease/parasite recognition, diagnostic sampling, and integrated pest management. These assets are produced first because technical or safety errors would have the greatest reader consequence.\n\n'''
                      f'''No item in this document is `APPROVED` artwork. Each is an approved production brief only. Actual final assets must pass every listed gate before layout.\n'''
                      + ''.join(sections), encoding='utf-8')

    by_ch = {}
    by_type = {}
    reuse = {}
    for x in queue:
        by_ch[x['chapter']] = by_ch.get(x['chapter'], 0) + 1
        by_type[x['visual_type']] = by_type.get(x['visual_type'], 0) + 1
        if x['reuse_family']:
            reuse[x['reuse_family']] = reuse.get(x['reuse_family'], 0) + 1

    ch_lines = '\n'.join(f'- Chapter {k}: **{v}**' for k, v in sorted(by_ch.items()))
    type_lines = '\n'.join(f'- {k}: **{v}**' for k, v in sorted(by_type.items()))
    reuse_lines = '\n'.join(f'- {k}: **{v}**' for k, v in sorted(reuse.items())) or '- none in this wave'

    REPORT.write_text(f'''# Visual Wave 01 Readiness Review\n\n'''
                      f'''**Date:** 17 September 2026  \n'''
                      f'''**Issues advanced:** #100 Illustrations, #101 Diagrams  \n'''
                      f'''**Result:** **READY FOR ASSET CREATION — {len(queue)} A_CORE VISUALS**\n\n'''
                      f'''## Scope\n\nWave 01 intentionally focuses on safety and bee-health material before lower-risk decorative or commercial visuals. It includes Chapters 21–25, 33, and 38–46.\n\n'''
                      f'''## Assets by Chapter\n\n{ch_lines}\n\n'''
                      f'''## Assets by Visual Type\n\n{type_lines}\n\n'''
                      f'''## Reuse Families\n\n{reuse_lines}\n\n'''
                      f'''## Production Controls\n\n'''
                      f'''- diagnostic signs must never be converted into image-only proof where confirmation is required;\n'''
                      f'''- all treatment/process visuals must remain label- and jurisdiction-safe;\n'''
                      f'''- safety visuals must show stop/escalation points explicitly;\n'''
                      f'''- disease and parasite scale/morphology must be technically reviewed;\n'''
                      f'''- colour must not carry the only diagnostic distinction;\n'''
                      f'''- every asset requires alt text and commercial publication provenance.\n\n'''
                      f'''## Deliverables\n\n'''
                      f'''- `assets/production-briefs/wave-01-bee-health-safety.md`\n'''
                      f'''- `assets/production-briefs/wave-01-bee-health-safety.json`\n'''
                      f'''- `assets/production-briefs/wave-01-bee-health-safety.csv`\n\n'''
                      f'''## Next Gate\n\nActual asset creation can now proceed in production order. Assets remain unapproved until post-generation technical review is completed.\n''', encoding='utf-8')

    print(f'wave01_assets={len(queue)}')
    print('by_chapter=', by_ch)
    print('by_type=', by_type)


if __name__ == '__main__':
    main()
