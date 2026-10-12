"""Tests for publication path safety and exclusion of internal manuscript notes."""
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from publication_preflight import (  # noqa: E402
    without_editorial_sections,
    rebase_local_links,
    validate_publication_images,
)


class PublicationPreflightTests(unittest.TestCase):
    def test_strip_editorial_sections_only_in_reader_output(self):
        original = (
            "# Chapter 1 — Test\n\n"
            "## Introduction\nKeep me.\n"
            "## Figure Placeholders\nDo not print placeholder list.\n"
            "### Nested Editor Note\nInvisible.\n"
            "## Practical Advice\nKeep practical text.\n"
            "## Review Notes\nInternal issue tracking only.\n"
        )
        result, omitted = without_editorial_sections(original)
        self.assertEqual(omitted, ["Figure Placeholders", "Review Notes"])
        self.assertIn("Keep me.", result)
        self.assertIn("Keep practical text.", result)
        self.assertNotIn("Invisible.", result)
        self.assertNotIn("Internal issue tracking", result)
        self.assertIn("Internal issue tracking", original)

    def test_image_path_rebased_and_readable(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            chapter = root / "chapters" / "chapter-01.md"
            image = root / "assets" / "photos" / "example.jpg"
            export_dir = root / "exports" / "publication"
            chapter.parent.mkdir(parents=True)
            image.parent.mkdir(parents=True)
            export_dir.mkdir(parents=True)
            image.write_bytes(b"example")
            text = "![Field context](../assets/photos/example.jpg)"
            result, links, images = rebase_local_links(text, chapter, root, export_dir)
            self.assertEqual(result, "![Field context](../../assets/photos/example.jpg)")
            self.assertEqual((links, images), (1, 1))
            self.assertEqual(validate_publication_images(result, root, export_dir), 1)

    def test_inline_figure_placeholders_and_drafting_handoff_are_hidden(self):
        original = (
            "# Chapter 11 — Communication\n\n"
            "## Recruitment Communication\n"
            "Useful reader text.\n\n"
            "[Figure placeholder: raw diagram briefing for production]\n\n"
            "Part 2 will continue with later topics, review questions, and references.\n\n"
            "## Real Content\nThis content must remain.\n"
        )
        proof, excluded = without_editorial_sections(original)
        self.assertEqual(
            excluded, ["Inline figure placeholder", "Draft continuation handoff"]
        )
        self.assertNotIn("[Figure placeholder:", proof)
        self.assertNotIn("Part 2 will continue", proof)
        self.assertIn("Useful reader text.", proof)
        self.assertIn("This content must remain.", proof)
        self.assertIn("[Figure placeholder:", original)

    def test_missing_assets_raise_instead_of_silent_broken_links(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "chapters").mkdir()
            (root / "exports" / "publication").mkdir(parents=True)
            with self.assertRaisesRegex(ValueError, "Missing local link target"):
                rebase_local_links(
                    "![Missing](../assets/photos/missing.jpg)",
                    root / "chapters" / "chapter-01.md",
                    root,
                    root / "exports" / "publication",
                )

    def test_links_cannot_escape_repo(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "chapters").mkdir()
            (root / "exports" / "publication").mkdir(parents=True)
            with self.assertRaisesRegex(ValueError, "escapes repository"):
                rebase_local_links(
                    "![Unsafe](../../outside.jpg)",
                    root / "chapters" / "chapter-01.md",
                    root,
                    root / "exports" / "publication",
                )

    def test_external_anchor_and_code_examples_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "chapters").mkdir()
            (root / "exports" / "publication").mkdir(parents=True)
            example = (
                "![external](https://example.org/bee.jpg)\n"
                "[jump](#figure)\n"
                "![link](mailto:someone@example.org)\n"
                "~~~md\n"
                "![not-an-asset](../assets/no-file.png)\n"
                "~~~\n"
            )
            result, links, images = rebase_local_links(
                example, root / "chapters" / "chapter-01.md", root, root / "exports" / "publication"
            )
            self.assertEqual(result, example)
            self.assertEqual((links, images), (0, 0))
            self.assertEqual(validate_publication_images(result, root, root / "exports" / "publication"), 0)


if __name__ == "__main__":
    unittest.main()
