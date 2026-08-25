# Ground-Truth Pilot — Document Selection (Milestone 1B-3)

---
title: "ContextForge — Ground-Truth Pilot Selection"
milestone: "1B-3"
document_id: "04_ground_truth_pilot_selection"
status: "pilot (5 documents) — validates schema/guidelines before full-corpus annotation"
version: "0.1.0"
last_updated: "2026-08-25"
depends_on:
  - "01_document_fidelity_model.md (1A, frozen)"
  - "02_benchmark_spec.md (1B-1, frozen)"
  - "03_corpus_construction_report.md (1B-2)"
  - "benchmarks/corpus/manifests/corpus-v0.1.json"
---

> **Scope.** Five documents were selected from `corpus-v0.1` for the ground-truth
> **pilot**. The pilot validates the annotation schema, guidelines, tooling, and
> inter-annotator agreement **before** annotating the remaining 25 documents. It
> does **not** annotate the whole corpus, build questions, or run any baseline.

## Selection method

Documents were chosen from the verified corpus manifest and coverage matrices to
**maximize category and fidelity-dimension diversity** while covering the hardest
structural/semantic relationships. Each selection cites its actual manifest
metadata (category, `fidelity_dimensions`, `adversarial_patterns`, difficulty).

Because full-document annotation is impractical for a pilot (1B-3 §14), each
document is annotated over a defined **pilot slice** (specific pages) chosen to
contain the structures that stress the target dimensions. Slices are recorded in
each annotation file (`pilot_slice`) and below.

## Selected documents

| Slot | ID | Category | Difficulty | Pilot slice (PDF pages) | Why selected |
|------|----|----------|-----------|--------------------------|--------------|
| A — Financial | **CF-001** | financial_annual_report | hard | 9–12 | Abbreviations list, summary headings, `%`/basis-point semantics, a cross-reference to a named box |
| B — Research | **CF-006** | research_paper | medium | 1–4 | Title/authors/abstract, section headings, bullet list, code block, **Figure 1 + caption**, references to Fig. 1 and Table 1 |
| C — Legal | **CF-012** | legal_statute | hard | 2–4 | Deep hierarchy (Title→Subtitle→Section→subsection), **defined terms**, statutory **cross-references**, margin notes, repeated furniture |
| D — Technical | **CF-019** | technical_document | medium | 6–9 | TOC, **List of Tables / Figures / Algorithms** (caption relationships), section hierarchy, cross-references, facts |
| E — Adversarial / relationship-heavy | **CF-004** | financial_annual_report | hard | 1, 3, 5, 6 | TOC + **List of Statistical Tables** (each entry references a table + page), dense-table document, financial facts with `%` |

### Per-document rationale (from manifest metadata)

- **CF-001** — *Monetary Policy Report, Feb 2025.* `fidelity_dimensions`:
  content, structure, layout, relationship, semantic, provenance.
  `adversarial_patterns`: AP-04, AP-10, AP-11, AP-07, AP-13. Stresses **semantic**
  fidelity (percent vs basis points), **relationship** (cross-reference to a box),
  and provenance. Slice avoids deep tables to keep the pilot tractable while still
  exercising facts and a `references` edge.
- **CF-006** — *Docling Technical Report* (CC BY 4.0). `adversarial_patterns`:
  AP-01, AP-05, AP-09. The strongest clean **figure↔caption** (`annotates`) and
  **cross-reference** (`references` to Fig. 1 / Table 1) case; also a code block
  and bullet list for node-type diversity.
- **CF-012** — *Inflation Reduction Act* (public law). AP-06, AP-08, AP-09.
  Deep **structural hierarchy** and statutory **cross-references** (e.g., "section
  55(b)", "26 USC 55" margin note) — the hardest structure/relationship case.
- **CF-019** — *NIST FIPS 197 (AES)*. AP-15, AP-03. Explicit **List of Tables /
  Figures / Algorithms** gives unambiguous caption/`illustrates` relationships and
  many cross-references; good for structure + relationship + provenance.
- **CF-004** — *IRS Data Book*. AP-02, AP-03, AP-11, AP-07. **Relationship-heavy**
  table-of-tables: each list item in "List of Statistical Tables" `references` a
  specific table on a specific page — a dense `references`/provenance test — plus
  financial facts (`$5.3 trillion`, `271.4 million returns`, `up 9 percent`).

## Diversity check

| Axis | Coverage across the 5 pilot docs |
|------|----------------------------------|
| Categories | financial (CF-001, CF-004), research (CF-006), legal (CF-012), technical (CF-019) |
| Fidelity dimensions | all 7 exercised (content/structure/layout/relationship/semantic/provenance; answerability supported by facts+provenance) |
| Adversarial patterns | AP-01, AP-02, AP-03, AP-04, AP-05, AP-06, AP-07, AP-08, AP-09, AP-10, AP-11, AP-13, AP-15 |
| Node-type variety | headings, paragraphs, lists/list-items, tables, figures, captions, footnotes/margin-notes, equations, code block |
| Relationship variety | contains, follows, references, illustrates/annotates, cites, belongs_to, continues |
| Redistributability | 4 public domain + 1 CC BY (all freely obtainable) |

> **Gaps carried from corpus-v0.1 (not blockers, per 1B-3 §18):** no scanned
> document (AP-14) and no non-English document are in the corpus yet; these belong
> to **corpus-v0.1.1** and will be annotated with the stabilized pilot guidelines.
