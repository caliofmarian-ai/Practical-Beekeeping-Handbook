#!/usr/bin/env python3
from __future__ import annotations
import json, math
from pathlib import Path
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"assets"/"diagrams"/"wave-02"
META=ROOT/"assets"/"production-briefs"/"wave-02-behaviour-site-c.json"
REPORT=ROOT/"docs"/"reviews"/"VISUAL_WAVE_02_BEHAVIOUR_SITE_C_REVIEW.md"
W,H=1400,1000
FONT="Arial,Helvetica,sans-serif"
C={"ink":"#1F2933","muted":"#52606D","blue":"#1565C0","blue_light":"#E3F2FD","green":"#2E7D32","green_light":"#E8F5E9","orange":"#EF6C00","orange_light":"#FFF3E0","red":"#C62828","red_light":"#FFEBEE","purple":"#6A1B9A","purple_light":"#F3E5F5","honey":"#D4A017","honey_light":"#FFF8E1","brown":"#8D6E63","grey":"#757575","grey_light":"#F5F5F5","bee":"#E0A419","bee_dark":"#5D4037","wing":"#D9EEF7","pollen":"#D98C10","water":"#64B5F6","resin":"#7A4D31","brood":"#B98755","wax":"#F4E7A1"}

def start(title,desc):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title>',f'<desc id="desc">{escape(desc)}</desc>',
            '<defs>',
            f'<marker id="ab" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="{C["blue"]}"/></marker>',
            f'<marker id="ag" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="{C["green"]}"/></marker>',
            f'<marker id="ao" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="{C["orange"]}"/></marker>',
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
def arrow(p,x1,y1,x2,y2,color="blue",width=4):
    col={"blue":C["blue"],"green":C["green"],"orange":C["orange"]}[color]; marker={"blue":"ab","green":"ag","orange":"ao"}[color]
    p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{width}" marker-end="url(#{marker})"/>')
def note(p,y,lines,kind="orange"):
    pal={"orange":(C["orange_light"],C["orange"]),"blue":(C["blue_light"],C["blue"]),"green":(C["green_light"],C["green"]),"purple":(C["purple_light"],C["purple"])}
    fill,stroke=pal[kind]; rect(p,55,y,1290,80,fill,stroke,2.5,14); multi(p,78,y+29,lines,17,600,C["ink"],23)
def circle_label(p,cx,cy,r,fill,stroke,title,sub=None):
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>')
    text(p,cx,cy-3,title,18,700,stroke,"middle")
    if sub:
        text(p,cx,cy+24,sub,13,500,C["muted"],"middle")
def bee(p,cx,cy,s=1):
    p.append(f'<path d="M{cx+5*s} {cy-18*s} C{cx+35*s} {cy-70*s} {cx+100*s} {cy-65*s} {cx+72*s} {cy-15*s} Z" fill="{C["wing"]}" opacity="0.7" stroke="#7EAFC3" stroke-width="{1.6*s}"/>')
    p.append(f'<circle cx="{cx-50*s}" cy="{cy}" r="{20*s}" fill="{C["bee"]}" stroke="{C["bee_dark"]}" stroke-width="{2*s}"/>')
    p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{34*s}" ry="{28*s}" fill="{C["bee"]}" stroke="{C["bee_dark"]}" stroke-width="{2*s}"/>')
    p.append(f'<ellipse cx="{cx+70*s}" cy="{cy}" rx="{45*s}" ry="{25*s}" fill="{C["bee"]}" stroke="{C["bee_dark"]}" stroke-width="{2*s}"/>')
    for x in [cx+50*s,cx+70*s,cx+90*s]: p.append(f'<line x1="{x}" y1="{cy-20*s}" x2="{x}" y2="{cy+20*s}" stroke="{C["bee_dark"]}" stroke-width="{3*s}"/>')
def flower(p,cx,cy,s=1,col="#D46FA8"):
    for a in range(0,360,72):
        ang=math.radians(a); x=cx+22*s*math.cos(ang); y=cy+22*s*math.sin(ang)
        p.append(f'<ellipse cx="{x}" cy="{y}" rx="{17*s}" ry="{10*s}" fill="{col}" transform="rotate({a} {x} {y})"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{10*s}" fill="#F4C542"/>')
def hive(p,x,y,w=270,h=320):
    rect(p,x,y,w,h,"#F6E3B4",C["brown"],4,8); rect(p,x-10,y-25,w+20,30,"#D6C6A0",C["brown"],3,4); rect(p,x+25,y+h,w-50,20,"#D6C6A0",C["brown"],3,4)
    p.append(f'<rect x="{x+80}" y="{y+h-18}" width="110" height="18" fill="#3D2E24"/>')
def small_comb(p,cx,cy,r=150):
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFF8DB" stroke="{C["brown"]}" stroke-width="4"/>')
    # representative brood center / pollen band / honey outer
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.48}" fill="{C["brood"]}" opacity="0.85"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.70}" fill="none" stroke="{C["pollen"]}" stroke-width="{r*0.18}" opacity="0.8"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.90}" fill="none" stroke="#F3D46C" stroke-width="{r*0.18}" opacity="0.8"/>')

def fig_11_2():
    p=start("Figure 11.2 — Distance and Dance Tempo Concept","Conceptual comparison showing how waggle-dance duration and repetition characteristics change with increasing foraging distance, without fixed universal calibration values.")
    text(p,55,100,"The dance encodes distance continuously; exact calibration varies with terrain, wind and experimental context.",18,400,C["muted"])
    distances=[("nearer source",260,3),("intermediate source",700,5),("farther source",1140,8)]
    for i,(lab,cx,n) in enumerate(distances):
        panel(p,cx-180,180,360,620,lab,"blue" if i<2 else "purple")
        # comb axis
        p.append(f'<line x1="{cx}" y1="260" x2="{cx}" y2="630" stroke="{C["grey"]}" stroke-width="4" stroke-dasharray="8 7"/>')
        # waggle loops
        y=320
        for k in range(n):
            p.append(f'<path d="M{cx} {y} C{cx-70} {y+30} {cx-70} {y+90} {cx} {y+115} C{cx+70} {y+90} {cx+70} {y+30} {cx} {y}" fill="none" stroke="{C["blue"]}" stroke-width="4"/>')
            y+=32
        text(p,cx,700,"longer waggle / slower repetition tendency → greater distance",14,700,C["muted"],"middle")
    note(p,865,["Do not turn this concept into one universal metres-per-second formula. Honey bees calibrate dance information in a context-sensitive way."],"orange")
    return finish(p)

def fig_11_4():
    p=start("Figure 11.4 — Alarm and Recruitment Signals","Comparison of guard/alarm signalling and food recruitment, clearly separating defence context from foraging recruitment.")
    text(p,55,100,"The same colony uses different channels and contexts; one signal does not have one invariant meaning.",18,400,C["muted"])
    panel(p,55,160,620,650,"Defence / alarm context","red")
    hive(p,125,330,250,300); bee(p,450,360,0.45); bee(p,520,430,0.40)
    p.append(f'<path d="M500 330 C620 280 650 250 700 210" fill="none" stroke="{C["red"]}" stroke-width="6" stroke-dasharray="8 6"/>')
    multi(p,95,680,["Guard assessment at entrance","alarm pheromone can recruit defenders","behaviour escalates with colony/context/environment"],16,500,C["ink"],27)
    panel(p,725,160,620,650,"Food recruitment context","green")
    hive(p,790,330,250,300); bee(p,1070,365,0.45); flower(p,1230,370,1.1,"#D46FA8")
    p.append(f'<path d="M1070 430 C1130 500 1190 500 1230 410" fill="none" stroke="{C["green"]}" stroke-width="5"/>')
    multi(p,765,680,["Successful forager returns to colony","dance/odour/trophallaxis support recruitment","source profitability shapes recruitment intensity"],16,500,C["ink"],27)
    note(p,865,["Alarm and food recruitment are context-dependent communication systems. Do not interpret one odour, vibration or dance element outside the behavioural setting."],"blue")
    return finish(p)

def fig_11_5():
    p=start("Figure 11.5 — Swarm Nest-Site Communication","Scout discovery, competing dances, evidence accumulation, quorum and swarm departure shown as a distributed group decision process.")
    text(p,55,100,"Nest-site choice emerges from scout competition and recruitment, not command by the queen.",18,400,C["muted"])
    steps=[("1 Scouts search","multiple cavities discovered"),("2 Dances compete","better sites recruit more scouts"),("3 Evidence converges","support shifts among alternatives"),("4 Quorum","enough scouts gather at one site"),("5 Departure","swarm moves after consensus process")]
    for i,(t,s) in enumerate(steps):
        x=45+i*270; panel(p,x,210,240,500,t,"purple" if i in (1,2) else "blue")
        if i==0:
            for xx,yy in [(x+70,390),(x+160,350),(x+120,480)]: bee(p,xx,yy,0.25)
        elif i==1:
            p.append(f'<path d="M{x+65} 400 C{x+15} 360 {x+15} 500 {x+65} 460 C{x+115} 500 {x+115} 360 {x+65} 400" fill="none" stroke="{C["purple"]}" stroke-width="4"/>')
            p.append(f'<path d="M{x+160} 400 C{x+120} 370 {x+120} 470 {x+160} 440 C{x+200} 470 {x+200} 370 {x+160} 400" fill="none" stroke="{C["orange"]}" stroke-width="4"/>')
        elif i==2:
            for k in range(6): p.append(f'<circle cx="{x+120+45*math.cos(k)}" cy="{420+45*math.sin(k)}" r="14" fill="{C["purple"]}" opacity="{0.45+0.08*k}"/>')
        elif i==3:
            hive(p,x+65,330,120,150)
            for k in range(5): bee(p,x+85+k*25,510,0.18)
        else:
            p.append(f'<ellipse cx="{x+120}" cy="430" rx="90" ry="55" fill="#F5D982" opacity="0.65"/>')
            for k in range(12):
                a=math.radians(k*30); bee(p,x+120+70*math.cos(a),430+45*math.sin(a),0.12)
        multi(p,x+18,610,[s],14,500,C["ink"],20)
        if i<4: arrow(p,x+240,455,x+270,455,"blue",3)
    note(p,865,["The queen does not select the new cavity. Scout-worker recruitment and quorum dynamics are central to nest-site decision-making."],"purple")
    return finish(p)

def fig_12_2():
    p=start("Figure 12.2 — Orientation Flight Versus Robbing","Side-by-side entrance-flight patterns and behavioural cues that help distinguish normal orientation flights from robbing.")
    text(p,55,100,"Both can look busy; use flight pattern, fighting, wax debris and attempts at cracks before deciding.",18,400,C["muted"])
    panel(p,55,160,620,650,"Orientation flights — normal learning","green")
    hive(p,175,420,260,300)
    for k in range(12):
        a=math.radians(k*30); x=305+220*math.cos(a); y=480+160*math.sin(a); bee(p,x,y,0.16)
        p.append(f'<path d="M{x} {y} Q 305 390 305 500" fill="none" stroke="#81C784" stroke-width="1.5" opacity="0.55"/>')
    multi(p,95,700,["young bees hover/arc facing hive","activity often concentrated near entrance","little fighting; no frantic crack-searching"],16,500,C["ink"],26)
    panel(p,725,160,620,650,"Robbing — investigate quickly","red")
    hive(p,845,420,260,300)
    for k,(x,y) in enumerate([(800,370),(1150,365),(780,520),(1180,540),(900,330),(1110,600)]):
        bee(p,x,y,0.18); p.append(f'<line x1="{x}" y1="{y}" x2="975" y2="560" stroke="{C["red"]}" stroke-width="2.5"/>')
    p.append(f'<circle cx="955" cy="710" r="9" fill="#E7D48A"/><circle cx="980" cy="715" r="9" fill="#E7D48A"/><circle cx="1005" cy="706" r="9" fill="#E7D48A"/>')
    multi(p,765,700,["irregular darting and fighting","bees investigate seams/cracks","wax debris/torn cappings may appear"],16,500,C["ink"],26)
    note(p,865,["Do not close a colony completely without considering ventilation. First remove exposed feed/honey, reduce defendable entrance as appropriate and stop the trigger."],"orange")
    return finish(p)

def fig_12_4():
    p=start("Figure 12.4 — Grooming and Hygienic Behaviour","Adult grooming contrasted with brood-cell detection and removal as two different colony defence behaviours.")
    text(p,55,100,"Both contribute to social defence, but grooming adult bees and hygienic brood removal are distinct behaviours.",18,400,C["muted"])
    panel(p,55,160,620,650,"Adult grooming","blue")
    bee(p,290,430,0.75); bee(p,450,490,0.45)
    p.append(f'<path d="M390 460 Q420 410 455 425" fill="none" stroke="{C["green"]}" stroke-width="5"/>')
    multi(p,95,665,["self-grooming removes particles/parasites","allogrooming = workers groom nestmates","effectiveness varies among stocks and context"],16,500,C["ink"],27)
    panel(p,725,160,620,650,"Hygienic brood behaviour","green")
    # capped cells and one opened
    for r in range(3):
        for c in range(4):
            x=845+c*95+(r%2)*47; y=330+r*95
            p.append(f'<circle cx="{x}" cy="{y}" r="36" fill="{C["brood"]}" stroke="#7E5638" stroke-width="3"/>')
    p.append(f'<circle cx="1035" cy="425" r="36" fill="#FFF5D6" stroke="{C["green"]}" stroke-width="5"/>')
    bee(p,1030,560,0.42); arrow(p,1030,535,1035,470,"green",3)
    multi(p,765,665,["workers detect abnormal/dead brood","cell is uncapped and brood removed","trait can reduce disease/parasite reproduction"],16,500,C["ink"],27)
    note(p,865,["Hygienic behaviour can reduce disease expression but does not make a colony immune or cancel monitoring/reporting obligations."],"green")
    return finish(p)

def fig_12_5():
    p=start("Figure 12.5 — Clustering and Thermoregulation","Cold-weather cluster contrasted with warm-weather ventilation, fanning and evaporative cooling.")
    text(p,55,100,"Honey bee colonies regulate nest temperature collectively; the strategy changes with heat load and season.",18,400,C["muted"])
    panel(p,55,160,620,650,"Cold conditions — cluster","purple")
    p.append(f'<circle cx="365" cy="465" r="180" fill="#F6CF58" opacity="0.35" stroke="{C["purple"]}" stroke-width="5"/>')
    for k in range(38):
        a=math.radians(k*137.5); rr=25+145*((k%11)/10); bee(p,365+rr*math.cos(a),465+rr*math.sin(a),0.11)
    text(p,365,680,"dense outer mantle + warmer brood/core region",16,700,C["purple"],"middle")
    panel(p,725,160,620,650,"Hot conditions — airflow + evaporation","blue")
    hive(p,875,370,300,320)
    for k in range(6):
        bee(p,850+k*55,720,0.18)
        p.append(f'<path d="M{850+k*55} 690 C{835+k*55} 655 {835+k*55} 620 {850+k*55} 595" fill="none" stroke="{C["blue"]}" stroke-width="3" marker-end="url(#ab)"/>')
    for x in [930,990,1050,1110]:
        p.append(f'<path d="M{x} 350 C{x-20} 320 {x-20} 280 {x} 245" fill="none" stroke="{C["blue"]}" stroke-width="3" marker-end="url(#ab)"/>')
    multi(p,765,765,["fanning increases airflow","water evaporation removes heat","bearding can reduce internal crowding"],16,500,C["ink"],25)
    note(p,865,["Bearding alone is not proof of dangerous overheating; interpret it with temperature, ventilation, hive condition and colony behaviour."],"blue")
    return finish(p)

def fig_13_1():
    p=start("Figure 13.1 — Brood-Nest Organisation","Representative comb pattern with central brood, pollen band and outer honey stores, explicitly labelled as variable rather than a fixed rule.")
    text(p,55,100,"A common pattern exists, but real colonies reshape it with season, comb age, flow and colony strength.",18,400,C["muted"])
    panel(p,55,150,830,720,"Representative brood frame","honey")
    # concentric zones
    p.append(f'<ellipse cx="470" cy="500" rx="320" ry="270" fill="#F5D66B" opacity="0.62" stroke="{C["honey"]}" stroke-width="4"/>')
    p.append(f'<ellipse cx="470" cy="500" rx="250" ry="205" fill="#E3A62D" opacity="0.60" stroke="#B66D13" stroke-width="3"/>')
    p.append(f'<ellipse cx="470" cy="510" rx="180" ry="145" fill="{C["brood"]}" opacity="0.88" stroke="#7E5638" stroke-width="4"/>')
    text(p,470,510,"brood",22,700,"#5C3C27","middle")
    text(p,470,330,"pollen band",18,700,"#9A6515","middle")
    text(p,470,230,"honey / nectar stores",18,700,C["brown"],"middle")
    panel(p,925,150,420,720,"Interpretation","blue")
    multi(p,955,220,["Typical tendency","brood concentrated centrally","pollen often near brood","honey often more peripheral/above","","But arrangement shifts with:","• season and nectar flow","• queen laying pattern","• comb position and age","• colony strength","• beekeeper manipulations"],16,500,C["ink"],26)
    note(p,895,["Use the pattern as a reading aid, not a geometric law. A colony can be healthy with stores and brood arranged differently from this schematic."],"orange")
    return finish(p)

def fig_13_2():
    p=start("Figure 13.2 — Colony as a Superorganism","Queen reproduction, worker labour, brood, food stores and thermoregulation linked as one functional colony system without an anthropomorphic command hierarchy.")
    text(p,55,100,"Colony function emerges from distributed interactions among thousands of bees and shared nest resources.",18,400,C["muted"])
    circle_label(p,700,480,115,C["honey_light"],C["brown"],"COLONY","superorganism")
    nodes=[(250,240,"Queen reproduction","egg production / pheromonal signals","purple"),(700,190,"Brood","future workforce + demand","orange"),(1150,250,"Worker labour","nursing, wax, defence, foraging","blue"),(1130,700,"Thermoregulation","heat, fanning, water, clustering","green"),(700,810,"Food stores","nectar/honey + pollen/bee bread","honey"),(260,700,"Foraging landscape","energy/protein/resin/water inputs","green")]
    pal={"purple":(C["purple_light"],C["purple"]),"orange":(C["orange_light"],C["orange"]),"blue":(C["blue_light"],C["blue"]),"green":(C["green_light"],C["green"]),"honey":(C["honey_light"],C["brown"])}
    for x,y,t,s,k in nodes:
        fill,stroke=pal[k]; circle_label(p,x,y,90,fill,stroke,t); text(p,x,y+117,s,14,500,C["muted"],"middle"); p.append(f'<line x1="{x}" y1="{y}" x2="700" y2="480" stroke="#B0BEC5" stroke-width="3"/>')
    note(p,900,["The queen is not a human-style ruler. Colony organisation is distributed through signals, local interactions, physiology, age structure and environmental feedback."],"blue")
    return finish(p)

def fig_13_4():
    p=start("Figure 13.4 — Resource Flow Through the Colony","Incoming nectar, pollen, water and resin routed through forager/receiver/nurse/processing functions toward brood care, stores, comb and nest maintenance.")
    text(p,55,100,"Different resources follow different pathways; the colony reallocates labour according to need.",18,400,C["muted"])
    resources=[("Nectar",C["honey"]),("Pollen",C["pollen"]),("Water",C["water"]),("Resin",C["resin"])]
    for i,(name,col) in enumerate(resources):
        y=210+i*160; circle_label(p,150,y,65,"#FFFFFF",col,name); arrow(p,220,y,385,y,"blue",3)
    panel(p,400,155,270,700,"Foragers + receivers","blue"); bee(p,525,340,0.45); multi(p,430,475,["collect and deliver resources","trophallaxis/transfer","sorting and immediate use"],16,500,C["ink"],25)
    arrow(p,670,500,770,500,"blue",4)
    panel(p,785,155,250,700,"House functions","purple"); multi(p,815,235,["nectar processing","nurse feeding","wax secretion","fanning / water use","propolis placement"],16,500,C["ink"],34)
    arrow(p,1035,500,1110,500,"green",4)
    panel(p,1125,155,220,700,"Outputs","green"); multi(p,1150,235,["brood growth","honey stores","bee bread","comb","nest sealing","temperature control"],16,600,C["ink"],34)
    note(p,890,["Resource flow is not linear inventory handling: the same nectar/water/pollen pool is continually redistributed among adult maintenance, brood, storage and processing."],"blue")
    return finish(p)

def fig_14_1():
    p=start("Figure 14.1 — Annual Colony Population Cycle","Conceptual forage, brood, adult population and stores curves across biological seasons rather than fixed calendar months.")
    text(p,55,100,"Curves are conceptual and should not be read as a forecast for a particular climate.",18,400,C["muted"])
    # chart
    x0,y0=110,780; x1=1300; ytop=180
    p.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="{C["ink"]}" stroke-width="3"/><line x1="{x0}" y1="{y0}" x2="{x0}" y2="{ytop}" stroke="{C["ink"]}" stroke-width="3"/>')
    labels=["survival / dearth","build-up","reproductive pressure","surplus / peak","preparation"]
    for i,l in enumerate(labels):
        x=x0+(i+0.5)*(x1-x0)/5; text(p,x,830,l,14,700,C["muted"],"middle")
        if i>0: p.append(f'<line x1="{x0+i*(x1-x0)/5}" y1="{ytop}" x2="{x0+i*(x1-x0)/5}" y2="{y0}" stroke="#ECEFF1" stroke-width="2"/>')
    def curve(points,color,label,ly):
        pts=" ".join(f"{x0+x*(x1-x0)},{y0-y*(y0-ytop)}" for x,y in points)
        p.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="7"/>'); text(p,1140,ly,label,16,700,color)
    curve([(0,0.25),(0.18,0.35),(0.35,0.75),(0.55,0.95),(0.72,0.55),(1,0.30)],C["green"],"brood",235)
    curve([(0,0.38),(0.2,0.42),(0.4,0.65),(0.62,0.92),(0.78,0.72),(1,0.42)],C["blue"],"adult bees",265)
    curve([(0,0.18),(0.2,0.48),(0.45,0.90),(0.63,0.75),(0.78,0.35),(1,0.20)],C["honey"],"forage",295)
    curve([(0,0.55),(0.2,0.30),(0.45,0.28),(0.67,0.78),(0.82,0.90),(1,0.62)],C["purple"],"stores",325)
    note(p,885,["The relative timing of brood, forage and adult population is the management signal. Replace these conceptual phases with local phenology, not month names."],"orange")
    return finish(p)

def fig_14_2():
    p=start("Figure 14.2 — Temperate Versus Warm-Climate Patterns","Conceptual comparison showing why seasonal colony management cannot be copied by calendar month between temperate and warm climates.")
    text(p,55,100,"Both panels are examples, not prescriptions; local rainfall, forage and temperature determine real patterns.",18,400,C["muted"])
    panel(p,55,160,620,650,"Temperate example","blue")
    # conceptual phases
    phases=[("cold / low brood",0.15,C["purple"]),("spring build-up",0.55,C["green"]),("peak / flow",0.9,C["honey"]),("decline / prepare",0.48,C["orange"])]
    x=100
    for name,hgt,col in phases:
        rect(p,x,700-hgt*380,120,hgt*380,"#FFFFFF",col,3,8); text(p,x+60,735,name,13,700,C["muted"],"middle"); x+=140
    panel(p,725,160,620,650,"Warm-climate example","green")
    phases2=[("dry dearth",0.30,C["orange"]),("rain/forage build",0.75,C["green"]),("flow / brood peak",0.88,C["honey"]),("short dearth / reset",0.45,C["purple"])]
    x=770
    for name,hgt,col in phases2:
        rect(p,x,700-hgt*380,120,hgt*380,"#FFFFFF",col,3,8); text(p,x+60,735,name,13,700,C["muted"],"middle"); x+=140
    note(p,875,["A 'January task' in one region may be biologically wrong elsewhere. Base management on brood state, forage, weather and colony condition."],"orange")
    return finish(p)

def fig_14_4():
    p=start("Figure 14.4 — Forage–Brood Feedback","Forage availability, nurse capacity, queen laying, brood demand and adult population linked over multiple weeks.")
    text(p,55,100,"Colony growth is delayed feedback: today's forage can change the workforce available weeks later.",18,400,C["muted"])
    nodes=[(220,300,"Forage availability","nectar + pollen",C["honey_light"],C["honey"]),(560,220,"Nurse capacity","brood-food production",C["purple_light"],C["purple"]),(900,300,"Queen laying","egg production responds to colony state",C["green_light"],C["green"]),(1120,590,"Brood demand","food + thermoregulation",C["orange_light"],C["orange"]),(700,760,"Adult population","future nurses + foragers",C["blue_light"],C["blue"]),(300,650,"Foraging force","resource intake capacity",C["green_light"],C["green"])]
    for x,y,t,s,fill,stroke in nodes:
        circle_label(p,x,y,82,fill,stroke,t); text(p,x,y+108,s,13,500,C["muted"],"middle")
    for a,b in [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0)]:
        arrow(p,nodes[a][0],nodes[a][1],nodes[b][0],nodes[b][1],"blue",3)
    text(p,700,495,"feedback unfolds over days to weeks",20,700,C["ink"],"middle")
    note(p,890,["Feeding or forage improvement cannot create an instant field force: eggs and larvae require development time before new adults become nurses and later foragers."],"blue")
    return finish(p)

def fig_15_2():
    p=start("Figure 15.2 — Good and Poor Flight Paths","Apiary entrance orientation away from public routes compared with a poor placement directing bee traffic toward doors, paths or livestock.")
    text(p,55,100,"Flight-path planning is a public-safety control, not just a convenience for the beekeeper.",18,400,C["muted"])
    panel(p,55,160,620,650,"Better placement","green")
    hive(p,150,430,250,300)
    # hedge lifts flight
    for x in range(470,620,28): p.append(f'<rect x="{x}" y="390" width="22" height="220" rx="10" fill="#6FAE62"/>')
    for y in [470,500,530]: p.append(f'<path d="M390 {y} C520 {y-30} 650 {y-130} 680 {y-230}" fill="none" stroke="{C["green"]}" stroke-width="3" marker-end="url(#ag)"/>')
    text(p,340,745,"entrance faces away from public movement; barrier encourages flight to rise",15,600,C["green"],"middle")
    panel(p,725,160,620,650,"Poor placement","red")
    hive(p,800,430,250,300)
    # door/path
    rect(p,1120,350,130,280,"#ECEFF1","#607D8B",3,4); text(p,1185,495,"door",18,700,C["grey"],"middle")
    p.append(f'<line x1="1060" y1="610" x2="1300" y2="610" stroke="#9E9E9E" stroke-width="14"/>')
    for y in [470,510,550]: p.append(f'<line x1="1040" y1="{y}" x2="1160" y2="{y-20}" stroke="{C["red"]}" stroke-width="3"/>')
    text(p,1035,745,"flight crosses doorway / path: repeated conflict risk",15,600,C["red"],"middle")
    note(p,875,["Also consider legal permission, neighbours, livestock, vehicle access and future changes at the site. A good flight path today may become poor after site use changes."],"orange")
    return finish(p)

def fig_15_3():
    p=start("Figure 15.3 — Drainage and Stand Placement","Stable elevated hive stands on well-drained ground contrasted with waterlogged or flood-prone placement.")
    text(p,55,100,"Dry access and stable stands protect colonies, equipment and beekeepers.",18,400,C["muted"])
    panel(p,55,160,620,650,"Well-drained / elevated","green")
    # ground slope
    p.append(f'<path d="M80 690 Q320 600 650 650 L650 790 L80 790 Z" fill="#B9D9A0" stroke="#6B9B55" stroke-width="3"/>')
    # stand
    p.append(f'<line x1="190" y1="560" x2="500" y2="560" stroke="#5D4037" stroke-width="18"/><line x1="220" y1="560" x2="210" y2="660" stroke="#5D4037" stroke-width="14"/><line x1="470" y1="560" x2="460" y2="630" stroke="#5D4037" stroke-width="14"/>')
    hive(p,220,250,250,300)
    p.append(f'<path d="M510 650 C560 625 610 620 650 625" fill="none" stroke="{C["blue"]}" stroke-width="5" marker-end="url(#ab)"/>')
    multi(p,95,735,["stable access","water drains away","hive floor kept above splash/vegetation"],15,500,C["ink"],23)
    panel(p,725,160,620,650,"Waterlogged / flood-prone","red")
    p.append(f'<rect x="760" y="630" width="550" height="160" fill="#B3E5FC" opacity="0.85"/>')
    hive(p,850,400,250,300)
    p.append(f'<path d="M780 620 Q930 585 1100 620 Q1200 650 1290 615" fill="none" stroke="{C["blue"]}" stroke-width="5"/>')
    multi(p,765,735,["muddy/unsafe footing","moisture and equipment damage risk","floodwater can contaminate hive products"],15,500,C["ink"],23)
    note(p,875,["Flood rescue never justifies entering unsafe water, unstable ground or electrical hazards. Site selection should prevent predictable exposure where possible."],"orange")
    return finish(p)

def fig_15_4():
    p=start("Figure 15.4 — Landscape Forage Mosaic","Hedgerows, crops, gardens, woodland edges and semi-natural habitat shown as a changing seasonal forage mosaic rather than a fixed-radius uniform circle.")
    text(p,55,100,"Honey bees use profitable patches within the landscape; they do not exploit every hectare equally.",18,400,C["muted"])
    rect(p,70,160,1260,650,"#F8FBF4","#90A4AE",2,20)
    # apiary center
    for i in range(3): hive(p,590+i*95,500,80,110)
    text(p,700,650,"apiary",18,700,C["brown"],"middle")
    # hedgerow
    for x in range(100,550,35): p.append(f'<circle cx="{x}" cy="350" r="24" fill="#6FAE62"/>')
    text(p,320,300,"hedgerow",17,700,C["green"],"middle")
    # crop
    rect(p,850,220,390,180,"#F5E6A9","#C6A22B",2,12); 
    for x in range(880,1210,45):
        for y in range(255,375,45): flower(p,x,y,0.28,"#E6C748")
    text(p,1045,200,"flowering crop",17,700,C["honey"],"middle")
    # gardens
    for x,y,col in [(210,590,"#D46FA8"),(290,650,"#7EAB62"),(370,580,"#B36DB8")]: flower(p,x,y,0.8,col)
    text(p,290,735,"gardens / urban forage",17,700,C["purple"],"middle")
    # woodland
    for x in [950,1040,1130,1220]:
        p.append(f'<rect x="{x-9}" y="535" width="18" height="130" fill="#7C5A38"/><circle cx="{x}" cy="520" r="58" fill="#5B9A57"/>')
    text(p,1090,735,"woodland edge",17,700,C["green"],"middle")
    # paths rather than radius circle
    for x,y in [(320,350),(1040,310),(290,620),(1090,560)]:
        p.append(f'<path d="M700 555 Q{(700+x)/2} {(555+y)/2-80} {x} {y}" fill="none" stroke="{C["blue"]}" stroke-width="3" stroke-dasharray="8 7" marker-end="url(#ab)"/>')
    note(p,875,["Forage value changes through the year. Record bloom timing and hive response rather than treating a mapped circle around the apiary as uniformly available forage."],"green")
    return finish(p)

ASSETS={
"fig-11-2-distance-dance-tempo.svg":fig_11_2,
"fig-11-4-alarm-recruitment-signals.svg":fig_11_4,
"fig-11-5-swarm-nest-site-communication.svg":fig_11_5,
"fig-12-2-orientation-vs-robbing.svg":fig_12_2,
"fig-12-4-grooming-hygienic-behaviour.svg":fig_12_4,
"fig-12-5-clustering-thermoregulation.svg":fig_12_5,
"fig-13-1-brood-nest-organisation.svg":fig_13_1,
"fig-13-2-colony-superorganism.svg":fig_13_2,
"fig-13-4-resource-flow-colony.svg":fig_13_4,
"fig-14-1-annual-colony-population-cycle.svg":fig_14_1,
"fig-14-2-temperate-warm-climate-patterns.svg":fig_14_2,
"fig-14-4-forage-brood-feedback.svg":fig_14_4,
"fig-15-2-good-poor-flight-paths.svg":fig_15_2,
"fig-15-3-drainage-stand-placement.svg":fig_15_3,
"fig-15-4-landscape-forage-mosaic.svg":fig_15_4,
}

def write_meta():
    data={"wave":2,"batch":"behaviour-site-c","asset_count":len(ASSETS),"assets":[]}
    for name in ASSETS:
        parts=name.split("-"); fid=f"{int(parts[1])}.{int(parts[2])}"
        data["assets"].append({"figure_id":fid,"path":"assets/diagrams/wave-02/"+name,"status":"ACTUAL_VECTOR_CREATED","layout_status":"PENDING_FINAL_LAYOUT_PROOF"})
    META.parent.mkdir(parents=True,exist_ok=True); META.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")

def write_report():
    lines=["# Visual Wave 02 — Behaviour and Site C Review","","**Result:** PASS — A_CORE COMMUNICATION / BEHAVIOUR / COLONY / SEASON / SITE BATCH CREATED","","## Assets created",""]
    lines += ["- "+n for n in ASSETS]
    lines += ["","## Editorial controls","",
              "- Dance-distance figure remains conceptual and avoids a false universal calibration.",
              "- Alarm/defence and food recruitment are separated by context.",
              "- Swarm nest-site decision is distributed among scouts and quorum dynamics; queen is not depicted as choosing the site.",
              "- Orientation flight and robbing are distinguished with multiple behavioural cues rather than one visual feature.",
              "- Grooming and hygienic brood removal are treated as distinct social-defence behaviours.",
              "- Thermoregulation figure avoids treating bearding alone as proof of heat emergency.",
              "- Brood/store arrangement is explicitly representative, not a fixed geometric law.",
              "- Colony-as-superorganism figure avoids anthropomorphic command hierarchy.",
              "- Seasonal curves are conceptual and not hemisphere/month specific.",
              "- Apiary siting prioritises public safety, drainage/flood risk and permission context.",
              "- Forage is depicted as a patchy landscape mosaic, not a uniformly exploited fixed-radius circle.",
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
    print(f"Created {len(ASSETS)} Wave 02 Behaviour/Site C SVGs.")

if __name__=="__main__":
    main()
