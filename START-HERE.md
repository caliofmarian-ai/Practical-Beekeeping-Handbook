# Start Here

This repository contains the working source for the Practical Beekeeping Handbook.

## Official Workflow

1. Work from the repository root.
2. Save official manuscript chapters inside chapters/.
3. Follow the chapter order in docs/BOOK_OUTLINE.md.
4. Follow all rules inside docs/standards/.
5. Use figure placeholders during manuscript drafting.
6. Add final illustrations during the illustration and layout stage.
7. Commit and push every completed issue.

## Official Chapter Naming Format

- chapters/chapter-01.md
- chapters/chapter-02.md
- chapters/chapter-03.md

## Official Image Naming Format

- assets/illustrations/chapter-01-figure-01.png

## Markdown Image Reference

![External anatomy of a worker honey bee](assets/illustrations/chapter-06-figure-01.png)

*Figure 6.1 — External anatomy of a worker honey bee.*

## Manuscript Rule

ASCII diagrams are not permitted in the final manuscript.

During drafting, use a figure placeholder:

> **Figure 6.1 — External anatomy of a worker honey bee.**
> *Professional illustration to be added during the illustration and layout stage.*

## Canonical Documents

- README.md
- docs/BOOK_OUTLINE.md
- docs/REPOSITORY_STRUCTURE.md
- docs/standards/WRITING_STANDARDS.md
- docs/standards/ILLUSTRATION_STANDARDS.md
- docs/standards/TABLE_STANDARDS.md
- docs/standards/CITATION_GUIDE.md


## Operational Control

- `docs/CENTRAL_ORCHESTRATOR.md` — verified project baselines, source-of-truth hierarchy, execution order, QA gates, and autonomous operating rules.
- `docs/production/MULTIVOLUME_EDITION.md` — current approved delivery direction and working five-volume architecture (Issue #230, recorded 27 October 2026).
- `docs/production/edition-plan.json` — machine-readable digital/print coverage and independent release gates.

## Current Editorial Hold

Read open Issue #228 and draft PR #229 before resuming publication work. The owner requires developed explanatory prose, not outline-style chapters dominated by lists. The historic technical/language review and the presence of all 74 chapter files do not constitute narrative approval.

The complete-digital plus multi-volume-print direction is approved; narrative quality, final pagination, image page proof, index, licensing and format approvals are not. Never close #228 or merge the prose sample solely because the edition structure has been approved.

`python scripts/build_edition_set.py` generates proof-only sources and the chapter inventory. `--check` verifies reproducibility. `--release-check` must remain blocked until every mandatory gate has evidence for the current source fingerprint. The generated files are not alternative editable manuscripts.
