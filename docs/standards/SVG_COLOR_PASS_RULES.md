# SVG Semantic Colour Pass Rules

**Status:** Canonical  
**Applies to:** deterministic SVG assets and future vector diagrams.

## Objective

Upgrade monochrome figures with restrained semantic colour while preserving the existing geometry, wording, accessibility metadata, and scientific meaning.

## Version 1 rules

The first colour pass is deliberately conservative:

- white background remains white;
- body text remains near-black;
- ordinary process panels receive a light chapter-family tint;
- secondary panels receive a second light tint;
- arrows receive the chapter-family primary colour;
- warning/stop classes receive red;
- legal/verification classes receive purple;
- notes receive a light honey/cream treatment;
- hub nodes use a dark chapter-family accent;
- direct biological morphology is not recoloured unless its meaning is unambiguous.

## Chapter-family themes

- Chapters 21–23: safety — blue with green/orange/red semantic accents.
- Chapters 24–25 and 33: installation/inspection/transport — blue/green.
- Chapter 38: emergency management — orange with blue support and red stop states.
- Chapters 39–45: bee health/diagnostics — purple/blue, with red/orange only for explicit disease/risk states.
- Chapter 46: IPM — blue/green, purple verification, orange contextual thresholds.

## Never do this automatically

- recolour brood/disease morphology to look more dramatic;
- use red merely because a condition is mentioned;
- turn uncertainty into an apparent diagnosis;
- recolour Varroa/Tropilaelaps/anatomy plates without biological review;
- remove patterns, borders, icons or text cues needed for greyscale;
- introduce gradients, shadows, or decorative effects that reduce print clarity.

## Required automated checks

The colour-pass workflow must verify:
- SVG is parseable XML;
- `<title>` and `<desc>` remain present;
- no external font, raster, or web dependency is added;
- semantic-colour-pass marker is present;
- file count is unchanged;
- the visual index and manifest are regenerated from the repository state.

## Final approval

Automated colour pass is **not** final art approval. Each figure remains subject to:
- scientific/mechanical review;
- safety/legal review;
- greyscale/final-size proof;
- accessibility/alt-text review;
- commercial-rights/provenance review;
- final PDF/EPUB/print proof.
