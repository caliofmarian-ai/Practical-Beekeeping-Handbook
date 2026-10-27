# Complete digital edition and multi-volume print edition

Decision recorded: 27 October 2026. Implementation: Issue #230.

## Approved direction and what remains provisional

The owner approved one complete digital edition and a printed edition in multiple volumes. The working plan retains five thematic volumes and the canonical outline version 1.1. This approves the delivery direction, not the final prose, pagination, print dimensions, cover, licence, imprint or release.

The authoritative allocation is `docs/production/edition-plan.json`. The plan does not renumber, delete, summarise or rewrite chapters. Its five-volume boundaries are a working grouping: physical binding and page balance must be reviewed after the narrative revision, with particular attention to the first volume. Rebalance boundaries if necessary rather than shrinking type, reducing figure labels or removing content to fit a binding limit.

| Working print volume | Canonical coverage |
|---|---|
| 1 — Foundations, Honey Bee Biology and Starting an Apiary | Chapters 1–23; Parts I–III |
| 2 — Colony Management | Chapters 24–38; Part IV |
| 3 — Bee Health | Chapters 39–46; Part V |
| 4 — Honey Production and Other Hive Products | Chapters 47–59; Parts VI–VII |
| 5 — Business, Sustainability and Reference Material | Chapters 60–74; Parts VIII–IX; References 75–85 |

The complete digital edition contains Chapters 1–74 and References 75–85. PDF, EPUB and web are rendering targets for the same content, not separate editable books. This change does not implement a production EPUB or web deployment.

## Reference and safety policy

Chapter bibliographies, practical warnings, caveats and contextual explanations remain in their original chapters. All eleven canonical reference sections are included in the complete digital source and at the end of Volume 5. Every generated volume includes a set locator directing readers to the other volumes and complete reference material. A print navigation and standalone safety review remains mandatory before publication; a link to another volume cannot replace an essential warning at the point of use.

Chapter numbers remain global across the set. Figure IDs and photo IDs retain their existing chapter-based identities. Page numbers will be local to each physical volume, and the final index must identify both volume and page. No page locator may be invented from the experimental 161-page pilot.

## Editorial hold discovered during live reconciliation

Issue #228 is an open P0 narrative-depth requirement. Draft PR #229 revises only three representative Chapter 1 sections and explicitly requires the owner's prose-style review. The historic closure of technical/language tasks and the existence of 74 chapter files do not satisfy that requirement. The approval of this edition direction must not be used to merge PR #229, close #228 or label the manuscript reader-ready.

Continue narrative revision in reviewed batches. Explanatory paragraphs should teach what happens, why it happens, how to recognise it, and the practical limits. Lists remain appropriate for ordered procedures, checklists and inventories after explanation. Structural counts are inspection aids only; they do not replace editorial judgement and must not become arbitrary word-count targets.

## Implemented source build

Run `python scripts/build_edition_set.py` from the repository root. It builds six proof-only Markdown files under `exports/editions/`: one complete digital source and five print-volume sources. It also creates a source-hashed inventory and `EDITION_READINESS.md` with chapter-level structural counts.

The builder reads canonical source files without editing them, removes only the same explicit drafting notes already excluded by the publication preflight, preserves substantive content, rebases existing image paths and validates selected asset files. It checks that all 74 chapters appear exactly once across print volumes, that all reference sections are retained, and that all 230 selected core diagram files and all 36 source photographs are accounted for. Asset presence is not final page placement: most diagrams still require integration into the publication layout.

Run `python scripts/build_edition_set.py --check` to reject a stale generated set. The workflow retains the generated output for review and includes the referenced images in the downloadable source package, preserving repository-relative paths.

## Release check

Run `python scripts/build_edition_set.py --release-check`. The command deliberately exits with status 2 while any mandatory gate is pending, lacks evidence or refers to a different source fingerprint. This is a readiness check, not a publisher or payment/deployment action. No production release is created by these scripts.

The independent gates cover narrative review, the owner's prose sample, scientific review after rewriting, visual page proof, pagination/index/navigation, rights/cover/imprint, digital format proof, and print sizing/format proof. Passing source-integrity CI does not change these gate states.

## Next production order

Complete and review the narrative model under #228/#229, then revise Chapters 1–5 and subsequent batches. Rebuild this edition set from the revised sources. Resolve the known small figure-label and table-hyphenation issues in actual page proofs. Measure every proposed volume, settle physical boundaries and printer-specific requirements, then generate volume-aware index locators and prove digital and print exports. Close #107–#110 only with their own evidence.

This document supersedes any earlier unresolved statement about whether the delivery should be single-volume or multi-volume. It does not supersede scientific or visual standards and does not close any editorial or format proof task.
