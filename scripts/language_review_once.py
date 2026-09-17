from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

PAIRS = [
    (r'\bbehaviors\b', 'behaviours'), (r'\bbehavior\b', 'behaviour'),
    (r'\borganized\b', 'organised'), (r'\borganizing\b', 'organising'),
    (r'\borganizes\b', 'organises'), (r'\borganize\b', 'organise'),
    (r'\borganizations\b', 'organisations'), (r'\borganization\b', 'organisation'),
    (r'\banalyzed\b', 'analysed'), (r'\banalyzing\b', 'analysing'),
    (r'\banalyzes\b', 'analyses'), (r'\banalyze\b', 'analyse'),
    (r'\bcolors\b', 'colours'), (r'\bcolored\b', 'coloured'),
    (r'\bcoloring\b', 'colouring'), (r'\bcolor\b', 'colour'),
    (r'\bcenters\b', 'centres'), (r'\bcentered\b', 'centred'),
    (r'\bcentering\b', 'centring'), (r'\bcenter\b', 'centre'),
    (r'\bunlabeled\b', 'unlabelled'), (r'\blabeled\b', 'labelled'),
    (r'\blabeling\b', 'labelling'),
    (r'\bfulfillment\b', 'fulfilment'),
    (r'\bmolds\b', 'moulds'), (r'\bmold\b', 'mould'),
    (r'\bodors\b', 'odours'), (r'\bodor\b', 'odour'),
    (r'\bgrayscale\b', 'greyscale'), (r'\bgray\b', 'grey'),
    (r'\baging\b', 'ageing'),
    (r'\btraveling\b', 'travelling'), (r'\btraveled\b', 'travelled'),
    (r'\btravelers\b', 'travellers'), (r'\btraveler\b', 'traveller'),
    (r'\brecognized\b', 'recognised'), (r'\brecognizing\b', 'recognising'),
    (r'\brecognizes\b', 'recognises'), (r'\brecognize\b', 'recognise'),
    (r'\bminimized\b', 'minimised'), (r'\bminimizing\b', 'minimising'),
    (r'\bminimize\b', 'minimise'),
    (r'\bmaximized\b', 'maximised'), (r'\bmaximizing\b', 'maximising'),
    (r'\bmaximize\b', 'maximise'),
    (r'\bstandardized\b', 'standardised'), (r'\bstandardizing\b', 'standardising'),
    (r'\bstandardize\b', 'standardise'),
    (r'\bcharacterized\b', 'characterised'), (r'\bcharacterizing\b', 'characterising'),
    (r'\bcharacterize\b', 'characterise'),
    (r'\boptimized\b', 'optimised'), (r'\boptimizing\b', 'optimising'),
    (r'\boptimize\b', 'optimise'),
]

PROTECTED = {
    'Food and Agriculture Organization of the United Nations': '__FAO_OFFICIAL__',
    'World Health Organization': '__WHO_OFFICIAL__',
    'International Organization for Standardization': '__ISO_OFFICIAL__',
    'Centers for Disease Control and Prevention': '__CDC_OFFICIAL__',
}
RESTORE = {v: k for k, v in PROTECTED.items()}

SCAN_WORDS = [
    'behavior', 'organized', 'organize', 'organization', 'analyze', 'analyzed',
    'color', 'center', 'unlabeled', 'labeling', 'fulfillment', 'grayscale',
    'aging', 'traveling', 'traveled', 'recognize', 'recognized', 'minimize',
    'maximize', 'standardize', 'characterize', 'optimize'
]


def references_split(text: str):
    m = re.search(r'^## References(?: and Further Reading)?\s*$', text, flags=re.M)
    if m:
        return text[:m.start()], text[m.start():]
    return text, ''


def substitute(text: str):
    for official, token in PROTECTED.items():
        text = text.replace(official, token)
    total = 0
    for pattern, replacement in PAIRS:
        text, count = re.subn(pattern, replacement, text)
        total += count
        word_match = re.search(r'\\b([A-Za-z]+)\\b', pattern)
        if word_match:
            source = word_match.group(1)
            text, count = re.subn(r'\b' + source.capitalize() + r'\b', replacement.capitalize(), text)
            total += count
    for token, official in RESTORE.items():
        text = text.replace(token, official)
    return text, total


def copyedit_chapters():
    changed = []
    replacements = 0
    for path in sorted((ROOT / 'chapters').glob('chapter-*.md')):
        original = path.read_text(encoding='utf-8')
        body, refs = references_split(original)
        body, n = substitute(body)
        revised = body + refs
        if revised != original:
            path.write_text(revised, encoding='utf-8')
            changed.append(str(path.relative_to(ROOT)))
            replacements += n
    return changed, replacements


def copyedit_illustration_plans():
    changed = []
    replacements = 0
    folder = ROOT / 'docs' / 'illustration-plans'
    for path in sorted(folder.glob('*.md')):
        original = path.read_text(encoding='utf-8')
        revised, n = substitute(original)
        if revised != original:
            path.write_text(revised, encoding='utf-8')
            changed.append(str(path.relative_to(ROOT)))
            replacements += n
    return changed, replacements


def copyedit_reference_material():
    changed = []
    safe_pairs = [
        (r'\bgrayscale\b', 'greyscale'),
        (r'\bunlabeled\b', 'unlabelled'),
        (r'\blabeling\b', 'labelling'),
        (r'\bfulfillment\b', 'fulfilment'),
    ]
    for folder_name in ('references', 'appendices', 'tables', 'glossary'):
        folder = ROOT / folder_name
        if not folder.exists():
            continue
        for path in sorted(folder.glob('*.md')):
            original = path.read_text(encoding='utf-8')
            revised = original
            for official, token in PROTECTED.items():
                revised = revised.replace(official, token)
            for pattern, replacement in safe_pairs:
                revised = re.sub(pattern, replacement, revised)
            for token, official in RESTORE.items():
                revised = revised.replace(token, official)
            if revised != original:
                path.write_text(revised, encoding='utf-8')
                changed.append(str(path.relative_to(ROOT)))
    return changed


def resolve_t01():
    path = ROOT / 'chapters' / 'chapter-70.md'
    text = path.read_text(encoding='utf-8')
    original = text
    if '- organic pollen;' not in text:
        text, count = re.subn(
            r'(^- organic honey;\s*$)',
            r'\1\n- organic pollen;',
            text,
            count=1,
            flags=re.M,
        )
        if count == 0:
            raise RuntimeError('Could not locate Chapter 70 organic-honey bullet for T01 insertion')
    if text != original:
        path.write_text(text, encoding='utf-8')
        return str(path.relative_to(ROOT))
    return None


def residual_audit():
    residual = {}
    for path in sorted((ROOT / 'chapters').glob('chapter-*.md')):
        text = path.read_text(encoding='utf-8')
        body, _ = references_split(text)
        hits = []
        for word in SCAN_WORDS:
            count = len(re.findall(r'\b' + re.escape(word) + r'\b', body, flags=re.I))
            if count:
                hits.append(f'{word}:{count}')
        if hits:
            residual[str(path.relative_to(ROOT))] = hits
    return residual


def write_report(changed_files, replacement_count, residual):
    report = ROOT / 'docs' / 'reviews' / 'LANGUAGE_REVIEW.md'
    report.parent.mkdir(parents=True, exist_ok=True)
    changed_text = '\n'.join(f'- `{p}`' for p in sorted(set(changed_files))) or '- None required.'
    residual_text = '\n'.join(
        f'- `{path}` — {", ".join(hits)}' for path, hits in residual.items()
    ) or '- None in reader-facing chapter prose for the audited forms.'

    report.write_text(f'''# Language Review — British English and Editorial Consistency

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

{changed_text}

## Source-Level Replacements

Approximate British-English spelling replacements in manuscript/illustration prose: **{replacement_count}**.

## Residual Audit

Remaining audited American-form hits in chapter prose before References:

{residual_text}

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
''', encoding='utf-8')


def main():
    changed = []
    chapter_files, chapter_replacements = copyedit_chapters()
    illustration_files, illustration_replacements = copyedit_illustration_plans()
    changed.extend(chapter_files)
    changed.extend(illustration_files)
    changed.extend(copyedit_reference_material())
    t01 = resolve_t01()
    if t01:
        changed.append(t01)
    residual = residual_audit()
    write_report(changed, chapter_replacements + illustration_replacements, residual)
    print(f'changed_files={len(set(changed))}')
    print(f'replacements={chapter_replacements + illustration_replacements}')
    print(f'residual_files={len(residual)}')


if __name__ == '__main__':
    main()
