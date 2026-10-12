"""Build a Chapter 1–5 figure-placement proof from canonical manuscript sources.

Not a final PDF, EPUB, or print edition. All original chapter files remain
unchanged; explicit anchors and approved A_CORE assets make placement auditable.
"""
import argparse
import hashlib
import json
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from build_publication_manuscript import normalise_chapter_heading
from publication_preflight import (
    rebase_local_links, validate_publication_images, without_editorial_sections
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "exports" / "proofs"
OUTPUT_MD = OUTPUT_DIR / "PBH-wave02-chapters-01-05.md"
OUTPUT_MANIFEST = OUTPUT_DIR / "PBH-wave02-layout-manifest.json"
PLACEMENT_PATH = ROOT / "docs" / "layout" / "figure-placements-wave02-ch01-05.json"
PRIORITY_PATH = ROOT / "assets" / "visual-production-priority.json"


def sha256(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def insert_figures_at_headings(markdown: str, additions: dict):
    """Insert pre-approved figure blocks after exact, unique Markdown headings."""
    occurrences = {heading: 0 for heading in additions}
    lines = []
    for line in markdown.splitlines(keepends=True):
        lines.append(line)
        heading = line.strip()
        if heading in additions:
            occurrences[heading] += 1
            if occurrences[heading] == 1:
                lines.append("\n" + "\n\n".join(additions[heading]) + "\n\n")
    invalid = {k: v for k, v in occurrences.items() if v != 1}
    if invalid:
        raise ValueError(f"Section anchors not found exactly once: {invalid}")
    return "".join(lines)


def approved_figure_map():
    registry = json.loads(PRIORITY_PATH.read_text(encoding="utf-8"))
    selected = registry["figures"]
    valid = {}
    for item in selected:
        if item.get("editorial_priority") != "A_CORE":
            continue
        figure_id = item["figure_id"]
        if figure_id in valid:
            raise ValueError(f"Duplicate A_CORE figure identifier: {figure_id}")
        valid[figure_id] = item
    if len(valid) != 230:
        raise ValueError(f"A_CORE registry changed: expected 230, got {len(valid)}")
    return valid


def produce(check: bool = False):
    placements = json.loads(PLACEMENT_PATH.read_text(encoding="utf-8"))
    figure_map = approved_figure_map()
    expected_chapters = [1, 2, 3, 4, 5]
    if placements["chapters"] != expected_chapters:
        raise ValueError("Pilot must cover exactly Chapters 1–5")
    plans = placements["placements"]
    if len(plans) != placements["expected_a_core_figures"] or len(plans) != 15:
        raise ValueError("The pilot placement manifest must contain 15 figures")

    expected_ids = {
        identifier for identifier, figure in figure_map.items()
        if figure["chapter"] in expected_chapters
    }
    actual_ids = [entry["figure_id"] for entry in plans]
    if len(set(actual_ids)) != len(actual_ids) or set(actual_ids) != expected_ids:
        raise ValueError("Pilot placements do not match the selected A_CORE set")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pages = [
        "# Practical Beekeeping Handbook\n",
        "**Layout proof — Chapters 1–5, selected A_CORE figures**\n",
        "**NOT FOR RELEASE — final placement, print legibility and legal proof pending**\n"
    ]
    manifest = {
        "schema_version": "1.0",
        "proof_id": placements["proof_id"],
        "status": "UNREVIEWED_PAGE_CONTEXT_PROOF",
        "source_placement_sha256": sha256(PLACEMENT_PATH),
        "source_visual_registry_sha256": sha256(PRIORITY_PATH),
        "chapters": [],
        "figures": [],
    }
    total_rebased = 0
    total_existing_images = 0

    for chapter_number in expected_chapters:
        source = ROOT / "chapters" / f"chapter-{chapter_number:02d}.md"
        body = normalise_chapter_heading(source.read_text(encoding="utf-8"), chapter_number)
        body, omitted = without_editorial_sections(body)
        body, rebased, existing_images = rebase_local_links(body, source, ROOT, OUTPUT_DIR)
        total_rebased += rebased
        total_existing_images += existing_images
        additions = {}

        for placement in plans:
            fid = placement["figure_id"]
            fig = figure_map[fid]
            if fig["chapter"] != chapter_number:
                continue
            path = ROOT / fig["final_asset_path"]
            if fig.get("production_status") != "APPROVED":
                raise ValueError(f"Figure {fid} is not approved")
            if fig.get("rights_status") != "ORIGINAL_FOR_HANDBOOK":
                raise ValueError(f"Rights status not cleared for figure {fid}")
            if fig.get("accuracy_status") != "PBH_V1_TECHNICAL_REVIEW_PASS":
                raise ValueError(f"Technical gate not passed for figure {fid}")
            if fig.get("accessibility_status") != "SVG_ACCESSIBILITY_GREYSCALE_PROOF_PASS":
                raise ValueError(f"Accessibility gate not passed for figure {fid}")
            if not path.is_file() or path.suffix.lower() != ".svg":
                raise ValueError(f"Missing actual SVG for {fid}: {path}")
            ET.parse(path)  # fails on malformed SVG source

            title = fig["working_title"]
            alt = re.sub(r"\s+", " ", fig["brief"]).replace("[", "(").replace("]", ")")
            relative = os.path.relpath(path, OUTPUT_DIR).replace(os.sep, "/")
            snippet = (
                f"<!-- PROOF_FIGURE: {fid}; A_CORE; PAGE_QA_PENDING -->\n"
                f"![{alt}]({relative})\n\n"
                f"*Figure {fid} — {title}.*"
            )
            heading = placement["after_heading"]
            additions.setdefault(heading, []).append(snippet)
            manifest["figures"].append({
                "figure_id": fid, "chapter": chapter_number,
                "title": title, "anchor": heading, "asset": fig["final_asset_path"],
                "asset_sha256": sha256(path), "alt_text": alt,
                "caption": f"Figure {fid} — {title}.",
                "placement_status": "IN_PROOF_NOT_PAGE_APPROVED",
            })

        body = insert_figures_at_headings(body, additions)
        pages.append("\n<!-- PAGEBREAK: CHAPTER -->\n")
        pages.append(body)
        manifest["chapters"].append({
            "number": chapter_number,
            "source": str(source.relative_to(ROOT)),
            "source_sha256": sha256(source),
            "editorial_blocks_removed": omitted,
            "selected_figure_count": sum(1 for e in manifest["figures"] if e["chapter"] == chapter_number),
        })

    markdown = "\n".join(pages).rstrip() + "\n"
    if len(re.findall(r"^# Chapter \d+ — ", markdown, re.M)) != 5:
        raise ValueError("Five canonical chapters were not assembled")
    if len(re.findall(r"<!-- PROOF_FIGURE:", markdown)) != 15:
        raise ValueError("Expected exactly 15 inserted figure markers")
    actual_image_count = validate_publication_images(markdown, ROOT, OUTPUT_DIR)
    if actual_image_count != 15 + total_existing_images:
        raise ValueError("Source photos or inserted figure files are missing")

    manifest["chapter_count"] = len(expected_chapters)
    manifest["placed_a_core_figures"] = len(manifest["figures"])
    manifest["images_verified_count"] = actual_image_count
    manifest["source_local_links_rebased"] = total_rebased
    manifest["generated_file"] = str(OUTPUT_MD.relative_to(ROOT))
    manifest["generated_sha256"] = hashlib.sha256(markdown.encode("utf-8")).hexdigest()
    manifest_text = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"

    if check:
        if not OUTPUT_MD.is_file() or not OUTPUT_MANIFEST.is_file():
            raise SystemExit("Layout proof missing; run without --check")
        if OUTPUT_MD.read_text(encoding="utf-8") != markdown:
            raise SystemExit("Layout proof Markdown is stale")
        if OUTPUT_MANIFEST.read_text(encoding="utf-8") != manifest_text:
            raise SystemExit("Layout proof manifest is stale")
    else:
        OUTPUT_MD.write_text(markdown, encoding="utf-8")
        OUTPUT_MANIFEST.write_text(manifest_text, encoding="utf-8")

    print(f"{'Verified' if check else 'Built'} {OUTPUT_MD.relative_to(ROOT)}")
    print(f"Chapters: {manifest['chapter_count']} | A_CORE figures: {len(manifest['figures'])}")
    print(f"Images verified: {actual_image_count} | Editorial sections excluded from proof")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build 15-figure first-five-chapters proof")
    parser.add_argument("--check", action="store_true")
    produce(check=parser.parse_args().check)
