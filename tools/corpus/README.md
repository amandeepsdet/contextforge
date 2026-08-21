# `tools/corpus/` — Corpus ingestion & QA utilities (Milestone 1B-2)

Lightweight, reproducible utilities for building and verifying the ContextForge
benchmark corpus. **These are not the parser.** They only fetch and fingerprint
source documents and generate coverage metadata.

Requirements: Python 3.x and [`pypdf`](https://pypi.org/project/pypdf/)
(`py -m pip install pypdf`).

| Script | Purpose |
|--------|---------|
| `download_corpus.py` | Read the manifest, download each `source_url`, compute SHA-256 + size + page count, and (with `--update`) record those verified fields into the manifest. Fails loudly on a hash mismatch. |
| `verify_hashes.py` | Check every recorded SHA-256 against the local raw file: `PASS` / `FAIL` / `MISSING` / `NORECORD`. Non-zero exit on any `FAIL`. |
| `build_matrices.py` | Generate `fidelity_coverage_matrix.csv`, `difficulty_matrix.csv`, `adversarial_coverage.json`, and `corpus-v0.1.md` from the manifest (deterministic, documented derivations). |
| `inspect_pdfs.py` | One-off objective QA probe: text density (likely-scanned flag), landscape-page count (AP-13 evidence), page-1 title snippet, duplicate SHA-256. |

## Usage

```powershell
py tools/corpus/download_corpus.py --update    # ingest + fingerprint all
py tools/corpus/verify_hashes.py               # verify recorded hashes
py tools/corpus/build_matrices.py              # regenerate coverage metadata
py tools/corpus/inspect_pdfs.py                # objective source QA probe
```

## Safety / integrity guarantees

- Only performs a plain HTTP(S) GET of the URL already recorded in the manifest;
  never bypasses access controls and never scrapes restricted material.
- Never silently replaces a source whose recorded SHA-256 no longer matches.
- Never invents metadata: only `sha256`, `file_size_bytes`, and `page_count` are
  written, and only from the bytes actually downloaded.
- Raw documents are written to the git-ignored `benchmarks/corpus/raw/`; nothing
  here commits binary documents. Reference-only (non-redistributable) documents
  are fetched for local hashing but never redistributed by this repository.
