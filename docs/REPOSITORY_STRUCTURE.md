# Repository Structure

## Purpose

This document defines the official repository structure for the Practical Beekeeping Handbook.

The structure is designed to support:

- professional book development;
- scientific and editorial review;
- original illustrations and photographs;
- print, PDF, EPUB, and Kindle production;
- long-term maintenance and version control.

---

## Official Directory Structure

Practical-Beekeeping-Handbook/
├── README.md
├── START-HERE.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── chapters/
├── assets/
│   ├── illustrations/
│   ├── photographs/
│   ├── diagrams/
│   └── covers/
├── appendices/
├── bibliography/
├── case-studies/
├── checklists/
├── docs/
│   ├── BOOK_OUTLINE.md
│   ├── REPOSITORY_STRUCTURE.md
│   └── standards/
├── drafts/
├── exports/
│   ├── pdf/
│   ├── epub/
│   ├── print/
│   └── kindle/
├── glossary/
├── notes/
├── quizzes/
├── references/
├── scripts/
├── tables/
└── templates/

---

## Directory Responsibilities

### chapters/

Contains the official manuscript chapters.

Official filename format:

- chapter-01.md
- chapter-02.md
- chapter-03.md

Chapter numbers must match the official order in docs/BOOK_OUTLINE.md.

### assets/illustrations/

Contains original professional illustrations used in the handbook.

Official filename format:

- chapter-01-figure-01.png
- chapter-01-figure-02.png

### assets/photographs/

Contains photographs that are original, licensed, public domain, or otherwise approved for publication.

Each photograph must have documented:

- creator or source;
- licence;
- date accessed, where applicable;
- chapter and figure number;
- caption;
- alt text.

### assets/diagrams/

Contains professional diagrams and infographics.

ASCII diagrams are not permitted in the final manuscript.

### appendices/

Contains supplementary technical information that would interrupt the main chapters.

### bibliography/

Contains the consolidated bibliography for the complete handbook.

### case-studies/

Contains practical examples and documented beekeeping scenarios.

### checklists/

Contains reusable operational checklists for inspections, feeding, harvesting, disease control, equipment preparation, and other practical tasks.

### docs/

Contains the official project plan, repository rules, book outline, and editorial standards.

### drafts/

Contains temporary working material that is not yet approved for inclusion in the manuscript.

Draft material must never be treated as final publication content.

### exports/

Contains generated publication files.

Source manuscript files must not be edited inside this directory.

### glossary/

Contains approved definitions of beekeeping terminology.

### notes/

Contains research notes, editorial notes, and unresolved questions.

### quizzes/

Contains optional educational review questions.

### references/

Contains chapter-specific sources, research papers, official guidance, and source records.

### scripts/

Contains automation used for validation, export, file checks, or publication builds.

### tables/

Contains complex reusable tables that are maintained separately from chapter files.

### templates/

Contains standard templates for chapters, figures, tables, checklists, references, and review records.

---

## Official Chapter Structure

Each manuscript chapter should contain, where relevant:

1. Chapter title
2. Learning objectives
3. Introduction
4. Main technical sections
5. Practical guidance
6. Safety notes
7. Tables
8. Figure placeholders
9. Practical checklist
10. Chapter summary
11. References and further reading

Not every chapter requires every element, but omissions must be appropriate to the subject.

---

## Figure Policy

During manuscript development, figures are represented by professional placeholders.

Example:

> **Figure 6.1 — External anatomy of a worker honey bee.**
> *Professional illustration to be added during the illustration and layout stage.*

Rules:

- Do not use ASCII drawings.
- Do not insert provisional low-quality artwork.
- Every figure must have a unique number.
- Every figure must be mentioned in the chapter text.
- All final illustrations must use a consistent visual style.
- Final figures must include captions and accessible alt text.
- Scientific structures and labels must be reviewed before publication.

---

## Naming Rules

Use lowercase filenames for manuscript and project documents where practical.

Approved chapter format:

- chapter-01.md

Approved illustration format:

- chapter-01-figure-01.png

Approved table format:

- chapter-01-table-01.md

Approved checklist format:

- chapter-01-checklist-01.md

Do not maintain two competing filename systems.

---

## Editorial Rules

All handbook content must be:

- original;
- accurate;
- practical;
- clearly structured;
- scientifically supportable;
- properly referenced;
- internally consistent;
- written in professional English;
- suitable for digital and print publication.

Content must not be duplicated across chapters unless a short cross-reference is necessary.

Terminology must remain consistent throughout the book.

---

## Workflow

Each issue follows this sequence:

Backlog → In Progress → Drafting → Review → Done

Before an issue is marked complete:

- the relevant repository files must exist;
- filenames must follow the official convention;
- content must meet the editorial standards;
- links and paths must be valid;
- duplicated or contradictory content must be removed;
- figure placeholders must be correctly numbered;
- references must be recorded;
- the result must be committed and pushed to GitHub.

---

## Publication Readiness

The repository must support:

- editable Markdown source;
- professional PDF export;
- print-ready edition;
- EPUB edition;
- Kindle-compatible edition;
- future revisions and translated editions.

The Markdown manuscript remains the canonical source.
