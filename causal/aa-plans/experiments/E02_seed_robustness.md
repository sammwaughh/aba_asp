# E02 — Seed Robustness

**Status:** spec, ready for implementation once E01 is green.
**Companion docs:** `EXPERIMENTS_PLAN.md`, `METRICS.md`, `INFRA.md`, `REPORT_OUTLINE.md` (F3).
**Role in the plan:** the single highest-leverage missing experiment; produces Figure F3 and provides the data backbone for E04.

---

## 1. Question

Holding everything else fixed (DGP, n, learner knobs), how stable are the metrics in `METRICS.md §3` across random seeds? In particular:

- What is the **median and IQR** of `body_parent_f1` per (DGP, target)?
- What is the **fraction_solved** per (DGP, target)?
- Are any (DGP, target) combinations **bimodal** (e.g., consistently solved-with-perfect-F1 *or* unsolved, with little mass in between)?

---

## 2. Hypothesis

1. Variance in `body_parent_f1` is **substantial** at n = 25 — large enough that single-seed conclusions are unreliable.
2. `fraction_solved` is **structurally distributed**:
   - High (>0.8) on chain DGPs.
   - Mixed (0.4–0.8) on confounder/collider DGPs.
   - Lowest on confounder-x2 and hub-x1/2/3 (where target value depends on a single common cause with low signal at n = 25).
3. At least one (DGP, target) combination is **bimodal** — most seeds either return a clean parent-citing rule *or* return `completed_no_solution`, with few intermediate seeds.
4. The **Python-Horn vs Prolog-aware coverage gap** (`cov_gap_pos`, `cov_gap_neg`) is non-zero on assumption-laden cells; the median gap is small (≤0.1) but the tail is informative.

These hypotheses are recorded *before* the runs and revisited in the report's discussion (§6).

---

## 3. DGPs included

The full DGP zoo from `EXPERIMENTS_PLAN.md §7`, **continuous variant** (consistent with the bridge-relevant setting in E10):

- `G3-chain` (edges: x0→x1→x2).
- `G3-fork` (edges: x0→x1, x0→x2).
- `G3-collider` (edges: x0→x2, x1→x2).
- `G4-forkchain` (edges: x0→x1, x0→x2, x2→x3).
- `G4-hub` (edges: x0→x1, x0→x2, x0→x3).

Each DGP simulates 4 variables (for G4-*) or 3 (for G3-*). All targets in each DGP are run.

A **discrete companion run** (`E02-disc`) using the same 5 DGPs but `graph_type: discrete` is run separately as part of E04's reuse-pool (see Section 11). Not part of headline E02.

---

## 4. Factors varied (the grid)

| Factor | Values |
|--------|--------|
| `dgp` | the 5 DGPs above |
| `target` | all variables of each DGP (3 for G3-\*, 4 for G4-\*) |
| `seed` | 0 … 29 (i.e. 30 seeds) |

---

## 5. Factors held fixed

| Factor | Value |
|--------|-------|
| n | 25 |
| graph_type | continuous |
| noise_type | gaussian |
| noise_scale | 1.0 |
| bins | 2 |
| bin_strategy | quantile |
| example_split | median |
| folding_steps | 15 |
| folding_mode | nd |
| prolog_timeout_s | 120 |
| query_timeout_s | 5 |

Why n = 25? Because (i) it is small enough that variance is informative (E03 will sweep n upwards), (ii) it is large enough for two-bin quantile splits to be non-degenerate, and (iii) it is comparable to the smallest-n cells in E03's grid so the row interlocks with E03.

---

## 6. Seeds

**30 seeds: 0, 1, …, 29.**

Per the `EXPERIMENTS_PLAN.md §8` decision. Seeds are passed to the simulator; BK ordering inside `generate_aba_background_knowledge` is deterministic given the data.

---

## 7. Metrics & outputs

### Per-cell metrics

Full metric panel from `METRICS.md §3`. The headline metrics for F3 are:

- `body_parent_f1` (primary).
- `fraction_solved` (annotation; computed at the aggregate level).
- `offgraph_rate` (secondary panel).
- `cov_gap_pos`, `cov_gap_neg` (recorded; surfaced in §6 discussion of the report).

### Aggregate

Per `METRICS.md §4`: `groupby(dgp, target)`; reduce over seed via median + IQR for ratios, fraction-mean for outcomes.

### Figures

- **F3 — Seed-stability boxplots** (`REPORT_OUTLINE.md §3 §5.2.1`). One panel per DGP. X-axis: targets. Y-axis: `body_parent_f1`. Whiskers: 5th/95th percentiles. Annotation per box: `fraction_solved (#solved/30)`. Cells with `fraction_solved == 0` shown as striped boxes (no claim attached, per `METRICS.md §4`).

### Tables

None in the body. An appendix table T-app-E02 lists median ± IQR for every metric per (DGP, target).

---

## 8. Configuration stub

`causal/configs/experiments/E02_seed_robustness.yaml`:

```yaml
experiment_id: E02_seed_robustness
description: "30 seeds per (DGP, target) at n=25; primary RQ2 variance source."
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
  prolog_timeout_s: 120
  query_timeout_s: 5

dgps:
  - { id: G3-chain,       nodes: 3, edges: [[0,1],[1,2]] }
  - { id: G3-fork,        nodes: 3, edges: [[0,1],[0,2]] }
  - { id: G3-collider,    nodes: 3, edges: [[0,2],[1,2]] }
  - { id: G4-forkchain,   nodes: 4, edges: [[0,1],[0,2],[2,3]] }
  - { id: G4-hub,         nodes: 4, edges: [[0,1],[0,2],[0,3]] }

grid:
  n: [25]
  seed: { range: [0, 30] }
  target: all

provenance:
  code_commit_required: true
```

Total cells: `(3 + 3 + 3 + 4 + 4) targets × 30 seeds × 1 n = 510`.

---

## 9. Estimated cost

| Cells | Median per cell | Tail per cell | Median total | Tail total |
|------:|----------------:|--------------:|-------------:|-----------:|
| 510 | 15 s | 60 s | ~2.1 h | ~8.5 h |

Plan: one overnight run, resumable. If wall-clock exceeds the tail estimate by >2×, lower `folding_steps` to 10 for a second pass and record the change in the decisions log.

---

## 10. Pass / learn criteria

E02 passes if **all** of the following hold:

- [ ] Runner completes 510 cells without infrastructure errors.
- [ ] Per (DGP, target), `fraction_solved` is computed and recorded.
- [ ] F3 renders from `results.parquet` via `analysis.py`.
- [ ] For each (DGP, target) with `fraction_solved ≥ 0.33`, we have ≥10 solved seeds; the boxplot uses only those.
- [ ] For each (DGP, target) with `fraction_solved < 0.33`, the box is rendered as "ghost" (striped, no IQR claim) and reported as such.
- [ ] All cells with outcome=`error` have a recorded `failure_reason`. The number of such cells is < 5% of total.

Learn — that is, what we *discover* even when the experiment passes:

- The **per-(DGP, target) variance profile** (the actual IQR widths), which we did not know before.
- The **bimodality map**: which combinations are bimodal and which are unimodal.
- The **coverage-gap profile**: where Prolog-aware coverage diverges most from Python-Horn.

---

## 11. Connection to other experiments

- **Feeds:** F3 (report §5.2.1) directly. **F5** (E04 — structural sweep) **uses the same `results.parquet` rows**, projected over (dgp, target) rather than (dgp, target, seed). E04 runs **no new cells**.
- **Depends on:** E01 green (P1 exit).
- **Blocks:** E03 (n-scaling). E03 reuses the n=25 column from E02's results so the n grid is sample-consistent.
- **Reuses:** none — E02 is the *primary* run.

A **discrete companion** experiment `E02-disc` (same grid but `graph_type: discrete`) is run optionally if compute permits; it feeds an appendix figure (F-app-1) but does *not* gate any in-body claim.

---

## 12. Risks & contingencies

| # | Risk | Mitigation |
|---|------|------------|
| R-E02-1 | Many (DGP, target) cells have `fraction_solved == 0`, leaving F3 mostly ghost-boxes. | Treat as a finding; widen the discussion in §6 (this is exactly the "no-solution-found is a result" point). |
| R-E02-2 | Compute overruns the overnight budget. | Resume runner; if it persists, drop `folding_steps` to 10 for a documented secondary pass. |
| R-E02-3 | Outcome distribution is suspiciously consistent (no bimodality at all). | Cross-check on `cov_gap_pos`/`cov_gap_neg`; revisit the bimodality hypothesis honestly in §6. |
| R-E02-4 | A seed causes a Prolog crash. | Marked as `error` with `failure_reason`; aggregate excludes it; manifest records the count. |

---

## 13. Open questions

- Should we report **mean ± SE** alongside median + IQR for any metric? *Default: no — ratios in [0,1] with small N are better summarised by quantiles.*
- Should we run a small **bootstrap CI** on the median? *Default: no for the body, yes for the appendix table (1000 BS reps).*
- Should `body_parent_f1 == NaN` (no non-trivial rules) be plotted as 0 or excluded from the box? *Default: excluded; the box uses only "solved with non-trivial rules" cells. The fraction of NaN cells is annotated separately.*

Resolutions append to the Decisions log in `EXPERIMENTS_PLAN.md`.
