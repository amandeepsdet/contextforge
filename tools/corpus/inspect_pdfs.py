#!/usr/bin/env python3
"""One-off QA probe for corpus-v0.1 (Milestone 1B-2 source QA).

Objectively inspects each downloaded raw PDF to support (not replace) manual QA:
- extractable text density on the first pages  -> flags likely-scanned documents
- count of landscape pages                     -> evidence for AP-13 (mixed orientation)
- a short title snippet from page 1            -> sanity-check the file is what we think
- duplicate SHA-256 across the corpus

This does not modify the manifest; it prints findings for review and for the
corpus construction report.
"""
from __future__ import annotations

import json
from pathlib import Path

from pypdf import PdfReader

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST = REPO_ROOT / "benchmarks" / "corpus" / "manifests" / "corpus-v0.1.json"
RAW = REPO_ROOT / "benchmarks" / "corpus" / "raw"

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
seen: dict[str, str] = {}

print(f"{'ID':7s} {'pages':>5s} {'land':>4s} {'txt/pg':>7s}  scanned?  title-snippet")
for doc in manifest["documents"]:
    doc_id = doc["document_id"]
    path = RAW / doc["local_filename"]
    if not path.exists():
        print(f"{doc_id:7s} MISSING")
        continue
    try:
        reader = PdfReader(str(path))
        n = len(reader.pages)
        sample = reader.pages[: min(5, n)]
        chars = sum(len((p.extract_text() or "")) for p in sample)
        per_page = chars / max(1, len(sample))
        landscape = 0
        for p in reader.pages:
            box = p.mediabox
            if float(box.width) > float(box.height):
                landscape += 1
        likely_scanned = "YES" if per_page < 50 else "no"
        snippet = (reader.pages[0].extract_text() or "").strip().replace("\n", " ")[:60]
    except Exception as exc:
        print(f"{doc_id:7s} ERROR {exc}")
        continue

    dup = seen.get(doc.get("sha256", ""))
    dupflag = f"  DUP-of {dup}" if dup else ""
    seen.setdefault(doc.get("sha256", ""), doc_id)
    print(f"{doc_id:7s} {n:5d} {landscape:4d} {per_page:7.0f}  {likely_scanned:8s}  {snippet}{dupflag}")
