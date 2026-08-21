#!/usr/bin/env python3
"""ContextForge corpus ingestion utility (Milestone 1B-2).

Reads the corpus manifest, downloads each source document *where a public URL is
recorded*, computes SHA-256 + size + page count, and — on first ingestion —
records those verifiable fields back into the manifest. On subsequent runs it
verifies recorded hashes and fails loudly on any mismatch.

This is NOT the parser. It only fetches and fingerprints source documents.

Guarantees / non-goals:
- Never bypasses access controls; only performs a plain HTTP(S) GET of the URL
  already recorded in the manifest.
- Never silently replaces a source file whose recorded SHA-256 no longer matches
  (a mismatch is a hard failure).
- Never invents metadata: only sha256 / file_size_bytes / page_count are written,
  and only from the bytes actually downloaded.
- Raw files land in a git-ignored directory; nothing here commits binaries.

Usage:
    py tools/corpus/download_corpus.py            # download + fingerprint all
    py tools/corpus/download_corpus.py --update   # also write hashes into manifest
    py tools/corpus/download_corpus.py --only CF-001
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = REPO_ROOT / "benchmarks" / "corpus" / "manifests" / "corpus-v0.1.json"
DEFAULT_RAW_DIR = REPO_ROOT / "benchmarks" / "corpus" / "raw"
USER_AGENT = "ContextForge-corpus-bot/0.1 (+https://github.com/amandeepsdet/contextforge)"
TIMEOUT = 60


def sha256_of(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


def count_pages(path: Path) -> int | None:
    """Best-effort PDF page count. Returns None if it cannot be determined."""
    if path.suffix.lower() != ".pdf":
        return None
    try:
        from pypdf import PdfReader  # local import so the tool degrades gracefully
    except ImportError:
        return None
    try:
        reader = PdfReader(str(path))
        if reader.is_encrypted:
            try:
                reader.decrypt("")
            except Exception:
                return None
        return len(reader.pages)
    except Exception:
        return None


def download(url: str, dest: Path) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read()


def main() -> int:
    ap = argparse.ArgumentParser(description="ContextForge corpus ingestion")
    ap.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    ap.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR)
    ap.add_argument("--update", action="store_true",
                    help="write computed sha256/size/page_count into the manifest")
    ap.add_argument("--only", default=None, help="restrict to a single document_id")
    args = ap.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    docs = manifest.get("documents", [])
    args.raw_dir.mkdir(parents=True, exist_ok=True)

    seen_hashes: dict[str, str] = {}
    failures = 0
    changed = False

    for doc in docs:
        doc_id = doc.get("document_id")
        if args.only and doc_id != args.only:
            continue
        url = doc.get("source_url")
        fname = doc.get("local_filename") or (f"{doc_id}.pdf")
        if not url:
            print(f"[SKIP   ] {doc_id}: no source_url recorded")
            continue

        dest = args.raw_dir / fname
        try:
            data = download(url, dest)
        except Exception as exc:  # network / HTTP error
            print(f"[FAIL   ] {doc_id}: download error: {exc}")
            failures += 1
            continue

        dest.write_bytes(data)
        digest = sha256_of(data)
        size = len(data)
        pages = count_pages(dest)

        recorded = doc.get("sha256")
        if recorded in (None, "", "null"):
            status = "RECORDED"
            if args.update:
                doc["sha256"] = digest
                doc["file_size_bytes"] = size
                if doc.get("page_count") in (None, "", "null") and pages is not None:
                    doc["page_count"] = pages
                changed = True
        elif recorded == digest:
            status = "PASS"
        else:
            status = "FAIL(hash mismatch)"
            failures += 1

        # duplicate detection across the corpus
        dup = seen_hashes.get(digest)
        dup_note = f"  DUPLICATE-of {dup}" if dup else ""
        seen_hashes.setdefault(digest, doc_id)

        print(f"[{status:8s}] {doc_id}: {size:>9d} B  pages={pages}  {fname}{dup_note}")

    if changed and args.update:
        args.manifest.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"\nManifest updated: {args.manifest}")

    print(f"\nDone. failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
