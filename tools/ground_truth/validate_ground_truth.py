#!/usr/bin/env python3
"""Validate ContextForge ground-truth annotation files (Milestone 1B-3).

Checks, per annotation file under benchmarks/ground_truth/pilot/CF-*/:
- JSON Schema conformance (benchmarks/ground_truth/schemas/ground_truth.schema.json)
- duplicate node IDs
- dangling edge references (source_id/target_id must resolve to a node)
- fact source_node must resolve to a node
- document_id must match the containing CF-xxx directory
- page_number must be within the document's page_count (from corpus-v0.1.json)

Reports PASS / FAIL / WARN per file. Exit code is non-zero if any FAIL.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parents[2]
PILOT = REPO_ROOT / "benchmarks" / "ground_truth" / "pilot"
SCHEMA = REPO_ROOT / "benchmarks" / "ground_truth" / "schemas" / "ground_truth.schema.json"
MANIFEST = REPO_ROOT / "benchmarks" / "corpus" / "manifests" / "corpus-v0.1.json"

ANNOTATION_FILES = ("annotator_a.json", "annotator_b.json", "adjudicated.json")


def load_page_counts() -> dict[str, int]:
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {d["document_id"]: d.get("page_count") for d in m["documents"]}


def validate_file(path: Path, validator: Draft202012Validator,
                  page_counts: dict[str, int]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warns: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"invalid JSON: {e}"], []

    for e in sorted(validator.iter_errors(data), key=lambda x: list(x.path)):
        loc = "/".join(str(p) for p in e.path)
        errors.append(f"schema: {loc}: {e.message}")
    if errors:
        return errors, warns  # schema failures first

    doc_id = data["document_id"]
    parent = path.parent.name
    if doc_id != parent:
        errors.append(f"document_id '{doc_id}' != directory '{parent}'")

    node_ids = [n["id"] for n in data["nodes"]]
    dupes = {i for i in node_ids if node_ids.count(i) > 1}
    if dupes:
        errors.append(f"duplicate node IDs: {sorted(dupes)}")
    id_set = set(node_ids)

    for e in data["edges"]:
        if e["source_id"] not in id_set:
            errors.append(f"edge {e['id']}: dangling source_id {e['source_id']}")
        if e["target_id"] not in id_set:
            errors.append(f"edge {e['id']}: dangling target_id {e['target_id']}")

    for f in data["facts"]:
        if f["source_node"] not in id_set:
            errors.append(f"fact {f['id']}: unresolved source_node {f['source_node']}")

    pc = page_counts.get(doc_id)
    def check_page(where: str, prov: dict) -> None:
        pn = prov.get("page_number")
        if pn is None:
            warns.append(f"{where}: page_number is null (state should be 'unresolved')")
        elif isinstance(pc, int) and pn > pc:
            errors.append(f"{where}: page_number {pn} exceeds document page_count {pc}")

    for n in data["nodes"]:
        check_page(f"node {n['id']}", n["provenance"])
    for f in data["facts"]:
        check_page(f"fact {f['id']}", f["provenance"])

    return errors, warns


def main() -> int:
    if not PILOT.exists():
        print(f"no pilot directory at {PILOT}")
        return 1
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    page_counts = load_page_counts()

    total = {"PASS": 0, "FAIL": 0}
    total_warn = 0
    for doc_dir in sorted(PILOT.glob("CF-*")):
        for name in ANNOTATION_FILES:
            fp = doc_dir / name
            if not fp.exists():
                continue
            errors, warns = validate_file(fp, validator, page_counts)
            rel = fp.relative_to(REPO_ROOT)
            if errors:
                total["FAIL"] += 1
                print(f"[FAIL] {rel}")
                for e in errors:
                    print(f"        - {e}")
            else:
                total["PASS"] += 1
                print(f"[PASS] {rel}")
            for w in warns:
                total_warn += 1
                print(f"  [WARN] {rel}: {w}")

    print(f"\nSummary: PASS={total['PASS']} FAIL={total['FAIL']} WARN={total_warn}")
    return 1 if total["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
