#!/usr/bin/env python3
from __future__ import annotations
import json, math
from pathlib import Path
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"assets"/"diagrams"/"wave-02"
META=ROOT/"assets"/"production-briefs"/"wave-02-apiary-equipment-d.json"
REPORT=ROOT/"docs"/"reviews"/"VISUAL_WAVE_02_APIARY_EQUIPMENT_D_REVIEW.md"
W,H=1400,1000
FONT="Arial,Helvetica,sans-serif"
C={"ink":"#1F2933","muted":"#52606D","blue":"#1565C0","blue_light":"#E3F2FD","green":"#2E7D32","green_light":"#E8F5E9","orange":"#EF6C00","orange_light":"#FFF3E0","red":"#C62828","red_light":"#FFEBEE","purple":"#6A1B9A","purple_light":"#F3E5F5","honey":"#D4A017","honey_light":"#FFF8E1","brown":"#8D6E63","grey":"#757575","grey_light":"#F5F5F5","wax":"#F4E7A1","wood":"#D9B57C","metal":"#90A4AE"}

def start(title,desc):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title>',f'<desc id="desc">{escape(desc)}</desc>',
            '<defs>',
            f'<marker id="ab" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="{C["blue"]}"/></marker>',
            f'<marker id="ag" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="{C["green"]}"/></marker>',
            f'<marker id="ao" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="{C["orange"]}"/></marker>',
            '</defs>',
            f'<rect width="{W}" height="{H}" fill="#fff"/>',
            f'<text x="55" y="60" font-family="{FONT}" font-size="34" font-weight="700" fill="{C["ink"]}">{escape(title)}</text>']
def finish(p): p.append("</svg>"); return "\n".join(p)+"\n"
def text(p,x,y,s,size=18,weight=400,fill=None,anchor="start"): p.append(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill or C["ink"]}" text-anchor="{anchor}">{escape(s)}</text>')
def multi(p,x,y,lines,size=16,weight=400,fill=None,lead=23,anchor="start"):
    for i,s in enumerate(lines): text(p,x,y+i*lead,s,size,weight,fill,anchor)
def rect(p,x,y,w,h,fill,stroke,sw=2,r=18): p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def panel(p,x,y,w,h,title,kind="blue"):
    pal={"blue":(C["blue_light"],C["blue"]),"green":(C["green_light"],C["green"]),"orange":(C["orange_light"],C["orange"]),"red":(C["red_light"],C["red"]),"purple":(C["purple_light"],C["purple"]),"honey":(C["honey_light"],C["brown"]),"grey":(C["grey_light"],C["grey"])}
    fill,stroke=pal[kind]; rect(p,x,y,w,h,fill,stroke,2.5,18); text(p,x+18,y+31,title,20,700,stroke)
def arrow(p,x1,y1,x2,y2,color="blue",width=4):
    col={"blue":C["blue"],"green":C["green"],"orange":C["orange"]}[color]; marker={"blue":"ab","green":"ag","orange":"ao"}[color]
    p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{width}" marker-end="url(#{marker})"/>')
def note(p,y,lines,kind="orange"):
    pal={"orange":(C["orange_light"],C["orange"]),"blue":(C["blue_light"],C["blue"]),"green":(C["green_light"],C["green"])}
    fill,stroke=pal[kind]; rect(p,55,y,1290,80,fill,stroke,2.5,14); multi(p,78,y+29,lines,17,600,C["ink"],23)
def hive(p,x,y,w=170,h=250,boxes=2):
    bh=h/boxes
    for i in range(boxes): rect(p,x,y+i*bh,w,bh,C["wood"],C["brown"],3,4)
    rect(p,x-10,y-25,w+20,28,"#CFBE9A",C["brown"],3,3); rect(p,x+15,y+h,w-30,18,"#CFBE9A",C["brown"],3,3)
    p.append(f'<rect x="{x+w*0.3}" y="{y+h-12}" width="{w*0.4}" height="12" fill="#3A2D24"/>')
def frame(p,x,y,w=150,h=360):
    rect(p,x,y,w,h,"#FFFBEA",C["brown"],4,3); p.append(f'<line x1="{x+15}" y1="{y+25}" x2="{x+w-15}" y2="{y+25}" stroke="{C["honey"]}" stroke-width="7"/>')
def tool_icon(p,cx,cy,kind):
    if kind=="smoker":
        rect(p,cx-40,cy-55,80,110,"#B0BEC5","#546E7A",3,18); p.append(f'<path d="M{cx} {cy-55} L{cx+30} {cy-105} L{cx+70} {cy-120}" fill="none" stroke="#546E7A" stroke-width="14"/>')
    elif kind=="hive_tool":
        p.append(f'<path d="M{cx-65} {cy+15} L{cx+55} {cy-25} L{cx+65} {cy} L{cx-55} {cy+40} Z" fill="#A9B4BD" stroke="#4E5964" stroke-width="3"/>')
    elif kind=="veil":
        p.append(f'<circle cx="{cx}" cy="{cy-25}" r="42" fill="#F6D9BA" stroke="{C["brown"]}" stroke-width="3"/><path d="M{cx-70} {cy-60} Q{cx} {cy-130} {cx+70} {cy-60} L{cx+85} {cy+40} L{cx-85} {cy+40} Z" fill="none" stroke="#455A64" stroke-width="4" stroke-dasharray="7 5"/>')
    elif kind=="feeder":
        rect(p,cx-60,cy-55,120,110,"#E3F2FD",C["blue"],3,10); p.append(f'<line x1="{cx}" y1="{cy-50}" x2="{cx}" y2="{cy+45}" stroke="#90CAF9" stroke-width="5"/>')
    elif kind=="record":
        rect(p,cx-48,cy-75,96,150,"#FAFAFA","#455A64",4,18); p.append(f'<line x1="{cx-28}" y1="{cy-35}" x2="{cx+28}" y2="{cy-35}" stroke="{C["blue"]}" stroke-width="3"/><line x1="{cx-28}" y1="{cy}" x2="{cx+28}" y2="{cy}" stroke="{C["blue"]}" stroke-width="3"/>')
    elif kind=="brush":
        p.append(f'<line x1="{cx-65}" y1="{cy}" x2="{cx+20}" y2="{cy}" stroke="{C["brown"]}" stroke-width="14"/>'); rect(p,cx+15,cy-35,60,70,"#F7E4A6",C["brown"],2,4)
    elif kind=="wash":
        p.append(f'<circle cx="{cx}" cy="{cy}" r="55" fill="#E3F2FD" stroke="{C["purple"]}" stroke-width="4"/>'); text(p,cx,cy+5,"mites",16,700,C["purple"],"middle")
def tag(p,x,y,site,colony):
    rect(p,x,y,210,90,"#FFF",C["blue"],3,10); text(p,x+15,y+32,site,15,700,C["blue"]); text(p,x+15,y+62,colony,20,700,C["ink"])

def fig_16_1():
    p=start("Figure 16.1 — Small Apiary Layout","Example small-apiary plan showing staggered hive entrances, landmarks, working aisle, vehicle approach and emergency access.")
    text(p,55,100,"Example layout only; statutory spacing and site rules vary by jurisdiction and property.",18,400,C["muted"])
    rect(p,60,150,1280,690,"#F8FBF4","#90A4AE",2,22)
    # vehicle lane
    rect(p,80,680,1240,100,"#ECEFF1","#90A4AE",2,10); text(p,700,740,"vehicle / emergency access",18,700,C["grey"],"middle")
    # hives staggered
    coords=[(150,250,0),(390,320,1),(650,245,0),(920,325,1)]
    for i,(x,y,flip) in enumerate(coords):
        hive(p,x,y,150,210,2)
        # flight direction
        sx=x+75; sy=y+200
        ex=sx+(-90 if flip else 90); ey=sy+130
        arrow(p,sx,sy,ex,ey,"green",3); text(p,x+75,y-12,f"H{i+1}",15,700,C["blue"],"middle")
    # landmarks
    for x,y in [(330,210),(600,400),(1080,235)]: p.append(f'<circle cx="{x}" cy="{y}" r="38" fill="#72A765"/><rect x="{x-5}" y="{y+30}" width="10" height="55" fill="#7C5A38"/>')
    # working aisle
    p.append(f'<path d="M110 600 L1180 600" stroke="{C["blue"]}" stroke-width="5" stroke-dasharray="12 8"/>'); text(p,650,585,"working aisle",16,700,C["blue"],"middle")
    note(p,865,["Preserve safe working clearance and a route for emergency access. Entrance orientation and landmarks can also reduce drift and public conflict."],"green")
    return finish(p)
def fig_16_2():
    p=start("Figure 16.2 — Growth Plan","Apiary growth from 1–5 colonies to medium-scale and multiple sites, showing when storage, extraction, transport and record systems become operational constraints.")
    text(p,55,100,"Expansion should follow management capacity, not only the desire to own more colonies.",18,400,C["muted"])
    stages=[("1–5 colonies","manual records","small storage","borrowed/shared extraction possible"),("Medium apiary","dedicated storage","scheduled extraction","transport + spare equipment"),("Multiple sites","site/colony coding","vehicle/logistics planning","batch traceability + labour system")]
    for i,(t,a,b,c) in enumerate(stages):
        x=80+i*440; panel(p,x,180,380,600,t,"green" if i==0 else ("blue" if i==1 else "purple"))
        for k in range(min(5,2+i*2)): hive(p,x+30+k*65,320+(k%2)*35,55,85,1)
        multi(p,x+25,570,[a,b,c],16,600,C["ink"],32)
        if i<2: arrow(p,x+380,480,x+430,480,"blue",4)
    note(p,865,["Growth constraints often appear first in time, storage, transport, disease control and records—not hive availability. Expand only when the operating system can scale."],"orange")
    return finish(p)
def fig_16_5():
    p=start("Figure 16.5 — Apiary Identification System","Site code plus colony code linked to inspection, queen, treatment and harvest records.")
    text(p,55,100,"A stable identity should follow a colony through inspections and treatments even when boxes or supers change.",18,400,C["muted"])
    tag(p,90,220,"SITE: DUB-A","COLONY: DUB-A-07")
    arrow(p,300,265,470,265,"blue",4)
    panel(p,485,160,350,590,"Colony record","blue")
    multi(p,515,225,["DUB-A-07","inspection dates","queen year/source","Varroa results","treatments + active ingredient","feeding / major events"],16,500,C["ink"],40)
    arrow(p,835,455,940,455,"green",4)
    panel(p,955,160,350,590,"Linked outputs","green")
    multi(p,985,225,["harvest lot","sample/lab result","equipment movement","colony sale/move","mortality/dead-out","follow-up action"],16,500,C["ink"],40)
    note(p,865,["Do not use box colour or physical hive position as the only colony identity. Equipment and colony location can change; the record identifier must remain controlled."],"blue")
    return finish(p)
def fig_17_1():
    p=start("Figure 17.1 — Common Movable-Frame Hive Families","Representative modular hive-family silhouettes for Langstroth, National, Dadant and another regional modular system, with proportions labelled as illustrative rather than interchangeable dimensions.")
    text(p,55,100,"Systems are shown conceptually. Use only dimensions and frame sizes defined for the specific named standard.",18,400,C["muted"])
    items=[("Langstroth","vertical modular","blue",3),("National","vertical modular","green",3),("Dadant","deep brood + supers","orange",2),("Regional modular example","local standard varies","purple",3)]
    for i,(name,sub,kind,boxes) in enumerate(items):
        x=65+i*335; panel(p,x,160,290,650,name,kind); hive(p,x+70,300,150,300,boxes); text(p,x+145,650,sub,15,700,C["muted"],"middle")
        multi(p,x+22,700,["frame compatibility depends","on the exact system standard"],14,500,C["ink"],21)
    note(p,865,["Do not mix frame/box dimensions between hive families merely because the equipment looks similar. Local availability and beekeeper ergonomics matter."],"orange")
    return finish(p)
def fig_17_2():
    p=start("Figure 17.2 — Horizontal Versus Vertical Expansion","Vertical stacked hive compared with a horizontal long hive, focusing on management trade-offs rather than declaring a winner.")
    text(p,55,100,"Both systems can house healthy colonies; handling, lifting and expansion workflow differ.",18,400,C["muted"])
    panel(p,55,160,620,650,"Vertical stacked hive","blue"); hive(p,245,280,230,440,4)
    multi(p,95,700,["expansion by adding boxes upward","heavy boxes may require lifting","supers can be removed for extraction","common modular equipment in many regions"],16,500,C["ink"],25)
    panel(p,725,160,620,650,"Horizontal / long hive","green"); rect(p,800,390,460,240,C["wood"],C["brown"],4,6)
    for x in range(830,1230,55): p.append(f'<line x1="{x}" y1="410" x2="{x}" y2="600" stroke="{C["brown"]}" stroke-width="3"/>')
    multi(p,765,700,["expansion along one long body","less vertical box lifting","frame handling can be individual","extraction compatibility depends on frame design"],16,500,C["ink"],25)
    note(p,865,["Choose a system for local equipment availability, management goals, beekeeper physical capacity and compatible processing equipment—not ideology."],"green")
    return finish(p)
def fig_17_4():
    p=start("Figure 17.4 — Hive-System Comparison Matrix","Comparison matrix for frame compatibility, lifting, supering, extraction, natural-comb handling and local equipment availability.")
    text(p,55,100,"Matrix compares management questions, not absolute winners.",18,400,C["muted"])
    cols=["System","Frame compatibility","Lifting","Supering","Extraction","Natural comb","Local availability"]
    widths=[170,190,150,150,160,170,210]; x=50
    xs=[]
    for w,c in zip(widths,cols): xs.append((x,w)); rect(p,x,160,w,80,C["grey_light"],C["grey"],2,6); text(p,x+w/2,205,c,14,700,C["ink"],"middle"); x+=w
    data=[("Vertical modular","standard-specific","box lifts","easy modular","usually strong","foundation or natural","region-dependent"),("Long / horizontal","system-specific","lower box lifting","not always used","frame-dependent","often practical","region-dependent"),("Top-bar / natural-comb","bar-specific","bar-by-bar","not typical","often not centrifugal","central design feature","region-dependent")]
    for r,row in enumerate(data):
        y=260+r*170
        for (x,w),val in zip(xs,row):
            rect(p,x,y,w,140,"#FFFFFF",C["blue"] if r==0 else (C["green"] if r==1 else C["orange"]),1.8,6); text(p,x+w/2,y+75,val,13,600,C["ink"],"middle")
    note(p,865,["A 'best hive' claim is incomplete unless it states the management goal, beekeeper constraints, climate, frame standard and local supply chain."],"orange")
    return finish(p)
def fig_18_1():
    p=start("Figure 18.1 — Exploded Modular Hive","Exploded modular hive showing roof, inner cover, honey supers, optional queen excluder, brood box, floor, entrance and stand.")
    text(p,55,100,"Component order shown for a common vertical modular concept; exact dimensions belong to the chosen hive standard.",18,400,C["muted"])
    cx=540; y=170
    parts=[("Roof",40,"#CFBE9A"),("Inner/crown cover",35,"#EEE1C6"),("Honey super",100,C["wood"]),("Honey super",100,C["wood"]),("Queen excluder — optional",25,"#B0BEC5"),("Brood box",170,"#CFA46A"),("Floor",35,"#BFA376"),("Stand",55,"#8D6E63")]
    for name,hgt,col in parts:
        rect(p,cx-210,y,420,hgt,col,C["brown"],3,4); text(p,770,y+hgt/2+6,name,16,700,C["ink"]); y+=hgt+25
    p.append(f'<rect x="{cx-55}" y="{y-115}" width="110" height="16" fill="#3A2D24"/>'); text(p,770,y-98,"entrance",16,700,C["red"])
    panel(p,975,180,330,560,"Functional layers","blue")
    multi(p,1000,240,["Weather protection","roof + cover","","Crop space","honey supers","","Brood nest","brood box","","Optional control","queen excluder where used","","Base / entrance","floor + stand"],15,500,C["ink"],25)
    note(p,875,["A queen excluder is a management tool, not an essential component of every hive. Do not mix component dimensions from incompatible hive standards."],"orange")
    return finish(p)
def fig_18_2():
    p=start("Figure 18.2 — Frame Spacing and Bee Space","Cross-section contrasting workable bee-space passage with excess spacing that invites brace/burr comb and too-narrow gaps that bees may propolise.")
    text(p,55,100,"Bee space is a functional gap concept; exact target dimensions depend on the hive standard and local equipment tolerances.",18,400,C["muted"])
    cases=[("Too narrow","propolising / restricted passage","red",45),("Functional bee-space range","passage maintained","green",95),("Too wide","brace/burr comb likely","orange",165)]
    for i,(title,sub,kind,gap) in enumerate(cases):
        x=55+i*440; panel(p,x,170,390,630,title,kind)
        rect(p,x+45,330,105,330,C["wood"],C["brown"],4,4); rect(p,x+150+gap,330,105,330,C["wood"],C["brown"],4,4)
        p.append(f'<line x1="{x+150}" y1="285" x2="{x+150+gap}" y2="285" stroke="{C["blue"]}" stroke-width="4"/>'); text(p,x+150+gap/2,265,"gap",15,700,C["blue"],"middle")
        if kind=="red":
            p.append(f'<path d="M{x+150} 490 C{x+165} 460 {x+170} 520 {x+195} 490" fill="none" stroke="#7A4D31" stroke-width="12"/>')
        if kind=="orange":
            p.append(f'<path d="M{x+150} 480 Q{x+225} 410 {x+315} 480 Q{x+225} 560 {x+150} 480" fill="{C["wax"]}" stroke="{C["brown"]}" stroke-width="3"/>')
        multi(p,x+30,710,[sub],16,600,C["ink"],22)
    note(p,865,["Use the frame and box dimensions specified for your hive family. This figure teaches the consequence of bad spacing, not a universal millimetre value."],"blue")
    return finish(p)
def fig_18_3():
    p=start("Figure 18.3 — Floor Types","Solid hive floor compared with screened floor and removable monitoring board, including ventilation and mite-monitoring implications.")
    text(p,55,100,"Floor choice modifies airflow and monitoring access; neither replaces Varroa management.",18,400,C["muted"])
    panel(p,55,160,620,650,"Solid floor","blue"); hive(p,185,290,250,340,2); p.append(f'<rect x="165" y="630" width="290" height="28" fill="#8D6E63"/>')
    multi(p,95,710,["simple closed base","debris accumulates on solid surface","ventilation depends on entrance/other openings"],16,500,C["ink"],25)
    panel(p,725,160,620,650,"Screened floor + monitoring board","green"); hive(p,855,290,250,340,2)
    p.append(f'<rect x="835" y="628" width="290" height="22" fill="#CFD8DC" stroke="#607D8B" stroke-width="3"/>')
    for x in range(850,1120,22): p.append(f'<line x1="{x}" y1="628" x2="{x+10}" y2="650" stroke="#607D8B" stroke-width="1.5"/>')
    p.append(f'<rect x="850" y="690" width="260" height="18" fill="#FFF8E1" stroke="{C["orange"]}" stroke-width="3"/>')
    text(p,980,735,"removable monitoring board",15,700,C["orange"],"middle")
    multi(p,765,775,["screen may increase lower ventilation","board can collect natural/treatment mite fall"],16,500,C["ink"],24)
    note(p,875,["Natural mite fall and screened floors are supporting tools. Quantitative Varroa monitoring and effective control remain necessary."],"orange")
    return finish(p)
def fig_19_1():
    p=start("Figure 19.1 — Frame Anatomy","Movable hive frame labelled with top bar, side bars, bottom bar, foundation or comb guide and optional wire/support.")
    text(p,55,100,"Frame dimensions and reinforcement details must match the selected hive system.",18,400,C["muted"])
    x,y=360,190; w,h=620,610
    rect(p,x,y,w,55,C["wood"],C["brown"],4,4); rect(p,x,y+55,45,h-110,C["wood"],C["brown"],4,4); rect(p,x+w-45,y+55,45,h-110,C["wood"],C["brown"],4,4); rect(p,x,y+h-55,w,55,C["wood"],C["brown"],4,4)
    rect(p,x+55,y+75,w-110,h-150,"#FFF9DE",C["honey"],2,3)
    for yy in [y+180,y+300,y+420,y+540]: p.append(f'<line x1="{x+55}" y1="{yy}" x2="{x+w-55}" y2="{yy}" stroke="#9E9E9E" stroke-width="2"/>')
    labels=[("top bar",x+300,y+28,100,160),("side bar",x+18,y+310,150,520),("bottom bar",x+300,y+h-25,1050,760),("foundation / guide",x+300,y+130,1040,330),("optional wire/support",x+300,y+300,1040,500)]
    for name,sx,sy,tx,ty in labels:
        p.append(f'<line x1="{sx}" y1="{sy}" x2="{tx}" y2="{ty}" stroke="{C["blue"]}" stroke-width="2.5"/>'); text(p,tx+8,ty+5,name,16,700,C["blue"])
    note(p,875,["Foundation authenticity cannot be judged reliably from colour alone. Frame and wire geometry must be compatible with the hive and extraction method."],"blue")
    return finish(p)
def fig_19_4():
    p=start("Figure 19.4 — Straight Natural Comb","Correct vertical guide alignment and full comb attachment contrasted with cross-comb caused by poor alignment or hive level.")
    text(p,55,100,"Fresh natural comb is soft and mechanically vulnerable; guide alignment and hive level strongly affect construction.",18,400,C["muted"])
    panel(p,55,160,620,650,"Straight comb","green")
    rect(p,135,260,460,50,C["wood"],C["brown"],4,3)
    p.append(f'<path d="M365 310 C315 420 325 610 365 690 C405 610 415 420 365 310 Z" fill="{C["wax"]}" stroke="{C["brown"]}" stroke-width="4"/>')
    p.append(f'<line x1="365" y1="220" x2="365" y2="720" stroke="{C["blue"]}" stroke-width="3" stroke-dasharray="9 7"/>')
    text(p,365,760,"guide and gravity aligned",16,700,C["green"],"middle")
    panel(p,725,160,620,650,"Cross-comb failure","red")
    rect(p,805,260,460,50,C["wood"],C["brown"],4,3)
    p.append(f'<path d="M940 310 C1040 390 1090 570 1190 690 C1110 690 965 610 900 500 C860 430 875 350 940 310 Z" fill="{C["wax"]}" stroke="{C["brown"]}" stroke-width="4"/>')
    p.append(f'<line x1="1035" y1="220" x2="1035" y2="720" stroke="{C["blue"]}" stroke-width="3" stroke-dasharray="9 7"/>')
    text(p,1035,760,"comb departs from guide",16,700,C["red"],"middle")
    note(p,875,["Never rotate or lay heavy new foundationless comb flat in hot conditions unless supported; comb can tear or collapse before wax fully melts."],"orange")
    return finish(p)
def fig_19_5():
    p=start("Figure 19.5 — Comb Age Sequence","Fresh honey comb to increasingly used brood comb with cocoon accumulation, illustrating why comb history changes colour, cell interior and residue load.")
    text(p,55,100,"Darkening is multi-causal; colour alone does not prove pesticide contamination or disease.",18,400,C["muted"])
    stages=[("Fresh comb","#FFF3B0","new wax / no brood cocoons"),("Used honey comb","#F1D277","propolis/pollen staining possible"),("Brood comb — several cycles","#C99459","cocoon layers accumulate"),("Old brood comb","#76513A","more cocoon/debris history; residue risk can rise")]
    for i,(t,col,sub) in enumerate(stages):
        x=60+i*335; panel(p,x,170,290,630,t,"honey" if i<2 else "orange")
        for rr in range(5):
            for cc in range(4):
                cx=x+55+cc*60+(rr%2)*30; cy=330+rr*70
                p.append(f'<polygon points="{cx},{cy-28} {cx+24},{cy-14} {cx+24},{cy+14} {cx},{cy+28} {cx-24},{cy+14} {cx-24},{cy-14}" fill="{col}" stroke="{C["brown"]}" stroke-width="{2+i*0.4}"/>')
        multi(p,x+22,720,[sub],14,500,C["ink"],21)
    note(p,875,["Comb replacement decisions should use history, condition, disease/residue risk and management goals—not a colour threshold alone."],"blue")
    return finish(p)
def fig_20_1():
    p=start("Figure 20.1 — Beginner Equipment Set","Core beginner equipment grouped as protective gear, hive-opening tools, feeding/handling items, records and basic spares.")
    text(p,55,100,"The essential set is task-based; optional gadgets are not mandatory beginner equipment.",18,400,C["muted"])
    items=[("Veil / suit","veil"),("Smoker","smoker"),("Hive tool","hive_tool"),("Brush","brush"),("Feeder","feeder"),("Record system","record")]
    for i,(lab,kind) in enumerate(items):
        row=i//3; col=i%3; x=90+col*420; y=180+row*330; panel(p,x,y,350,270,lab,"blue" if i<3 else "green"); tool_icon(p,x+175,y+140,kind)
    note(p,875,["Add gloves, spare boxes/frames, first-aid and task-specific tools according to colony temperament, hive system, health plan and local conditions."],"orange")
    return finish(p)
def fig_20_2():
    p=start("Figure 20.2 — Equipment by Task","Beekeeping equipment grouped by inspection, feeding, swarm capture, queen work, Varroa monitoring, harvest and processing.")
    text(p,55,100,"Organising by task prevents overbuying and makes missing safety/food-contact controls obvious.",18,400,C["muted"])
    groups=[("Inspection",["veil/PPE","smoker","hive tool","records"],"blue"),("Feeding",["food-grade feeder","clean mixing container","scale"],"green"),("Swarm capture",["box/container","sheet/brush","PPE"],"orange"),("Queen work",["cage","marking tools","magnification if needed"],"purple"),("Varroa monitoring",["sampling jar","wash/sugar-roll equipment","count record"],"purple"),("Harvest/processing",["covers","food-grade containers","refractometer","extractor/strainers"],"honey")]
    for i,(t,vals,k) in enumerate(groups):
        row=i//3; col=i%3; x=60+col*440; y=170+row*350; panel(p,x,y,390,290,t,k); multi(p,x+25,y+95,["• "+v for v in vals],15,500,C["ink"],30)
    note(p,885,["Food-contact harvest/processing tools should remain visibly and physically separate from dirty field tools and disease-suspect equipment."],"green")
    return finish(p)
def fig_20_4():
    p=start("Figure 20.4 — Clean Equipment Workflow","Controlled streams separating routine apiary tools, honey-room food-contact tools and disease-suspect tools to reduce cross-contamination.")
    text(p,55,100,"The safest workflow prevents suspect equipment from crossing into clean food or healthy-colony streams.",18,400,C["muted"])
    streams=[("Routine apiary tools","field use → clean/decontaminate as required → return to field","blue"),("Honey-room tools","food-contact use → food-safe cleaning → dry protected storage","green"),("Disease-suspect tools","isolate → pathogen-appropriate decontamination/disposition → release only when safe","red")]
    for i,(t,sub,k) in enumerate(streams):
        y=175+i*220; panel(p,70,y,1260,175,t,k)
        multi(p,100,y+80,[sub],16,600,C["ink"],24)
        arrow(p,430,y+120,560,y+120,"blue" if k!="red" else "orange",3); arrow(p,880,y+120,1020,y+120,"green" if k=="green" else "blue",3)
    note(p,875,["No single disinfectant or cleaning method is universal. Match decontamination to the suspected pathogen, material, food-contact status and current official guidance."],"orange")
    return finish(p)

ASSETS={
"fig-16-1-small-apiary-layout.svg":fig_16_1,
"fig-16-2-growth-plan.svg":fig_16_2,
"fig-16-5-apiary-identification-system.svg":fig_16_5,
"fig-17-1-common-movable-frame-hives.svg":fig_17_1,
"fig-17-2-horizontal-vs-vertical-expansion.svg":fig_17_2,
"fig-17-4-hive-system-comparison-matrix.svg":fig_17_4,
"fig-18-1-exploded-modular-hive.svg":fig_18_1,
"fig-18-2-frame-spacing-bee-space.svg":fig_18_2,
"fig-18-3-floor-types.svg":fig_18_3,
"fig-19-1-frame-anatomy.svg":fig_19_1,
"fig-19-4-straight-natural-comb.svg":fig_19_4,
"fig-19-5-comb-age-sequence.svg":fig_19_5,
"fig-20-1-beginner-equipment-set.svg":fig_20_1,
"fig-20-2-equipment-by-task.svg":fig_20_2,
"fig-20-4-clean-equipment-workflow.svg":fig_20_4,
}
def write_meta():
    data={"wave":2,"batch":"apiary-equipment-d","asset_count":len(ASSETS),"assets":[]}
    for name in ASSETS:
        parts=name.split("-"); fid=f"{int(parts[1])}.{int(parts[2])}"
        data["assets"].append({"figure_id":fid,"path":"assets/diagrams/wave-02/"+name,"status":"ACTUAL_VECTOR_CREATED","layout_status":"PENDING_FINAL_LAYOUT_PROOF"})
    META.parent.mkdir(parents=True,exist_ok=True); META.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
def write_report():
    lines=["# Visual Wave 02 — Apiary and Equipment D Review","","**Result:** PASS — A_CORE APIARY / HIVE / FRAME / EQUIPMENT BATCH CREATED","","## Assets created",""]
    lines += ["- "+n for n in ASSETS]
    lines += ["","## Editorial controls","",
              "- Apiary layouts are examples rather than statutory spacing rules and preserve access/safety logic.",
              "- Growth planning shows storage, extraction, transport and records as scaling constraints.",
              "- Colony/site identification is record-driven rather than dependent on physical box position.",
              "- Hive-family figures explicitly avoid mixing dimensions and avoid declaring a universal winner.",
              "- Bee-space graphic teaches consequences without inventing one universal millimetre value.",
              "- Screened floors are not presented as a Varroa-control substitute.",
              "- Foundationless comb is shown as mechanically vulnerable while fresh/warm.",
              "- Comb age is separated from colour-only contamination claims.",
              "- Beginner equipment is task-based and excludes optional gadgets as mandatory.",
              "- Food-contact, routine field and disease-suspect tool streams are separated.",
              "","## Remaining gates","","Final print-size, greyscale, accessibility and layout proof remain required.",""]
    REPORT.parent.mkdir(parents=True,exist_ok=True); REPORT.write_text("\n".join(lines),encoding="utf-8")
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for name,fn in ASSETS.items():
        s=fn(); ET.fromstring(s)
        if "<title" not in s or "<desc" not in s: raise RuntimeError(name)
        (OUT/name).write_text(s,encoding="utf-8")
    write_meta(); write_report(); print(f"Created {len(ASSETS)} Wave 02 Apiary/Equipment D SVGs.")
if __name__=="__main__": main()
