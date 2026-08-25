# Ground-Truth Annotation Guidelines (Milestone 1B-3)

---
title: "ContextForge — Ground-Truth Annotation Guidelines"
milestone: "1B-3"
document_id: "04_ground_truth_annotation_guidelines"
status: "v0.1 (pilot) — subject to change control (see ground_truth_guideline_changelog.md)"
version: "0.1.0"
last_updated: "2026-08-25"
schema: "benchmarks/ground_truth/schemas/ground_truth.schema.json"
---

> **Purpose.** These guidelines are precise enough for **two independent
> annotators** to annotate the same document **without seeing each other's work**.
> They define nodes, relationships, facts, the three ground-truth levels,
> provenance, and — critically — how to handle **ambiguity** without guessing.
>
> **The source document is the ground truth.** Never use any parser's or
> converter's output (Firecrawl, Docling, MarkItDown, PyMuPDF, Markdown) as an
> annotation source (1B-3 §17). Annotate only what is visible in the original PDF.

## 0. Golden rules

1. Annotate the **source PDF**, never a tool's output.
2. **Never guess silently.** If unsure, set `state` to `uncertain` (best guess
   recorded) or `unresolved` (no defensible choice), and explain in `notes`.
3. **Do not invent coordinates.** If a reliable bbox is unavailable, set
   `bbox: null` and use `page_number` + `text_anchor` (§4).
4. Keep the pilot **practical** (1B-3 §14): annotate structurally meaningful
   blocks and the relationships/facts needed for L1–L7 questions, not every word.
5. Annotator B must be produced **independently** — never copied from or
   mechanically transformed from Annotator A.

## 1. Units of annotation and the three levels

Ground truth is layered (1B-1 §7). Annotate all three levels for the pilot slice:

| Level | What to annotate |
|-------|------------------|
| **L1 — Content** | node `normalized_content` / `raw_content` for each block (text, numbers). |
| **L2 — Structure / Layout** | node `type`, `source_order` (reading order), and structural edges (`contains`, `follows`, `belongs_to`, `continues`). |
| **L3 — Semantic / Relationships** | typed relationship edges (`references`, `illustrates`, `annotates`, `cites`, `explains`, `derived_from`) and `Fact` tuples. |

## 2. Nodes

### 2.1 Node types (schema `enum`)

`document · page · heading · paragraph · list · list_item · table · table_row ·
table_cell · figure · chart · caption · footnote · equation · code_block · other`

Use `other` only when nothing else fits, and explain in `notes` (e.g., a running
header/footer → `other`, `subtype: "page_furniture"`; a statutory margin note →
`other`, `subtype: "margin_note"`).

### 2.2 Node ID convention

`CF-XXX/pN/<type><k>` where `pN` is the 1-based PDF page and `k` is a per-page
counter, e.g. `CF-006/p3/fig1`, `CF-001/p11/head1`, `CF-012/p2/sec1`. IDs must be
**unique within a file** and **stable** (do not renumber after adjudication).

### 2.3 Required node fields

`id`, `type`, and `provenance` are required. Provide `normalized_content` for
content-bearing nodes. `source_order` is the reading-order rank **within the
pilot slice** (integer, ascending); ties are not allowed — if order is ambiguous,
pick one and set `state: uncertain` with a note.

### 2.4 Granularity rules

- A **heading** is a single node; the section body is separate paragraph/list/…
  nodes linked by `belongs_to`/`contains` (§3).
- A **list** node contains `list_item` nodes (one per item) via `contains`.
- For **tables** in the pilot slice, annotate the `table` node and its `caption`;
  annotate `table_row`/`table_cell` **only** where a fact depends on a specific
  cell (keep it practical). Represent uncaptured detail with `state:
  not_applicable` rather than fabricating cells.
- **Page furniture** (running headers/footers, VerDate lines, page numbers) →
  `other` with `subtype: "page_furniture"`; used to test AP-07 handling.

## 3. Relationships (edges)

### 3.1 Edge types (schema `enum`) and when to use them

| Edge | Meaning | Typical use |
|------|---------|-------------|
| `contains` | structural parent→child | list → list_item; table → row/cell; section-heading → block (structural) |
| `belongs_to` | child→section membership | paragraph → its heading/section (inverse-ish of contains at section level) |
| `follows` | reading-order successor | block B `follows` block A |
| `continues` | same logical element split across pages/columns | table (p2) `continues` table (p1) |
| `references` | an in-text pointer to a target | "see Fig. 1" paragraph → figure; TOC entry → target |
| `illustrates` | figure/chart depicts a concept/section | figure → the section/algorithm it illustrates |
| `annotates` | caption/footnote/margin-note attached to a target | caption → figure; footnote → value/call-site |
| `cites` | reference to an external work | paragraph → bibliography entry `[13]` |
| `explains` | prose explains a table/chart | paragraph → table |
| `derived_from` | chart derived from underlying data | chart → table |

Choose the **most specific** edge. Do **not** invent new edge types. Use
`belongs_to` for section membership and `contains` for direct structural nesting;
if both seem to apply, prefer `contains` for direct parent→child and add
`belongs_to` only for section membership that isn't direct nesting.

### 3.2 Edge evidence rule

Every edge must have **visible source evidence** (an explicit pointer like "see
Fig. 1", a caption physically under a figure, a TOC line with a page number). If
the relationship is only inferred without visible evidence, set `state:
uncertain` and explain; if there is no defensible basis, do **not** create the
edge (record the question in `notes` on a related node).

## 4. Provenance

Every node and every fact carries `provenance`:

- `document_id` (required), `page_number` (required; the 1-based **PDF** page).
- `bbox`: `[x0,y0,x1,y1]` **only if reliably known**; otherwise `null`. **Do not
  invent coordinates.** (The pilot uses `bbox: null` throughout because reliable
  coordinates were not extracted; this is represented explicitly, per 1B-3 §4.)
- `text_anchor`: a short verbatim quote (≤ ~80 chars) copied from the page that
  locates the node/fact. This is the primary locator when `bbox` is null.
- For table-cell provenance: `table_id`, `row`, `column`, `cell` where applicable.

Provenance must point to the **actual** source text. If provenance cannot be
determined, set `page_number: null` and `state: unresolved` with a note (never
fabricate a page).

## 5. Facts (semantic layer)

A `Fact` is a semantic tuple grounded in the document (1B-1 §6.4). Fields:
`subject`, `predicate`, `object`, plus optional `unit`, `sign`, `qualifier`,
`period`; and required `source_node` + `provenance`.

- Encode **units and signs explicitly**: `20%` → `object:"20"`, `unit:"percent"`;
  `20 percentage points` → `unit:"percentage_points"`; `100 basis points` →
  `unit:"basis_points"`. Accounting negatives → `sign:"negative"`.
- `period` captures the time reference (`"FY2025"`, `"2024"`, `"12 months ending
  Dec 2024"`).
- Only encode facts that are **stated** in the document and are plausibly useful
  for L1–L7 questions. Do **not** infer facts not present.
- If a value's unit or period is ambiguous, set `state: uncertain` with a note.

## 6. Ambiguity handling (mandatory)

Use the `state` field explicitly — never resolve ambiguity silently:

| Situation | Action |
|-----------|--------|
| Block/type boundary unclear | pick the best type, `state: uncertain`, note the alternative |
| Table header ambiguous | annotate best reading, `state: uncertain`, note the competing header |
| Reading order ambiguous (multi-column) | assign an order, `state: uncertain`, note the alternative order |
| Figure/caption association unclear | create `annotates` edge with `state: uncertain`, or omit with a note if no basis |
| Footnote association uncertain | `annotates` edge `state: uncertain`; if target unknown, `state: unresolved` |
| Semantic relationship uncertain | `state: uncertain` (has basis) or omit + note (no basis) |
| Provenance not determinable | `page_number: null`, `state: unresolved`, note |
| Content not applicable to a level | `state: not_applicable` |

## 7. Level-of-effort / scope (pilot)

Annotate the **pilot slice** pages only. Target roughly 12–30 nodes, 8–20 edges,
and 4–10 facts per document — enough to exercise every fidelity dimension and to
support example L1–L7 questions, without transcribing every token. Prefer depth on
the hard structures (tables, figures/captions, cross-references, defined terms)
over breadth.

## 8. QA before finalizing (per annotation file)

- Source PDF present locally; every `page_number` is valid for that PDF.
- Node IDs unique; every edge `source_id`/`target_id` resolves to a node in the
  same file; every fact `source_node` resolves.
- `text_anchor`s are real quotes from the cited page.
- No annotation derived from any parser output.
- Run `py tools/ground_truth/validate_ground_truth.py` → must be PASS.

## 9. Change control

These guidelines are versioned. Any rule change discovered during the pilot is
recorded in
[ground_truth_guideline_changelog.md](ground_truth_guideline_changelog.md) with
the reason and whether prior annotations must be re-reviewed. Do **not** silently
alter annotations to match a changed rule.
