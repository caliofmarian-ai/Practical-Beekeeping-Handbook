# A_CORE Photograph Layout Preparation — Pass 01

**Issue:** #102 — Reference 84 — Photographs  
**Date:** 2026-09-20  
**Result:** PASS — 10 READY SOURCE PHOTOGRAPHS PLACED IN CHAPTER SOURCE

## Scope

This pass takes the ten A_CORE photograph source files that reached `SOURCE_FILE_READY` in PR #174 and moves them into manuscript layout preparation.

## Result

- source-ready photographs: **10/10**
- chapter-source placements: **10/10**
- missing manuscript references: **0**
- duplicate manuscript references: **0**
- alt text drafted: **10/10**
- captions drafted: **10/10**
- creator/rights credit retained: **10/10**
- external hotlinked images: **0**
- generated-photo substitutes: **0**

The machine-readable placement record is:

`assets/photos/a-core/photo-layout-manifest-01.json`

## Chapters updated

- Chapter 3 — P03.01 Honey Bee on Flower
- Chapter 9 — P09.01 Worker Carrying Pollen
- Chapter 25 — P25.02 Healthy Capped Worker Brood
- Chapter 39 — P39.01 Healthy Larvae Reference
- Chapter 39 — P39.02 Chalkbrood Mummies
- Chapter 40 — P40.01 Adult Female Varroa on Bee
- Chapter 40 — P40.02 Tropilaelaps Specimen
- Chapter 41 — P41.02 Deformed-Wing Bee
- Chapter 49 — P49.02 Uncapping Detail
- Chapter 58 — P58.01 Royal Jelly in Queen Cell

## Editorial safeguards retained

- A normal brood photograph is not described as proof of a disease-free colony.
- Failure to see Varroa in a photograph or routine inspection is not treated as evidence of low infestation.
- Deformed wings are not treated as a quantitative mite count.
- Tropilaelaps morphology is presented as context, with surveillance/laboratory confirmation retained for unfamiliar specimens.
- Chalkbrood appearance is interpreted with colony history and other signs rather than as a photograph-only diagnostic rule.
- Pollinator flower visitation is not equated automatically with successful pollination.

## Manifest reconciliation

`assets/photo-production-manifest.json` has been synchronised for these ten positions:
- `production_status = SOURCE_FILE_READY`
- current rights status copied from the validated source manifest
- source-resolution review marked PASS
- repository source path, SHA-256 and pixel dimensions recorded

The final-asset path intentionally remains unset because page crop, export colour management and final page proof have not yet been approved.

## Boundary

Placement in Markdown source is not final print approval. The next required gates are:

1. render the affected chapters/pages in the publication build;
2. inspect crop, size, caption wrapping and page balance;
3. verify attribution treatment in PDF/EPUB;
4. keep sourcing/capturing the remaining A_CORE positions;
5. mark final placement only after export proof.

Issue #102 remains open.
