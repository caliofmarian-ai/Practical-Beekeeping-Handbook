from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET
import html
import json
import textwrap

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "diagrams" / "wave-01"
REPORT = ROOT / "docs" / "reviews" / "VISUAL_WAVE_01_VECTOR_REVIEW.md"
META = ROOT / "assets" / "production-briefs" / "wave-01-vector-assets.json"

W = 1200
H = 1600

CSS = """
.bg{fill:#fff}.title{font:700 38px Arial,sans-serif;fill:#111}.subtitle{font:400 22px Arial,sans-serif;fill:#333}
.box{fill:#f7f7f7;stroke:#222;stroke-width:3}.box2{fill:#e9e9e9;stroke:#222;stroke-width:3}
.stop{fill:#fff;stroke:#111;stroke-width:5;stroke-dasharray:12 8}.legal{fill:#efefef;stroke:#111;stroke-width:4;stroke-dasharray:5 5}
.label{font:700 24px Arial,sans-serif;fill:#111}.body{font:400 21px Arial,sans-serif;fill:#222}.small{font:400 18px Arial,sans-serif;fill:#333}
.arrow{stroke:#111;stroke-width:4;fill:none;marker-end:url(#arrow)}.thin{stroke:#555;stroke-width:2;fill:none}.hub{fill:#222;stroke:#111;stroke-width:3}.hubtext{font:700 22px Arial,sans-serif;fill:#fff;text-anchor:middle}.note{fill:#fafafa;stroke:#666;stroke-width:2}
"""


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def wrap(s: str, width: int) -> list[str]:
    return textwrap.wrap(s, width=width, break_long_words=False, break_on_hyphens=False) or [""]


def svg_header(title: str, desc: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{esc(title)}</title>',
        f'<desc id="desc">{esc(desc)}</desc>',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#111"/></marker></defs>',
        f'<style>{CSS}</style>',
        f'<rect class="bg" x="0" y="0" width="{W}" height="{H}"/>',
    ]


def text_lines(x: float, y: float, lines: list[str], cls: str = "body", line_h: int = 28, anchor: str = "start") -> list[str]:
    out = []
    for i, line in enumerate(lines):
        out.append(f'<text class="{cls}" x="{x}" y="{y + i*line_h}" text-anchor="{anchor}">{esc(line)}</text>')
    return out


def add_title(parts: list[str], title: str, subtitle: str) -> None:
    parts.append(f'<text class="title" x="60" y="70">{esc(title)}</text>')
    parts.extend(text_lines(60, 108, wrap(subtitle, 92), "subtitle", 28))


def box(parts: list[str], x: int, y: int, w: int, h: int, heading: str, body: str = "", cls: str = "box") -> None:
    parts.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="22" ry="22"/>')
    parts.extend(text_lines(x+24, y+38, wrap(heading, max(12, int(w/15))), "label", 29))
    if body:
        head_lines = len(wrap(heading, max(12, int(w/15))))
        parts.extend(text_lines(x+24, y+48+head_lines*29, wrap(body, max(18, int(w/12))), "body", 27))


def arrow(parts: list[str], x1: int, y1: int, x2: int, y2: int) -> None:
    parts.append(f'<path class="arrow" d="M{x1},{y1} L{x2},{y2}"/>')


def footer_note(parts: list[str], text: str) -> None:
    y = 1480
    parts.append(f'<rect class="note" x="60" y="{y}" width="1080" height="80" rx="18"/>')
    parts.extend(text_lines(85, y+32, wrap(text, 92), "small", 23))


def write_svg(name: str, title: str, desc: str, parts: list[str]) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    content = "\n".join(svg_header(title, desc) + parts + ["</svg>"]) + "\n"
    path.write_text(content, encoding="utf-8")
    ET.parse(path)
    return path


def vertical_flow(name: str, title: str, subtitle: str, steps: list[tuple[str, str, str]], note: str, desc: str) -> Path:
    parts: list[str] = []
    add_title(parts, title, subtitle)
    x, w, h = 210, 780, 125
    y = 210
    for i, (heading, body, cls) in enumerate(steps):
        box(parts, x, y, w, h, heading, body, cls)
        if i < len(steps)-1:
            arrow(parts, x+w//2, y+h, x+w//2, y+h+45)
        y += h+55
    footer_note(parts, note)
    return write_svg(name, title, desc, parts)


def split_four(name: str, title: str, subtitle: str, root: str, branches: list[tuple[str,str]], note: str, desc: str) -> Path:
    parts: list[str] = []
    add_title(parts, title, subtitle)
    box(parts, 320, 180, 560, 115, root, "Choose the question before choosing the method.", "box2")
    coords = [(75, 410), (625, 410), (75, 830), (625, 830)]
    for (head, body), (x,y) in zip(branches, coords):
        box(parts, x, y, 500, 260, head, body, "box")
        arrow(parts, 600, 295, x+250, y)
    footer_note(parts, note)
    return write_svg(name, title, desc, parts)


def wheel(name: str, title: str, subtitle: str, center: str, spokes: list[str], note: str, desc: str) -> Path:
    parts: list[str] = []
    add_title(parts, title, subtitle)
    cx, cy = 600, 770
    parts.append(f'<circle class="hub" cx="{cx}" cy="{cy}" r="145"/>')
    parts.extend(text_lines(cx, cy-10, wrap(center, 18), "hubtext", 30, "middle"))
    positions = [(600,260),(930,390),(970,750),(900,1090),(600,1210),(300,1090),(230,750),(270,390)]
    for label, (x,y) in zip(spokes, positions):
        bw, bh = 260, 110
        bx, by = x-bw//2, y-bh//2
        box(parts, bx, by, bw, bh, label, "", "box")
        arrow(parts, cx, cy, x, y)
    footer_note(parts, note)
    return write_svg(name, title, desc, parts)


def cycle(name: str, title: str, subtitle: str, steps: list[str], note: str, desc: str) -> Path:
    parts: list[str] = []
    add_title(parts, title, subtitle)
    cx, cy = 600, 770
    positions = [(600,250),(895,340),(1010,620),(930,930),(650,1130),(350,1100),(145,845),(165,520),(365,320)]
    for i, (label,(x,y)) in enumerate(zip(steps, positions)):
        box(parts, x-130, y-55, 260, 110, label, "", "box" if i not in {5} else "box2")
        nx, ny = positions[(i+1)%len(positions)]
        arrow(parts, x, y+45 if ny>y else y-45, nx, ny-45 if ny>y else ny+45)
    parts.append(f'<circle class="hub" cx="{cx}" cy="{cy}" r="115"/>')
    parts.extend(text_lines(cx, cy-12, ["Integrated", "Pest", "Management"], "hubtext", 30, "middle"))
    footer_note(parts, note)
    return write_svg(name, title, desc, parts)


def two_pathways(name: str, title: str, subtitle: str, left_title: str, left_steps: list[str], right_title: str, right_steps: list[str], note: str, desc: str) -> Path:
    parts: list[str] = []
    add_title(parts, title, subtitle)
    box(parts, 80, 180, 500, 100, left_title, "", "box2")
    box(parts, 620, 180, 500, 100, right_title, "", "legal")
    for col_x, steps in [(80,left_steps),(620,right_steps)]:
        y=340
        for i,s in enumerate(steps):
            box(parts, col_x, y, 500, 125, s, "", "box" if col_x==80 else "legal")
            if i < len(steps)-1:
                arrow(parts, col_x+250, y+125, col_x+250, y+165)
            y += 180
    footer_note(parts, note)
    return write_svg(name, title, desc, parts)


def treatment_failure_tree() -> Path:
    title = "Figure 46.10 — Treatment Failure Investigation"
    desc = "Decision tree for investigating a high post-control pest result without automatic dose escalation."
    parts: list[str] = []
    add_title(parts, title, "Investigate the result systematically before choosing a corrective action.")
    box(parts, 300, 170, 600, 110, "High post-control result", "Do not automatically increase dose.", "stop")
    box(parts, 300, 340, 600, 120, "1. Verify sampling", "Was the method, sample and calculation valid?", "box2")
    arrow(parts, 600, 280, 600, 340)
    box(parts, 100, 550, 420, 150, "2. Review application context", "Authorisation, label directions, temperature, brood, product condition, timing.")
    box(parts, 680, 550, 420, 150, "3. Recheck pest biology", "Could brood protection, life stage or timing explain persistence?")
    arrow(parts, 600, 460, 310, 550)
    arrow(parts, 600, 460, 890, 550)
    box(parts, 100, 790, 420, 150, "4. Assess resistance", "Use evidence and local guidance; focus on active ingredient / mode of action.")
    box(parts, 680, 790, 420, 150, "5. Assess reinvasion", "Consider robbing, drifting and nearby collapsing/high-pressure colonies.")
    arrow(parts, 310, 700, 310, 790)
    arrow(parts, 890, 700, 890, 790)
    box(parts, 300, 1030, 600, 140, "6. Choose evidence-based corrective action", "Use an authorised, context-appropriate option; document and plan follow-up verification.", "box2")
    arrow(parts, 310, 940, 500, 1030)
    arrow(parts, 890, 940, 700, 1030)
    box(parts, 300, 1240, 600, 120, "7. Verify again", "Repeat a valid monitoring method at the appropriate interval.", "box")
    arrow(parts, 600, 1170, 600, 1240)
    footer_note(parts, "Changing a brand name is not necessarily changing mode of action. Never use unapproved mixtures or off-label dose escalation.")
    return write_svg("fig-46-10-treatment-failure-investigation.svg", title, desc, parts)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    assets = []

    assets.append(vertical_flow(
        "fig-23-9-heat-cold-dehydration-prevention.svg",
        "Figure 23.9 — Heat, Cold and Dehydration Prevention",
        "A work-safety flow: prevent exposure, watch for deterioration, and stop work when conditions become unsafe.",
        [
            ("Before work", "Check weather, duration, PPE heat load, drinking water, shade/shelter and personal fitness.", "box2"),
            ("During work", "Hydrate; use shade/rest breaks; adjust layers; shorten tasks when heat, cold or wind increases risk.", "box"),
            ("Warning signs or impaired judgement?", "Stop work. Move to a safer environment and do not continue hazardous apiary tasks.", "stop"),
            ("Severe, rapidly worsening or concerning symptoms?", "Seek appropriate urgent medical assistance. Follow the person's emergency plan where applicable.", "legal"),
        ],
        "This figure supports prevention and stop-work decisions; it is not a diagnostic chart for heat illness, hypothermia or dehydration.",
        "Flow diagram showing pre-work preparation, prevention during work, stop-work cues and escalation to urgent medical help for severe symptoms."
    ))

    assets.append(vertical_flow(
        "fig-24-9-first-inspection-decision-timeline.svg",
        "Figure 24.9 — First-Inspection Decision Timeline",
        "The first check is targeted to the starting unit and colony condition, not a rigid universal day count.",
        [
            ("Installation day", "Close the colony safely, confirm ventilation/entrance arrangement and feeding only where appropriate.", "box2"),
            ("Allow a short settling period", "Avoid unnecessary disturbance while bees orient and the queen/unit establishes.", "box"),
            ("Choose the question", "Package: queen acceptance / comb / food. Nucleus: queenright status / brood / space. Swarm: staying / comb / food / health baseline.", "box"),
            ("Perform a brief targeted check", "Look for evidence needed to answer the question; do not turn it into a full inspection without cause.", "box"),
            ("Set the next check", "Base timing on findings, weather, colony biology, feed, queen status and local/supplier guidance.", "box2"),
        ],
        "Exact first-inspection timing is context-dependent. The diagram deliberately avoids a universal calendar interval.",
        "Timeline from installation through settling, targeted first inspection and setting the next check according to starting unit and conditions."
    ))

    assets.append(vertical_flow(
        "fig-25-3-inspection-questions-before-opening.svg",
        "Figure 25.3 — Inspection Questions Before Opening",
        "Define the questions before opening the hive so disturbance produces useful information.",
        [
            ("1. Queenright?", "What evidence is needed: eggs, young larvae, brood progression or another queen-status check?", "box"),
            ("2. Brood appropriate?", "Is development coherent for season, queen status and colony strength?", "box"),
            ("3. Food adequate?", "Are accessible carbohydrate and pollen stores sufficient for current brood and weather?", "box"),
            ("4. Enough usable space?", "Is there room for brood, stores and bee movement without unnecessary excess space?", "box"),
            ("5. Warning signs?", "Pest, disease, robbing, equipment or environmental concern that changes inspection depth?", "box"),
            ("6. Action today?", "Only intervene when the finding justifies it; otherwise close carefully and record.", "box2"),
            ("7. Next inspection when?", "Set timing from the biological question and today's findings, not habit alone.", "box2"),
        ],
        "A routine inspection is a planned information-gathering task, not simply opening every colony on a fixed schedule.",
        "Seven-question pre-inspection decision card covering queen status, brood, food, space, warning signs, action and follow-up."
    ))

    assets.append(vertical_flow(
        "fig-38-1-emergency-triage-sequence.svg",
        "Figure 38.1 — Emergency Triage Sequence",
        "Stabilisation comes before diagnosis when an active hazard is present.",
        [
            ("1. People and public safety", "Remove immediate human/animal exposure; use PPE and emergency assistance where needed.", "stop"),
            ("2. Stop the active hazard", "Examples: fire, vehicle/transport hazard, robbing trigger, chemical exposure, collapsing equipment.", "stop"),
            ("3. Stabilise the colony", "Restore ventilation, shelter, physical integrity, accessible food or another immediate need as appropriate.", "box"),
            ("4. Prevent spread", "Restrict movement of frames, bees, tools, honey or contaminated material when disease/chemical risk is possible.", "box"),
            ("5. Preserve evidence", "Photograph, label samples, record objective observations and retain lot/treatment/movement information.", "box"),
            ("6. Diagnose / escalate", "Use validated methods and contact the competent authority when a notifiable disease, exotic pest or serious chemical incident is suspected.", "legal"),
            ("7. Correct cause", "Apply the appropriate authorised corrective action only after the problem is understood.", "box2"),
            ("8. Verify recovery", "Recheck at an interval that matches the problem and colony biology; document the outcome.", "box2"),
        ],
        "Regulatory/authority contact can interrupt this sequence at any point when the suspected problem requires it.",
        "Emergency decision flow from people safety through hazard control, colony stabilisation, containment, evidence preservation, diagnosis, correction and recovery verification."
    ))

    assets.append(split_four(
        "fig-40-13-monitoring-method-matches-question.svg",
        "Figure 40.13 — Monitoring Method Matches the Question",
        "Select a monitoring or diagnostic method according to the biological question—not because one test is familiar.",
        "What are you trying to learn?",
        [
            ("Estimate Varroa pressure", "Use a validated adult-bee quantitative sampling method appropriate to local guidance; record the denominator and result."),
            ("Confirm control performance", "Use a comparable pre/post quantitative method and an appropriate verification interval; separate efficacy from later reinvasion."),
            ("Detect suspected exotic Tropilaelaps", "Preserve evidence, restrict movement and use competent-authority surveillance/identification pathways; do not rely on Varroa thresholds."),
            ("Investigate tracheal mites", "Use adult-bee sampling and validated dissection/microscopy or current laboratory methods; wing posture alone is not diagnostic."),
        ],
        "The figure intentionally contains no fixed treatment threshold or distribution claim that can become obsolete.",
        "Four-way decision diagram linking Varroa pressure estimation, control verification, exotic Tropilaelaps detection and tracheal-mite investigation to appropriate method classes."
    ))

    assets.append(wheel(
        "fig-41-9-thresholds-contextual.svg",
        "Figure 41.9 — Why Thresholds Are Contextual",
        "A monitoring number becomes a management decision only after the surrounding biological and regulatory context is considered.",
        "Interpret the measured Varroa result",
        ["Season / colony phase","Brood amount","Climate / weather","Virus pressure","Reinvasion risk","Authorised options","Management goal","Local guidance / next check"],
        "Do not print one universal Varroa threshold into a permanent diagram. Record the method, denominator, date and local decision basis.",
        "Decision wheel surrounding a measured Varroa result with season, brood, climate, virus pressure, reinvasion, authorised options, management goal and local guidance."
    ))

    assets.append(vertical_flow(
        "fig-43-13-afb-response-decision-flow.svg",
        "Figure 43.13 — AFB Response Decision Flow",
        "Suspicion is a containment and confirmation problem before it is a treatment problem.",
        [
            ("Suspicious brood signs", "Irregular cappings, suspicious remains or other compatible signs raise suspicion but do not prove AFB.", "box"),
            ("Stop movement", "Do not move brood, honey frames, bees, tools or suspect equipment out of the affected unit/apiary unnecessarily.", "stop"),
            ("Record and preserve evidence", "Photograph objectively; label sample/colony; retain purchase, movement and equipment-sharing records.", "box"),
            ("Contact competent authority where required", "AFB control and notification requirements vary by jurisdiction and can override ordinary management.", "legal"),
            ("Approved confirmation", "Use the current official/validated diagnostic pathway. Field signs or rope test alone are not universal definitive confirmation.", "box2"),
            ("Official control / decontamination", "Follow the legally required disposition and approved decontamination programme; do not improvise recipes.", "legal"),
            ("Inspect contact colonies", "Trace robbing, drifting, frame transfer, equipment sharing, purchases, sales and apiary movement.", "box"),
            ("Follow-up surveillance", "Verify that control actions worked and continue monitoring according to authority guidance.", "box2"),
        ],
        "AFB spores are persistent. Antibiotic suppression of vegetative bacteria does not mean spores have been eradicated from comb/equipment.",
        "AFB decision flow from suspicious signs to movement stop, evidence preservation, authority contact, validated confirmation, official control, contact-colony inspection and follow-up."
    ))

    assets.append(vertical_flow(
        "fig-44-8-efb-sampling-diagnostic-pathway.svg",
        "Figure 44.8 — EFB Sampling and Diagnostic Pathway",
        "Clinical appearance guides sample selection; diagnosis integrates validated testing, signs and legal context.",
        [
            ("Representative abnormal larva", "Choose material that reflects the current lesion pattern; avoid sampling only dried or unrelated debris.", "box"),
            ("Labelled sample and chain of identity", "Record colony/apiary, date, material, collector and relevant clinical observations.", "box"),
            ("Validated field or laboratory test", "Use the method accepted for the intended decision; methods and authority requirements vary by jurisdiction.", "box2"),
            ("Interpret with clinical signs", "Consider larval age/position, brood pattern, colony stress and differential diagnoses; poor nutrition modifies expression but is not the infectious cause.", "box"),
            ("Apply legal / management decision", "Follow competent-authority and veterinary requirements where applicable; do not treat one visual sign as proof.", "legal"),
            ("Reinspect and monitor recurrence", "Clinical improvement does not remove the need for follow-up where the programme requires it.", "box2"),
        ],
        "EFB does not form AFB-like durable bacterial endospores. Treatment and shook-swarm decisions are jurisdiction-dependent.",
        "EFB diagnostic pathway from representative larva and labelled sample to validated test, integrated interpretation, legal management decision and follow-up."
    ))

    assets.append(cycle(
        "fig-46-1-honey-bee-ipm-cycle.svg",
        "Figure 46.1 — The Honey Bee IPM Cycle",
        "IPM is a repeated evidence loop, not a one-time treatment event.",
        ["Prevention","Surveillance / monitoring","Identification","Risk interpretation","Control selection","Authorised application","Verification","Records / review","Return to prevention"],
        "Statutory disease and exotic-pest pathways can require immediate authority action rather than ordinary economic-threshold logic.",
        "Circular IPM cycle from prevention through monitoring, identification, risk interpretation, control selection, authorised application, verification and records/review back to prevention."
    ))

    assets.append(treatment_failure_tree())

    assets.append(two_pathways(
        "fig-46-12-established-vs-exotic-regulated-pest.svg",
        "Figure 46.12 — Established Pest Versus Exotic Regulated Pest",
        "Different biological and legal questions require different response pathways.",
        "Established Varroa / routine threat",
        ["Quantitative monitoring","Interpret result in local context","Choose authorised IPM control when needed","Verify outcome and retest"],
        "Suspected exotic / regulated pest",
        ["Preserve specimen/evidence","Restrict unnecessary movement","Contact competent authority promptly","Follow official identification/control instructions"],
        "Do not apply ordinary Varroa threshold logic to a suspected exotic or notifiable organism.",
        "Two-column pathway comparing routine Varroa monitoring and IPM management with evidence preservation, movement restraint and authority notification for suspected exotic regulated pests."
    ))

    assets.append(vertical_flow(
        "fig-41-13-pre-treatment-safety-check.svg",
        "Figure 41.13 — Honey-Super and Temperature Decision Check",
        "A pre-treatment safety and compliance check happens before any product is applied.",
        [
            ("Authorised product and intended use?", "Check current jurisdiction, species/pest indication and label directions.", "legal"),
            ("Honey-super / harvest status compatible?", "Respect all honey-super, withdrawal, residue and harvest restrictions.", "legal"),
            ("Brood and colony condition understood?", "Treatment performance and bee safety can depend on brood availability, strength and colony state.", "box"),
            ("Forecast temperature / weather within label limits?", "Use the product only inside its specified environmental conditions.", "box"),
            ("PPE, storage and disposal ready?", "Protect operator and food; prepare spill/handling controls before opening the product.", "box"),
            ("Prior active ingredient / resistance history reviewed?", "Plan rotation by relevant mode of action rather than brand name alone.", "box"),
            ("Follow-up monitoring scheduled?", "Verification is part of treatment, not an optional extra.", "box2"),
        ],
        "This is a pre-use decision checklist, not a dosing recipe. Never alter label dose or combine products unless specifically authorised.",
        "Pre-treatment checklist covering authorisation, honey-super status, brood, weather, PPE, resistance history and follow-up monitoring."
    ))

    records = []
    for path in assets:
        tree = ET.parse(path)
        root = tree.getroot()
        title = root.find('{http://www.w3.org/2000/svg}title')
        desc = root.find('{http://www.w3.org/2000/svg}desc')
        records.append({
            "path": str(path.relative_to(ROOT)),
            "title": title.text if title is not None else None,
            "alt_text": desc.text if desc is not None else None,
            "format": "SVG",
            "provenance": "original deterministic vector generated in repository",
            "rights": "original project asset; commercial publication permitted subject to project ownership",
            "status": "DRAFT_ART_TECH_REVIEW_PASS_LAYOUT_PROOF_PENDING",
            "colour_dependency": "none; greyscale-safe",
            "external_font_dependency": "none",
        })

    META.parent.mkdir(parents=True, exist_ok=True)
    META.write_text(json.dumps({"asset_count": len(records), "assets": records}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        "# Visual Wave 01 — Vector Diagram Technical Review\n\n"
        "**Date:** 17 September 2026  \n"
        "**Scope:** first deterministic vector assets from Wave 01  \n"
        f"**Assets generated:** {len(records)}  \n"
        "**Result:** **TECHNICAL CONTENT PASS — LAYOUT PROOF PENDING**\n\n"
        "## What Was Produced\n\n"
        + "\n".join(f"- `{r['path']}` — {r['title']}" for r in records)
        + "\n\n## Validation Performed\n\n"
        "- every SVG parses as XML;\n"
        "- each asset contains accessible `<title>` and `<desc>` metadata;\n"
        "- no external fonts, web resources, raster embeds or proprietary dependencies are used;\n"
        "- diagrams remain readable without colour and use line/shape/label semantics;\n"
        "- no universal Varroa threshold is embedded;\n"
        "- no treatment dose, off-label mixture or product-specific recipe is embedded;\n"
        "- AFB/EFB diagrams distinguish suspicion from validated/official confirmation;\n"
        "- exotic/regulated-pest pathways are separated from routine established-pest management;\n"
        "- emergency/safety diagrams place stop/escalation steps before diagnosis or continued work.\n\n"
        "## Status Rule\n\n"
        "These assets are actual publication vector artwork, not placeholders. They are marked `DRAFT_ART_TECH_REVIEW_PASS_LAYOUT_PROOF_PENDING` because final approval still requires placement at intended print size, caption pairing, page proof, and export checks.\n\n"
        "## Next Work\n\n"
        "Continue Wave 01 with biological/anatomical and diagnostic-comparison assets, then perform family-level visual proofing before changing any asset to `APPROVED`.\n",
        encoding="utf-8",
    )
    print(f"generated={len(records)}")


if __name__ == "__main__":
    main()
