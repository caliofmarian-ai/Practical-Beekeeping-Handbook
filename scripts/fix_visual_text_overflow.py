#!/usr/bin/env python3
from __future__ import annotations
import argparse, html, json, math, re
from pathlib import Path
from PIL import ImageFont

ROOT=Path(__file__).resolve().parents[1]
SVG_ROOT=ROOT/"assets"/"diagrams"
REPORT=ROOT/"docs"/"reviews"/"VISUAL_TEXT_FIT_FIXES.md"
JSON_REPORT=ROOT/"assets"/"visual-text-fit-fixes.json"

ROOT_RE=re.compile(r"<svg\b[^>]*>",re.I)
TEXT_BLOCK_RE=re.compile(r'(<text\b[^>]*>)(.*?)</text>',re.I|re.S)
ATTR_RE=re.compile(r'([A-Za-z_:][-A-Za-z0-9_:.]*)="([^"]*)"')
CSS_FONT_SHORTHAND=re.compile(r'\.([A-Za-z0-9_-]+)\s*\{[^}]*?font\s*:[^;}]*?([0-9.]+)px',re.I|re.S)
CSS_FONT_SIZE=re.compile(r'\.([A-Za-z0-9_-]+)\s*\{[^}]*?font-size\s*:\s*([0-9.]+)px',re.I|re.S)
FONT_PATH="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def classes(text):
    out={}
    for c,s in CSS_FONT_SHORTHAND.findall(text):out[c]=float(s)
    for c,s in CSS_FONT_SIZE.findall(text):out[c]=float(s)
    return out

def viewbox(text):
    m=ROOT_RE.search(text); attrs=dict(ATTR_RE.findall(m.group(0))) if m else {}
    v=attrs.get("viewBox","").replace(","," ").split()
    if len(v)==4:return tuple(float(x) for x in v)
    return (0,0,float(attrs.get("width","0")),float(attrs.get("height","0")))

def size_of(attrs,cm):
    if "font-size" in attrs:
        try:return float(attrs["font-size"])
        except:return None
    for c in attrs.get("class","").split():
        if c in cm:return cm[c]
    return None

def measure(text,size):
    try:
        font=ImageFont.truetype(FONT_PATH,max(1,round(size)))
        b=font.getbbox(text);return (b[2]-b[0])*1.05
    except:return len(text)*size*.58

def available(attrs,x0,w,margin=55):
    x=float(attrs.get("x","0").split()[0].split(",")[0])
    a=attrs.get("text-anchor","start")
    if a=="middle":return max(20,2*min(x-(x0+margin),(x0+w-margin)-x))
    if a=="end":return max(20,x-(x0+margin))
    return max(20,(x0+w-margin)-x)

def wrap_words(label,size,maxw):
    words=label.split()
    lines=[]; cur=""
    for word in words:
        trial=word if not cur else cur+" "+word
        if cur and measure(trial,size)>maxw:
            lines.append(cur);cur=word
        else:cur=trial
    if cur:lines.append(cur)
    return lines

def replace_font_size_in_tag(tag,newsize):
    if 'font-size="' in tag:
        return re.sub(r'font-size="[0-9.]+"','font-size="'+str(newsize)+'"',tag,count=1)
    return tag

def replace_class_font(text,cls,oldsize,newsize):
    # Replace only the font-size token inside the named class rule.
    pat=re.compile(r'(\.'+re.escape(cls)+r'\s*\{[^}]*?font\s*:[^;}]*?)([0-9.]+)(px)',re.I|re.S)
    return pat.sub(lambda m:m.group(1)+str(newsize)+m.group(3),text,count=1)

def process(path):
    text=path.read_text(encoding="utf-8")
    x0,y0,w,h=viewbox(text)
    cm=classes(text)
    changes=[]
    # First normalise portrait title scale to the same PBH-v1 34 px visual tier.
    if 'data-canvas-profile="portrait-field"' in text and cm.get("title",0)>34:
        old=cm["title"];text=replace_class_font(text,"title",old,34);changes.append({"kind":"portrait-title","from":old,"to":34})
        cm=classes(text)

    def repl(m):
        open_tag,body=m.group(1),m.group(2)
        attrs=dict(ATTR_RE.findall(open_tag))
        if "transform" in attrs:return m.group(0)
        size=size_of(attrs,cm)
        if not size:return m.group(0)
        label=html.unescape(re.sub(r"<[^>]+>","",body))
        label=re.sub(r"\s+"," ",label).strip()
        if not label:return m.group(0)
        try:x=float(attrs.get("x","0").split()[0].split(",")[0]);y=float(attrs.get("y","0").split()[0].split(",")[0])
        except:return m.group(0)
        maxw=available(attrs,x0,w)
        actual=measure(label,size)
        if actual<=maxw+3:return m.group(0)

        is_title=label.startswith("Figure ")
        is_bottom=y>=y0+h*.84
        if is_title:
            target=max(28,min(34,math.floor(size*maxw/actual)))
            if target<size:
                newtag=replace_font_size_in_tag(open_tag,target)
                # Class title was already normalised; if class-based and still too wide, wrap instead.
                if newtag!=open_tag:
                    changes.append({"kind":"title-size","text":label[:90],"from":size,"to":target})
                    return newtag+body+"</text>"

        # Bottom notes retain font size and scientific content; wrap across available width.
        if is_bottom or len(label)>=80:
            lines=wrap_words(label,size,maxw)
            lineh=max(15,round(size*1.22,1))
            # If too many lines for remaining canvas, modestly reduce to >=12.
            remaining=(y0+h-18)-y
            target=size
            while len(lines)>max(1,int(remaining//lineh)) and target>12:
                target=max(12,target-1)
                maxw=available(attrs,x0,w)
                lines=wrap_words(label,target,maxw)
                lineh=max(15,round(target*1.22,1))
            if len(lines)>=2:
                newtag=replace_font_size_in_tag(open_tag,target)
                xpos=attrs.get("x","0")
                spans=[]
                for i,line in enumerate(lines):
                    dy="0" if i==0 else str(lineh)
                    spans.append('<tspan x="'+xpos+'" dy="'+dy+'">'+html.escape(line,quote=False)+'</tspan>')
                changes.append({"kind":"wrap","text":label[:90],"lines":len(lines),"font":target})
                return newtag+"".join(spans)+"</text>"

        # Internal label: shrink only as far as the PBH-v1 12 px floor.
        target=max(12,math.floor(size*maxw/actual))
        if target<size and measure(label,target)<=maxw+3:
            newtag=replace_font_size_in_tag(open_tag,target)
            if newtag!=open_tag:
                changes.append({"kind":"internal-size","text":label[:90],"from":size,"to":target})
                return newtag+body+"</text>"

        # If a 12px label still cannot fit, wrap it rather than clipping it.
        target=max(12,min(size,14))
        lines=wrap_words(label,target,maxw)
        if len(lines)>=2:
            newtag=replace_font_size_in_tag(open_tag,target)
            xpos=attrs.get("x","0");lineh=max(15,round(target*1.2,1))
            spans=[]
            for i,line in enumerate(lines):
                dy="0" if i==0 else str(lineh)
                spans.append('<tspan x="'+xpos+'" dy="'+dy+'">'+html.escape(line,quote=False)+'</tspan>')
            changes.append({"kind":"internal-wrap","text":label[:90],"lines":len(lines),"font":target})
            return newtag+"".join(spans)+"</text>"
        return m.group(0)

    new=TEXT_BLOCK_RE.sub(repl,text)
    if new!=path.read_text(encoding="utf-8"):
        path.write_text(new,encoding="utf-8")
    return changes

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--apply",action="store_true");args=ap.parse_args()
    all_changes={}
    if args.apply:
        for p in sorted(SVG_ROOT.glob("**/*.svg")):
            ch=process(p)
            if ch:all_changes[str(p.relative_to(ROOT))]=ch
    counts={}
    for changes in all_changes.values():
        for c in changes:counts[c["kind"]]=counts.get(c["kind"],0)+1
    payload={"changed_files":len(all_changes),"change_counts":counts,"changes":all_changes}
    JSON_REPORT.write_text(json.dumps(payload,indent=2)+"\n")
    lines=["# Visual Text-Fit Reconciliation","",f"**Changed SVGs:** **{len(all_changes)}**","", "## Change counts"]
    for k,v in sorted(counts.items()):lines.append(f"- {k}: **{v}**")
    lines += ["","Scientific text was retained. Long notes were wrapped rather than deleted; internal labels were reduced only to the PBH-v1 12 px source floor, otherwise wrapped.","","Final reconciliation validator must confirm that no measured visible text extends beyond the SVG viewBox."]
    REPORT.write_text("\n".join(lines)+"\n")
    print(json.dumps({"changed_files":len(all_changes),"change_counts":counts},indent=2))
if __name__=="__main__":main()
