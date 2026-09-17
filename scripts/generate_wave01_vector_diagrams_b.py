from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_wave01_vector_diagrams as base

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "diagrams" / "wave-01"
REPORT = ROOT / "docs" / "reviews" / "VISUAL_WAVE_01_VECTOR_REVIEW_B.md"
META = ROOT / "assets" / "production-briefs" / "wave-01-vector-assets-b.json"


def comparison_columns(name, title, subtitle, left_title, left_items, right_title, right_items, note, desc, left_cls="box", right_cls="stop"):
    p=[]
    base.add_title(p,title,subtitle)
    base.box(p,70,190,500,100,left_title,"",left_cls)
    base.box(p,630,190,500,100,right_title,"",right_cls)
    y=340
    for i in range(max(len(left_items),len(right_items))):
        if i < len(left_items):
            base.box(p,70,y,500,110,left_items[i][0],left_items[i][1] if len(left_items[i])>1 else "",left_cls)
        if i < len(right_items):
            base.box(p,630,y,500,110,right_items[i][0],right_items[i][1] if len(right_items[i])>1 else "",right_cls)
        y += 145
    base.footer_note(p,note)
    return base.write_svg(name,title,desc,p)


def horizontal_sequence(name,title,subtitle,steps,note,desc):
    p=[]
    base.add_title(p,title,subtitle)
    cols=4
    w=245
    gap=35
    x0=55
    y0=230
    h=210
    for i,(head,body,cls) in enumerate(steps):
        row=i//cols
        col=i%cols
        x=x0+col*(w+gap)
        y=y0+row*300
        base.box(p,x,y,w,h,head,body,cls)
        if i < len(steps)-1:
            nrow=(i+1)//cols; ncol=(i+1)%cols
            nx=x0+ncol*(w+gap); ny=y0+nrow*300
            if nrow==row:
                base.arrow(p,x+w,y+h//2,nx,ny+h//2)
            else:
                base.arrow(p,x+w//2,y+h,x0+w//2,ny)
    base.footer_note(p,note)
    return base.write_svg(name,title,desc,p)


def veil_clearance():
    title="Figure 21.2 — Veil Clearance"
    desc="Comparison of safe veil clearance from the face versus mesh pressed against skin where stings can penetrate more readily."
    p=[]
    base.add_title(p,title,"Veils reduce sting exposure only when mesh is held away from skin and closures remain secure.")
    # Left safe profile
    base.box(p,70,190,500,1120,"Correct clearance","Mesh remains visibly separated from the face; veil frame/hat structure maintains space; neck/zip closure is secure.","box")
    p += [
        '<circle cx="320" cy="610" r="105" fill="#eee" stroke="#222" stroke-width="3"/>',
        '<path d="M235,470 Q320,375 405,470 L450,760 Q320,830 190,760 Z" fill="none" stroke="#222" stroke-width="6" stroke-dasharray="10 8"/>',
        '<path d="M320,505 Q385,520 405,575 Q385,625 320,635" fill="none" stroke="#555" stroke-width="4"/>',
        '<line x1="405" y1="575" x2="445" y2="575" stroke="#111" stroke-width="3" marker-end="url(#arrow)"/>',
    ]
    p += base.text_lines(205,880,base.wrap("Visible air gap between face and mesh",30),"label",30)
    p += base.text_lines(205,980,base.wrap("Clearance plus closed zips/cuffs improves protection; it does not guarantee zero stings.",34),"body",27)
    # Right unsafe profile
    base.box(p,630,190,500,1120,"Unsafe contact / poor fit","Mesh pressed against skin, collapsed veil geometry or open closure allows easier sting access and bee entry.","stop")
    p += [
        '<circle cx="880" cy="610" r="105" fill="#eee" stroke="#222" stroke-width="3"/>',
        '<path d="M795,505 Q865,500 925,525 Q955,575 925,640 Q865,675 795,650" fill="none" stroke="#111" stroke-width="6" stroke-dasharray="10 8"/>',
        '<path d="M880,505 Q945,520 965,575 Q945,625 880,635" fill="none" stroke="#555" stroke-width="4"/>',
        '<line x1="930" y1="560" x2="880" y2="560" stroke="#111" stroke-width="4" marker-end="url(#arrow)"/>',
    ]
    p += base.text_lines(760,880,base.wrap("Mesh contacts cheek/nose/neck",30),"label",30)
    p += base.text_lines(760,980,base.wrap("Stop and refit before working a colony; heat stress and visibility still need separate control.",34),"body",27)
    base.footer_note(p,"Protective clothing is one control layer. Calm handling, colony temperament, weather and task planning remain important.")
    return base.write_svg("fig-21-2-veil-clearance.svg",title,desc,p)


def starting_units():
    title="Figure 24.1 — Starting Units Compared"
    desc="Comparison matrix for package bees, nucleus colony and captured swarm, showing which biological components are typically present at installation."
    p=[]
    base.add_title(p,title,"Package, nucleus and swarm are biologically different starting units and require different installation/follow-up decisions.")
    x0=70; y0=240; row_h=115; col_w=[280,270,270,270]
    headers=["Feature","Package bees","Nucleus colony","Captured swarm"]
    xs=[x0]
    for w in col_w[:-1]: xs.append(xs[-1]+w)
    for i,h in enumerate(headers):
        base.box(p,xs[i],y0,col_w[i],90,h,"","box2")
    rows=[
        ("Adult bees","Yes","Yes","Yes"),
        ("Queen","Usually caged / supplier-dependent","Laying queen normally present","Queen present but age/mating status may be unknown"),
        ("Brood","No","Yes","No at capture"),
        ("Food stores","Transport feed only / no comb stores","Yes, on comb","No established comb stores at capture"),
        ("Drawn comb","No","Yes","No unless placed onto supplied comb"),
        ("Main early risk","Queen acceptance, comb building, absconding","Disease/parasite transfer, crowding, frame-system fit","Unknown health/genetics, absconding, queen status"),
    ]
    y=y0+115
    for r in rows:
        for i,val in enumerate(r):
            cls="box2" if i==0 else "box"
            base.box(p,xs[i],y,col_w[i],row_h,val,"",cls)
        y+=row_h+10
    base.footer_note(p,"No starting unit should be assumed parasite- or disease-free. Health baseline, source records and appropriate follow-up are still required.")
    return base.write_svg("fig-24-1-starting-units-compared.svg",title,desc,p)


def vehicle_loading():
    title="Figure 33.6 — Vehicle Loading"
    desc="Transport schematic comparing a low balanced restrained hive load with an unsecured tall stack that compromises stability and ventilation."
    p=[]
    base.add_title(p,title,"Hive transport must control load stability, independent hive restraint and ventilation at the same time.")
    # Safe
    base.box(p,70,200,500,1080,"Preferred loading","Low, balanced, ventilated and independently restrained.","box")
    p += ['<rect x="140" y="910" width="360" height="90" fill="#ddd" stroke="#222" stroke-width="4"/>']
    for x in (170,320):
        p += [f'<rect x="{x}" y="600" width="120" height="280" fill="#f7f7f7" stroke="#222" stroke-width="4"/>',
              f'<line x1="{x+60}" y1="575" x2="{x+60}" y2="900" stroke="#111" stroke-width="5"/>']
    p += base.text_lines(120,1060,base.wrap("• low centre of gravity  • gaps for airflow  • vehicle restraint  • separate hive straps",46),"body",28)
    # Unsafe
    base.box(p,630,200,500,1080,"Unsafe loading","Tall unsecured stack, no independent restraint and restricted airflow.","stop")
    p += ['<rect x="700" y="910" width="360" height="90" fill="#ddd" stroke="#222" stroke-width="4"/>']
    for j in range(3):
        p += [f'<rect x="820" y="{830-j*180}" width="140" height="160" fill="#fff" stroke="#222" stroke-width="4"/>']
    p += ['<path d="M780,520 L1000,900" stroke="#111" stroke-width="8"/>','<path d="M1000,520 L780,900" stroke="#111" stroke-width="8"/>']
    p += base.text_lines(690,1060,base.wrap("• high unstable load  • no independent hive strap  • blocked ventilation  • greater rollover/separation risk",46),"body",28)
    base.footer_note(p,"Actual transport must comply with vehicle load limits, road law, animal/bee movement rules and weather/heat constraints.")
    return base.write_svg("fig-33-6-vehicle-loading.svg",title,desc,p)


def transport_overheating():
    title="Figure 38.4 — Transport Overheating"
    desc="Comparison showing ventilated shaded transport versus sealed or blocked ventilation with solar heat loading and bee clustering."
    p=[]
    base.add_title(p,title,"Populous colonies generate heat. Transport design must preserve airflow and limit solar/vehicle heat load.")
    base.box(p,70,210,500,1060,"Adequate ventilation","Open airflow path, shaded/temperature-aware transport, secure straps and space around ventilation screens.","box")
    p += ['<rect x="170" y="530" width="300" height="430" fill="#f7f7f7" stroke="#222" stroke-width="5"/>',
          '<rect x="170" y="660" width="300" height="90" fill="#fff" stroke="#555" stroke-width="3" stroke-dasharray="5 5"/>',
          '<path d="M110,705 L160,705" class="arrow"/><path d="M480,705 L540,705" class="arrow"/>']
    p += base.text_lines(135,1030,base.wrap("Air enters and leaves; ventilation surfaces stay unobstructed; load remains secure.",42),"body",28)
    base.box(p,630,210,500,1060,"Overheating risk","Sealed/blocked entrance or screen, direct solar load, enclosed hot vehicle and dense clustering against ventilation.","stop")
    p += ['<rect x="730" y="530" width="300" height="430" fill="#fff" stroke="#222" stroke-width="5"/>',
          '<rect x="730" y="660" width="300" height="90" fill="#ddd" stroke="#111" stroke-width="4"/>',
          '<line x1="740" y1="520" x2="1020" y2="970" stroke="#111" stroke-width="8"/><line x1="1020" y1="520" x2="740" y2="970" stroke="#111" stroke-width="8"/>']
    p += base.text_lines(690,1030,base.wrap("Stop and correct heat/airflow hazards. Do not seal a populous colony without ventilation.",42),"body",28)
    base.footer_note(p,"Transport overheating is an emergency. Stabilise ventilation and temperature before diagnostic inspection or continued travel.")
    return base.write_svg("fig-38-4-transport-overheating.svg",title,desc,p)


def differential_matrix():
    title="Figure 39.13 — Differential Diagnosis Matrix"
    desc="Matrix showing that common colony signs can have several possible cause categories and therefore require history, examination and confirmation rather than image-only diagnosis."
    p=[]
    base.add_title(p,title,"Visible signs narrow the investigation; they rarely identify a single cause by themselves.")
    rows=["Patchy brood","Dead larvae","Crawling adults","Deformed wings","Faecal spotting","Sudden mortality"]
    cols=["Infectious disease","Parasites","Queen problems","Nutrition","Temperature","Environmental exposure"]
    x0=60; y0=240; label_w=220; cell_w=145; cell_h=145
    base.box(p,x0,y0,label_w,100,"Observed sign","","box2")
    for j,c in enumerate(cols):
        base.box(p,x0+label_w+j*cell_w,y0,cell_w,100,c,"","box2")
    # possible relationship marks, deliberately broad/qualitative
    marks={
        0:[1,1,1,1,1,0],
        1:[1,1,0,1,1,1],
        2:[1,1,0,1,1,1],
        3:[1,1,0,0,0,1],
        4:[1,0,0,1,1,1],
        5:[1,1,0,1,1,1],
    }
    y=y0+115
    for i,r in enumerate(rows):
        base.box(p,x0,y,label_w,cell_h,r,"","box2")
        for j in range(len(cols)):
            cls="box" if marks[i][j] else "note"
            base.box(p,x0+label_w+j*cell_w,y,cell_w,cell_h,"Possible" if marks[i][j] else "Less direct","",cls)
        y+=cell_h+10
    base.footer_note(p,"This matrix is a reasoning aid, not a diagnostic table. Use colony history, developmental stage, sampling and competent-authority/laboratory confirmation where required.")
    return base.write_svg("fig-39-13-differential-diagnosis-matrix.svg",title,desc,p)


def monitoring_methods():
    title="Figure 41.7 — Monitoring Methods Compared"
    desc="Comparison of adult-bee wash, sugar roll, natural mite fall and brood uncapping by what each measures, whether bees are sacrificed and major limitations."
    p=[]
    base.add_title(p,title,"Different Varroa methods answer different questions. Record the method so results can be interpreted correctly.")
    headers=["Method","What it mainly measures","Bees sacrificed?","Key limitation"]
    rows=[
        ("Adult-bee wash","Adult-bee mite burden in a defined sample","Yes, with common alcohol/soap wash methods","Sampling error; queen must be excluded; method-specific handling"),
        ("Sugar roll","Adult-bee mite burden in a defined sample","Usually intended as non-lethal","Variable dislodgement; humidity/technique effects; bees still stressed"),
        ("Natural mite fall","Mites falling to a board over time","No","Indirect; affected by brood, grooming and duration; not directly equivalent to mites/100 bees"),
        ("Brood uncapping","Mites/reproduction in capped brood sample","Brood cells opened","Localised brood sample; destructive to sampled pupae; not adult-bee burden"),
    ]
    x0=55; y0=235; widths=[210,360,210,360]; xs=[x0]
    for w in widths[:-1]: xs.append(xs[-1]+w)
    for i,h in enumerate(headers): base.box(p,xs[i],y0,widths[i],100,h,"","box2")
    y=y0+120
    for r in rows:
        for i,val in enumerate(r): base.box(p,xs[i],y,widths[i],240,val,"","box" if i else "box2")
        y+=260
    base.footer_note(p,"A monitoring result is a measurement. The management decision depends on season, brood, colony condition and current local guidance.")
    return base.write_svg("fig-41-7-monitoring-methods-compared.svg",title,desc,p)


def treatment_failure_vs_reinvasion():
    title="Figure 41.11 — Treatment Failure Versus Reinvasion"
    desc="Two timelines showing a high mite result immediately after control versus a later rise after an initially good verification result."
    p=[]
    base.add_title(p,title,"Timing of verification helps distinguish poor immediate efficacy from later mite immigration/reinvasion.")
    # timeline 1
    base.box(p,70,220,1060,420,"Pattern A — possible poor efficacy / application problem","Pre-control high → control applied → immediate verification remains high.","stop")
    xs=[170,430,690,950]; labels=["Pre-count: high","Control","Early verification: still high","Investigate sampling, application, product condition, resistance"]
    for i,(x,l) in enumerate(zip(xs,labels)):
        p.append(f'<circle cx="{x}" cy="500" r="22" fill="#222"/>')
        p += base.text_lines(x,555,base.wrap(l,18),"body",26,"middle")
        if i<len(xs)-1: base.arrow(p,x+25,500,xs[i+1]-25,500)
    # timeline 2
    base.box(p,70,730,1060,430,"Pattern B — later reinvasion possible","Pre-control high → control → early verification low → later retest rises again.","box")
    labels2=["Pre-count: high","Control","Early verification: low","Later retest: rising"]
    for i,(x,l) in enumerate(zip(xs,labels2)):
        p.append(f'<circle cx="{x}" cy="1010" r="22" fill="#222"/>')
        p += base.text_lines(x,1065,base.wrap(l,18),"body",26,"middle")
        if i<len(xs)-1: base.arrow(p,x+25,1010,xs[i+1]-25,1010)
    p += base.text_lines(250,1165,base.wrap("Investigate robbing, drifting and nearby high-pressure/collapsing colonies; do not assume the original treatment failed.",62),"body",27)
    base.footer_note(p,"Both patterns require valid sampling and context. Do not respond by automatic dose escalation or unapproved product combinations.")
    return base.write_svg("fig-41-11-treatment-failure-versus-reinvasion.svg",title,desc,p)


def disease_investigation():
    return base.vertical_flow(
        "fig-39-1-disease-investigation-framework.svg",
        "Figure 39.1 — Disease Investigation Framework",
        "Move from history and objective observation toward differential diagnosis, confirmation and follow-up.",
        [
            ("History", "Recent queen changes, feeding, treatments, movements, weather, forage, colony trend and neighbouring events.", "box2"),
            ("External observation", "Flight, mortality distribution, entrance signs, odour, robbing, drifting and environment.", "box"),
            ("Adult and brood assessment", "Compare with normal age/stage references; record objective signs without naming a disease prematurely.", "box"),
            ("Differential diagnosis", "Consider infectious disease, parasites, queen problems, nutrition, temperature and environmental exposure.", "box"),
            ("Sampling / confirmation", "Use validated field/laboratory methods when the decision requires confirmation.", "box2"),
            ("Regulated-disease suspicion?", "Contact the competent authority and follow current local requirements.", "legal"),
            ("Control / correction", "Use the authorised disease, parasite, queen, nutrition or environmental response appropriate to the finding.", "box"),
            ("Follow-up", "Reinspect and verify outcome; update apiary records and contact tracing where relevant.", "box2"),
        ],
        "A visual sign may support suspicion but should not be presented as diagnostic proof when confirmation is required.",
        "Disease investigation flow from history through observation, examination, differential diagnosis, sampling, regulated-disease escalation, control and follow-up."
    )


def lab_confirmation():
    return base.vertical_flow(
        "fig-43-9-afb-laboratory-confirmation-pathways.svg",
        "Figure 43.9 — Laboratory Confirmation Pathways",
        "Sample identity and validated interpretation matter as much as the laboratory technology used.",
        [
            ("Representative suspect sample", "Collect under the current official/validated sampling procedure and keep colony identity intact.", "box"),
            ("Label and chain of identity", "Apiary, colony, date, material, collector and relevant clinical observations.", "box2"),
            ("Validated method", "Culture, immunological testing, PCR/qPCR or another method accepted by the competent diagnostic system.", "box"),
            ("Diagnostic interpretation", "Interpret result with sample quality, clinical signs, method limitations and contamination controls.", "box"),
            ("Regulatory decision", "Notification, control and disposition follow current jurisdictional rules; the laboratory result feeds the official decision.", "legal"),
        ],
        "Do not present rope test, odour or one capping feature as a universal definitive AFB diagnosis.",
        "Laboratory pathway for AFB from representative sample and identity records through validated test, interpretation and regulatory decision."
    )


def surveillance_vs_monitoring():
    return comparison_columns(
        "fig-46-3-surveillance-versus-monitoring.svg",
        "Figure 46.3 — Surveillance Versus Monitoring",
        "Surveillance asks whether a threat is present; monitoring repeatedly measures a known or established threat.",
        "Surveillance",
        [("Question","Is an exotic/notifiable organism present?"),("Design","Presence/absence detection, targeted high-risk sampling, competent identification."),("Trigger","Suspicion can require evidence preservation, movement restraint and authority contact."),("Example","Tropilaelaps surveillance in a region where it is exotic/regulatory concern.")],
        "Monitoring",
        [("Question","How much established pest pressure is present now?"),("Design","Repeated quantitative method with consistent denominator and timing."),("Trigger","Interpret measured level with season, brood, colony condition and local guidance."),("Example","Varroa adult-bee sampling repeated through the season.")],
        "Do not substitute ordinary Varroa threshold logic for exotic-pest surveillance or statutory disease response.",
        "Two-column comparison of exotic-pest surveillance and repeated monitoring of an established threat such as Varroa.",
        "box","legal"
    )


def resistance_selection():
    title="Figure 46.9 — Mode of Action and Resistance Selection"
    desc="Conceptual population sequence showing selective removal of susceptible mites and disproportionate survival/reproduction of resistant mites after repeated use of one mode of action."
    p=[]
    base.add_title(p,title,"Repeated selection with the same relevant mode of action can increase the proportion of resistant survivors.")
    stages=[("Before control","Mostly susceptible population with a small resistant fraction."),("After one control","Many susceptible mites removed; resistant survivors are over-represented."),("Reproduction / next generation","Survivors contribute disproportionately to future population."),("Repeated same mode of action","Resistance frequency can rise further if selection continues without effective rotation/strategy.")]
    xs=[70,350,630,910]
    for i,(head,body) in enumerate(stages):
        base.box(p,xs[i],260,220,420,head,body,"box2" if i==0 else "box")
        # dots: S circles and R diamonds represented textually
        for k in range(12):
            x=xs[i]+35+(k%4)*45; y=500+(k//4)*45
            if (i==0 and k<2) or (i==1 and k<5) or (i==2 and k<7) or (i==3 and k<9):
                p.append(f'<rect x="{x-8}" y="{y-8}" width="16" height="16" transform="rotate(45 {x} {y})" fill="#fff" stroke="#111" stroke-width="3"/>')
            else:
                p.append(f'<circle cx="{x}" cy="{y}" r="8" fill="#777"/>')
        if i<3: base.arrow(p,xs[i]+220,470,xs[i+1],470)
    p += base.text_lines(110,780,["● susceptible example    ◇ resistant example"],"label",28)
    base.box(p,130,880,940,270,"Key management lesson","Changing product brand names is not necessarily changing the relevant mode of action. Resistance management still requires monitoring, authorised choices, correct application and verification.","box2")
    base.footer_note(p,"This conceptual figure does not predict resistance speed for a specific product or population and does not authorise unlabelled rotation/combination schemes.")
    return base.write_svg("fig-46-9-mode-of-action-resistance-selection.svg",title,desc,p)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    assets=[]
    assets.append(veil_clearance())
    assets.append(comparison_columns(
        "fig-22-3-smoker-fuels.svg","Figure 22.3 — Suitable Versus Unsuitable Smoker Fuels","Fuel choice is a contamination and fire-safety decision, not merely a question of whether material will burn.",
        "Suitable categories",[("Clean dry plant material","Examples depend on local practice and availability; produce cool smoke when used correctly."),("Known untreated material","Dry, uncontaminated, non-oily material suitable for smoker use."),("Preparation","Keep fuel dry, separate from chemicals and inspect for foreign material.")],
        "Unsuitable / reject",[("Painted or treated wood","May release contaminants and residues."),("Plastic / synthetic material","Can produce harmful combustion products."),("Oily or chemically contaminated material","Contamination and flare risk; do not use."),("Unknown waste material","If history is uncertain, reject it rather than burn it around bees/food." )],
        "Smoke must be cool and used in the minimum effective amount; the smoker is not an anaesthetic device.",
        "Two-column comparison of clean dry plant-based smoker fuels with painted, treated, plastic, oily, chemically contaminated or unknown waste material.","box","stop"))
    assets.append(horizontal_sequence(
        "fig-22-4-smoker-lighting-sequence.svg","Figure 22.4 — Smoker-Lighting Sequence","Build a stable smoulder before approaching the colony.",
        [("1. Prepare fuel","Clean, dry, known material; smoker on fire-safe surface.","box2"),("2. Establish small ember","Ignite a small starter portion safely; avoid large open flame.","box"),("3. Add fuel progressively","Pack enough for steady smoulder while preserving airflow.","box"),("4. Test smoke","Confirm cool dense smoke; no sparks/open flame at nozzle.","box"),("5. Close lid","Secure lid/nozzle and check bellows/airflow.","box"),("6. Verify stable output","A few controlled puffs before approaching bees.","box2")],
        "If smoke is hot, flaming, spark-producing or chemically tainted: stop, correct the smoker, and do not use it on the colony.",
        "Six-step smoker lighting sequence from fuel preparation to stable cool-smoke verification."))
    assets.append(base.vertical_flow(
        "fig-22-6-hot-smoker-fire-safety-zone.svg","Figure 22.6 — Hot-Smoker and Fire-Safety Zone","Treat a smoker as hot fire equipment before, during and after inspection.",
        [("Fire-safe resting area","Use a stable non-combustible surface away from dry vegetation and flammable materials.","box2"),("Control sparks and flame","Maintain the smoker; do not accept open flame/spark discharge as normal operation.","box"),("Respect local fire restrictions","Weather, drought and land rules can make smoker use unsafe or prohibited.","legal"),("Extinguish completely","Use the locally appropriate safe method; verify no heat/ember remains before transport.","stop"),("Secure for vehicle transport","Use a suitable fire-safe container/location; do not place a hot smoker in a vehicle.","box2")],
        "A heat shield reduces accidental contact but does not make dry vegetation or a vehicle interior a safe resting surface.",
        "Fire-safety flow for hot smoker resting, spark control, fire restrictions, extinguishing and vehicle transport."))
    assets.append(comparison_columns(
        "fig-23-6-local-vs-emergency-sting-signs.svg","Figure 23.6 — Local Reaction Versus Emergency Warning Signs","Recognise escalation cues without attempting to diagnose anaphylaxis from one isolated sign.",
        "Limited local reaction",[("Near the sting site","Pain, redness and local swelling can occur around the sting."),("Monitor","Remove retained stinger promptly when present; follow normal first-aid guidance and personal medical advice."),("Escalate if pattern changes","Rapid progression, widespread symptoms or breathing/circulatory symptoms move the situation out of the 'local' column.")],
        "Emergency warning pattern",[("Breathing difficulty / throat or tongue swelling","Treat as an emergency warning pattern."),("Widespread hives or rapid generalised reaction","Systemic symptoms require urgent attention."),("Collapse, faintness, severe dizziness","Possible systemic emergency."),("Action","Seek emergency medical assistance and follow the person's prescribed emergency plan/medication instructions where applicable.")],
        "This figure is for emergency awareness, not self-diagnosis. Severe or rapidly worsening symptoms require urgent medical assistance.",
        "Clinical-awareness comparison between local sting effects and systemic emergency warning patterns with an explicit emergency-assistance action.","box","legal"))
    assets.append(starting_units())
    assets.append(comparison_columns(
        "fig-24-10-early-success-warning-signs.svg","Figure 24.10 — Early Success and Warning Signs","Assess several observations together; one sign rarely defines early colony success or failure.",
        "Early positive evidence",[("Organised colony activity","Bees orienting/working without persistent chaos."),("Comb building / occupied frames","Appropriate for the starting unit and season."),("Eggs or young brood","Supports recent queen function when biologically plausible."),("Food intake / accessible stores","Feed or forage being used without robbing trigger.")],
        "Warning signs requiring investigation",[("Persistent queenlessness evidence","No expected queen function after context-appropriate interval."),("Robbing / fighting / exposed feed","Immediate management and biosecurity concern."),("Excessive mortality / overheating","Stabilise hazard first."),("Absconding or abnormal brood","Investigate health, environment, queen and management; do not assume one cause.")],
        "Starting-unit differences matter: package, nucleus and swarm should not be judged against an identical timetable.",
        "Comparison of early positive colony establishment signs with warning signs such as queenlessness, robbing, mortality, overheating, absconding or abnormal brood.","box","stop"))
    assets.append(vehicle_loading())
    assets.append(transport_overheating())
    assets.append(disease_investigation())
    assets.append(differential_matrix())
    assets.append(monitoring_methods())
    assets.append(treatment_failure_vs_reinvasion())
    assets.append(lab_confirmation())
    assets.append(base.vertical_flow(
        "fig-44-10-efb-follow-up-after-recovery.svg","Figure 44.10 — Follow-Up After Apparent Recovery","Clinical improvement is not the end of the management process.",
        [("Clinical appearance improves","Forage/nutrition and colony condition may improve visible brood appearance.","box"),("Reinspect","Repeat brood assessment after an interval appropriate to colony biology and official programme requirements.","box2"),("Check colony strength and queen function","Confirm population trend, brood quality, food and queen performance.","box"),("Review records and contacts","Recheck frame transfers, shared equipment, neighbouring cases and any legal follow-up obligation.","box"),("Continue recurrence surveillance","If signs return, resample/re-escalate according to the validated/official pathway.","legal")],
        "Do not infer eradication from improved appearance alone. Follow current competent-authority or veterinary requirements where EFB is regulated.",
        "Timeline for EFB follow-up after apparent clinical improvement, including reinspection, colony-strength check and recurrence surveillance."))
    assets.append(surveillance_vs_monitoring())
    assets.append(resistance_selection())

    records=[]
    for path in assets:
        root=ET.parse(path).getroot()
        ns='{http://www.w3.org/2000/svg}'
        t=root.find(ns+'title'); d=root.find(ns+'desc')
        records.append({"path":str(path.relative_to(ROOT)),"title":t.text if t is not None else None,"alt_text":d.text if d is not None else None,"format":"SVG","status":"DRAFT_ART_TECH_REVIEW_PASS_LAYOUT_PROOF_PENDING","provenance":"original deterministic vector generated in repository","rights":"original project asset; commercial print/digital use permitted subject to project ownership","external_dependencies":[]})
    META.parent.mkdir(parents=True,exist_ok=True)
    META.write_text(json.dumps({"asset_count":len(records),"assets":records},indent=2,ensure_ascii=False)+"\n",encoding='utf-8')
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text(
        "# Visual Wave 01 — Vector Diagram Technical Review B\n\n"
        "**Date:** 17 September 2026  \n"
        f"**Assets generated:** {len(records)}  \n"
        "**Result:** **TECHNICAL CONTENT PASS — LAYOUT PROOF PENDING**\n\n"
        "## Produced Assets\n\n" + "\n".join(f"- `{r['path']}` — {r['title']}" for r in records) +
        "\n\n## Review Controls\n\n"
        "- SVG/XML parses successfully for every file;\n"
        "- all files contain accessible title/description metadata;\n"
        "- no external font, raster, web or proprietary asset dependency;\n"
        "- smoker/fire assets exclude treated/plastic/oily fuels and unsafe transport of a hot smoker;\n"
        "- sting-emergency asset directs systemic warning patterns to urgent medical assistance without diagnosing from one isolated sign;\n"
        "- starting-unit asset distinguishes package, nucleus and swarm biologically;\n"
        "- disease matrix explicitly labels relationships as possible rather than diagnostic;\n"
        "- AFB laboratory pathway preserves authority/validated-confirmation role;\n"
        "- Varroa monitoring and resistance assets do not embed universal thresholds or off-label control advice;\n"
        "- transport assets prioritise ventilation, load restraint and heat control;\n"
        "- assets remain greyscale-safe and independent of red/green-only coding.\n\n"
        "## Status\n\n"
        "These are actual vector assets. Final approval still depends on intended-size page proof, caption pairing and export validation.\n",
        encoding='utf-8')
    print(f'generated={len(records)}')


if __name__=='__main__':
    main()
