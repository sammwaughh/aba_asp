# E09 — Implied Skeleton (RQ3 step 1)

**Read after:** [`meta-understanding-plan.md`](../meta-understanding-plan.md) — **Phase 5c** (RQ3: skeleton before bridge).

**Status:** spec, runs after E02 + E03 (and ideally E04) are green.
**Companion docs:** `EXPERIMENTS_PLAN.md`, `METRICS.md` (§3.7), `INFRA.md`, `REPORT_OUTLINE.md` (F6).
**Role in the plan:** the **first answer to RQ3**. Turns δ-rule outputs into a candidate graph and compares to G\* and to constraint-based baselines. Produces Figure F6.

E09 is mostly an **analysis pass** over data already produced by E02 and E03, plus a small new baseline run.

---

## 1. Question

Can the **δ-rules produced by ABA-ASP across all targets of a DGP** be turned into a useful candidate causal graph?

Concretely:

1. Build, from the per-target δ-rule sets, an **implied undirected skeleton** `S_impl`. How does its F1 against G\*'s true skeleton compare to (i) a constraint-based baseline (PC), (ii) a trivial "fully-connected" baseline?
2. Build, from the same δ-rules, **directional candidate edges** under two rules (D1 "rule-as-edge", D2 "conservative"). How do directed F1, precision, and recall compare to PC's CPDAG output?
3. How do all of the above **scale with n** (using E03's data) and **with structure** (using E02 / E04's data)?

This is the bridge between "the learner outputs δ-rules" and "those δ-rules look like a graph". E09 is *not yet* the Causal ABA bridge — that is E10.

---

## 2. Hypothesis

1. `skel_f1` of the implied skeleton **beats the fully-connected baseline by a comfortable margin** on all DGPs at n ≥ 50; at n = 25 it beats the baseline only on chain-like DGPs.
2. `skel_f1` is **comparable to** PC's skeleton F1 on chain DGPs; **worse than** PC on confounder DGPs (because the implied skeleton inherits ABA-ASP's confounder-target failures from RQ1); **competitive with or better than** PC on small n (where CI tests are unreliable).
3. **D2 (conservative direction) beats D1 (rule-as-edge) on confounder DGPs** because D1 over-orients body-variables that are co-effects of the same confounder.
4. **Implied-skeleton F1 increases with n**, with an elbow near where `body_parent_f1` elbows (n ≈ 25–50 for 3-node, 50–100 for 4-node).
5. The **union of D1 ∪ PC** would be a stronger candidate than either alone. (This is a forward-pointing hypothesis tested in E10.)

---

## 3. DGPs included

The full DGP zoo (continuous): `G3-chain`, `G3-fork`, `G3-collider`, `G4-forkchain`, `G4-hub`.

Where possible, the discrete companion data from `E02-disc` is included in an appendix view.

---

## 4. Method (formal)

This section is the **methodological contribution** of E09. It is also written into §5.3.1 of the report and Appendix E (extended pseudocode).

### 4.1 Inputs

For a single `(dgp, n, seed, config)` cell, the inputs to the implied-skeleton method are:

- The DGP's variable set `V = {x0, x1, …, x_{k-1}}`.
- The set of `solved`-outcome target rules, indexed by target: `R_t` for each `t ∈ V`.

We aggregate across targets — i.e. we need the full set of (target, δ-rules) pairs from the same `(dgp, n, seed, config)`.

### 4.2 Per-node candidate predictor set

For each target `t`:

```
B_t = { v ∈ V \ {t} : ∃ r ∈ R_t such that v ∈ body_vars(r) and r is non-trivial }
```

`body_vars` is defined in `METRICS.md §3.4`. If `R_t = ∅` (cell unsolved for target `t`), `B_t = ∅`.

### 4.3 Implied undirected skeleton

```
S_impl = { {t, v} : t ∈ V, v ∈ B_t }    (as an undirected set; duplicates merged)
```

### 4.4 Directional rules

**D1 — rule-as-edge (permissive):**

```
E_D1 = { v → t : t ∈ V, v ∈ B_t }
```

**D2 — conservative direction:**

```
E_D2 = { v → t : t ∈ V, v ∈ B_t, and v ∈ ancestors(t, G*) ∪ parents(t, G*) }
```

D2 *uses G\* to filter*: this makes it not a discovery method per se, but a **diagnostic** that says "*if* the learner gets the ordering right (i.e. cites an ancestor), how often does it pick the correct direction?". It is a meaningful upper bound on what a future direction-aware version of the bridge could achieve.

(D2 should not be used as a deliverable discovery method in the report's bridge claims. It is reported as an *analytic baseline* — see Section 12 risks.)

### 4.5 Comparison to G\*

For the implied skeleton:

```
S_true = { {u, v} : (u, v) ∈ E(G*) or (v, u) ∈ E(G*) }
skel_precision = |S_impl ∩ S_true| / |S_impl|          (NaN if S_impl = ∅)
skel_recall    = |S_impl ∩ S_true| / |S_true|          (NaN if S_true = ∅)
skel_f1        = harmonic mean
```

For directed candidates (D1 and D2 separately):

```
dir_precision = |E_D ∩ E(G*)| / |E_D|
dir_recall    = |E_D ∩ E(G*)| / |E(G*)|
dir_f1        = harmonic mean
```

---

## 5. Baselines

E09 compares the implied skeleton against two baselines and two reference methods.

### 5.1 Trivial baseline — Fully Connected (FC)

Predict every undirected edge: `S_FC = { {u, v} : u, v ∈ V, u ≠ v }`.

- `skel_recall(FC) = 1.0`.
- `skel_precision(FC) = |S_true| / (k choose 2)` — for 3 nodes that's e.g. 2/3 = 0.67 on chain.
- `skel_f1(FC)` is a lower-bound that **any non-trivial method must beat**.

### 5.2 Reference method — PC

We use the `pc` import already present via `ArgCausalDisco/cd_algorithms/models.py`. CI test:

- **Continuous** DGPs: `fisherz` (Fisher's z-transform).
- **Discrete** DGPs: `chisq` (Pearson's chi-square).

Significance level: `alpha = 0.05`.

PC outputs a CPDAG. From it we derive:

- `skel_PC` = the underlying skeleton.
- `dir_PC` = the set of directed edges in the CPDAG (undirected edges are excluded from the precision/recall comparison; we record them separately as `n_undirected_PC`).

### 5.3 Optional method — GES

If time permits, GES is also run as a score-based reference. Score: BIC for discrete; bicd for continuous.

### 5.4 Reference upper bound — D2

As noted in Section 4.4, D2 is a diagnostic upper bound, not a deliverable method.

---

## 6. Factors varied (the grid)

The grid is the **set of (dgp, n, seed, config) tuples** from E02 ∪ E03 that have at least one `solved` cell per target. E09 itself adds no new cells *for the implied-skeleton pipeline*; it does add new cells for the **baseline runs**.

### Baseline grid (new cells, very cheap):

| Factor | Values |
|--------|--------|
| `method` | {PC, FC, GES (optional)} |
| `dgp` | DGP zoo |
| `n` | {6, 12, 25, 50, 100, 200} (same as E03) |
| `seed` | 0 … 29 |

Total baseline cells: 2 (or 3) methods × 5 DGPs × 6 n × 30 seeds = **900 (or 1350) cells**. Each cell runs PC/GES on the same simulated dataset and records a metric panel.

---

## 7. Factors held fixed

For the implied-skeleton pipeline: whatever was fixed in E02 / E03.

For the baselines:

- Significance level: 0.05.
- CI test: fisherz (continuous), chisq (discrete).
- GES score: BIC / bicd.
- Random seed: same as the simulator seed (PC is mostly deterministic given data, but seed-controlled tie-breaking is recorded).

---

## 8. Seeds

30 simulator seeds, same as E02/E03 (and the same seed indexes — so the implied skeleton and the PC baseline are computed on the **same datasets**, removing seed variance from the comparison).

---

## 9. Metrics & outputs

### Per-`(dgp, n, seed, config)` row (new rows in `results.parquet`)

The implied-skeleton metrics from `METRICS.md §3.7`:

- `skel_precision`, `skel_recall`, `skel_f1` (implied).
- `dir_d1_precision`, `dir_d1_recall`, `dir_d1_f1`.
- `dir_d2_precision`, `dir_d2_recall`, `dir_d2_f1`.

A new `method` column is added so PC / FC / GES baselines coexist as separate rows with the same metric panel.

### Aggregate

`groupby(method, dgp, n)`; reduce over seed via median + IQR.

### Figures

- **F6 — Implied skeleton F1 vs n**, one panel per DGP. X-axis: log-spaced n. Y-axis: `skel_f1` (median; shaded IQR). Lines:
  - `impl` (the ABA-ASP implied skeleton).
  - `PC` (constraint-based reference).
  - `FC` (trivial baseline).
  - (optional) `GES`.
- **F6b — Directed F1 (D1 vs D2 vs PC-directed)**, one panel per DGP. Same x-axis.

These two sub-figures fit on a single page in the report.

### Tables

- An appendix table T-app-E09 lists `skel_f1` and `dir_d1_f1` per (DGP, n, method) with IQR.

---

## 10. Configuration stub

`causal/configs/experiments/E09_implied_skeleton.yaml`:

```yaml
experiment_id: E09_implied_skeleton
description: "Build implied skeleton from ABA-ASP rules; compare to PC and FC baselines."
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

dgps:
  - { id: G3-chain,     nodes: 3, edges: [[0,1],[1,2]] }
  - { id: G3-fork,      nodes: 3, edges: [[0,1],[0,2]] }
  - { id: G3-collider,  nodes: 3, edges: [[0,2],[1,2]] }
  - { id: G4-forkchain, nodes: 4, edges: [[0,1],[0,2],[2,3]] }
  - { id: G4-hub,       nodes: 4, edges: [[0,1],[0,2],[0,3]] }

modes:                # E09 introduces a "mode" column; runner branches accordingly
  - { id: impl, source_experiments: [E02_seed_robustness, E03_sample_scaling] }
  - { id: PC,   ci_test: fisherz, alpha: 0.05 }
  - { id: FC,   trivial: true }
  - { id: GES,  score: bicd, optional: true }

grid:
  n: [6, 12, 25, 50, 100, 200]
  seed: { range: [0, 30] }

provenance:
  code_commit_required: true
```

The `mode` block is an E09-specific extension; the runner implementation note is added to `INFRA.md` when E09 is implemented.

---

## 11. Estimated cost

| Component | Cells | Time per cell | Median total |
|-----------|------:|---------------:|-------------:|
| Implied skeleton (analysis only) | reuses E02/E03 rows | <1 s each | minutes |
| PC baseline | 900 | ~1 s | ~15 min |
| FC baseline | 900 | ~0 s (closed-form) | seconds |
| GES baseline (optional) | 900 | ~5 s | ~1.25 h |

**Total: ~20 minutes** (excluding GES). E09 is dominated by analysis, not by Prolog calls.

---

## 12. Pass / learn criteria

E09 passes if:

- [ ] `aggregate_implied_skeleton` (see `METRICS.md §5.1`) produces a `results.parquet` slice with the implied-skeleton metrics for every `(dgp, n, seed, config)` shared with E02/E03.
- [ ] PC and FC baselines produce the same metric panel structure.
- [ ] F6 and F6b render from `results.parquet`.
- [ ] On **at least three DGPs**, the implied skeleton beats FC by a clear margin (median `skel_f1` outside FC's IQR).
- [ ] D1 vs D2 comparison renders correctly and the D2 diagnostic is **labelled "uses G\*"** in the caption — so we don't accidentally claim D2 as a discovery method.

Learn:

- The actual scaling of implied-skeleton F1 with n.
- Where the implied skeleton beats PC (small n? specific structures?) and where it loses.
- The headline orientation result: how often D1 disagrees with G\*.

---

## 13. Risks & contingencies

| # | Risk | Mitigation |
|---|------|------------|
| R-E09-1 | The implied skeleton is dominated by `S_impl = V × V` because the learner cites too many off-graph variables. | Report this honestly; if `skel_precision` near FC baseline, the conclusion is "δ-rules need filtering before they can serve as hints" — itself a finding informing E10. |
| R-E09-2 | PC fails or times out on small n. | Use the `causal-learn` library as a backup (more robust API); record fallbacks. |
| R-E09-3 | D2 is misread as a discovery method. | The caption and the report's §5.3.1 explicitly label D2 as "uses G\*"; this is an analytic baseline. |
| R-E09-4 | `body_vars` strips suffixes too aggressively and merges distinct variables (e.g. `x10_bin0` reduced to `x1`). | Unit tests cover the digit-boundary edge case; default regex is anchored on `^x\d+` followed by a delimiter. |
| R-E09-5 | The discrete companion looks very different from the continuous view. | Place it in the appendix; do not let it complicate the F6 narrative. |

---

## 14. Connection to other experiments

- **Reuses:** E02 + E03 (all solved cells). Optionally E04's structural view.
- **Adds:** baseline rows (PC, FC, optional GES) into a separate sub-file of `results.parquet` or a new `results_baselines.parquet`.
- **Feeds:** F6 and F6b (report §5.3.1); the "implied skeleton" framing is referenced in E10.
- **Depends on:** E02 + E03 complete.
- **Blocks:** E10. The bridge experiment uses the implied-skeleton + per-edge confidence concept defined here.

---

## 15. Open questions

- Should we filter `B_t` to only the **top-k most-frequent** body variables (across non-trivial rules of `t`)? *Default: no in the headline figure; an appendix sensitivity sweep with k=1 is added if the implied skeleton over-recalls.*
- Should we weight edges by their occurrence count across rules (giving a `confidence_edge`)? *Default: yes, this is recorded as `edge_confidence` in `coverage_detail.json` and is used as a hint signal in E10.*
- Should PC be run on the **same binned data** that ABA-ASP sees, or on the raw continuous data? *Default: raw continuous data (with `fisherz`). This makes PC a fair comparator on the original DGP.*
- Should we treat **unsolved** cells as `S_impl = ∅` or omit them from the aggregate? *Default: include them as `S_impl = ∅` so the aggregate accounts for unsolved cells; we cross-report `fraction_solved` alongside `skel_f1`.*

Resolutions append to the Decisions log in `EXPERIMENTS_PLAN.md`.
