# Visual Production Preflight — References 82–85

**Issues:** #100, #101, #102, #103  
**Date:** 17 September 2026  
**Status:** **PREFLIGHT PASS — ASSET PRODUCTION / SOURCING NEXT**

## 1. Purpose

This preflight converts the 74 chapter illustration plans and photographic shot register into machine-readable production manifests before final asset creation. It does not mark unproduced assets as approved.

## 2. Inventory

- canonical chapter illustration plans found: **74 / 74**
- parsed planned figures/illustrations/visuals: **760**
- duplicate figure IDs: **0**
- parsed planned photographs: **93**
- duplicate photograph IDs: **0**
- semantic index: **present** (`references/index.md`)
- diagram register: **present** (`references/diagrams.md`)
- illustration register: **present** (`references/illustrations.md`)
- photograph register: **present** (`references/photographs.md`)

## 3. Source-Heading Normalisation

The historical plans used several harmless heading conventions. The production manifest normalises all of them to chapter-scoped `Figure chapter.sequence` IDs:

- figure: **623**
- illustration: **27**
- visual: **110**

This changes production metadata only; manuscript wording is not altered.

## 4. Generated Production Manifests

- `assets/visual-production-manifest.json` — complete figure briefs and production metadata
- `assets/visual-production-manifest.csv` — production-board friendly figure index
- `assets/photo-production-manifest.json` — photograph sourcing/rights queue

All figure records remain at **BRIEF_READY** / **PENDING_ASSET_REVIEW** until actual assets pass accuracy, rights, accessibility and proof gates.

## 5. Figure-Type Distribution

- anatomical: **17**
- chart_data: **44**
- comparison: **114**
- decision_flow: **47**
- life_cycle: **4**
- map_landscape: **35**
- process: **79**
- scientific_illustration: **375**
- technical_cutaway: **15**
- timeline: **30**

Classification is a production-routing aid; each finished visual still requires technical review.

## 6. Corrective Finding Resolved

Formatting validation exposed a pre-production gap: standard dedicated illustration-plan files for Chapters 22–25 were missing even though older planning material existed. Standard professional plans were created for Chapters 22–25, and `references/illustrations.md` is updated so they are no longer legacy-filename exceptions.

## 7. Asset Gates

No final figure or photograph can move to `APPROVED` until it passes:

1. manuscript alignment;
2. scientific/mechanical accuracy;
3. safety/legal review;
4. greyscale and final-size legibility;
5. alt-text/accessibility review;
6. commercial print/digital rights/provenance;
7. final-layout proof verification.

## 8. Production Order

1. bee-health diagnostic/life-cycle visuals;
2. safety/practical handling sequences;
3. anatomy/biology core plates;
4. honey-processing and food-safety diagrams;
5. hive-product processing/safety visuals;
6. traceability/business/compliance diagrams;
7. sustainability/research/future diagrams;
8. field photographs with verified provenance/rights.

## 9. Reference 85 Index

The semantic index correctly uses chapter/reference locators rather than invented page numbers. Issue #103 remains open until final print/PDF pagination is stable and page locators are generated and proofed.

## 10. Conclusion

Visual inventory and production routing are deterministic. The next work is actual illustration/diagram production and photograph sourcing/rights review, followed by placement and final pagination.
