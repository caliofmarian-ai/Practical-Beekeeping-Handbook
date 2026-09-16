# Reference 82 — Illustrations

## Status

**PRE-LAYOUT REGISTER — FINAL ARTWORK NOT YET PRODUCED**

This register consolidates the illustration planning for Chapters 1–74. It is not a substitute for the final production assets. In accordance with the handbook workflow, no provisional artwork is inserted into the reader-facing manuscript. Final professional illustrations will be generated, reviewed, rights-cleared where necessary, and placed during layout.

Issue #100 remains open until those assets are complete.

---

## 1. Inventory Audit

A repository audit performed after completion of Chapter 74 found:

- Chapters **26–74** already had dedicated files named `chapter-NN-illustration-plan.md`.
- Chapters **22–25** had valid earlier plans under legacy filenames `chapter-22.md` through `chapter-25.md`.
- Chapters **1–21** had no dedicated illustration-plan files in `main`.
- This reference-material branch adds dedicated, standardised plans for Chapters **1–21**, eliminating the missing-plan gap.
- The archived noncanonical Honey Quality draft and its archived illustration plan remain under `docs/reference/` and are **not** part of the canonical figure sequence.

After this branch, every canonical chapter 1–74 has a chapter-level visual plan.

### Naming note

For final production, legacy files for Chapters 22–25 should be treated as authoritative plan sources despite their shorter filenames. Renaming can be done during the formatting pass if desired, but duplicate copies should not be created merely for filename consistency.

---

## 2. Figure Identification System

Use:

`Figure <chapter>.<sequence>`

Examples:

- `Figure 6.1` — external worker anatomy;
- `Figure 41.6` — adult-bee Varroa wash procedure;
- `Figure 67.1` — traceability chain;
- `Figure 74.1` — future-of-beekeeping systems map.

Rules:

1. figure numbers restart at `.1` for every chapter;
2. a multi-panel figure remains one figure if panels are parts of one teaching concept;
3. a visual reused in another chapter should normally be cross-referenced, not silently duplicated and renumbered;
4. if the reused visual is materially adapted, create a new figure and record its source relationship;
5. reference-section visuals, if any, use `Figure R82.x`, `R83.x`, etc., to avoid collision with chapter figures.

---

## 3. Master Asset Metadata

Every final illustration asset must carry the following metadata in the production register:

| Field | Required content |
|---|---|
| Figure ID | e.g. `41.6` |
| Chapter | Chapter number and title |
| Working title | Human-readable title |
| Visual type | anatomical / process / decision flow / comparison / map / chart / technical cutaway / behavioural |
| Purpose | The decision or concept the figure teaches |
| Final caption | Reader-facing caption |
| Source basis | Chapter text + cited scientific/technical sources |
| Provenance | Original commissioned / generated / adapted / licensed |
| Rights | Commercial print + digital rights status |
| Accuracy reviewer | Person/role/date |
| Accessibility | Alt text / greyscale / colour-independent coding |
| Print size | single-column / double-column / full page |
| Resolution/vector status | production requirement |
| Production status | planned / drafted / technical review / approved / placed |
| Revision ID | final asset version |

No asset is **APPROVED** merely because it looks attractive.

---

## 4. Visual Classes

### 4.1 Anatomical and biological illustrations

Use for:

- external/internal honey bee anatomy;
- queen/drone/worker differences;
- brood stages;
- glands and reproductive structures;
- Varroa/Tropilaelaps/tracheal mites;
- disease cell-level signs;
- pollen, wax, propolis, royal jelly, and venom origins.

**Production requirement:** scientifically accurate proportions, structures, developmental stage, orientation, and scale cues.

### 4.2 Hive and equipment technical illustrations

Use for:

- hive types/components;
- frames/foundation;
- feeders;
- queen-rearing equipment;
- transport ventilation;
- honey extraction/processing;
- wax rendering;
- cold-chain and storage systems.

**Production requirement:** mechanical geometry must be internally consistent. Do not combine dimensions from incompatible hive systems.

### 4.3 Process illustrations

Use for:

- inspections;
- feeding;
- swarm capture;
- splits;
- queen introduction/rearing;
- Varroa sampling;
- disease sampling;
- harvest and extraction;
- creamed-honey production;
- pollen/propolis/royal-jelly handling;
- traceability and recall.

**Production requirement:** safe sequence, explicit stop points, and no off-label treatment or unsafe equipment shortcuts.

### 4.4 Comparative plates

Use when visual comparison improves diagnosis or choice:

- healthy versus abnormal brood;
- AFB versus EFB versus chilled brood/sacbrood;
- Varroa versus Tropilaelaps;
- dry versus wet cappings;
- old versus new comb;
- good versus poor apiary site;
- balanced versus unbalanced extractor.

**Production requirement:** comparison must not imply that appearance alone provides definitive diagnosis where laboratory/inspector confirmation is required.

### 4.5 Maps and landscape illustrations

Use for:

- forage mosaics;
- apiary placement;
- pollinator habitat connectivity;
- dated pest-distribution examples;
- movement/traceability routes.

**Production requirement:** date all distributions that can change, especially exotic/invasive pests. Avoid decorative global maps with unsupported precision.

### 4.6 Charts and data graphics

Use for:

- colony seasonal dynamics;
- scale-hive curves;
- crystallisation;
- time–temperature quality effects;
- IPM decision logic;
- business break-even/capacity concepts;
- evidence hierarchy.

**Production requirement:** axes, units, uncertainty, and conceptual-versus-measured status must be explicit.

---

## 5. Part-by-Part Illustration Register

The detailed working titles reside in the chapter plan files. This master register tracks readiness at chapter level.

| Part | Chapters | Plan status | Production status |
|---|---|---|---|
| I — Foundations | 1–5 | Complete | Artwork pending |
| II — Honey Bee Biology | 6–14 | Complete | Artwork pending |
| III — Starting an Apiary | 15–23 | Complete; 22–23 legacy filenames | Artwork pending |
| IV — Colony Management | 24–38 | Complete; 24–25 legacy filenames | Artwork pending |
| V — Bee Health | 39–46 | Complete | Artwork pending |
| VI — Honey Production | 47–54 | Complete | Artwork pending |
| VII — Other Hive Products | 55–59 | Complete | Artwork pending |
| VIII — Business | 60–69 | Complete | Artwork pending |
| IX — Sustainability | 70–74 | Complete | Artwork pending |

---

## 6. High-Priority Visual Families

These visuals have unusually high teaching value and should receive first production priority.

### Biology

- worker external/internal anatomy;
- life-cycle and caste timelines;
- queen reproductive anatomy;
- worker task plasticity;
- waggle-dance geometry;
- brood-nest/colony organisation;
- seasonal population dynamics.

### Safe practical handling

- hive opening/inspection sequence;
- protective clothing and veil clearance;
- smoker-safe operation;
- swarm capture;
- split/nucleus construction;
- queen introduction;
- colony transport ventilation and securing.

### Bee health

- healthy versus diseased brood;
- AFB/EFB differential;
- Varroa reproductive cycle;
- adult-bee wash;
- Varroa versus Tropilaelaps morphology;
- Nosema microscopy workflow;
- virus/Varroa pathway;
- IPM cycle.

### Honey and products

- nectar-to-honey pathway;
- refractometer sampling/use;
- extraction-room flow;
- tangential versus radial extraction;
- time–temperature quality concepts;
- creamed-honey crystal structure;
- comb-honey quality defects;
- wax rendering safety;
- pollen preservation;
- propolis collection/extraction system;
- royal-jelly cold chain;
- bee-venom collection safety concept.

### Business and sustainability

- cost structure and bottleneck capacity;
- lot traceability chain;
- mock recall flow;
- food-safety hazard map;
- compliance matrix;
- biodiversity versus managed-bee distinction;
- pollinator habitat network;
- research-evidence hierarchy;
- technology-adoption framework.

---

## 7. Consolidation Opportunities

Final layout should reduce needless repetition by reusing or adapting approved visuals.

### Candidate A — Varroa life cycle
Primary figure should be produced once at high technical quality. Chapters 40, 41, 45, and 46 can cross-reference or use simplified derivative panels.

### Candidate B — Healthy brood reference
One anatomically accurate healthy brood plate can support disease chapters, with disease-specific comparison panels built from the same visual system.

### Candidate C — Traceability chain
Chapters 48, 50, 52, 64, 66, 67, and the appendices all use lot-flow concepts. Use one core visual grammar rather than unrelated arrows in every chapter.

### Candidate D — Evidence ladder
Chapter 56 (propolis claims), Chapter 59 (venom), Chapter 73 (research), and Chapter 74 (future technologies) benefit from a shared visual language for “laboratory → field → replicated evidence → guideline/authorisation”.

### Candidate E — Honey quality indicators
Moisture, HMF, diastase, conductivity, crystallisation, and phase separation recur across Chapters 48–53 and the archived Honey Quality reference. Consolidate into a consistent data-graphic family.

### Candidate F — Food-processing zones
Extraction, processing, storage, pollen, royal jelly, and food-safety chapters should share standard clean/incoming/quarantine zone symbols.

---

## 8. Visuals That Should Not Be Combined

Some apparent duplicates teach different questions and should remain distinct:

- **AFB/EFB clinical signs** versus **laboratory sampling workflow**;
- **Varroa monitoring** versus **treatment selection**;
- **comb-honey product defects** versus **beeswax source/contaminant streams**;
- **managed honey-bee forage** versus **wild-pollinator conservation habitat**;
- **food traceability** versus **bee/queen breeding pedigree**.

Consolidation must never remove diagnostic nuance.

---

## 9. Style System

Final illustrations should follow `docs/standards/ILLUSTRATION_STANDARDS.md` and these book-wide conventions:

- clean scientific editorial style rather than cartoon decoration;
- realistic bee, comb, equipment, and plant proportions;
- restrained colour palette suitable for print;
- labels outside critical anatomical detail where possible;
- leader lines with clear endpoints;
- consistent worker/queen/drone iconography;
- consistent healthy/suspect/hazard symbol system;
- no red/green-only coding;
- metric units primary where dimensions are shown;
- scale bars for micro/macro comparisons;
- dashed line = conceptual/hidden route, solid line = physical route or observed sequence;
- arrows require an explicit meaning in the legend.

---

## 10. Accessibility Requirements

Every final figure must:

1. remain understandable in greyscale;
2. avoid relying only on colour hue;
3. use readable labels at final print size;
4. include alt text in EPUB/digital editions;
5. avoid text embedded so small that zoom is required in print;
6. distinguish conceptual diagrams from literal anatomical/engineering views;
7. provide scale or magnification where size can be misunderstood.

---

## 11. Rights and Provenance

Preferred order:

1. original technical illustration commissioned/generated specifically for this handbook;
2. original author-owned photograph/diagram adapted into a figure;
3. openly licensed source compatible with commercial print/digital use;
4. specifically licensed third-party asset with documented permission.

Never rely on “found on the internet”.

For every adapted asset, retain:

- source URL/publication;
- creator;
- licence/permission;
- date obtained;
- permitted uses;
- modifications made;
- attribution text if required.

No font files, proprietary source assets, or unlicensed stock material should be distributed with the book repository.

---

## 12. Accuracy Review Gates

### Gate A — manuscript alignment
Does the figure teach exactly what the final chapter says?

### Gate B — technical review
Are anatomy, equipment, disease signs, units, directions, and processes correct?

### Gate C — safety/legal review
Does the image accidentally show unsafe handling, off-label medicines, contamination, or a legally false claim?

### Gate D — visual proof
Is it readable at final print size and in greyscale?

### Gate E — rights/provenance
Can it legally be published commercially in all intended formats?

Only after all five gates is status changed to **APPROVED FOR LAYOUT**.

---

## 13. Production Status Vocabulary

- `PLANNED` — described in chapter plan only.
- `BRIEF READY` — consolidated art brief approved.
- `DRAFT ART` — first asset produced.
- `TECH REVIEW` — awaiting/under scientific or mechanical review.
- `REVISION` — corrections required.
- `APPROVED` — technically/legally/accessibly approved.
- `PLACED` — inserted into final layout.
- `PROOF VERIFIED` — checked in final PDF/EPUB/print proof.

At the time of this register, chapter visual content is predominantly **PLANNED**. That is intentional; final artwork production is the next publishing phase, not something to fake with placeholders.

---

## 14. Completion Criteria for Reference 82 / Issue #100

Issue #100 is complete only when:

- [x] every canonical chapter has a visual plan;
- [x] the master register exists;
- [ ] duplicate/merge decisions are finalised after technical review;
- [ ] every selected figure has a final production brief;
- [ ] final assets are created;
- [ ] technical accuracy is approved;
- [ ] rights/provenance are documented;
- [ ] alt text is written;
- [ ] print/greyscale legibility is verified;
- [ ] figures are placed in final layout;
- [ ] final PDF/EPUB/print proofs are checked.

**Therefore this reference register is a major completion step, but Issue #100 must remain open until layout assets are actually produced and verified.**