# E05 — Noise / SNR (appendix)

**Status:** appendix-bound spec. Runs only if compute budget permits after E02–E07 + E09 complete.
**Companion docs:** `EXPERIMENTS_PLAN.md`, `METRICS.md`, `INFRA.md`, `REPORT_OUTLINE.md` (App. B).
**Role in the plan:** ablation of noise scale on continuous DGPs. Lives in the appendix; informs §6 discussion of when ABA-ASP recovery breaks down.

---

## 1. Question

For continuous DGPs with linear-Gaussian mechanisms, how does ABA-ASP's behaviour change with the **noise scale** of the additive Gaussian term?

- Does **`body_parent_f1` decline monotonically** with increasing noise?
- Does **`fraction_solved`** decline faster, slower, or at the same rate?
- Is there a **noise threshold** above which the median outcome flips from `solved` to `completed_no_solution`?

E05 is an *appendix* result: it informs the discussion but does not gate any in-body claim.

---

## 2. Hypothesis

1. `body_parent_f1` declines roughly **logarithmically** with noise scale: nearly flat from 0.1 to 1.0, then a steep drop as noise approaches the signal scale (≥ 2.0).
2. `fraction_solved` declines **faster** than `body_parent_f1` — i.e., higher noise pushes more cells into `completed_no_solution` before pushing solved cells into low-F1 territory. (Intuition: when binning gets confused, Prolog gives up rather than emit a bad rule.)
3. The decline is **steeper on confounder/collider DGPs** than on chain DGPs — confounding signal is already weak at moderate noise.
4. There is **no useful learning** at noise_scale ≥ 4.0 on any DGP at n=25.

---

## 3. DGPs included

The same two-DGP slice as E06:

- `G3-chain` (continuous).
- `G3-fork` (continuous).

Two is enough for an appendix study.

---

## 4. Factors varied (the grid)

| Factor | Values |
|--------|--------|
| `noise_scale` | {0.1, 0.5, 1.0, 2.0, 4.0} |
| `dgp` | {G3-chain, G3-fork} |
| `target` | all (3 each) |
| `seed` | 0 … 29 |

Cells: 5 × 2 × 3 × 30 = **900**. Default-of-defaults cell (`noise_scale=1.0`) is shared with E02 via resume.

---

## 5. Factors held fixed

| Factor | Value |
|--------|-------|
| graph_type | continuous |
| noise_type | gaussian |
| n | 25 |
| bins | 2 |
| bin_strategy | quantile |
| example_split | median |
| folding_steps | 15 |
| folding_mode | nd |
| prolog_timeout_s | 120 |

---

## 6. Seeds

**30 simulator seeds: 0, 1, …, 29.**

---

## 7. Metrics & outputs

### Per-cell metrics

Full panel from `METRICS.md §3`.

### Aggregate

`groupby(dgp, target, noise_scale)`; reduce over seed via median + IQR.

### Figures

- **F-app-4 (appendix)**: one panel per DGP; x-axis: log-spaced `noise_scale`; y-axis: `body_parent_f1` (median; shaded IQR). Lines: targets. Annotation: `fraction_solved` per (DGP, target, noise_scale).

### Tables

- An appendix table T-app-E05 lists per (DGP, target, noise_scale) the median ± IQR of `body_parent_f1`, `fraction_solved`, and `offgraph_rate`.

---

## 8. Configuration stub

`causal/configs/experiments/E05_noise.yaml`:

```yaml
experiment_id: E05_noise
description: "Noise/SNR ablation on continuous DGPs. Appendix-bound."
owner: sam

defaults:
  graph_type: continuous
  noise_type: gaussian
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

grid:
  noise_scale: [0.1, 0.5, 1.0, 2.0, 4.0]
  seed: { range: [0, 30] }
  target: all

provenance:
  code_commit_required: true
  resume_from_experiments: [E02_seed_robustness]
```

---

## 9. Estimated cost

| Cells | Median per cell | Median total |
|------:|----------------:|-------------:|
| 900 (180 reused from E02) → **720 new** | ~15 s | ~3 h |

Tail: ~10 h. Plan: overnight run, low priority.

---

## 10. Pass / learn criteria

E05 passes if:

- [ ] All 720 new cells complete.
- [ ] F-app-4 and T-app-E05 render from `results.parquet`.
- [ ] The `noise_scale = 1.0` column in E05 matches E02's results exactly.

Learn:

- The actual shape of the noise-vs-F1 curve.
- Whether `fraction_solved` declines faster than `body_parent_f1` (the hypothesis above).
- Whether noise affects chain vs fork DGPs differently — useful for §6 discussion.

---

## 11. Connection to other experiments

- **Reuses:** noise_scale=1.0 cells from E02.
- **Feeds:** F-app-4 and T-app-E05 (appendix).
- **Depends on:** E02 complete.
- **Blocks:** nothing.

---

## 12. Risks & contingencies

| # | Risk | Mitigation |
|---|------|------------|
| R-E05-1 | High noise produces degenerate continuous data (single bin populated). | Detected at BK generation; mark cells `skipped` with reason `"degenerate_continuous_bins"`; reported as count. |
| R-E05-2 | Compute budget tight. | Cut to {0.1, 1.0, 4.0} as a coarser sweep. |
| R-E05-3 | Findings contradict §6 narrative about noise. | Rewrite the discussion paragraph; appendix is honest. |

---

## 13. Open questions

- Should we vary `noise_type` (Gaussian vs Laplace vs uniform)? *Default: no — out of scope for interim.*
- Should noise scale interact with `bins` (more bins for higher SNR)? *Default: no — too many factors; lives in post-interim follow-up.*

Resolutions append to the Decisions log in `EXPERIMENTS_PLAN.md`.
