# `tools/ground_truth/` — Annotation validation & agreement tooling (1B-3)

Utilities for the ground-truth annotation pilot. Requirements: Python 3.x,
[`jsonschema`](https://pypi.org/project/jsonschema/) and
[`pypdf`](https://pypi.org/project/pypdf/) (page-count cross-check).

| Script | Purpose |
|--------|---------|
| `validate_ground_truth.py` | Validate every `benchmarks/ground_truth/pilot/CF-*/(annotator_a|annotator_b|adjudicated).json` against `benchmarks/ground_truth/schemas/ground_truth.schema.json` plus structural checks (duplicate IDs, dangling edges, unresolved fact `source_node`, `document_id` vs directory, `page_number` within the document's `page_count`). Reports PASS/FAIL/WARN; non-zero exit on any FAIL. |
| `compare_annotations.py` | Inter-annotator agreement per class: node-type Cohen's κ, structural-membership rate, reading-order Kendall's τ, relationship-edge P/R/F1, fact-tuple P/R/F1, provenance location agreement. Writes `agreement_results.json`. |

```powershell
py tools/ground_truth/validate_ground_truth.py
py tools/ground_truth/compare_annotations.py
```

**Integrity notes.** Annotations are grounded only in the source PDFs (never in any
parser/converter output). Agreement is computed from genuinely separate annotation
files. See `docs/milestone-1/05_ground_truth_pilot_report.md` for the single-agent
IAA caveat and the interpretation of these metrics.
