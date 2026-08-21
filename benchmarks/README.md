# `benchmarks/` — ContextForge benchmark (design only)

**No benchmark corpora, no runs, and no scores exist yet.** This directory holds
the benchmark *design*. The normative specification is:

- [../docs/milestone-1/02_benchmark_spec.md](../docs/milestone-1/02_benchmark_spec.md) — **Milestone 1B-1 Benchmark Specification**

It builds on the frozen Milestone 1A fidelity model:

- [../docs/milestone-1/01_document_fidelity_model.md](../docs/milestone-1/01_document_fidelity_model.md)

## Purpose

ContextForge's central hypothesis is that **extraction fidelity does not
guarantee downstream AI answerability** (hypothesis H1 in the fidelity model).
The benchmark measures whether an AI system can correctly answer L1–L7 questions
about a source document using **only** a system's generated representation — not
a Markdown/text similarity score.

## Sub-milestones

| Sub-milestone | Deliverable | State |
|---|---|---|
| **1B-1** | Benchmark specification | complete (spec only) |
| 1B-2 | Corpus construction | not started |
| 1B-3 | Ground-truth annotation | not started |
| 1B-4 | Question set construction | not started |
| 1B-5 | Baseline execution | not started |

## Directory layout (see spec §22)

```
benchmarks/
├── README.md            <- you are here
├── spec/                <- normative machine-readable excerpts (later)
├── schemas/             <- JSON schema placeholders (ground truth, question, run manifest, result)
├── corpus/              <- corpus MANIFEST only (raw files git-ignored)
├── ground_truth/        <- ground-truth annotations, versioned (1B-3)
├── questions/           <- question sets, versioned (1B-4)
├── baselines/           <- per-system adapter specs + pinned configs (no code yet)
├── runs/                <- run manifests + raw outputs (raw outputs git-ignored)
└── results/             <- scored results + generated reports
```

## What must NOT appear here prematurely

- Any claim that ContextForge outperforms Firecrawl, Docling, MarkItDown,
  PyMuPDF, or any other system.
- Invented or illustrative "results" presented as measurements.
- Benchmark corpora containing copyrighted or sensitive documents.

Raw corpora and generated outputs are git-ignored (see `.gitignore`). Only
benchmark *definitions, methodology, schemas, ground truth, questions, and
reports* belong in version control.
