# Layout Pilot — Chapters 1–5 (PBH-WAVE02-CH01-05)

**Review date:** 2026-10-12  
**Issues:** #225 (pilot), #100 (illustrations), #101 (diagrams), #107 (PDF)  
**Status:** GENERATED; STRUCTURAL CHECKS PASS; **NOT APPROVED FOR RELEASE OR PRINT**

## Verified pilot output

- Chapters: **5/5** (canonical Chapters 1–5), chapter files unchanged.
- Approved A_CORE SVG figures: **15/15** registered, source-checked, and inserted after explicit heading anchors.
- PDF captions found in PDF text: **15/15**.
- Generated PDF pages: **161** at experimental **176 × 250 mm** page size.
- Original diagrams remain PBH-v1 SVGs; no duplicated hand-drawn figures.
- No PDF pages are fully blank in automated text-layer extraction (the opening page is intentionally sparse).
- Inline `[Figure placeholder: ...]` statements were detected during actual proof inspection; preflight now excludes **42** across the full 74-chapter assembled reader edition. One Chapter 11 drafting handoff sentence is also excluded.
- Full reader-edition manifest rebuilt with 35/35 existing photo links validated.
- The repository retains the original chapter manuscript for editorial traceability.

## Manual visual spot-check (non-exhaustive)

Reviewed sampled rendered pages, including page 2 (body heading typography), page 5 (Figure 1.2, cutaway), page 60 (Figure 2.1, timeline plus table).

**Findings to resolve during page proof:**
1. **Figure micro-labels** inside some approved A_CORE SVGs remain too small to read comfortably at the experimental B5-scale page width (notably the small explanatory text on Figure 1.2 and Figure 2.1). Asset-level SVG validation alone is insufficient to establish practical printed legibility.
2. Some table cells contain **undesirable hyphenation/word splitting** in the experimental format, visible on the historical timeline table (page 60).
3. Precise placement, page breaks, orphans, long tables, caption proximity, alt text in PDF and output-specific colour/greyscale must be checked across **all** pages, not inferred from 15 successful captions.
4. The experimental 5-chapter proof already occupies **161 pages**, indicating that volume count, trim size, typography and editorial density require an explicit feasibility decision before final print design. Do not extrapolate a final page count from this preliminary subset.
5. The cover, print specifications, ISBN/imprint and project licence remain owner-level publication decisions; these are outside this code-only pilot.

## Engineering state

- Source-of-truth Markdown, Figure A_CORE visual manifest, figure placement manifest and renderer are versioned.
- GitHub Actions provides a downloadable proof PDF, Markdown, manifest, preflight JSON and selected page PNGs.
- Proof artifacts are explicitly marked `GENERATED_NOT_VISUALLY_APPROVED`.
- Technical gate passes are **not** final legal, accessibility, scientific figure-in-page or print proofs.

## Next actions

1. Review page-level typography, tables and micro-labels on the 15 figures. Trial larger figure placements or selective label redesign; preserve scientific meaning.
2. Choose provisional book trim/volume strategy before expanding layout to 74 chapters.
3. Expand placement manifests by chapter groups after proof QA, without rewriting canonical chapter text.
4. Finish the authentic photo P59.02 (#102); never use generated pseudo-photography as diagnostic or documentary evidence.
5. Run full-book proof, final index and PDF/EPUB/print pipelines, then seek owner approval for release.

**Result:** The pilot demonstrates a repeatable publishing pipeline, **not** a complete or print-approved edition.
