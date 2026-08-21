# `benchmarks/runs/` — Benchmark run manifests + raw outputs

**Empty in Milestone 1B-1.** No runs have been executed.

Each execution is stamped with a **Benchmark Run ID** (e.g., `BMR-2026-001`) and
an immutable run manifest capturing versions, configuration, and artifact hashes
(spec §20). Raw system outputs are stored immutably but are **git-ignored**;
only run manifests are version-controlled.

See [../../docs/milestone-1/02_benchmark_spec.md](../../docs/milestone-1/02_benchmark_spec.md)
§8–§9 (raw vs normalized) and §20 (Run ID).
