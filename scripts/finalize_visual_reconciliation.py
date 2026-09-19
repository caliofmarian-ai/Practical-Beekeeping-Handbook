#!/usr/bin/env python3
from __future__ import annotations
import argparse, html, json, re, tempfile, xml.etree.ElementTree as ET
from pathlib import Path
import cairosvg
from PIL import Image, ImageFont

ROOT=Path(__file__).resolve().parents[1]
SVG_ROOT=ROOT/"assets"/"diagrams"
REGISTRY=ROOT/"assets"/"visual-master-registry.json"
PASS03=ROOT/"assets"/"visual-reconciliation-pass-03.json"
REPORT=ROOT/"docs"/"reviews"/"VISUAL_RECONCILIATION_FINAL.md"
JSON_REPORT=ROOT/"assets"/"visual-reconciliation-final.json"

ROOT_RE=re.compile(r"<svg\b[^>]*>",re.I)
TITLE_RE=re.compile(r'<title[^>]*>\s*Figure\s+([0-9]+(?:\.[0-9]+)?)\s+[—-]',re.I)
TEXT_BLOCK_RE=re.compile(r'(<text\b[^>]*>)(.*?)</text>',re.I|re.S)
ATTR_RE=re.compile(r'([A-Za-z_:][-A-Za-z0-9_:.]*)="([^"]*)"')
HEX_RE=re.compile(r"#[0-9A-Fa-f]{6}\b")
CSS_FONT_SHORTHAND=re.compile(r'\.([A-Za-z0-9_-]+)\s*\{[^}]*?font\s*:[^;}]*?([0-9.]+)px',re.I|re.S)
CSS_FONT_SIZE=re.compile(r'\.([A-Za-z0-9_-]+)\s*\{[^}]*?font-size\s*:\s*([0-9.]+)px',re.I|re.S)
RED={"#C62828","#FFEBEE","#8E0000"}
GREEN={"#2E7D32","#E8F5E9","#1B5E20"}
FONT_PATH="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def figure_id(text):
    m=TITLE_RE.search(text)
    return m.group(1) if m else None

def root_attr(text,name,value):
    m=ROOT_RE.search(text)
    if not m: return text
    root=m.group(0)
    pat=re.compile(re.escape(name)+r'="[^"]*"')
    if pat.search(root):
        new=pat.sub(name+'="'+value+'"',root)
    else:
        new=root[:-1]+' '+name+'="'+value+'">'
    return text[:m.start()]+new+text[m.end():]

def render(path,width):
    with tempfile.TemporaryDirectory() as td:
        png=Path(td)/"x.png"
        cairosvg.svg2png(bytestring=path.read_bytes(),write_to=str(png),output_width=width)
        im=Image.open(png).convert("L")
        hist=im.histogram(); total=sum(hist)
        return {
          "width":im.width,"height":im.height,
          "whiteish_fraction":sum(hist[248:256])/total if total else 1.0
        }

def class_font_sizes(text):
    out={}
    for cls,size in CSS_FONT_SHORTHAND.findall(text): out[cls]=float(size)
    for cls,size in CSS_FONT_SIZE.findall(text): out[cls]=float(size)
    return out

def viewbox(text):
    m=ROOT_RE.search(text)
    if not m: return (0,0,0,0)
    attrs=dict(ATTR_RE.findall(m.group(0)))
    vb=attrs.get("viewBox","").replace(","," ").split()
    if len(vb)==4:
        return tuple(float(x) for x in vb)
    return (0,0,float(attrs.get("width","0")),float(attrs.get("height","0")))

def source_font_size(attrs,classes):
    if "font-size" in attrs:
        try:return float(attrs["font-size"])
        except:return None
    cls=attrs.get("class","").split()
    for c in cls:
        if c in classes:return classes[c]
    return None

def text_overflow_checks(text,rel):
    x0,y0,w,h=viewbox(text)
    classes=class_font_sizes(text)
    issues=[]
    for open_tag,body in TEXT_BLOCK_RE.findall(text):
        attrs=dict(ATTR_RE.findall(open_tag))
        if "transform" in attrs: continue
        size=source_font_size(attrs,classes)
        if not size: continue
        raw=re.sub(r"<[^>]+>","",body)
        label=html.unescape(re.sub(r"\s+"," ",raw).strip())
        if not label: continue
        try:x=float(attrs.get("x","0").split()[0].split(",")[0])
        except:continue
        try:y=float(attrs.get("y","0").split()[0].split(",")[0])
        except:y=0
        try:
            font=ImageFont.truetype(FONT_PATH,max(1,round(size)))
            bbox=font.getbbox(label)
            width=(bbox[2]-bbox[0])*1.05
        except:
            width=len(label)*size*0.58
        anchor=attrs.get("text-anchor","start")
        if anchor=="middle": left=x-width/2; right=x+width/2
        elif anchor=="end": left=x-width; right=x
        else: left=x; right=x+width
        if left < x0-3 or right > x0+w+3 or y < y0-3 or y > y0+h+3:
            issues.append({
              "path":rel,"text":label[:180],"font_size":size,
              "estimated_left":round(left,1),"estimated_right":round(right,1),
              "canvas_left":x0,"canvas_right":x0+w,"y":y
            })
    return issues

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--apply",action="store_true"); args=ap.parse_args()
    registry=json.loads(REGISTRY.read_text())
    pass03=json.loads(PASS03.read_text())
    paths=sorted(SVG_ROOT.glob("**/*.svg"))

    by_fid={}
    for p in paths:
        fid=figure_id(p.read_text(encoding="utf-8"))
        if fid: by_fid[fid]=p

    membership={}
    missing_registry=[]
    for family,entry in registry["families"].items():
        for master in entry.get("masters",[]):
            p=ROOT/master
            if not p.exists():
                missing_registry.append({"family":family,"missing":master})
            else:
                membership.setdefault(master,set()).add(family)
        for fid in entry.get("derivatives",[]):
            p=by_fid.get(fid)
            if p is None:
                missing_registry.append({"family":family,"missing_figure_id":fid})
            else:
                membership.setdefault(str(p.relative_to(ROOT)),set()).add(family)

    changed=[]
    if args.apply:
        for p in paths:
            rel=str(p.relative_to(ROOT)); t=p.read_text(encoding="utf-8")
            n=root_attr(t,"data-reconciliation-pass","FINAL")
            fams=sorted(membership.get(rel,[]))
            if fams: n=root_attr(n,"data-master-family",",".join(fams))
            if n!=t:
                p.write_text(n,encoding="utf-8"); changed.append(rel)

    render_fail=[]; blank_like=[]; text_overflow=[]; red_green_fail=[]; min_font_fail=[]; family_marker_fail=[]
    for p in paths:
        rel=str(p.relative_to(ROOT)); t=p.read_text(encoding="utf-8")
        classes=class_font_sizes(t)
        sizes=[]
        for open_tag,_ in TEXT_BLOCK_RE.findall(t):
            a=dict(ATTR_RE.findall(open_tag)); s=source_font_size(a,classes)
            if s:sizes.append(s)
        if sizes and min(sizes)<12:
            min_font_fail.append({"path":rel,"min_font":min(sizes)})
        text_overflow.extend(text_overflow_checks(t,rel))
        cols={x.upper() for x in HEX_RE.findall(t)}
        if cols&RED and cols&GREEN:
            visible_text=len(TEXT_BLOCK_RE.findall(t))
            has_noncolour=(visible_text>=5 or "stroke-dasharray" in t or "marker-end" in t)
            if not has_noncolour:
                red_green_fail.append({"path":rel,"visible_text_nodes":visible_text})
        if rel in membership:
            m=ROOT_RE.search(t); root=m.group(0) if m else ""
            mm=re.search(r'data-master-family="([^"]+)"',root)
            actual=set(mm.group(1).split(",")) if mm else set()
            if not membership[rel].issubset(actual):
                family_marker_fail.append({"path":rel,"expected":sorted(membership[rel]),"actual":sorted(actual)})
        try:
            for width in (520,390):
                m=render(p,width)
                if m["whiteish_fraction"]>0.995:
                    blank_like.append({"path":rel,"width":width,"whiteish_fraction":m["whiteish_fraction"]})
        except Exception as ex:
            render_fail.append({"path":rel,"error":str(ex)})

    pass03_dirty=bool(pass03.get("render_failures") or pass03.get("blank_like_renders") or pass03.get("critical_text_under_10") or pass03.get("small_text_10_to_under_12") or pass03.get("master_derivatives_missing"))
    hard_fail=bool(render_fail or blank_like or text_overflow or red_green_fail or min_font_fail or family_marker_fail or missing_registry or pass03_dirty)
    status="HOLD" if hard_fail else "READY_FOR_LAYOUT_PROOF"

    if args.apply:
        for p in paths:
            t=p.read_text(encoding="utf-8")
            n=root_attr(t,"data-reconciliation-status",status)
            if n!=t:
                p.write_text(n,encoding="utf-8")
                rel=str(p.relative_to(ROOT))
                if rel not in changed: changed.append(rel)

    payload={
      "visual_system":"PBH-v1","status":status,"svg_count":len(paths),"changed_file_count":len(changed),
      "registered_family_assets":len(membership),"registered_families":len(registry["families"]),
      "render_failures":render_fail,"blank_like_renders":blank_like,"text_overflow_flags":text_overflow,
      "red_green_redundancy_failures":red_green_fail,"minimum_font_failures":min_font_fail,
      "family_marker_failures":family_marker_fail,"missing_registry_items":missing_registry,"pass03_clean":not pass03_dirty
    }
    JSON_REPORT.write_text(json.dumps(payload,indent=2)+"\n")

    lines=[
      "# Final Visual Reconciliation Report","",
      "**Result:** **"+status+"**","",
      "## Scope", "- SVG assets: **"+str(len(paths))+"**","- A_CORE production target: **230 / 230**",
      "- registered master families: **"+str(len(registry["families"]))+"**",
      "- SVGs explicitly linked to a master family: **"+str(len(membership))+"**","",
      "## Final hard gates",
      "- render failures: **"+str(len(render_fail))+"**",
      "- blank-like renders: **"+str(len(blank_like))+"**",
      "- estimated visible-text overflow flags: **"+str(len(text_overflow))+"**",
      "- source text below 12 px: **"+str(len(min_font_fail))+"**",
      "- red/green figures lacking non-colour cue proxy: **"+str(len(red_green_fail))+"**",
      "- missing master-family markers: **"+str(len(family_marker_fail))+"**",
      "- missing master/derivative registry items: **"+str(len(missing_registry))+"**",
      "- Pass 03 hard QA clean: **"+("YES" if payload["pass03_clean"] else "NO")+"**","",
      "## Reconciliation conclusion",
      "Figma, Canva, generated SVG and other production methods are tools only. Final assets are governed by PBH-v1 in GitHub.",
      "The final set uses one semantic colour grammar, one typography policy, three intentional canvas layout profiles, registered biological/technical masters, accessibility metadata and proof-level rendering checks.","",
      "Long explanatory notes are retained when measured text remains within the SVG canvas; final page-layout proof will decide composition without deleting scientific content.","",
      "## Next publication stage",
      "If status is READY_FOR_LAYOUT_PROOF, visual reconciliation is complete. Next: final page composition, print-size proof, PDF/EPUB rendering, index/cross-reference proof and print-ready packaging."
    ]
    if hard_fail:
        lines += ["","## HOLD details"]
        for name,items in [("Render failures",render_fail),("Blank renders",blank_like),("Text overflow",text_overflow),("Red/green redundancy",red_green_fail),("Minimum font",min_font_fail),("Family marker",family_marker_fail),("Registry gaps",missing_registry)]:
            if items:
                lines += ["","### "+name]
                for item in items[:120]: lines.append("- "+json.dumps(item,ensure_ascii=False))
    REPORT.write_text("\n".join(lines)+"\n")
    print(json.dumps(payload,indent=2))

if __name__=="__main__":
    main()
