"""Publication gate: every selected V1 real photograph is present, placed and rights-tracked.

This verifies source bytes and chapter/publication references. It does NOT
certify clinical diagnoses, final page legibility or licence compliance in
published print/EPUB/PDF outputs.
"""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
PRIORITY = ROOT / "assets/photo-production-priority.json"
ASSEMBLY_MANIFEST = ROOT / "exports/publication/manifest.json"
PUBLICATION = ROOT / "exports/publication/Practical-Beekeeping-Handbook.md"


def validate():
    photo_manifest = json.loads(PRIORITY.read_text(encoding="utf-8"))
    published_manifest = json.loads(ASSEMBLY_MANIFEST.read_text(encoding="utf-8"))
    published = PUBLICATION.read_text(encoding="utf-8")
    selected = [x for x in photo_manifest["photos"] if x.get("editorial_priority") == "A_CORE"]
    errors = []
    if len(selected) != 36:
        errors.append(f"Expected 36 A_CORE V1 photographs, got {len(selected)}")
    ids = [x["asset_id"] for x in selected]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate selected photo asset_id")
    for photo in selected:
        asset_id = photo["asset_id"]
        path_str = photo.get("repository_source_path")
        if photo.get("production_status") != "SOURCE_FILE_READY":
            errors.append(f"{asset_id}: source is not ready")
        if not photo.get("rights_status", "").startswith("VERIFIED_"):
            errors.append(f"{asset_id}: source licence has not been verified")
        if not path_str:
            errors.append(f"{asset_id}: no repository photo path")
            continue
        target = (ROOT / path_str).resolve()
        if not target.is_relative_to(ROOT.resolve()) or not target.is_file():
            errors.append(f"{asset_id}: repository file missing: {path_str}")
            continue
        actual_sha = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual_sha != photo.get("source_sha256"):
            errors.append(f"{asset_id}: photographic source SHA mismatch: recorded {photo.get('source_sha256')}, actual {actual_sha}")
        if target.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            errors.append(f"{asset_id}: unexpected photo file format")
        chapter = ROOT / "chapters" / f"chapter-{int(photo['chapter']):02d}.md"
        if not chapter.is_file() or f"../{path_str}" not in chapter.read_text(encoding="utf-8"):
            errors.append(f"{asset_id}: authentic photo not embedded in canonical Chapter {photo['chapter']}")
        if f"../../{path_str}" not in published:
            errors.append(f"{asset_id}: compiled edition missing correct rebased path")

    if published_manifest.get("local_images_verified_count") != 36:
        errors.append("Assembled reader edition does not verify exactly 36 local images")
    if photo_manifest["current_v1_status"].get("source_file_ready_and_chapter_placed_count") != 36:
        errors.append("Photo priority status is not reconciled to 36 chapter placements")
    if photo_manifest["current_v1_status"].get("remaining_count") != 0:
        errors.append("Photo priority still reports missing A_CORE assets")
    if errors:
        print("FAIL: photographic preflight\n" + "\n".join(" - " + e for e in errors), file=sys.stderr)
        raise SystemExit(1)
    print("PASS: all 36/36 real V1 A_CORE source files, checksums, rights flags, chapter embeds and compiled links verified.")
    print("NOTE: page proof, accessibility, output-format attributions and print licensing remain separate gates.")


if __name__ == "__main__":
    validate()
