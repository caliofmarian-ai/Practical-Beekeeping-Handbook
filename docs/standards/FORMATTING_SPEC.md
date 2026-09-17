# Publication Formatting Specification — Practical Beekeeping Handbook

**Issue:** #106  
**Edition:** 2026 manuscript  
**Status:** Canonical formatting authority for pre-layout assembly

## 1. Purpose

This specification defines how the technically reviewed and language-reviewed manuscript is assembled for final visual production and export. It does not alter scientific meaning, legal wording, source titles, URLs, DOI strings, or chapter authority.

## 2. Publication Order

The final publication order is fixed by `docs/BOOK_OUTLINE.md`:

- Part I — Foundations: Chapters 1–5
- Part II — Honey Bee Biology: Chapters 6–14
- Part III — Starting an Apiary: Chapters 15–23
- Part IV — Colony Management: Chapters 24–38
- Part V — Bee Health: Chapters 39–46
- Part VI — Honey Production: Chapters 47–54
- Part VII — Other Hive Products: Chapters 55–59
- Part VIII — Beekeeping Business: Chapters 60–69
- Part IX — Sustainability: Chapters 70–74
- Reference Material: 75–85

No chapter may be silently omitted, renumbered, duplicated, or reordered during layout.

## 3. Chapter Openings

Reader-facing chapter titles use:

`Chapter 41 — Varroa Destructor`

Use an em dash in final output. Source files may retain legacy dash variants; the assembly/export stage normalises displayed headings only.

Each chapter begins on a new publication page in print/PDF output. EPUB output starts each chapter as a new semantic section.

## 4. Part Openings

Each Part receives a dedicated opening page/section with:

- Part number;
- Part title;
- chapter range;
- a short navigational subtitle only if already approved in manuscript metadata.

No decorative copy is invented during formatting.

## 5. Heading Hierarchy

- `#` — book/part/chapter opening only;
- `##` — primary chapter sections;
- `###` — secondary subsections;
- `####` — use only when technically necessary.

Do not skip heading levels for visual appearance.

## 6. Body Text

- British English follows `docs/standards/LANGUAGE_STYLE_SHEET.md`.
- Scientific names remain italicised in Markdown.
- Short safety instructions may use bold emphasis.
- Avoid all-caps body prose.
- Paragraphs remain left aligned; final typesetting may use justified text only if word spacing remains acceptable.

## 7. Lists

Bulleted and numbered lists must retain logical nesting and parallel grammar. Avoid splitting a short list across pages where the layout engine can prevent it without excessive whitespace.

## 8. Tables

Tables must:

- remain legible in greyscale;
- repeat header rows when split across print pages where the export engine supports it;
- avoid reducing body text below the minimum readable size;
- be converted to landscape or redesigned rather than compressed beyond legibility;
- retain units in headings where practical;
- keep warnings/limitations adjacent to the table they qualify.

Large reference tables may move to landscape pages or appendices while retaining cross-reference identity.

## 9. Warnings and Cautions

Use a consistent hierarchy:

- **Emergency** — immediate risk to life or severe injury;
- **Warning** — serious safety, legal, food-safety, or colony-risk consequence;
- **Caution** — important operational limitation or avoidable damage risk;
- **Note** — contextual clarification.

Do not rely on colour alone. Use text labels, icons and border/shape differences in final layout.

## 10. Figures, Diagrams and Photographs

Final artwork is governed by:

- `references/illustrations.md`;
- `references/diagrams.md`;
- `references/photographs.md`;
- per-chapter plans in `docs/illustration-plans/`.

Manuscript source retains no provisional artwork. The assembled publication source contains non-printing layout anchors identifying the chapter visual plan. Final assets are inserted only after Issues #100–#102 complete review.

## 11. Captions

Caption pattern:

`Figure 41.6 — Adult-Bee Wash Procedure. Numbered sequence showing ...`

Captions should state the instructional point, not merely repeat the image title. Technical limitations belong in the caption where omission could mislead.

## 12. Accessibility

Final visual production must:

- avoid red/green-only distinctions;
- use labels/patterns as well as colour;
- maintain sufficient contrast;
- provide meaningful alt text for digital editions;
- keep text in diagrams large enough for print;
- provide scale bars or magnification cues where scientific interpretation depends on size.

## 13. Greyscale

All diagrams and essential illustrations must remain interpretable in greyscale. Colour may enhance comprehension but must not carry the only distinction between states, categories, safe/unsafe paths, or disease features.

## 14. Units and Numbers

Follow the language style sheet:

- metric primary;
- space between number and unit: `20 °C`, `5 kg`, `3 km`;
- decimal point in English edition;
- avoid false precision.

## 15. References

Reference titles, journal titles, organisation names, legal titles, URLs and DOI strings retain their exact source spelling. Formatting may normalise punctuation and spacing but not source meaning.

## 16. Footnotes and Endnotes

Prefer inline explanatory prose where practical. Use notes only where essential to prevent interruption of the main practical sequence. Legal or scientific qualifications that materially change a decision must remain visible in the main text, not hidden in endnotes.

## 17. Equations and Calculations

Keep equations close to the worked example. Variables and units must be defined. Do not convert explanatory calculations into decorative images.

## 18. Review Questions

The established 100-question sections remain part of the manuscript. In print layout, allow multi-column treatment only if numbering order remains unambiguous and answerability is not reduced.

## 19. Page-Break Intent

The deterministic assembled source uses non-printing comments for page-break intent:

- part opening;
- chapter opening;
- reference-section opening.

The export pipeline translates these markers for PDF/print while EPUB treats them as section boundaries.

## 20. Asset Anchors

At the end of each assembled chapter, the build system inserts a non-printing anchor:

`<!-- ASSET-PLAN: docs/illustration-plans/chapter-41-illustration-plan.md -->`

This links final-layout production to the approved plan without embedding provisional art.

## 21. Front Matter

Pre-layout assembled source includes:

- title page metadata;
- edition/date;
- author credit;
- table-of-contents marker;
- publication-status notice for pre-release builds.

Final copyright, ISBN, publisher/imprint and print-manufacturing details remain release-stage metadata unless already supplied.

## 22. Back Matter

Reference Material 75–85 remains in canonical order. Final page locators in Reference 85 Index cannot be completed until final pagination is stable.

## 23. Validation Gates

Assembly must fail if any of the following occur:

- a chapter file from 1–74 is missing;
- a chapter number is duplicated or unexpected;
- a required Reference Material source is missing;
- publication order differs from the canonical map;
- an illustration-plan path is missing for a chapter;
- generated output is empty.

## 24. Export Separation

Issue #106 produces a validated publication-order Markdown source and layout rules only.

- PDF generation: Issue #107
- EPUB generation: Issue #108
- Print-ready package: Issue #109
- Final figure/diagram/photo assets: Issues #100–#102
- Final index pagination: Issue #103

## 25. Quality Principle

Formatting must never hide uncertainty, reduce warning visibility, compress tables below practical readability, or replace explanatory scientific content with decorative design. Visual polish is subordinate to technical clarity.
