from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
FIGURES_PATH = ROOT / 'assets' / 'visual-production-manifest.json'
PHOTOS_PATH = ROOT / 'assets' / 'photo-production-manifest.json'
OUT_JSON = ROOT / 'assets' / 'visual-production-priority.json'
OUT_CSV = ROOT / 'assets' / 'visual-production-priority.csv'
PHOTO_JSON = ROOT / 'assets' / 'photo-production-priority.json'
REPORT = ROOT / 'docs' / 'reviews' / 'VISUAL_RATIONALISATION.md'

TYPE_WEIGHT = {
    'life_cycle': 5,
    'decision_flow': 5,
    'anatomical': 5,
    'technical_cutaway': 4,
    'process': 4,
    'comparison': 4,
    'chart_data': 3,
    'timeline': 3,
    'map_landscape': 3,
    'scientific_illustration': 2,
}

HIGH_KEYWORDS = [
    'varroa', 'tropilaelaps', 'foulbrood', 'nosema', 'virus', 'disease', 'diagnos',
    'emergency', 'first aid', 'safety', 'smoker', 'anatom', 'brood', 'queen',
    'swarm', 'inspection', 'sampling', 'refractometer', 'extract', 'traceability',
    'haccp', 'food safety', 'wax rendering', 'pollen', 'propolis', 'royal jelly',
    'venom', 'biodiversity', 'pollinator', 'evidence', 'life cycle', 'ventilation'
]
LOW_KEYWORDS = ['record sheet', 'record example', 'worksheet', 'dashboard concept', 'checklist', 'form example']

REUSE_RULES = [
    ('VARROA_CORE', ['varroa life cycle', 'varroa reproductive cycle']),
    ('HEALTHY_BROOD_REFERENCE', ['healthy brood', 'healthy larvae', 'brood reference']),
    ('TRACEABILITY_CHAIN', ['traceability chain', 'lot traceability', 'traceability flow']),
    ('EVIDENCE_LADDER', ['evidence ladder', 'evidence hierarchy']),
    ('HONEY_QUALITY_FAMILY', ['hmf', 'diastase', 'honey quality', 'moisture', 'crystallisation']),
    ('CLEAN_ZONE_SYSTEM', ['clean and dirty', 'clean zone', 'hygiene zone', 'workflow']),
    ('BEE_CASTE_ANATOMY', ['worker anatomy', 'queen anatomy', 'drone anatomy']),
    ('APIARY_SITE_SYSTEM', ['apiary site', 'site selection', 'apiary layout']),
]


def score(fig):
    s = TYPE_WEIGHT.get(fig['visual_type'], 1)
    text = (fig['working_title'] + ' ' + fig.get('brief', '')).lower()
    s += sum(2 for k in HIGH_KEYWORDS if k in text)
    s -= sum(2 for k in LOW_KEYWORDS if k in text)
    ch = fig['chapter']
    if 39 <= ch <= 46:
        s += 3
    elif ch in {21, 22, 23, 24, 25, 33, 38}:
        s += 2
    elif 6 <= ch <= 14:
        s += 1
    elif 47 <= ch <= 59:
        s += 1
    return s


def reuse_family(fig):
    text = (fig['working_title'] + ' ' + fig.get('brief', '')).lower()
    for family, terms in REUSE_RULES:
        if any(term in text for term in terms):
            return family
    return None


def chapter_limits(ch):
    if 39 <= ch <= 46:
        return 5, 2
    if ch in {21, 22, 23, 24, 25, 33, 38}:
        return 4, 2
    if 60 <= ch <= 74:
        return 2, 2
    return 3, 2


def prioritise_figures(figures):
    by_ch = {}
    for f in figures:
        item = dict(f)
        item['priority_score'] = score(item)
        item['reuse_family'] = reuse_family(item)
        by_ch.setdefault(item['chapter'], []).append(item)

    out = []
    for ch in sorted(by_ch):
        items = sorted(by_ch[ch], key=lambda x: (-x['priority_score'], int(x['figure_id'].split('.')[1])))
        core_n, support_n = chapter_limits(ch)
        for i, item in enumerate(items):
            if i < core_n:
                item['editorial_priority'] = 'A_CORE'
                item['selection_status'] = 'SELECT_FOR_FINAL_LAYOUT'
            elif i < core_n + support_n:
                item['editorial_priority'] = 'B_SUPPORTING'
                item['selection_status'] = 'SELECT_IF_LAYOUT_ALLOWS'
            else:
                item['editorial_priority'] = 'C_OPTIONAL_MERGE'
                item['selection_status'] = 'MERGE_CROSS_REFERENCE_OR_OMIT_UNLESS_NEEDED'
            out.append(item)
    return out


def photo_score(photo):
    text = (photo['working_title'] + ' ' + photo.get('shot_brief', '')).lower()
    s = 0
    for kw in ['confirmed', 'disease', 'varroa', 'foulbrood', 'nosema', 'safety', 'first-aid',
               'first aid', 'brood', 'refractometer', 'quality', 'damage', 'habitat', 'apiary site',
               'transport', 'wax', 'pollen', 'propolis', 'royal jelly', 'venom']:
        if kw in text:
            s += 2
    if photo['chapter'] in range(39, 47):
        s += 3
    if photo['chapter'] in {15, 21, 22, 23, 24, 25, 33, 38, 48, 49, 52, 54, 55, 56, 57, 58, 59}:
        s += 1
    return s


def prioritise_photos(photos):
    items = []
    for p in photos:
        q = dict(p)
        q['priority_score'] = photo_score(q)
        items.append(q)
    ranked = sorted(items, key=lambda x: (-x['priority_score'], x['chapter'], x['photo_id']))
    # Keep the photo programme intentionally small: photographs are for real-world
    # appearance/provenance where illustration is inferior, not decoration.
    a_n = min(40, len(ranked))
    b_n = min(25, max(0, len(ranked) - a_n))
    for i, p in enumerate(ranked):
        if i < a_n:
            p['editorial_priority'] = 'A_CORE'
            p['selection_status'] = 'SOURCE_OR_CREATE'
        elif i < a_n + b_n:
            p['editorial_priority'] = 'B_SUPPORTING'
            p['selection_status'] = 'SOURCE_IF_RIGHTS_AND_LAYOUT_ALLOW'
        else:
            p['editorial_priority'] = 'C_OPTIONAL'
            p['selection_status'] = 'OMIT_UNLESS_UNIQUE_VALUE_CONFIRMED'
    return sorted(ranked, key=lambda x: (x['chapter'], x['photo_id']))


def main():
    figures = json.loads(FIGURES_PATH.read_text(encoding='utf-8'))['figures']
    photos = json.loads(PHOTOS_PATH.read_text(encoding='utf-8'))['photos']

    prioritised = prioritise_figures(figures)
    pphotos = prioritise_photos(photos)

    fig_counts = {}
    for x in prioritised:
        fig_counts[x['editorial_priority']] = fig_counts.get(x['editorial_priority'], 0) + 1
    photo_counts = {}
    for x in pphotos:
        photo_counts[x['editorial_priority']] = photo_counts.get(x['editorial_priority'], 0) + 1

    # Count potential reuse families to guide consolidation rather than duplicate art.
    reuse_counts = {}
    for x in prioritised:
        if x['reuse_family']:
            reuse_counts[x['reuse_family']] = reuse_counts.get(x['reuse_family'], 0) + 1

    OUT_JSON.write_text(json.dumps({
        'policy': {
            'A_CORE': 'selected for final layout unless later technical review rejects or merges it',
            'B_SUPPORTING': 'selected when it adds non-duplicative teaching value and space permits',
            'C_OPTIONAL_MERGE': 'merge, cross-reference, or omit unless later review shows unique value',
        },
        'counts': fig_counts,
        'figures': prioritised,
    }, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    fields = ['asset_id','figure_id','chapter','chapter_title','working_title','visual_type','priority_score','editorial_priority','selection_status','reuse_family','source_plan']
    with OUT_CSV.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in sorted(prioritised, key=lambda x: (x['chapter'], int(x['figure_id'].split('.')[1]))):
            w.writerow({k: row.get(k) for k in fields})

    PHOTO_JSON.write_text(json.dumps({
        'counts': photo_counts,
        'photos': pphotos,
    }, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    fig_lines = '\n'.join(f'- {k}: **{v}**' for k, v in sorted(fig_counts.items()))
    photo_lines = '\n'.join(f'- {k}: **{v}**' for k, v in sorted(photo_counts.items()))
    reuse_lines = '\n'.join(f'- {k}: **{v} planned candidates**' for k, v in sorted(reuse_counts.items())) or '- None detected.'

    core = fig_counts.get('A_CORE', 0)
    supporting = fig_counts.get('B_SUPPORTING', 0)
    optional = fig_counts.get('C_OPTIONAL_MERGE', 0)

    REPORT.write_text(f'''# Visual Rationalisation Review

**Date:** 17 September 2026  
**Scope:** Issues #100–#102  
**Result:** **PRODUCTION SET RATIONALISED — DO NOT PRODUCE ALL 760 PLANNED VISUALS BLINDLY**

## 1. Reason for This Pass

The chapter-level planning process intentionally over-captured useful visual ideas. Preflight found **{len(prioritised)}** distinct planned figure/illustration/diagram briefs. Producing all of them as separate final assets would create unnecessary cost, repetition, layout density and review burden.

This pass routes those briefs into a smaller editorial production hierarchy while preserving every original brief in the source manifest.

## 2. Figure Priorities

{fig_lines}

Recommended first production wave: **{core} A_CORE** assets.  
Potential second wave: **{supporting} B_SUPPORTING** assets.  
The remaining **{optional}** items should normally be merged, cross-referenced, converted to text/table treatment, or omitted unless they provide unique teaching value.

## 3. Photograph Priorities

{photo_lines}

Photographs remain deliberately limited because they are used only for authentic appearance, field context or diagnosis where illustration is inferior. Decorative stock photography remains excluded.

## 4. Reuse / Consolidation Families

{reuse_lines}

A reuse family does not automatically mean identical art can be reused. It flags briefs that must be reviewed together so the book develops one coherent core figure and derivative/cross-reference treatment where possible.

## 5. Safety and Accuracy Rule

Automated scoring determines production order only. It does **not** approve scientific content. Every produced asset still requires the visual gates in `references/illustrations.md` and `docs/reviews/VISUAL_PREFLIGHT.md`.

## 6. Production Files

- `assets/visual-production-priority.json`
- `assets/visual-production-priority.csv`
- `assets/photo-production-priority.json`

These files are the operational queue for asset creation and sourcing.

## 7. Editorial Decision

Final layout should not be forced to include a fixed number of visuals per chapter. The A/B/C routing exists to reduce duplication and focus production on visuals that change understanding, decisions, safety or diagnostic accuracy.

**Next step:** produce A_CORE assets by technical family, review them as a set, then add B_SUPPORTING assets only where the proof demonstrates real additional value.
''', encoding='utf-8')

    print('figure_counts', fig_counts)
    print('photo_counts', photo_counts)
    print('reuse_counts', reuse_counts)


if __name__ == '__main__':
    main()
