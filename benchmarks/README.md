# `benchmarks/` — Methodology placeholder (Milestone 1B)

**No benchmark corpora, no runs, and no scores exist yet.** This directory is a
placeholder for the benchmark *design* that Milestone 1B will produce. It
currently defines only intent and constraints, not results.

## Purpose

ContextForge's central hypothesis is that **extraction fidelity does not
guarantee downstream AI answerability** (hypothesis H1 in the fidelity model).
Testing that hypothesis requires a benchmark that measures whether an AI system
can correctly answer questions about a source document using **only** a
system's generated representation — not a Markdown/text similarity score.

## What 1B must define (not yet done)

- **Corpora specification** — document classes (financial reports, research
  papers, scanned invoices, presentations, multi-column articles, spreadsheets)
  and how ground truth is established.
- **Question taxonomy** — the L1–L7 answerability classes defined in
  [../docs/milestone-1/01_document_fidelity_model.md](../docs/milestone-1/01_document_fidelity_model.md)
  (direct extraction, structural, spatial, relational, semantic, cross-element,
  provenance).
- **Scoring** — how semantic correctness and provenance correctness are graded,
  including confidence intervals and per-class weighting.
- **Fairness protocol** — identical inputs and documented configurations across
  all systems under comparison; no cross-configuration comparisons.
- **Reproducibility** — deterministic harness, pinned model versions, published
  prompts.

## What must NOT appear here prematurely

- Any claim that ContextForge outperforms Firecrawl, Docling, MarkItDown,
  PyMuPDF, or any other system.
- Invented or illustrative "results" presented as measurements.
- Benchmark corpora containing copyrighted or sensitive documents.

Raw corpora and generated outputs are git-ignored (see `.gitignore`). Only
benchmark *definitions, methodology, and specifications* belong in version
control.
