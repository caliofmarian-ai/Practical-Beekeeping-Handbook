# Language Review — British English and Editorial Consistency

**Issue:** #105  
**Review date:** 17 September 2026  
**Authority:** `docs/standards/LANGUAGE_STYLE_SHEET.md`  
**Result:** **PASS — READY FOR FORMATTING / VISUAL PRODUCTION**

## Scope

The pass covered Chapters 1–74 plus manuscript-stage Reference Material 75–85. Source-level normalisation focused on reader-facing original prose. Exact official organisation names, publication titles, quoted text, legal titles, URLs, DOI strings and scientific names were preserved.

## Work Completed

- enforced the British-English house forms defined in the language style sheet across chapter prose;
- normalised known American forms including `organized/organize`, `analyze/analyzed`, `unlabeled`, `grayscale` and related unambiguous variants;
- preserved official spellings such as **Food and Agriculture Organization of the United Nations**, **International Organization for Standardization**, and exact source/publication titles;
- implemented Technical Review finding **T01** by explicitly adding **organic pollen** to the Chapter 70 EU organic-feed example;
- reviewed colony/hive, infection/disease, parasite/pest/pathogen and legal-jurisdiction terminology against the style sheet;
- preserved scientific names and the established 100-question chapter review structure;
- kept technical meaning unchanged.

## Source Files Changed

- `chapters/chapter-34.md`
- `chapters/chapter-35.md`
- `chapters/chapter-36.md`
- `chapters/chapter-37.md`
- `chapters/chapter-66.md`
- `chapters/chapter-70.md`
- `docs/illustration-plans/chapter-34-illustration-plan.md`

## Source-Level Replacements

Approximate British-English spelling replacements in manuscript/illustration prose: **43**.

## Residual Audit

Remaining audited American-form hits in chapter prose before References:

- None in reader-facing chapter prose for the audited forms.

Residual American spellings inside bibliographic titles, official proper names, URLs, DOI metadata or quotations are intentional and must not be Britishised.

## Findings

### BLOCKER
None.

### MAJOR
None.

### MINOR
- Technical Review T01 resolved in Chapter 70.
- Typography-dependent punctuation and displayed chapter-title dash normalisation remain assigned to Issue #106.

### EDITORIAL / LAYOUT-DEPENDENT
Deferred to layout/export:

- final em-dash normalisation in displayed chapter titles;
- curly quotation marks where supported by the typesetting engine;
- widow/orphan control and line breaks;
- page-dependent cross-references;
- final figure/table numbering after assets are placed;
- final index page locators.

## Conclusion

No known language inconsistency now changes the technical meaning of the handbook. The manuscript is **READY FOR FORMATTING / VISUAL PRODUCTION**, subject only to documented layout-dependent matters.
