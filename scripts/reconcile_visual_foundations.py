#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SVG_ROOT = ROOT / "assets" / "diagrams"
REPORT = ROOT / "docs" / "reviews" / "VISUAL_RECONCILIATION_PASS_01.md"
JSON_REPORT = ROOT / "assets" / "visual-reconciliation-pass-01.json"

CANONICAL = {
    "#2E7D32","#E8F5E9","#1B5E20",
    "#C62828","#FFEBEE","#8E0000",
    "#EF6C00","#FFF3E0","#E65100",
    "#1565C0","#E3F2FD","#0D47A1",
    "#6A1B9A","#F3E5F5","#4A148C",
    "#D4A017","#FFF8E1","#8D6E63",
    "#757575","#F5F5F5","#424242",
    "#1F2933","#52606D","#FFFFFF"
}
NATURAL_ALLOWED = {
    "#FFF4C8","#D4C27A","#F6E3B4","#D6C6A0","#FFF9E5",
    "#F6CF58","#C38A57","#8A5A35","#E1A11E","#9A6515",
    "#E0A419","#5D4037","#D9EEF7","#8AB8C8","#7EAFC3",
    "#3C2E25","#4FC3F7","#FDFDFD","#B8B8B0","#E9E4D6",
    "#FFFDF4","#B98755","#D7AB7A","#F0C55F","#C7701A",
    "#E3A52F","#A65B24","#D98C10","#C88D28","#F7D66D",
    "#FFF5B5","#FFF7D6","#37474F","#64B5F6","#B0BEC5",
    "#FFFDF3","#E0F2F1","#00897B","#CE93D8"
}

ROOT_RE = re.compile(r"<svg\b[^>]*>", re.I)
DIM_RE = re.compile(r'\b(width|height)="([^"]+)"')
VIEWBOX_RE = re.compile(r'\bviewBox="([^"]+)"', re.I)
HEX_RE = re.compile(r"#[0-9A-Fa-f]{3,8}\b")
STROKE_RE = re.compile(r'stroke-width="([^"]+)"')
FONT_ATTR_RE = re.compile(r'font-family="([^"]+)"')
FONT_STACK_RE = re.compile(r'Arial\s*,\s*(?:Helvetica\s*,\s*)?sans-serif', re.I)

def canvas_profile(width: str|None, height: str|None, viewbox: str|None) -> str:
    pair = (width or "", height or "")
    if pair == ("1400","1000"):
        return "landscape-standard"
    if pair == ("1400","1050"):
        return "landscape-scientific"
    if pair == ("1200","1600"):
        return "portrait-field"
    if viewbox:
        vals=viewbox.replace(","," ").split()
        if len(vals)==4:
            try:
                w,h=float(vals[2]),float(vals[3])
                if h>w:
                    return "portrait-custom"
                return "landscape-custom"
            except ValueError:
                pass
    return "custom"

def root_meta(text: str) -> dict:
    m=ROOT_RE.search(text)
    root=m.group(0) if m else ""
    dims=dict(DIM_RE.findall(root))
    vb=VIEWBOX_RE.search(root)
    return {
        "root": root,
        "width": dims.get("width"),
        "height": dims.get("height"),
        "viewBox": vb.group(1) if vb else None,
        "profile": canvas_profile(dims.get("width"),dims.get("height"),vb.group(1) if vb else None),
        "role_img": 'role="img"' in root,
        "aria": 'aria-labelledby="title desc"' in root,
        "visual_system": 'data-visual-system="PBH-v1"' in root,
        "preserve_aspect": 'preserveAspectRatio=' in root,
    }

def normalise(text: str, profile: str) -> tuple[str,list[str]]:
    changes=[]
    m=ROOT_RE.search(text)
    if not m:
        return text,["missing-root"]
    root=m.group(0)
    new=root
    if 'data-visual-system=' not in new:
        new=new[:-1] + ' data-visual-system="PBH-v1">'
        changes.append("visual-system-marker")
    if 'data-canvas-profile=' not in new:
        new=new[:-1] + f' data-canvas-profile="{profile}">'
        changes.append("canvas-profile-marker")
    if 'preserveAspectRatio=' not in new:
        new=new[:-1] + ' preserveAspectRatio="xMidYMid meet">'
        changes.append("preserve-aspect-ratio")
    if 'role="img"' not in new:
        new=new[:-1] + ' role="img">'
        changes.append("role-img")
    if '<title' in text and '<desc' in text and 'aria-labelledby=' not in new:
        new=new[:-1] + ' aria-labelledby="title desc">'
        changes.append("aria-labelledby")
    text=text[:m.start()]+new+text[m.end():]

    before=text
    text=FONT_STACK_RE.sub("Arial,Helvetica,sans-serif",text)
    if text!=before:
        changes.append("font-stack")

    before=text
    text=re.sub(r'(?i)#fff(?![0-9a-f])',"#FFFFFF",text)
    if text!=before:
        changes.append("white-token")

    before=text
    text=re.sub(r'(?i)#(?:111|222)(?![0-9a-f])',"#1F2933",text)
    if text!=before:
        changes.append("ink-token")

    if "visual-system:PBH-v1" not in text:
        root_end=ROOT_RE.search(text).end()
        text=text[:root_end]+'\n<!-- visual-system:PBH-v1 -->'+text[root_end:]
        changes.append("reconciliation-comment")
    return text,changes

def scan(path: Path) -> dict:
    text=path.read_text(encoding="utf-8")
    meta=root_meta(text)
    colors=[c.upper() for c in HEX_RE.findall(text)]
    fonts=FONT_ATTR_RE.findall(text)
    css_font_variants=sorted(set(re.findall(r'font:[^;}]+',text)))
    strokes=STROKE_RE.findall(text)
    return {
        "path": str(path.relative_to(ROOT)),
        **{k:v for k,v in meta.items() if k!="root"},
        "has_title": "<title" in text,
        "has_desc": "<desc" in text,
        "font_attrs": sorted(set(fonts)),
        "uses_arial_stack": bool(re.search(r'Arial\s*,\s*(?:Helvetica\s*,\s*)?sans-serif',text,re.I)),
        "css_font_variants": css_font_variants[:20],
        "colors": sorted(set(colors)),
        "unknown_colors": sorted({c for c in colors if c not in CANONICAL and c not in NATURAL_ALLOWED}),
        "stroke_widths": sorted(set(strokes)),
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--apply",action="store_true")
    args=ap.parse_args()

    paths=sorted(SVG_ROOT.glob("**/*.svg"))
    before=[scan(p) for p in paths]
    changed={}
    if args.apply:
        for p,rec in zip(paths,before):
            text=p.read_text(encoding="utf-8")
            new,changes=normalise(text,rec["profile"])
            if new!=text:
                p.write_text(new,encoding="utf-8")
                changed[rec["path"]]=changes
    after=[scan(p) for p in paths]

    profiles=collections.Counter(r["profile"] for r in after)
    wave_counts=collections.Counter(r["path"].split("/")[2] for r in after)
    missing_title=[r["path"] for r in after if not r["has_title"]]
    missing_desc=[r["path"] for r in after if not r["has_desc"]]
    missing_aria=[r["path"] for r in after if not r["aria"]]
    missing_system=[r["path"] for r in after if not r["visual_system"]]
    font_deviation=[r["path"] for r in after if ("<text" in (ROOT/r["path"]).read_text(encoding="utf-8") and not r["uses_arial_stack"])]
    unknown=[r for r in after if r["unknown_colors"]]

    payload={
        "visual_system":"PBH-v1",
        "svg_count":len(after),
        "changed_file_count":len(changed),
        "changed":changed,
        "wave_counts":dict(wave_counts),
        "canvas_profiles":dict(profiles),
        "missing_title":missing_title,
        "missing_desc":missing_desc,
        "missing_aria":missing_aria,
        "missing_visual_system_marker":missing_system,
        "font_deviation":font_deviation,
        "unknown_colour_files":[{"path":r["path"],"colours":r["unknown_colors"]} for r in unknown],
        "stroke_width_inventory":sorted({s for r in after for s in r["stroke_widths"]}),
    }
    JSON_REPORT.parent.mkdir(parents=True,exist_ok=True)
    JSON_REPORT.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")

    lines=[
        "# Visual Reconciliation — Pass 01: Foundations",
        "",
        "**Result:** " + ("PASS — SAFE GLOBAL FOUNDATIONS NORMALISED" if not missing_title and not missing_desc and not missing_aria and not missing_system and not font_deviation else "REVIEW REQUIRED"),
        "",
        "## Scope",
        f"- SVG assets scanned: **{len(after)}**",
        f"- SVG files changed by safe normalisation: **{len(changed)}**",
        f"- Waves/directories: **{len(wave_counts)}**",
        "",
        "## Safe normalisation applied",
        "- added `data-visual-system=\"PBH-v1\"` to every SVG root;",
        "- classified each SVG with a canvas-profile marker without resizing biological/technical content;",
        "- added `preserveAspectRatio=\"xMidYMid meet\"` where absent;",
        "- normalised the handbook sans-serif stack to `Arial,Helvetica,sans-serif`;",
        "- normalised shorthand white and pure near-black tokens to the canonical white/ink tokens;",
        "- preserved biological/natural colours and did **not** force high-fidelity plates into schematic colours;",
        "",
        "## Canvas profiles",
    ]
    for k,v in sorted(profiles.items()):
        lines.append(f"- {k}: **{v}**")
    lines += [
        "",
        "Canvas profiles are intentional layout classes, not separate visual styles. Final layout may scale them, but reconciliation must preserve one typography/colour/line-work grammar.",
        "",
        "## Metadata/accessibility gate",
        f"- missing title: **{len(missing_title)}**",
        f"- missing desc: **{len(missing_desc)}**",
        f"- missing aria-labelledby: **{len(missing_aria)}**",
        f"- missing PBH-v1 marker: **{len(missing_system)}**",
        f"- text-bearing files outside canonical Arial/Helvetica stack after pass: **{len(font_deviation)}**",
        "",
        "## Colour drift requiring editorial review",
        f"- files containing colours outside the canonical semantic + approved natural/biological allowance set: **{len(unknown)}**",
        "",
        "These colours are **not automatically replaced** because morphology, natural materials and diagnostic appearance take priority over branding. They are queued for Pass 02 family-level review.",
        "",
        "## Line-weight review",
        f"- distinct stroke-width values detected: **{len(payload['stroke_width_inventory'])}**",
        "",
        "Pass 01 does not flatten all stroke widths: anatomy and microscopic detail require finer lines than process diagrams. Pass 02 will map values to family-level primary/secondary/detail roles.",
        "",
        "## Next mandatory pass",
        "Pass 02 will reconcile visual families rather than doing blind global replacements:",
        "- process/decision-flow grammar;",
        "- safety/caution/danger cards;",
        "- healthy brood / queen-cell / Varroa / anatomy masters;",
        "- honey-product and clean-zone systems;",
        "- traceability/legal/business diagrams;",
        "- recurring icons, arrows and callouts;",
        "- greyscale and thumbnail checks.",
        "",
        "**Publication state:** `PENDING_FINAL_RECONCILIATION`",
    ]
    if unknown:
        lines += ["","### Files queued for colour-family review"]
        for r in unknown[:80]:
            lines.append(f"- `{r['path']}`: {', '.join(r['unknown_colors'])}")
        if len(unknown)>80:
            lines.append(f"- … plus {len(unknown)-80} more; full list in `assets/visual-reconciliation-pass-01.json`.")
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({"svg_count":len(after),"changed":len(changed),"unknown_colour_files":len(unknown),"profiles":dict(profiles)},indent=2))

if __name__=="__main__":
    main()
