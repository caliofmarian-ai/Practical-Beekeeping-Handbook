"""Render the five-chapter layout pilot to a PDF and page-preview PNGs.

Dependencies (CI): markdown, weasyprint, pymupdf. The proof is NOT a
publisher-approved print master and does not establish image licensing.
"""
import argparse
import hashlib
import html
import json
import re
from pathlib import Path

import markdown as markdown_package
import pymupdf
from weasyprint import HTML

ROOT = Path(__file__).resolve().parents[1]
PROOFS = ROOT / "exports" / "proofs"
SOURCE = PROOFS / "PBH-wave02-chapters-01-05.md"
FIGURE_MANIFEST = PROOFS / "PBH-wave02-layout-manifest.json"
OUTPUT_PDF = PROOFS / "PBH-wave02-chapters-01-05-PROOF.pdf"
REPORT = PROOFS / "PBH-wave02-pdf-preflight.json"
PREVIEWS = PROOFS / "page-previews"

FIGURE_PATTERN = re.compile(
    r"<!-- PROOF_FIGURE:\s*(?P<id>\d+\.\d+);\s*A_CORE;\s*PAGE_QA_PENDING\s*-->\s*"
    r"!\[(?P<alt>[^\]\n]+)\]\((?P<path>[^)\n]+)\)\s*"
    r"\*Figure (?P<caption_id>\d+\.\d+) — (?P<title>[^\n*]+)\.\*",
    re.MULTILINE,
)

PRINT_STYLES = r"""
@page {
    size: 176mm 250mm;
    margin: 17mm 16mm 19mm 16mm;
    @top-right {
        content: "PRACTICAL BEEKEEPING · LAYOUT PROOF";
        font-family: DejaVu Sans, sans-serif;
        font-size: 7.2pt;
        color: #56606a;
    }
    @bottom-center {
        content: counter(page);
        font-family: DejaVu Sans, sans-serif;
        font-size: 8pt;
        color: #555;
    }
}
@page :first {
    @top-right { content: none; }
}
body {
    font-family: "DejaVu Serif", Georgia, serif;
    color: #202429;
    font-size: 9.7pt;
    line-height: 1.46;
    hyphens: auto;
}
h1, h2, h3, h4, figcaption, th {
    font-family: "DejaVu Sans", Arial, sans-serif;
}
h1 {
    break-before: page;
    color: #193e50;
    font-size: 20pt;
    line-height: 1.18;
    margin: 0 0 9mm;
}
body > h1:first-child { break-before: auto; margin-top: 26mm; }
h2 {
    color: #173c4b;
    font-size: 13pt;
    margin-top: 7mm;
    margin-bottom: 2.5mm;
    break-after: avoid;
}
h3, h4 { color: #394a54; break-after: avoid; }
h3 { font-size: 10.3pt; margin-top: 4mm; }
h4 { font-size: 9.8pt; }
p { margin: 0 0 3.5mm; }
li { margin-bottom: 1mm; }
ol, ul { padding-left: 6mm; }
strong { color: #1e3746; }
blockquote {
    border-left: 2.5px solid #bd8b3c;
    padding: 1mm 0 1mm 4mm;
    margin-left: 0;
    color: #444;
}
figure {
    margin: 5mm 0 6mm;
    padding: 2.5mm;
    border: 0.4pt solid #d5dbdb;
    break-inside: avoid;
    text-align: center;
}
figure img {
    display: block;
    max-width: 100%;
    max-height: 132mm;
    width: auto;
    height: auto;
    margin: 0 auto;
    object-fit: contain;
}
figcaption {
    margin-top: 2.5mm;
    font-size: 8.5pt;
    line-height: 1.33;
    color: #27343d;
    text-align: left;
    break-before: avoid;
}
table {
    border-collapse: collapse;
    font-size: 8.5pt;
    width: 100%;
    margin: 4mm 0;
    break-inside: auto;
}
tr { break-inside: avoid; }
thead { display: table-header-group; }
th, td {
    padding: 2mm;
    border-bottom: 0.4pt solid #bac2c4;
    vertical-align: top;
}
th { background: #eef3f4; font-weight: bold; }
a { color: #17617a; text-decoration: none; overflow-wrap: anywhere; }
hr { border: 0; border-top: 0.4pt solid #ccd2d5; margin: 5mm 0; }
"""


def replace_figure(match):
    figure_id = match.group("id")
    if figure_id != match.group("caption_id"):
        raise ValueError(f"Figure marker/caption mismatch: {figure_id}")
    alt = html.escape(match.group("alt"), quote=True)
    path = html.escape(match.group("path"), quote=True)
    caption = html.escape("Figure " + figure_id + " — " + match.group("title") + ".")
    return (
        '<figure class="core-figure" data-figure-id="' + figure_id + '">'
        '<img src="' + path + '" alt="' + alt + '">'
        "<figcaption>" + caption + "</figcaption></figure>"
    )


def render():
    original_md = SOURCE.read_text(encoding="utf-8")
    manifest = json.loads(FIGURE_MANIFEST.read_text(encoding="utf-8"))
    clean_md, number = FIGURE_PATTERN.subn(replace_figure, original_md)
    if number != manifest["placed_a_core_figures"] or number != 15:
        raise ValueError(f"Expected 15 complete SVG figure blocks, found {number}")

    inside = markdown_package.markdown(
        clean_md, extensions=["tables", "fenced_code", "sane_lists"]
    )
    document = (
        '<!doctype html><html lang="en"><head>'
        '<meta charset="utf-8"><title>PBH Chapters 1–5 — UNREVIEWED PROOF</title>'
        '<style>' + PRINT_STYLES + '</style></head><body>'
        + inside + '</body></html>'
    )
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    pdf_bytes = HTML(
        string=document, base_url=SOURCE.parent.resolve().as_uri() + "/"
    ).write_pdf()
    OUTPUT_PDF.write_bytes(pdf_bytes)

    pdf = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    text_pages = [" ".join(page.get_text("text").split()) for page in pdf]
    if len(pdf) < 10:
        raise ValueError(f"Too few PDF pages for five chapters: {len(pdf)}")
    if sum(len(t) for t in text_pages) < 60000:
        raise ValueError("PDF proof appears to be missing substantial text")
    caption_pages = {}
    missing = []
    for item in manifest["figures"]:
        figure_id = item["figure_id"]
        searched = f"Figure {figure_id}"
        found = [i for i, text in enumerate(text_pages) if searched in text]
        if not found:
            missing.append(figure_id)
        else:
            caption_pages[figure_id] = found[0] + 1
    if missing:
        raise ValueError("Figure captions missing from PDF: " + ", ".join(missing))

    # These are reference thumbnails, not human approval of page layout.
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    selections = {0, min(1, len(pdf) - 1)}
    for figure_id in ("1.2", "2.1", "3.2", "4.1", "5.2"):
        if figure_id in caption_pages:
            selections.add(caption_pages[figure_id] - 1)
    selections.add(len(pdf) - 1)
    images = []
    for page_idx in sorted(selections):
        name = f"proof-page-{page_idx + 1:03d}.png"
        target = PREVIEWS / name
        pix = pdf[page_idx].get_pixmap(matrix=pymupdf.Matrix(1.35, 1.35), alpha=False)
        pix.save(target)
        images.append(str(target.relative_to(ROOT)))

    report = {
        "proof_id": manifest["proof_id"],
        "status": "GENERATED_NOT_VISUALLY_APPROVED",
        "pdf": str(OUTPUT_PDF.relative_to(ROOT)),
        "pdf_sha256": hashlib.sha256(pdf_bytes).hexdigest(),
        "pdf_bytes": len(pdf_bytes),
        "pages": len(pdf),
        "chapters": 5,
        "approved_A_CORE_figure_count": 15,
        "PDF_figure_caption_count": len(caption_pages),
        "figure_caption_pages": caption_pages,
        "preview_pngs": images,
        "pending": [
            "Human page-by-page visual proof for clipping, blank areas, image rendering and legibility",
            "Full-book layout and remaining chapter figures",
            "Rights/attribution and final printing specifications",
            "Index and final PDF/EPUB/print release gates",
        ],
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        f"PROOF GENERATED: pages={len(pdf)}; 15/15 captions present; "
        f"PDF bytes={len(pdf_bytes)}; preview PNGs={len(images)}"
    )
    pdf.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.parse_args()
    render()
