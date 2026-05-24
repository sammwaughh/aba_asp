# E06 — Binning Ablation

**Status:** spec, runs after E02 is green.
**Companion docs:** `EXPERIMENTS_PLAN.md`, `METRICS.md`, `INFRA.md`, `REPORT_OUTLINE.md` (T1a).
**Role in the plan:** justifies the default bin choices for continuous DGPs; produces Table T1a.

---

## 1. Question

For continuous DGPs, three knobs control how raw values become BK predicates and how E+/E− are defined:

1. `bins` — number of bins per variable.
2. `bin_strategy` — `quantile` vs `uniform`.
3. `example_split` — how E+/E− are computed for a continuous target: `median`, `top_bottom_third` (E+ = top third, E− = bottom third, middle discarded), or `bin_specific` (use the target's own bin to define E+/E−).

Each knob trades expressivity for stability. **E06 measures that trade-off.**

---

## 2. Hypothesis

1. **`bins = 2` (quantile, median split)** is a strong default at small n. Increasing `bins` raises rule complexity faster than it helps `body_parent_f1`.
2. **`uniform` binning** is *worse* than `quantile` at small n because tail bins can be empty.
3. **`top_bottom_third` example_split** improves `body_parent_f1` on a subset of cells (cleaner E+/E−) at the cost of throwing away middle samples; we expect a net loss at n=25 but possibly a net gain at n=100+.
4. **`bin_specific` example_split** decouples E+/E− from the median, which we expect to *increase* `offgraph_rate` because the learner has more freedom to cite the matching bin's own predicate (a degenerate rule).
5. The default (`bins=2`, `quantile`, `median`) is **either the best or within the IQR of the best** combination on every (DGP, target) cell at n=25.

---

## 3. DGPs included

To keep the grid tractable, E06 uses **two** DGPs that already showed informative behaviour in earlier Phase 3 runs:

- `G3-chain` (continuous) — the clean baseline; one body-parent-correct rule is expected on most cells.
- `G3-fork` (continuous) — the difficult baseline; the n=6 confounder-x2 cell produced `completed_no_solution`. The question is whether binning choices recover signal on this DGP at slightly larger n.

We **do not** include `G3-collider` or the G4-\* DGPs in E06's body — those are appendix candidates if compute permits. The point is to justify defaults, not to be comprehensive.

---

## 4. Factors varied (the grid)

E06 is split into **three one-at-a-time sub-experiments** so each factor is varied independently. This keeps the table interpretable and rules out interaction effects without paying for the full 3×2×3 Cartesian.

### E06a — `bins` sweep

| Factor | Values |
|--------|--------|
| `bins` | {2, 3, 4} |
| `bin_strategy` | quantile (held) |
| `example_split` | median (held) |
| `dgp` | {G3-chain, G3-fork} |
| `target` | all (3 each) |
| `seed` | 0 … 29 |

Cells: 3 × 2 × 3 × 30 = **540**.

### E06b — `bin_strategy` sweep

| Factor | Values |
|--------|--------|
| `bin_strategy` | {quantile, uniform} |
| `bins` | 2 (held) |
| `example_split` | median (held) |
| `dgp` | {G3-chain, G3-fork} |
| `target` | all |
| `seed` | 0 … 29 |

Cells: 2 × 2 × 3 × 30 = **360**.

### E06c — `example_split` sweep

| Factor | Values |
|--------|--------|
| `example_split` | {median, top_bottom_third, bin_specific} |
| `bins` | 2 (held) |
| `bin_strategy` | quantile (held) |
| `dgp` | {G3-chain, G3-fork} |
| `target` | all |
| `seed` | 0 … 29 |

Cells: 3 × 2 × 3 × 30 = **540**.

**Total across E06a + E06b + E06c**: **1440 cells**. (The default-of-defaults cell is shared across all three sub-experiments via runner reuse, so duplicates are skipped.)

---

## 5. Factors held fixed

| Factor | Value |
|--------|-------|
| graph_type | continuous |
| noise_type | gaussian |
| noise_scale | 1.0 |
| n | 25 |
| folding_steps | 15 |
| folding_mode | nd |
| prolog_timeout_s | 120 |

---

## 6. Seeds

**30 seeds: 0, 1, …, 29.** Same as E02; ensures cross-experiment comparability.

---

## 7. Metrics & outputs

### Per-cell metrics

Full panel from `METRICS.md §3`.

### Aggregate

Per sub-experiment: `groupby(dgp, target, <swept_factor>)`; reduce over seed via median + IQR.

### Tables

- **T1a — binning ablation (in body)**: a compact one-page table.
  - Row groups: (DGP, target).
  - Columns: each cell of the swept factor.
  - Metric in each cell: `body_parent_f1` median (IQR) and `fraction_solved` percentage.
  - One sub-table per sub-experiment (E06a, E06b, E06c); they sit side-by-side or stacked.

### Figures

No figures in the body. Optional appendix figure F-app-2 is a heatmap of `body_parent_f1` across all combinations of (bins, strategy, split) at fixed DGP=G3-chain target=x2.

---

## 8. Configuration stub

`causal/configs/experiments/E06_binning.yaml` (single file, three named sub-grids):

```yaml
experiment_id: E06_binning
description: "One-at-a-time ablation of bins, bin_strategy, example_split on 2 continuous DGPs."
owner: sam

defaults:
  graph_type: continuous
  noise_type: gaussian
  noise_scale: 1.0
  n: 25
  bins: 2
  bin_strategy: quantile
  example_split: median
  folding_steps: 15
  folding_mode: nd
  prolog_timeout_s: 120

dgps:
  - { id: G3-chain, nodes: 3, edges: [[0,1],[1,2]] }
  - { id: G3-fork,  nodes: 3, edges: [[0,1],[0,2]] }

subgrids:
  E06a_bins:
    grid:
      bins: [2, 3, 4]
      seed: { range: [0, 30] }
      target: all
  E06b_strategy:
    grid:
      bin_strategy: [quantile, uniform]
      seed: { range: [0, 30] }
      target: all
  E06c_split:
    grid:
      example_split: [median, top_bottom_third, bin_specific]
      seed: { range: [0, 30] }
      target: all

provenance:
  code_commit_required: true
```

(The runner supports a `subgrids` block by enumerating each sub-grid as if it were a separate experiment, but writing all rows into a single `results.parquet` with a `subgrid_id` column. The implementation note is in `INFRA.md §3.2`.)

---

## 9. Estimated cost

| Sub-experiment | Cells | Median per cell | Median total |
|----------------|------:|----------------:|-------------:|
| E06a (bins) | 540 | ~18 s (higher bins → more candidate predicates) | ~2.7 h |
| E06b (strategy) | 360 | ~15 s | ~1.5 h |
| E06c (split) | 540 | ~15 s | ~2.3 h |
| **Total** | **1440** | — | **~6.5 h** |

Tail: ~22 h. Plan: overnight run.

---

## 10. Pass / learn criteria

E06 passes if:

- [ ] Each sub-grid completes.
- [ ] T1a renders end-to-end from `results.parquet`.
- [ ] Each (DGP, target) row in T1a has a "winning" combination identified, with statistical justification (the winner's IQR overlaps no other cell's IQR — or the winner shares the lead with overlap, which is also a finding).

Learn:

- Whether the chosen defaults (bins=2, quantile, median) are the actual winners or a defensible compromise.
- The marginal cost of moving to bins=3 in terms of `wall_clock_s` and `n_target_rules`.
- Whether `top_bottom_third` ever wins, and when.

---

## 11. Connection to other experiments

- **Reuses:** the default-of-defaults cells are shared with E02 via resume.
- **Feeds:** T1a (report §5.2.3).
- **Depends on:** E02 complete (so the resume reuse is meaningful).
- **Blocks:** nothing — E06 is a leaf experiment.

---

## 12. Risks & contingencies

| # | Risk | Mitigation |
|---|------|------------|
| R-E06-1 | `uniform` strategy produces many empty bins at n=25, causing degenerate BK. | Detect at BK-generation time; mark such cells `skipped` with reason `"degenerate_uniform_bins"`; report the count alongside results. |
| R-E06-2 | `top_bottom_third` produces empty E+ or E− on small n. | Skip with reason `"empty_examples_split"`; this is itself a finding about the split's small-n cost. |
| R-E06-3 | Findings disagree with our predicted defaults. | Update the defaults in `EXPERIMENTS_PLAN.md §8`; rerun affected downstream experiments only if interpretation changes materially. |
| R-E06-4 | T1a becomes too dense to read at a glance. | Move full per-cell values to T-app-E06; keep T1a as a "winner per (DGP, target)" summary. |

---

## 13. Open questions

- Should we run a 4-bin "fine" study only on n=100 cells (where there is more data to support finer bins)? *Default: no for interim; flag as a follow-up.*
- Should `bin_specific` example_split count `vars` from the bin predicate as "ghost" matches (since the target bin variable matches the target itself)? *Default: this is handled in `body_vars` — predicate prefix `x{i}` strips suffixes; we record an additional `degenerate_hit` count.*
- Should we report only "default vs winner" as a compact summary? *Default: yes — that is exactly T1a's role.*

Resolutions append to the Decisions log in `EXPERIMENTS_PLAN.md`.
