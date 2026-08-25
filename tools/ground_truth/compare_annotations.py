#!/usr/bin/env python3
"""Inter-annotator agreement analysis for the ground-truth pilot (1B-3).

For each pilot document with both annotator_a.json and annotator_b.json, aligns
nodes across the two annotators (by page + fuzzy text_anchor, independent of the
per-annotator IDs) and computes agreement **separately per annotation class**
(1B-3 §8), because one metric does not fit all classes:

- node type            -> Cohen's kappa + raw agreement over aligned nodes
- structural membership -> agreement rate of each aligned node's parent target
- reading/sequence     -> Kendall's tau over aligned nodes' source_order
- relationship edges   -> precision / recall / F1 over aligned edge signatures
- facts                -> precision / recall / F1 over normalized fact tuples
- provenance           -> page+anchor location-agreement rate over matched facts

Writes benchmarks/ground_truth/pilot/agreement_results.json and prints a summary.

NOTE: alignment is anchor-based, so it does not assume shared IDs. This measures
schema/guideline robustness; see the pilot report for the interpretation caveat
(both passes were produced by a single agent).
"""
from __future__ import annotations

import json
import re
from itertools import combinations
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PILOT = REPO_ROOT / "benchmarks" / "ground_truth" / "pilot"

_word = re.compile(r"[a-z0-9]+")


def toks(s: str | None) -> set[str]:
    return set(_word.findall((s or "").lower()))


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def anchor(node: dict) -> str:
    prov = node.get("provenance", {})
    return prov.get("text_anchor") or node.get("normalized_content") or ""


def page_of(node: dict) -> int | None:
    return node.get("provenance", {}).get("page_number")


def align_nodes(a_nodes: list[dict], b_nodes: list[dict], thresh: float = 0.5):
    """Greedy best-match alignment by same page + max anchor Jaccard."""
    pairs = []
    for na in a_nodes:
        for nb in b_nodes:
            if page_of(na) != page_of(nb):
                continue
            s = jaccard(toks(anchor(na)), toks(anchor(nb)))
            if s >= thresh:
                pairs.append((s, na["id"], nb["id"]))
    pairs.sort(reverse=True)
    used_a, used_b, matches = set(), set(), {}
    for _, ida, idb in pairs:
        if ida in used_a or idb in used_b:
            continue
        used_a.add(ida)
        used_b.add(idb)
        matches[ida] = idb
    return matches


def cohen_kappa(labels_a: list[str], labels_b: list[str]) -> float | None:
    n = len(labels_a)
    if n == 0:
        return None
    cats = sorted(set(labels_a) | set(labels_b))
    if len(cats) == 1:
        return 1.0  # perfect, single category
    po = sum(1 for x, y in zip(labels_a, labels_b) if x == y) / n
    ca = {c: labels_a.count(c) / n for c in cats}
    cb = {c: labels_b.count(c) / n for c in cats}
    pe = sum(ca[c] * cb[c] for c in cats)
    if pe == 1.0:
        return 1.0
    return round((po - pe) / (1 - pe), 4)


def kendall_tau(order_a: dict[str, int], order_b: dict[str, int], matches: dict[str, str]) -> float | None:
    ids = [ida for ida in matches if ida in order_a and matches[ida] in order_b]
    if len(ids) < 2:
        return None
    conc = disc = 0
    for i, j in combinations(ids, 2):
        da = order_a[i] - order_a[j]
        db = order_b[matches[i]] - order_b[matches[j]]
        if da * db > 0:
            conc += 1
        elif da * db < 0:
            disc += 1
    denom = conc + disc
    return round((conc - disc) / denom, 4) if denom else None


def prf(tp: int, a_total: int, b_total: int) -> dict:
    p = tp / a_total if a_total else 0.0
    r = tp / b_total if b_total else 0.0
    f1 = (2 * p * r / (p + r)) if (p + r) else 0.0
    return {"precision": round(p, 4), "recall": round(r, 4), "f1": round(f1, 4),
            "tp": tp, "a_total": a_total, "b_total": b_total}


def edge_sig(edge: dict, node_anchor: dict[str, str]) -> tuple:
    return (edge["type"], node_anchor.get(edge["source_id"], edge["source_id"]),
            node_anchor.get(edge["target_id"], edge["target_id"]))


def norm_fact(f: dict) -> tuple:
    return (
        " ".join(sorted(toks(f.get("subject")))),
        " ".join(sorted(toks(f.get("predicate")))),
        " ".join(sorted(toks(f.get("object")))),
        (f.get("unit") or "").lower(),
        (f.get("sign") or "").lower(),
        (f.get("period") or "").lower(),
    )


def analyze(a: dict, b: dict) -> dict:
    a_nodes, b_nodes = a["nodes"], b["nodes"]
    matches = align_nodes(a_nodes, b_nodes)
    a_by = {n["id"]: n for n in a_nodes}
    b_by = {n["id"]: n for n in b_nodes}

    # node type agreement
    la, lb = [], []
    for ida, idb in matches.items():
        la.append(a_by[ida]["type"])
        lb.append(b_by[idb]["type"])
    node_type = {"aligned": len(matches),
                 "raw_agreement": round(sum(1 for x, y in zip(la, lb) if x == y) / len(la), 4) if la else None,
                 "cohen_kappa": cohen_kappa(la, lb),
                 "a_nodes": len(a_nodes), "b_nodes": len(b_nodes)}

    # structural membership: parent via contains/belongs_to edges
    def parent_map(nodes_edges, kind):
        pm = {}
        for e in nodes_edges:
            if e["type"] in ("contains", "belongs_to"):
                child = e["target_id"] if e["type"] == "contains" else e["source_id"]
                parent = e["source_id"] if e["type"] == "contains" else e["target_id"]
                pm[child] = parent
        return pm
    pa = parent_map(a["edges"], "a")
    pb = parent_map(b["edges"], "b")
    mem_total = mem_agree = 0
    for ida, idb in matches.items():
        if ida in pa and idb in pb:
            mem_total += 1
            # parents agree if they align to each other
            if matches.get(pa[ida]) == pb[idb]:
                mem_agree += 1
    membership = {"comparable": mem_total,
                  "agreement": round(mem_agree / mem_total, 4) if mem_total else None}

    # reading order
    oa = {n["id"]: n.get("source_order") for n in a_nodes if n.get("source_order") is not None}
    ob = {n["id"]: n.get("source_order") for n in b_nodes if n.get("source_order") is not None}
    reading = {"kendall_tau": kendall_tau(oa, ob, matches)}

    # relationship edges (exclude structural contains/belongs_to; those are membership)
    rel_types = {"references", "illustrates", "annotates", "cites", "explains",
                 "derived_from", "continues", "follows"}
    aa = {n["id"]: anchor(n) for n in a_nodes}
    ba = {n["id"]: anchor(n) for n in b_nodes}
    a_edges = [edge_sig(e, aa) for e in a["edges"] if e["type"] in rel_types]
    b_edges = [edge_sig(e, ba) for e in b["edges"] if e["type"] in rel_types]

    def edge_match(sig_a, b_list):
        for sb in b_list:
            if sig_a[0] == sb[0] and jaccard(toks(sig_a[1]), toks(sb[1])) >= 0.5 \
                    and jaccard(toks(sig_a[2]), toks(sb[2])) >= 0.5:
                return True
        return False
    tp_e = sum(1 for sa in a_edges if edge_match(sa, b_edges))
    edges_res = prf(tp_e, len(a_edges), len(b_edges))

    # facts F1 + provenance agreement
    fa = a["facts"]
    fb = b["facts"]
    fb_norm = [norm_fact(f) for f in fb]
    tp_f = 0
    prov_total = prov_agree = 0
    for f in fa:
        nf = norm_fact(f)
        # match by subject+period+unit primarily
        cand = [j for j, g in enumerate(fb) if norm_fact(g)[0] == nf[0] and norm_fact(g)[5] == nf[5]]
        if cand:
            j = cand[0]
            if fb_norm[j][2] == nf[2] and fb_norm[j][3] == nf[3] and fb_norm[j][4] == nf[4]:
                tp_f += 1
            # provenance agreement on aligned facts
            prov_total += 1
            pa_ = f["provenance"]
            pb_ = fb[j]["provenance"]
            if pa_.get("page_number") == pb_.get("page_number") and \
                    jaccard(toks(pa_.get("text_anchor")), toks(pb_.get("text_anchor"))) >= 0.5:
                prov_agree += 1
    facts_res = prf(tp_f, len(fa), len(fb))
    provenance = {"aligned_facts": prov_total,
                  "location_agreement": round(prov_agree / prov_total, 4) if prov_total else None}

    return {"node_type": node_type, "structural_membership": membership,
            "reading_order": reading, "relationship_edges": edges_res,
            "facts": facts_res, "provenance": provenance}


def main() -> int:
    results = {}
    for doc_dir in sorted(PILOT.glob("CF-*")):
        fa = doc_dir / "annotator_a.json"
        fb = doc_dir / "annotator_b.json"
        if not (fa.exists() and fb.exists()):
            continue
        a = json.loads(fa.read_text(encoding="utf-8"))
        b = json.loads(fb.read_text(encoding="utf-8"))
        results[doc_dir.name] = analyze(a, b)

    out = PILOT / "agreement_results.json"
    out.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")

    print(f"{'doc':8s} {'nodeK':>6s} {'nodeAgr':>7s} {'memb':>5s} {'tau':>6s} "
          f"{'edgeF1':>6s} {'factF1':>6s} {'provAgr':>7s}")
    for doc, r in results.items():
        nt, mem, rd = r["node_type"], r["structural_membership"], r["reading_order"]
        e, f, pv = r["relationship_edges"], r["facts"], r["provenance"]
        print(f"{doc:8s} {str(nt['cohen_kappa']):>6s} {str(nt['raw_agreement']):>7s} "
              f"{str(mem['agreement']):>5s} {str(rd['kendall_tau']):>6s} "
              f"{e['f1']:>6.2f} {f['f1']:>6.2f} {str(pv['location_agreement']):>7s}")
    print(f"\nwrote {out.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
