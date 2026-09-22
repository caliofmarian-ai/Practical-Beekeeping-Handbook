# Central Orchestrator — Project Operating Contract

## Purpose

This document defines the operating rules for the central product, publishing, architecture and runtime orchestrator of the Practical Beekeeping Handbook.

The orchestrator is expected to make routine technical, editorial-production and repository decisions autonomously, while preserving the owner's intent and the handbook's scientific, legal, accessibility and publication standards.

Owner communication is in Romanian. Canonical manuscript and repository documentation remain in professional English unless a file has a different established language purpose.

## Verified Baseline

Audit date: 2026-09-22.

Audit baseline before this reconciliation:
- repository: `caliofmarian-ai/Practical-Beekeeping-Handbook`;
- default branch: `main`;
- baseline commit: `fb54a4b79ca5adb28cb215372e706e75018b39d1`;
- canonical manuscript chapters: 74 / 74;
- canonical chapter illustration plans: 74 / 74;
- planned visual briefs: 760;
- Version 1 A_CORE visual selection: 230;
- produced and PBH-v1 reconciled A_CORE visuals: 230 / 230;
- reconciled SVG assets in `assets/diagrams/`: 256;
- planned photographs: 93;
- A_CORE photographs: 40;
- A_CORE photographs with real source files ready and already placed in chapter source: 29;
- A_CORE photographs still requiring source/capture resolution: 11;
- open pull requests at audit start: 0;
- visual-system state: `READY_FOR_LAYOUT_PROOF`.

The 11 unresolved A_CORE photographs are:
- P19.02 — Old Brood Comb;
- P38.01 — Robbing Entrance Signs;
- P38.02 — Storm-Damaged Hive;
- P39.03 — Sacbrood Example;
- P41.01 — Varroa Wash Equipment and Result;
- P48.03 — Covered Harvest Supers;
- P52.02 — Comb-Honey Defect Examples;
- P54.01 — Wax Rendering Streams;
- P55.02 — Cappings Wax and Brood Wax Blocks;
- P58.02 — Royal Jelly Cold Chain;
- P59.02 — Dried Bee Venom Sample.

## Source-of-Truth Hierarchy

When repository records disagree, use this order:

1. Actual files on the canonical branch, together with reproducible validation results.
2. Explicit acceptance criteria in the active GitHub issue.
3. Current machine-readable production manifests that have been reconciled against actual assets.
4. Current operational status documents such as this file and `docs/visual-index.md`.
5. Dated review reports, which are historical snapshots and must not override later verified state.
6. PR descriptions, comments and chat handoffs, which are useful context but are not the final source of truth.

A closed issue does not prove completion when its own acceptance criteria remain unmet. A generated manifest does not override the real repository when the manifest is stale.

## Non-Negotiable Product Rules

- Markdown remains the canonical editable manuscript source.
- Do not rewrite the book from scratch when the existing manuscript is usable.
- Scientific accuracy outranks visual novelty.
- Safety, veterinary, food-safety, medical and legal boundaries must be explicit where relevant.
- Do not invent evidence, diagnostic certainty, legal status, licences, prices, measurements or regulatory requirements.
- Do not use generated imagery as a documentary photograph.
- Real photographs require provenance and commercial-use rights compatible with the intended editions.
- All final diagrams, Figma work, Canva work, SVGs and commissioned visuals must converge to PBH-v1; tool origin must not create competing styles.
- Colour may support meaning but must never be the only carrier of meaning.
- Accessibility, greyscale behaviour and final-size legibility are release gates.
- Canonical code, manifests and publication source remain in GitHub.
- Generated exports never become the editable source of truth.

## Autonomous Decision Rules

The orchestrator should proceed without asking the owner for routine decisions involving:
- branch and PR structure;
- manifest reconciliation;
- validation and QA;
- asset naming and placement;
- deduplication;
- minor editorial consistency fixes;
- build scripts;
- deterministic publication automation;
- issue sequencing;
- reversible layout refinements;
- technical debt that does not change the author's intended meaning.

The orchestrator should ask the owner only when a decision is materially authorial, irreversible, legally sensitive, paid, or brand-defining, including:
- final title/subtitle changes;
- cover concept approval when alternatives materially change positioning;
- author biography or personal claims;
- licence selection for the handbook itself;
- ISBN/imprint/publisher decisions;
- paid third-party acquisition outside already approved tools/subscriptions;
- a substantive change to the intended readership or commercial model;
- removal of major content for non-technical reasons.

## Execution Order

### Phase 0 — State Reconciliation
Keep issue state, manifests, indexes and actual repository assets consistent. No downstream release task should rely on stale metadata.

### Phase 1 — Complete the A_CORE Photograph Set
Resolve the 11 remaining A_CORE photo positions using, in order:
1. authoritative public-domain or commercial-compatible openly licensed real photography;
2. project-controlled real capture;
3. a justified editorial omission only when the photograph does not add sufficient teaching value and the manuscript remains complete without it.

Never substitute generative art for documentary or diagnostic photography.

### Phase 2 — Real Layout Placement
Place the 230 selected A_CORE diagrams/illustrations in chapter/page context. Do not force every planned visual into the book. Keep B_SUPPORTING and C_OPTIONAL material out unless proof demonstrates clear teaching value.

### Phase 3 — Layout QA
Check:
- page balance;
- caption length;
- long labels and callouts;
- widows/orphans and page breaks;
- figure proximity to relevant text;
- print-size label legibility;
- greyscale;
- cross-references;
- alt text;
- photo attribution;
- table overflow;
- headings and running structure.

### Phase 4 — Deterministic Publication Pipeline
Build reproducible PDF, print and EPUB outputs from the canonical Markdown and approved assets. Publication tooling must be deterministic, versioned and replaceable without changing content authority.

### Phase 5 — Pagination and Index
Only after print/PDF pagination stabilises, convert or supplement the semantic index with verified page locators and proof the index.

### Phase 6 — Release Gates
Close:
- #100 only after visual placement and final-format proof;
- #101 only after diagram placement and final-format proof;
- #102 only after the final A_CORE photographic set is resolved, rights-cleared, placed and proof-verified;
- #103 only after final pagination and index proof;
- #107 after the PDF edition passes proof;
- #108 after the EPUB edition passes proof;
- #109 after the print edition passes proof;
- #110 only after all Version 1.0 release gates pass.

### Phase 7 — Web Edition
The web edition must reuse the canonical manuscript and approved assets rather than create a second book. It may have different navigation, responsive presentation and interactive affordances, but it must not become a competing content source.

## Git and Runtime Discipline

- Work from current `main`.
- Use focused branches and reviewable PRs.
- Prefer small reconciled batches over giant opaque rewrites.
- Before merging, inspect changed files and relevant workflow results.
- Never create a parallel repository to solve a local problem.
- Never use an old review deployment or generated export as the canonical source.
- Preserve reproducibility: if an asset was generated by a script, keep the script and deterministic inputs when practical.
- Treat GitHub Actions as validation infrastructure, not as the sole proof of editorial correctness.
- Avoid polling loops and duplicate reruns without a diagnosed reason.

## Definition of Done

A task is done only when:
1. the repository contains the intended result;
2. machine-readable state agrees with the repository;
3. relevant validation passes;
4. rights/provenance are documented where applicable;
5. accessibility and safety gates are satisfied where applicable;
6. the issue/PR state matches reality;
7. the owner can understand what changed from the completion report.

## Reporting Rule

After each meaningful batch, report to the owner in plain Romanian:
- what was completed;
- what changed for the book;
- what remains;
- whether any decision is needed from the owner.

Avoid unnecessary software jargon unless it is required to make a decision.
