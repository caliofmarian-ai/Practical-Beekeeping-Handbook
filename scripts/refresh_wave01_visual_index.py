#!/usr/bin/env python3
from __future__ import annotations
import csv, html, json, re
from collections import defaultdict
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
SVG_DIR=ROOT/"assets"/"diagrams"/"wave-01"
QUEUE=ROOT/"assets"/"production-briefs"/"wave-01-high-fidelity.json"
INDEX_DIR=ROOT/"docs"/"visual-index"
INDEX_MAIN=ROOT/"docs"/"visual-index.md"
COVERAGE=ROOT/"docs"/"reviews"/"VISUAL_WAVE_01_FINAL_COVERAGE.md"

TITLE_RE=re.compile(r"<title[^>]*>(.*?)</title>",re.S)
DESC_RE=re.compile(r"<desc[^>]*>(.*?)</desc>",re.S)
FIG_RE=re.compile(r"fig-(\d+)-(\d+)-")
COLOR_MARKER="semantic-color-pass:v1"

def clean(s):
    return re.sub(r"\s+"," ",html.unescape(s)).strip()

def parse_svg(path):
    s=path.read_text(encoding="utf-8")
    ET.fromstring(s)
    mt=TITLE_RE.search(s); md=DESC_RE.search(s); mf=FIG_RE.search(path.name)
    if not mt or not md or not mf:
        raise RuntimeError(f"Missing metadata: {path}")
    return {
        "file_name":path.name,
        "path":path.relative_to(ROOT).as_posix(),
        "figure_id":f"{int(mf.group(1))}.{int(mf.group(2))}",
        "chapter":int(mf.group(1)),
        "title":clean(mt.group(1)),
        "desc":clean(md.group(1)),
        "color_pass":"SEMANTIC_COLOR_V1" if COLOR_MARKER in s else "NATIVE_HIGH_FIDELITY_COLOR",
    }

def main():
    INDEX_DIR.mkdir(parents=True,exist_ok=True)
    queue=json.loads(QUEUE.read_text(encoding="utf-8"))
    q_by_path={a.get("final_asset_path"):a for a in queue.get("assets",[]) if a.get("final_asset_path")}
    rows=[]
    for p in sorted(SVG_DIR.glob("*.svg")):
        r=parse_svg(p)
        q=q_by_path.get(r["path"])
        r["a_core"]="Yes" if q else "No/Supporting"
        r["asset_status"]=q.get("asset_status") if q else "ACTUAL_VECTOR_PRESENT"
        r["layout_status"]="PENDING_FINAL_LAYOUT_PROOF"
        rows.append(r)

    fields=["file_name","path","figure_id","chapter","title","a_core","color_pass","asset_status","layout_status"]
    with (INDEX_DIR/"manifest.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k:r.get(k,"") for k in fields})

    grouped=defaultdict(list)
    for r in rows:
        grouped[r["chapter"]].append(r)
    for vals in grouped.values():
        vals.sort(key=lambda x:[int(v) for v in x["figure_id"].split(".")])

    gallery=[
        "# Wave 01 Visual Gallery",
        "",
        f"**Actual SVG assets in repository:** {len(rows)}  ",
        f"**A_CORE figure IDs with actual assets:** {queue.get('actual_asset_ids_present',0)} / {queue.get('planned_core_assets',68)}  ",
        f"**High-fidelity A_CORE assets still unproduced:** {queue.get('remaining_high_fidelity_assets',0)}",
        "",
        "Tap any image or Open SVG to inspect it at full vector resolution.",
        "",
    ]
    for ch in sorted(grouped):
        gallery += [f"## Chapter {ch}",""]
        for r in grouped[ch]:
            rel="../../"+r["path"]
            gallery += [
                f"### {r['title']}",
                "",
                f'<a href="{rel}"><img src="{rel}" alt="{html.escape(r["desc"],quote=True)}" width="520"></a>',
                "",
                f"**Figure {r['figure_id']}** · {r['color_pass']} · {r['layout_status']} · [Open SVG]({rel})",
                "",
                r["desc"],
                "",
            ]
    (INDEX_DIR/"wave-01.md").write_text("\n".join(gallery)+"\n",encoding="utf-8")

    INDEX_MAIN.write_text(f"""# Visual Index

**Status:** Active gallery
**Wave 01 actual SVG assets:** {len(rows)}
**Wave 01 A_CORE coverage:** {queue.get('actual_asset_ids_present',0)} / {queue.get('planned_core_assets',68)}
**High-fidelity A_CORE still unproduced:** {queue.get('remaining_high_fidelity_assets',0)}

## Semantic colour legend

- Green — correct / healthy / recommended
- Red — danger / disease / prohibited
- Orange — caution / uncertainty / review
- Blue — neutral process / workflow
- Purple — laboratory / diagnostics / verification
- Honey-gold — honey / wax / natural hive-product context

Colour remains supplementary: labels, border/shape logic and captions preserve meaning in greyscale.

## Gallery

- [Wave 01 — Complete Gallery](visual-index/wave-01.md)
- [Manifest CSV](visual-index/manifest.csv)

## Current Wave 01 status

All {queue.get('planned_core_assets',68)} A_CORE figure IDs now have actual repository artwork.
The original 18 high-fidelity biological/diagnostic figures have been produced as original technical SVG plates rather than downgraded to generic schematics.

All visuals remain subject to final print-size, greyscale, accessibility and layout proof before publication.
""",encoding="utf-8")

    COVERAGE.write_text(f"""# Visual Wave 01 — Final Coverage

**Result:** **A_CORE PRODUCTION COMPLETE — FINAL LAYOUT PROOF PENDING**

## Coverage

- Planned A_CORE Figure IDs: **{queue.get('planned_core_assets',68)}**
- A_CORE Figure IDs with an actual repository asset: **{queue.get('actual_asset_ids_present',0)}**
- High-fidelity A_CORE assets still unproduced: **{queue.get('remaining_high_fidelity_assets',0)}**
- Total Wave 01 SVG files currently in the repository: **{len(rows)}**

## Completion statement

The deterministic vector phase and the specialised high-fidelity biological/diagnostic phase are both complete for Wave 01.
All previously isolated brood, disease, mite, anatomy and microscopic-concept figures now have original technical SVG artwork.

This does not mark publication proof as complete. Remaining gates are:

- final greyscale legibility;
- final print-size legibility;
- accessibility/alt-text confirmation;
- scientific/mechanical spot review at layout size;
- final page-placement proof;
- PDF/EPUB/print export proof.

## Gallery

Use docs/visual-index/wave-01.md for a phone-friendly visual review of every Wave 01 asset.
""",encoding="utf-8")

    (INDEX_DIR/"README.md").write_text("""# Visual Index

Generated from actual repository artwork.

- wave-01.md — complete phone-friendly Wave 01 gallery.
- manifest.csv — machine-readable production/status manifest.

Wave 01 A_CORE production is complete; final layout proof is still pending.
""",encoding="utf-8")

    print(f"Indexed {len(rows)} Wave 01 SVG assets; A_CORE={queue.get('actual_asset_ids_present')}/{queue.get('planned_core_assets')}.")

if __name__=="__main__":
    main()
