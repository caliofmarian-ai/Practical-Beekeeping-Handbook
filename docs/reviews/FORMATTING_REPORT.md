# Formatting Review — Publication Manuscript Assembly

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

- **chapter count 74** — PASS
- **reference count 11** — PASS
- **asset anchor count 74** — PASS
- **part count 9** — PASS
- **manifest chapter count 74** — PASS
- **manifest reference count 11** — PASS
- **manifest asset plan count 74** — PASS
- **canonical chapter sequence** — PASS
- **canonical reference sequence** — PASS
- **em dash chapter titles** — PASS
- **non empty manuscript** — PASS

## 4. Canonical Assembly Result

- Parts: **9**
- Chapters: **74**
- Reference Material sections: **11**
- Chapter illustration-plan anchors: **74**
- Publication manuscript characters: **3,334,818**
- Generated SHA-256: `f963b0334a5fbbf8339fdc31c33c66b01a3a4bfef2affc204e49864ad17aa702`

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
