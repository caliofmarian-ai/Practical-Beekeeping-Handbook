"""Assemble one digital book and five print proof sources; never approve publication.

Standard-library-only. Canonical chapters, reference files and artwork are read,
not edited. Structural metrics are descriptive, NOT a prose-quality score.
"""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from build_publication_manuscript import REFERENCE_SOURCES, normalise_chapter_heading
from publication_preflight import (
    without_editorial_sections, rebase_local_links, validate_publication_images,
)

ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = "docs/production/edition-plan.json"
OUT_PATH = "exports/editions"
REQUIRED_GATES = {
    "narrative_review", "owner_prose_sample", "scientific_review_after_rewrite",
    "visual_page_proof", "pagination_index_navigation", "rights_cover_imprint",
    "digital_format_proof", "print_size_and_format_proof",
}
WORDS = re.compile(r"\b\w+(?:['\u2019-]\w+)*\b")


class ReleaseBlocked(ValueError):
    """Expected refusal to label incomplete material a release."""


def digest(data):
    return hashlib.sha256(data).hexdigest()


def numbers(value):
    if value is None:
        return []
    if (not isinstance(value, list) or len(value) != 2
            or any(type(n) is not int for n in value) or value[0] > value[1]):
        raise ValueError(f"Invalid inclusive range: {value!r}")
    return list(range(value[0], value[1] + 1))


def validate_plan(plan):
    if plan.get("schema_version") != "1.0":
        raise ValueError("Unsupported edition-plan schema")
    digital = plan["digital"]
    if numbers(digital["chapter_range"]) != list(range(1, 75)):
        raise ValueError("Digital edition must retain all 74 chapters in order")
    if numbers(digital["reference_range"]) != list(range(75, 86)):
        raise ValueError("Digital edition must retain References 75–85")
    volumes = plan["print_volumes"]
    if len(volumes) != 5 or [v["number"] for v in volumes] != list(range(1, 6)):
        raise ValueError("Working architecture requires five ordered volumes")
    ids = [digital["id"]] + [v["id"] for v in volumes]
    if len(set(ids)) != 6 or any(not re.fullmatch(r"[a-z0-9-]+", x) for x in ids):
        raise ValueError("Edition IDs must be unique safe slugs")
    chapters = [n for v in volumes for n in numbers(v["chapter_range"])]
    references = [n for v in volumes for n in numbers(v["reference_range"])]
    if chapters != list(range(1, 75)):
        raise ValueError("Print chapters are omitted, duplicated or reordered")
    if references != list(range(75, 86)):
        raise ValueError("Print references are omitted, duplicated or reordered")
    homes = [v["id"] for v in volumes if numbers(v["reference_range"])]
    if homes != [plan["reference_policy"]["complete_reference_home"]]:
        raise ValueError("Reference-home policy disagrees with volume allocation")
    expected = {"chapters": 74, "references": 11, "a_core_figures": 230,
                "a_core_photographs": 36}
    if plan["resource_expectations"] != expected:
        raise ValueError("Resource baseline changed: reconcile explicitly")
    gates = plan["release_gates"]
    if len(gates) != len(REQUIRED_GATES) or {g["id"] for g in gates} != REQUIRED_GATES:
        raise ValueError("Mandatory release gates are missing or duplicated")


def release_blockers(plan, fingerprint):
    validate_plan(plan)
    return [g["id"] for g in plan["release_gates"]
            if g.get("state") != "APPROVED" or not g.get("evidence")
            or g.get("approved_source_fingerprint") != fingerprint]


def require_release(plan, fingerprint):
    blocked = release_blockers(plan, fingerprint)
    if blocked:
        raise ReleaseBlocked("RELEASE BLOCKED: " + ", ".join(blocked))


def structure_metrics(text):
    """Count reader-body structure, excluding review questions and bibliography.

    Forty-word paragraph counts are a descriptive bucket, not an acceptance
    criterion. No ratio, word minimum or list count grants editorial approval.
    """
    body = []
    skip = False
    fenced = False
    for line in text.splitlines():
        if re.match(r"^\s*(?:\x60{3,}|~{3,})", line):
            fenced = not fenced
            continue
        if fenced:
            continue
        h2 = re.match(r"^##\s+(.+)$", line)
        if h2:
            skip = h2.group(1).strip().casefold() in {
                "review questions", "knowledge check", "references",
                "references and further reading", "learning objectives",
            }
        if not skip:
            body.append(line)
    bullets = sum(bool(re.match(r"^\s*[-+*]\s+", x)) for x in body)
    numbered = sum(bool(re.match(r"^\s*\d+[.)]\s+", x)) for x in body)
    paragraphs, current = [], []
    for line in body + [""]:
        structural = (not line.strip() or re.match(r"^\s*(?:#{1,6}\s|[-+*]\s|\d+[.)]\s|\||!\[|<!--|---)", line))
        if structural:
            if current:
                paragraphs.append(" ".join(current))
                current = []
        else:
            current.append(line.strip())
    lengths = [len(WORDS.findall(p)) for p in paragraphs]
    return {
        "reader_word_tokens": len(WORDS.findall(text)),
        "body_bullet_lines": bullets, "body_numbered_lines": numbered,
        "prose_paragraphs": len(lengths),
        "paragraphs_at_least_40_tokens": sum(n >= 40 for n in lengths),
        "human_narrative_review": "PENDING_ISSUE_228_NOT_AUTOMATICALLY_SCORED",
    }


def read_required(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError(f"Missing or unsafe required source: {relative}")
    return path, path.read_bytes()


def make_outputs(root=ROOT):
    root = Path(root).resolve()
    out_dir = root / OUT_PATH
    plan = json.loads((root / PLAN_PATH).read_text(encoding="utf-8"))
    validate_plan(plan)
    source_hashes = {}

    def read(relative):
        path, data = read_required(root, relative)
        source_hashes[relative] = digest(data)
        return path, data.decode("utf-8")

    _, outline = read(plan["canonical_outline"])
    if [int(n) for n in re.findall(r"^(\d+)\.\s+", outline, re.M)] != list(range(1, 86)):
        raise ValueError("Canonical outline no longer contains positions 1–85 exactly once")
    chapters, rows = {}, []
    chapter_volume = {n: v["id"] for v in plan["print_volumes"] for n in numbers(v["chapter_range"])}
    for n in range(1, 75):
        relative = f"chapters/chapter-{n:02d}.md"
        path, raw = read(relative)
        read(f"docs/illustration-plans/chapter-{n:02d}-illustration-plan.md")
        clean, omitted = without_editorial_sections(normalise_chapter_heading(raw, n))
        chapters[n] = (path, clean)
        rows.append({"chapter": n, "volume": chapter_volume[n], "source": relative,
                     "source_sha256": source_hashes[relative],
                     "title": clean.splitlines()[0].removeprefix("# "),
                     "editorial_blocks_excluded": len(omitted), **structure_metrics(clean)})
    references = {}
    for n, title, relative in REFERENCE_SOURCES:
        path, raw = read(relative)
        clean, _ = without_editorial_sections(raw)
        lines = clean.splitlines()
        if lines and lines[0].startswith("# "):
            lines[0] = "## " + lines[0][2:]
        references[n] = (path, f"# Reference {n} — {title}\n\n" + "\n".join(lines) + "\n")

    _, figure_json = read("assets/visual-production-priority.json")
    _, photo_json = read("assets/photo-production-priority.json")
    figures = [a for a in json.loads(figure_json)["figures"] if a.get("editorial_priority") == "A_CORE"]
    photos = [a for a in json.loads(photo_json)["photos"] if a.get("editorial_priority") == "A_CORE"]
    for assets, expected, field in [(figures, 230, "final_asset_path"), (photos, 36, "repository_source_path")]:
        if len(assets) != expected or len({a["asset_id"] for a in assets}) != expected:
            raise ValueError(f"Selected asset count/identity mismatch: {field}")
        for asset in assets:
            if asset["chapter"] not in chapters:
                raise ValueError(f"Asset assigned to unknown chapter: {asset['asset_id']}")
            path, data = read_required(root, asset[field])
            source_hashes[asset[field]] = digest(data)
            if field == "final_asset_path" and asset.get("production_status") != "APPROVED":
                raise ValueError(f"Selected diagram not asset-approved: {asset['asset_id']}")
            if field == "repository_source_path":
                if digest(data) != asset.get("source_sha256"):
                    raise ValueError(f"Photo source checksum mismatch: {asset['asset_id']}")
                if asset[field] not in chapters[asset["chapter"]][1]:
                    raise ValueError(f"Selected photo is not linked in its chapter: {asset['asset_id']}")
    figure_counts = Counter(a["chapter"] for a in figures)
    photo_counts = Counter(a["chapter"] for a in photos)
    for row in rows:
        row.update(a_core_figures=figure_counts[row["chapter"]],
                   a_core_photos=photo_counts[row["chapter"]])

    layout_inputs = {k: v for k, v in plan.items() if k != "release_gates"}
    fingerprint = digest(json.dumps({"plan": layout_inputs, "sources": source_hashes},
                                    sort_keys=True, ensure_ascii=False).encode("utf-8"))
    blockers = release_blockers(plan, fingerprint)
    navigation = ["## Set navigation", "", "| Edition | Chapters |", "|---|---|"]
    editions = [plan["digital"]] + plan["print_volumes"]
    for edition in editions:
        first, last = edition["chapter_range"]
        navigation.append(f"| [{edition['title']}]({edition['id']}.md) | {first}–{last} |")
    navigation.append("\nComplete References 75–85 are in Volume 5 and the complete digital edition. Chapter bibliographies and warnings remain within their chapters.\n")
    outputs, summaries = {}, []
    for edition in editions:
        content = [f"# {plan['book_title']}\n", f"**{edition['title']}**\n",
                   "**WORKING MANUSCRIPT — NOT A RELEASE OR A PRINT MASTER.**\n",
                   "Narrative revision (#228), image placement, pagination and format proof remain pending. Chapter numbers are global and unchanged. No final page count is claimed.\n",
                   "\n".join(navigation)]
        included = numbers(edition["chapter_range"])
        refs = numbers(edition["reference_range"])
        for n, (path, text) in [(n, chapters[n]) for n in included] + [(n, references[n]) for n in refs]:
            text, _, _ = rebase_local_links(text, path, root, out_dir)
            kind = "chapter" if n <= 74 else "reference"
            content += [f'\n<a id="{kind}-{n:02d}"></a>\n', text]
        markdown = "\n".join(content).rstrip() + "\n"
        if [int(n) for n in re.findall(r"^# Chapter (\d+) — ", markdown, re.M)] != included:
            raise ValueError(f"Chapter coverage mismatch in {edition['id']}")
        if [int(n) for n in re.findall(r"^# Reference (\d+) — ", markdown, re.M)] != refs:
            raise ValueError(f"Reference coverage mismatch in {edition['id']}")
        image_count = validate_publication_images(markdown, root, out_dir)
        name = edition["id"] + ".md"
        outputs[name] = markdown
        summaries.append({"id": edition["id"], "title": edition["title"],
                          "chapters": included, "references": refs,
                          "generated_sha256": digest(markdown.encode("utf-8")),
                          "local_image_links_verified": image_count,
                          "reader_word_tokens": sum(r["reader_word_tokens"] for r in rows if r["chapter"] in included),
                          "a_core_figures": sum(figure_counts[n] for n in included),
                          "a_core_photos": sum(photo_counts[n] for n in included)})
    inventory = {"schema_version": "1.0", "status": "PROOF_SOURCES_ONLY",
                 "source_fingerprint": fingerprint, "source_hashes": source_hashes,
                 "format_direction_status": plan["format_direction_status"],
                 "grouping_status": plan["grouping_status"],
                 "release_blockers": blockers, "chapters": rows, "editions": summaries,
                 "metrics_caveat": "Approximate Markdown word tokens and structural counts are not page counts or editorial sign-off. Questions, bibliography and learning objectives are excluded from body list/paragraph counts."}
    outputs["edition-inventory.json"] = json.dumps(inventory, indent=2, ensure_ascii=False) + "\n"
    report = ["# Edition architecture and editorial readiness", "",
              "**Proof sources only. Not a publication approval.**", "",
              "The owner approved a complete digital book plus a multi-volume print edition. The five-volume grouping is provisional until revised prose and physical-size proof are reviewed.", "",
              "| Print volume | Chapters | Approx. chapter word tokens | Core figures | Core photographs |",
              "|---|---:|---:|---:|---:|"]
    for row in summaries[1:]:
        report.append(f"| {row['title']} | {row['chapters'][0]}–{row['chapters'][-1]} | {row['reader_word_tokens']:,} | {row['a_core_figures']} | {row['a_core_photos']} |")
    report += ["", "All 74 chapters occur exactly once across the print set. References 75–85 occur in Volume 5 and in the complete digital edition. Chapter references and safety text are retained.", "",
               "Selected figures are counted as source assets, not as final placed/approved pages. Existing photographs are rebased and validated in the generated sources.", "",
               "## Publication holds", "", ", ".join(blockers) or "No pending manifest gates; independent release authorisation still required.", "",
               "Issue #228 and draft PR #229 must not be closed by format approval. All chapter-level narrative-review statuses remain pending. Revise and review text before freezing pagination, index or binding specifications.", "",
               "## Chapter inventory", "", "The following structural counts guide inspection only. Lists may be appropriate in checklists; counts cannot determine quality. No chapter is automatically approved.", "",
               "| Chapter | Volume | Word tokens | Body bullet lines | Body numbered lines | Prose paragraphs | Paragraphs with 40+ tokens |",
               "|---:|---|---:|---:|---:|---:|---:|"]
    for row in rows:
        report.append(f"| {row['chapter']} | {row['volume']} | {row['reader_word_tokens']} | {row['body_bullet_lines']} | {row['body_numbered_lines']} | {row['prose_paragraphs']} | {row['paragraphs_at_least_40_tokens']} |")
    report += ["", f"Source fingerprint: `{fingerprint}`", "",
               "Rebuild with `python scripts/build_edition_set.py`; verify with `--check`. `--release-check` exits 2 while gates are pending or approval evidence is stale."]
    outputs["EDITION_READINESS.md"] = "\n".join(report) + "\n"
    return plan, inventory, outputs


def build(root=ROOT, check=False, release_check=False):
    plan, inventory, outputs = make_outputs(root)
    if release_check:
        require_release(plan, inventory["source_fingerprint"])
        return inventory
    destination = Path(root) / OUT_PATH
    for name, content in outputs.items():
        path = destination / name
        if check:
            if not path.is_file() or path.read_text(encoding="utf-8") != content:
                raise ValueError(f"Missing/stale edition output: {path}")
        else:
            destination.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    print("PASS: complete digital source, five print sources, 74 chapters, 11 references")
    print("Source assets verified: 230 core figures and 36 core photographs")
    print("Publication holds: " + ", ".join(inventory["release_blockers"]))
    return inventory


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--release-check", action="store_true")
    args = parser.parse_args()
    try:
        build(check=args.check, release_check=args.release_check)
    except ReleaseBlocked as exc:
        parser.exit(2, str(exc) + "\n")
