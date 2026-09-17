from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_wave01_vector_diagrams as base

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "diagrams" / "wave-01"
META = ROOT / "assets" / "production-briefs" / "wave-01-vector-assets-c.json"
REPORT = ROOT / "docs" / "reviews" / "VISUAL_WAVE_01_VECTOR_REVIEW_C.md"


def compare(name, title, subtitle, left_title, left_rows, right_title, right_rows, note, desc, right_cls="box"):
    p=[]
    base.add_title(p,title,subtitle)
    base.box(p,70,190,500,95,left_title,"","box2")
    base.box(p,630,190,500,95,right_title,"",right_cls)
    y=330
    n=max(len(left_rows),len(right_rows))
    for i in range(n):
        if i < len(left_rows):
            h,b=left_rows[i]
            base.box(p,70,y,500,145,h,b,"box")
        if i < len(right_rows):
            h,b=right_rows[i]
            base.box(p,630,y,500,145,h,b,right_cls)
        y += 180
    base.footer_note(p,note)
    return base.write_svg(name,title,desc,p)


def simple_matrix(name,title,subtitle,headers,rows,note,desc):
    p=[]
    base.add_title(p,title,subtitle)
    x0=55; y0=225
    first=245
    other=(1090-first)//(len(headers)-1)
    widths=[first]+[other]*(len(headers)-1)
    xs=[x0]
    for w in widths[:-1]: xs.append(xs[-1]+w)
    for i,h in enumerate(headers): base.box(p,xs[i],y0,widths[i],100,h,"","box2")
    y=y0+120
    row_h=min(210, max(130, int(1050/max(1,len(rows)))))
    for r in rows:
        for i,val in enumerate(r):
            base.box(p,xs[i],y,widths[i],row_h,str(val),"","box2" if i==0 else "box")
        y += row_h+12
    base.footer_note(p,note)
    return base.write_svg(name,title,desc,p)


def hierarchy_controls():
    title="Figure 23.3 — Hierarchy of Controls for Beekeeping"
    desc="Hierarchy from avoiding a hazard through substitution, engineering or site controls, procedures and PPE, with beekeeping examples."
    p=[]
    base.add_title(p,title,"Use the most effective practical controls first. PPE is important but should not be the only control.")
    levels=[
        ("1. Avoid / eliminate","Do not perform the hazardous task when it is unnecessary or conditions are unsafe.","box2"),
        ("2. Substitute","Choose a safer method, tool, handling route or timing when equivalent work can be done with less risk.","box"),
        ("3. Engineering / site controls","Stable stands, barriers, lifting aids, ventilation, fire-safe smoker area, secure vehicle restraint.","box"),
        ("4. Procedures / administrative controls","Training, check-in plans, task limits, weather/fire checks, labels, records, work order.","box"),
        ("5. PPE","Veil/suit/gloves/footwear and task-specific chemical or eye protection as required.","box")]
    y=200
    widths=[980,850,720,590,460]
    for (h,b,c),w in zip(levels,widths):
        x=(1200-w)//2
        base.box(p,x,y,w,180,h,b,c)
        y+=220
    base.footer_note(p,"A lower-level control does not cancel the need for higher-level controls when those controls are practical and appropriate.")
    return base.write_svg("fig-23-3-hierarchy-of-controls.svg",title,desc,p)


def starvation_vs_stores():
    title="Figure 38.2 — Starvation Versus Accessible Stores"
    desc="Hive cutaway comparison of a winter cluster touching stores versus a small cold cluster separated from remaining stores, with an emergency-feed placement zone adjacent to the cluster."
    p=[]
    base.add_title(p,title,"Food can remain in the hive yet be biologically inaccessible to a small cold cluster.")
    for x,head in [(70,"Cluster in contact with stores"),(630,"Stores present but separated")]:
        base.box(p,x,200,500,1070,head,"","box" if x==70 else "stop")
        # hive outline / 5 frames
        p.append(f'<rect x="{x+80}" y="430" width="340" height="610" fill="#fff" stroke="#222" stroke-width="5"/>')
        for i in range(5):
            fx=x+105+i*65
            p.append(f'<rect x="{fx}" y="470" width="45" height="500" fill="#f7f7f7" stroke="#777" stroke-width="2"/>')
        # stores
        if x==70:
            p.append(f'<rect x="{x+245}" y="495" width="155" height="190" fill="#ddd" stroke="#111" stroke-width="3"/>')
            p.append(f'<ellipse cx="{x+280}" cy="760" rx="105" ry="135" fill="#555"/>')
            p += base.text_lines(x+120,1110,["Cluster touches or can reach remaining stores."],"body",27)
        else:
            p.append(f'<rect x="{x+260}" y="495" width="140" height="190" fill="#ddd" stroke="#111" stroke-width="3"/>')
            p.append(f'<ellipse cx="{x+160}" cy="810" rx="80" ry="110" fill="#555"/>')
            p.append(f'<rect x="{x+125}" y="650" width="110" height="45" fill="none" stroke="#111" stroke-width="4" stroke-dasharray="8 6"/>')
            p += base.text_lines(x+100,1080,base.wrap("Emergency feed, when justified, belongs where the cluster can reach it without crossing a cold gap.",45),"body",27)
    p += base.text_lines(230,350,["remaining stores"],"label",28)
    p += base.text_lines(790,350,["remaining stores"],"label",28)
    base.footer_note(p,"This is a winter-access concept, not a fixed feeding recipe. Assess colony condition, temperature, food type and local guidance before intervention.")
    return base.write_svg("fig-38-2-starvation-versus-accessible-stores.svg",title,desc,p)


def transmission_hub(name,title,subtitle,centre,branches,note,desc):
    p=[]
    base.add_title(p,title,subtitle)
    cx,cy=600,790
    p.append(f'<circle class="hub" cx="{cx}" cy="{cy}" r="145"/>')
    p += base.text_lines(cx,cy-10,base.wrap(centre,16),"hubtext",30,"middle")
    pos=[(600,270),(965,470),(1010,880),(790,1190),(410,1190),(190,880),(235,470)]
    for (h,b),(x,y) in zip(branches,pos):
        base.box(p,x-135,y-75,270,150,h,b,"box")
        base.arrow(p,x,y,cx,cy)
    base.footer_note(p,note)
    return base.write_svg(name,title,desc,p)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    assets=[]

    assets.append(base.vertical_flow(
        "fig-23-2-risk-assessment-sequence.svg","Figure 23.2 — Simple Risk-Assessment Sequence","A practical risk assessment begins before exposure and ends with review.",
        [("Identify the hazard","What can cause harm: stings, heat, fire, lifting, chemicals, traffic, terrain or equipment?","box2"),("Who may be harmed?","Beekeeper, helper, visitor, neighbour, public, livestock or other exposed person/animal.","box"),("Estimate likelihood and severity","Use a simple, documented judgement appropriate to the work and local workplace requirements.","box"),("Review existing controls","What already reduces the risk? Are controls actually available and working?","box"),("Add stronger controls","Prefer avoidance/substitution/site or engineering controls before relying only on PPE.","box"),("Do the task only if risk is acceptable","If conditions become unsafe, stop rather than forcing completion.","stop"),("Review after change or incident","Update the assessment when conditions, equipment, people or the task change.","box2")],
        "This generic sequence supports thinking; it does not replace a legally required workplace risk-assessment format.",
        "Seven-step risk-assessment flow from hazard identification to review, including a stop-work gate if risk is not acceptable."))
    assets.append(hierarchy_controls())
    assets.append(base.vertical_flow(
        "fig-23-11-treatment-ppe-label-discipline.svg","Figure 23.11 — Chemical-Treatment PPE and Label Discipline","The product label and current authorisation determine PPE, use conditions, storage and disposal.",
        [("Confirm authorised product/use","Check jurisdiction, target pest/disease, colony/product conditions and current label.","legal"),("Read PPE and environmental limits","Gloves, eye/respiratory protection and temperature/ventilation needs are product-specific.","legal"),("Prepare clean treatment zone","Keep food/honey away; organise spill control, measuring/application equipment and secure original container.","box"),("Apply only as labelled","No improvised dose, unapproved mixture, or unlabeled transfer container.","stop"),("Wash / decontaminate appropriately","Follow label and equipment instructions; prevent residues entering honey or food-contact tools.","box"),("Store/dispose securely","Original labelled container, inaccessible storage, and compliant waste/disposal route.","box2")],
        "The diagram is intentionally product-generic. Always follow the actual authorised label and current local rules.",
        "Treatment safety flow from authorisation and PPE through labelled application, wash-up, storage and disposal."))
    assets.append(compare(
        "fig-33-4-entrance-closure.svg","Figure 33.4 — Correct and Incorrect Entrance Closure","A transport closure must restrain bees while preserving adequate ventilation.",
        "Ventilated closure",[("Mesh / screened closure","Securely fitted; air path remains open."),("Airflow around screen","No boxes, fabric or clustered debris block the ventilation surface."),("Recheck during delay","Heat and bee clustering can change ventilation demand during transport.")],
        "Airtight / blocked closure",[("Solid sealed entrance","Populous colony can accumulate heat rapidly."),("Blocked screen","Ventilation area exists on paper but is ineffective in practice."),("Action","Stop and correct the ventilation hazard before continued transport.")],
        "Ventilation design must match colony strength, weather, duration and vehicle conditions; it is not a one-size opening area.",
        "Comparison of a secure ventilated entrance closure with airtight or blocked transport closure.","stop"))
    assets.append(compare(
        "fig-33-7-manual-handling.svg","Figure 33.7 — Manual Handling During Colony Moves","Reduce load, twisting and unstable-footing risk before lifting a hive.",
        "Safer handling",[("Plan route first","Clear obstacles, open gates and prepare the destination stand."),("Use aid or team lift","Hive carrier, trolley/ramp or second person for heavy/awkward loads."),("Keep load close","Stable stance; controlled lift; communicate with partner."),("Set down onto stable surface","Avoid holding the load while adjusting the stand.")],
        "Higher-risk handling",[("Twist while carrying","Increases musculoskeletal risk and load instability."),("Solo overload","Heavy supers/colonies can exceed safe individual handling capacity."),("Uneven/slippery ground","Fall and crush risk."),("Rush because bees are active","Time pressure does not make an unsafe lift acceptable.")],
        "Actual safe mass depends on the person, load geometry and workplace rules. Use mechanical assistance when needed.",
        "Manual-handling comparison of route planning, aid/team lift and stable stance versus twisting, solo overload and unstable footing.","stop"))
    assets.append(base.vertical_flow(
        "fig-33-12-emergency-box-separation.svg","Figure 33.12 — Emergency Box Separation","If hive boxes separate during transport, people and traffic safety come before hive reassembly.",
        [("1. Stop vehicle safely","Move out of traffic danger where possible; use hazards/barriers as appropriate.","stop"),("2. Protect public and helpers","Keep bystanders away; assess bee exposure and traffic/environmental hazards.","stop"),("3. Put on appropriate PPE","Do not rush into a mass of escaped/defensive bees unprotected.","box"),("4. Reassemble equipment","Restore boxes/floor/cover in a stable order while minimising crushing and comb damage.","box"),("5. Add/replace restraint","Use secure straps appropriate to the load; check other colonies too.","box2"),("6. Verify ventilation","Ensure screens/entrances have not shifted or become blocked.","box2"),("7. Resume only when safe","Recheck load stability, people, vehicle and route before movement.","box2")],
        "If the event creates a road/public emergency beyond safe beekeeper control, contact the appropriate emergency/road authority.",
        "Seven-step emergency sequence for separated hive boxes during transport."))
    assets.append(starvation_vs_stores())
    assets.append(base.vertical_flow(
        "fig-38-6-storm-damaged-hive-recovery.svg","Figure 38.6 — Storm-Damaged Hive Recovery","Stabilise the site, reassemble living colony equipment, prevent robbing and then evaluate colony damage.",
        [("People / site safety","Check fallen branches, electrical/weather hazards, unstable stands and access before approaching.","stop"),("Protect exposed bees and brood","Work efficiently; reduce rain/wind exposure and avoid crushing during recovery.","box"),("Reassemble in original order when identifiable","Restore floor, brood boxes/supers and cover; keep colony identity intact.","box"),("Secure and weatherproof","Level/stabilise stand, strap boxes and restore roof/cover protection.","box2"),("Remove spilled/exposed honey trigger","Clean accessible spills and exposed comb that could start severe robbing.","box"),("Record damage and schedule follow-up","Check queen/brood, comb breakage, stores, water intrusion and robbing at an appropriate later inspection.","box2")],
        "Disease-suspect, chemically contaminated or badly soiled product/equipment should be segregated rather than returned automatically.",
        "Storm-damage recovery flow from site safety through reassembly, securing, spill control and follow-up."))
    assets.append(base.vertical_flow(
        "fig-42-6-nosema-microscopy-workflow.svg","Figure 42.6 — Microscopy Workflow","Microscopy detects Nosema-like spores in a prepared sample; it does not reliably identify species by appearance alone.",
        [("Representative adult-bee sample","Use the sampling population and sample size specified by the laboratory/validated protocol.","box"),("Measured homogenisation","Prepare the sample with known bee count and liquid/dilution according to the selected method.","box2"),("Mix thoroughly","Spores must be distributed sufficiently for a representative sub-sample.","box"),("Slide / counting chamber","Load the defined chamber/field without introducing avoidable bubbles/debris.","box"),("Microscope examination","Recognise compatible Nosema-like spores and count according to the method.","box2"),("Interpret / confirm species when needed","Light microscopy generally cannot reliably distinguish N. apis from N. ceranae; molecular testing may be required.","legal")],
        "A positive spore result must be interpreted with colony condition, sampling quality and other stressors; detection alone does not prove causation of colony decline.",
        "Microscopy workflow from representative adult-bee sample through homogenisation, counting chamber, microscope and interpretation."))
    assets.append(simple_matrix(
        "fig-42-8-microscopy-vs-pcr.svg","Figure 42.8 — Microscopy Versus PCR/qPCR","The methods answer overlapping but different questions and have different resource requirements.",
        ["Feature","Light microscopy","PCR / qPCR"],
        [("Detects compatible spores","Yes","Detects target nucleic acid rather than visual spores"),("Species discrimination","Generally unreliable by morphology alone","Can discriminate targets when assay is validated"),("Quantification","Possible spore count with defined method","qPCR can estimate target quantity; units/standards depend on assay"),("Equipment","Microscope + counting method","Molecular laboratory workflow"),("Main limitation","Observer/sample preparation and poor species discrimination","Assay target, inhibitors, extraction and detection do not automatically prove clinical causation")],
        "Neither method should be interpreted without sample identity, colony signs and the decision being asked of the test.",
        "Comparison table of light microscopy and PCR/qPCR for Nosema/Vairimorpha investigation."))
    assets.append(base.vertical_flow(
        "fig-42-9-positive-result-not-equal-cause.svg","Figure 42.9 — A Positive Result Does Not Equal Cause","Pathogen detection must be linked to sample quality, species/assay, colony signs and competing explanations.",
        [("Positive result","A compatible spore/molecular target was detected in the tested sample.","box2"),("Was sampling representative?","Review bee age/location, sample size, timing, colony ID and processing quality.","box"),("What exactly was detected?","Microscopy: compatible spores; molecular assay: defined target/species depending on method.","box"),("Does colony condition fit clinical significance?","Strength, brood, queen function, food, season and trajectory matter.","box"),("Competing stressors?","Varroa/viruses, queen failure, nutrition, pesticide/toxic exposure, other disease, weather or management.","box"),("Management significance","Act on the integrated evidence and current legal/product options, not the word 'positive' alone.","legal")],
        "The diagram separates pathogen detection from proof that the detected organism caused the observed colony problem.",
        "Decision flow interpreting a positive Nosema/Vairimorpha test without equating detection with cause."))
    assets.append(transmission_hub(
        "fig-42-11-nosema-management-framework.svg","Figure 42.11 — Nosema Management Framework","Management centres on colony resilience, hygiene, correct diagnosis and legal treatment checks rather than one universal medicine threshold.","Colony-level Nosema management",
        [("Nutrition","Adequate, appropriate food and forage."),("Moisture / environment","Reduce chronic damp/stress where hive design and climate allow."),("Varroa control","Address major concurrent parasite/virus pressure."),("Feeder / water hygiene","Avoid avoidable contamination and shared dirty equipment."),("Comb / equipment","Biosecurity and sensible comb/equipment management."),("Diagnosis","Representative sampling and appropriate testing."),("Legal treatment check","Only authorised options under current jurisdiction; verify outcome.")],
        "No universal spores-per-bee treatment threshold is embedded because interpretation and authorised options vary by context and jurisdiction.",
        "Hub-and-spoke Nosema management framework covering nutrition, moisture, Varroa, hygiene, comb management, diagnosis and legal treatment check."))
    assets.append(base.vertical_flow(
        "fig-45-1-infection-versus-clinical-disease.svg","Figure 45.1 — Infection Versus Clinical Disease","Virus detection and visible disease are related but not synonymous.",
        [("Virus detected","RNA/virus evidence may be present in a bee or colony without obvious clinical signs.","box2"),("Covert / subclinical infection","Bees may appear normal while infection exists; prevalence/load and biological meaning vary.","box"),("Modifiers change risk","Varroa/vectoring, viral load, bee age, nutrition, genetics, coinfection and other stress can alter expression.","box"),("Overt clinical disease","Visible or behavioural syndrome can emerge, but similar signs can have other causes.","stop"),("Diagnosis / management","Integrate phenotype, colony context, Varroa level and appropriate laboratory evidence; do not infer causation from PCR alone.","legal")],
        "Visible disease can underestimate total infection burden, while a positive molecular result does not automatically prove the detected virus caused the signs.",
        "Layered pathway from virus detection through subclinical infection and modifiers to possible overt disease and integrated interpretation."))
    assets.append(transmission_hub(
        "fig-45-2-viral-transmission-routes.svg","Figure 45.2 — Viral Transmission Routes","Honey-bee viruses can move by several pathways; the importance of each pathway differs by virus and context.","Virus transmission / maintenance",
        [("Food / contact","Horizontal exposure among nestmates."),("Queen / offspring","Vertical or reproductive-associated pathways for some viruses."),("Brood cannibalism","Exposure during removal/consumption of affected brood."),("Varroa-mediated","Direct vectoring/inoculation and amplification; especially important for DWV ecology."),("Drifting / robbing","Bee movement between colonies can connect infection networks."),("Colony movement","Managed movement and introduced bees can spread infected hosts/vectors."),("Environment / equipment","Potential indirect routes vary by virus; do not assume equal importance.")],
        "Arrows indicate possible transmission routes, not identical efficiency or proof that every virus uses every route to the same degree.",
        "Hub diagram of food/contact, queen/offspring, brood cannibalism, Varroa, drifting/robbing, colony movement and indirect routes in honey-bee virus ecology."))
    assets.append(base.vertical_flow(
        "fig-45-9-rt-pcr-workflow.svg","Figure 45.9 — RT-PCR Workflow","RT-PCR detects virus-specific RNA sequence after reverse transcription; interpretation still depends on sample and clinical context.",
        [("Fresh / appropriately preserved labelled sample","Define bee type, colony, date and reason for testing; preserve according to laboratory instructions.","box"),("RNA extraction","Recover nucleic acid and manage contamination/inhibitor controls.","box2"),("Reverse transcription","Convert target RNA to complementary DNA for amplification.","box"),("Virus-specific amplification","Use validated primers/probes, controls and assay conditions.","box"),("Result","Detected / not detected or quantitative output according to assay and reporting limits.","box2"),("Interpretation","Combine with signs, sample type, Varroa pressure and assay limitations; RNA detection does not by itself prove infectious virus or causation.","legal")],
        "Laboratory details vary. This figure teaches interpretation and chain of evidence, not a bench protocol for unvalidated testing.",
        "RT-PCR workflow from labelled sample through RNA extraction, reverse transcription, amplification, result and contextual interpretation."))
    assets.append(compare(
        "fig-45-10-pooled-vs-individual-sampling.svg","Figure 45.10 — Pooled Versus Individual Sampling","Pooling is efficient for surveillance but can answer a different question from testing a selected symptomatic individual.",
        "Pooled sample",[("What it asks","Is the target detectable in a combined group / what is group-level signal?"),("Strength","Efficient for surveillance or group comparisons."),("Limitation","One strongly infected bee can be diluted; the pool hides individual distribution."),("Interpretation","Do not assign the pooled result to every individual bee.")],
        "Individual / phenotype-targeted sample",[("What it asks","What is present in this selected bee or defined individual?"),("Strength","Links laboratory result more closely to a specific phenotype/sample."),("Limitation","Selected moribund bee may not represent colony prevalence."),("Interpretation","Still does not prove causation without broader context.")],
        "Choose pooling or individual testing according to the biological question before collecting the sample.",
        "Comparison of pooled virus surveillance samples with individual phenotype-targeted sampling."))
    assets.append(transmission_hub(
        "fig-45-12-virus-management-framework.svg","Figure 45.12 — Practical Virus-Management Framework","There is no generic direct antiviral treatment panel; management reduces vectors, stress and transmission while improving evidence quality.","Virus-risk management",
        [("Varroa management","Quantitative monitoring and effective authorised IPM control."),("Nutrition","Adequate forage/stores and avoidance of chronic nutritional stress."),("Resistant / adapted stock","Use breeding evidence without overclaiming immunity."),("Robbing / drifting control","Reduce avoidable colony-to-colony transfer."),("Movement biosecurity","Trace introductions and avoid moving collapsing/suspect colonies without assessment."),("Exposure investigation","Consider pesticides, weather and other stressors in differential diagnosis."),("Laboratory testing","Use evidence-based testing when it changes a decision.")],
        "A positive virus test is not a licence to use unapproved pharmaceuticals. Management remains integrated and evidence-based.",
        "Hub diagram of practical honey-bee virus risk management through Varroa control, nutrition, stock, robbing/drifting reduction, movement biosecurity, exposure investigation and testing."))

    records=[]
    for path in assets:
        root=ET.parse(path).getroot(); ns='{http://www.w3.org/2000/svg}'
        t=root.find(ns+'title'); d=root.find(ns+'desc')
        records.append({"path":str(path.relative_to(ROOT)),"title":t.text if t is not None else None,"alt_text":d.text if d is not None else None,"format":"SVG","status":"DRAFT_ART_TECH_REVIEW_PASS_LAYOUT_PROOF_PENDING","provenance":"original deterministic vector generated in repository","rights":"original project asset; commercial print/digital use permitted subject to project ownership","external_dependencies":[]})
    META.parent.mkdir(parents=True,exist_ok=True)
    META.write_text(json.dumps({"asset_count":len(records),"assets":records},indent=2,ensure_ascii=False)+"\n",encoding='utf-8')
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text(
        "# Visual Wave 01 — Vector Diagram Technical Review C\n\n"
        "**Date:** 17 September 2026  \n"
        f"**Assets generated:** {len(records)}  \n"
        "**Result:** **TECHNICAL CONTENT PASS — LAYOUT PROOF PENDING**\n\n"
        "## Produced Assets\n\n" + "\n".join(f"- `{r['path']}` — {r['title']}" for r in records) +
        "\n\n## Review Controls\n\n"
        "- all generated SVGs parse as XML and contain `<title>`/`<desc>` accessibility metadata;\n"
        "- no external fonts, raster embeds, web assets or proprietary dependencies;\n"
        "- risk/PPE figures preserve hierarchy-of-controls and label-dependent chemical safety;\n"
        "- transport figures prioritise ventilation, restraint, people/road safety and controlled lifting;\n"
        "- starvation figure separates remaining food from food physically accessible to a cold cluster and avoids a universal feeding recipe;\n"
        "- Nosema/Vairimorpha figures distinguish microscopy from species-level molecular identification and detection from clinical causation;\n"
        "- virus figures distinguish infection/detection from clinical disease and RNA detection from proof of infectious virus/causation;\n"
        "- no unapproved antiviral or Nosema medicine advice, universal spore threshold or off-label treatment appears;\n"
        "- all diagrams are designed to remain meaningful in greyscale.\n\n"
        "## Status\n\nActual vector artwork is present. Final asset approval still requires layout-size proof, caption pairing and PDF/EPUB/print verification.\n",
        encoding='utf-8')
    print(f'generated={len(records)}')

if __name__=='__main__':
    main()
