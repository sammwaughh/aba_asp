# Milestone 1 — High-level path to completion

**Role:** primary working reference for finishing Milestone 1 (M1.2 then M1.3).  
**Parent index:** [`milestone1-plan.md`](milestone1-plan.md)  
**Status:** active (2026-07-16)

Organising question for all of Milestone 1:

> When and how are mechanism-aligned rules recovered by unguided ABA Learning — and what is recovered instead?

No Causal ABA integration in this milestone. Large-graph / bnlearn comparisons are **not** part of Milestone 1; they are reserved for a later evaluation phase against any Causal-ABA-informed solution.

---

## Where we are

| Part | Status | What exists |
|------|--------|-------------|
| **M1.1** | Closed | Parent-position / representation-order control; ordering mechanism established |
| **M1.2 pilot** | Analysed (Stages 0–3) | 2 arms × 5 minimal handcrafted fixtures (10 cells); locked intended rules; cell inspection |
| **M1.2 expanded** | Next | Broader graph set + chosen DGP(s); same qualitative discipline |
| **M1.3** | After expanded M1.2 | Evidence-backed claims about recovery patterns and limits |
| **M1.4** | Does not exist | Large-graph tests deferred to a future evaluation milestone |

Pilot artefacts (keep; do not discard):  
`docs/experiments/qualitative/M1.2-config-comparison.md`,  
`docs/experiments/qualitative/M1.2-config-comparison-cell-inspection.md`,  
`causal/outputs/aba_learning/grid/M12_*`.

---

## Path to finish M1.2 and M1.3

### 1. Lock the expanded M1.2 design (before more runs)

Decide and write down once:

- **Graph set:** Fabrizio’s usable small DAGs already in the repo.  
  **Exclude:** random graphs, bnlearn networks, cycles.
- **DGP set:** which generative regimes to use, and how many (handcrafted locked mechanisms; Fabrizio random discrete BN; possibly more). Decide carefully; compare within-DGP first; across-DGP only when the question is DGP sensitivity.
- **Intended learned rules:** for every (graph, DGP, target) cell, state the intended rule(s) derived from true parents/mechanism **before** running.
- **Arms:** ECAI (`configs/ecai2024_config.pl`) and AAMAS (`configs/aamas2025_config.pl`) only. No RuleML.
- **Success criteria (kept separate):**
  1. match to the intended learned rule(s);
  2. ASP coverage of E⁺ / rejection of E⁻.  
  Never conflate them. The purpose of the grid is primarily **qualitative inspection of run traces** — what happens, why, and which patterns recur across graphs — to feed M1.3.

Do not expand the grid until every new cell has a stated intended output.

### 2. Finish expanded M1.2 (evidence collection)

- Implement fixtures / simulators for the chosen graphs × DGPs.
- Run under the same runner / feature-BK discipline as the pilot.
- Produce per-cell artefacts and a summary matrix.
- Inspect in plain English: what was intended, what was learned, whether it matches, what was recovered instead.
- Only then treat M1.2 as **done**.

Detail plan (when expanded): [`milestone1_part2/`](milestone1_part2/README.md).

### 3. Do M1.3 (claims + attribution)

Using the expanded M1.2 matrix:

- Draft **candidate claims** in plain English about when/how mechanism-aligned rules are recovered and what appears instead.
- For each claim that matters, design the **smallest follow-up probes** needed (trace reading, option flip, correlation ladder, success-boundary fixture, etc.).
- Run those probes; keep only claims that survive.
- Write M1.3 as evidence-backed subsections in ordinary language (not a forced category system).

M1.3 is done when we can state succinctly: what unguided ABA Learning does on these graphs/DGPs, why (with evidence), and what remains open for Milestone 2.

Detail plan: [`milestone1_part3/`](milestone1_part3/README.md).

### 4. Close Milestone 1

Consolidate findings into a Milestone 1 write-up answering the organising question, and list which limits (if any) motivate Causal ABA guidance in Milestone 2.

---

## One-line discipline

Expand M1.2 for breadth (graphs × DGPs × locked intended rules) → use that matrix to drive M1.3 claims and targeted evidence → write up Milestone 1 → only later escalate to large-graph evaluation against a Causal-ABA-informed solution.
