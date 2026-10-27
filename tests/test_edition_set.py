"""Synthetic fixtures: structural tests are not editorial approval of the book."""
import copy
import hashlib
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from build_edition_set import (  # noqa: E402
    REFERENCE_SOURCES, REQUIRED_GATES, ReleaseBlocked, build, make_outputs,
    numbers, require_release, structure_metrics, validate_plan,
)


class EditionSetTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.plan = json.loads((REPO / "docs/production/edition-plan.json").read_text())
        self.put("docs/production/edition-plan.json", json.dumps(self.plan))
        self.put("docs/BOOK_OUTLINE.md", "\n".join(f"{n}. Topic {n}" for n in range(1, 86)))
        photos = []
        for n in range(1, 75):
            text = (f"# Chapter {n} — Topic {n}\n\n## Explanation\n"
                    "A continuous explanatory paragraph is preserved here.\n\n"
                    "## Review Notes\nInternal planning only.\n\n"
                    "## Practical guidance\nThis is retained in every edition.\n")
            if n <= 36:
                path = f"assets/photos/photo-{n:02d}.jpg"
                data = f"synthetic photo {n}".encode()
                self.put(path, data)
                text += f"\n![Photo {n}](../{path})\n"
                photos.append({"asset_id": f"P{n:02d}.01", "chapter": n,
                               "editorial_priority": "A_CORE", "repository_source_path": path,
                               "source_sha256": hashlib.sha256(data).hexdigest()})
            self.put(f"chapters/chapter-{n:02d}.md", text)
            self.put(f"docs/illustration-plans/chapter-{n:02d}-illustration-plan.md", "# Plan\n")
        for n, title, path in REFERENCE_SOURCES:
            self.put(path, f"# Reference {n} — {title}\n\nReference text retained.\n")
        figures = []
        for n in range(1, 231):
            path = f"assets/diagrams/figure-{n:03d}.svg"
            self.put(path, '<svg xmlns="http://www.w3.org/2000/svg"></svg>')
            figures.append({"asset_id": f"F{n}", "chapter": (n - 1) % 74 + 1,
                            "editorial_priority": "A_CORE", "production_status": "APPROVED",
                            "final_asset_path": path})
        self.put("assets/visual-production-priority.json", json.dumps({"figures": figures}))
        self.put("assets/photo-production-priority.json", json.dumps({"photos": photos}))

    def put(self, path, value):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(value if isinstance(value, bytes) else value.encode("utf-8"))

    def test_complete_coverage_and_image_accounting(self):
        _, inventory, outputs = make_outputs(self.root)
        digital, *volumes = inventory["editions"]
        self.assertEqual(digital["chapters"], list(range(1, 75)))
        self.assertEqual(digital["references"], list(range(75, 86)))
        self.assertEqual([n for v in volumes for n in v["chapters"]], list(range(1, 75)))
        self.assertEqual([n for v in volumes for n in v["references"]], list(range(75, 86)))
        self.assertEqual(sum(v["a_core_figures"] for v in volumes), 230)
        self.assertEqual(sum(v["a_core_photos"] for v in volumes), 36)
        self.assertEqual(sum(v["local_image_links_verified"] for v in volumes), 36)
        self.assertEqual(digital["local_image_links_verified"], 36)
        self.assertEqual(len(outputs), 8)
        self.assertEqual(len(inventory["chapters"]), 74)

    def test_source_files_unchanged_and_notes_not_printed(self):
        chapter = self.root / "chapters/chapter-01.md"
        before = chapter.read_bytes()
        build(self.root)
        build(self.root, check=True)
        self.assertEqual(chapter.read_bytes(), before)
        assembled = (self.root / "exports/editions/volume-01.md").read_text()
        self.assertNotIn("Internal planning only", assembled)
        self.assertIn("This is retained in every edition", assembled)
        self.assertIn("../../assets/photos/photo-01.jpg", assembled)

    def test_stale_output_detected(self):
        build(self.root)
        self.put("exports/editions/volume-03.md", "stale")
        with self.assertRaisesRegex(ValueError, "stale edition"):
            build(self.root, check=True)

    def test_required_sources_missing(self):
        for relative in ("chapters/chapter-74.md",
                         "docs/illustration-plans/chapter-01-illustration-plan.md",
                         "glossary/glossary.md", "assets/diagrams/figure-001.svg"):
            with self.subTest(relative=relative):
                target = self.root / relative
                saved = target.read_bytes()
                target.unlink()
                with self.assertRaisesRegex(ValueError, "Missing or unsafe"):
                    make_outputs(self.root)
                target.write_bytes(saved)

    def test_photo_bytes_cannot_silently_change(self):
        self.put("assets/photos/photo-01.jpg", b"changed")
        with self.assertRaisesRegex(ValueError, "checksum mismatch"):
            make_outputs(self.root)

    def test_missing_link_fails(self):
        self.put("chapters/chapter-74.md", "# Chapter 74 — Topic 74\n![Missing](../assets/missing.jpg)\n")
        with self.assertRaisesRegex(ValueError, "Missing local link"):
            make_outputs(self.root)

    def test_chapter_omissions_overlaps_and_order_rejected(self):
        for limits in ([25, 38], [23, 38], [38, 24]):
            with self.subTest(limits=limits):
                plan = copy.deepcopy(self.plan)
                plan["print_volumes"][1]["chapter_range"] = limits
                with self.assertRaises(ValueError):
                    validate_plan(plan)

    def test_reference_loss_or_duplication_rejected(self):
        for target, limits in ((4, [76, 85]), (0, [75, 85])):
            plan = copy.deepcopy(self.plan)
            plan["print_volumes"][target]["reference_range"] = limits
            with self.assertRaises(ValueError):
                validate_plan(plan)

    def test_incomplete_digital_book_rejected(self):
        plan = copy.deepcopy(self.plan)
        plan["digital"]["chapter_range"] = [1, 73]
        with self.assertRaises(ValueError):
            validate_plan(plan)

    def test_duplicate_or_unsafe_output_ids_rejected(self):
        for identifier in ("volume-02", "../../outside"):
            plan = copy.deepcopy(self.plan)
            plan["print_volumes"][0]["id"] = identifier
            with self.assertRaises(ValueError):
                validate_plan(plan)

    def test_bad_ranges_rejected(self):
        for value in ([], [1], [3, 1], [True, 2], [1.0, 2], "1-2"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                numbers(value)

    def test_mandatory_gates_cannot_be_removed(self):
        plan = copy.deepcopy(self.plan)
        plan["release_gates"].pop()
        with self.assertRaisesRegex(ValueError, "Mandatory release gates"):
            require_release(plan, "fingerprint")

    def test_approval_of_format_does_not_approve_text(self):
        self.assertEqual(self.plan["format_direction_status"], "OWNER_APPROVED")
        with self.assertRaisesRegex(ReleaseBlocked, "narrative_review"):
            require_release(self.plan, "fingerprint")

    def test_approval_requires_current_source_evidence(self):
        for evidence, fingerprint in ((None, "current"), ("test evidence", "stale")):
            plan = copy.deepcopy(self.plan)
            for gate in plan["release_gates"]:
                gate.update(state="APPROVED", evidence=evidence,
                            approved_source_fingerprint=fingerprint)
            with self.assertRaises(ReleaseBlocked):
                require_release(plan, "current")

    def test_future_matching_evidence_can_pass(self):
        plan = copy.deepcopy(self.plan)
        for gate in plan["release_gates"]:
            gate.update(state="APPROVED", evidence="synthetic-test-only",
                        approved_source_fingerprint="current")
        require_release(plan, "current")

    def test_metrics_do_not_treat_questions_as_prose_failure(self):
        text = ("## Explanation\nA paragraph that explains a topic.\n\n- Useful item\n"
                "## Review Questions\n1. A question\n2. Another question\n"
                "## References\n- Bibliography item\n")
        metrics = structure_metrics(text)
        self.assertEqual(metrics["body_bullet_lines"], 1)
        self.assertEqual(metrics["body_numbered_lines"], 0)
        self.assertIn("PENDING", metrics["human_narrative_review"])

    def test_source_changes_invalidate_fingerprint(self):
        _, first, _ = make_outputs(self.root)
        path = self.root / "chapters/chapter-01.md"
        path.write_text(path.read_text() + "\nAdditional source text.\n")
        _, second, _ = make_outputs(self.root)
        self.assertNotEqual(first["source_fingerprint"], second["source_fingerprint"])

    def test_navigation_resolves_to_generated_editions(self):
        _, _, outputs = make_outputs(self.root)
        for name, text in outputs.items():
            if not name.endswith(".md") or name == "EDITION_READINESS.md":
                continue
            targets = re.findall(r"\]\(((?:volume-\d+|digital-complete)\.md)\)", text)
            self.assertEqual(len(targets), 6)
            self.assertTrue(all(target in outputs for target in targets))


if __name__ == "__main__":
    unittest.main()
