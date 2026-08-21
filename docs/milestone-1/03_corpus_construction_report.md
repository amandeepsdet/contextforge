# ContextForge — Corpus Construction Report (Milestone 1B-2)

---
title: "ContextForge — Corpus Construction Report"
milestone: "1B-2"
document_id: "03_corpus_construction_report"
status: "corpus-v0.1 — first research corpus (not production/final)"
version: "0.1.0"
last_updated: "2026-08-21"
depends_on:
  - "01_document_fidelity_model.md (Milestone 1A, frozen)"
  - "02_benchmark_spec.md (Milestone 1B-1, frozen)"
---

> **Scope.** This report documents how the **corpus-v0.1** research corpus was
> assembled for the ContextForge benchmark. It follows the frozen 1A fidelity
> model and 1B-1 benchmark specification. **No competitor baseline was run, no
> parser was built, and no benchmark results exist.** This is corpus
> construction only (sub-milestone 1B-2).

> **Integrity note.** Every byte-level field (SHA-256, file size) and every page
> count in the manifest was produced by **actually downloading** the source and
> computing it with `tools/corpus/` — none were hand-entered. Adversarial-pattern
> and scanned/orientation claims were **objectively re-checked** with a PDF probe;
> where an assumption proved false (see §7, §10, §11) it was corrected rather
> than asserted.

---

## 1. Objective

Assemble a small (~30-document), deliberately difficult, reproducible corpus that
collectively exercises the seven fidelity dimensions (1A §3) and the adversarial
patterns (1A §13), under the inclusion/exclusion, licensing, manifest, hashing,
and versioning rules of the benchmark specification (1B-1 §4–§6, §21).

The corpus is a **curated test set with a documented reason for every inclusion**,
not "30 random PDFs".

## 2. Corpus composition

**Total documents: 30** (`corpus-v0.1`). Canonical machine-readable manifest:
[../../benchmarks/corpus/manifests/corpus-v0.1.json](../../benchmarks/corpus/manifests/corpus-v0.1.json).
Generated summary: [../../benchmarks/corpus/manifests/corpus-v0.1.md](../../benchmarks/corpus/manifests/corpus-v0.1.md).

| Category | Count | Document IDs |
|----------|:-----:|--------------|
| financial_annual_report | 9 | CF-001, CF-002, CF-003, CF-004, CF-005, CF-026, CF-027, CF-028, CF-030 |
| invoice_statement_form | 6 | CF-020, CF-021, CF-022, CF-023, CF-024, CF-025 |
| research_paper | 5 | CF-006, CF-007, CF-008, CF-010, CF-011 |
| technical_document | 5 | CF-015, CF-016, CF-017, CF-018, CF-019 |
| legal_statute | 3 | CF-012, CF-013, CF-014 |
| investor_presentation | 1 | CF-029 |
| mixed_adversarial | 1 | CF-009 |

Page-count buckets: 1–5 pp ×3, 6–20 pp ×9, 21–100 pp ×12, >100 pp ×6 (largest:
CF-014 at 906 pp). Difficulty: easy ×1, medium ×18, hard ×9, adversarial ×2.

> These counts **deviate** from the 1B-1 §4.1 targets. The deviations and their
> reasons are recorded in §10 and §11 (notably: an over-representation of
> financial/government documents, and unmet scanned and language-diversity
> requirements). Per 1B-1 §4/§17 and the task's integrity rules, deviations are
> documented rather than forced.

## 3. Selection methodology

For each candidate document the following were assessed (from 1B-2 §4): domain,
format, page count, native vs scanned, layout/table/chart/figure complexity,
footnotes, captions, multi-column, multi-page tables, repeated furniture,
cross-references, mixed orientation, semantic relationships, and estimated
difficulty. A document qualified only if it exhibited **≥2 difficulty factors**
(1B-1 §5.1) and had a documented `inclusion_reason` in the manifest.

Selection was **not** optimized for or against any parser (benchmark neutrality,
1B-2 §2.9). No document was chosen because it might make a competitor fail, and
no hard document was dropped for being inconvenient.

## 4. Source policy

Sources were preferred in this order (1B-1 §5.3): public-domain U.S. Government
works, openly-licensed (e.g., CC BY) works, then publicly-available but
copyright-restricted works stored as **reference-only** (URL + hash, file not
redistributed). Primary source organizations used:

- **U.S. Federal Reserve Board** — Monetary Policy Reports, Financial Stability
  Report (public domain).
- **U.S. IRS** — forms and publications (public domain).
- **U.S. GPO / GovInfo** — public laws (public domain).
- **U.S. NIST** — Special Publications and FIPS (public domain).
- **arXiv** — research papers (one CC BY; others obtain-by-URL, license
  unverified).
- **Berkshire Hathaway Inc.** — shareholder letters (copyright; reference-only).

## 5. Licensing summary

| Redistribution status | Count | Documents |
|-----------------------|:-----:|-----------|
| Redistributable (public domain or CC BY) | 23 | all CF-0xx except those below |
| Reference-only (copyright or unverified license) | 7 | CF-005, CF-007, CF-008, CF-009, CF-010, CF-011, CF-030 |

- **Public domain (17 U.S.C. §105):** all Federal Reserve, IRS, GovInfo/GPO, and
  NIST documents (22 docs).
- **CC BY 4.0:** CF-006 (Docling report; license confirmed on the arXiv abstract).
- **Reference-only — copyright:** CF-005, CF-030 (Berkshire letters).
- **Reference-only — unverified arXiv license:** CF-007, CF-008, CF-009, CF-010,
  CF-011. These are freely downloadable from arXiv, but the arXiv default license
  does not necessarily grant redistribution, so they are marked
  `redistributable: false` pending per-paper license verification (integrity rule:
  do not fabricate licenses; mark UNKNOWN).

**No document file is committed to git.** Raw files live in the git-ignored
`benchmarks/corpus/raw/` (see repository `.gitignore` and 1B-1 §5.3, §22).

## 6. Difficulty model

Difficulty is recorded two ways:

1. A categorical `difficulty` per document (`easy | medium | hard | adversarial`).
2. Structured factors in
   [../../benchmarks/corpus/manifests/difficulty_matrix.csv](../../benchmarks/corpus/manifests/difficulty_matrix.csv):
   `table_complexity`, `chart_complexity`, `layout_complexity`, `ocr_required`,
   `relationship_complexity`, `semantic_complexity`, and `overall_difficulty`.

The categorical factor columns are **derived deterministically** from manifest
`difficulty_tags` by documented rules in `tools/corpus/build_matrices.py` (e.g.,
`table_complexity = high` iff tags include dense/multi-page/merged tables). They
are **corpus coverage metadata, not measured accuracy**.

## 7. Adversarial coverage

Coverage of the 15 patterns (1A §13), generated into
[../../benchmarks/corpus/manifests/adversarial_coverage.json](../../benchmarks/corpus/manifests/adversarial_coverage.json):

| Pattern | Covered by |
|---------|-----------|
| AP-01 Multi-column reading order | CF-006, CF-007, CF-008, CF-009, CF-010, CF-011, CF-017 |
| AP-02 Multi-page table continuation | CF-004, CF-015 |
| AP-03 Nested/merged table headers | CF-004, CF-016, CF-019, CF-020, CF-021, CF-022, CF-023, CF-024 |
| AP-04 Chart + table relationship | CF-001, CF-002, CF-003, CF-009, CF-026, CF-029 |
| AP-05 Figure + caption | CF-006, CF-007, CF-008, CF-009, CF-010, CF-011 |
| AP-06 Footnote association | CF-012, CF-013, CF-014 |
| AP-07 Repeated headers/footers | CF-001, CF-002, CF-003, CF-014, CF-015, CF-016, CF-017, CF-018, CF-026, CF-027, CF-028 |
| AP-08 Semantic duplication | CF-005, CF-012, CF-013, CF-014, CF-021, CF-023, CF-030 |
| AP-09 Cross-page references | CF-006, CF-007, CF-008, CF-010, CF-011, CF-012, CF-013, CF-014, CF-015, CF-016, CF-017, CF-018 |
| AP-10 Units and percentages | CF-001, CF-002, CF-003, CF-005, CF-029, CF-030 |
| AP-11 Financial tables with totals | CF-001, CF-002, CF-003, CF-004, CF-005, CF-020, CF-022, CF-024, CF-025, CF-026, CF-027, CF-028, CF-030 |
| AP-12 Text boxes / floating elements | CF-009, CF-020, CF-021, CF-022, CF-023, CF-024, CF-025, CF-029 |
| AP-13 Mixed-orientation pages | CF-002, CF-003 |
| **AP-14 Scanned pages** | **NONE — documented gap (see §11)** |
| AP-15 Diagram / architecture relationships | CF-010, CF-015, CF-018, CF-019 |

**14 of 15 patterns covered.** AP-13 is backed by **objective** evidence (the QA
probe found 3 landscape pages in each of CF-002 and CF-003). **AP-14 (scanned) is
not covered** and is the corpus's principal known gap (§11).

## 8. Fidelity coverage

[../../benchmarks/corpus/manifests/fidelity_coverage_matrix.csv](../../benchmarks/corpus/manifests/fidelity_coverage_matrix.csv)
records, per document, a 0/1/2 value for each of the seven dimensions
(`content_fidelity`, `structural_fidelity`, `layout_fidelity`,
`relationship_fidelity`, `semantic_fidelity`, `provenance_fidelity`,
`ai_answerability`):

- **0** = not meaningfully exercised, **1** = exercised, **2** = strongly
  exercised (dimension present **and** document difficulty is hard/adversarial).

All seven dimensions are exercised by multiple documents. `ai_answerability` is
only marked where a document was explicitly curated for downstream questioning
(e.g., CF-009, CF-029); it will be populated more fully once the 1B-4 question set
exists. This matrix is **coverage metadata, not accuracy**.

## 9. Diversity analysis

| Axis | Result | 1B-1 §4.2 requirement | Met? |
|------|--------|-----------------------|:----:|
| Page count | 6 docs >100 pp; 3 docs ≤5 pp; wide spread | ≥6 >20 pp; ≥3 single-page-ish | Yes |
| Tables | ≥18 docs with non-trivial tables | ≥12 | Yes |
| Multi-page tables | CF-004, CF-015 (+ long statutes) | ≥4 | Partial |
| Merged/nested headers | 8 docs (AP-03) | ≥4 | Yes |
| Charts | 6 docs (AP-04) | ≥6 | Yes |
| Multi-column | 7 docs (AP-01) | ≥5 | Yes |
| Footnotes | CF-012/013/014 (+ papers) | ≥4 | Yes |
| Mixed orientation | CF-002, CF-003 (objective) | ≥2 | Yes |
| Cross-page references | 12 docs (AP-09) | ≥4 | Yes |
| **Native vs scanned** | **30 native / 0 scanned** | ≥4 scanned | **No (§11)** |
| **Language** | **30 English / 0 other** | ≥2 non-English | **No (§11)** |

## 10. Excluded candidates and reasons

| Candidate | Category intended | Reason not included |
|-----------|-------------------|---------------------|
| RFC 8446, RFC 791 (rfc-editor.org `.pdf`) | technical | The `rfc-editor.org/rfc/rfcNNNN.pdf` path returned **HTTP 404** during ingestion; replaced by verified NIST PDFs (CF-018, CF-019). |
| U.S. Supreme Court slip opinions | legal | The `/opinions/23pdf/<docket>_<suffix>.pdf` filename suffix is not derivable without scraping each opinion; to avoid fabricating URLs, legal was covered via public-domain statutes instead. |
| Chronicling America newspapers (LoC) | scanned | JSON endpoints redirected/404'd in this environment; could not obtain a verified direct PDF URL. |
| Internet Archive open search results | scanned | Returned unvetted, low-provenance items unsuitable for a reputable benchmark. |
| 1990s Fed reports & FOMC transcripts | scanned | Downloaded and probed — they carry **text layers** (born-digital), so they do **not** satisfy AP-14; retained as native historical financial reports (CF-026/027/028). |
| Investor slide decks (company IR sites) | presentation | Copyright + volatile URLs; not reliably verifiable. Category represented thinly by a chart-dense public-domain report (CF-029). |

## 11. Known limitations

1. **AP-14 (scanned) not covered / scanned category empty.** Every candidate
   expected to be image-only turned out born-digital (text layer), and reputable
   image-only public-domain PDFs could not be verified in this environment.
   Rather than assert uninspected coverage or inject an unlabeled synthetic scan
   (both forbidden by the integrity rules), this is recorded as an open gap.
   *Remediation (v0.1.1/1B corpus follow-up):* add a genuinely scanned
   public-domain document from a verified source (e.g., National Archives,
   FRASER, or a curated Internet Archive item), **or** a clearly-labeled
   image-only rasterization of a public-domain source, before 1B-5 baselines run.
2. **Language diversity unmet (English-only).** 1B-1 §4.2 asks for ≥2 non-English
   documents; v0.1 has none. Remediation: add openly-licensed non-English
   documents (e.g., EUR-Lex) in a follow-up.
3. **Category imbalance.** Financial/government documents dominate (9 financial +
   6 IRS forms + 3 statutes + 5 NIST). This reflects where public-domain,
   stable-URL, structurally-hard documents are easiest to source. Downstream
   analysis must weight by category and not over-generalize.
4. **Reference-only arXiv licenses.** Five papers are `redistributable: false`
   pending per-paper license verification; only CF-006 is confirmed CC BY.
5. **Coverage matrices are heuristic metadata**, derived from tags by documented
   rules — not measured parser accuracy.
6. **Synthetic-scan hash caveat (if remediation chosen):** a rasterized fixture's
   SHA-256 would be renderer-version dependent; it would be labeled synthetic and
   its non-determinism documented.

## 12. Final corpus manifest reference

- Canonical: [../../benchmarks/corpus/manifests/corpus-v0.1.json](../../benchmarks/corpus/manifests/corpus-v0.1.json) (30 records, all with verified SHA-256, size, page count)
- Human summary: [../../benchmarks/corpus/manifests/corpus-v0.1.md](../../benchmarks/corpus/manifests/corpus-v0.1.md)
- Fidelity coverage: [../../benchmarks/corpus/manifests/fidelity_coverage_matrix.csv](../../benchmarks/corpus/manifests/fidelity_coverage_matrix.csv)
- Difficulty factors: [../../benchmarks/corpus/manifests/difficulty_matrix.csv](../../benchmarks/corpus/manifests/difficulty_matrix.csv)
- Adversarial coverage: [../../benchmarks/corpus/manifests/adversarial_coverage.json](../../benchmarks/corpus/manifests/adversarial_coverage.json)

Version label: **`corpus-v0.1`** — the first research corpus. Not a production,
final, or complete benchmark.

## 13. QA status

Per-document source QA (1B-2 §15) was performed with objective tooling:

- **Hashes:** `py tools/corpus/verify_hashes.py` → **PASS=30, FAIL=0, MISSING=0,
  NORECORD=0**.
- **Downloads/URLs:** all 30 URLs resolve to valid PDFs (`%PDF` header, parseable
  by pypdf); the 2 original RFC URLs that 404'd were replaced (§10).
- **Page counts:** computed by pypdf during ingestion.
- **Duplicate detection:** no duplicate SHA-256 across the corpus.
- **Title sanity check:** page-1 text snippets matched the expected title for all
  30 (e.g., CF-029 → "Financial Stability Report November 2024").
- **Scanned/orientation probe:** `tools/corpus/inspect_pdfs.py` — flagged
  CF-026/027/028 as **born-digital** (correcting the initial scanned hypothesis)
  and confirmed **3 landscape pages** each in CF-002/003 (AP-13).
- **Withdrawn-status note:** CF-016 (NIST SP 800-171r2) and CF-018 (NIST SP
  800-63-3) carry NIST "Withdrawn/superseded" banners; they remain valid,
  stable, public-domain documents and are retained intentionally.

No parser evaluation was performed (out of scope for 1B-2).

## 14. Reproducibility instructions

```powershell
# 1. Download every source and verify/record fingerprints (raw files are git-ignored)
py tools/corpus/download_corpus.py --update

# 2. Verify recorded SHA-256 against local files (PASS/FAIL/MISSING)
py tools/corpus/verify_hashes.py

# 3. Regenerate coverage matrices and the summary from the manifest
py tools/corpus/build_matrices.py

# 4. (Optional) objective QA probe: scanned-ness, landscape pages, titles, duplicates
py tools/corpus/inspect_pdfs.py
```

Requirements: Python 3.x and `pypdf` (`py -m pip install pypdf`). A SHA-256
mismatch is a **hard failure** (non-zero exit), so silent source drift is
detected. Reference-only documents are obtained from their `source_url`; they are
never redistributed by this repository.

---

### Appendix — no results, no baselines

This milestone produced **no** benchmark scores and ran **no** competitor system
(Firecrawl, Docling, MarkItDown, PyMuPDF). Baseline execution is sub-milestone
1B-5 and is gated behind ground-truth annotation (1B-3) and the question set
(1B-4).
