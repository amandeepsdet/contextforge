#!/usr/bin/env python3
"""Generate corpus-v0.1 coverage matrices and summary from the manifest.

Deterministic, documented derivations from the (verified) manifest. Outputs:
- fidelity_coverage_matrix.csv   (0/1/2 coverage per fidelity dimension)
- difficulty_matrix.csv          (categorical difficulty factors)
- adversarial_coverage.json      (adversarial pattern -> [document_ids])
- corpus-v0.1.md                 (human-readable summary + balance stats)

These are CORPUS COVERAGE METADATA, not benchmark accuracy. Values describe how
strongly a document is expected to exercise a dimension, derived from manifest
tags by the documented rules below.
"""
from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MAN_DIR = REPO_ROOT / "benchmarks" / "corpus" / "manifests"
MANIFEST = MAN_DIR / "corpus-v0.1.json"

DIM_COLS = [
    ("content", "content_fidelity"),
    ("structure", "structural_fidelity"),
    ("layout", "layout_fidelity"),
    ("relationship", "relationship_fidelity"),
    ("semantic", "semantic_fidelity"),
    ("provenance", "provenance_fidelity"),
    ("answerability", "ai_answerability"),
]

AP_NAMES = {
    "AP-01": "Multi-column reading-order", "AP-02": "Multi-page table continuation",
    "AP-03": "Nested/merged table headers", "AP-04": "Chart + table relationship",
    "AP-05": "Figure + caption", "AP-06": "Footnote association",
    "AP-07": "Repeated headers/footers", "AP-08": "Semantic duplication",
    "AP-09": "Cross-page references", "AP-10": "Units and percentages",
    "AP-11": "Financial tables with totals", "AP-12": "Text boxes / floating elements",
    "AP-13": "Mixed-orientation pages", "AP-14": "Scanned pages",
    "AP-15": "Diagram / architecture relationships",
}


def cov_value(dim: str, dims: list[str], difficulty: str) -> int:
    if dim not in dims:
        return 0
    return 2 if difficulty in ("hard", "adversarial") else 1


def cat(tags: set[str], high: set[str], medium: set[str], default: str = "none") -> str:
    if tags & high:
        return "high"
    if tags & medium:
        return "medium"
    return default


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    docs = manifest["documents"]

    # fidelity coverage matrix
    with (MAN_DIR / "fidelity_coverage_matrix.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["document_id"] + [c for _, c in DIM_COLS])
        for d in docs:
            dims = d.get("fidelity_dimensions", [])
            diff = d.get("difficulty", "medium")
            w.writerow([d["document_id"]] + [cov_value(k, dims, diff) for k, _ in DIM_COLS])

    # difficulty matrix
    with (MAN_DIR / "difficulty_matrix.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["document_id", "page_count", "table_complexity", "chart_complexity",
                    "layout_complexity", "ocr_required", "relationship_complexity",
                    "semantic_complexity", "overall_difficulty"])
        for d in docs:
            t = set(d.get("difficulty_tags", []))
            table = cat(t, {"dense_financial_tables", "multi_page_tables", "merged_headers", "merged_cells"},
                        {"financial_tables", "tables", "boxes", "line_item_totals", "schedules",
                         "form_fields", "repeated_form_grid", "worksheets"})
            chart = cat(t, {"chart_dense"}, {"charts", "chart_table_relationship"})
            layout = cat(t, {"infographics", "landscape_tables", "multi_column"},
                         {"two_column", "boxes", "callouts", "spatial_grouping", "flow_diagrams", "TOC"},
                         default="low")
            ocr = "yes" if d.get("native_or_scanned") == "scanned" else "no"
            rel = cat(t, {"cross_references"},
                      {"figures", "captions", "references", "chart_table_relationship",
                       "defined_terms", "flow_diagrams"}, default="low")
            sem = cat(t, {"percentage_points", "defined_terms", "narrative_number_relationships"},
                      {"totals", "line_item_totals", "formulas", "financial_line_items"}, default="low")
            w.writerow([d["document_id"], d.get("page_count"), table, chart, layout, ocr,
                        rel, sem, d.get("difficulty")])

    # adversarial coverage
    ap_map: dict[str, list[str]] = defaultdict(list)
    for d in docs:
        for ap in d.get("adversarial_patterns", []):
            ap_map[ap].append(d["document_id"])
    coverage = {ap: {"name": AP_NAMES[ap], "documents": sorted(ap_map.get(ap, []))}
                for ap in sorted(AP_NAMES)}
    (MAN_DIR / "adversarial_coverage.json").write_text(
        json.dumps(coverage, indent=2) + "\n", encoding="utf-8")

    covered = [ap for ap in AP_NAMES if ap_map.get(ap)]
    uncovered = [ap for ap in AP_NAMES if not ap_map.get(ap)]

    # balance stats
    by_cat = Counter(d["category"] for d in docs)
    by_lang = Counter(d["language"] for d in docs)
    by_ns = Counter(d["native_or_scanned"] for d in docs)
    by_diff = Counter(d["difficulty"] for d in docs)
    redis = Counter("redistributable" if d["redistributable"] else "reference-only" for d in docs)
    pages = [d["page_count"] for d in docs if isinstance(d.get("page_count"), int)]
    buckets = Counter()
    for p in pages:
        buckets["1-5" if p <= 5 else "6-20" if p <= 20 else "21-100" if p <= 100 else ">100"] += 1

    # human summary
    lines = [f"# ContextForge Corpus v0.1 - summary (generated)\n",
             f"Total documents: **{len(docs)}**\n",
             "> Generated by tools/corpus/build_matrices.py from corpus-v0.1.json. Do not edit by hand.\n",
             "## Category distribution", ""]
    for k, v in sorted(by_cat.items()):
        lines.append(f"- {k}: {v}")
    lines += ["", "## Language distribution"] + [f"- {k}: {v}" for k, v in sorted(by_lang.items())]
    lines += ["", "## Native vs scanned"] + [f"- {k}: {v}" for k, v in sorted(by_ns.items())]
    lines += ["", "## Difficulty distribution"] + [f"- {k}: {v}" for k, v in sorted(by_diff.items())]
    lines += ["", "## Redistribution"] + [f"- {k}: {v}" for k, v in sorted(redis.items())]
    lines += ["", "## Page-count buckets"] + [f"- {k}: {v}" for k, v in sorted(buckets.items())]
    lines += ["", "## Adversarial coverage (AP-01..AP-15)", ""]
    for ap in sorted(AP_NAMES):
        ds = ", ".join(sorted(ap_map.get(ap, []))) or "**NONE - GAP**"
        lines.append(f"- {ap} {AP_NAMES[ap]}: {ds}")
    lines += ["", f"Covered patterns: {len(covered)}/15. Uncovered: {', '.join(uncovered) or 'none'}.", ""]
    (MAN_DIR / "corpus-v0.1.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # console summary
    print(f"documents={len(docs)}")
    print("category:", dict(sorted(by_cat.items())))
    print("language:", dict(by_lang))
    print("native/scanned:", dict(by_ns))
    print("difficulty:", dict(by_diff))
    print("redistribution:", dict(redis))
    print("page buckets:", dict(buckets))
    print(f"adversarial covered={len(covered)}/15 uncovered={uncovered}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
