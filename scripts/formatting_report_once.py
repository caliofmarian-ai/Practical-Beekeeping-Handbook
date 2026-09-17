from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / 'exports' / 'publication' / 'Practical-Beekeeping-Handbook.md'
MANIFEST = ROOT / 'exports' / 'publication' / 'manifest.json'
REPORT = ROOT / 'docs' / 'reviews' / 'FORMATTING_REPORT.md'


def main():
    if not MANUSCRIPT.is_file() or not MANIFEST.is_file():
        raise SystemExit('Publication manuscript or manifest is missing')

    data = json.loads(MANIFEST.read_text(encoding='utf-8'))
    text = MANUSCRIPT.read_text(encoding='utf-8')

    chapter_count = len(re.findall(r'^# Chapter \d+ — ', text, flags=re.M))
    reference_count = len(re.findall(r'^# Reference \d+ — ', text, flags=re.M))
    asset_anchor_count = len(re.findall(r'^<!-- ASSET-PLAN: ', text, flags=re.M))
    part_count = len(re.findall(r'^# Part (?:I|V|X)+ — ', text, flags=re.M))

    checks = {
        'chapter_count_74': chapter_count == 74,
        'reference_count_11': reference_count == 11,
        'asset_anchor_count_74': asset_anchor_count == 74,
        'part_count_9': part_count == 9,
        'manifest_chapter_count_74': data.get('chapter_count') == 74,
        'manifest_reference_count_11': data.get('reference_count') == 11,
        'manifest_asset_plan_count_74': data.get('asset_plan_count') == 74,
        'canonical_chapter_sequence': [x['number'] for x in data.get('chapters', [])] == list(range(1, 75)),
        'canonical_reference_sequence': [x['number'] for x in data.get('references', [])] == list(range(75, 86)),
        'em_dash_chapter_titles': not bool(re.search(r'^# Chapter \d+\s+[–-]\s+', text, flags=re.M)),
        'non_empty_manuscript': len(text) > 100000,
    }
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        raise SystemExit('Formatting validation failed: ' + ', '.join(failed))

    rows = '\n'.join(f'- **{name.replace("_", " ")}** — PASS' for name in checks)

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(f'''# Formatting Review — Publication Manuscript Assembly

**Issue:** #106  
**Review date:** 17 September 2026  
**Formatting authority:** `docs/standards/FORMATTING_SPEC.md`  
**Language authority:** `docs/standards/LANGUAGE_STYLE_SHEET.md`  
**Result:** **PASS — READY FOR VISUAL PRODUCTION / EXPORT**

## 1. Scope

This formatting pass assembled the technically and linguistically reviewed handbook into a deterministic publication-order Markdown source while preserving the canonical source chapters and reference material.

The pass intentionally does **not** create the final PDF, EPUB or print package. It establishes a validated publication source for those later export stages.

## 2. Generated Publication Files

- `exports/publication/Practical-Beekeeping-Handbook.md`
- `exports/publication/manifest.json`

The manifest records source paths and SHA-256 hashes so the assembled edition can be traced back to the source manuscript used for the build.

## 3. Structural Validation

{rows}

## 4. Canonical Assembly Result

- Parts: **9**
- Chapters: **{chapter_count}**
- Reference Material sections: **{reference_count}**
- Chapter illustration-plan anchors: **{asset_anchor_count}**
- Publication manuscript characters: **{len(text):,}**
- Generated SHA-256: `{data.get('generated_sha256', '')}`

All Chapters 1–74 appear exactly once and in canonical order. Reference Material 75–85 appears exactly once and in canonical order.

## 5. Formatting Decisions Applied

- displayed chapter headings are normalised in the assembled output to `Chapter N — Title` using an em dash;
- part-opening and chapter-opening page-break intent is encoded through non-printing comments;
- every chapter is linked to its approved per-chapter illustration plan through a non-printing `ASSET-PLAN` anchor;
- source chapter files remain the editorial authority and are not rewritten merely for layout punctuation;
- official source titles, URLs, DOI strings and legal titles remain untouched;
- visual production remains external to the reader-facing manuscript until final assets pass review;
- Reference Material sources are inserted as deterministic back matter and their first headings are demoted only in the assembled output to preserve hierarchy.

## 6. Table and Visual Readiness

`docs/standards/FORMATTING_SPEC.md` now defines:

- print-safe table behaviour;
- repeated table headers where supported;
- landscape/redesign fallback instead of unreadably small text;
- warning hierarchy independent of colour;
- greyscale-safe visual requirements;
- digital alt-text requirement;
- caption style and scientific limitation notes;
- page-break intent and chapter asset anchors.

## 7. Remaining Publishing Dependencies

These are intentional dependencies, not formatting failures:

- **#100 Reference 82 — Illustrations:** final illustration assets, review and linking;
- **#101 Reference 83 — Diagrams:** final diagram assets, review and linking;
- **#102 Reference 84 — Photographs:** final photography/rights review and linking;
- **#103 Reference 85 — Index:** final page locators after pagination stabilises;
- **#107 PDF:** final PDF generation and preflight;
- **#108 EPUB:** semantic EPUB generation and validation;
- **#109 Print:** print-ready package, bleed/margins/colour/profile/preflight as applicable.

## 8. Known Layout-Stage Items

The following remain appropriately deferred until final visual assets and target trim/export formats are known:

- final pagination;
- widow/orphan tuning;
- exact image dimensions and crop;
- final table breaks;
- final figure/diagram/photo numbering after asset consolidation;
- index page locators;
- printer-specific bleed, spine and colour-profile requirements.

## 9. Conclusion

Formatting Issue #106 has produced a deterministic, validated publication manuscript without weakening technical content or prematurely embedding provisional artwork.

**Status: READY FOR VISUAL PRODUCTION / EXPORT.**
''', encoding='utf-8')

    print(f'Formatting report written: {REPORT.relative_to(ROOT)}')
    print(f'chapters={chapter_count} references={reference_count} assets={asset_anchor_count} chars={len(text)}')


if __name__ == '__main__':
    main()
