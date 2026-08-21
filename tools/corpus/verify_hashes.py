#!/usr/bin/env python3
"""ContextForge corpus hash verification (Milestone 1B-2).

Checks every corpus document's local raw file against the SHA-256 recorded in the
manifest and reports one of:

    PASS      recorded hash matches the local file
    FAIL      recorded hash does NOT match the local file  (loud failure)
    MISSING   local raw file is absent (download it with download_corpus.py)
    NORECORD  manifest has no recorded sha256 yet (run ingestion with --update)

Exit code is non-zero if any FAIL is encountered, so this is CI-friendly.

Usage:
    py tools/corpus/verify_hashes.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = REPO_ROOT / "benchmarks" / "corpus" / "manifests" / "corpus-v0.1.json"
DEFAULT_RAW_DIR = REPO_ROOT / "benchmarks" / "corpus" / "raw"


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify corpus SHA-256 hashes")
    ap.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    ap.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR)
    args = ap.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    docs = manifest.get("documents", [])

    counts = {"PASS": 0, "FAIL": 0, "MISSING": 0, "NORECORD": 0}
    for doc in docs:
        doc_id = doc.get("document_id")
        fname = doc.get("local_filename") or f"{doc_id}.pdf"
        recorded = doc.get("sha256")
        path = args.raw_dir / fname

        if recorded in (None, "", "null"):
            status = "NORECORD"
        elif not path.exists():
            status = "MISSING"
        elif sha256_of_file(path) == recorded:
            status = "PASS"
        else:
            status = "FAIL"

        counts[status] += 1
        print(f"[{status:8s}] {doc_id}: {fname}")

    print("\nSummary: " + "  ".join(f"{k}={v}" for k, v in counts.items()))
    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
