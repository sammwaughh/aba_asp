# Milestone 1 — High-level path to completion

**Role:** primary working reference for finishing Milestone 1 (M1.2 then M1.3).  
**Parent index:** [`milestone1-plan.md`](milestone1-plan.md)  
**Status:** active (2026-07-16)

Organising question for all of Milestone 1:

> When and how are mechanism-aligned / correct general rules recovered by unguided ABA Learning — and what is recovered instead?

No Causal ABA integration in this milestone. Large-graph / bnlearn comparisons are **not** part of Milestone 1; they are reserved for a later evaluation phase against any Causal-ABA-informed solution.

---

## Where we are

| Part | Status | What exists |
|------|--------|-------------|
| **M1.1** | Closed | Parent-position / representation-order control; ordering mechanism established |
| **M1.2 pilot** | Analysed (Stages 0–3) | Historical 10-cell grid; to be redesigned under the expanded Approach |
| **M1.2 expanded** | Design lock in progress | Approach locked; graph/mechanism cards next |
| **M1.3** | After expanded M1.2 | Evidence-backed claims about recovery patterns and limits |
| **M1.4** | Does not exist | Large-graph tests deferred to a future evaluation milestone |

**Expanded M1.2 Approach (design reference):**  
[`milestone1_part2/milestone1_part2_expanded_approach.md`](milestone1_part2/milestone1_part2_expanded_approach.md)

Pilot artefacts (keep for provenance; not the expanded design):  
`docs/experiments/qualitative/M1.2-config-comparison.md`,  
`docs/experiments/qualitative/M1.2-config-comparison-cell-inspection.md`,  
`causal/outputs/aba_learning/grid/M12_*`.

---

## Path to finish M1.2 and M1.3

### 1. Lock the expanded M1.2 design (before more runs) — **in progress**

**Approach locked** (DGP, labelling, BK, configs, predictor policy, inspection stance):  
[`milestone1_part2/milestone1_part2_expanded_approach.md`](milestone1_part2/milestone1_part2_expanded_approach.md)

Still to lock under that Approach:

- **Graph set:** which of Fabrizio’s usable small DAGs to include (exclude random / bnlearn / cycles).
- **Mechanism cards:** for each selected graph, every \(f_y\in\{\mathrm{copy},\min,\max\}\), every non-source target, ancestor/descendant sets, reference \(\mathcal{H}_t^\star\).
- Redesign of the original five pilot motifs inside the same regime.

Do not implement or run the expanded grid until every selected cell has those inputs written down.

### 2. Finish expanded M1.2 (evidence collection)

- Implement fixtures / BK under the Approach.
- Run all cells: (fixture, non-source target, ECAI|AAMAS).
- Produce per-cell artefacts and a summary matrix.
- Inspect in plain English: what was wanted, what was learned, whether it matches, what was recovered instead (including descendant citation as an explicit failure mode).
- Only then treat M1.2 as **done**.

Detail: [`milestone1_part2/`](milestone1_part2/README.md).

### 3. Do M1.3 (claims + attribution)

Using the expanded M1.2 matrix:

- Draft **candidate claims** in plain English about when/how correct general rules are recovered and what appears instead.
- For each claim that matters, design the **smallest follow-up probes** needed.
- Run those probes; keep only claims that survive.
- Write M1.3 as evidence-backed subsections in ordinary language (not a forced category system).

Detail: [`milestone1_part3/`](milestone1_part3/README.md).

### 4. Close Milestone 1

Consolidate findings into a Milestone 1 write-up answering the organising question, and list which limits (if any) motivate Causal ABA guidance in Milestone 2.

---

## One-line discipline

Lock Approach + graph/mechanism cards → expand M1.2 evidence → M1.3 claims and probes → Milestone 1 write-up → only later large-graph evaluation against a Causal-ABA-informed solution.
