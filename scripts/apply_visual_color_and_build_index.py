#!/usr/bin/env python3
from __future__ import annotations
import csv, html, json, re
from collections import defaultdict
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SVG_DIR = ROOT / "assets" / "diagrams" / "wave-01"
DOCS_DIR = ROOT / "docs"
INDEX_DIR = DOCS_DIR / "visual-index"
REPORT_DIR = DOCS_DIR / "reviews"
HF_PATH = ROOT / "assets" / "production-briefs" / "wave-01-high-fidelity.json"

P = {
 "green":"#2E7D32","green_light":"#E8F5E9","red":"#C62828","red_light":"#FFEBEE",
 "orange":"#EF6C00","orange_light":"#FFF3E0","blue":"#1565C0","blue_light":"#E3F2FD",
 "purple":"#6A1B9A","purple_light":"#F3E5F5","honey":"#D4A017","honey_light":"#FFF8E1",
 "brown":"#8D6E63","grey":"#757575","ink":"#1F2933","muted":"#52606D"
}
THEMES = {
 "safety": dict(primary=P["blue"],dark="#0D47A1",box=P["blue_light"],box2=P["green_light"],obj="#EAF2F8"),
 "operations": dict(primary=P["blue"],dark="#0D47A1",box=P["blue_light"],box2=P["green_light"],obj="#EDF4F8"),
 "emergency": dict(primary=P["orange"],dark="#E65100",box=P["orange_light"],box2=P["blue_light"],obj="#FFF8F0"),
 "health": dict(primary=P["purple"],dark="#4A148C",box=P["purple_light"],box2=P["blue_light"],obj="#F7F2FA"),
 "ipm": dict(primary=P["blue"],dark="#0D47A1",box=P["blue_light"],box2=P["green_light"],obj="#EEF6F3"),
}
CATEGORY = {
 21:("Safety","safety"),22:("Safety","safety"),23:("Safety","safety"),
 24:("Hive Installation","operations"),25:("Hive Inspection","operations"),33:("Moving Colonies","operations"),
 38:("Emergency Colony Management","emergency"),
 39:("Bee Health / Disease","health"),40:("Bee Health / Parasites","health"),
 41:("Bee Health / Varroa","health"),42:("Bee Health / Nosema","health"),
 43:("Bee Health / AFB","health"),44:("Bee Health / EFB","health"),
 45:("Bee Health / Viruses","health"),46:("Bee Health / IPM","ipm"),
}
STYLE_RE=re.compile(r"<style>.*?</style>",re.S)
TITLE_RE=re.compile(r"<title[^>]*>(.*?)</title>",re.S)
DESC_RE=re.compile(r"<desc[^>]*>(.*?)</desc>",re.S)
FIG_RE=re.compile(r"fig-(\d+)-(\d+)-")
MARKER="<!-- semantic-color-pass:v1 -->"

def chap(name):
 m=FIG_RE.search(name)
 if not m: raise ValueError(name)
 return int(m.group(1))

def figid(name):
 m=FIG_RE.search(name)
 return f"{int(m.group(1))}.{int(m.group(2))}" if m else "?"

def clean(s):
 return re.sub(r"\s+"," ",html.unescape(s)).strip()

def css(t):
 return f"""<style>
.bg{{fill:#fff}}.title{{font:700 38px Arial,sans-serif;fill:{P['ink']}}}.subtitle{{font:400 22px Arial,sans-serif;fill:{P['muted']}}}
.box{{fill:{t['box']};stroke:{t['dark']};stroke-width:3}}.box2{{fill:{t['box2']};stroke:{t['dark']};stroke-width:3}}
.stop{{fill:{P['red_light']};stroke:{P['red']};stroke-width:5;stroke-dasharray:12 8}}
.legal{{fill:{P['purple_light']};stroke:{P['purple']};stroke-width:4;stroke-dasharray:5 5}}
.label{{font:700 24px Arial,sans-serif;fill:{P['ink']}}}.body{{font:400 21px Arial,sans-serif;fill:{P['ink']}}}.small{{font:400 18px Arial,sans-serif;fill:{P['muted']}}}
.arrow{{stroke:{t['primary']};stroke-width:4;fill:none;marker-end:url(#arrow)}}.thin{{stroke:{P['grey']};stroke-width:2;fill:none}}
.hub{{fill:{t['dark']};stroke:{t['dark']};stroke-width:3}}.hubtext{{font:700 22px Arial,sans-serif;fill:#fff;text-anchor:middle}}
.note{{fill:{P['honey_light']};stroke:{P['brown']};stroke-width:2}}
.good{{fill:{P['green_light']};stroke:{P['green']};stroke-width:3}}
.warn{{fill:{P['orange_light']};stroke:{P['orange']};stroke-width:3;stroke-dasharray:8 5}}
.danger{{fill:{P['red_light']};stroke:{P['red']};stroke-width:4}}
.lab{{fill:{P['purple_light']};stroke:{P['purple']};stroke-width:3}}
.natural{{fill:{P['honey_light']};stroke:{P['brown']};stroke-width:3}}
</style>"""

def theme(ch):
 key=CATEGORY.get(ch,("General","operations"))[1]
 return key,THEMES[key]

def recolor(path):
 s=path.read_text(encoding="utf-8")
 ch=chap(path.name); theme_name,t=theme(ch)
 if not STYLE_RE.search(s): raise RuntimeError(f"No style block: {path}")
 s=STYLE_RE.sub(css(t),s,count=1)
 s=re.sub(r'(<marker id="arrow".*?<path[^>]*?fill=")#[0-9A-Fa-f]{3,6}(")',rf'\g<1>{t["primary"]}\2',s,count=1,flags=re.S)
 for old,new in {"#eee":t["obj"],"#f7f7f7":t["box"],"#e9e9e9":t["box2"],"#efefef":P["purple_light"],"#fafafa":P["honey_light"]}.items():
  s=re.sub(re.escape(old),new,s,flags=re.I)
 if MARKER not in s:
  s=s.replace(">\n<title",">\n"+MARKER+"\n<title",1)
 ET.fromstring(s)
 mt,md=TITLE_RE.search(s),DESC_RE.search(s)
 if not mt or not md: raise RuntimeError(f"Missing title/desc: {path}")
 path.write_text(s,encoding="utf-8")
 return {
  "file_name":path.name,"path":path.relative_to(ROOT).as_posix(),"figure_id":figid(path.name),
  "chapter":ch,"title":clean(mt.group(1)),"desc":clean(md.group(1)),
  "category":CATEGORY.get(ch,("General","operations"))[0],"theme":theme_name,
  "status":"ACTUAL_VECTOR_PRESENT","color_pass":"SEMANTIC_COLOR_V1",
  "high_fidelity_required":"No","notes":"Final layout/greyscale proof still required."
 }

def high_fidelity():
 if not HF_PATH.exists(): return []
 data=json.loads(HF_PATH.read_text(encoding="utf-8"))
 out=[]
 for a in data.get("assets",[]):
  ch=int(a.get("chapter",0))
  out.append({
   "file_name":"","path":"","figure_id":str(a.get("figure_id","")),"chapter":ch,
   "title":a.get("working_title",""),"desc":a.get("brief",""),
   "category":CATEGORY.get(ch,("Bee Health / High Fidelity","health"))[0],"theme":"high-fidelity",
   "status":"HIGH_FIDELITY_PENDING","color_pass":"NOT_APPLICABLE_YET","high_fidelity_required":"Yes",
   "notes":a.get("recommended_medium","High-fidelity asset required.")
  })
 return out

def make_outputs(rows,hf):
 INDEX_DIR.mkdir(parents=True,exist_ok=True); REPORT_DIR.mkdir(parents=True,exist_ok=True)
 fields=["file_name","path","figure_id","chapter","title","category","theme","status","color_pass","high_fidelity_required","notes"]
 with (INDEX_DIR/"manifest.csv").open("w",encoding="utf-8",newline="") as f:
  w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
  for r in rows+hf: w.writerow({k:r.get(k,"") for k in fields})

 main=f"""# Visual Index

**Status:** Active gallery
**Wave 01 actual SVG assets:** {len(rows)}
**High-fidelity biological/diagnostic assets pending:** {len(hf)}

## Semantic colour legend

- Green — correct / healthy / recommended
- Red — danger / disease / prohibited
- Orange — caution / uncertainty / review
- Blue — neutral process / workflow
- Purple — laboratory / diagnostics / verification
- Honey-gold — honey / wax / natural hive-product context

Colour is never the only carrier of meaning.

## Gallery

- [Wave 01 — Safety & Bee Health](visual-index/wave-01.md)
- [Manifest CSV](visual-index/manifest.csv)
- [High-fidelity queue](../assets/production-briefs/wave-01-high-fidelity.md)

Existing vectors remain final-layout-proof pending.
"""
 (DOCS_DIR/"visual-index.md").write_text(main,encoding="utf-8")

 grouped=defaultdict(list)
 for r in rows: grouped[r["chapter"]].append(r)
 for vals in grouped.values(): vals.sort(key=lambda x:[int(p) for p in x["figure_id"].split(".")])
 lines=["# Wave 01 Visual Gallery","",f"**Actual SVG assets:** {len(rows)}  ",f"**High-fidelity items pending:** {len(hf)}","","Tap an image or Open SVG to inspect it at full vector resolution.",""]
 for ch in sorted(grouped):
  lines += [f"## Chapter {ch} — {CATEGORY.get(ch,('General','operations'))[0]}",""]
  for r in grouped[ch]:
   rel="../../"+r["path"]
   lines += [f"### {r['title']}","",f'<a href="{rel}"><img src="{rel}" alt="{html.escape(r["desc"],quote=True)}" width="520"></a>',"",f"**Figure {r['figure_id']}** · SEMANTIC_COLOR_V1 · [Open SVG]({rel})","",r["desc"],""]
 if hf:
  lines += ["## High-Fidelity Queue","","These items are deliberately not replaced by low-detail schematics.",""]
  for r in sorted(hf,key=lambda x:(x["chapter"],[int(p) for p in x["figure_id"].split(".")])):
   lines.append(f"- **Figure {r['figure_id']} — {r['title']}** — {r['notes']}")
 (INDEX_DIR/"wave-01.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
 (INDEX_DIR/"README.md").write_text("# Visual Index\n\nGenerated from actual repository assets by scripts/apply_visual_color_and_build_index.py.\n",encoding="utf-8")

 counts=defaultdict(int)
 for r in rows: counts[r["chapter"]]+=1
 report=["# Visual Semantic Colour Pass V1 — Review","","**Result:** PASS — conservative semantic colour layer applied without geometry/text changes","",f"- SVG files processed: **{len(rows)}**",f"- high-fidelity assets excluded from automated recolouring: **{len(hf)}**","- all processed SVGs parse as XML and retain title/desc metadata","- final greyscale/final-size/layout proof remains required","","## Coverage by chapter","","| Chapter | Recoloured SVGs |","|---:|---:|"]
 for ch in sorted(counts): report.append(f"| {ch} | {counts[ch]} |")
 report += ["","The pass changes the shared vector colour language only. The high-fidelity brood, disease, mite and anatomy set remains isolated for specialised production.",""]
 (REPORT_DIR/"VISUAL_SEMANTIC_COLOR_PASS_V1.md").write_text("\n".join(report),encoding="utf-8")

def main():
 files=sorted(SVG_DIR.glob("*.svg"))
 if not files: raise SystemExit("No SVG files found")
 before=len(files); rows=[recolor(p) for p in files]
 if len(list(SVG_DIR.glob("*.svg"))) != before: raise RuntimeError("SVG count changed")
 hf=high_fidelity(); make_outputs(rows,hf)
 print(f"Processed {len(rows)} SVGs; high-fidelity queue: {len(hf)}")

if __name__=="__main__": main()
