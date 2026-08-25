# Ground-Truth Annotation Guideline Changelog

---
title: "ContextForge — Ground-Truth Guideline Changelog"
milestone: "1B-3"
document_id: "ground_truth_guideline_changelog"
last_updated: "2026-08-25"
governs: "docs/milestone-1/04_ground_truth_annotation_guidelines.md"
---

> Change control for the annotation guidelines (guidelines §9). Each entry records
> the rule change, the reason (a pilot disagreement or a discovered ambiguity),
> and whether previously completed annotations must be re-reviewed. **Guidelines
> are not silently altered, and annotations are never silently changed to match.**

## Version history

| Guidelines version | Date | Summary |
|--------------------|------|---------|
| v0.1 | 2026-08-25 | Initial guidelines used for the pilot. |
| v0.2 (proposed) | 2026-08-25 | Adds rules GC-1…GC-10 arising from the pilot disagreements (`benchmarks/ground_truth/pilot/disagreements.json`). **Not yet applied to guidelines prose; to be folded in before full-corpus annotation (1B-3 full run).** |

## Proposed rules from the pilot (v0.2)

| ID | Rule | Origin | Re-review needed? |
|----|------|--------|-------------------|
| **GC-1** | A term/definition **glossary** with no visible ruling/gridlines is a `list` of `list_item`, not a `table`. | D-01 (CF-001) | Pilot adjudications already conform. Applies to future docs. |
| **GC-2** | A **bold run-in lead-in** that titles the paragraph it starts (e.g., "Inflation.") is a `heading` with `subtype: run_in`. | Proactive clarification (CF-001; no A/B disagreement, but ambiguous) | None. |
| **GC-3** | Encode a value's **unit verbatim**. Conversions (e.g., 100 basis points = 1 percentage point) go in `qualifier`, never by rewriting the primary `unit`/`object`. | D-02 (CF-001) | None (adjudicated conforms). |
| **GC-4** | `caption → figure` always uses **`annotates`** (required). `figure → section` may additionally use **`illustrates`**. The two are **not mutually exclusive**. | D-03 (CF-006) | None. |
| **GC-5** | A block of **monospaced source code** is a `code_block`, not `other`. | D-04 (CF-006) | None. |
| **GC-6** | A **statutory/marginal side-note** (marginal citation or flag such as "26 USC 55", "Definition.") is `other` with `subtype: margin_note`, **not** `footnote`. | D-05 (CF-012) | None. |
| **GC-7** | Numeric `object` values are normalized to **bare digits** (no grouping separators); the grouped source form is preserved in `qualifier`. Applies to fully-written numbers (e.g., $1,000,000,000). | D-07 (CF-012) | None. |
| **GC-8** | **External cross-reference targets** (whose body lies outside the document) are represented as nodes with `state: unresolved` plus the `references` edge — **not omitted**. | D-06 (CF-012) | None. |
| **GC-9** | A **caption reference list** (List of Tables/Figures/Algorithms, Table of Contents) with dot leaders and page numbers is a `list` of `list_item`, **not** a `table`, even though it looks tabular. | D-08 (CF-019), D-09 (CF-004) | None. |
| **GC-10** | **Scaled magnitudes** (thousand/million/billion/trillion) keep the scale word in `unit` (e.g., `USD_trillion`); do **not** expand to full digits, which would imply unstated precision. Contrast with GC-7, which applies to already-fully-written numbers. | D-10 (CF-004) | None. |

## Re-review determination

All pilot **adjudicated** files already apply GC-1…GC-10 (the rules were derived
during adjudication), so **no pilot annotation requires re-review**. The rules
must be folded into the guidelines prose (producing guidelines **v0.2**) and used
from the start of the full-corpus annotation run. Because these are additive
clarifications rather than reversals, they do not invalidate the pilot's
adjudicated ground truth.
