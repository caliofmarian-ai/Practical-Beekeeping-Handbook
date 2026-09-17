from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / 'assets' / 'production-briefs' / 'wave-01-bee-health-safety.json'
DIAGRAM_DIR = ROOT / 'assets' / 'diagrams' / 'wave-01'
OUT_JSON = ROOT / 'assets' / 'production-briefs' / 'wave-01-coverage.json'
REPORT = ROOT / 'docs' / 'reviews' / 'VISUAL_WAVE_01_COVERAGE.md'


def main():
    q = json.loads(QUEUE.read_text(encoding='utf-8'))
    assets = q['assets']
    produced = {}
    for p in sorted(DIAGRAM_DIR.glob('fig-*.svg')):
        m = re.match(r'fig-(\d+)-(\d+)-', p.name)
        if not m:
            continue
        fid = f"{int(m.group(1))}.{int(m.group(2))}"
        produced.setdefault(fid, []).append(str(p.relative_to(ROOT)))

    rows=[]
    for a in assets:
        fid=a['figure_id']
        paths=produced.get(fid,[])
        row=dict(a)
        row['produced_paths']=paths
        row['coverage_status']='ACTUAL_VECTOR_PRESENT' if paths else 'NOT_YET_PRODUCED'
        # Routing only; not an approval decision.
        if not paths:
            vt=a.get('visual_type','')
            title=a.get('working_title','').lower()
            high_fidelity_terms=('anatom','brood','larva','mite','varroa','tropilaelaps','tracheal','wing','phenotype','cell','life cycle','midgut','spore')
            row['recommended_next_route']='HIGH_FIDELITY_TECHNICAL_ART_OR_AUTHENTIC_PHOTO' if vt in {'anatomical','life_cycle'} or any(t in title for t in high_fidelity_terms) else 'VECTOR_DIAGRAM_CANDIDATE'
        else:
            row['recommended_next_route']='LAYOUT_PROOF_AND_CAPTION_PAIRING'
        rows.append(row)

    covered=[r for r in rows if r['coverage_status']=='ACTUAL_VECTOR_PRESENT']
    remaining=[r for r in rows if r['coverage_status']=='NOT_YET_PRODUCED']
    vector_remaining=[r for r in remaining if r['recommended_next_route']=='VECTOR_DIAGRAM_CANDIDATE']
    fidelity_remaining=[r for r in remaining if r['recommended_next_route']=='HIGH_FIDELITY_TECHNICAL_ART_OR_AUTHENTIC_PHOTO']

    OUT_JSON.parent.mkdir(parents=True,exist_ok=True)
    OUT_JSON.write_text(json.dumps({
        'wave':1,
        'planned_core_assets':len(rows),
        'actual_vector_assets_covering_core_ids':len(covered),
        'remaining_core_ids':len(remaining),
        'remaining_vector_candidates':len(vector_remaining),
        'remaining_high_fidelity_candidates':len(fidelity_remaining),
        'assets':rows,
    },indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

    chapter_counts={}
    for r in rows:
        ch=r['chapter']
        c=chapter_counts.setdefault(ch,{'planned':0,'covered':0,'remaining':0})
        c['planned']+=1
        if r['coverage_status']=='ACTUAL_VECTOR_PRESENT': c['covered']+=1
        else: c['remaining']+=1

    lines=[]
    lines += ['# Visual Wave 01 — Production Coverage Audit','',
              '**Date:** 17 September 2026  ',
              '**Scope:** 68 A_CORE Wave 01 safety/bee-health briefs  ',
              '**Purpose:** measure actual asset production, not plan count  ','',
              '## Summary','',
              f'- A_CORE briefs in Wave 01: **{len(rows)}**',
              f'- A_CORE figure IDs with actual SVG asset present: **{len(covered)}**',
              f'- A_CORE figure IDs not yet produced: **{len(remaining)}**',
              f'- remaining route: vector-diagram candidates: **{len(vector_remaining)}**',
              f'- remaining route: high-fidelity technical art/authentic-photo candidates: **{len(fidelity_remaining)}**','',
              '> Coverage means an actual SVG exists for that Figure ID. It does **not** mean final layout approval. Produced SVGs still require caption pairing and final-size PDF/EPUB/print proof.','',
              '## Coverage by Chapter','',
              '| Chapter | Planned A_CORE | Actual asset | Remaining |','|---:|---:|---:|---:|']
    for ch in sorted(chapter_counts):
        c=chapter_counts[ch]
        lines.append(f"| {ch} | {c['planned']} | {c['covered']} | {c['remaining']} |")

    lines += ['','## Remaining A_CORE Assets','']
    if not remaining:
        lines.append('- None.')
    else:
        for r in remaining:
            lines.append(f"- **Figure {r['figure_id']} — {r['working_title']}** — `{r['visual_type']}` — route: `{r['recommended_next_route']}`")

    lines += ['','## Editorial Interpretation','',
              '- Diagram/process/control assets can continue as deterministic vectors where that medium improves clarity.',
              '- Anatomical, microscopic, disease-sign and morphology assets should not be forced into simplistic schematic art merely to raise the completion percentage.',
              '- High-fidelity biological visuals require stricter morphology/scale review and may be better served by specialised original illustration or rights-cleared authentic photography.',
              '- `ACTUAL_VECTOR_PRESENT` is therefore a production milestone, not an accuracy waiver or final-placement status.','',
              '## Next Gate','',
              'Produce any remaining true vector candidates, then move the unresolved biological/morphological set into a high-fidelity technical-art queue with explicit reference and review requirements.','']
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text('\n'.join(lines),encoding='utf-8')
    print(f"covered={len(covered)} remaining={len(remaining)} vector={len(vector_remaining)} high_fidelity={len(fidelity_remaining)}")

if __name__=='__main__':
    main()
