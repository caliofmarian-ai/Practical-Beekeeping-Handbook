# Visual Reconciliation — Pass 01: Foundations

**Result:** PASS — SAFE GLOBAL FOUNDATIONS NORMALISED

## Scope
- SVG assets scanned: **256**
- SVG files changed by safe normalisation: **256**
- Waves/directories: **10**

## Safe normalisation applied
- added `data-visual-system="PBH-v1"` to every SVG root;
- classified each SVG with a canvas-profile marker without resizing biological/technical content;
- added `preserveAspectRatio="xMidYMid meet"` where absent;
- normalised the handbook sans-serif stack to `Arial,Helvetica,sans-serif`;
- normalised shorthand white and pure near-black tokens to the canonical white/ink tokens;
- preserved biological/natural colours and did **not** force high-fidelity plates into schematic colours;

## Canvas profiles
- landscape-scientific: **18**
- landscape-standard: **162**
- portrait-field: **76**

Canvas profiles are intentional layout classes, not separate visual styles. Final layout may scale them, but reconciliation must preserve one typography/colour/line-work grammar.

## Metadata/accessibility gate
- missing title: **0**
- missing desc: **0**
- missing aria-labelledby: **0**
- missing PBH-v1 marker: **0**
- text-bearing files outside canonical Arial/Helvetica stack after pass: **0**

## Colour drift requiring editorial review
- files containing colours outside the canonical semantic + approved natural/biological allowance set: **96**

These colours are **not automatically replaced** because morphology, natural materials and diagnostic appearance take priority over branding. They are queued for Pass 02 family-level review.

## Line-weight review
- distinct stroke-width values detected: **154**

Pass 01 does not flatten all stroke widths: anatomy and microscopic detail require finer lines than process diagrams. Pass 02 will map values to family-level primary/secondary/detail roles.

## Next mandatory pass
Pass 02 will reconcile visual families rather than doing blind global replacements:
- process/decision-flow grammar;
- safety/caution/danger cards;
- healthy brood / queen-cell / Varroa / anatomy masters;
- honey-product and clean-zone systems;
- traceability/legal/business diagrams;
- recurring icons, arrows and callouts;
- greyscale and thumbnail checks.

**Publication state:** `PENDING_FINAL_RECONCILIATION`

### Files queued for colour-family review
- `assets/diagrams/wave-01/fig-21-1-protective-clothing-system.svg`: #EAF2F8
- `assets/diagrams/wave-01/fig-21-2-veil-clearance.svg`: #555, #EAF2F8
- `assets/diagrams/wave-01/fig-22-1-smoker-anatomy.svg`: #555, #EAF2F8
- `assets/diagrams/wave-01/fig-23-1-apiary-hazard-map.svg`: #555, #EAF2F8
- `assets/diagrams/wave-01/fig-24-2-prepared-receiving-hive.svg`: #555, #777, #EDF4F8
- `assets/diagrams/wave-01/fig-25-7-brood-pattern-interpretation.svg`: #3E2B22, #5A4030, #795A43
- `assets/diagrams/wave-01/fig-33-6-vehicle-loading.svg`: #DDD
- `assets/diagrams/wave-01/fig-38-2-starvation-versus-accessible-stores.svg`: #555, #777, #DDD
- `assets/diagrams/wave-01/fig-38-4-transport-overheating.svg`: #555, #DDD
- `assets/diagrams/wave-01/fig-39-2-healthy-brood-reference.svg`: #FFFBEA
- `assets/diagrams/wave-01/fig-39-3-patchy-brood-multiple-causes.svg`: #3E2B22, #5A4030, #795A43
- `assets/diagrams/wave-01/fig-39-4-afb-suspicion-features.svg`: #3E2B22, #4E3024, #5A4030, #795A43, #7A3F20, #F6E7B0, #FFF1CF
- `assets/diagrams/wave-01/fig-40-3-varroa-reproductive-cycle.svg`: #5C2A1D, #9E4B2F, #A67C73, #B96B4B, #C6BAA6, #D8EEF6, #F3E9D5, #F4E7A1, #F7C8D1
- `assets/diagrams/wave-01/fig-40-4-varroa-on-adult-bees.svg`: #5C2A1D, #6D4C41, #9B6414, #9E4B2F, #B96B4B, #B97714, #C89A70, #EAAE3A
- `assets/diagrams/wave-01/fig-40-7-varroa-tropilaelaps-comparison.svg`: #5C2A1D, #603226, #9E4B2F, #A95B3A, #B96B4B, #BF7654
- `assets/diagrams/wave-01/fig-40-8-tropilaelaps-life-cycle.svg`: #603226, #6D4C41, #A67C73, #A95B3A, #BF7654, #C6BAA6, #E1C8B8, #E7D9CE, #F3E9D5, #F4E7A1, #F4EFE8
- `assets/diagrams/wave-01/fig-41-1-varroa-life-cycle-worker-brood.svg`: #5C2A1D, #9E4B2F, #A67C73, #B96B4B, #C6BAA6, #D8EEF6, #F3E9D5, #F4E7A1, #F7C8D1
- `assets/diagrams/wave-01/fig-41-3-adult-bee-feeding-site.svg`: #5C2A1D, #6D4C41, #9B6414, #9E4B2F, #B96B4B, #B97714, #C89A70, #EAAE3A
- `assets/diagrams/wave-01/fig-42-1-nosema-life-cycle.svg`: #6D4C41, #726F67, #9A673A, #B96F52, #C98F4F, #E5B77D, #E8E4D8, #F8D9C5
- `assets/diagrams/wave-01/fig-42-3-healthy-vs-affected-midgut.svg`: #6D4C41, #726F67, #9A673A, #B86A8A, #B96F52, #C98F4F, #E5B77D, #E8E4D8, #F2D2C3, #F7D8C7
- `assets/diagrams/wave-01/fig-43-2-healthy-brood-vs-early-afb.svg`: #3E2B22, #5A4030, #795A43
- `assets/diagrams/wave-01/fig-43-3-disease-stage-cell-series.svg`: #4E3024, #7A3F20, #8C4A2F, #F6E7B0
- `assets/diagrams/wave-01/fig-44-2-healthy-vs-efb-open-brood.svg`: #9B5E2E, #C9893E, #D9A441
- `assets/diagrams/wave-01/fig-45-3-varroa-dwv-interaction.svg`: #5C2A1D, #6D4C41, #7B1FA2, #9E4B2F, #A67C73, #B96B4B, #C6BAA6, #D8E6EC, #F3E9D5, #F4E7A1
- `assets/diagrams/wave-01/fig-46-6-drone-brood-removal-sequence.svg`: #5C2A1D, #6D4C41, #9E4B2F, #B96B4B, #FFF3C8, #FFF8DE
- `assets/diagrams/wave-01/fig-46-9-mode-of-action-resistance-selection.svg`: #777
- `assets/diagrams/wave-02/fig-02-3-movable-frame-breakthrough.svg`: #F4E7A1, #FFFDF0
- `assets/diagrams/wave-02/fig-02-4-global-traditions.svg`: #90A4AE, #F8FBFD
- `assets/diagrams/wave-02/fig-03-2-pollination-network.svg`: #81C784, #BA68C8, #E57373, #F4C542
- `assets/diagrams/wave-02/fig-03-3-managed-vs-wild-pollinators.svg`: #6A8FB3, #7B4A7A, #7FBF6A, #9CCCE2, #D46FA8, #D98CDB, #F4C542
- `assets/diagrams/wave-02/fig-03-4-ecosystem-service-pathway.svg`: #8E63B6, #A37312, #B23A3A, #D46FA8, #D7E8A2, #E57373, #F4C542, #FFF7CC
- `assets/diagrams/wave-02/fig-04-1-hive-product-overview.svg`: #4E3224, #7A4D31, #9A6A0A, #B76E1E, #C2A85A, #D8A927, #E0A51B, #E6C6D0, #E7B438, #F4E7A1, #FFF3D1
- `assets/diagrams/wave-02/fig-04-2-product-origin-map.svg`: #7A4D31
- `assets/diagrams/wave-02/fig-05-3-traditional-vs-precision-tools.svg`: #455A64, #4E5964, #546E7A, #607D8B, #9AA5B1, #ECEFF1, #FAFAFA
- `assets/diagrams/wave-02/fig-06-1-external-worker-anatomy.svg`: #2F2B28
- `assets/diagrams/wave-02/fig-06-4-internal-systems.svg`: #B68D39, #C98F4F, #D69A5C, #E9B677
- `assets/diagrams/wave-02/fig-07-1-complete-development-cycle.svg`: #CFD8DC
- `assets/diagrams/wave-02/fig-07-2-larval-growth-feeding.svg`: #C7A94E, #E2DDD0, #FFF3D1
- `assets/diagrams/wave-02/fig-08-2-queen-reproductive-system.svg`: #AD5A7C, #C97E9D, #DDEAF8, #F7D7E2
- `assets/diagrams/wave-02/fig-08-3-mating-sperm-storage.svg`: #6FA8DC, #A9A79F, #DDEAF8, #FFFDF7
- `assets/diagrams/wave-02/fig-09-2-worker-specialised-structures.svg`: #9A6A0A, #E9B93E, #FFFBEA
- `assets/diagrams/wave-02/fig-09-3-forager-resource-types.svg`: #4E3224, #7A4D31, #90CAF9
- `assets/diagrams/wave-02/fig-10-2-drone-development.svg`: #7B563A, #D5A777, #D7AC7D
- `assets/diagrams/wave-02/fig-10-3-drone-reproductive-anatomy.svg`: #A85F4A, #A98252, #AA7047, #EAB6A6, #F0C6A2, #F6E8C6
- `assets/diagrams/wave-02/fig-11-4-alarm-recruitment-signals.svg`: #3D2E24, #D46FA8, #F4C542
- `assets/diagrams/wave-02/fig-11-5-swarm-nest-site-communication.svg`: #3D2E24, #F5D982
- `assets/diagrams/wave-02/fig-12-2-orientation-vs-robbing.svg`: #3D2E24, #81C784, #E7D48A
- `assets/diagrams/wave-02/fig-12-4-grooming-hygienic-behaviour.svg`: #7E5638, #FFF5D6
- `assets/diagrams/wave-02/fig-12-5-clustering-thermoregulation.svg`: #3D2E24
- `assets/diagrams/wave-02/fig-13-1-brood-nest-organisation.svg`: #5C3C27, #7E5638, #B66D13, #E3A62D, #F5D66B
- `assets/diagrams/wave-02/fig-13-4-resource-flow-colony.svg`: #7A4D31
- `assets/diagrams/wave-02/fig-14-1-annual-colony-population-cycle.svg`: #ECEFF1
- `assets/diagrams/wave-02/fig-15-2-good-poor-flight-paths.svg`: #3D2E24, #607D8B, #6FAE62, #9E9E9E, #ECEFF1
- `assets/diagrams/wave-02/fig-15-3-drainage-stand-placement.svg`: #3D2E24, #6B9B55, #B3E5FC, #B9D9A0
- `assets/diagrams/wave-02/fig-15-4-landscape-forage-mosaic.svg`: #3D2E24, #5B9A57, #6FAE62, #7C5A38, #7EAB62, #90A4AE, #B36DB8, #C6A22B, #D46FA8, #E6C748, #F4C542, #F5E6A9, #F8FBF4
- `assets/diagrams/wave-02/fig-16-1-small-apiary-layout.svg`: #3A2D24, #72A765, #7C5A38, #90A4AE, #CFBE9A, #D9B57C, #ECEFF1, #F8FBF4
- `assets/diagrams/wave-02/fig-16-2-growth-plan.svg`: #3A2D24, #CFBE9A, #D9B57C
- `assets/diagrams/wave-02/fig-17-1-common-movable-frame-hives.svg`: #3A2D24, #CFBE9A, #D9B57C
- `assets/diagrams/wave-02/fig-17-2-horizontal-vs-vertical-expansion.svg`: #3A2D24, #CFBE9A, #D9B57C
- `assets/diagrams/wave-02/fig-18-1-exploded-modular-hive.svg`: #3A2D24, #BFA376, #CFA46A, #CFBE9A, #D9B57C, #EEE1C6
- `assets/diagrams/wave-02/fig-18-2-frame-spacing-bee-space.svg`: #7A4D31, #D9B57C, #F4E7A1
- `assets/diagrams/wave-02/fig-18-3-floor-types.svg`: #3A2D24, #607D8B, #CFBE9A, #CFD8DC, #D9B57C
- `assets/diagrams/wave-02/fig-19-1-frame-anatomy.svg`: #9E9E9E, #D9B57C, #FFF9DE
- `assets/diagrams/wave-02/fig-19-4-straight-natural-comb.svg`: #D9B57C, #F4E7A1
- `assets/diagrams/wave-02/fig-19-5-comb-age-sequence.svg`: #76513A, #C99459, #F1D277, #FFF3B0
- `assets/diagrams/wave-02/fig-20-1-beginner-equipment-set.svg`: #455A64, #4E5964, #546E7A, #90CAF9, #A9B4BD, #F6D9BA, #F7E4A6, #FAFAFA
- `assets/diagrams/wave-03/fig-26-6-brood-nest-before-after-overfeeding.svg`: #A65C00, #B8860B, #F3C85B
- `assets/diagrams/wave-03/fig-28-1-natural-swarm-cycle.svg`: #C69C5D
- `assets/diagrams/wave-03/fig-28-3-brood-nest-restriction.svg`: #A65C00, #B8860B, #F3C85B
- `assets/diagrams/wave-03/fig-28-5-queen-cell-types.svg`: #C69C5D
- `assets/diagrams/wave-03/fig-29-1-swarm-reproductive-sequence.svg`: #C69C5D
- `assets/diagrams/wave-03/fig-29-10-installing-the-swarm.svg`: #C69C5D
- `assets/diagrams/wave-03/fig-29-15-first-inspection.svg`: #F3C85B
- `assets/diagrams/wave-03/fig-30-1-resources-required-for-a-split.svg`: #C69C5D, #F3C85B
- `assets/diagrams/wave-03/fig-30-2-donor-colony-assessment.svg`: #A65C00
- `assets/diagrams/wave-03/fig-31-2-queen-failure-vs-other-problems.svg`: #F3C85B
- `assets/diagrams/wave-03/fig-32-10-queen-cell-protection.svg`: #C69C5D
- `assets/diagrams/wave-03/fig-32-11-mating-nucleus.svg`: #C69C5D, #F3C85B
- `assets/diagrams/wave-03/fig-32-3-breeder-colony-selection.svg`: #C69C5D
- `assets/diagrams/wave-04/fig-37-1-inspection-mistakes.svg`: #FFFDF2
- … plus 16 more; full list in `assets/visual-reconciliation-pass-01.json`.
