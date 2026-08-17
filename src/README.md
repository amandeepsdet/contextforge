# `src/` — Implementation (not started)

**There is no source code in this directory yet, and that is intentional.**

ContextForge is currently in **Milestone 1A: Document Fidelity Model**, a
research and discovery phase. Writing parser or IR code now would lock in
architectural decisions before the project has established *what* it is trying
to preserve and *how* that preservation will be measured.

## Implementation gate

Implementation (Rust) begins **only after** the Milestone 1 discovery gates are
satisfied. At minimum:

1. **1A complete** — fidelity dimensions precisely defined, adversarial patterns
   cataloged, competitor capabilities evidence-backed, hypotheses stated.
   See [../docs/milestone-1/01_document_fidelity_model.md](../docs/milestone-1/01_document_fidelity_model.md).
2. **1B complete** — an answerability-based benchmark harness and corpora
   specification exist and are reproducible.
3. **1C complete** — baseline measurements of existing systems against that
   benchmark have been collected, so implementation work has a target to beat
   and a way to know whether it is doing so.

Until then, the intended pipeline remains a *design*, not code:

```
Source Document
    -> Format Parsing
    -> Layout Understanding
    -> Semantic Document Representation / IR
    -> Context Optimization
    -> Markdown / JSON / AI Context / RAG Chunks
```

## Why the delay is deliberate

Rust is an implementation choice, **not** a differentiator (see Section 15 of
the fidelity model). Starting to code before the fidelity model and benchmark
exist would risk optimizing the wrong objective — for example, minimizing tokens
or maximizing Markdown similarity — instead of maximizing measurable, verifiable
downstream answerability under a token budget.
