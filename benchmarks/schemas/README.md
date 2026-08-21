# `benchmarks/schemas/` — Schema placeholders (Milestone 1B-1)

**No finalized schemas exist yet.** This directory will hold machine-readable
(JSON Schema) definitions derived from
[../../docs/milestone-1/02_benchmark_spec.md](../../docs/milestone-1/02_benchmark_spec.md).
They are intentionally **not** implemented in 1B-1 (specification only).

Planned schemas and their governing spec sections:

| Planned file | Purpose | Spec section |
|--------------|---------|--------------|
| `ground_truth.schema.json` | node/edge/fact annotation schema | §6 Ground Truth Model |
| `question.schema.json` | L1–L7 benchmark question schema | §9 Question schema |
| `run_manifest.schema.json` | Benchmark Run ID manifest (reproducibility) | §20 Reproducibility |
| `result.schema.json` | scored per-answer / per-document results | §11, §23 |

> These are **benchmark artifacts**, not the production ContextForge IR. The
> production IR is deliberately not frozen (fidelity model §7, §15).
