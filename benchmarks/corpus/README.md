# `benchmarks/corpus/` — Corpus manifest (metadata only)

**Empty in Milestone 1B-1.** Corpus construction is **1B-2** and has not started.

This directory will hold the **corpus manifest** (document metadata: id, category,
source URL, license, retrieval date, hash, difficulty tags) as defined in
[../../docs/milestone-1/02_benchmark_spec.md](../../docs/milestone-1/02_benchmark_spec.md)
§4–§5.

Raw document files (`*.pdf`, `*.docx`, `*.pptx`, `*.xlsx`, …) are **git-ignored**
and are **not** stored here. Non-redistributable documents are represented by a
reference (URL + hash + date) only (spec §5.3).
