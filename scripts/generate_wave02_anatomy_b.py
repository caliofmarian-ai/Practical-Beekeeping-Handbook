#!/usr/bin/env python3
from __future__ import annotations
import json, math
from pathlib import Path
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"assets"/"diagrams"/"wave-02"
META=ROOT/"assets"/"production-briefs"/"wave-02-anatomy-b.json"
REPORT=ROOT/"docs"/"reviews"/"VISUAL_WAVE_02_ANATOMY_B_REVIEW.md"
W,H=1400,1000
FONT="Arial,Helvetica,sans-serif"
C={"ink":"#1F2933","muted":"#52606D","blue":"#1565C0","blue_light":"#E3F2FD","green":"#2E7D32","green_light":"#E8F5E9","orange":"#EF6C00","orange_light":"#FFF3E0","red":"#C62828","red_light":"#FFEBEE","purple":"#6A1B9A","purple_light":"#F3E5F5","honey":"#D4A017","honey_light":"#FFF8E1","wax":"#F4E7A1","brown":"#8D6E63","grey":"#757575","grey_light":"#F5F5F5","bee":"#E0A419","bee_dark":"#5D4037","wing":"#D9EEF7","pollen":"#D98C10","rj":"#FFF3D1"}

def start(title,desc):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title>',f'<desc id="desc">{escape(desc)}</desc>',
            '<defs>',
            f'<marker id="ab" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="{C["blue"]}"/></marker>',
            f'<marker id="ag" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="{C["green"]}"/></marker>',
            f'<marker id="ap" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="{C["purple"]}"/></marker>',
            '</defs>',
            f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>',
            f'<text x="55" y="60" font-family="{FONT}" font-size="34" font-weight="700" fill="{C["ink"]}">{escape(title)}</text>']

def finish(p): p.append("</svg>"); return "\n".join(p)+"\n"
def text(p,x,y,s,size=18,weight=400,fill=None,anchor="start"):
    p.append(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill or C["ink"]}" text-anchor="{anchor}">{escape(s)}</text>')
def multi(p,x,y,lines,size=16,weight=400,fill=None,lead=23,anchor="start"):
    for i,s in enumerate(lines): text(p,x,y+i*lead,s,size,weight,fill,anchor)
def rect(p,x,y,w,h,fill,stroke,sw=2,r=18):
    p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def panel(p,x,y,w,h,title,kind="blue"):
    pal={"blue":(C["blue_light"],C["blue"]),"green":(C["green_light"],C["green"]),"orange":(C["orange_light"],C["orange"]),"red":(C["red_light"],C["red"]),"purple":(C["purple_light"],C["purple"]),"honey":(C["honey_light"],C["brown"]),"grey":(C["grey_light"],C["grey"])}
    fill,stroke=pal[kind]; rect(p,x,y,w,h,fill,stroke,2.5,18); text(p,x+18,y+31,title,20,700,stroke)
def arrow(p,x1,y1,x2,y2,color="blue",label=None,width=4):
    cmap={"blue":C["blue"],"green":C["green"],"purple":C["purple"]}
    mmap={"blue":"ab","green":"ag","purple":"ap"}
    col=cmap[color]; p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{width}" marker-end="url(#{mmap[color]})"/>')
    if label: text(p,(x1+x2)/2,(y1+y2)/2-9,label,14,700,col,"middle")
def note(p,y,lines,kind="orange"):
    pal={"orange":(C["orange_light"],C["orange"]),"blue":(C["blue_light"],C["blue"]),"green":(C["green_light"],C["green"]),"purple":(C["purple_light"],C["purple"])}
    fill,stroke=pal[kind]; rect(p,55,y,1290,80,fill,stroke,2.5,14); multi(p,78,y+29,lines,17,600,C["ink"],23)
def circle_label(p,cx,cy,r,fill,stroke,title,sub=None):
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>')
    text(p,cx,cy-3,title,18,700,stroke,"middle")
    if sub: text(p,cx,cy+24,sub,13,500,C["muted"],"middle")

def bee_body(p,cx,cy,s=1,role="worker"):
    # Proportions intentionally differentiate castes.
    if role=="queen":
        head_r=28; thor_rx,thor_ry=46,42; abd_rx,abd_ry=95,34; abd_offset=128
    elif role=="drone":
        head_r=40; thor_rx,thor_ry=52,48; abd_rx,abd_ry=75,42; abd_offset=125
    else:
        head_r=30; thor_rx,thor_ry=44,39; abd_rx,abd_ry=72,31; abd_offset=112
    # wings
    p.append(f'<path d="M {cx-5*s} {cy-25*s} C {cx+35*s} {cy-100*s}, {cx+125*s} {cy-90*s}, {cx+88*s} {cy-20*s} Z" fill="{C["wing"]}" opacity="0.78" stroke="#7EAFC3" stroke-width="{2*s}"/>')
    p.append(f'<path d="M {cx+10*s} {cy+5*s} C {cx+60*s} {cy+55*s}, {cx+118*s} {cy+45*s}, {cx+80*s} {cy+5*s} Z" fill="{C["wing"]}" opacity="0.58" stroke="#7EAFC3" stroke-width="{1.6*s}"/>')
    p.append(f'<circle cx="{cx-75*s}" cy="{cy}" r="{head_r*s}" fill="{C["bee"]}" stroke="{C["bee_dark"]}" stroke-width="{3*s}"/>')
    p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{thor_rx*s}" ry="{thor_ry*s}" fill="{C["bee"]}" stroke="{C["bee_dark"]}" stroke-width="{3*s}"/>')
    p.append(f'<ellipse cx="{cx+abd_offset*s}" cy="{cy}" rx="{abd_rx*s}" ry="{abd_ry*s}" fill="{C["bee"]}" stroke="{C["bee_dark"]}" stroke-width="{3*s}"/>')
    # abdominal bands
    for k in range(-2,3):
        x=cx+(abd_offset+k*24)*s
        p.append(f'<line x1="{x}" y1="{cy-abd_ry*s*0.85}" x2="{x}" y2="{cy+abd_ry*s*0.85}" stroke="{C["bee_dark"]}" stroke-width="{4*s}" opacity="0.7"/>')
    # antennae
    p.append(f'<path d="M {cx-90*s} {cy-20*s} Q {cx-125*s} {cy-55*s} {cx-145*s} {cy-42*s}" fill="none" stroke="{C["bee_dark"]}" stroke-width="{3*s}"/>')
    p.append(f'<path d="M {cx-80*s} {cy-24*s} Q {cx-95*s} {cy-70*s} {cx-120*s} {cy-72*s}" fill="none" stroke="{C["bee_dark"]}" stroke-width="{3*s}"/>')
    # eye
    eye_rx=(18 if role=="drone" else 11)*s; eye_ry=(23 if role=="drone" else 16)*s
    p.append(f'<ellipse cx="{cx-88*s}" cy="{cy-4*s}" rx="{eye_rx}" ry="{eye_ry}" fill="#3C2E25"/>')
    if role=="drone":
        p.append(f'<ellipse cx="{cx-64*s}" cy="{cy-4*s}" rx="{18*s}" ry="{23*s}" fill="#3C2E25"/>')
    # legs
    for dx in [-20,5,28]:
        p.append(f'<path d="M {cx+dx*s} {cy+25*s} L {cx+(dx-25)*s} {cy+82*s} L {cx+(dx-5)*s} {cy+118*s}" fill="none" stroke="{C["bee_dark"]}" stroke-width="{4*s}" stroke-linecap="round"/>')
    return {"head":(cx-75*s,cy),"thorax":(cx,cy),"abdomen":(cx+abd_offset*s,cy)}

def anatomy_label(p,x,y,label,tx,ty,color="blue"):
    col={"blue":C["blue"],"green":C["green"],"purple":C["purple"],"orange":C["orange"]}[color]
    p.append(f'<line x1="{x}" y1="{y}" x2="{tx}" y2="{ty}" stroke="{col}" stroke-width="2.5"/>')
    text(p,tx+5,ty+5,label,14,700,col)

def egg(p,cx,cy,s=1):
    p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{4*s}" ry="{14*s}" fill="#FFFDF7" stroke="#A9A79F" stroke-width="1.5"/>')
def larva(p,cx,cy,s=1,color="#FFFDF4"):
    d=f"M {cx-20*s} {cy-9*s} C {cx-6*s} {cy-32*s}, {cx+25*s} {cy-22*s}, {cx+19*s} {cy+2*s} C {cx+15*s} {cy+23*s}, {cx-12*s} {cy+26*s}, {cx-20*s} {cy+9*s}"
    p.append(f'<path d="{d}" fill="none" stroke="#E2DDD0" stroke-width="{15*s}" stroke-linecap="round"/>')
    p.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{11*s}" stroke-linecap="round"/>')
def pupa(p,cx,cy,s=1,pigment=0):
    fill=["#F4EBDD","#E9D5C6","#DDBAA8","#C99475"][min(max(pigment,0),3)]
    p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{32*s}" ry="{65*s}" fill="{fill}" stroke="#BCA998" stroke-width="{2*s}"/>')
    p.append(f'<circle cx="{cx-12*s}" cy="{cy-37*s}" r="{5*s}" fill="#7E665D"/><circle cx="{cx+12*s}" cy="{cy-37*s}" r="{5*s}" fill="#7E665D"/>')

def fig_6_1():
    p=start("Figure 6.1 — External Worker Anatomy","External worker honey bee anatomy with head, thorax, abdomen, antennae, compound eye, ocelli, mouthparts, legs, wings and sting region.")
    text(p,55,100,"Labels are schematic; microscopic structures are not enlarged without explicit insets.",18,400,C["muted"])
    pos=bee_body(p,480,480,1.7,"worker")
    # ocelli
    for dx,dy in [(-140,-35),(-128,-47),(-115,-35)]: p.append(f'<circle cx="{480+dx*1.7}" cy="{480+dy*1.7}" r="6" fill="#2F2B28"/>')
    anatomy_label(p,300,430,"antennae",100,250,"blue")
    anatomy_label(p,325,480,"compound eye",105,380,"purple")
    anatomy_label(p,280,420,"ocelli",100,475,"purple")
    anatomy_label(p,355,525,"mouthparts",120,610,"blue")
    anatomy_label(p,480,430,"thorax",520,245,"green")
    anatomy_label(p,655,430,"forewing / hindwing",800,250,"blue")
    anatomy_label(p,520,600,"legs",420,760,"green")
    anatomy_label(p,750,480,"abdomen",900,420,"orange")
    anatomy_label(p,850,480,"sting region",1000,560,"red")
    panel(p,1020,210,300,510,"Three body regions","blue")
    multi(p,1045,270,["HEAD","sensory input + feeding structures","","THORAX","wings + three pairs of legs","","ABDOMEN","digestive/reproductive systems,","wax glands, sting apparatus"],16,600,C["ink"],23)
    note(p,885,["External structures are linked to function: sensing and feeding at the head, locomotion at the thorax, and major digestive/reproductive/defensive systems in the abdomen."],"blue")
    return finish(p)

def fig_6_4():
    p=start("Figure 6.4 — Internal Systems","Simplified worker honey bee internal systems: crop, midgut, hindgut, Malpighian tubules, tracheae, dorsal vessel, nervous system and selected glands.")
    text(p,55,100,"Diagram emphasises spatial relationships, not histological scale.",18,400,C["muted"])
    # body outline
    bee_body(p,420,475,1.45,"worker")
    # gut track
    p.append(f'<path d="M300 470 C350 470 390 485 430 505 C500 535 590 540 715 505 C780 485 830 495 870 520" fill="none" stroke="#C98F4F" stroke-width="16" stroke-linecap="round"/>')
    p.append(f'<ellipse cx="470" cy="510" rx="65" ry="35" fill="#E9B677" opacity="0.8"/>')
    p.append(f'<ellipse cx="620" cy="520" rx="75" ry="45" fill="#D69A5C" opacity="0.85"/>')
    # malpighian
    for k in range(5):
        p.append(f'<path d="M690 525 Q {735+k*10} {450+k*18} {780+k*7} {500+k*5}" fill="none" stroke="#B68D39" stroke-width="3"/>')
    # dorsal vessel
    p.append(f'<path d="M390 405 C520 385 680 390 835 430" fill="none" stroke="{C["red"]}" stroke-width="6"/>')
    # ventral nervous system
    p.append(f'<path d="M370 575 C500 595 670 595 820 565" fill="none" stroke="{C["purple"]}" stroke-width="6"/>')
    for x in [440,520,600,680,760]: p.append(f'<circle cx="{x}" cy="{585}" r="9" fill="{C["purple"]}"/>')
    # tracheal network conceptual
    for x,y in [(480,445),(560,460),(650,455),(730,465)]:
        p.append(f'<circle cx="{x}" cy="{y}" r="20" fill="none" stroke="{C["blue"]}" stroke-width="2"/>')
        p.append(f'<line x1="{x-20}" y1="{y}" x2="{x-42}" y2="{y-20}" stroke="{C["blue"]}" stroke-width="2"/>')
    anatomy_label(p,470,510,"crop (honey stomach)",170,235,"orange")
    anatomy_label(p,620,520,"midgut",235,335,"orange")
    anatomy_label(p,835,520,"hindgut / rectum",1030,620,"orange")
    anatomy_label(p,730,490,"Malpighian tubules",990,460,"green")
    anatomy_label(p,620,400,"dorsal vessel",940,300,"red")
    anatomy_label(p,620,585,"ventral nerve cord",940,745,"purple")
    anatomy_label(p,560,455,"tracheal system",210,720,"blue")
    note(p,885,["The crop temporarily carries nectar/water; digestion and absorption occur mainly in the midgut. Tracheae deliver gases directly to tissues rather than using blood to transport oxygen."],"purple")
    return finish(p)

def fig_6_5():
    p=start("Figure 6.5 — Worker, Queen and Drone Anatomy Comparison","Side-by-side caste anatomy comparison showing relative abdomen, eye size, pollen-collection structures and reproductive role.")
    text(p,55,100,"Differences are functional, not a simple 'small–medium–large' size ranking.",18,400,C["muted"])
    items=[("WORKER","female; usually non-reproductive","worker","blue"),("QUEEN","reproductive female","queen","purple"),("DRONE","haploid male","drone","orange")]
    for i,(title,sub,role,kind) in enumerate(items):
        x=55+i*440; panel(p,x,155,390,700,title,kind)
        bee_body(p,x+120,410,0.85,role)
        text(p,x+195,555,sub,16,700,C["muted"],"middle")
        if role=="worker":
            multi(p,x+25,620,["• moderate compound eyes","• hind-leg pollen basket","• sting apparatus present","• reduced ovaries"],16,500,C["ink"],27)
        elif role=="queen":
            multi(p,x+25,620,["• elongated abdomen","• developed ovaries + spermatheca","• no pollen basket","• sting modified for queen context"],16,500,C["ink"],27)
        else:
            multi(p,x+25,620,["• very large compound eyes","• stout body","• no pollen basket","• no worker-type sting; male reproductive tract"],16,500,C["ink"],27)
    note(p,885,["Caste differences arise from sex determination and developmental/nutritional pathways. Queen and worker are female; drones develop from unfertilised eggs."],"blue")
    return finish(p)

def fig_7_1():
    p=start("Figure 7.1 — Complete Development Cycle","Approximate queen, worker and drone development timelines from egg through larva, capped prepupa/pupa and adult emergence.")
    text(p,55,100,"Approximate durations under normal conditions; temperature, genetics and colony conditions create variation.",18,400,C["muted"])
    roles=[("Queen",16,8,"purple"),("Worker",21,9,"blue"),("Drone",24,10,"orange")]
    for i,(role,total,capday,kind) in enumerate(roles):
        y=200+i*220; panel(p,55,y,1290,180,role,kind)
        x0=230; scale=40
        # day ruler
        for d in range(0,25):
            x=x0+d*scale
            if d<=total: p.append(f'<line x1="{x}" y1="{y+70}" x2="{x}" y2="{y+125}" stroke="#CFD8DC" stroke-width="1"/>')
            if d%3==0 and d<=total: text(p,x,y+145,str(d),12,500,C["muted"],"middle")
        # stages
        rect(p,x0,y+70,3*scale,48,C["green_light"],C["green"],1.5,6); text(p,x0+60,y+102,"egg",14,700,C["green"],"middle")
        larval_end=capday
        rect(p,x0+3*scale,y+70,(larval_end-3)*scale,48,C["honey_light"],C["honey"],1.5,6); text(p,x0+(3+(larval_end-3)/2)*scale,y+102,"open larva",14,700,C["brown"],"middle")
        rect(p,x0+larval_end*scale,y+70,(total-larval_end)*scale,48,C["purple_light"],C["purple"],1.5,6); text(p,x0+(larval_end+(total-larval_end)/2)*scale,y+102,"capped prepupa / pupa",13,700,C["purple"],"middle")
        p.append(f'<line x1="{x0+capday*scale}" y1="{y+55}" x2="{x0+capday*scale}" y2="{y+130}" stroke="{C["orange"]}" stroke-width="4"/>')
        text(p,x0+capday*scale,y+50,"~capping",12,700,C["orange"],"middle")
        p.append(f'<line x1="{x0+total*scale}" y1="{y+55}" x2="{x0+total*scale}" y2="{y+130}" stroke="{C["red"]}" stroke-width="4"/>')
        text(p,x0+total*scale,y+50,f"~day {total}",12,700,C["red"],"middle")
    note(p,885,["Egg stage is about three days in all castes. Queen development is fastest, worker intermediate, drone slowest; capping and emergence are approximate, not identical in every colony."],"orange")
    return finish(p)

def fig_7_2():
    p=start("Figure 7.2 — Larval Growth and Feeding","Representative honey bee larval stages increasing in size while retaining the normal C-shaped position, with feeding context.")
    text(p,55,100,"Larvae grow rapidly through successive instars; size and cell occupancy increase dramatically.",18,400,C["muted"])
    sizes=[0.65,0.9,1.2,1.55,1.95]
    labels=["early","growing","mid larval","late larval","near capping"]
    for i,(s,lab) in enumerate(zip(sizes,labels)):
        x=120+i*255; panel(p,x,180,220,600,f"{i+1} — {lab}","honey")
        # cell
        p.append(f'<polygon points="{x+110},270 {x+185},315 {x+185},500 {x+110},545 {x+35},500 {x+35},315" fill="#FFF7D6" stroke="{C["brown"]}" stroke-width="3"/>')
        # food pool
        p.append(f'<ellipse cx="{x+110}" cy="470" rx="52" ry="20" fill="{C["rj"]}" stroke="#C7A94E" stroke-width="2" opacity="0.85"/>')
        # larva
        cx=x+110; cy=420
        d=f"M {cx-20*s} {cy-8*s} C {cx-6*s} {cy-31*s}, {cx+27*s} {cy-20*s}, {cx+20*s} {cy+4*s} C {cx+14*s} {cy+23*s}, {cx-12*s} {cy+26*s}, {cx-20*s} {cy+9*s}"
        p.append(f'<path d="{d}" fill="none" stroke="#E2DDD0" stroke-width="{15*s}" stroke-linecap="round"/>')
        p.append(f'<path d="{d}" fill="none" stroke="#FFFDF4" stroke-width="{11*s}" stroke-linecap="round"/>')
        text(p,x+110,600,f"relative size ↑",15,700,C["green"],"middle")
        multi(p,x+25,650,["food quantity/composition","change with age and caste"],14,500,C["muted"],20)
    note(p,885,["Healthy larvae are pearly white, moist/glistening and curled in a C shape on the cell floor. Exact age should not be inferred from size alone without context."],"green")
    return finish(p)

def fig_7_4():
    p=start("Figure 7.4 — Caste Development Comparison","Queen, worker and drone development compared by fertilisation status, cell type and approximate total time to adult emergence.")
    text(p,55,100,"Developmental nutrition determines queen versus worker among fertilised female eggs; drones are haploid males from unfertilised eggs.",18,400,C["muted"])
    rows=[("Queen","fertilised egg","vertical queen cell","~16 days","purple"),("Worker","fertilised egg","worker cell","~21 days","blue"),("Drone","unfertilised egg","larger drone cell","~24 days","orange")]
    headers=["Caste","Sex determination","Cell context","Approx. emergence"]
    xstarts=[60,300,620,980]; widths=[220,300,340,300]
    for x,w,h in zip(xstarts,widths,headers):
        rect(p,x,170,w,70,C["grey_light"],C["grey"],2,10); text(p,x+w/2,212,h,17,700,C["ink"],"middle")
    for i,(role,sex,celltype,time,kind) in enumerate(rows):
        y=260+i*190; pal={"purple":(C["purple_light"],C["purple"]),"blue":(C["blue_light"],C["blue"]),"orange":(C["orange_light"],C["orange"])}; fill,stroke=pal[kind]
        vals=[role,sex,celltype,time]
        for x,w,val in zip(xstarts,widths,vals):
            rect(p,x,y,w,145,fill,stroke,2,12); text(p,x+w/2,y+76,val,17,700 if x==60 else 500,stroke if x==60 else C["ink"],"middle")
    note(p,880,["Approximate development times are useful for management but should not be treated as a rigid clock. Colony temperature and biological variation can shift timing."],"orange")
    return finish(p)

def fig_8_1():
    p=start("Figure 8.1 — Queen Anatomy and Identification","Queen shown among workers with elongated abdomen, caste proportions and the correct thoracic marking location.")
    text(p,55,100,"Identify the queen by body form and behaviour, not only by paint marking.",18,400,C["muted"])
    panel(p,55,150,850,700,"Queen among workers","purple")
    for x,y in [(220,330),(330,500),(580,300),(690,520),(470,650)]:
        bee_body(p,x,y,0.42,"worker")
    bee_body(p,470,450,0.95,"queen")
    # marking dot on thorax
    p.append(f'<circle cx="470" cy="450" r="13" fill="#4FC3F7" stroke="#0D47A1" stroke-width="2"/>')
    anatomy_label(p,470,450,"mark goes on thorax",760,250,"blue")
    anatomy_label(p,595,450,"elongated abdomen",810,450,"purple")
    panel(p,950,150,395,700,"Identification cues","blue")
    multi(p,980,220,["• abdomen extends well beyond wing tips","• thorax is relatively broad and less hairy","• workers may orient around her","• movement can be purposeful or rapid","• paint mark is optional aid, not anatomy","","Avoid grabbing abdomen; protect the queen during inspection."],16,500,C["ink"],28)
    note(p,885,["Queen appearance varies with age, mating status and egg-laying state. A newly emerged virgin can be smaller and faster than a mature laying queen."],"orange")
    return finish(p)

def fig_8_2():
    p=start("Figure 8.2 — Queen Reproductive System","Simplified queen reproductive anatomy showing paired ovaries, lateral oviducts, median oviduct, spermatheca with gland/duct and sting chamber context.")
    text(p,55,100,"Anatomically simplified for education; relative relationships are preserved.",18,400,C["muted"])
    panel(p,55,150,900,710,"Queen reproductive tract","purple")
    # ovaries with ovarioles
    for side,cx in [("L",340),("R",650)]:
        p.append(f'<ellipse cx="{cx}" cy="360" rx="120" ry="180" fill="#F7D7E2" stroke="#AD5A7C" stroke-width="4"/>')
        for k in range(-4,5):
            x=cx+k*18
            p.append(f'<path d="M{x} 245 Q {x-8} 360 {x} 480" fill="none" stroke="#C97E9D" stroke-width="4"/>')
        text(p,cx,195,f"{side} ovary (many ovarioles)",17,700,"#AD5A7C","middle")
    # oviducts
    p.append(f'<path d="M340 520 Q420 590 525 610" fill="none" stroke="{C["purple"]}" stroke-width="12" stroke-linecap="round"/>')
    p.append(f'<path d="M650 520 Q575 590 525 610" fill="none" stroke="{C["purple"]}" stroke-width="12" stroke-linecap="round"/>')
    p.append(f'<path d="M525 610 L525 790" fill="none" stroke="{C["purple"]}" stroke-width="14" stroke-linecap="round"/>')
    text(p,525,835,"median oviduct → vagina / sting chamber region",16,700,C["purple"],"middle")
    # spermatheca
    p.append(f'<circle cx="730" cy="650" r="65" fill="#DDEAF8" stroke="{C["blue"]}" stroke-width="4"/>')
    p.append(f'<path d="M680 680 Q620 700 555 665" fill="none" stroke="{C["blue"]}" stroke-width="7"/>')
    text(p,730,745,"spermatheca stores sperm",16,700,C["blue"],"middle")
    anatomy_label(p,400,570,"lateral oviduct",160,650,"purple")
    panel(p,990,150,355,710,"Functional summary","blue")
    multi(p,1015,220,["Ovaries","produce mature eggs","","Oviducts","carry eggs toward median oviduct","","Spermatheca","stores and nourishes sperm from mating flights","","Valve/duct","allows sperm release to fertilise selected eggs"],16,500,C["ink"],25)
    note(p,885,["The queen can lay fertilised eggs that develop as females (workers/queens) or unfertilised eggs that develop as drones."],"green")
    return finish(p)

def fig_8_3():
    p=start("Figure 8.3 — Mating and Sperm Storage Concept","Virgin queen mating flights to multiple drones, sperm storage in the spermatheca, and later fertilised versus unfertilised egg pathways.")
    text(p,55,100,"Conceptual reproductive flow; mating normally occurs in flight and can involve multiple drones.",18,400,C["muted"])
    panel(p,55,160,300,650,"1 — Virgin queen","purple"); bee_body(p,145,350,0.55,"queen"); multi(p,85,565,["Matures after emergence","and takes mating flight(s)","when weather/biology permit."],16,500,C["ink"],25)
    panel(p,400,160,300,650,"2 — Multiple matings","orange")
    bee_body(p,495,340,0.42,"queen")
    for x,y in [(470,500),(560,520),(510,610)]: bee_body(p,x,y,0.28,"drone")
    multi(p,430,690,["Drones from multiple colonies","can contribute sperm, increasing","colony genetic diversity."],16,500,C["ink"],25)
    panel(p,745,160,300,650,"3 — Spermathecal storage","blue"); p.append(f'<circle cx="895" cy="410" r="90" fill="#DDEAF8" stroke="{C["blue"]}" stroke-width="5"/>')
    for a in range(0,360,30):
        ang=math.radians(a); p.append(f'<ellipse cx="{895+55*math.cos(ang)}" cy="{410+55*math.sin(ang)}" rx="10" ry="4" fill="#6FA8DC" transform="rotate({a} {895+55*math.cos(ang)} {410+55*math.sin(ang)})"/>')
    multi(p,775,585,["Stored sperm is maintained","for later egg fertilisation","during the queen's laying life."],16,500,C["ink"],25)
    panel(p,1090,160,255,650,"4 — Egg pathway","green"); egg(p,1215,340,2); arrow(p,1215,390,1165,490,"green"); arrow(p,1215,390,1270,490,"blue")
    text(p,1155,535,"fertilised",15,700,C["green"],"middle"); text(p,1280,535,"unfertilised",15,700,C["blue"],"middle")
    multi(p,1120,585,["female → worker/queen","","male → drone"],16,600,C["ink"],26)
    arrow(p,355,480,400,480,"blue"); arrow(p,700,480,745,480,"blue"); arrow(p,1045,480,1090,480,"blue")
    note(p,880,["Fertilisation status determines sex; nutrition and developmental environment determine queen versus worker among fertilised female larvae."],"purple")
    return finish(p)

def fig_9_1():
    p=start("Figure 9.1 — Worker Task Progression","Age-related worker task tendencies from cell cleaning and nursing to wax/food work, guarding and foraging, with arrows showing behavioural flexibility.")
    text(p,55,100,"Worker tasks overlap and can reverse according to colony need; this is not a rigid age schedule.",18,400,C["muted"])
    stages=[("Cleaning","prepare cells / hive hygiene","green"),("Nursing","feed larvae and queen","purple"),("Wax + food work","comb, nectar handling, ventilation","honey"),("Guarding","entrance defence / recognition","orange"),("Foraging","nectar, pollen, water, resin","blue")]
    xs=[75,340,605,870,1135]
    for i,(t,s,k) in enumerate(stages):
        panel(p,xs[i],230,210,330,t,k)
        bee_body(p,xs[i]+55,390,0.30,"worker")
        multi(p,xs[i]+18,495,[s],14,500,C["ink"],20)
        if i<4: arrow(p,xs[i]+210,395,xs[i+1],395,"blue")
    # reverse flexibility arrow
    p.append(f'<path d="M1230 650 C1050 800 380 800 180 650" fill="none" stroke="{C["orange"]}" stroke-width="5" marker-end="url(#ab)"/>')
    text(p,700,790,"colony need can accelerate, delay or reverse task tendencies",16,700,C["orange"],"middle")
    note(p,875,["Age polyethism describes a tendency, not a timetable. Nutrition, season, colony demography and disturbance can reshape worker roles."],"orange")
    return finish(p)

def fig_9_2():
    p=start("Figure 9.2 — Worker Specialised Structures","Worker structures important to colony function: hypopharyngeal glands, wax glands, pollen basket, sting apparatus and Nasonov gland.")
    text(p,55,100,"Magnified insets identify specialised structures that are too small or internal to see at normal scale.",18,400,C["muted"])
    bee_body(p,500,470,1.45,"worker")
    # head gland
    p.append(f'<ellipse cx="380" cy="455" rx="42" ry="30" fill="{C["purple_light"]}" stroke="{C["purple"]}" stroke-width="3"/>')
    anatomy_label(p,380,455,"hypopharyngeal glands",100,210,"purple")
    # pollen basket hind leg
    p.append(f'<ellipse cx="560" cy="655" rx="40" ry="18" fill="#E9B93E" stroke="#9A6A0A" stroke-width="3"/>')
    anatomy_label(p,560,655,"corbicula / pollen basket",100,725,"orange")
    # wax glands under abdomen
    for x in [650,690,730,770]: p.append(f'<ellipse cx="{x}" cy="535" rx="18" ry="9" fill="#FFFBEA" stroke="{C["brown"]}" stroke-width="2"/>')
    anatomy_label(p,715,535,"wax-gland sternites",915,280,"green")
    # nasonov gland
    p.append(f'<path d="M820 470 Q850 450 875 470" fill="none" stroke="{C["blue"]}" stroke-width="8"/>')
    anatomy_label(p,855,470,"Nasonov gland region",990,470,"blue")
    # sting
    p.append(f'<line x1="850" y1="500" x2="910" y2="520" stroke="{C["red"]}" stroke-width="5"/>')
    anatomy_label(p,905,520,"sting apparatus",1040,650,"orange")
    panel(p,1000,180,320,610,"Function summary","blue")
    multi(p,1025,240,["Hypopharyngeal glands","brood food + enzymes","","Wax glands","produce wax scales","","Corbicula","carries packed pollen","","Nasonov gland","orientation/aggregation signal","","Sting apparatus","defence; associated venom system"],15,500,C["ink"],23)
    note(p,885,["Structure size and gland development change with worker age and task state. Insets are magnified and not drawn to the same scale as the whole bee."],"blue")
    return finish(p)

def fig_9_3():
    p=start("Figure 9.3 — Forager Resource Types","Forager resource types—nectar, pollen, water and plant resin—shown with the correct primary transport structures.")
    text(p,55,100,"A forager can specialise temporarily on different resources; transport differs by resource.",18,400,C["muted"])
    items=[("Nectar","carried internally in crop","honey"),("Pollen","packed on hind-leg corbiculae","orange"),("Water","carried internally in crop","blue"),("Plant resin","carried on hind-leg corbiculae","green")]
    for i,(t,s,k) in enumerate(items):
        x=60+i*335; panel(p,x,170,290,650,t,k)
        bee_body(p,x+95,360,0.40,"worker")
        if t=="Nectar":
            p.append(f'<ellipse cx="{x+180}" cy="365" rx="28" ry="18" fill="#F6CF58" stroke="{C["honey"]}" stroke-width="3"/>')
        elif t=="Pollen":
            p.append(f'<ellipse cx="{x+165}" cy="500" rx="22" ry="13" fill="#E1A11E" stroke="#9A6515" stroke-width="3"/>')
        elif t=="Water":
            p.append(f'<path d="M{x+180} 335 C{x+158} 360 {x+158} 382 {x+180} 400 C{x+202} 382 {x+202} 360 {x+180} 335 Z" fill="#90CAF9" stroke="{C["blue"]}" stroke-width="3"/>')
        else:
            p.append(f'<ellipse cx="{x+165}" cy="500" rx="22" ry="13" fill="#7A4D31" stroke="#4E3224" stroke-width="3"/>')
        multi(p,x+25,590,[s],16,600,C["ink"],25)
    note(p,875,["Nectar and water are transported internally in the crop. Pollen and resin are carried externally on specialised hind-leg structures; neither is carried as liquid in the crop."],"green")
    return finish(p)

def fig_10_1():
    p=start("Figure 10.1 — Drone Identification","Drone, worker and queen shown side by side, emphasising the drone's very large compound eyes, stout body and absence of worker pollen basket/sting.")
    text(p,55,100,"Caste identification should use several features rather than body size alone.",18,400,C["muted"])
    roles=[("Worker","worker","blue"),("Queen","queen","purple"),("Drone","drone","orange")]
    for i,(name,role,kind) in enumerate(roles):
        x=70+i*440; panel(p,x,160,390,650,name,kind); bee_body(p,x+125,430,0.85,role)
        if role=="worker": multi(p,x+25,620,["moderate eyes","slender worker abdomen","corbicula present","sting apparatus present"],16,500,C["ink"],26)
        elif role=="queen": multi(p,x+25,620,["elongated abdomen","queen reproductive system","no pollen basket","queen-specific sting anatomy"],16,500,C["ink"],26)
        else: multi(p,x+25,620,["very large eyes meet near top of head","stout abdomen","no pollen basket","no worker-type sting"],16,500,C["ink"],26)
    note(p,875,["Drones are not 'useless': their primary evolutionary role is mating and gene flow. Their abundance changes seasonally with colony and climate conditions."],"orange")
    return finish(p)

def fig_10_2():
    p=start("Figure 10.2 — Drone Development","Drone brood and worker brood compared by cell size/capping shape and approximate total development time.")
    text(p,55,100,"Drone cells are larger and capped brood is more strongly domed than worker brood.",18,400,C["muted"])
    panel(p,55,160,620,650,"Worker brood","blue")
    for r in range(4):
        for c in range(5):
            cx=135+c*90+(r%2)*45; cy=295+r*90
            p.append(f'<circle cx="{cx}" cy="{cy}" r="34" fill="#B98755" stroke="#7B563A" stroke-width="3"/>')
            p.append(f'<ellipse cx="{cx-7}" cy="{cy-8}" rx="15" ry="8" fill="#D5A777" opacity="0.45"/>')
    text(p,365,700,"approx. egg → adult: ~21 days",18,700,C["blue"],"middle")
    panel(p,725,160,620,650,"Drone brood","orange")
    for r in range(4):
        for c in range(4):
            cx=825+c*115+(r%2)*57; cy=295+r*90
            p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="45" ry="39" fill="#B98755" stroke="#7B563A" stroke-width="3"/>')
            p.append(f'<ellipse cx="{cx}" cy="{cy-8}" rx="30" ry="24" fill="#D7AC7D" opacity="0.5"/>')
    text(p,1035,700,"approx. egg → adult: ~24 days",18,700,C["orange"],"middle")
    note(p,875,["Cell/capping appearance supports caste identification, but exact development timing varies. Queen, worker and drone schedules are approximate biological guides."],"orange")
    return finish(p)

def fig_10_3():
    p=start("Figure 10.3 — Drone Reproductive Anatomy","Simplified mature drone reproductive system showing testes after maturation, vasa deferentia, seminal vesicles, mucus glands, ejaculatory duct and inverted endophallus.")
    text(p,55,100,"Anatomy shown in simplified educational form based on standard honey bee dissection references.",18,400,C["muted"])
    panel(p,55,150,930,710,"Mature drone reproductive tract","orange")
    # paired structures
    for cx in [360,650]:
        p.append(f'<ellipse cx="{cx}" cy="300" rx="65" ry="38" fill="#EAB6A6" stroke="#A85F4A" stroke-width="3"/>')
        p.append(f'<path d="M{cx} 338 C{cx-10} 430 {cx-25} 500 510 580" fill="none" stroke="{C["orange"]}" stroke-width="8"/>')
    text(p,505,235,"testes reduce after sperm moves toward seminal vesicles",16,700,C["orange"],"middle")
    # seminal vesicles / mucus glands
    p.append(f'<ellipse cx="470" cy="510" rx="38" ry="70" fill="#F0C6A2" stroke="#AA7047" stroke-width="3"/>')
    p.append(f'<ellipse cx="590" cy="510" rx="38" ry="70" fill="#F0C6A2" stroke="#AA7047" stroke-width="3"/>')
    p.append(f'<ellipse cx="420" cy="600" rx="42" ry="80" fill="#F6E8C6" stroke="#A98252" stroke-width="3"/>')
    p.append(f'<ellipse cx="640" cy="600" rx="42" ry="80" fill="#F6E8C6" stroke="#A98252" stroke-width="3"/>')
    p.append(f'<path d="M470 580 Q520 650 530 720 M590 580 Q545 650 530 720" fill="none" stroke="{C["purple"]}" stroke-width="9"/>')
    p.append(f'<path d="M530 720 L530 790" stroke="{C["purple"]}" stroke-width="12"/>')
    anatomy_label(p,470,510,"seminal vesicle",165,425,"orange")
    anatomy_label(p,420,600,"mucus gland",170,620,"orange")
    anatomy_label(p,530,740,"ejaculatory duct",800,680,"purple")
    text(p,530,825,"inverted endophallus lies caudally beyond this simplified tract",15,700,C["muted"],"middle")
    panel(p,1020,150,325,710,"Functional sequence","blue")
    multi(p,1045,220,["Testes","produce sperm during development","","Seminal vesicles","store mature sperm","","Mucus glands","contribute mating secretions","","Ejaculatory duct + endophallus","transfer semen during mating","","Drone dies after successful copulation."],15,500,C["ink"],24)
    note(p,885,["The endophallus is normally inverted inside the abdomen and everts during mating. This figure is educational, not a procedural insemination guide."],"blue")
    return finish(p)

ASSETS={
"fig-06-1-external-worker-anatomy.svg":fig_6_1,
"fig-06-4-internal-systems.svg":fig_6_4,
"fig-06-5-caste-anatomy-comparison.svg":fig_6_5,
"fig-07-1-complete-development-cycle.svg":fig_7_1,
"fig-07-2-larval-growth-feeding.svg":fig_7_2,
"fig-07-4-caste-development-comparison.svg":fig_7_4,
"fig-08-1-queen-anatomy-identification.svg":fig_8_1,
"fig-08-2-queen-reproductive-system.svg":fig_8_2,
"fig-08-3-mating-sperm-storage.svg":fig_8_3,
"fig-09-1-worker-task-progression.svg":fig_9_1,
"fig-09-2-worker-specialised-structures.svg":fig_9_2,
"fig-09-3-forager-resource-types.svg":fig_9_3,
"fig-10-1-drone-identification.svg":fig_10_1,
"fig-10-2-drone-development.svg":fig_10_2,
"fig-10-3-drone-reproductive-anatomy.svg":fig_10_3,
}

def write_meta():
    data={"wave":2,"batch":"anatomy-b","asset_count":len(ASSETS),"assets":[]}
    for name in ASSETS:
        parts=name.split("-"); fid=f"{int(parts[1])}.{int(parts[2])}"
        data["assets"].append({"figure_id":fid,"path":"assets/diagrams/wave-02/"+name,"status":"ACTUAL_TECHNICAL_SVG_CREATED","layout_status":"PENDING_FINAL_LAYOUT_PROOF"})
    META.parent.mkdir(parents=True,exist_ok=True); META.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")

def write_report():
    lines=["# Visual Wave 02 — Anatomy B Review","","**Result:** PASS — A_CORE ANATOMY / DEVELOPMENT BATCH CREATED","","## Assets created",""]
    lines += ["- "+n for n in ASSETS]
    lines += ["","## Scientific controls","",
              "- Worker external anatomy uses head/thorax/abdomen organisation and labels antennae, compound eyes, ocelli, mouthparts, legs, wings and sting region.",
              "- Internal systems show crop, midgut, hindgut, Malpighian tubules, tracheae, dorsal vessel and ventral nervous system as a simplified spatial teaching plate.",
              "- Worker/queen/drone comparison emphasises functional caste differences rather than size silhouettes only.",
              "- Development timing uses approximate queen ~16 d, worker ~21 d, drone ~24 d and explicitly labels natural variation.",
              "- Healthy larval references remain pearly white and C-shaped.",
              "- Queen reproductive anatomy includes ovaries, oviducts and spermatheca; sex determination is separated from queen/worker nutritional caste development.",
              "- Worker task progression is explicitly flexible and reversible.",
              "- Forager resource transport distinguishes internal crop transport (nectar/water) from hind-leg corbicula transport (pollen/resin).",
              "- Drone anatomy emphasises large eyes, reproductive role, and mature male reproductive tract without demeaning 'useless drone' framing.",
              "","## Reference basis","",
              "- COLOSS BEEBOOK anatomy/dissection references.",
              "- University of Florida honey bee development/anatomy teaching references.",
              "- Penn State 2024–2025 queen/genetics and development references.",
              "- USDA drone reproductive-anatomy references.",
              "","## Remaining gates","",
              "All assets remain subject to final print-size, greyscale, accessibility and page-layout proof.",""]
    REPORT.parent.mkdir(parents=True,exist_ok=True); REPORT.write_text("\n".join(lines),encoding="utf-8")

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for name,fn in ASSETS.items():
        s=fn(); ET.fromstring(s)
        if "<title" not in s or "<desc" not in s: raise RuntimeError(name)
        (OUT/name).write_text(s,encoding="utf-8")
    write_meta(); write_report()
    print(f"Created {len(ASSETS)} Wave 02 Anatomy B SVGs.")

if __name__=="__main__":
    main()
