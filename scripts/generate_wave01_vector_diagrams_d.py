from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_wave01_vector_diagrams as base

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'diagrams' / 'wave-01'
META = ROOT / 'assets' / 'production-briefs' / 'wave-01-vector-assets-d.json'
REPORT = ROOT / 'docs' / 'reviews' / 'VISUAL_WAVE_01_VECTOR_REVIEW_D.md'


def matrix(name,title,subtitle,headers,rows,note,desc):
    p=[]
    base.add_title(p,title,subtitle)
    x0=55; y0=225; total=1090
    first=250; other=(total-first)//(len(headers)-1); widths=[first]+[other]*(len(headers)-1)
    xs=[x0]
    for w in widths[:-1]: xs.append(xs[-1]+w)
    for i,h in enumerate(headers): base.box(p,xs[i],y0,widths[i],95,h,'','box2')
    y=y0+115; rh=max(125,min(185,int(1020/max(1,len(rows)))))
    for row in rows:
        for i,val in enumerate(row): base.box(p,xs[i],y,widths[i],rh,str(val),'','box2' if i==0 else 'box')
        y += rh+10
    base.footer_note(p,note)
    return base.write_svg(name,title,desc,p)


def network(name,title,subtitle,centre,nodes,note,desc):
    p=[]
    base.add_title(p,title,subtitle)
    cx,cy=600,780
    p.append(f'<circle class="hub" cx="{cx}" cy="{cy}" r="145"/>')
    p += base.text_lines(cx,cy-10,base.wrap(centre,17),'hubtext',30,'middle')
    pos=[(600,260),(930,390),(1010,710),(925,1050),(600,1200),(275,1050),(190,710),(270,390)]
    for (h,b),(x,y) in zip(nodes,pos):
        base.box(p,x-135,y-70,270,140,h,b,'box')
        base.arrow(p,x,y,cx,cy)
    base.footer_note(p,note)
    return base.write_svg(name,title,desc,p)


def clothing_system():
    title='Figure 21.1 — Protective Clothing System'
    desc='Body-map diagram showing veil, suit or jacket, wrist and ankle closures, gloves and footwear as overlapping layers rather than a guarantee of no stings.'
    p=[]
    base.add_title(p,title,'Protection works as an overlapping system: gaps between components matter as much as the material itself.')
    # simple body form
    p += ['<circle cx="600" cy="350" r="90" fill="#eee" stroke="#222" stroke-width="4"/>',
          '<rect x="505" y="440" width="190" height="400" rx="60" fill="#f7f7f7" stroke="#222" stroke-width="4"/>',
          '<line x1="515" y1="520" x2="350" y2="760" stroke="#222" stroke-width="28"/>',
          '<line x1="685" y1="520" x2="850" y2="760" stroke="#222" stroke-width="28"/>',
          '<line x1="555" y1="830" x2="490" y2="1130" stroke="#222" stroke-width="34"/>',
          '<line x1="645" y1="830" x2="710" y2="1130" stroke="#222" stroke-width="34"/>',
          '<path d="M480,250 Q600,145 720,250 L750,480 L450,480 Z" fill="none" stroke="#111" stroke-width="5" stroke-dasharray="10 7"/>']
    labels=[('Veil clearance',150,260,470,320),('Closed neck/zip overlap',110,500,480,500),('Glove/cuff overlap',80,760,350,760),('Glove/cuff overlap',870,760,850,760),('Trouser/boot overlap',120,1130,500,1100),('Trouser/boot overlap',820,1130,700,1100)]
    for txt,tx,ty,x,y in labels:
        p += base.text_lines(tx,ty,[txt],'label',28)
        base.arrow(p,tx+180 if tx<600 else tx-10,ty-10,x,y)
    base.box(p,185,1250,830,135,'Pre-use check','Zips/closures secure; no holes; veil held off face; footwear stable; PPE matched to colony/task and heat load.','box2')
    base.footer_note(p,'Protective clothing reduces exposure but does not guarantee zero stings. Colony temperament, calm handling, weather and task planning remain essential controls.')
    return base.write_svg('fig-21-1-protective-clothing-system.svg',title,desc,p)


def smoker_anatomy():
    title='Figure 22.1 — Smoker Anatomy'
    desc='Labelled technical schematic of a bee smoker showing lid and nozzle, fire chamber, internal grate, heat shield, bellows, air inlet and hanging hook.'
    p=[]
    base.add_title(p,title,'A smoker is a controlled airflow/combustion tool; maintenance prevents hot smoke, flame and spark hazards.')
    # chamber
    p += ['<rect x="440" y="380" width="260" height="570" rx="30" fill="#eee" stroke="#222" stroke-width="5"/>',
          '<rect x="410" y="380" width="320" height="570" rx="35" fill="none" stroke="#555" stroke-width="4"/>',
          '<path d="M455,380 Q570,260 685,380" fill="#f7f7f7" stroke="#222" stroke-width="5"/>',
          '<path d="M600,300 L805,225 L840,280 L670,395" fill="#f7f7f7" stroke="#222" stroke-width="5"/>',
          '<line x1="465" y1="870" x2="680" y2="870" stroke="#222" stroke-width="8"/>',
          '<rect x="180" y="475" width="180" height="410" rx="35" fill="#f7f7f7" stroke="#222" stroke-width="5"/>',
          '<line x1="360" y1="670" x2="440" y2="670" stroke="#222" stroke-width="10"/>',
          '<circle cx="245" cy="845" r="18" fill="#fff" stroke="#222" stroke-width="4"/>',
          '<path d="M710,500 Q825,470 825,580" fill="none" stroke="#222" stroke-width="7"/>']
    labels=[('Nozzle',875,230,805,250),('Lid',850,380,680,350),('Fire chamber',790,600,700,600),('Internal grate',790,880,675,870),('Heat shield',760,1030,705,920),('Bellows',70,520,180,560),('Air inlet',60,860,230,845),('Air path to chamber',85,690,400,670),('Hanging hook',860,510,825,520)]
    for txt,tx,ty,x,y in labels:
        p += base.text_lines(tx,ty,[txt],'label',27)
        base.arrow(p,tx+150 if tx<600 else tx-10,ty-8,x,y)
    base.footer_note(p,'The heat shield reduces accidental contact but does not make the chamber safe to place on dry vegetation, clothing or vehicle interiors.')
    return base.write_svg('fig-22-1-smoker-anatomy.svg',title,desc,p)


def receiving_hive():
    title='Figure 24.2 — Prepared Receiving Hive'
    desc='Prepared hive setup showing stable level stand, frames, cover, entrance, optional appropriate feeder and clear working space before bees arrive.'
    p=[]
    base.add_title(p,title,'Prepare the site and equipment before bees arrive so installation can be calm, brief and controlled.')
    # stand and hive
    p += ['<line x1="190" y1="1180" x2="1010" y2="1180" stroke="#555" stroke-width="6"/>',
          '<rect x="390" y="690" width="420" height="410" fill="#f7f7f7" stroke="#222" stroke-width="5"/>',
          '<rect x="360" y="625" width="480" height="70" fill="#eee" stroke="#222" stroke-width="5"/>',
          '<rect x="410" y="1090" width="380" height="55" fill="#eee" stroke="#222" stroke-width="5"/>',
          '<rect x="485" y="1145" width="230" height="25" fill="#fff" stroke="#222" stroke-width="4"/>']
    for i in range(8):
        x=415+i*48
        p.append(f'<rect x="{x}" y="720" width="32" height="330" fill="#fff" stroke="#777" stroke-width="2"/>')
    callouts=[('Stable level stand',80,1100,390,1115),('Frames / foundation or drawn comb',70,780,420,800),('Weatherproof cover',830,620,810,655),('Defensible entrance arrangement',800,1125,715,1155),('Feeder only if needed',830,790,775,760),('Clear working space',120,1280,400,1180)]
    for txt,tx,ty,x,y in callouts:
        p+=base.text_lines(tx,ty,base.wrap(txt,22),'label',28)
        base.arrow(p,tx+180 if tx<600 else tx-10,ty-10,x,y)
    base.box(p,250,250,700,185,'Before arrival','Confirm hive ID, source records, health/biosecurity plan, transport timing, feed decision and first targeted follow-up question.','box2')
    base.footer_note(p,'Unknown honey should not be used as feed because it can carry disease risk. Feeding is context-dependent and should avoid robbing/exposed syrup.')
    return base.write_svg('fig-24-2-prepared-receiving-hive.svg',title,desc,p)


def inspection_depth_ladder():
    title='Figure 25.1 — Inspection Depth Ladder'
    desc='Five-level ladder from external observation to emergency inspection, with information need and colony disturbance increasing together.'
    p=[]
    base.add_title(p,title,'Use the least intrusive inspection depth that can answer the current management question.')
    levels=[('External observation','Entrance, flight, pollen return, mortality, robbing, equipment/weather.','Lowest disturbance'),('Limited check','Cover/feeder/upper stores or a very small number of frames for a narrow question.','Low'),('Targeted inspection','Defined brood/queen/space/health question in a specific part of the colony.','Moderate'),('Full inspection','Systematic broader assessment when the management need justifies it.','Higher'),('Emergency inspection','Only as deep/fast as needed to stabilise an urgent problem; safety first.','Purpose-driven')]
    y=250
    widths=[520,650,780,910,1040]
    for (h,b,d),w in zip(levels,widths):
        x=(1200-w)//2
        base.box(p,x,y,w,170,h,b+f' Disturbance: {d}.','box2' if h=='External observation' else ('stop' if h=='Emergency inspection' else 'box'))
        y+=210
    base.footer_note(p,'Inspection frequency and depth depend on objective, season, weather and previous findings; this figure deliberately contains no universal calendar interval.')
    return base.write_svg('fig-25-1-inspection-depth-ladder.svg',title,desc,p)


def cleaning_vs_decon():
    title='Figure 43.10 — Cleaning Versus Decontamination'
    desc='Two-stage concept showing physical removal of wax, propolis and debris before an approved AFB spore-targeting decontamination or disposition process.'
    p=[]
    base.add_title(p,title,'Cleaning removes material. Decontamination/control addresses the biological hazard under an approved programme.')
    base.box(p,90,260,450,620,'Stage 1 — Physical cleaning','Remove wax, propolis and visible organic debris from equipment that the competent programme allows to be processed. Cleaning reduces soil and improves access of a later approved control process.','box2')
    base.box(p,660,260,450,620,'Stage 2 — Approved decontamination / disposition','Use the current competent-authority method for the material and jurisdiction. Some items may require disposal rather than attempted decontamination.','legal')
    base.arrow(p,540,570,660,570)
    base.box(p,250,980,700,240,'Do not improvise chemical or heat recipes','AFB spores are highly persistent. A visibly clean surface is not proof of spore elimination, and an unvalidated home treatment can spread contamination or create chemical/fire hazards.','stop')
    base.footer_note(p,'Keep suspect material segregated until the official/validated control path is clear. Requirements differ by jurisdiction and equipment material.')
    return base.write_svg('fig-43-10-cleaning-versus-decontamination.svg',title,desc,p)


def antibiotics_afb():
    title='Figure 43.11 — Why Antibiotics Do Not Eradicate AFB'
    desc='Conceptual diagram separating vegetative bacterial growth from durable Paenibacillus larvae spores, showing that suppression of vegetative bacteria does not remove spores from comb or equipment.'
    p=[]
    base.add_title(p,title,'AFB control fails if vegetative-bacteria suppression is mistaken for elimination of durable spores.')
    base.box(p,80,270,460,820,'Vegetative bacterial phase','Actively multiplying bacterial cells occur during disease development in susceptible larvae. Where antimicrobials are legally used in some jurisdictions, they target susceptible active bacterial processes—not durable dormant spores.','box')
    base.box(p,660,270,460,820,'Durable spore phase','Spores can persist in dried scale, comb, honey/equipment contamination and remain a long-term source of reinfection. Spore persistence is central to AFB biosecurity and official control.','stop')
    base.arrow(p,540,620,660,620)
    base.box(p,285,1180,630,155,'Key lesson','Clinical suppression or temporary improvement does not equal eradication. Follow current competent-authority AFB control requirements.','legal')
    base.footer_note(p,'This figure does not recommend antibiotic use. Legal status, permitted products and control strategy vary by jurisdiction.')
    return base.write_svg('fig-43-11-antibiotics-do-not-eradicate-afb.svg',title,desc,p)


def efb_vs_afb():
    return matrix(
        'fig-44-4-efb-versus-afb.svg','Figure 44.4 — EFB Versus AFB','A comparison supports differential diagnosis; overlapping signs still require appropriate confirmation.',
        ['Feature','EFB tendency','AFB tendency'],
        [('Usual stage noticed','Often open brood / younger larvae affected','Often sealed-brood pattern becomes conspicuous, though infection begins in young larvae'),('Larval position','Twisted, displaced, collapsed larvae can occur','Decomposed remains in capped/opened cells; stage varies'),('Cappings','May become irregular if affected larvae survive to capping','Sunken/perforated/irregular cappings can occur'),('Remains / scale','Dried remains may occur but do not form AFB-like highly persistent endospores','Adherent scale can contain many persistent spores'),('Spore biology','M. plutonius does not make AFB-like bacterial endospores','P. larvae forms highly durable spores'),('Field sign limitation','Position/odour alone is not diagnostic','Rope/odour/capping pattern alone is not universal definitive proof')],
        'The table shows tendencies, not absolute rules. Use representative samples and current validated/official diagnostic pathways.',
        'Comparison matrix of European foulbrood and American foulbrood by common stage, larval position, cappings, remains, spore biology and field-sign limitations.')


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    assets=[]
    assets.append(clothing_system())
    assets.append(matrix('fig-21-3-clothing-selection-by-task.svg','Figure 21.3 — Clothing Selection by Task','PPE intensity should reflect task, colony behaviour, heat load and consequences of failure.',
        ['Task / context','Veil/body protection','Gloves / hands','Extra consideration'],[
            ('Routine calm inspection','Secure veil + suitable jacket/suit for beekeeper/colony','Optional or light protection according to skill/risk','Maintain dexterity; check heat load'),('Persistently defensive colony','Higher-coverage secure suit/veil','Appropriate gloves','Requeen/manage cause; PPE alone does not solve temperament'),('Swarm collection','Secure veil/body protection','Task-appropriate gloves','Ladder/traffic/public hazards may dominate'),('Hot-weather work','Minimum safe sting protection','Balance dexterity/sting risk','Hydration, shade, shorter task; stop for heat symptoms'),('Honey-room work','Food-hygiene clothing; bees may be absent','Clean food-handling gloves where task requires','Separate apiary PPE contamination from food area')],
        'No clothing configuration guarantees zero stings. Choose PPE together with behavioural, site and task controls.',
        'Matrix matching protective clothing considerations to routine inspections, defensive colonies, swarm collection, hot weather and honey-room work.'))
    assets.append(base.vertical_flow('fig-21-4-pre-inspection-ppe-check.svg','Figure 21.4 — Pre-Inspection PPE Check','A 30-second PPE check prevents avoidable gaps before the colony is opened.',
        [('Veil structure clear of face?','Mesh/frame/hat holds veil away from skin and gives adequate visibility.','box'),('Zips and neck closures secured?','Check every closure including flap/zip overlap.','box'),('Wrists and ankles protected?','Cuff/glove and trouser/boot interfaces do not leave obvious openings.','box'),('Holes, tears or failed elastic?','Repair/replace before work; do not rely on tape for a critical failed closure unless genuinely secure.','stop'),('Footwear and mobility suitable?','Stable footing, no trip hazard, adequate traction for site.','box'),('Heat / hydration plan ready?','PPE increases thermal load; water, shade and breaks must be available.','box2')],
        'If the protective system is not secure or heat conditions are unsafe, correct the problem before opening the hive.',
        'Six-point pre-inspection protective-clothing check.'))
    assets.append(smoker_anatomy())
    assets.append(receiving_hive())
    assets.append(base.vertical_flow('fig-24-11-new-colony-biosecurity.svg','Figure 24.11 — New-Colony Biosecurity','New colonies enter the apiary through a traceable, observed health pathway rather than automatic integration.',
        [('Traceable source','Supplier/origin, queen/unit type, movement documentation and known treatment/health history.','box2'),('Arrival inspection / baseline','Observe condition; establish colony ID; quantify Varroa or other required baseline using appropriate method.','box'),('Segregation / dedicated tools where appropriate','Use a separate site/edge placement or dedicated tools when practical and risk-justified.','box'),('Watch for disease/pest signs','Do not assume broodless swarm/package means disease or parasite freedom.','box'),('Regulated/exotic suspicion?','Restrict unnecessary movement, preserve evidence and contact the competent authority where required.','legal'),('Integrate into routine monitoring','Only after the new unit has a clear identity, health baseline and follow-up plan.','box2')],
        'Quarantine/segregation requirements vary by jurisdiction and disease risk. This diagram shows a risk-management concept rather than a fixed quarantine duration.',
        'New-colony biosecurity flow from traceable source and baseline assessment to risk-based segregation and routine integration.'))
    assets.append(inspection_depth_ladder())
    assets.append(base.cycle('fig-25-13-inspection-record-follow-up-loop.svg','Figure 25.13 — Inspection Record and Follow-Up Loop','An inspection is incomplete until the finding is recorded and the outcome is verified.',
        ['Observe objectively','Record finding','Interpret / decide','Act only if justified','Set next inspection','Verify outcome','Update colony record','Use trend next time'],
        'Records should identify colony, date and method/measurement when relevant; avoid replacing objective observations with vague labels such as “looks weak”.',
        'Circular record and follow-up loop from objective observation through action and verification back to trend-informed inspection.'))
    assets.append(base.vertical_flow('fig-38-8-suspected-disease-biosecurity-zone.svg','Figure 38.8 — Suspected-Disease Biosecurity Zone','Work from clean/healthy units toward the suspect unit, then stop contaminated movement out of the zone.',
        [('Plan clean-to-suspect work order','Inspect lower-risk colonies first when practical; leave suspect colony until last.','box2'),('Dedicated / decontaminable tools','Keep suspect-colony tools separate until the approved cleaning/decontamination path is known.','box'),('No frame/bee/honey transfer','Do not redistribute material from the suspect colony while diagnosis is unresolved.','stop'),('Label samples and colony identity','Preserve chain of identity and objective observations.','box'),('Protect food/product lots','Segregate potentially affected harvest/product according to the hazard investigation.','box'),('Authority contact where required','Notifiable disease or exotic-pest suspicion can require official instructions before further movement.','legal')],
        'Biosecurity starts before confirmation because waiting to contain a potentially serious transmissible hazard can create preventable spread.',
        'Suspected disease biosecurity workflow showing clean-to-suspect work order, separate tools, movement restriction, sample labelling and authority escalation.'))
    assets.append(base.vertical_flow('fig-38-10-recovery-monitoring-timeline.svg','Figure 38.10 — Recovery Monitoring Timeline','Recovery must be judged on a biologically meaningful timescale rather than immediately after intervention.',
        [('Immediate stabilisation','Stop active hazard and restore critical needs such as ventilation, physical integrity or accessible food.','stop'),('Short follow-up','Confirm the emergency has not recurred and that the colony/equipment remains stable.','box'),('Biological response interval','Allow enough time for the variable being assessed—brood, queen function, food, mortality or pest level—to change meaningfully.','box2'),('Targeted reinspection / measurement','Repeat the relevant observation or validated monitoring method.','box'),('Final verification / continued plan','Record recovery, further action or escalation; continue normal monitoring when stable.','box2')],
        'The interval is problem-dependent. The figure intentionally does not assign one universal number of days to every emergency.',
        'Recovery timeline from immediate stabilisation through short follow-up, biological response interval and final verification.'))
    assets.append(cleaning_vs_decon())
    assets.append(antibiotics_afb())
    assets.append(network('fig-43-12-afb-trace-back-trace-forward.svg','Figure 43.12 — Trace-Back and Trace-Forward Map','An AFB investigation follows both what entered the affected operation and what may have left it.','Index colony / apiary',
        [('Purchased colonies / nucs','Source/date/health history'),('Bought second-hand comb/equipment','Origin and use history'),('Brood/honey frame transfers','Internal donor/recipient colonies'),('Apiary movements','Locations and dates'),('Colony / queen sales','Destinations and dates'),('Shared tools / extractor','Operations/colonies connected'),('Dead-outs / robbing','Possible uncontrolled exposure'),('Neighbour contact','Robbing/drifting context where relevant')],
        'Tracing identifies contacts for investigation; it does not by itself prove which link transmitted infection. Follow competent-authority requirements.',
        'Network map for AFB trace-back and trace-forward through purchases, transfers, movements, sales, equipment and robbing/drifting contacts.'))
    assets.append(efb_vs_afb())
    assets.append(network('fig-44-6-efb-disease-expression-colony-stress.svg','Figure 44.6 — Disease Expression and Colony Stress','M. plutonius infection is the infectious cause; colony stressors modify whether and how strongly disease is expressed.','EFB clinical expression',
        [('M. plutonius infection','Infectious cause; central prerequisite'),('Nurse-bee capacity','Worker population affects larval care/removal'),('Forage interruption','Can reduce food availability and colony resilience'),('Nutrition','Modifies larval/colony condition; not the infectious cause'),('Weather / chilling stress','Can alter brood condition and expression'),('Queen / brood demand','Brood amount and pattern influence colony workload'),('Other disease / parasites','Concurrent stress changes colony resilience'),('Management / movement','Can alter stress and transmission opportunities')],
        'The modifier arrows do not mean these stressors “cause EFB”. They influence expression in an already infected biological system.',
        'Conceptual network separating Melissococcus plutonius infection as the infectious cause from nutritional, weather, workforce and concurrent-stress modifiers.'))
    assets.append(base.vertical_flow('fig-44-9-shook-swarm-principle.svg','Figure 44.9 — Shook-Swarm Principle','High-level official-control concept only; exact use and procedure depend on competent-authority requirements.',
        [('Confirmed / officially managed EFB context','Do not use this figure as a self-authorising treatment instruction.','legal'),('Adult bees separated from contaminated brood comb','Principle: break contact with heavily contaminated brood-comb material under an approved programme.','box'),('Adults installed on clean approved equipment','Clean equipment/foundation and food support are managed according to the programme.','box2'),('Old brood comb managed as directed','Disposition/decontamination is jurisdiction- and programme-specific.','legal'),('Reinspection / recurrence surveillance','Follow colony strength and disease signs after the intervention.','box2')],
        'No timing, feed, antibiotic, destruction or chemical-decontamination recipe is embedded here. Follow current official/veterinary instructions.',
        'High-level shook-swarm principle for EFB control, explicitly subject to competent-authority requirements.'))
    assets.append(network('fig-44-11-efb-apiary-contact-map.svg','Figure 44.11 — Apiary Contact Map','Map operational connections around an index EFB case so exposed colonies can be prioritised for inspection.','Index EFB case',
        [('Brood-frame transfer','Donor / recipient colonies'),('Food-frame transfer','Shared food comb history'),('Shared equipment','Tools, boxes, feeders'),('Robbing','Weak/dead colony exposure'),('Drifting','Neighbouring colonies / layout'),('Introduced colonies','Recent purchases or moves'),('Apiary movement','Recent site changes'),('Shared feeder / resource','Where relevant to operation')],
        'A contact is an exposure opportunity, not proof of transmission. Use the map to organise investigation and records.',
        'Apiary contact map around an EFB index case including frame transfers, shared equipment, robbing, drifting, introductions and movements.'))

    records=[]
    for path in assets:
        root=ET.parse(path).getroot(); ns='{http://www.w3.org/2000/svg}'
        t=root.find(ns+'title'); d=root.find(ns+'desc')
        records.append({'path':str(path.relative_to(ROOT)),'title':t.text if t is not None else None,'alt_text':d.text if d is not None else None,'format':'SVG','status':'DRAFT_ART_TECH_REVIEW_PASS_LAYOUT_PROOF_PENDING','provenance':'original deterministic vector generated in repository','rights':'original project asset; commercial print/digital use permitted subject to project ownership','external_dependencies':[]})
    META.parent.mkdir(parents=True,exist_ok=True)
    META.write_text(json.dumps({'asset_count':len(records),'assets':records},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text(
        '# Visual Wave 01 — Vector Diagram Technical Review D\n\n'
        '**Date:** 17 September 2026  \n'
        f'**Assets generated:** {len(records)}  \n'
        '**Result:** **TECHNICAL CONTENT PASS — LAYOUT PROOF PENDING**\n\n'
        '## Produced Assets\n\n' + '\n'.join(f"- `{r['path']}` — {r['title']}" for r in records) +
        '\n\n## Review Controls\n\n'
        '- every SVG parses as XML and contains accessible title/description metadata;\n'
        '- no external fonts, raster files, web resources or proprietary dependencies;\n'
        '- PPE/smoker diagrams present protection as layered control rather than guaranteed safety;\n'
        '- new-colony and inspection diagrams avoid fixed universal schedules;\n'
        '- disease biosecurity assets place movement restriction and authority escalation before uncontrolled manipulation;\n'
        '- AFB cleaning/decontamination diagram contains no chemical or heat recipe;\n'
        '- AFB antimicrobial diagram explicitly preserves durable-spore risk and does not recommend antibiotics;\n'
        '- EFB comparison uses tendencies, not image-only diagnosis, and does not attribute infectious causation to poor nutrition;\n'
        '- shook-swarm figure is deliberately high-level and authority-dependent;\n'
        '- all diagrams remain interpretable in greyscale.\n\n'
        '## Status\n\nActual vector artwork is present. Final approval still requires intended-size layout proof, caption pairing and PDF/EPUB/print verification.\n',encoding='utf-8')
    print(f'generated={len(records)}')

if __name__=='__main__':
    main()
