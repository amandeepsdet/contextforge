# Ground-Truth Annotation Pilot — Report (Milestone 1B-3)

---
title: "ContextForge — Ground-Truth Pilot Report"
milestone: "1B-3"
document_id: "05_ground_truth_pilot_report"
status: "pilot complete (5 documents) — full-corpus annotation NOT started"
version: "0.1.0"
last_updated: "2026-08-25"
depends_on:
  - "04_ground_truth_pilot_selection.md"
  - "04_ground_truth_annotation_guidelines.md"
  - "benchmarks/ground_truth/schemas/ground_truth.schema.json"
  - "benchmarks/ground_truth/pilot/*"
---

> **Bottom line.** The schema, guidelines, tooling, and adjudication workflow are
> **validated** on 5 diverse documents. Structural membership, reading order, and
> provenance agreement were perfect; **node-type**, **relationship-edge**, and
> **fact-normalization** disagreements were concentrated in a small number of
> genuinely ambiguous constructs, which produced 10 guideline rules (GC-1…GC-10)
> now ready to fold in before full-corpus annotation.

> **IAA interpretation caveat (important).** Both annotation passes
> (`annotator_a`, `annotator_b`) were produced by a **single AI agent in two
> independent passes**, not by two humans. Agreement here therefore measures
> **schema/guideline robustness and construct ambiguity**, *not* human annotator
> reliability. Real human double-annotation (with the stabilized v0.2 guidelines)
> is required before the numbers can be read as inter-annotator reliability. This
> is stated so the metrics are not over-interpreted.

## 1. Selected documents

| ID | Category | Slice (pages) | Key structures exercised |
|----|----------|---------------|--------------------------|
| CF-001 | financial | 9–12 | glossary, run-in headings, `%`/basis-point facts, box cross-reference |
| CF-006 | research | 1–4 | title/abstract, bullet list, code block, figure+caption, Fig./Table references |
| CF-012 | legal | 2–4 | Title/Subtitle/Section hierarchy, defined term, statutory cross-reference, margin notes |
| CF-019 | technical | 6–9 | TOC, List of Tables/Figures (reference lists), AES facts |
| CF-004 | financial (adversarial) | 1,3,5,6 | Contents, List of Statistical Tables, `$`-scaled + `%` facts |

Rationale: [04_ground_truth_pilot_selection.md](04_ground_truth_pilot_selection.md).

## 2. Annotation counts

| Document | Nodes (A / B / adj) | Edges (A / B) | Facts (A / B) |
|----------|---------------------|---------------|---------------|
| CF-001 | 19 / 19 / 19 | 10 / 10 | 6 / 6 |
| CF-006 | 19 / 19 / 18 | 9 / 9 | 4 / 4 |
| CF-012 | 14 / 13 / 13 | 10 / 9 | 4 / 4 |
| CF-019 | 14 / 14 / 14 | 10 / 10 | 3 / 3 |
| CF-004 | 13 / 13 / 13 | 9 / 9 | 4 / 4 |
| **Total** | **79 / 78 / 77** | **48 / 47** | **21 / 21** |

Total annotation items compared (A+B) = 79+78 nodes + 48+47 edges + 21+21 facts
= **294**.

## 3. Agreement metrics (per class)

Computed by `tools/ground_truth/compare_annotations.py`
([agreement_results.json](../../benchmarks/ground_truth/pilot/agreement_results.json)).
Node alignment is anchor-based (page + fuzzy `text_anchor`), independent of IDs.

| Document | node-type κ | node raw | membership | reading-order τ | edge F1 | fact F1 | provenance |
|----------|:----------:|:--------:|:----------:|:---------------:|:-------:|:-------:|:----------:|
| CF-001 | 0.72 | 0.79 | 1.00 | 1.00 | 1.00 | 0.83 | 1.00 |
| CF-004 | 0.72 | 0.77 | 1.00 | 1.00 | 1.00 | 0.75 | 1.00 |
| CF-006 | 0.93 | 0.95 | 1.00 | 1.00 | 0.75 | 1.00 | 1.00 |
| CF-012 | 0.78 | 0.85 | 1.00 | 1.00 | 0.80 | 0.50 | 1.00 |
| CF-019 | 0.73 | 0.79 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| **mean** | **0.78** | **0.83** | **1.00** | **1.00** | **0.91** | **0.82** | **1.00** |

**Metric choice per class** (1B-3 §8): Cohen's κ for node type (categorical);
raw agreement rate for structural membership; Kendall's τ for reading order;
precision/recall/F1 for relationship edges and for fact tuples; page+anchor
location-agreement rate for provenance.

**Reading of the numbers.** Structure (membership), order (τ), and provenance are
perfect because both passes read the same source and the guidelines pin those
choices well. The **spread is in node type and facts**, exactly where the
constructs are ambiguous (list vs table; unit normalization) — the intended
pilot signal.

## 4. Disagreement analysis

[disagreements.json](../../benchmarks/ground_truth/pilot/disagreements.json) records
10 material disagreement groups (19 individual items):

| Class | Count (items) | Examples |
|-------|:-------------:|----------|
| node type | 13 | glossary list↔table (D-01), List-of-Tables list↔table (D-08, D-09), code_block↔other (D-04), margin_note↔footnote (D-05) |
| relationship edge | 2 | caption `annotates`↔figure `illustrates` (D-03); external cross-reference kept↔omitted (D-06) |
| fact | 4 | basis_points↔percent (D-02), separators↔bare digits (D-07 ×2), trillion scale↔expanded (D-10) |

- **Disagreements per 100 annotations:** 19 / 294 ≈ **6.5**.
- **Top disagreement class:** `schema_ambiguity` (7 of 10 groups) — dominated by
  the **list-vs-table** ambiguity for term/definition and caption-reference lists.
- **No** `annotation_error`, `provenance_ambiguity`, or `source_document_ambiguity`
  disagreements were observed in the pilot.

## 5. Adjudication outcomes

Every disagreement was adjudicated (canonical files:
`benchmarks/ground_truth/pilot/CF-*/adjudicated.json`) and produced a guideline
rule:

| Disagreement | Adjudicated result | Rule |
|--------------|--------------------|------|
| glossary / caption-reference lists as table | → **list** | GC-1, GC-9 |
| basis points / trillion scaling | → **keep stated unit/scale**, conversions in `qualifier` | GC-3, GC-10 |
| caption vs figure→section | → **keep both** (`annotates` + `illustrates`) | GC-4 |
| code as `other` | → **`code_block`** | GC-5 |
| margin note as footnote | → **`other`/`margin_note`** | GC-6 |
| grouped numbers | → **bare digits** in `object` | GC-7 |
| external cross-reference omitted | → **node with `state: unresolved`** + edge | GC-8 |

Full rationale and re-review determination:
[ground_truth_guideline_changelog.md](ground_truth_guideline_changelog.md).
Because the rules were derived during adjudication, **no pilot annotation needs
re-review**; the rules are additive and must be folded into guidelines **v0.2**.

## 6. Schema problems

- **None structural.** All 15 files pass
  `tools/ground_truth/validate_ground_truth.py` (**PASS=15, FAIL=0, WARN=0**):
  schema conformance, unique node IDs, resolvable edge/fact references, matching
  `document_id`, and in-range `page_number`.
- **Observations (not failures):** margin notes and code were representable only
  via `other` + `subtype` until GC-5/GC-6 clarified usage; a future schema version
  may promote `margin_note` to a first-class enum value. The 1B-1 §6.1 `Block`
  type was unused (blocks were annotated as `paragraph`/`other`), which is
  acceptable but should be documented in the schema notes.

## 7. Guideline problems (resolved → v0.2)

The pilot surfaced ambiguity in: list-vs-table classification (GC-1, GC-9),
run-in headings (GC-2), unit/number normalization (GC-3, GC-7, GC-10),
caption/figure edges (GC-4), code blocks (GC-5), margin notes (GC-6), and
external cross-reference handling (GC-8). All are now written as GC-1…GC-10.

## 8. Unresolved ambiguity / limitations

1. **Single-agent IAA caveat** (see header) — the headline limitation; real human
   double-annotation is required.
2. **No bounding boxes.** The pilot used `bbox: null` throughout and relied on
   `page_number` + `text_anchor`. A policy for capturing reliable coordinates
   (and whether spatial/L3 questions need them) is still open.
3. **Alignment tooling.** Anchor-based alignment required giving container nodes
   distinct multi-entry anchors to avoid parent/child collisions; a future version
   should either use shared stable node IDs or a more robust matcher.
4. **Scope.** Each document was annotated over a **pilot slice**, not end-to-end.

## 9. Pilot quality metrics (summary)

| Metric | Value |
|--------|-------|
| Documents annotated (double + adjudicated) | 5 |
| Nodes / edges / facts per document (A, mean) | 15.8 / 9.6 / 4.2 |
| Node-type κ (mean) | 0.78 |
| Relationship-edge F1 (mean) | 0.91 |
| Fact F1 (mean) | 0.82 |
| Membership / reading-order / provenance agreement | 1.00 / 1.00 / 1.00 |
| Material disagreements per 100 annotations | ≈ 6.5 |
| Schema validation pass rate | 15/15 (100%) |

No single aggregate agreement score is reported: the classes measure different
things and are not meaningfully averaged into one number (1B-3 §13).

## 10. Future L1–L7 question support (spot check)

The adjudicated ground truth already supports example questions without further
annotation:

- **L1 (direct):** "What was the PCE inflation rate?" → CF-001/f1 (2.6%, 12-month).
- **L2 (structural):** "Which section discusses the AES key expansion?" → CF-019 TOC entry.
- **L4 (relational):** "Which figure corresponds to Docling's pipeline description?" → CF-006 `references`/`annotates` on fig1.
- **L5 (semantic):** "Did the Fed cut rates by 100 basis points or 1 percentage point?" → CF-001/f5 (unit-faithful).
- **L7 (provenance):** "What page states the $5.3 trillion figure?" → CF-004/f1 provenance (page 5).

## 11. Corpus-v0.1 gaps (carried, not blockers)

Per 1B-3 §18: the pilot runs on `corpus-v0.1`, which has **no scanned document
(AP-14)** and **no non-English document**. These belong to **corpus-v0.1.1** and
will be annotated with the stabilized v0.2 guidelines. They do not block the pilot.

## 12. What must be fixed before full-corpus annotation

1. **Fold GC-1…GC-10 into guidelines v0.2** and re-issue.
2. **Use ≥2 genuinely independent human annotators** (removes the single-agent
   caveat; the current numbers are optimistic).
3. **Decide the bbox/coordinate policy** for provenance and L3 spatial questions.
4. **Harden the alignment tool** (shared stable IDs or a stronger matcher).
5. **Add corpus-v0.1.1** (scanned + non-English) before or alongside the full run.

---

### Reproduce

```powershell
py tools/ground_truth/validate_ground_truth.py     # PASS=15
py tools/ground_truth/compare_annotations.py        # writes agreement_results.json
```

No competitor baseline was run; no L1–L7 question set was built; Milestone 1C has
not started.
