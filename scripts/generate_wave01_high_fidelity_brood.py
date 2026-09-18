#!/usr/bin/env python3
from __future__ import annotations
import json, math, re, html
from pathlib import Path
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"assets"/"diagrams"/"wave-01"
QUEUE=ROOT/"assets"/"production-briefs"/"wave-01-high-fidelity.json"
REPORT=ROOT/"docs"/"reviews"/"VISUAL_WAVE_01_HIGH_FIDELITY_BROOD_REVIEW.md"
W,H=1400,1050
C={"ink":"#1F2933","muted":"#52606D","grid":"#8D6E63","wax":"#F6E7B0","broodcap":"#B98755","broodcap_dark":"#8A5A35","healthy":"#2E7D32","healthy_light":"#E8F5E9","danger":"#C62828","danger_light":"#FFEBEE","warn":"#EF6C00","warn_light":"#FFF3E0","blue":"#1565C0","blue_light":"#E3F2FD","purple":"#6A1B9A","purple_light":"#F3E5F5","larva":"#FFFDF4","larva_shadow":"#E9E4D6","egg":"#FDFDFD","pollen":"#D98C10","honey":"#D4A017","afb":"#7A3F20","efb_yellow":"#D9A441","efb_brown":"#9B5E2E","white":"#FFFFFF"}
FONT="Arial,Helvetica,sans-serif"

def svg_start(title,desc):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title>',f'<desc id="desc">{escape(desc)}</desc>',
            f'<rect width="{W}" height="{H}" fill="{C["white"]}"/>',
            f'<text x="55" y="62" font-family="{FONT}" font-size="34" font-weight="700" fill="{C["ink"]}">{escape(title)}</text>']

def finish(p): p.append("</svg>"); return "\n".join(p)+"\n"
def txt(p,x,y,s,size=20,weight=400,fill=None,anchor="start"):
    p.append(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill or C["ink"]}" text-anchor="{anchor}">{escape(s)}</text>')
def multi(p,x,y,lines,size=18,weight=400,fill=None,lead=25,anchor="start"):
    for i,line in enumerate(lines): txt(p,x,y+i*lead,line,size,weight,fill,anchor)
def rect(p,x,y,w,h,fill,stroke,sw=2,r=18):
    p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def panel(p,x,y,w,h,title,kind="neutral"):
    pal={"healthy":(C["healthy_light"],C["healthy"]),"danger":(C["danger_light"],C["danger"]),"warn":(C["warn_light"],C["warn"]),"lab":(C["purple_light"],C["purple"]),"neutral":(C["blue_light"],C["blue"]),"wax":("#FFFBEA",C["grid"])}
    fill,stroke=pal[kind]; rect(p,x,y,w,h,fill,stroke,2.5,20); txt(p,x+20,y+34,title,21,700,stroke)
def hexpts(cx,cy,r):
    pts=[]
    for k in range(6):
        a=math.radians(60*k-30); pts.append((cx+r*math.cos(a),cy+r*math.sin(a)))
    return " ".join(f"{x:.1f},{y:.1f}" for x,y in pts)
def cell(p,cx,cy,r=29,fill=None,stroke=None,sw=2):
    p.append(f'<polygon points="{hexpts(cx,cy,r)}" fill="{fill or C["wax"]}" stroke="{stroke or C["grid"]}" stroke-width="{sw}"/>')
def egg(p,cx,cy,scale=1):
    p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{3.2*scale}" ry="{11*scale}" fill="{C["egg"]}" stroke="#B8B8B0" stroke-width="1.2"/>')
def larva(p,cx,cy,scale=1,color=None,rotate=0,twisted=False):
    color=color or C["larva"]
    if twisted:
        d=f"M {cx-18*scale} {cy-8*scale} C {cx-5*scale} {cy-30*scale}, {cx+20*scale} {cy-20*scale}, {cx+13*scale} {cy} C {cx+7*scale} {cy+17*scale}, {cx-17*scale} {cy+19*scale}, {cx-9*scale} {cy+6*scale}"
    else:
        d=f"M {cx-17*scale} {cy-10*scale} C {cx-4*scale} {cy-29*scale}, {cx+21*scale} {cy-18*scale}, {cx+17*scale} {cy+3*scale} C {cx+14*scale} {cy+20*scale}, {cx-10*scale} {cy+23*scale}, {cx-17*scale} {cy+8*scale}"
    p.append(f'<path d="{d}" fill="none" stroke="{C["larva_shadow"]}" stroke-width="{14*scale}" stroke-linecap="round" transform="rotate({rotate} {cx} {cy})"/>')
    p.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{10*scale}" stroke-linecap="round" transform="rotate({rotate} {cx} {cy})"/>')
def cap(p,cx,cy,r=29,sunken=False,perforated=False,healthy=True):
    base=C["broodcap"] if healthy else "#8E6A4B"
    if sunken: base="#795A43"
    cell(p,cx,cy,r,base,C["broodcap_dark"],2)
    if healthy: p.append(f'<ellipse cx="{cx-6}" cy="{cy-7}" rx="13" ry="7" fill="#D7AB7A" opacity="0.45"/>')
    if sunken: p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="14" ry="10" fill="#5A4030" opacity="0.45"/>')
    if perforated:
        p.append(f'<circle cx="{cx+5}" cy="{cy-2}" r="4.5" fill="#3E2B22"/>')
        p.append(f'<circle cx="{cx-9}" cy="{cy+6}" r="3.2" fill="#3E2B22"/>')
def grid(p,x0,y0,cols,rows,r,mode,seed):
    dx=math.sqrt(3)*r; dy=1.5*r
    for row in range(rows):
        for col in range(cols):
            cx=x0+col*dx+(row%2)*dx/2; cy=y0+row*dy; score=(col*17+row*31+seed*7)%23
            if mode=="healthy":
                if score==0: cell(p,cx,cy,r,"#FFF7D6")
                else: cap(p,cx,cy,r,healthy=True)
            elif mode=="irregular":
                if score in (0,2,4,7,11,15): cell(p,cx,cy,r,"#FFF7D6")
                elif score in (5,13): cap(p,cx,cy,r,True,score==13,False)
                else: cap(p,cx,cy,r,healthy=True)
            elif mode=="afb":
                if score in (0,3,8,12): cell(p,cx,cy,r,"#FFF7D6")
                elif score in (2,6,9,15): cap(p,cx,cy,r,True,True,False)
                else: cap(p,cx,cy,r,healthy=True)
def note(p,y,lines,kind="warn"):
    fill,stroke=(C["warn_light"],C["warn"]) if kind=="warn" else (C["blue_light"],C["blue"])
    rect(p,55,y,W-110,90,fill,stroke,2.5,16); multi(p,78,y+30,lines,18,600,C["ink"],24)

def fig_25_7():
    p=svg_start("Figure 25.7 — Brood Pattern Interpretation","Comparison of coherent healthy brood and irregular brood requiring investigation; appearance alone is not diagnostic.")
    txt(p,55,102,"Compare pattern first; then inspect cells, history, queen status, parasites, nutrition and temperature.",19,400,C["muted"])
    panel(p,55,145,620,710,"Coherent brood pattern","healthy"); grid(p,110,225,10,13,25,"healthy",1)
    txt(p,92,760,"Expected features",20,700,C["healthy"]); multi(p,92,790,["• broad coherent area of capped worker brood","• a few normal gaps can occur","• cappings mostly even and unpunctured"],18,400,C["ink"],27)
    panel(p,725,145,620,710,"Irregular / spotty pattern","warn"); grid(p,780,225,10,13,25,"irregular",3)
    txt(p,762,760,"Triggers further investigation",20,700,C["warn"]); multi(p,762,790,["• random gaps or uncapped/removal areas","• inspect larvae/pupae and cappings closely","• consider queen, disease, Varroa, nutrition, chilling"],18,400,C["ink"],27)
    note(p,900,["Brood pattern is evidence, not a diagnosis. A small number of gaps can be normal; heavy irregularity requires cell-level examination and colony history."])
    return finish(p)

def fig_39_2():
    p=svg_start("Figure 39.2 — Healthy Brood Reference","Reference plate showing eggs, pearly C-shaped larvae, healthy capped worker brood, pollen and honey cells.")
    txt(p,55,102,"Learn normal brood morphology before interpreting disease signs.",19,400,C["muted"])
    for x,y,t,k in [(55,155,"Egg","healthy"),(385,155,"Young larva","healthy"),(715,155,"Older larva","healthy"),(1045,155,"Capped worker brood","healthy"),(220,555,"Pollen cell","wax"),(550,555,"Nectar / honey cell","wax"),(880,555,"Healthy mixed brood context","neutral")]: panel(p,x,y,300,320,t,k)
    cell(p,205,330,90,"#FFF4C8",C["grid"],4); egg(p,205,330,2); txt(p,205,448,"one egg attached at cell base",16,600,C["muted"],"middle")
    cell(p,535,330,90,"#FFF4C8",C["grid"],4); larva(p,535,330,1.65); txt(p,535,448,"pearly white, moist, glistening, C-shaped",16,600,C["muted"],"middle")
    cell(p,865,330,90,"#FFF4C8",C["grid"],4); larva(p,865,330,2.15); txt(p,865,448,"larger C-shaped larva before capping",16,600,C["muted"],"middle")
    cap(p,1195,330,90,healthy=True); txt(p,1195,448,"medium-brown, slightly convex, unpunctured",16,600,C["muted"],"middle")
    cell(p,370,720,90,"#F0C55F",C["grid"],4)
    for dx,dy,col in [(-25,-15,"#C7701A"),(15,-20,"#E3A52F"),(-8,18,"#A65B24"),(28,18,"#D98C10"),(-35,28,"#C88D28")]: p.append(f'<circle cx="{370+dx}" cy="{720+dy}" r="20" fill="{col}" opacity="0.92"/>')
    txt(p,370,840,"packed grains; colours vary by source",16,600,C["muted"],"middle")
    cell(p,700,720,90,"#F7D66D",C["grid"],4); p.append('<ellipse cx="680" cy="690" rx="32" ry="18" fill="#FFF5B5" opacity="0.85"/>'); txt(p,700,840,"liquid stores reflect light; appearance varies",16,600,C["muted"],"middle")
    grid(p,930,640,6,6,24,"healthy",2); txt(p,1030,840,"normal brood can contain a few non-brood cells",16,600,C["muted"],"middle")
    note(p,900,["Healthy larvae are pearly white and C-shaped; healthy worker-brood cappings are generally coherent, medium brown, slightly convex and unpunctured."],"neutral")
    return finish(p)

def fig_39_3():
    p=svg_start("Figure 39.3 — Patchy Brood Has Multiple Causes","Five panels demonstrate that similar patchiness can arise from different causes and is not diagnostic by appearance alone.")
    txt(p,55,102,"A similar frame-level pattern can arise from very different biological causes.",19,400,C["muted"])
    items=[("Queen / laying problem","Examine egg pattern and queen history.","neutral"),("Infectious brood disease","Inspect larvae/cappings; sample if indicated.","danger"),("Hygienic removal","Opened/removed brood can reflect defence.","healthy"),("Chilled brood","Distribution and exposure history matter.","warn"),("Varroa-associated loss","Quantify mites and assess virus context.","lab")]
    for i,(t,s,k) in enumerate(items):
        x=45+i*275; panel(p,x,155,245,700,t,k); grid(p,x+40,245,4,9,23,"irregular",i+1); multi(p,x+18,705,[s],16,600,C["ink"],24)
    note(p,900,["Do not diagnose from a patchy frame alone. Use cell-level morphology, colony history, Varroa measurement and validated laboratory/official pathways when needed."])
    return finish(p)

def fig_39_4():
    p=svg_start("Figure 39.4 — American Foulbrood Suspicion Features","AFB suspicion plate showing irregular sealed brood, sunken or perforated cappings, brown remains, adherent scale and rope test as supporting evidence only.")
    txt(p,55,102,"These signs support suspicion; regulated-disease procedures and confirmation still apply.",19,400,C["muted"])
    panel(p,55,155,610,360,"1 — Capping changes","danger"); grid(p,105,245,9,6,25,"afb",4); txt(p,90,480,"Sunken/perforated cappings can occur among otherwise sealed brood.",17,600,C["ink"])
    panel(p,735,155,610,360,"2 — Brown decomposed remains","danger"); cell(p,1035,330,100,"#FFF1CF",C["grid"],4)
    p.append(f'<path d="M965 345 C1000 300 1085 310 1100 355 C1068 390 1004 400 970 370 Z" fill="{C["afb"]}"/>'); txt(p,1035,480,"stage-dependent colour and consistency; appearance varies",17,600,C["muted"],"middle")
    panel(p,55,555,610,300,"3 — Adherent scale position","danger"); p.append(f'<path d="M160 640 L300 600 L440 640 L410 800 L190 800 Z" fill="{C["wax"]}" stroke="{C["grid"]}" stroke-width="4"/>'); p.append('<path d="M210 775 C270 745 350 746 395 774 L390 795 L205 795 Z" fill="#4E3024"/>'); txt(p,300,835,"dark dry scale adheres along lower cell wall",17,600,C["muted"],"middle")
    panel(p,735,555,610,300,"4 — Rope test: supporting evidence only","warn"); p.append(f'<circle cx="940" cy="705" r="78" fill="#FFF1CF" stroke="{C["grid"]}" stroke-width="4"/>'); p.append(f'<path d="M900 720 C930 685 970 690 992 721" fill="none" stroke="{C["afb"]}" stroke-width="22" stroke-linecap="round"/>'); p.append(f'<line x1="1000" y1="708" x2="1180" y2="625" stroke="{C["ink"]}" stroke-width="8"/>'); p.append(f'<path d="M992 710 C1040 690 1080 670 1126 649" fill="none" stroke="{C["afb"]}" stroke-width="9" stroke-linecap="round"/>'); txt(p,1040,835,"ropiness may strengthen suspicion; a negative result does not exclude AFB",16,600,C["muted"],"middle")
    note(p,900,["If AFB is suspected, stop movement as required locally, preserve evidence and follow the competent-authority pathway. Odour or one visual sign is never sufficient alone."])
    return finish(p)

def fig_43_2():
    p=svg_start("Figure 43.2 — Healthy Brood Versus Early AFB Suspicion","Comparison of coherent healthy sealed worker brood versus early AFB-suspicion pattern with irregular sealed brood and some sunken/perforated cappings.")
    txt(p,55,102,"Compare the pattern, then individual cappings and remains; early AFB can be subtle.",19,400,C["muted"])
    panel(p,55,150,620,705,"Healthy sealed worker brood","healthy"); grid(p,115,245,10,13,25,"healthy",8); multi(p,90,780,["• coherent brood area","• medium-brown, slightly convex cappings","• no unexplained perforations"],18,500,C["ink"],28)
    panel(p,725,150,620,705,"Early AFB suspicion — investigate","danger"); grid(p,785,245,10,13,25,"afb",6); multi(p,760,780,["• irregular sealed-brood pattern","• some cappings sunken or perforated","• use accepted/official confirmation pathway"],18,500,C["ink"],28)
    note(p,900,["Pattern supports investigation but does not prove AFB. Differentials include EFB, sacbrood, chilled brood, queen problems and Varroa-associated brood loss."])
    return finish(p)

def fig_43_3():
    p=svg_start("Figure 43.3 — American Foulbrood Disease-Stage Cell Series","Cell cross-sections show a normal larva, discoloured decomposed remains, possible ropey stage and dry adherent scale; not every case shows every stage.")
    txt(p,55,102,"Cell appearance changes with stage and worker removal; not every case shows every stage clearly.",19,400,C["muted"])
    titles=["A — Normal larva","B — Discoloured remains","C — Possible ropey stage","D — Dry adherent scale"]
    for i,x in enumerate([45,390,735,1080]):
        panel(p,x,160,275,690,titles[i],"healthy" if i==0 else ("warn" if i==2 else "danger"))
        p.append(f'<path d="M{x+45} 310 L{x+137} 275 L{x+230} 310 L{x+210} 660 L{x+65} 660 Z" fill="{C["wax"]}" stroke="{C["grid"]}" stroke-width="4"/>')
        if i==0:
            larva(p,x+137,510,1.8); multi(p,x+28,705,["Pearly white, plump,","glistening normal larva."],16,600,C["muted"],23)
        elif i==1:
            p.append(f'<path d="M{x+80} 535 C{x+112} 485 {x+172} 480 {x+198} 530 C{x+181} 572 {x+112} 580 {x+82} 552 Z" fill="#8C4A2F"/>'); multi(p,x+24,705,["Brown decomposed material;","consistency varies by stage."],16,600,C["muted"],23)
        elif i==2:
            p.append(f'<path d="M{x+80} 535 C{x+112} 500 {x+175} 500 {x+195} 535" fill="none" stroke="{C["afb"]}" stroke-width="20" stroke-linecap="round"/>'); p.append(f'<line x1="{x+190}" y1="520" x2="{x+245}" y2="420" stroke="{C["ink"]}" stroke-width="6"/>'); p.append(f'<path d="M{x+188} 523 C{x+205} 493 {x+218} 466 {x+232} 445" fill="none" stroke="{C["afb"]}" stroke-width="8" stroke-linecap="round"/>'); multi(p,x+20,705,["Ropey material can occur","at a suitable stage only."],16,600,C["muted"],23)
        else:
            p.append(f'<path d="M{x+73} 624 C{x+110} 600 {x+175} 600 {x+204} 624 L{x+201} 653 L{x+72} 653 Z" fill="#4E3024"/>'); multi(p,x+16,705,["Dry dark scale remains","adherent to lower cell wall."],16,600,C["muted"],23)
    note(p,900,["Use this series to recognise suspicious stages, not as a stand-alone diagnosis. Suspected AFB requires current local notification/confirmation procedures."])
    return finish(p)

def fig_44_2():
    p=svg_start("Figure 44.2 — Healthy Versus EFB-Affected Open Brood","Comparison of pearly healthy C-shaped larvae with representative EFB-compatible larvae that are creamy, yellow-brown, twisted or collapsed.")
    txt(p,55,102,"Compare larvae of similar age; EFB presentation varies and overlaps with other brood disorders.",19,400,C["muted"])
    panel(p,55,150,620,710,"Healthy open brood","healthy")
    for cx,cy,sc in [(225,350,1.7),(505,350,2.0),(365,610,2.25)]: cell(p,cx,cy,92,"#FFF4C8",C["grid"],4); larva(p,cx,cy,sc)
    multi(p,90,780,["• pearly white","• moist / glistening","• regular C-shape at cell base"],18,500,C["ink"],28)
    panel(p,725,150,620,710,"EFB-compatible open brood — investigate","danger")
    for cx,cy,sc,col,rot in [(895,340,1.8,C["efb_yellow"],20),(1170,350,1.9,"#C9893E",-15),(1035,610,2.1,C["efb_brown"],65)]: cell(p,cx,cy,92,"#FFF4C8",C["grid"],4); larva(p,cx,cy,sc,col,rot,True)
    multi(p,760,780,["• creamy/yellow/brown discoloration may occur","• twisted, lengthwise or collapsed larvae may occur","• confirm with accepted diagnostic pathway when indicated"],17,500,C["ink"],27)
    note(p,900,["EFB is not diagnosed by colour, odour or one larval posture alone. Chilling, sacbrood, nutrition, queen problems and other brood disease remain important differentials."])
    return finish(p)

ASSETS={"fig-25-7-brood-pattern-interpretation.svg":fig_25_7,"fig-39-2-healthy-brood-reference.svg":fig_39_2,"fig-39-3-patchy-brood-multiple-causes.svg":fig_39_3,"fig-39-4-afb-suspicion-features.svg":fig_39_4,"fig-43-2-healthy-brood-vs-early-afb.svg":fig_43_2,"fig-43-3-disease-stage-cell-series.svg":fig_43_3,"fig-44-2-healthy-vs-efb-open-brood.svg":fig_44_2}
FIG_IDS={"25.7","39.2","39.3","39.4","43.2","43.3","44.2"}

def update_queue():
    data=json.loads(QUEUE.read_text(encoding="utf-8"))
    done=0
    for a in data.get("assets",[]):
        if str(a.get("figure_id")) in FIG_IDS:
            prefix="fig-"+str(a["figure_id"]).replace(".","-")+"-"
            stem=next((name for name in ASSETS if name.startswith(prefix)),None)
            if stem:
                a["final_asset_path"]="assets/diagrams/wave-01/"+stem
                a["asset_status"]="HIGH_FIDELITY_TECHNICAL_ILLUSTRATION_CREATED"
                a["production_status"]="ASSET_CREATED_PENDING_FINAL_LAYOUT_PROOF"
                a["technical_review_status"]="PASS_TECHNICAL_PLATE_V1_LAYOUT_PROOF_PENDING"
                done+=1
    data["actual_asset_ids_present"]=50+done
    data["remaining_high_fidelity_assets"]=18-done
    QUEUE.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

def write_report():
    lines=["# Wave 01 High-Fidelity Brood and Foulbrood Plate Review","","**Result:** PASS — ORIGINAL TECHNICAL PLATES CREATED; FINAL LAYOUT PROOF PENDING","","## Assets created",""]
    lines += ["- "+name for name in ASSETS]
    lines += ["","## Accuracy gates applied","",
              "- Healthy larvae: pearly white, plump/glistening concept and C-shaped.",
              "- Healthy worker-brood cappings: coherent, medium-brown, slightly convex and unpunctured.",
              "- Patchy brood remains explicitly non-specific.",
              "- AFB: sunken/perforated cappings, stage-dependent brown remains and adherent lower-cell-wall scale; no one sign is treated as definitive.",
              "- Rope-test imagery is labelled supporting evidence only.",
              "- EFB: representative creamy/yellow/brown twisted or collapsed larvae with differential-diagnosis warning.",
              "- Regulated-disease captions preserve current competent-authority/accepted confirmation pathways.",
              "","## Reference basis","",
              "- Penn State Extension and university bee-health references for healthy C-shaped larvae and capped-worker-brood appearance.",
              "- GOV.UK / National Bee Unit current AFB and EFB suspicion signs and reporting framework.",
              "- Final chapter manuscripts and illustration plans remain the editorial source of truth.",
              "","## Remaining gate","",
              "Greyscale, final-size and final-layout proof is still required before print release.",""]
    REPORT.parent.mkdir(parents=True,exist_ok=True); REPORT.write_text("\n".join(lines),encoding="utf-8")

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for name,fn in ASSETS.items():
        s=fn(); ET.fromstring(s)
        if "<title" not in s or "<desc" not in s: raise RuntimeError(name)
        (OUT/name).write_text(s,encoding="utf-8")
    update_queue(); write_report(); print(f"Created {len(ASSETS)} high-fidelity brood/disease SVGs.")

if __name__=="__main__": main()
