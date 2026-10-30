# Narrative Review — Wave 01 (Chapters 1–5)

**Issue:** #228  
**Branch:** `editorial/narrative-wave-01-ch01-05`  
**Status:** FIRST NARRATIVE PASS COMPLETE — OWNER/PR REVIEW PENDING

## Editorial objective

Convert Chapters 1–5 from outline-heavy instructional drafts into developed book prose without weakening science, practical value, safety, source traceability, or useful field checklists.

The accepted model is now defined in `docs/standards/WRITING_STANDARDS.md` as **narrative-first**:
- explain what the subject is;
- explain how it works;
- explain why it matters;
- connect it to field observation or action;
- state important limits and context;
- use lists as supplements, not substitutes for explanation.

## Quantitative change

| Chapter | Main words | Revised words | Main bullet lines | Revised bullet lines |
|---|---:|---:|---:|---:|
| 1 — Introduction to Beekeeping | 5,133 | 7,490 | 453 | 78 |
| 2 — History of Beekeeping | 7,203 | 8,375 | 379 | 169 |
| 3 — Importance of Honey Bees | 6,546 | 6,704 | 419 | 178 |
| 4 — Products of the Hive | 7,426 | 7,701 | 369 | 111 |
| 5 — Modern Beekeeping | 2,895 | 3,944 | 166 | 25 |
| **Total** | **29,203** | **34,214** | **1,786** | **561** |

The word-count increase is about 17%, while bullet-line dependence fell by about 69%. This is not a word-count target; it is evidence that explanation replaced outline structure rather than merely adding filler.

## Chapter ownership and duplication control

To prevent the book from repeating the same lesson in several chapters, Wave 01 assigns a primary home to overlapping subjects:

| Subject | Primary chapter in Wave 01 | Treatment elsewhere |
|---|---|---|
| beginner mindset, observation before intervention, responsibility | Chapter 1 | short references only |
| historical development of hives, frames and apicultural knowledge | Chapter 2 | Chapter 5 states the management consequence, not the history |
| pollination biology, pollinator diversity, pollination contracts | Chapter 3 | Chapter 5 handles only operational/logistics consequences |
| biological origin, quality and risks of hive products | Chapter 4 | Chapter 1 gives only the beginner welfare principle; Chapter 5 defers product detail |
| standardisation, preventive systems, IPM concept, mechanisation, sensors and scalable management | Chapter 5 | detailed procedures remain in later specialist chapters |
| records and traceability | Chapters 36 and 67 (full treatment later) | Chapters 1 and 5 establish only the management principle |

## Cross-chapter similarity audit

A paragraph-level similarity pass was run after revision. The high-overlap cases initially found were reduced by replacing duplicate explanations with chapter ownership and cross-references.

Two intentional overlaps remain:
1. **Colony food before harvest** — Chapter 1 states the welfare principle; Chapter 4 applies it to honey harvest.
2. **Severe sting/anaphylaxis symptoms** — safety-critical emergency wording is repeated briefly where venom is discussed.

These are retained intentionally because the project standard allows concise repetition when immediate welfare or safety decisions depend on it.

No exact duplicate explanatory paragraph remains across Chapters 1–5.

## Narrative decisions by chapter

### Chapter 1
Expanded the foundational narrative around the colony as a living system, observation, responsibility, realistic expectations, site/capacity planning, ethics and decision-making. Checklists remain because they serve field readiness.

### Chapter 2
Converted long descriptive inventories into historical explanation and cause/effect. Preserved the evidence table and timeline as appropriate reference structures. Removed modern sensor detail that belongs to Chapter 5.

### Chapter 3
Developed pollination concepts, crop dependence, pollinator complementarity, measurement, food-security context and conservation limits. Retained practical assessment/checklist sections.

### Chapter 4
Developed the biology, handling logic and risk boundaries for honey, beeswax, propolis, pollen, royal jelly and venom. Preserved processing/traceability checklists where scanning is more useful than prose.

### Chapter 5
Rewritten around what is uniquely modern: system design, standardisation, preventive management, IPM, scaling, mechanisation, data and digital tools. Explicitly defers history to Chapter 2, pollination to Chapter 3, hive-product detail to Chapter 4, inspections to later chapters, records to Chapter 36 and traceability to Chapter 67.

## Safety and evidence boundary

Narrative revision did not authorise new treatments, disease thresholds, legal claims, or medical advice. Existing safety boundaries and references were preserved. Safety-critical material may be repeated concisely even when a related explanation appears elsewhere.

## Next editorial step

Before scaling the model to Chapters 6–74:
1. run repository/build validation on this wave;
2. review the actual diff and resolve any science/cross-reference regression;
3. rebuild the reader manuscript from the revised source;
4. obtain owner approval of the Wave 01 writing style;
5. apply the same ownership/duplication audit to each subsequent wave.

**Narrative status:** Chapters 1–5 first pass complete; not yet final publication sign-off.
