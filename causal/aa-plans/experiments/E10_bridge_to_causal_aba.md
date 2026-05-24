# E10 — Bridge to Causal ABA (RQ3 preliminary)

**Status:** spec, runs after E09 is green. The most ambitious experiment in the interim plan; deliberately scoped to **one figure + one table + a written roadmap**.
**Companion docs:** `EXPERIMENTS_PLAN.md`, `METRICS.md` (§3.8), `INFRA.md`, `REPORT_OUTLINE.md` (F7, T2, §5.3.2, §7).
**Role in the plan:** the *preliminary* answer to RQ3. We demonstrate that δ-rule hints can be injected into Causal ABA and that this changes the output in interpretable ways. The **full benchmark** is post-interim.

---

## 1. Question

Can ABA-ASP's δ-rules be turned into **directional hints for Causal ABA**, such that the bridge produces graphs that are at least as good as Causal ABA on CI facts alone?

We answer this on a small but careful slice:

1. **What is Causal ABA's exact input contract?** (Phase A.)
2. **How does a δ-rule body translate into a hint?** (Phase B.)
3. **On a single representative DGP and two sample sizes, does `ci_plus_hints` improve over `ci_only`?** (Phase D.)

The interim deliverable is one figure (F7), one table (T2), and a **detailed roadmap** for the full benchmark.

---

## 2. Hypothesis

1. The Causal ABA implementation in `ArgCausalDisco/causalaba.py` (and/or `abapc.py`) accepts CI facts in an ASP-encoded form and produces a graph or a set of admissible graphs; preferences or extra-facts are an accepted extension point.
2. **A directional hint** for an edge `u → t` can be encoded either as (a) an additional ASP fact, (b) a preference / priority statement, or (c) a weighted argument — at least one of these forms is supported by Causal ABA without code changes.
3. On a representative DGP (e.g. `G3-collider` or `G3-chain`), at small n (n=25), `ci_plus_hints` reduces median `shd` by ≥1 edge relative to `ci_only`, on the majority of seeds where ABA-ASP's δ-rule for that target is body-parent-correct.
4. The improvement is **most visible** where CI tests are unreliable (small n, weak edges) — and absent or negative where CI tests are confident.
5. On at least one DGP × n combination, `ci_plus_hints` **degrades** Ĝ relative to `ci_only` — i.e. wrong hints actively mislead Causal ABA. This is also reported, and it motivates the post-interim work on **hint confidence**.

---

## 3. Structure: four phases

E10 is split into four phases. Phases A–C are **investigation and setup**, Phase D is the actual experiment.

### Phase A — Investigate Causal ABA API

Time-box: **2 working days**.

Tasks:

1. Read `argumentative-causal-discovery.pdf` end-to-end, focusing on the input/output contract.
2. Map the paper's formalism to the code:
   - `ArgCausalDisco/causalaba.py` — main Causal ABA entry, likely a class or function.
   - `ArgCausalDisco/abapc.py` — the ABA-PC hybrid the paper describes (combines PC's CI tests with ABA reasoning).
   - `ArgCausalDisco/encodings/*.lp` — ASP encodings. These are likely where extra facts/preferences are accepted.
   - `ArgCausalDisco/eval_aspcr.py` — runs the evaluation pipeline; useful as a working example.
   - `ArgCausalDisco/experiments.py`, `experiments_bnlearn.py` — see what kinds of inputs they actually call with.
   - `ArgCausalDisco/notebooks/` — likely the "live" entry points worth replicating.
3. Run the existing Causal ABA examples from the repo end-to-end on the local `aba-env`. Document the command and confirm it produces sensible output.
4. Identify the **injection point** for an extra directional hint. Candidates:
   - Add an ASP fact `arrow(u, t)` (or similar) before the solver call.
   - Add a preference statement on edge orientation.
   - Pre-populate a "weight" or "confidence" map keyed by edge.
5. Write a **mini-spec** `aa-plans/experiments/CAUSAL_ABA_API.md` summarising:
   - The data structure used to call Causal ABA.
   - The input contract: required keys, accepted optional keys.
   - The supported injection mode(s).
   - A minimal working example.

**Phase A exit criterion:** `CAUSAL_ABA_API.md` exists; we can call Causal ABA from a Python script in `aba-env` and obtain a graph for a known toy input.

### Phase B — Bridge design

Time-box: **1 working day**, after Phase A.

Two design choices to lock down:

#### B1 — From δ-rule to directional hint

Given a non-trivial target rule `r : t(A) :- v_{i_1}_bin*(A), v_{i_2}_bin*(A), ...`, derive the set of directional hints:

```
hints(r) = { v_{i_k} → t : k = 1, ..., len(body(r)) }
```

For a (dgp, target, seed) cell with multiple δ-rules, aggregate:

```
hint_count(v, t) = #δ-rules for target t whose body cites v (after stripping)
edge_confidence(v, t) = hint_count(v, t) / #non-trivial target rules for t
```

Three hint-modes are then implementable:

- **`hard_facts`**: emit one hint per (v, t) with `edge_confidence > 0`.
- **`top1_per_target`**: emit only the highest-confidence hint per target (i.e. argmax_v edge_confidence(v, t)). Conservative.
- **`weighted`** (post-interim — see §7 roadmap): pass `edge_confidence` to Causal ABA as a per-fact weight.

For the **interim**, we run only `hard_facts` and `top1_per_target` modes. `weighted` is deferred unless Phase A reveals it is trivially supported.

#### B2 — Bridge modes for the comparison

| Mode | Inputs |
|------|--------|
| `ci_only` | CI facts from `fisherz` at α=0.05 |
| `ci_plus_hints_hard` | CI facts + hard-facts hints from Phase B1 |
| `ci_plus_hints_top1` | CI facts + top-1 hints from Phase B1 |

We do **not** run a "hints-only" mode in the interim (post-interim work).

### Phase C — Comparator

Time-box: **0.5 days**.

Set up:

- The CI-fact extraction that Causal ABA consumes (likely already present in `ArgCausalDisco`; we wrap it).
- An `evaluate_bridge(Ĝ, G*)` function returning `shd`, `dir_edge_precision/recall/f1`, `skel_*` per `METRICS.md §3.8`.
- A small reference run that confirms `ci_only` mode reproduces (within tolerance) one of `ArgCausalDisco`'s own benchmark results.

### Phase D — The interim experiment

Time-box: **1 day of compute** (resumable).

#### Grid

| Factor | Values |
|--------|--------|
| `dgp` | **2 DGPs**, chosen post-Phase-A. Default choice: `G3-collider` (rich CI structure) and `G3-fork` (where ABA-ASP often fails — a stress case). |
| `n` | {25, 100} |
| `bridge_mode` | {ci_only, ci_plus_hints_hard, ci_plus_hints_top1} |
| `seed` | 0 … 29 |

Cells: 2 × 2 × 3 × 30 = **360 bridge runs**. Plus the underlying ABA-ASP runs for the hint inputs are **already done in E02 + E03**.

#### Inputs per cell

- Simulated data (continuous, same seed pool as E02/E03).
- Computed CI facts (from `fisherz`, α=0.05).
- For `ci_plus_hints_*`: the δ-rule-derived hints for **this seed's** ABA-ASP output, taken from E02 / E03 `results.parquet` rows.

#### Outputs per cell

Bridge metrics from `METRICS.md §3.8`:

- `shd`, `dir_edge_precision/recall/f1`, `skel_*`, `runtime_s_bridge`, plus a `hint_count` for the cell.

---

## 4. DGPs included

**Two DGPs in Phase D**, both continuous:

- `G3-collider` — the structurally rich case where CI tests are most useful (v-structures help orient).
- `G3-fork` — the failure case where ABA-ASP often returns no solution; tests whether **partial hints** still help.

Selected DGPs may shift after Phase A (e.g. if Causal ABA's reference benchmarks use particular ones, we align). Any such change is logged in the Decisions log.

---

## 5. Factors held fixed

| Factor | Value |
|--------|-------|
| graph_type | continuous |
| noise_type | gaussian |
| noise_scale | 1.0 |
| bins | 2 |
| bin_strategy | quantile |
| example_split | median |
| folding_steps | 15 |
| folding_mode | nd |
| CI test | fisherz, alpha=0.05 |
| Causal ABA mode | "default" (decided in Phase A) |

---

## 6. Seeds

**30 simulator seeds: 0, 1, …, 29.** Same pool as E02/E03 so hints are deterministically tied to specific seeds.

---

## 7. Metrics & outputs

### Per-cell metrics

Bridge metrics (`METRICS.md §3.8`) **plus**:

- `hint_count` — number of hints injected this cell (NaN for `ci_only`).
- `hint_correct_count` — number of injected hints whose direction matches G\*.
- `hint_oriented_correctly_rate` = `hint_correct_count / hint_count` (NaN if `hint_count = 0`).

This last metric tells us how *correct* the hints were, independent of how well Causal ABA used them.

### Aggregate

`groupby(dgp, n, bridge_mode)`; reduce over seed via median + IQR.

### Figures

- **F7 — Bridge preliminary** (single figure in §5.3.2):
  - Single panel: x-axis labels are (DGP, n) pairs; box-and-whisker per bridge_mode of `dir_edge_f1` (or `shd` — decided after seeing the numbers). 30 seeds per box.
  - Annotation: `hint_oriented_correctly_rate` median next to each `ci_plus_hints_*` box.

### Tables

- **T2 — Bridge summary**: rows = (DGP, n), columns = bridge_mode. Each cell: `dir_edge_f1` median (IQR), `shd` median (IQR), `runtime_s_bridge` median.

A footnote in T2 records `hint_oriented_correctly_rate` per cell.

---

## 8. Configuration stub

`causal/configs/experiments/E10_bridge.yaml`:

```yaml
experiment_id: E10_bridge
description: "Preliminary bridge: rule-derived hints + CI facts into Causal ABA."
owner: sam

defaults:
  graph_type: continuous
  noise_type: gaussian
  noise_scale: 1.0
  bins: 2
  bin_strategy: quantile
  example_split: median
  folding_steps: 15
  folding_mode: nd
  ci_test: fisherz
  ci_alpha: 0.05
  causal_aba_mode: default            # finalised in Phase A

dgps:                                  # may be revised after Phase A
  - { id: G3-collider, nodes: 3, edges: [[0,2],[1,2]] }
  - { id: G3-fork,     nodes: 3, edges: [[0,1],[0,2]] }

# Hints source: E02 and E03 results.parquet rows; runner picks matching (dgp, target, seed, n).
hints_source:
  experiments: [E02_seed_robustness, E03_sample_scaling]
  hint_derivation:
    aggregation: "edge_confidence"     # see Phase B1
    modes_emitted: [hard, top1]

grid:
  n: [25, 100]
  bridge_mode: [ci_only, ci_plus_hints_hard, ci_plus_hints_top1]
  seed: { range: [0, 30] }

provenance:
  code_commit_required: true
```

---

## 9. Estimated cost

| Phase | Time |
|-------|------|
| A — Investigation | 2 days (writing, no compute) |
| B — Design | 1 day (writing, light code) |
| C — Comparator | 0.5 days |
| D — Run + analysis | 360 cells × ~5–30 s each ≈ **30 min – 3 h compute** |

E10 is **bounded** in compute. The bulk of E10's cost is wall-clock for Phases A/B/C, not Prolog.

---

## 10. Pass / learn criteria

E10 passes if **all** of:

- [ ] `CAUSAL_ABA_API.md` exists and is correct (Phase A done).
- [ ] We can call Causal ABA in `ci_only`, `ci_plus_hints_hard`, and `ci_plus_hints_top1` modes from `run_grid.py`.
- [ ] Phase D produces a `results.parquet` slice with 360 rows, each with the bridge metric panel.
- [ ] F7 and T2 render from `results.parquet`.
- [ ] We can write the §5.3.2 paragraph **truthfully**, i.e. claim only what F7/T2 actually show.
- [ ] The §7 roadmap is finalised based on what we *learned* in E10 (not what we wished for).

Learn — and report — at minimum these facts in §5.3.2:

- Whether `ci_plus_hints_*` helps on (DGP, n) median, IQR, and tail.
- The `hint_oriented_correctly_rate` — how good ABA-ASP's hints actually are.
- Whether hints helped more on `G3-collider` or `G3-fork`, and why.
- At least one **negative finding** (a case where hints hurt or were uninformative).

---

## 11. Risks & contingencies

| # | Risk | Mitigation |
|---|------|------------|
| R-E10-1 | Causal ABA's API is harder than expected; Phase A overruns. | The time-box is hard: at day 2, if we are not running their reference example, we descope to **a non-bridge alternative**: implied-skeleton vs PC, with hints framed only conceptually in §5.3.2. The §7 roadmap then becomes "the bridge implementation is the first deliverable post-interim". |
| R-E10-2 | Causal ABA does not accept additional facts/preferences without code changes. | Investigate a minimal patch in a fork of `ArgCausalDisco`; if non-trivial, descope as above. |
| R-E10-3 | Hints help everywhere — no negative finding. | Add a **wrong-hint stress test**: deliberately inject a hint contradicting G\* on a small slice (post-D, ≤30 cells). The expected negative finding emerges. |
| R-E10-4 | Hints help nowhere — uniformly negative result. | This is also a clear finding; the §7 roadmap then prioritises **hint confidence weighting** and **filtering**. |
| R-E10-5 | Causal ABA wall-clock is heavy at n=100. | Drop to n ∈ {25, 50}; record. |

If R-E10-1 or R-E10-2 fires, the interim report's §5.3.2 is reframed as:

> "We demonstrate that the implied-skeleton method (E09) is a candidate hint source; the bridge to Causal ABA itself is left to post-interim work. The remaining engineering and design questions are detailed in §7."

This is an acceptable interim outcome.

---

## 12. Post-interim roadmap (for §7 of the report)

The §7 (Plan for the remainder of the project) writeup is **derived from this section**.

### R1 — Full bridge benchmark

- Extend to the full DGP zoo (5 graphs), n ∈ {12, 25, 50, 100, 200}, ≥30 seeds.
- Add `GES` and `FCI` references.
- Report SHD distribution, directed F1, and skeleton F1 jointly.

### R2 — Confidence-weighted hints

- Use `edge_confidence` (Phase B1) as a per-hint weight inside Causal ABA.
- Compare to binary hints; expect monotone improvement.

### R3 — Hint disagreement resolution

- Where δ-rule-derived hints contradict CI test outcomes (e.g. CI says u ⊥ t given S, but δ-rule cites u in t's body), record the conflict rate. Investigate whether Causal ABA's argumentation semantics resolves these "naturally" or whether explicit preferences are needed.

### R4 — Beyond toy graphs

- Add 5-node and 6-node DGPs.
- Add real or semi-synthetic datasets (e.g. bnlearn benchmarks already in `ArgCausalDisco`).

### R5 — Alternative bridges

- Hints as **soft constraints** rather than facts.
- Hints as **arguments** with their own attackers in the AAF.
- A pure "argumentative learner" that emits arguments directly (no ABA-ASP intermediary).

### R6 — Theoretical questions

- Is there an equivalence (or partial equivalence) between an ABA-ASP δ-rule with assumptions and a Causal ABA argument? If so, the bridge is *structural*, not merely "directional hint".

R1, R2, R3 are the first three deliverables of the post-interim period. R4–R6 are MSc-thesis-scale.

---

## 13. Connection to other experiments

- **Depends on:** E02 + E03 + E09 complete. Phase A depends on `argumentative-causal-discovery.pdf` and `ArgCausalDisco`.
- **Reuses:** δ-rule-derived hints from E02 and E03; same simulator seeds.
- **Feeds:** F7 + T2 in report §5.3.2; roadmap text in §7.
- **Blocks:** the supervisor's pipeline (Experiment 1 sanity check + Alt 3 — these are R1 in §12).

---

## 14. Open questions

- Should we include `ci_only` runs from PC and FCI separately, or only from Causal ABA's `ci_only` mode? *Default: only Causal ABA's `ci_only`; PC is already in F6 via E09.*
- Should we record per-edge hint attribution in `coverage_detail.json`? *Default: yes; useful for the §6 discussion paragraph on "wrong hints".*
- Should we use **all** of E02 + E03's hint cells, or filter to those with `body_parent_f1 > 0.5`? *Default: use all; filtering is a *post hoc* analysis recorded as a sensitivity check.*
- Should we run a tiny "hint disagreement" appendix study? *Default: only if time permits in the interim window.*

Resolutions append to the Decisions log in `EXPERIMENTS_PLAN.md`.

---

## 15. What "begun to answer RQ3" looks like in the report

Concretely, §5.3.2 will read (in skeleton):

1. *Sentence 1*: We describe the bridge implementation (Phase A/B/C summary, ~3 sentences).
2. *Sentence 2*: F7 shows that on `G3-collider` at n=25, `ci_plus_hints_*` improves median directed F1 by ~X (with IQR); the improvement attenuates at n=100 where CI tests are themselves reliable.
3. *Sentence 3*: On `G3-fork` at n=25, hints actively degrade Ĝ in a subset of seeds — those where ABA-ASP returned an off-graph δ-rule. This is the negative finding.
4. *Sentence 4*: Inline reference to T2 for full numbers.
5. *Sentence 5*: Forward-pointer to §7's roadmap items R1–R3.

(Numbers in *sentence 2* and *sentence 3* are filled in after Phase D actually runs.)
