# ContextForge

> An open-source, Rust-based **document compiler** that transforms complex
> documents into semantically faithful, token-efficient context for AI systems.

**Project status: Milestone 1A — Document Fidelity Model (research / discovery).**
No parser, no extraction code, and no benchmark results exist yet. This
repository currently contains *research and specification artifacts only*.

---

## What ContextForge is (and is not)

ContextForge is **not** simply "PDF → Markdown". Markdown is only one of several
possible output representations. The intended pipeline is:

```
Source Document
    -> Format Parsing
    -> Layout Understanding
    -> Semantic Document Representation / IR
    -> Context Optimization
    -> Markdown / JSON / AI Context / RAG Chunks
```

The core research question is whether an **AI-oriented representation** of a
document can preserve information — semantic relationships, provenance, and
answerability — that is frequently lost when complex documents (financial
tables, multi-column layouts, charts, footnotes, merged cells, multi-page
tables) are flattened into text or Markdown.

This is a **hypothesis under investigation**, not a proven claim. See
[docs/milestone-1/01_document_fidelity_model.md](docs/milestone-1/01_document_fidelity_model.md)
for the full, evidence-labeled treatment.

---

## What is being researched (Milestone 1A)

- A precise, testable definition of **document fidelity** for AI context.
- Seven fidelity dimensions: Content, Structure, Layout/Spatial, Relationships,
  Semantics, Provenance, and AI Answerability.
- A conceptual **Semantic Document Graph** model (nodes + typed edges).
- A catalog of **adversarial document patterns** that break naive parsers.
- An **evidence-labeled competitive baseline** (Firecrawl, Docling, MarkItDown,
  PyMuPDF).
- Explicit **hypotheses** to validate in later milestones.

## What is explicitly NOT done yet

- No Rust implementation.
- No parser or extraction engine.
- No benchmark scores.
- No claim that ContextForge is "better than" any existing system.

Any superiority claim requires a reproducible benchmark, which does not yet
exist. This is a deliberate guardrail (see Section 15 of the fidelity model).

---

## Repository layout

```
contextforge/
├── README.md                 <- you are here
├── LICENSE                   <- Apache-2.0
├── .gitignore
├── docs/
│   └── milestone-1/
│       └── 01_document_fidelity_model.md   <- primary Milestone 1A deliverable
├── benchmarks/
│   └── README.md             <- benchmark methodology placeholder (1B)
└── src/
    └── README.md             <- implementation gate notice (no code yet)
```

---

## Roadmap (placeholder — subject to validation)

| Milestone | Theme | Status |
|-----------|-------|--------|
| **1A** | Document Fidelity Model (definitions, dimensions, adversarial catalog, baseline) | In progress |
| 1B | Benchmark design: answerability-based evaluation harness & corpora spec | Not started |
| 1C | Baseline measurements of existing systems against the benchmark | Not started |
| 2+  | IR design and Rust implementation | Gated on 1A–1C discovery outcomes |

Milestones beyond 1A are intentionally under-specified. Their scope depends on
what the discovery phase reveals.

---

## Contribution philosophy

1. **Evidence over assertion.** Capability claims about any system (including
   ContextForge) must cite a primary source or a reproducible benchmark.
2. **Honesty about uncertainty.** Distinguish established fact, project
   hypothesis, and open question. Label them.
3. **No premature lock-in.** Schemas, weights, and architecture remain
   proposals until validated.
4. **Fair comparison.** Never compare systems using different inputs or
   configurations without documenting the differences.

Contributions to the research artifacts (definitions, adversarial cases,
sourced competitor capabilities, benchmark design) are welcome during
Milestone 1. Implementation contributions are deferred until the Milestone 1
discovery gates are satisfied.

---

## License

Licensed under the [Apache License 2.0](LICENSE). Rationale for choosing
Apache-2.0 over other permissive licenses is documented in Section 7-adjacent
notes of the fidelity model and the deliverable's front matter.
