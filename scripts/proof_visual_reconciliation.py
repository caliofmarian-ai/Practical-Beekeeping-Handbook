#!/usr/bin/env python3
from __future__ import annotations
import json, math, re, statistics, tempfile
from pathlib import Path

import cairosvg
from PIL import Image, ImageStat

ROOT=Path(__file__).resolve().parents[1]
SVG_ROOT=ROOT/"assets"/"diagrams"
REPORT=ROOT/"docs"/"reviews"/"VISUAL_RECONCILIATION_PASS_03.md"
JSON_REPORT=ROOT/"assets"/"visual-reconciliation-pass-03.json"
REGISTRY=ROOT/"assets"/"visual-master-registry.json"

FONT_ATTR=re.compile(r'font-size="([0-9.]+)"')
FONT_CSS=re.compile(r'font\s*:\s*[^;}]*?([0-9.]+)px',re.I)
TITLE_RE=re.compile(r'<title[^>]*>\s*Figure\s+([0-9]+(?:\.[0-9]+)?)\s+[—-]',re.I)
TEXT_RE=re.compile(r'<text\b[^>]*>(.*?)</text>',re.I|re.S)
TAG_RE=re.compile(r'<[^>]+>')
HEX_RE=re.compile(r"#[0-9A-Fa-f]{6}\b")

RED={"#C62828","#FFEBEE","#8E0000"}
GREEN={"#2E7D32","#E8F5E9","#1B5E20"}

def profile(text:str)->str:
    m=re.search(r'data-canvas-profile="([^"]+)"',text)
    return m.group(1) if m else "unknown"

def font_sizes(text:str):
    vals=[float(x) for x in FONT_ATTR.findall(text)]
    vals += [float(x) for x in FONT_CSS.findall(text)]
    return vals

def text_nodes(text:str):
    out=[]
    for raw in TEXT_RE.findall(text):
        clean=TAG_RE.sub("",raw)
        clean=re.sub(r"\s+"," ",clean).strip()
        if clean: out.append(clean)
    return out

def render_metrics(path:Path):
    data=path.read_bytes()
    result={}
    with tempfile.TemporaryDirectory() as td:
        for width in (520,390):
            out=Path(td)/f"{width}.png"
            cairosvg.svg2png(bytestring=data,write_to=str(out),output_width=width)
            im=Image.open(out).convert("RGB")
            gs=im.convert("L")
            st=ImageStat.Stat(gs)
            hist=gs.histogram()
            total=sum(hist)
            whiteish=sum(hist[248:256])/total if total else 1
            dark=sum(hist[:90])/total if total else 0
            result[str(width)]={
                "width":im.width,"height":im.height,
                "grayscale_mean":round(st.mean[0],3),
                "grayscale_stddev":round(st.stddev[0],3),
                "whiteish_fraction":round(whiteish,5),
                "dark_fraction":round(dark,5)
            }
    return result

def main():
    paths=sorted(SVG_ROOT.glob("**/*.svg"))
    render_fail=[]
    blank_like=[]
    critical_text=[]
    small_text=[]
    long_lines=[]
    dual_red_green=[]
    figure_ids={}
    render_summary={}
    profile_counts={}
    min_font_by_profile={}

    for p in paths:
        rel=str(p.relative_to(ROOT))
        text=p.read_text(encoding="utf-8")
        prof=profile(text)
        profile_counts[prof]=profile_counts.get(prof,0)+1
        title=TITLE_RE.search(text)
        if title: figure_ids[title.group(1)]=rel

        fs=font_sizes(text)
        if fs:
            mn=min(fs)
            min_font_by_profile.setdefault(prof,[]).append(mn)
            if mn<10:
                critical_text.append({"path":rel,"min_font":mn})
            elif mn<12:
                small_text.append({"path":rel,"min_font":mn})
        for line in text_nodes(text):
            if len(line)>110:
                long_lines.append({"path":rel,"chars":len(line),"text":line[:180]})

        cols={c.upper() for c in HEX_RE.findall(text)}
        if cols&RED and cols&GREEN:
            dual_red_green.append(rel)

        try:
            rm=render_metrics(p)
            render_summary[rel]=rm
            for width,m in rm.items():
                if m["whiteish_fraction"]>0.995 or m["grayscale_stddev"]<7:
                    blank_like.append({"path":rel,"width":int(width),**m})
        except Exception as e:
            render_fail.append({"path":rel,"error":str(e)})

    registry=json.loads(REGISTRY.read_text(encoding="utf-8"))
    missing_derivatives=[]
    for family,entry in registry["families"].items():
        for fid in entry.get("derivatives",[]):
            if fid not in figure_ids:
                missing_derivatives.append({"family":family,"figure_id":fid})

    prof_font_stats={}
    for prof,vals in min_font_by_profile.items():
        prof_font_stats[prof]={
            "count":len(vals),
            "min":min(vals),
            "median":statistics.median(vals),
            "p10":sorted(vals)[max(0,math.floor(len(vals)*0.1)-1)]
        }

    payload={
      "visual_system":"PBH-v1","pass":3,"svg_count":len(paths),
      "render_failures":render_fail,
      "blank_like_renders":blank_like,
      "critical_text_under_10":critical_text,
      "small_text_10_to_under_12":small_text,
      "long_single_text_nodes":long_lines,
      "red_green_dual_semantic_files":dual_red_green,
      "master_derivatives_missing":missing_derivatives,
      "canvas_profiles":profile_counts,
      "minimum_font_stats_by_profile":prof_font_stats,
      "render_summary":render_summary
    }
    JSON_REPORT.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")

    hard_fail=bool(render_fail or blank_like or missing_derivatives or critical_text)
    lines=[
      "# Visual Reconciliation — Pass 03: Proof-Level QA","",
      "**Result:** "+("HOLD — HARD QA ISSUES FOUND" if hard_fail else "PASS — RENDER / ACCESSIBILITY PROOF COMPLETE; EDITORIAL SPOT-CHECK QUEUE REMAINS"),"",
      "## Render proof",
      f"- SVGs rendered at 520 px and 390 px: **{len(paths)-len(render_fail)} / {len(paths)}**",
      f"- render failures: **{len(render_fail)}**",
      f"- blank-like / near-empty renders: **{len(blank_like)}**","",
      "## Typography/readability proxy",
      f"- critical source text below 10 px: **{len(critical_text)}**",
      f"- review text from 10 px to below 12 px: **{len(small_text)}**",
      f"- unusually long single text nodes over 110 characters: **{len(long_lines)}**","",
      "These thresholds are a proof queue, not an automatic failure for every scientific micro-label. No text is resized blindly because that can create overlap or corrupt anatomical annotation.","",
      "## Greyscale / colour-independence proxy",
      f"- files containing both red and green semantic colours and therefore requiring explicit non-colour cue spot-check: **{len(dual_red_green)}**",
      "- all figures were rasterised to greyscale during rendering and checked for non-blank luminance structure;",
      "- semantic meaning still requires family-level editorial spot checks for labels/icons/border patterns.","",
      "## Master-family proof",
      f"- registered master families: **{len(registry['families'])}**",
      f"- missing registered derivative Figure IDs: **{len(missing_derivatives)}**","",
      "## Canvas profiles"
    ]
    for k,v in sorted(profile_counts.items()):
        lines.append(f"- {k}: **{v}**")
    lines += ["","## Minimum source font by profile"]
    for k,v in sorted(prof_font_stats.items()):
        lines.append(f"- {k}: min {v['min']} px · median {v['median']} px · p10 {v['p10']} px")
    if critical_text:
        lines += ["","### Critical text queue"]+[f"- {r['path']}: {r['min_font']} px" for r in critical_text]
    if small_text:
        lines += ["","### Small-text review queue"]+[f"- {r['path']}: {r['min_font']} px" for r in small_text]
    if long_lines:
        lines += ["","### Long single-node text review queue"]+[f"- {r['path']}: {r['chars']} chars" for r in long_lines[:80]]
    lines += ["","## Next action","Resolve any hard QA flags, then run targeted editorial spot checks on red/green figures and master-family derivatives. After those checks, promote the visual system from PENDING_FINAL_RECONCILIATION_PROOF to READY_FOR_LAYOUT_PROOF.","","**Publication state:** PENDING_FINAL_RECONCILIATION_PROOF"]
    REPORT.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in payload.items() if k!="render_summary"},indent=2))

if __name__=="__main__": main()
