# E07 — Learner Ablation

**Read after:** [`meta-understanding-plan.md`](../meta-understanding-plan.md) — **Phase 5b** (ablations).

**Status:** spec, runs after E02 is green.
**Companion docs:** `EXPERIMENTS_PLAN.md`, `METRICS.md`, `INFRA.md`, `REPORT_OUTLINE.md` (T1b).
**Role in the plan:** justifies the default learner settings; produces Table T1b and informs whether "no solution found" is intrinsic or budget-limited.

---

## 1. Question

Two learner-side knobs plausibly affect outcomes:

1. `folding_steps` — the budget of folding rounds before Prolog gives up.
2. `folding_mode` — `nd` (non-deterministic) vs `greedy`. Different exploration strategies.

A third, more subtle knob:

3. **BK ordering** — the row order of `x_i_bin_j` facts inside `bk.aba`, which affects `nd` folding selection.

**Question:** how do these knobs affect the metric panel, and specifically:

- Does **raising `folding_steps`** monotonically increase `fraction_solved` and decrease `completed_no_solution`?
- Does **`greedy`** trade `fraction_solved` for wall-clock (faster but more "no solution found")?
- Is **BK ordering** a significant nuisance factor on `nd` (i.e., a problem we must report transparently)?

---

## 2. Hypothesis

1. `folding_steps`: increasing from 5 → 30 raises `fraction_solved` substantially (5 → 10 is the biggest jump; 15 → 30 is small). Median `wall_clock_s` grows roughly linearly with the budget.
2. `folding_mode`: `greedy` cuts wall-clock by a factor of 2–4× but **lowers** `fraction_solved` by 0.1–0.3 on hard cells (confounder targets, hub-of-4).
3. BK ordering: `nd` is **moderately sensitive** — the same (DGP, target, seed) cell with a different BK permutation can flip between `solved` and `completed_no_solution`. `greedy` is much less sensitive.
4. The chosen defaults (`folding_steps=15`, `folding_mode=nd`) are a defensible Pareto point on (`fraction_solved`, `wall_clock_s`).

---

## 3. DGPs included

Same two-DGP slice as E06, plus the structurally hardest DGP from E04 (likely `G4-hub` based on our priors):

- `G3-chain` — clean baseline.
- `G3-fork` — confounder; the No-solution-found pattern.
- `G4-hub` — the worst-case 4-node structure.

Three DGPs is enough: we are characterising the learner's behaviour as a function of its knobs, not the DGP zoo.

---

## 4. Factors varied (the grid)

E07 is split into **three sub-experiments** (one per knob), each varying that knob with others at default.

### E07a — `folding_steps` sweep

| Factor | Values |
|--------|--------|
| `folding_steps` | {5, 10, 15, 30} |
| `folding_mode` | nd (held) |
| `dgp` | {G3-chain, G3-fork, G4-hub} |
| `target` | all |
| `seed` | 0 … 29 |

Cells: 4 × 3 × (3+3+4) × 30 = **1200**. (3 + 3 + 4 = 10 targets total.)

Actually counting properly: G3-chain has 3 targets, G3-fork has 3, G4-hub has 4 = **10 targets**. So 4 × 10 × 30 = **1200** cells.

### E07b — `folding_mode` sweep

| Factor | Values |
|--------|--------|
| `folding_mode` | {nd, greedy} |
| `folding_steps` | 15 (held) |
| `dgp` | {G3-chain, G3-fork, G4-hub} |
| `target` | all |
| `seed` | 0 … 29 |

Cells: 2 × 10 × 30 = **600**.

### E07c — BK-ordering sensitivity

| Factor | Values |
|--------|--------|
| `bk_permutation_seed` | {0, 1, 2, 3, 4} (5 permutations of the BK row order) |
| `folding_mode` | {nd, greedy} |
| `folding_steps` | 15 (held) |
| `dgp` | {G3-chain, G3-fork} (G4-hub omitted for cost) |
| `target` | x2 only (the most informative target) |
| `seed` | 0 … 29 |

Cells: 5 × 2 × 2 × 1 × 30 = **600**.

The runner accepts a `bk_permutation_seed`; in the BK-generation step a deterministic shuffle of the BK rows is applied.

**Total E07a + E07b + E07c**: **2400 cells**. Default-of-defaults cells are shared with E02 via resume.

---

## 5. Factors held fixed

| Factor | Value |
|--------|-------|
| graph_type | continuous |
| noise_type | gaussian |
| noise_scale | 1.0 |
| n | 25 |
| bins | 2 |
| bin_strategy | quantile |
| example_split | median |
| prolog_timeout_s | 240 (raised for `folding_steps=30`) |

---

## 6. Seeds

**30 simulator seeds: 0, 1, …, 29.** Separately for E07c: **5 BK-permutation seeds**.

---

## 7. Metrics & outputs

### Per-cell metrics

Full panel from `METRICS.md §3`, with an additional column `bk_permutation_seed` (NaN for E07a/E07b).

### Aggregate

Per sub-experiment: `groupby(dgp, target, <swept_factor>)`; reduce over seed via median + IQR, plus mean for `fraction_solved`.

### Tables

- **T1b — learner ablation (in body)**: stacked sub-tables for E07a and E07b.
  - Each row: (DGP, target).
  - Columns: each value of the swept knob.
  - Each entry: `body_parent_f1` median (IQR) + `fraction_solved`%.

### Figures

- **F-app-3 — BK-ordering sensitivity** (appendix). One panel per (DGP, mode); X-axis: permutation seed; Y-axis: `fraction_solved` over the 30 simulator seeds. The spread across permutation seeds is the headline.

---

## 8. Configuration stub

`causal/configs/experiments/E07_learner_ablation.yaml`:

```yaml
experiment_id: E07_learner_ablation
description: "Sweeps over folding_steps, folding_mode, and BK ordering."
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
  prolog_timeout_s: 240

dgps:
  - { id: G3-chain, nodes: 3, edges: [[0,1],[1,2]] }
  - { id: G3-fork,  nodes: 3, edges: [[0,1],[0,2]] }
  - { id: G4-hub,   nodes: 4, edges: [[0,1],[0,2],[0,3]] }

subgrids:
  E07a_folding_steps:
    grid:
      folding_steps: [5, 10, 15, 30]
      seed: { range: [0, 30] }
      target: all
  E07b_folding_mode:
    grid:
      folding_mode: [nd, greedy]
      seed: { range: [0, 30] }
      target: all
  E07c_bk_ordering:
    dgps_override:
      - { id: G3-chain, nodes: 3, edges: [[0,1],[1,2]] }
      - { id: G3-fork,  nodes: 3, edges: [[0,1],[0,2]] }
    grid:
      folding_mode: [nd, greedy]
      bk_permutation_seed: [0, 1, 2, 3, 4]
      seed: { range: [0, 30] }
      target: [x2]

provenance:
  code_commit_required: true
```

---

## 9. Estimated cost

| Sub-experiment | Cells | Median per cell | Median total |
|----------------|------:|----------------:|-------------:|
| E07a (folding_steps) | 1200 | ~25 s (higher budget → longer tail) | ~8.3 h |
| E07b (folding_mode) | 600 | ~15 s | ~2.5 h |
| E07c (BK ordering) | 600 | ~15 s | ~2.5 h |
| **Total** | **2400** | — | **~13 h** |

Tail: ~40 h. Plan: weekend run, resumable.

---

## 10. Pass / learn criteria

E07 passes if:

- [ ] Each sub-grid completes.
- [ ] T1b renders end-to-end from `results.parquet`.
- [ ] F-app-3 renders.
- [ ] The defaults (`folding_steps=15`, `folding_mode=nd`) are *defensibly* Pareto on `(fraction_solved, wall_clock_s)`. If not, we record the new defaults and rerun any in-body affected experiment with sufficient compute headroom.

Learn:

- The actual diminishing-returns curve of `folding_steps`.
- Whether `greedy` is a useful default for any (DGP, target).
- The magnitude of BK-ordering sensitivity in absolute terms.

---

## 11. Connection to other experiments

- **Reuses:** default-of-defaults cells from E02 via resume.
- **Feeds:** T1b (report §5.2.3), F-app-3, and a "learner sensitivity" paragraph in §6.
- **Depends on:** E02 complete (for the resume reuse), and `INFRA.md` support for `bk_permutation_seed`.
- **Blocks:** nothing.

A *potential* indirect impact: if E07 finds the defaults wrong, downstream experiments may need to be re-run with new defaults. We minimise this risk by running E07 immediately after E02.

---

## 12. Risks & contingencies

| # | Risk | Mitigation |
|---|------|------------|
| R-E07-1 | `folding_steps=30` is slow and dominates wall-clock. | Already in cost estimate; resumable; if blown, drop to {5, 10, 15, 25}. |
| R-E07-2 | `greedy` mode is unsupported by current `run_aba_asp.py` glue. | Verify supported `learning_options` in `run_aba_asp.py` before launching E07b; if missing, descope E07b to a note. |
| R-E07-3 | BK-permutation sensitivity is very high — flips half the cells. | This is a strong finding. Add a §6 paragraph and emphasise it in §7's next-steps. |
| R-E07-4 | `bk_permutation_seed` interacts unexpectedly with the simulator seed. | The permutation is applied **only** to the BK row order, not to the data; document this in `INFRA.md` and unit-test it. |

---

## 13. Open questions

- Should we vary `folding_steps` jointly with n? *Default: no; the joint sweep is huge. The single-n sweep at n=25 is sufficient for interim.*
- Should we run E07c (BK ordering) on G4-hub too? *Default: no — cost dominates and the G3-fork case already exhibits the sensitivity if it exists.*
- Should we surface `wall_clock_s` as a primary metric in T1b? *Default: yes — a small secondary column.*

Resolutions append to the Decisions log in `EXPERIMENTS_PLAN.md`.
