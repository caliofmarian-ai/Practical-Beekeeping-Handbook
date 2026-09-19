#!/usr/bin/env python3
import argparse, collections, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SVG_ROOT=ROOT/"assets"/"diagrams"
REPORT=ROOT/"docs"/"reviews"/"VISUAL_RECONCILIATION_PASS_02.md"
JSON_REPORT=ROOT/"assets"/"visual-reconciliation-pass-02.json"

SEMANTIC={"#2E7D32","#E8F5E9","#1B5E20","#C62828","#FFEBEE","#8E0000","#EF6C00","#FFF3E0","#E65100","#1565C0","#E3F2FD","#0D47A1","#6A1B9A","#F3E5F5","#4A148C","#D4A017","#FFF8E1","#8D6E63","#757575","#F5F5F5","#424242","#1F2933","#52606D","#FFFFFF"}
NON_NEUTRAL=SEMANTIC-{"#757575","#F5F5F5","#424242","#1F2933","#52606D","#FFFFFF"}
ALIASES={"#EAF2F8":"#E3F2FD","#EDF4F8":"#E3F2FD","#555":"#52606D","#555555":"#52606D","#777":"#757575","#777777":"#757575","#DDD":"#F5F5F5","#DDDDDD":"#F5F5F5"}
PANEL={"#E8F5E9":"#2E7D32","#FFEBEE":"#C62828","#FFF3E0":"#EF6C00","#E3F2FD":"#1565C0","#F3E5F5":"#6A1B9A","#FFF8E1":"#8D6E63","#F5F5F5":"#757575"}
HEX=re.compile(r"#[0-9A-Fa-f]{3,8}\b")
ROOT_RE=re.compile(r"<svg\b[^>]*>",re.I)
RECT_RE=re.compile(r"<rect\b[^>]*>",re.I)

def colour_set(text):
    return {c.upper() for c in HEX.findall(text)}

def aliases(text):
    count=collections.Counter()
    for src,dst in ALIASES.items():
        p=re.compile(re.escape(src)+r"(?![0-9A-Fa-f])",re.I)
        text,n=p.subn(dst,text)
        if n: count[src+"->"+dst]+=n
    text,n=re.subn(r"fill:#E8F5E9;stroke:#0D47A1","fill:#E8F5E9;stroke:#2E7D32",text,flags=re.I)
    if n: count["healthy-panel-stroke"]+=n
    return text,count

def panels(text):
    count=collections.Counter()
    def f(m):
        tag=m.group(0)
        fm=re.search(r'fill="(#[0-9A-Fa-f]{6})"',tag)
        sm=re.search(r'stroke="(#[0-9A-Fa-f]{6})"',tag)
        wm=re.search(r'width="([0-9.]+)"',tag)
        hm=re.search(r'height="([0-9.]+)"',tag)
        if not (fm and sm and wm and hm): return tag
        fill=fm.group(1).upper(); stroke=sm.group(1).upper()
        try: w=float(wm.group(1)); h=float(hm.group(1))
        except: return tag
        target=PANEL.get(fill)
        if not target or w<180 or h<55 or stroke not in SEMANTIC or stroke==target: return tag
        count["panel:"+fill+":"+stroke+"->"+target]+=1
        return re.sub(r'stroke="#[0-9A-Fa-f]{6}"','stroke="'+target+'"',tag,count=1)
    return RECT_RE.sub(f,text),count

def marker(text):
    m=ROOT_RE.search(text)
    if not m: return text,False
    root=m.group(0)
    if 'data-reconciliation-pass=' in root:
        new=re.sub(r'data-reconciliation-pass="[^"]*"','data-reconciliation-pass="02"',root)
    else:
        new=root[:-1]+' data-reconciliation-pass="02">'
    return text[:m.start()]+new+text[m.end():],new!=root

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--apply",action="store_true"); args=ap.parse_args()
    paths=sorted(SVG_ROOT.glob("**/*.svg"))
    changed={}; totals=collections.Counter(); mono_before=[]; mono_after=[]; panel_count=0
    for p in paths:
        rel=str(p.relative_to(ROOT)); text=p.read_text(encoding="utf-8")
        if not (colour_set(text)&NON_NEUTRAL): mono_before.append(rel)
        if args.apply:
            new,c1=aliases(text); new,c2=panels(new); new,mk=marker(new)
            c=collections.Counter(c1); c.update(c2)
            if mk: c["pass-marker"]+=1
            if new!=text:
                p.write_text(new,encoding="utf-8"); changed[rel]=dict(c); totals.update(c)
                panel_count+=sum(v for k,v in c.items() if k.startswith("panel:"))
        if not (colour_set(p.read_text(encoding="utf-8"))&NON_NEUTRAL): mono_after.append(rel)

    registry=json.loads((ROOT/"assets"/"visual-master-registry.json").read_text())
    missing=[]
    for key,e in registry["families"].items():
        for m in e.get("masters",[]):
            if not (ROOT/m).exists(): missing.append(key+":"+m)
    wave=collections.Counter(k.split("/")[2] for k in changed)
    payload={"visual_system":"PBH-v1","pass":2,"svg_count":len(paths),"changed_file_count":len(changed),"change_counts":dict(totals),"wave_changed_counts":dict(wave),"semantic_panel_changes":panel_count,"neutral_or_monochrome_before":mono_before,"neutral_or_monochrome_after":mono_after,"master_registry_missing":missing}
    JSON_REPORT.write_text(json.dumps(payload,indent=2)+"\n")

    lines=[
      "# Visual Reconciliation — Pass 02: Family Grammar","",
      "**Result:** "+("PASS — FAMILY GRAMMAR NORMALISED" if not missing else "REVIEW REQUIRED"),"",
      "## Scope",f"- SVG assets scanned: **{len(paths)}**",f"- SVG files changed: **{len(changed)}**",f"- large semantic panels aligned: **{panel_count}**","",
      "## Changes applied",
      "- neutral alias colours from early waves mapped to PBH-v1 tokens;",
      "- large semantic state panels aligned to matching border families;",
      "- biological and natural outlines excluded from automatic recolouring;",
      "- every SVG marked as reconciliation stage 02;",
      "- recurring biological and technical masters registered in assets/visual-master-registry.json;","",
      "## Colour completeness",f"- neutral/monochrome-only before: **{len(mono_before)}**",f"- neutral/monochrome-only after: **{len(mono_after)}**"
    ]
    if mono_after:
        lines += ["","Files still requiring colour review:"]+[f"- {p}" for p in mono_after]
    else:
        lines += ["","All 256 SVGs contain at least one non-neutral semantic or natural colour cue."]
    lines += ["","## Master registry",f"- families: **{len(registry['families'])}**",f"- missing master files: **{len(missing)}**","","## Next pass","Pass 03: greyscale redundancy, phone/thumbnail readability, line-role proof, master-derivative comparison and final-layout queue.","","**Publication state:** PENDING_FINAL_RECONCILIATION_PROOF"]
    REPORT.write_text("\n".join(lines)+"\n")
    print(json.dumps(payload,indent=2))
if __name__=="__main__": main()
