# Practical Beekeeping Handbook — Visual Foundations v1

**Status:** Canonical for final reconciliation  
**Parent standard:** `docs/standards/VISUAL_STYLE_GUIDE.md`

## One visual system, multiple production tools

Figma, Canva, SVG generation, photography and other illustration tools are production methods only. Their visual signatures must disappear in final publication.

Every final figure belongs to **PBH-v1**, regardless of tool origin.

## Canonical typography

- Sans-serif family: `Arial, Helvetica, sans-serif`.
- Dark primary text: `#1F2933`.
- Secondary text: `#52606D`.
- Titles: bold, concise, left-aligned unless the figure family requires a centred scientific comparison.
- Labels: bold enough to survive phone and print reduction.
- Long prose inside figures should be replaced by concise labels/callouts where possible.

## Canonical semantic colour

Use `VISUAL_STYLE_GUIDE.md` as the semantic authority.

Natural biological colours are allowed where accuracy requires them. Natural colour is never recoloured merely to match brand aesthetics.

## Canvas profiles

The handbook permits a small number of **layout profiles**, not competing styles:

- `landscape-standard` — 1400×1000: general diagrams, comparisons and process figures.
- `landscape-scientific` — 1400×1050: high-fidelity scientific/diagnostic plates where extra vertical detail is justified.
- `portrait-field` — 1200×1600: field-reference/safety plates designed for vertical reading.
- custom profiles require explicit review.

These profiles may be scaled during final layout. Their internal visual grammar must remain consistent.

## Line-weight roles

Do not force one numerical stroke width across all figures. Use role-based hierarchy:

- primary structural outline — strongest line;
- secondary object/diagram outline — medium line;
- connector/arrow — medium line with consistent arrowhead family;
- detail/guide — light line;
- microscopic/anatomical detail — may be finer where accuracy requires it.

Within one figure family, equivalent roles must use equivalent apparent weight after final scaling.

## Cards and states

- process/info: blue;
- correct/healthy/released: green;
- caution/review/uncertain: orange;
- danger/prohibited/failed: red;
- diagnostic/laboratory/verification: purple;
- natural hive-product context: honey-gold/cream/brown;
- inactive/secondary: grey.

Every state also needs a non-colour cue: label, icon, border, shape, line style or position.

## Recurring masters

Do not independently redraw a recurring object when a canonical master exists. Master families include:

- HEALTHY_BROOD_REFERENCE;
- VARROA_CORE;
- BEE_CASTE_ANATOMY;
- QUEEN_CELL_FAMILY;
- HONEY_QUALITY_FAMILY;
- CLEAN_ZONE_SYSTEM;
- TRACEABILITY_CHAIN;
- WAX_SOURCE_STREAM_MASTER;
- COMB_AGE_CUTAWAY_MASTER;
- NURSE_GLAND_ROYAL_JELLY_MASTER;
- STING_VENOM_ANATOMY_MASTER.

## Accessibility metadata

Every SVG must contain:

- `role="img"`;
- `aria-labelledby="title desc"`;
- a meaningful `<title id="title">`;
- a meaningful `<desc id="desc">`;
- `data-visual-system="PBH-v1"`;
- a canvas-profile marker.

## Reconciliation principle

Automated normalisation may fix metadata, typography stacks and clearly equivalent tokens. It must **not** automatically change biological morphology, diagnostic colour, natural material colour, scale cues, fine anatomical line work or safety meaning.

Those changes require family-level editorial review.
