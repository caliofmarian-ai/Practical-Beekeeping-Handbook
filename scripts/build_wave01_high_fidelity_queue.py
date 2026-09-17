from pathlib import Path
import csv
import json
import re

ROOT=Path(__file__).resolve().parents[1]
QUEUE=ROOT/'assets'/'production-briefs'/'wave-01-bee-health-safety.json'
DIAGRAMS=ROOT/'assets'/'diagrams'/'wave-01'
OUT_JSON=ROOT/'assets'/'production-briefs'/'wave-01-high-fidelity.json'
OUT_CSV=ROOT/'assets'/'production-briefs'/'wave-01-high-fidelity.csv'
OUT_MD=ROOT/'assets'/'production-briefs'/'wave-01-high-fidelity.md'
REPORT=ROOT/'docs'/'reviews'/'VISUAL_WAVE_01_FINAL_COVERAGE.md'

PHOTO_PREFERRED_TERMS=('brood reference','affected open brood','disease-stage','varroa on adult','deformed','phenotype','clinical signs')
ILLUSTRATION_PREFERRED_TYPES={'anatomical','life_cycle','technical_cutaway'}


def main():
    data=json.loads(QUEUE.read_text(encoding='utf-8'))
    produced=set()
    for p in DIAGRAMS.glob('fig-*.svg'):
        m=re.match(r'fig-(\d+)-(\d+)-',p.name)
        if m: produced.add(f"{int(m.group(1))}.{int(m.group(2))}")
    remaining=[]
    for a in data['assets']:
        if a['figure_id'] in produced: continue
        x=dict(a)
        title=a['working_title'].lower(); vt=a.get('visual_type','')
        if any(t in title for t in PHOTO_PREFERRED_TERMS):
            medium='AUTHENTIC_RIGHTS_CLEARED_PHOTO_OR_TECHNICAL_COMPARISON_PLATE'
        elif vt in ILLUSTRATION_PREFERRED_TYPES or any(t in title for t in ('mite','midgut','brood','larva','cell','life cycle')):
            medium='HIGH_FIDELITY_ORIGINAL_TECHNICAL_ILLUSTRATION'
        else:
            medium='HIGH_FIDELITY_TECHNICAL_ILLUSTRATION_OR_PHOTO'
        x['recommended_medium']=medium
        x['asset_status']='BRIEF_READY_HIGH_FIDELITY_ASSET_NOT_YET_CREATED'
        x['reference_requirements']=[
            'source chapter final text', 'chapter illustration plan',
            'scientific/diagnostic source references',
            'scale or magnification cue where size can be misunderstood',
            'diagnostic limitation in caption where appearance is non-specific'
        ]
        x['approval_gates']=[
            'manuscript alignment','scientific morphology/anatomy accuracy',
            'diagnostic limitation review','safety/legal review',
            'commercial rights/provenance','greyscale/final-size legibility',
            'alt text/accessibility','final layout proof'
        ]
        remaining.append(x)

    planned=len(data['assets']); covered=planned-len(remaining)
    OUT_JSON.parent.mkdir(parents=True,exist_ok=True)
    OUT_JSON.write_text(json.dumps({'planned_core_assets':planned,'actual_asset_ids_present':covered,'remaining_high_fidelity_assets':len(remaining),'assets':remaining},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    fields=['production_order','asset_id','figure_id','chapter','chapter_title','working_title','visual_type','recommended_medium','source_plan','asset_status']
    with OUT_CSV.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for r in remaining: w.writerow({k:r.get(k) for k in fields})
    md=['# Wave 01 — High-Fidelity Biological / Diagnostic Asset Queue','',f'**Remaining A_CORE assets:** {len(remaining)}','',
        'These items are intentionally withheld from low-detail deterministic SVG treatment. They require morphology, anatomy, microscopic structure, disease-sign nuance or authentic field appearance that must survive expert review.','']
    for r in remaining:
        md += [f"## {r['production_order']}. Figure {r['figure_id']} — {r['working_title']}",'',f"- Chapter: {r['chapter']} — {r['chapter_title']}",f"- Type: `{r['visual_type']}`",f"- Recommended medium: `{r['recommended_medium']}`",f"- Source plan: `{r['source_plan']}`",f"- Brief: {r['brief']}",'- Status: `BRIEF_READY_HIGH_FIDELITY_ASSET_NOT_YET_CREATED`','']
    OUT_MD.write_text('\n'.join(md),encoding='utf-8')

    chapter={}
    for a in data['assets']:
        c=chapter.setdefault(a['chapter'],{'planned':0,'present':0,'remaining':0})
        c['planned']+=1
        if a['figure_id'] in produced:c['present']+=1
        else:c['remaining']+=1
    lines=['# Visual Wave 01 — Final Coverage and High-Fidelity Handoff','', '**Date:** 17 September 2026  ',
           '**Result:** **ALL DETERMINISTIC VECTOR CANDIDATES PRODUCED — HIGH-FIDELITY SET ISOLATED**','',
           '## Coverage','',f'- A_CORE briefs: **{planned}**',f'- A_CORE Figure IDs with an actual SVG asset: **{covered}**',f'- remaining high-fidelity biological/diagnostic assets: **{len(remaining)}**','',
           '| Chapter | A_CORE | Actual SVG present | High-fidelity remaining |','|---:|---:|---:|---:|']
    for ch in sorted(chapter):
        c=chapter[ch]; lines.append(f"| {ch} | {c['planned']} | {c['present']} | {c['remaining']} |")
    lines += ['','## Why the Remaining Set Is Separate','',
              'The remaining items are dominated by brood/disease appearances, mite morphology, life cycles, anatomy and microscopic concepts. Producing them as generic low-detail schematics would risk teaching incorrect morphology or turning suggestive signs into apparent diagnostic proof.','',
              'They are therefore routed to specialised original technical illustration or authentic rights-cleared photography, with explicit scale, provenance and diagnostic-limitation review.','',
              '## Deliverables','',
              '- `assets/production-briefs/wave-01-high-fidelity.md`',
              '- `assets/production-briefs/wave-01-high-fidelity.json`',
              '- `assets/production-briefs/wave-01-high-fidelity.csv`','',
              '## Status Rule','',
              'The existing SVGs are real artwork but remain layout-proof pending. The high-fidelity queue remains unproduced until actual original/licensed assets pass the full visual gates. No placeholder is counted as complete.','']
    REPORT.parent.mkdir(parents=True,exist_ok=True); REPORT.write_text('\n'.join(lines),encoding='utf-8')
    print(f'planned={planned} present={covered} remaining={len(remaining)}')

if __name__=='__main__': main()
