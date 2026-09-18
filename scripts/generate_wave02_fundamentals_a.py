#!/usr/bin/env python3
from __future__ import annotations
import math, json
from pathlib import Path
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"assets"/"diagrams"/"wave-02"
REPORT=ROOT/"docs"/"reviews"/"VISUAL_WAVE_02_FUNDAMENTALS_A_REVIEW.md"
META=ROOT/"assets"/"production-briefs"/"wave-02-fundamentals-a.json"
W,H=1400,1000
FONT="Arial,Helvetica,sans-serif"
C={
"ink":"#1F2933","muted":"#52606D","blue":"#1565C0","blue_light":"#E3F2FD","green":"#2E7D32","green_light":"#E8F5E9",
"orange":"#EF6C00","orange_light":"#FFF3E0","red":"#C62828","red_light":"#FFEBEE","purple":"#6A1B9A","purple_light":"#F3E5F5",
"honey":"#D4A017","honey_light":"#FFF8E1","wax":"#F4E7A1","brown":"#8D6E63","grey":"#757575","grey_light":"#F5F5F5",
"bee":"#E0A419","bee_dark":"#5D4037","wing":"#D9EEF7","pollen":"#D98C10","propolis":"#7A4D31","rj":"#FFF3D1","venom":"#C62828"
}

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
def arrow(p,x1,y1,x2,y2,color="blue",label=None,width=4):
    cmap={"blue":C["blue"],"green":C["green"],"orange":C["orange"]}
    mmap={"blue":"ab","green":"ag","orange":"ao"}
    col=cmap[color]
    p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{width}" marker-end="url(#{mmap[color]})"/>')
    if label: text(p,(x1+x2)/2,(y1+y2)/2-9,label,14,700,col,"middle")
def note(p,lines,y=880,kind="orange"):
    pal={"orange":(C["orange_light"],C["orange"]),"blue":(C["blue_light"],C["blue"]),"green":(C["green_light"],C["green"])}
    fill,stroke=pal[kind]; rect(p,55,y,1290,80,fill,stroke,2.5,14); multi(p,78,y+29,lines,17,600,C["ink"],23)
def circle_label(p,cx,cy,r,fill,stroke,title,sub=None):
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>')
    text(p,cx,cy-3,title,18,700,stroke,"middle")
    if sub: text(p,cx,cy+24,sub,13,500,C["muted"],"middle")
def bee_icon(p,cx,cy,s=1.0,queen=False,drone=False):
    body=C["bee"]
    p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{38*s}" ry="{27*s}" fill="{body}" stroke="{C["bee_dark"]}" stroke-width="{2*s}"/>')
    abdomen_rx=55*s if queen else 46*s
    abdomen_ry=24*s if not drone else 31*s
    p.append(f'<ellipse cx="{cx+70*s}" cy="{cy}" rx="{abdomen_rx}" ry="{abdomen_ry}" fill="{body}" stroke="{C["bee_dark"]}" stroke-width="{2*s}"/>')
    p.append(f'<circle cx="{cx-48*s}" cy="{cy}" r="{22*s}" fill="{body}" stroke="{C["bee_dark"]}" stroke-width="{2*s}"/>')
    for off in [45,70,95]: p.append(f'<line x1="{cx+off*s}" y1="{cy-abdomen_ry}" x2="{cx+off*s}" y2="{cy+abdomen_ry}" stroke="{C["bee_dark"]}" stroke-width="{3*s}"/>')
    p.append(f'<path d="M {cx-5*s} {cy-18*s} C {cx+15*s} {cy-70*s} {cx+65*s} {cy-65*s} {cx+48*s} {cy-15*s} Z" fill="{C["wing"]}" opacity="0.8" stroke="#8AB8C8" stroke-width="{1.5*s}"/>')
    if drone:
        p.append(f'<circle cx="{cx-58*s}" cy="{cy-5*s}" r="{11*s}" fill="#3C2E25"/><circle cx="{cx-38*s}" cy="{cy-5*s}" r="{11*s}" fill="#3C2E25"/>')
def hive_box(p,x,y,w=360,h=440):
    p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#F6E3B4" stroke="{C["brown"]}" stroke-width="5"/>')
    p.append(f'<rect x="{x-15}" y="{y-35}" width="{w+30}" height="38" fill="#D6C6A0" stroke="{C["brown"]}" stroke-width="4"/>')
    p.append(f'<rect x="{x+15}" y="{y+h}" width="{w-30}" height="24" fill="#D6C6A0" stroke="{C["brown"]}" stroke-width="4"/>')
def comb_frame(p,x,y,w=90,h=340,brood=False,pollen=False,honey=False):
    p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#FFF9E5" stroke="{C["brown"]}" stroke-width="4"/>')
    if honey: rect(p,x+12,y+15,w-24,70,"#F6CF58",C["honey"],1.5,5)
    if brood: rect(p,x+15,y+110,w-30,145,"#C38A57","#8A5A35",1.5,20)
    if pollen: rect(p,x+18,y+275,w-36,45,"#E1A11E","#9A6515",1.5,6)
def flower(p,cx,cy,s=1,color="#D774A8"):
    for ang in range(0,360,72):
        a=math.radians(ang)
        p.append(f'<ellipse cx="{cx+22*s*math.cos(a)}" cy="{cy+22*s*math.sin(a)}" rx="{18*s}" ry="{10*s}" fill="{color}" transform="rotate({ang} {cx+22*s*math.cos(a)} {cy+22*s*math.sin(a)})"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{11*s}" fill="#F4C542"/>')
def hive_product_icon(p,cx,cy,kind):
    if kind=="honey":
        p.append(f'<path d="M{cx} {cy-34} C{cx-24} {cy-8} {cx-28} {cy+8} {cx} {cy+33} C{cx+28} {cy+8} {cx+24} {cy-8} {cx} {cy-34} Z" fill="#E0A51B" stroke="#9A6A0A" stroke-width="3"/>')
    elif kind=="wax":
        p.append(f'<polygon points="{cx-38},{cy} {cx-19},{cy-33} {cx+19},{cy-33} {cx+38},{cy} {cx+19},{cy+33} {cx-19},{cy+33}" fill="{C["wax"]}" stroke="{C["brown"]}" stroke-width="3"/>')
    elif kind=="pollen":
        for dx,dy,col in [(-18,-8,"#D98C10"),(4,-18,"#E7B438"),(20,4,"#B76E1E"),(-10,18,"#D8A927")]: p.append(f'<circle cx="{cx+dx}" cy="{cy+dy}" r="15" fill="{col}"/>')
    elif kind=="propolis":
        p.append(f'<path d="M{cx-35} {cy+18} L{cx-10} {cy-30} L{cx+32} {cy-18} L{cx+40} {cy+18} L{cx+5} {cy+32} Z" fill="{C["propolis"]}" stroke="#4E3224" stroke-width="3"/>')
    elif kind=="rj":
        p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="42" ry="30" fill="{C["rj"]}" stroke="#C2A85A" stroke-width="3"/>')
    elif kind=="venom":
        p.append(f'<path d="M{cx} {cy-35} C{cx-25} {cy-8} {cx-26} {cy+12} {cx} {cy+35} C{cx+26} {cy+12} {cx+25} {cy-8} {cx} {cy-35} Z" fill="#E6C6D0" stroke="{C["red"]}" stroke-width="3"/>')
        p.append(f'<path d="M{cx+25} {cy+8} L{cx+55} {cy+28}" stroke="{C["red"]}" stroke-width="5"/>')

def fig_1_2():
    p=start("Figure 1.2 — What a Colony Contains","Generic hive cutaway showing queen, workers, drones when present, brood, pollen, honey and comb without implying fixed positions.")
    text(p,55,100,"A colony is the living social unit; the hive is its housing. Resource and brood positions vary.",18,400,C["muted"])
    hive_box(p,160,180,520,620)
    for i,x in enumerate([210,320,430,540]):
        comb_frame(p,x,255,85,455,brood=(i in (1,2)),pollen=(i in (1,2,3)),honey=True)
    bee_icon(p,870,315,0.75,queen=True); text(p,1020,320,"queen",18,700,C["purple"])
    for px,py in [(860,440),(930,470),(820,520)]: bee_icon(p,px,py,0.42)
    text(p,1020,470,"workers",18,700,C["blue"])
    bee_icon(p,885,615,0.55,drone=True); text(p,1020,620,"drone when present",18,700,C["orange"])
    arrow(p,700,310,790,315,"blue"); text(p,750,280,"comb stores / brood",15,700,C["blue"],"middle")
    panel(p,790,710,500,115,"Key distinction","green")
    multi(p,815,755,["Colony = queen, workers, drones when present, brood and stores.","Hive = the physical housing and removable equipment."],16,600,C["ink"],22)
    note(p,880,["This cutaway is schematic. Brood, pollen and honey are organised dynamically and should not be read as fixed to these exact positions."],"blue")
    return finish(p)

def fig_1_3():
    p=start("Figure 1.3 — The Beekeeping Year at a Glance","Season-neutral circular sequence of colony build-up, reproduction/swarming pressure, surplus collection, preparation and winter/dearth survival.")
    text(p,55,100,"The sequence is biological rather than tied to fixed calendar months or one hemisphere.",18,400,C["muted"])
    cx,cy=700,500
    stages=[("Build-up","brood and workforce increase",270,C["green_light"],C["green"]),
            ("Reproduction pressure","swarming risk can rise",0,C["orange_light"],C["orange"]),
            ("Surplus collection","nectar storage and honey crop",70,C["honey_light"],C["honey"]),
            ("Preparation","stores, health and colony structure",145,C["blue_light"],C["blue"]),
            ("Winter / dearth survival","conserve heat/resources; conditions vary",215,C["purple_light"],C["purple"])]
    coords=[]
    for title,sub,ang,fill,stroke in stages:
        a=math.radians(ang); x=cx+300*math.cos(a); y=cy+290*math.sin(a); coords.append((x,y))
        rect(p,x-130,y-70,260,140,fill,stroke,3,22); text(p,x,y-15,title,18,700,stroke,"middle"); multi(p,x,y+15,[sub],14,500,C["ink"],20,"middle")
    for i in range(len(coords)):
        x1,y1=coords[i]; x2,y2=coords[(i+1)%len(coords)]
        arrow(p,x1,y1,x2,y2,"blue",width=3)
    circle_label(p,cx,cy,110,C["grey_light"],C["grey"],"COLONY CYCLE","climate + forage + health")
    note(p,880,["Warm climates may not have a broodless winter. Use local phenology and colony observations rather than fixed seasonal dates."],"orange")
    return finish(p)

def fig_1_4():
    p=start("Figure 1.4 — Beginner Decision Path","Beginner beekeeping path from learning biology through equipment, site, healthy bees, systematic inspection, health monitoring, surplus harvest and records.")
    text(p,55,100,"A reliable beginner sequence puts biology and safety before honey yield.",18,400,C["muted"])
    steps=[("1 Learn biology","understand colony, brood, food and season"),("2 Obtain safe equipment","hive system, PPE, smoker/tools"),("3 Select a site","access, flight path, water, forage, safety"),("4 Acquire healthy bees","traceable source and health baseline"),("5 Inspect systematically","answer defined questions, avoid over-opening"),("6 Monitor health","Varroa, disease signs, food and queen status"),("7 Harvest only surplus","ripeness + colony stores + food safety"),("8 Keep records","actions, results, treatments, follow-up")]
    x0,y0=70,180
    for i,(t,s) in enumerate(steps):
        row=i//4; col=i%4; x=x0+col*325; y=y0+row*300
        k="green" if i in (0,7) else "blue"; panel(p,x,y,280,190,t,k); multi(p,x+18,y+75,[s],15,500,C["ink"],21)
        if col<3: arrow(p,x+280,y+95,x+315,y+95,"blue")
        elif row==0: arrow(p,x+140,y+190,x+140,y+275,"blue")
    note(p,835,["The path is iterative: records from inspections and monitoring feed back into better decisions rather than a one-way march toward harvest."],"green")
    return finish(p)

def fig_2_1():
    p=start("Figure 2.1 — Timeline of Beekeeping Development","Conceptual timeline from honey hunting and fixed-comb hives to movable frames, centrifugal extraction and modern bee-health/precision systems without forcing one universal global chronology.")
    text(p,55,100,"Different regions followed different paths; this is a technology sequence, not a single worldwide timeline.",18,400,C["muted"])
    y=510; p.append(f'<line x1="100" y1="{y}" x2="1300" y2="{y}" stroke="{C["blue"]}" stroke-width="7"/>')
    items=[(150,"Honey hunting",["wild nests","destructive harvest risk"]),(410,"Fixed-comb hives",["skeps/logs/clay/boxes","regional traditions"]),(690,"Movable frames",["inspectable comb","bee-space principle"]),(950,"Centrifugal extraction",["comb reuse","larger-scale harvest"]),(1220,"Modern systems",["bee health/IPM","data + food standards"])]
    for i,(x,t,sub) in enumerate(items):
        col=[C["orange"],C["brown"],C["green"],C["honey"],C["purple"]][i]
        p.append(f'<circle cx="{x}" cy="{y}" r="24" fill="#FFFFFF" stroke="{col}" stroke-width="7"/>')
        rect(p,x-120,220 if i%2==0 else 610,240,150,"#FFFFFF",col,2.5,18); text(p,x,260 if i%2==0 else 650,t,18,700,col,"middle"); multi(p,x,292 if i%2==0 else 682,sub,14,500,C["ink"],20,"middle")
    note(p,865,["Historical practices should be interpreted in their regional context. The sequence does not imply that every society progressed through the same hive forms or dates."],"orange")
    return finish(p)

def fig_2_3():
    p=start("Figure 2.3 — Movable-Frame Breakthrough","Technical comparison of fixed comb attached to a hive wall versus removable frames preserving deliberate bee-space gaps.")
    text(p,55,100,"Movable frames allow individual combs to be removed and inspected without routinely destroying the nest.",18,400,C["muted"])
    panel(p,55,160,620,650,"Fixed comb","orange")
    rect(p,125,255,470,430,"#FFF8E1",C["brown"],4,10)
    for i in range(4):
        x=185+i*95; p.append(f'<path d="M{x} 285 C{x-20} 390 {x-15} 550 {x} 630 C{x+25} 550 {x+20} 390 {x} 285 Z" fill="{C["wax"]}" stroke="{C["brown"]}" stroke-width="4"/>')
    multi(p,95,735,["Comb is attached to the cavity/hive.","Inspection or harvest may require cutting comb.","Spacing is created by bees, not the beekeeper."],17,500,C["ink"],26)
    panel(p,725,160,620,650,"Movable-frame system","green")
    rect(p,795,255,470,430,"#FFF8E1",C["brown"],4,10)
    for i in range(4):
        x=850+i*100; rect(p,x,290,65,330,"#FFFDF0",C["brown"],4,5)
    # bee spaces
    for x in [930,1030,1130]:
        p.append(f'<line x1="{x}" y1="320" x2="{x}" y2="590" stroke="{C["blue"]}" stroke-width="4" stroke-dasharray="8 7"/>')
    text(p,1030,660,"controlled gaps preserve removable comb",16,700,C["blue"],"middle")
    note(p,865,["Bee space is a design principle, not one universal hive dimension. Actual frame and box dimensions depend on the hive system."],"blue")
    return finish(p)

def fig_2_4():
    p=start("Figure 2.4 — Global Traditions","Map-style overview of regional historical apiculture traditions, presented as parallel traditions rather than one linear global progression.")
    text(p,55,100,"Representative examples only; regional practices overlap and changed through time.",18,400,C["muted"])
    # stylised continents
    rect(p,80,180,1240,620,"#F8FBFD","#90A4AE",2,28)
    shapes=[("Europe",330,300,"skeps, logs, boxes"),("North Africa / Mediterranean",610,480,"clay and horizontal hives"),("Sub-Saharan Africa",440,650,"log, bark and local hives"),("West / Central Asia",830,330,"clay, wall and box traditions"),("South / East Asia",1030,520,"log, wall, movable and indigenous systems"),("Americas",180,515,"honey hunting, stingless-bee and later imported systems")]
    for i,(name,x,y,sub) in enumerate(shapes):
        fill=[C["blue_light"],C["orange_light"],C["green_light"],C["purple_light"],C["honey_light"],C["grey_light"]][i]
        stroke=[C["blue"],C["orange"],C["green"],C["purple"],C["honey"],C["grey"]][i]
        circle_label(p,x,y,78,fill,stroke,name)
        text(p,x,y+105,sub,14,500,C["muted"],"middle")
    note(p,850,["This overview is deliberately non-linear. Historical hive forms were shaped by local materials, bee species/subspecies, climate, culture and harvesting goals."],"orange")
    return finish(p)

def fig_3_2():
    p=start("Figure 3.2 — Pollination Is a Network","Network linking flowering crops and wild plants to honey bees and several wild-pollinator groups, showing that honey bees are important but not the only pollinators.")
    text(p,55,100,"Pollination outcomes emerge from plant traits, pollinator communities, weather and landscape context.",18,400,C["muted"])
    plant_nodes=[(200,260,"Fruit crop","#E57373"),(200,500,"Seed crop","#81C784"),(200,740,"Wild plant","#BA68C8")]
    poll_nodes=[(760,220,"Honey bees","managed + feral",C["honey_light"],C["honey"]),(1040,340,"Wild bees","diverse taxa",C["green_light"],C["green"]),(1040,590,"Hoverflies","important in many systems",C["blue_light"],C["blue"]),(760,740,"Butterflies / moths","context-dependent",C["purple_light"],C["purple"])]
    for x,y,t,col in plant_nodes:
        flower(p,x-55,y,1.0,col); text(p,x+10,y+6,t,18,700,C["ink"])
    for x,y,t,sub,fill,stroke in poll_nodes: circle_label(p,x,y,80,fill,stroke,t,sub)
    for px,py,_,_ in plant_nodes:
        for qx,qy,_,_,_,_ in poll_nodes:
            p.append(f'<line x1="{px+90}" y1="{py}" x2="{qx-85}" y2="{qy}" stroke="#B0BEC5" stroke-width="2.2" opacity="0.8"/>')
    note(p,865,["Managed honey bees can be valuable crop pollinators, but pollinator abundance is not the same as pollinator biodiversity. Conservation should include diverse wild pollinator groups."],"green")
    return finish(p)

def fig_3_3():
    p=start("Figure 3.3 — Managed Bees Versus Wild Pollinator Conservation","Side-by-side distinction between livestock management of Apis mellifera and conservation of diverse wild bee, hoverfly and butterfly communities.")
    text(p,55,100,"Managed-colony health and wild-pollinator conservation are related but different objectives.",18,400,C["muted"])
    panel(p,55,160,620,650,"Managed honey bees — livestock management","blue")
    hive_box(p,145,285,250,300); bee_icon(p,470,350,0.6)
    multi(p,95,650,["• beekeeper controls housing, movement and treatments","• colony health, Varroa and food production are managed","• stocking density and forage competition still matter"],17,500,C["ink"],27)
    panel(p,725,160,620,650,"Wild pollinators — biodiversity conservation","green")
    flower(p,930,340,1.2,"#D46FA8"); flower(p,1120,390,0.9,"#7FBF6A")
    bee_icon(p,880,510,0.35)
    p.append(f'<ellipse cx="1060" cy="520" rx="24" ry="14" fill="#6A8FB3"/><path d="M1035 512 Q1000 470 1018 450" fill="none" stroke="#9CCCE2" stroke-width="5"/><path d="M1085 512 Q1120 470 1102 450" fill="none" stroke="#9CCCE2" stroke-width="5"/>')
    p.append(f'<path d="M1180 500 Q1140 455 1120 500 Q1140 545 1180 500 Q1220 455 1240 500 Q1220 545 1180 500" fill="#D98CDB" stroke="#7B4A7A" stroke-width="2"/>')
    multi(p,765,650,["• conserve nesting sites, host plants and landscape diversity","• avoid assuming one managed species replaces wild diversity","• habitat and pesticide risk operate at landscape scale"],17,500,C["ink"],27)
    note(p,865,["A good pollinator strategy can support both responsible managed-bee husbandry and wild-pollinator habitat without treating them as interchangeable."],"green")
    return finish(p)

def fig_3_4():
    p=start("Figure 3.4 — Ecosystem-Service Pathway","Flower visitation to pollen transfer, fruit or seed set, and food/ecological outcomes, with an explicit caveat that plant dependence on animal pollination varies.")
    text(p,55,100,"The pathway is conditional: some plants depend strongly on animal pollination, others only partly or not at all.",18,400,C["muted"])
    steps=[("Flower visitation","pollinator contacts floral structures"),("Pollen transfer","compatible pollen reaches stigma"),("Fertilisation","when biology and timing permit"),("Fruit / seed set","quantity or quality may improve"),("Food / ecological outcomes","yield, regeneration, wildlife resources")]
    for i,(t,s) in enumerate(steps):
        x=50+i*270; panel(p,x,260,235,360,t,"green" if i in (1,3) else "blue")
        if i==0: flower(p,x+118,440,1.2,"#D46FA8"); bee_icon(p,x+95,365,0.28)
        elif i==1:
            p.append(f'<circle cx="{x+118}" cy="420" r="52" fill="#FFF7CC" stroke="{C["orange"]}" stroke-width="3"/>')
            for k in range(8):
                a=math.radians(k*45); p.append(f'<circle cx="{x+118+35*math.cos(a)}" cy="{420+35*math.sin(a)}" r="7" fill="{C["pollen"]}"/>')
        elif i==2:
            p.append(f'<ellipse cx="{x+118}" cy="420" rx="55" ry="80" fill="#D7E8A2" stroke="{C["green"]}" stroke-width="3"/>')
        elif i==3:
            p.append(f'<circle cx="{x+118}" cy="420" r="62" fill="#E57373" stroke="#B23A3A" stroke-width="3"/>')
        else:
            flower(p,x+90,410,0.8,"#8E63B6"); p.append(f'<circle cx="{x+155}" cy="440" r="36" fill="#F6CF58" stroke="#A37312" stroke-width="3"/>')
        multi(p,x+18,550,[s],14,500,C["ink"],20)
        if i<4: arrow(p,x+235,440,x+270,440,"blue")
    note(p,850,["Do not convert this pathway into a universal percentage of food production. Pollinator dependence varies by crop, cultivar, region and production system."],"orange")
    return finish(p)

def fig_4_1():
    p=start("Figure 4.1 — Hive-Product Overview","Six hive products—honey, beeswax, pollen, propolis, royal jelly and bee venom—shown with their biological origin in the colony.")
    text(p,55,100,"Products differ in biological origin, collection method, preservation needs and safety risks.",18,400,C["muted"])
    items=[("Honey","nectar/honeydew collected, processed and ripened by bees","honey"),("Beeswax","wax scales secreted by worker abdominal glands","wax"),("Pollen","plant pollen carried by foragers; bee bread is stored/processed pollen","pollen"),("Propolis","plant resins collected and modified by bees","propolis"),("Royal jelly","glandular secretion of nurse workers","rj"),("Bee venom","venom-gland/sting apparatus product; high allergy hazard","venom")]
    for i,(t,s,k) in enumerate(items):
        row=i//3; col=i%3; x=70+col*440; y=170+row*360
        panel(p,x,y,390,300,t,"red" if k=="venom" else "honey")
        hive_product_icon(p,x+85,y+125,k); multi(p,x+155,y+105,[s],15,500,C["ink"],22)
        if k=="venom": text(p,x+155,y+215,"ANAPHYLAXIS RISK",16,700,C["red"])
    note(p,875,["Biological activity reported in research does not automatically authorise a consumer health claim. Product category and claims are regulated separately."],"orange")
    return finish(p)

def fig_4_2():
    p=start("Figure 4.2 — Product Origin Map Inside the Hive","Hive cutaway mapping honey, wax, pollen/bee bread, propolis, royal jelly and venom to their biological origin or storage site.")
    text(p,55,100,"The map separates where a product is made, collected, stored or delivered; not every product is stored in comb.",18,400,C["muted"])
    hive_box(p,120,170,670,650)
    for i,x in enumerate([180,315,450,585]):
        comb_frame(p,x,255,95,470,brood=(i in (1,2)),pollen=(i in (1,2)),honey=True)
    # product labels around hive
    callouts=[("Honey",900,210,"stored in comb after nectar/honeydew processing",C["honey"]),("Wax",1090,320,"worker wax glands → comb construction",C["brown"]),("Pollen / bee bread",950,450,"forager pollen loads → stored/processed cells",C["pollen"]),("Propolis",1080,590,"plant resin → cracks and nest surfaces",C["propolis"]),("Royal jelly",870,700,"nurse glands → fed to larvae/queen",C["purple"]),("Venom",1130,760,"venom gland + sting apparatus, not comb storage",C["red"])]
    for title,x,y,sub,col in callouts:
        p.append(f'<circle cx="{x}" cy="{y}" r="8" fill="{col}"/>'); text(p,x+18,y+5,title,17,700,col); text(p,x+18,y+27,sub,13,500,C["muted"])
    arrow(p,790,300,890,210,"blue"); arrow(p,620,550,1060,590,"orange"); arrow(p,670,680,850,700,"blue")
    note(p,875,["The diagram is functional, not anatomical scale. It prevents a common misunderstanding: propolis, royal jelly and venom are not simply 'stored hive products' like honey."],"blue")
    return finish(p)

def fig_4_4():
    p=start("Figure 4.4 — From Colony to Market","Hive-product chain from harvest through hygiene or preservation, traceability, testing where required, and compliant packaging and claims.")
    text(p,55,100,"Different products need different controls, but every commercial chain must preserve identity, safety and truthful claims.",18,400,C["muted"])
    steps=[("1 Harvest","appropriate colony/product method"),("2 Preserve / handle hygienically","drying, cooling, clean equipment as product requires"),("3 Traceability","apiary, date, lot, process, inputs"),("4 Test where required","moisture, residues, microbiology, identity, quality"),("5 Pack correctly","food/contact suitability, net quantity, storage"),("6 Claims and sale","origin/product claims supported and legally permitted")]
    for i,(t,s) in enumerate(steps):
        row=i//3; col=i%3; x=75+col*440; y=190+row*330
        panel(p,x,y,390,235,t,"green" if i in (2,4) else "blue"); multi(p,x+20,y+85,[s],15,500,C["ink"],22)
        if col<2: arrow(p,x+390,y+120,x+430,y+120,"blue")
        elif row==0: arrow(p,x+195,y+235,x+195,y+305,"blue")
    note(p,870,["Testing is risk- and product-dependent. No amount of processing or marketing can legitimately 'fix' an unidentified or contaminated lot."],"orange")
    return finish(p)

def fig_5_2():
    p=start("Figure 5.2 — Evidence-Based Decision Loop","Observe, measure, interpret, act, verify, record and improve shown as a continuous beekeeping management loop.")
    text(p,55,100,"A decision is incomplete until its effect is checked and recorded.",18,400,C["muted"])
    cx,cy=700,505; r=300
    nodes=[("Observe",270),("Measure",322),("Interpret",14),("Act",66),("Verify",118),("Record",170),("Improve",220)]
    coords=[]
    for i,(t,ang) in enumerate(nodes):
        a=math.radians(ang); x=cx+r*math.cos(a); y=cy+r*math.sin(a); coords.append((x,y))
        fill=[C["blue_light"],C["purple_light"],C["orange_light"],C["green_light"],C["green_light"],C["blue_light"],C["honey_light"]][i]
        stroke=[C["blue"],C["purple"],C["orange"],C["green"],C["green"],C["blue"],C["brown"]][i]
        circle_label(p,x,y,78,fill,stroke,t)
    for i in range(len(coords)):
        x1,y1=coords[i]; x2,y2=coords[(i+1)%len(coords)]; arrow(p,x1,y1,x2,y2,"blue",width=3)
    circle_label(p,cx,cy,108,C["grey_light"],C["grey"],"EVIDENCE","not habit alone")
    note(p,875,["Examples: mite count before/after control, hive weight before/after feeding, colony response after requeening. Verification prevents repeated ineffective action."],"green")
    return finish(p)

def fig_5_3():
    p=start("Figure 5.3 — Traditional Tools and Precision Tools","Hive tool, smoker and direct frame inspection shown alongside scales, sensors and digital records; technology augments rather than replaces biological inspection.")
    text(p,55,100,"Precision tools increase observation frequency, but sensors do not diagnose a colony by themselves.",18,400,C["muted"])
    panel(p,55,160,620,650,"Direct / traditional tools","honey")
    # hive tool
    p.append(f'<path d="M150 320 L430 270 L445 300 L165 355 Z" fill="#9AA5B1" stroke="#4E5964" stroke-width="4"/>')
    text(p,300,395,"hive tool",18,700,C["grey"],"middle")
    # smoker
    p.append(f'<rect x="180" y="470" width="110" height="160" rx="22" fill="#B0BEC5" stroke="#546E7A" stroke-width="4"/><path d="M235 470 L260 410 L310 390" fill="none" stroke="#546E7A" stroke-width="16"/>')
    text(p,235,675,"smoker",18,700,C["grey"],"middle")
    comb_frame(p,440,455,120,220,brood=True,pollen=True,honey=True); text(p,500,705,"frame inspection",18,700,C["brown"],"middle")
    panel(p,725,160,620,650,"Precision / digital tools","blue")
    # scale
    rect(p,800,300,180,90,"#ECEFF1","#607D8B",4,12); text(p,890,355,"hive scale",18,700,C["blue"],"middle")
    # sensor
    p.append(f'<circle cx="1120" cy="340" r="65" fill="{C["purple_light"]}" stroke="{C["purple"]}" stroke-width="4"/>'); text(p,1120,347,"sensor",18,700,C["purple"],"middle")
    # phone records
    rect(p,860,500,170,260,"#FAFAFA","#455A64",6,24); rect(p,885,540,120,110,C["blue_light"],C["blue"],2,8); text(p,945,690,"records",18,700,C["blue"],"middle")
    # chart
    p.append(f'<polyline points="1090,700 1130,650 1170,670 1210,590 1250,610" fill="none" stroke="{C["green"]}" stroke-width="6"/>'); text(p,1175,745,"trend data",18,700,C["green"],"middle")
    note(p,875,["Use technology as an additional observation layer. Validate unusual sensor readings with colony inspection, calibrated equipment and biological context."],"orange")
    return finish(p)

def fig_5_4():
    p=start("Figure 5.4 — Modern Risk Landscape","Modern beekeeping risk map linking Varroa/viruses, invasive pests, climate/weather, pesticides, market standards and labour/business constraints.")
    text(p,55,100,"Risk is multi-domain: biological, environmental, food-production and business pressures interact.",18,400,C["muted"])
    circle_label(p,700,500,110,C["honey_light"],C["brown"],"BEEKEEPING","system")
    nodes=[(260,240,"Varroa + viruses","parasite–pathogen pressure","red"),(700,190,"Invasive pests","surveillance / movement","orange"),(1140,250,"Climate + weather","forage, heat, drought, storms","blue"),(1140,700,"Pesticides","exposure + incident response","orange"),(700,815,"Market standards","food safety, labels, authenticity","purple"),(260,700,"Labour + business","cost, time, cash flow, skill","green")]
    for x,y,t,s,k in nodes:
        pal={"red":(C["red_light"],C["red"]),"orange":(C["orange_light"],C["orange"]),"blue":(C["blue_light"],C["blue"]),"purple":(C["purple_light"],C["purple"]),"green":(C["green_light"],C["green"])}
        fill,stroke=pal[k]; circle_label(p,x,y,92,fill,stroke,t); text(p,x,y+120,s,14,500,C["muted"],"middle"); p.append(f'<line x1="{x}" y1="{y}" x2="700" y2="500" stroke="#B0BEC5" stroke-width="3"/>')
    note(p,900,["A modern management plan should not optimise only honey yield. Colony health, food compliance, environmental risk and business resilience all constrain decisions."],"blue")
    return finish(p)

ASSETS={
"fig-01-2-what-a-colony-contains.svg":fig_1_2,
"fig-01-3-beekeeping-year-at-a-glance.svg":fig_1_3,
"fig-01-4-beginner-decision-path.svg":fig_1_4,
"fig-02-1-beekeeping-development-timeline.svg":fig_2_1,
"fig-02-3-movable-frame-breakthrough.svg":fig_2_3,
"fig-02-4-global-traditions.svg":fig_2_4,
"fig-03-2-pollination-network.svg":fig_3_2,
"fig-03-3-managed-vs-wild-pollinators.svg":fig_3_3,
"fig-03-4-ecosystem-service-pathway.svg":fig_3_4,
"fig-04-1-hive-product-overview.svg":fig_4_1,
"fig-04-2-product-origin-map.svg":fig_4_2,
"fig-04-4-from-colony-to-market.svg":fig_4_4,
"fig-05-2-evidence-based-decision-loop.svg":fig_5_2,
"fig-05-3-traditional-vs-precision-tools.svg":fig_5_3,
"fig-05-4-modern-risk-landscape.svg":fig_5_4,
}

def write_meta():
    data={"wave":2,"batch":"fundamentals-a","asset_count":len(ASSETS),"assets":[]}
    for name in ASSETS:
        parts=name.split("-")
        fid=f"{int(parts[1])}.{int(parts[2])}"
        data["assets"].append({"figure_id":fid,"path":"assets/diagrams/wave-02/"+name,"status":"ACTUAL_VECTOR_CREATED","layout_status":"PENDING_FINAL_LAYOUT_PROOF"})
    META.parent.mkdir(parents=True,exist_ok=True); META.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")

def write_report():
    lines=["# Visual Wave 02 — Fundamentals A Review","","**Result:** PASS — FIRST FUNDAMENTALS A_CORE VECTOR BATCH CREATED","","## Assets created",""]
    lines += ["- "+name for name in ASSETS]
    lines += ["","## Editorial controls","",
              "- Chapter 1 distinguishes colony from hive and avoids a fixed brood/store layout.",
              "- Seasonal cycle is climate/hemisphere neutral.",
              "- Historical timeline is conceptual and does not imply one global linear progression.",
              "- Pollination figures explicitly include wild pollinator diversity and avoid unsupported global percentages.",
              "- Hive-product figures separate biological origin from market claims and visibly flag venom allergy risk.",
              "- Technology is presented as augmentation, not autonomous colony diagnosis.",
              "- Modern-risk map combines biological, environmental, food-standard and business constraints.",
              "","## Remaining gates","",
              "All assets remain subject to final print-size, greyscale, accessibility and layout proof.",""]
    REPORT.parent.mkdir(parents=True,exist_ok=True); REPORT.write_text("\n".join(lines),encoding="utf-8")

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for name,fn in ASSETS.items():
        s=fn(); ET.fromstring(s)
        if "<title" not in s or "<desc" not in s: raise RuntimeError(name)
        (OUT/name).write_text(s,encoding="utf-8")
    write_meta(); write_report()
    print(f"Created {len(ASSETS)} Wave 02 Fundamentals A SVGs.")

if __name__=="__main__":
    main()
