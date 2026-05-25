# E08 — BK Content Ablation (appendix)

**Read after:** [`meta-understanding-plan.md`](../meta-understanding-plan.md) — **Phase 5d** (appendix experiments; skim).

**Status:** appendix-bound spec. Runs only if compute budget permits after E02–E07 + E09 complete.
**Companion docs:** `EXPERIMENTS_PLAN.md`, `METRICS.md`, `INFRA.md`, `REPORT_OUTLINE.md` (App. B).
**Role in the plan:** stresses the BK content side of the pipeline; informs §6 discussion and is a precursor to RQ3's "what does the learner do under realistic BK noise" question.

---

## 1. Question

When the BK shown to ABA-ASP **deviates from the ground-truth predictor set**, how does this affect the metric panel? Two deviations are interesting:

1. **Irrelevant columns injected**: add 1 or 2 columns that are independent of all G\* variables. Does the learner cite them in body rules (false positives)?
2. **True parent dropped**: exclude a known true parent from the BK (in addition to the target). Does the learner fall back on ancestors / siblings, or fail entirely?

E08 is an **appendix** result — it informs the discussion but does not gate any in-body claim. It is, however, the most direct precursor to a *realistic* RQ3 setting where the bridge will see BK that contains both relevant and irrelevant variables.

---

## 2. Hypothesis

1. **Irrelevant column injection**:
   - `offgraph_rate` rises measurably with each irrelevant column added.
   - `body_parent_precision` falls; `body_parent_recall` is roughly stable.
   - `n_target_rules` grows (the learner produces more — and worse — rules).
2. **Dropped-parent stress**:
   - On chain DGPs (`G3-chain`), dropping x0 (the root) does not affect target x1 (still has direct parent x0 → x1 — but x0 is gone, so x1 falls back to itself or to x2; **expected**: target x1 produces an off-graph rule citing x2, or `completed_no_solution`).
   - On confounder DGPs (`G3-fork`), dropping x0 (the confounder) leaves x1 and x2 marginally correlated; targets become **harder**; expected fraction_solved drop.
   - The effect is more severe for confounder/collider DGPs than for chain.

---

## 3. DGPs included

Two-DGP slice (consistent with E05/E06):

- `G3-chain` (continuous).
- `G3-fork` (continuous).

---

## 4. Factors varied (the grid)

Two sub-experiments.

### E08a — Irrelevant column injection

| Factor | Values |
|--------|--------|
| `n_irrelevant_cols` | {0, 1, 2} |
| `irrelevant_distribution` | `gaussian` (mean 0, std 1) |
| `dgp` | {G3-chain, G3-fork} |
| `target` | all (3 each) |
| `seed` | 0 … 29 |

Irrelevant columns are appended **after** the DGP's variables and named `noise0`, `noise1`. The BK generation picks them up as ordinary continuous variables (with their own binning), exactly as it would a real variable.

Cells: 3 × 2 × 3 × 30 = **540**.

### E08b — Dropped-parent stress

| Factor | Values |
|--------|--------|
| `dropped_parent` | one ground-truth parent of the current target (DGP-specific) |
| `dgp` | {G3-chain, G3-fork} |
| `target` | per DGP: {x1, x2} for G3-chain; {x1, x2} for G3-fork (root drops are not meaningful) |
| `seed` | 0 … 29 |

For each (DGP, target), we run two cells per seed: with all parents in BK (the baseline, reused from E02), and with one parent dropped from BK (`exclude_cols = [target, dropped_parent]`).

Cells (new): 2 × 2 × 30 = **120**. Baselines (60) are reused from E02 via resume.

**Total E08a + E08b: 660 cells** (about 540 + 120 new).

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
| folding_steps | 15 |
| folding_mode | nd |
| prolog_timeout_s | 120 |

---

## 6. Seeds

**30 simulator seeds: 0, 1, …, 29.** Irrelevant columns in E08a are seeded identically (same seed reproduces the same `noiseK` realisations).

---

## 7. Metrics & outputs

### Per-cell metrics

Full panel from `METRICS.md §3`. Specifically for E08a we add a derived metric:

- `offgraph_rate_to_noise` = (Σ_{r non-trivial} 1[body cites a `noiseK`]) / (#non-trivial target rules), recorded alongside the standard `offgraph_rate`. (For E08b, this is NaN.)

### Aggregate

Per sub-experiment: `groupby(dgp, target, <swept factor>)`; reduce over seed via median + IQR.

### Figures

- **F-app-5 (appendix)** — Irrelevant column injection:
  - Left panel: `body_parent_precision` median (IQR) vs `n_irrelevant_cols`, per DGP.
  - Right panel: `offgraph_rate_to_noise` median (IQR) vs `n_irrelevant_cols`.
- **F-app-6 (appendix)** — Dropped-parent stress:
  - Bar chart: `body_parent_f1` and `fraction_solved` for "all parents in BK" vs "one parent dropped", per (DGP, target).

### Tables

- An appendix table T-app-E08 lists per (DGP, target, condition) the median ± IQR of `body_parent_f1`, `offgraph_rate`, and `fraction_solved`.

---

## 8. Configuration stub

`causal/configs/experiments/E08_bk_content.yaml`:

```yaml
experiment_id: E08_bk_content
description: "BK-content stress: irrelevant columns + dropped parent. Appendix-bound."
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
  E08a_irrelevant_cols:
    grid:
      n_irrelevant_cols: [0, 1, 2]
      irrelevant_distribution: [gaussian]
      seed: { range: [0, 30] }
      target: all
  E08b_dropped_parent:
    grid:
      dropped_parent: auto   # runner picks a true parent of current target per DGP
      seed: { range: [0, 30] }
      target: [x1, x2]       # roots excluded

provenance:
  code_commit_required: true
  resume_from_experiments: [E02_seed_robustness]
```

The `dropped_parent: auto` value tells the runner: "for each (DGP, target), drop **one** of the true parents of `target` in G\*; if `target` has multiple parents, drop the first by node index". This choice is documented in the manifest.

---

## 9. Estimated cost

| Sub-experiment | Cells (new) | Median per cell | Median total |
|----------------|------------:|----------------:|-------------:|
| E08a | 360 | ~15 s | ~1.5 h |
| E08b | 120 | ~15 s | ~30 min |
| **Total** | **480** | — | **~2 h** |

Tail: ~6 h. Plan: overnight run, low priority.

---

## 10. Pass / learn criteria

E08 passes if:

- [ ] Each sub-grid completes.
- [ ] F-app-5, F-app-6, and T-app-E08 render from `results.parquet`.
- [ ] The `n_irrelevant_cols = 0` baseline in E08a matches E02's results exactly (sample-consistency check).
- [ ] The `dropped_parent` cells include a non-NaN `body_parent_recall` so we can compute the fall-back behaviour.

Learn:

- Whether `offgraph_rate_to_noise` rises proportional to `n_irrelevant_cols` (linear) or super-linearly.
- Whether dropping a true parent causes `completed_no_solution` rather than a wrong rule — a hypothesis directly testable here.
- Whether the learner's behaviour under BK noise is **predictable** (informs whether δ-rule confidence as in E10 Phase B1 is meaningful under BK noise).

---

## 11. Connection to other experiments

- **Reuses:** `n_irrelevant_cols=0` cells from E02 via resume; baseline cells of E08b similarly.
- **Feeds:** F-app-5, F-app-6, T-app-E08; one paragraph in §6 discussion of "realistic BK".
- **Depends on:** E02 complete; runner must accept `n_irrelevant_cols` and `dropped_parent` config keys.
- **Blocks:** nothing.

---

## 12. Risks & contingencies

| # | Risk | Mitigation |
|---|------|------------|
| R-E08-1 | Irrelevant-column injection breaks BK generation (e.g. naming collisions). | Reserved namespace `noiseK` for irrelevant columns; runner unit-tested for the injection. |
| R-E08-2 | Dropping a parent leaves E+/E− unchanged and the cell is uninformative. | The cell is still run; if `outcome != solved`, that *is* the finding for that (DGP, target). |
| R-E08-3 | Findings contradict the hypothesis (e.g. injecting irrelevant columns has **no effect**). | Negative result is reported honestly. This would be evidence that ABA-ASP is more robust to BK noise than expected — useful for the discussion. |
| R-E08-4 | E08b cells require non-default BK generation logic. | Runner accepts an `exclude_cols_extra` keyword; default empty. |

---

## 13. Open questions

- Should irrelevant columns be **correlated** with each other (group of confounded noise)? *Default: no — independent Gaussian noise is the cleanest test.*
- Should we drop a parent **and** add an irrelevant column simultaneously? *Default: no — orthogonal sub-experiments are easier to interpret.*
- Should we test dropping a **non-parent ancestor** (e.g. x0 when target = x2 in `G3-chain`)? *Default: no for interim; would belong in a follow-up.*
- For G3-collider, dropping one parent of x2 produces effectively a chain. Should we run this for fun? *Default: only if compute permits; logged in appendix.*

Resolutions append to the Decisions log in `EXPERIMENTS_PLAN.md`.
