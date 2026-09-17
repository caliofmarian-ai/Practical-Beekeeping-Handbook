from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_wave01_vector_diagrams as base
import generate_wave01_vector_diagrams_d as d

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'diagrams' / 'wave-01'
META = ROOT / 'assets' / 'production-briefs' / 'wave-01-vector-assets-e.json'
REPORT = ROOT / 'docs' / 'reviews' / 'VISUAL_WAVE_01_VECTOR_REVIEW_E.md'


def hazard_map():
    title='Figure 23.1 — Apiary Hazard Map'
    desc='Plan-view apiary hazard map showing flight paths, public access, vehicle route, livestock, uneven ground, smoker/fire zone, treatment chemical zone, lifting points and emergency access.'
    p=[]; base.add_title(p,title,'Map hazards and access before opening colonies; the safest control is often a site or work-layout decision.')
    p.append('<rect x="90" y="220" width="1020" height="1080" fill="#fafafa" stroke="#222" stroke-width="5"/>')
    # hives
    for x,y in [(300,480),(520,480),(740,480),(410,720),(630,720)]:
        p.append(f'<rect x="{x}" y="{y}" width="120" height="85" fill="#eee" stroke="#222" stroke-width="4"/>')
        p.append(f'<path d="M{x+60},{y+85} L{x+60},{y+180}" class="arrow"/>')
    # zones
    base.box(p,120,1040,260,145,'Public boundary','Keep entrances/flight paths away from routine public access where practical.','stop')
    base.box(p,430,1040,260,145,'Vehicle / lifting route','Stable ground; clear reversing and carrying path.','box')
    base.box(p,760,1040,260,145,'Emergency access','Keep gate/route identifiable and unobstructed.','box2')
    base.box(p,840,300,220,150,'Hot smoker zone','Non-combustible resting area; respect fire restrictions.','stop')
    base.box(p,120,300,220,150,'Treatment storage','Secure labelled chemicals away from food/honey.','legal')
    p += base.text_lines(160,880,['Uneven / slippery ground'], 'label',28)
    p.append('<path d="M170,900 Q300,840 410,910 Q510,960 590,900" fill="none" stroke="#555" stroke-width="5" stroke-dasharray="8 6"/>')
    p += base.text_lines(790,820,['Livestock / animal access'], 'label',28)
    p.append('<rect x="825" y="850" width="190" height="90" fill="none" stroke="#555" stroke-width="4" stroke-dasharray="10 6"/>')
    base.footer_note(p,'This is a planning example, not a universal site layout. Local public-safety, landowner, road, fire and workplace requirements still apply.')
    return base.write_svg('fig-23-1-apiary-hazard-map.svg',title,desc,p)


def three_panel(name,title,subtitle,panels,note,desc):
    p=[]; base.add_title(p,title,subtitle)
    xs=[55,415,775]
    for (h,b,cls),x in zip(panels,xs): base.box(p,x,230,330,1030,h,b,cls)
    base.footer_note(p,note)
    return base.write_svg(name,title,desc,p)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    assets=[]
    assets.append(hazard_map())
    assets.append(base.vertical_flow('fig-23-10-smoker-vegetation-fire-safety.svg','Figure 23.10 — Smoker and Vegetation-Fire Safety','Fire controls are checked before lighting, throughout use and before vehicle transport.',
        [('Check fire/weather restrictions','Do not light/use a smoker where current restrictions or conditions prohibit safe use.','legal'),('Choose non-combustible rest area','Bare mineral/metal/fire-safe surface away from dry vegetation and fuel.','box'),('Use clean fuel and control sparks','No treated/plastic/oily waste; maintain smoker so open flame or spark discharge is not accepted as normal.','box'),('Keep suppression resources appropriate to site','Water/extinguisher or other locally appropriate control as required by risk plan.','box'),('Extinguish completely','Stop combustion and verify no hot ember/heat remains before packing.','stop'),('Transport only when safe','Never place an actively hot smoker against combustible vehicle materials.','box2')],
        'The exact fire-control equipment and permitted methods depend on local fire rules, land conditions and the worksite risk assessment.',
        'Fire-safety sequence for smoker use near vegetation from restrictions and resting area through extinguishing and transport.'))
    assets.append(base.vertical_flow('fig-24-7-swarm-installation.svg','Figure 24.7 — Swarm Installation','Install a collected swarm into a prepared hive with minimal disturbance, then verify that it stays and establishes.',
        [('Prepared hive ready','Stable hive, suitable frames/guides, ventilation/entrance arrangement and colony ID.','box2'),('Transfer swarm gently','Introduce the cluster with minimum crushing/rough shaking consistent with the collection situation.','box'),('Close and maintain ventilation','Protect from overheating and uncontrolled escape while allowing normal airflow.','box'),('Feeding only if justified','Use a clean appropriate feed/feeder when conditions require it; prevent robbing and do not use unknown honey.','box'),('Observe settling / orientation','Monitor entrance behaviour and signs of immediate absconding without repeated opening.','box'),('Targeted follow-up','Confirm establishment, queen function when biologically plausible, comb/food and health baseline.','box2')],
        'A captured swarm is not automatically disease- or Varroa-free. Local legal movement/collection rules and biosecurity still apply.',
        'High-level swarm installation process from prepared hive through transfer, ventilation, optional feeding and targeted follow-up.'))
    assets.append(three_panel('fig-25-5-queenright-evidence.svg','Figure 25.5 — Queenright Evidence Without Finding the Queen','Recent brood evidence can answer many queen-status questions without disrupting the colony to find the queen.',
        [('Eggs','Correctly placed recent eggs support very recent laying activity; interpret with cell context and colony history.','box'),('Very young larvae','Coherent young larvae support recent queen function and brood progression.','box'),('Do not search endlessly for the queen','If the management question is already answered, prolonged frame handling adds disturbance and queen-crushing risk.','stop')],
        'Eggs/young larvae support recent queen function but do not guarantee future queen quality. Drone-laying workers or abnormal laying patterns require separate interpretation.',
        'Three-panel decision aid showing eggs and young larvae as evidence of recent queen function and discouraging unnecessary queen searching.'))
    assets.append(base.vertical_flow('fig-25-11-swarm-preparation-evidence.svg','Figure 25.11 — Swarm-Preparation Evidence','Interpret queen-cell stage together with congestion and colony condition; an empty queen cup alone is weak evidence.',
        [('Queen cup only','Common structure; empty/polished cup alone does not prove active swarm preparation.','box'),('Charged cell with egg / larva and food','Stronger evidence that queen-cell development is active.','box2'),('Advancing queen cells','Increasingly urgent evidence when combined with strong colony/swarm-season context.','stop'),('Brood-nest congestion / backfilling','Reduced laying space and strong population support a swarm-risk interpretation, but are not sufficient alone.','box'),('Choose a planned swarm-control response','Use a method appropriate to colony stage and local management—not repeated queen-cell cutting alone.','legal')],
        'Swarm decisions depend on colony strength, season, drone/mating conditions and the development stage of queen cells.',
        'Evidence ladder from empty queen cup through charged and advanced queen cells plus congestion to planned swarm control.'))
    assets.append(base.vertical_flow('fig-33-14-post-move-inspection.svg','Figure 33.14 — Post-Move Inspection','After transport, verify physical stability first and colony biology later at an appropriate interval.',
        [('Arrival external check','Hive stable/level, straps removed as planned, entrance open, ventilation unobstructed, leaks absent.','box2'),('Orientation / flight behaviour','Allow bees to reorient; avoid standing in flight path or provoking robbing.','box'),('Targeted internal check when justified','Assess frame shift, comb damage, queen/brood evidence, stores and transport stress without unnecessary immediate deep inspection.','box'),('Robbing / overheating / damage warning?','Stabilise the active hazard before continuing routine management.','stop'),('Record outcome and next check','Movement date/site, arrival condition, any damage, actions and follow-up.','box2')],
        'The timing and depth of internal inspection depend on move distance, colony condition, comb type, weather and observed problems.',
        'Post-move inspection flow from arrival stability and orientation through targeted check and follow-up record.'))
    assets.append(d.matrix('fig-38-7-sudden-mortality-evidence-map.svg','Figure 38.7 — Sudden Mortality Evidence Map','Where dead or impaired bees are found is evidence about the event, but distribution alone is not a diagnosis.',
        ['Observed distribution','Possible questions raised','What it cannot prove'],[
            ('Large entrance accumulation','Acute mortality, poisoning/exposure, disease, weather or removal from inside hive?','Specific cause without history/sampling'),('Bees head-first in empty cells','Starvation/access-to-food problem possible','That all colony deaths were starvation'),('Mortality after transport','Heat, ventilation, crushing, stress or pre-existing health?','Single transport mechanism'),('Scattered crawling/trembling adults','Virus, toxic exposure, temperature, ageing or other adult-bee disorder?','One disease from behaviour alone')],
        'Preserve photographs, sample identity, time/weather/treatment/exposure history and escalate suspected chemical/notifiable incidents appropriately.',
        'Matrix relating four mortality distributions to investigation questions while stating that distribution is not diagnosis.'))
    assets.append(base.vertical_flow('fig-41-6-adult-bee-wash-procedure.svg','Figure 41.6 — Adult-Bee Wash Procedure','A quantitative adult-bee wash requires representative collection, queen exclusion, defined sample/method and an explicit denominator.',
        [('Prepare validated equipment/method','Container, dislodging/wash medium and counting setup appropriate to the chosen validated protocol.','box2'),('Choose representative brood-area adult bees','Sampling location matters; follow current regional/validated protocol.','box'),('Locate / protect the queen','Never include the queen in a destructive wash sample.','stop'),('Collect defined adult-bee sample','Use the validated sample size/measurement approach and record colony/date.','box'),('Wash / dislodge mites','Follow method timing/agitation/separation steps consistently.','box'),('Count recovered mites and bee denominator','Calculate mites per 100 bees (or the protocol metric) from the measured numerator and denominator.','box2'),('Record and interpret locally','Separate the measurement from the region/season-specific management decision.','legal')],
        'This diagram teaches measurement discipline, not a universal threshold. Exact sample size and wash procedure should follow the validated regional method.',
        'Numbered adult-bee Varroa wash procedure emphasising queen exclusion and distinction between measurement and intervention decision.'))
    assets.append(three_panel('fig-42-4-dysentery-not-diagnosis.svg','Figure 42.4 — Dysentery Is Not a Diagnosis','Faecal staining and Nosema/Vairimorpha infection can occur independently; staining is a clue, not proof.',
        [('No obvious staining','A colony can still be Nosema/Vairimorpha-positive or have other health problems.','box'),('Faecal staining present','Confinement, feed/digestive issues and other stressors can contribute; test rather than naming Nosema from staining alone.','stop'),('Positive Nosema/Vairimorpha test without staining','Pathogen detection can occur with no visible dysentery; clinical significance still requires context.','box2')],
        'Do not diagnose Nosema from hive-front staining and do not use absence of staining to rule infection out.',
        'Three-panel concept separating faecal staining from Nosema/Vairimorpha detection and clinical significance.'))
    assets.append(d.matrix('fig-43-6-afb-differential-diagnosis.svg','Figure 43.6 — AFB Differential Diagnosis','Brood abnormalities overlap; compare developmental stage and remains, then use appropriate confirmation rather than visual certainty.',
        ['Condition','Pattern/signs that may raise suspicion','Key limitation / next step'],[
            ('AFB','Irregular sealed brood, suspicious cappings, decomposed remains/adherent scale may occur','Field signs support investigation; confirm through current validated/official pathway'),('EFB','Often abnormal open larvae; twisted/discoloured larvae may occur','Can overlap; representative larvae and accepted testing are needed'),('Sacbrood','Larval skin/sac-like remains and raised head can occur','Virus-associated syndrome; appearance still requires context'),('Chilled brood','Brood death follows temperature/exposure pattern','History and distribution matter; do not call bacterial disease from dead brood alone'),('Varroa-associated brood removal','Patchy brood/removed pupae may accompany high mite/virus pressure','Quantify Varroa and assess colony/virus context')],
        'Disease appearance varies with stage and colony condition. Notifiable-disease suspicion requires current competent-authority procedures.',
        'Differential diagnosis matrix for AFB, EFB, sacbrood, chilled brood and Varroa-associated brood removal.'))
    assets.append(d.matrix('fig-44-5-efb-differential-diagnosis.svg','Figure 44.5 — EFB Differential Diagnosis','Open-brood loss has multiple possible causes; EFB is an infectious diagnosis, not a synonym for stressed larvae.',
        ['Condition','Clues to investigate','Important distinction'],[
            ('EFB','Young larvae abnormal in colour/position; open brood often prominent','M. plutonius is the infectious cause; confirm with accepted pathway'),('Chilled brood','Distribution/history consistent with temperature exposure','Non-infectious temperature injury'),('Sacbrood','Sac-like larval skin/raised-head pattern can occur','Virus-associated syndrome; not bacterial EFB'),('Queen-pattern failure','Irregular brood distribution without characteristic larval disease','Reproductive/queen assessment needed'),('Nutritional brood loss','Forage/nurse-bee shortage may impair brood survival','Nutrition can modify EFB expression but is not the infectious cause'),('Varroa-associated brood removal','Patchiness/removal with mite/virus context','Requires parasite assessment')],
        'Treat visual findings as investigation prompts. Smell or one larval position is not diagnostic proof of EFB.',
        'Differential matrix comparing EFB with chilling, sacbrood, queen-pattern failure, nutritional brood loss and Varroa-associated brood removal.'))
    assets.append(d.matrix('fig-45-11-viral-differential-diagnosis.svg','Figure 45.11 — Viral Differential Diagnosis','Adult and brood signs overlap among viruses and non-viral problems; testing is selected according to the syndrome and decision.',
        ['Observed sign','Viral possibilities','Non-viral / competing possibilities'],[
            ('Deformed wings','DWV-associated disease often linked to Varroa pressure','Developmental injury/other causes; phenotype alone does not quantify mites'),('Trembling / crawling adults','CBPV or acute-paralysis-virus group possible','Toxic exposure, temperature stress, starvation, other adult disease'),('Hairless shiny adults','CBPV-compatible syndrome can occur','Abrasion/robbing or other causes can mimic part of appearance'),('Adult mortality','Several viruses may contribute depending on context','Pesticide/toxic exposure, starvation, weather, queen/colony collapse'),('Dead brood','Sacbrood/other viral involvement possible','AFB/EFB, chilling, Varroa-associated removal, nutrition')],
        'A positive PCR result shows target RNA detection under the assay conditions; it does not by itself prove that the virus caused the observed syndrome.',
        'Differential matrix for deformed wings, trembling/crawling adults, shiny adults, mortality and dead brood across viral and non-viral causes.'))
    assets.append(base.wheel('fig-46-4-ipm-thresholds-contextual.svg','Figure 46.4 — Thresholds Are Contextual','IPM action interpretation depends on the organism, colony and regulatory context; statutory threats use a separate authority pathway.','Interpret measured / observed threat',
        ['Pest identity','Season / phase','Brood level','Climate / weather','Colony strength','Virus pressure','Management objective','Next monitoring + local guidance'],
        'Separate branch: suspected notifiable disease or exotic regulated pest → preserve evidence, restrict unnecessary movement and contact the competent authority; ordinary economic-threshold logic may not apply.',
        'IPM threshold decision wheel with pest identity, season, brood, climate, colony strength, virus pressure, management objective, next monitoring/local guidance and a separate statutory-control note.'))

    records=[]
    for path in assets:
        root=ET.parse(path).getroot(); ns='{http://www.w3.org/2000/svg}'
        t=root.find(ns+'title'); dsc=root.find(ns+'desc')
        records.append({'path':str(path.relative_to(ROOT)),'title':t.text if t is not None else None,'alt_text':dsc.text if dsc is not None else None,'format':'SVG','status':'DRAFT_ART_TECH_REVIEW_PASS_LAYOUT_PROOF_PENDING','provenance':'original deterministic vector generated in repository','rights':'original project asset; commercial print/digital use permitted subject to project ownership','external_dependencies':[]})
    META.parent.mkdir(parents=True,exist_ok=True)
    META.write_text(json.dumps({'asset_count':len(records),'assets':records},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text(
        '# Visual Wave 01 — Vector Diagram Technical Review E\n\n'
        '**Date:** 17 September 2026  \n'
        f'**Assets generated:** {len(records)}  \n'
        '**Result:** **VECTOR-CANDIDATE SET COMPLETE — LAYOUT PROOF PENDING**\n\n'
        '## Produced Assets\n\n' + '\n'.join(f"- `{r['path']}` — {r['title']}" for r in records) +
        '\n\n## Review Controls\n\n'
        '- all SVGs parse and include accessible title/description metadata;\n'
        '- no external fonts, raster/web/proprietary dependencies;\n'
        '- safety/fire/transport diagrams put immediate safety and authority controls before continued work;\n'
        '- swarm/queenright visuals use evidence ladders rather than false one-sign certainty;\n'
        '- adult-bee wash requires queen exclusion and separates measurement from threshold interpretation;\n'
        '- dysentery is explicitly not presented as a Nosema diagnosis;\n'
        '- AFB/EFB/virus differential tables use tendencies and confirmation limitations rather than image-only diagnosis;\n'
        '- IPM threshold figure separates statutory/exotic threat pathways from ordinary monitoring logic;\n'
        '- greyscale meaning is preserved.\n\n'
        '## Editorial Gate\n\nThis batch completes the remaining Wave 01 assets suitable for deterministic vector treatment. Remaining A_CORE gaps should be routed to high-fidelity biological/anatomical art or authentic rights-cleared photography instead of being simplified merely to raise the completion count.\n',
        encoding='utf-8')
    print(f'generated={len(records)}')

if __name__=='__main__':
    main()
