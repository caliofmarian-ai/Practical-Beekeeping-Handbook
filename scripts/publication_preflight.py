"""Preflight for the reader-facing assembled Markdown edition.

The 74 chapter files and illustration plans remain the editable source of truth.
This module is intentionally standard-library-only and does not approve final art
or substitute an EPUB/PDF/print proof.
"""

import os
import re
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit, urlunsplit

# Only these explicit editorial sections are excluded, and only at build time.
INTERNAL_SECTION_HEADERS = {"Review Notes", "Figure Placeholders"}
# Chapter drafting left inline notes, not just H2 planning sections.
INLINE_PLACEHOLDER = re.compile(
    r"^\s*\[(?:Figure|Photo|Illustration|Diagram)\s+placeholder:.*\]\s*$",
    re.IGNORECASE,
)
DRAFT_CONTINUATION = re.compile(
    r"^Part\s+\d+\s+will continue with\s+.*\.\s*$",
    re.IGNORECASE,
)
MARKDOWN_LINK = re.compile(
    r'''(?P<opening>!?\[[^\]\n]*\]\()(?P<target>[^)\s]+)(?P<closing>(?:\s+["'][^"']*["'])?\))'''
)
FENCE = re.compile(r"^\s*(?:\x60{3,}|~{3,})")


def without_editorial_sections(markdown: str):
    """Remove named, editor-only H2 blocks; never change the chapter source."""
    kept = []
    excluded = []
    hiding = False

    for line in markdown.splitlines(keepends=True):
        match = re.match(r"^##\s+(.+?)\s*$", line.strip())
        if match:
            section = match.group(1).strip()
            hiding = section in INTERNAL_SECTION_HEADERS
            if hiding:
                excluded.append(section)
                continue
        elif re.match(r"^#\s+", line):
            hiding = False
        if not hiding:
            if INLINE_PLACEHOLDER.fullmatch(line.strip()):
                excluded.append('Inline figure placeholder')
                continue
            if DRAFT_CONTINUATION.fullmatch(line.strip()):
                excluded.append('Draft continuation handoff')
                continue
            kept.append(line)

    return "".join(kept).rstrip() + "\n", excluded


def _outside_fences(markdown: str):
    """Yield (line, is_fenced) preserving newlines, to avoid rewriting examples."""
    fenced = False
    for line in markdown.splitlines(keepends=True):
        if FENCE.match(line):
            fenced = not fenced
            yield line, True
        else:
            yield line, fenced


def rebase_local_links(markdown: str, source: Path, root: Path, publication_dir: Path):
    """Make local Markdown links relative to the assembled file, with fail-fast checks."""
    source = source.resolve()
    root = root.resolve()
    publication_dir = publication_dir.resolve()
    local_links = 0
    local_images = 0

    def transform(m):
        nonlocal local_links, local_images
        original = m.group("target")
        target = urlsplit(original)

        # Preserve external links, mailto, in-page links and anchored references.
        if target.scheme or target.netloc or not target.path or target.path.startswith("/"):
            return m.group(0)

        resolved = (source.parent / unquote(target.path)).resolve()
        if not resolved.is_relative_to(root):
            raise ValueError(f"Link escapes repository: {source.relative_to(root)}: {original}")
        if not resolved.is_file():
            raise ValueError(f"Missing local link target: {source.relative_to(root)}: {original}")

        rebased_path = os.path.relpath(resolved, publication_dir).replace(os.sep, "/")
        updated = urlunsplit(("", "", quote(rebased_path, safe="/._~-"), target.query, target.fragment))
        local_links += 1
        if m.group("opening").startswith("!"):
            local_images += 1
        return m.group("opening") + updated + m.group("closing")

    new_text = []
    for line, fenced in _outside_fences(markdown):
        new_text.append(line if fenced else MARKDOWN_LINK.sub(transform, line))
    return "".join(new_text), local_links, local_images


def validate_publication_images(markdown: str, root: Path, publication_dir: Path):
    """Validate source paths of all local inline images visible to readers."""
    root = root.resolve()
    publication_dir = publication_dir.resolve()
    count = 0

    for line, fenced in _outside_fences(markdown):
        if fenced:
            continue
        for match in MARKDOWN_LINK.finditer(line):
            if not match.group("opening").startswith("!"):
                continue
            target = urlsplit(match.group("target"))
            if target.scheme or target.netloc:
                continue
            if not target.path or target.path.startswith("/"):
                raise ValueError(f"Invalid publication image URL: {match.group('target')}")
            resolved = (publication_dir / unquote(target.path)).resolve()
            if not resolved.is_relative_to(root) or not resolved.is_file():
                raise ValueError(f"Broken publication image URL: {match.group('target')}")
            count += 1
    return count
