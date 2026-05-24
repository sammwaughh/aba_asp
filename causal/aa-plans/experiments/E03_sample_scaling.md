# E03 — Sample-size scaling

**Status:** spec, runs after E02 is green.
**Companion docs:** `EXPERIMENTS_PLAN.md`, `METRICS.md`, `INFRA.md`, `REPORT_OUTLINE.md` (F4).
**Role in the plan:** the n-scaling experiment; produces Figure F4 and the data that E09 reuses to assess implied-skeleton scaling.

---

## 1. Question

Holding the DGP and learner knobs fixed, how does ABA-ASP's body-level recovery behaviour change as the sample size n grows?

Specifically:

- Does **`body_parent_f1` increase monotonically with n**, and if so where is the **elbow**?
- Does **`fraction_solved` increase with n** (we expect yes), and how quickly?
- Does **`offgraph_rate` decrease with n** (we expect yes — small n encourages spurious bin-specific rules)?
- Does **`wall_clock_s` grow super-linearly** with n at fixed `folding_steps`?

---

## 2. Hypothesis

1. `body_parent_f1` is **monotone non-decreasing** in n, with an **elbow around n ≈ 25–50** for the 3-node DGPs and **n ≈ 50–100** for the 4-node DGPs.
2. `fraction_solved` increases from <0.4 at n=6 to >0.9 at n ≥ 100 on chain DGPs; the increase is slower on confounder/collider/hub DGPs.
3. `offgraph_rate` is highest at small n (where rules are forced to cite the only available *distinguishing* bin) and decays as n grows.
4. `wall_clock_s` grows roughly **super-linearly** with n because more E+/E- examples means more candidate folds; we expect the growth rate to vary by `folding_mode` (a hook for E07's comparison).
5. The **coverage gap** `cov_gap_pos` shrinks with n: more data means fewer assumption-laden rules.

---

## 3. DGPs included

The full DGP zoo (continuous), identical to E02. Sharing DGPs lets us interpret E03 as "the same E02 question, with n on the x-axis".

- `G3-chain`, `G3-fork`, `G3-collider`, `G4-forkchain`, `G4-hub` — continuous.

---

## 4. Factors varied (the grid)

| Factor | Values |
|--------|--------|
| `dgp` | the 5 DGPs above |
| `target` | all variables of each DGP |
| `n` | **{6, 12, 25, 50, 100, 200}** |
| `seed` | 0 … 29 (30 seeds) |

Note: the **n = 25 column** intentionally overlaps with E02 to provide a *sample-consistency check* (same DGP, target, seed, knobs should yield identical metrics).

---

## 5. Factors held fixed

| Factor | Value | Note |
|--------|-------|------|
| graph_type | continuous | |
| noise_type | gaussian | |
| noise_scale | 1.0 | |
| bins | 2 | |
| bin_strategy | quantile | |
| example_split | median | |
| folding_steps | 15 | may be temporarily lowered for the n=200 column — see Section 9 |
| folding_mode | nd | |
| prolog_timeout_s | 240 | doubled vs E02 to accommodate the n=200 tail |
| query_timeout_s | 5 | |

---

## 6. Seeds

**30 seeds: 0, 1, …, 29.** Same as E02.

For sample consistency, the (dgp, target, seed, n=25) cells in E03 are not re-executed if E02's matching `metrics.json` already exists; the runner reuses them via the resumability mechanism (`INFRA.md §4.5`). The reuse is logged in `manifest.json` for E03.

---

## 7. Metrics & outputs

### Per-cell metrics

Full metric panel from `METRICS.md §3`.

### Aggregate

`groupby(dgp, target, n)`; reduce over seed via median + IQR.

### Figures

- **F4 — n-scaling curves**, one panel per DGP. X-axis: log-spaced n. Y-axis: `body_parent_f1` (median; shaded IQR). Lines: targets within the DGP. Annotation: `fraction_solved` per (DGP, target, n) printed as a small number at each marker.
  - Optional twin panel: `offgraph_rate` on a secondary axis or as inset.

### Tables

- An appendix table T-app-E03 lists median ± IQR per (DGP, target, n) for `body_parent_f1`, `fraction_solved`, `offgraph_rate`, and `wall_clock_s`.

---

## 8. Configuration stub

`causal/configs/experiments/E03_sample_scaling.yaml`:

```yaml
experiment_id: E03_sample_scaling
description: "Sweep n on the DGP zoo at fixed knobs; produces F4."
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
  prolog_timeout_s: 240
  query_timeout_s: 5

dgps:
  - { id: G3-chain,     nodes: 3, edges: [[0,1],[1,2]] }
  - { id: G3-fork,      nodes: 3, edges: [[0,1],[0,2]] }
  - { id: G3-collider,  nodes: 3, edges: [[0,2],[1,2]] }
  - { id: G4-forkchain, nodes: 4, edges: [[0,1],[0,2],[2,3]] }
  - { id: G4-hub,       nodes: 4, edges: [[0,1],[0,2],[0,3]] }

grid:
  n: [6, 12, 25, 50, 100, 200]
  seed: { range: [0, 30] }
  target: all

provenance:
  code_commit_required: true
  resume_from_experiments: [E02_seed_robustness]   # reuse the n=25 cells
```

Total cells (nominal, before resume reuse): `17 targets × 6 n × 30 seeds = 3060`. With E02 reuse: **2550 new cells**.

---

## 9. Estimated cost

| n | Median per cell | Tail per cell | Cells (new) | Median total |
|--:|----------------:|--------------:|------------:|-------------:|
|   6 | 8 s   | 30 s  | 510 | ~1.1 h |
|  12 | 12 s  | 40 s  | 510 | ~1.7 h |
|  25 | 15 s  | 60 s  | 0 (reused) | 0 |
|  50 | 25 s  | 90 s  | 510 | ~3.5 h |
| 100 | 45 s  | 180 s | 510 | ~6.4 h |
| 200 | 90 s  | 360 s | 510 | ~12.8 h |

**Median total: ~25 hours; tail: ~75 hours.** Plan: weekend-long resumable run.

**Contingency:** if the n=200 column blows up, drop `folding_steps` from 15 to 10 *only for n=200* and record the change in the manifest. A second pass at full `folding_steps=15` for n=200 can run later if time permits and is a separate experiment ID.

---

## 10. Pass / learn criteria

E03 passes if:

- [ ] All n columns complete; n=200 may use a lower `folding_steps` as noted above.
- [ ] **Sample-consistency check**: for every (dgp, target, seed) shared between E02 and the n=25 column, the metric panels match byte-for-byte. A mismatch is a runner-determinism bug and blocks downstream experiments.
- [ ] F4 renders end-to-end from `results.parquet`.
- [ ] For each DGP, the n grid spans `fraction_solved` from < 0.5 (small n) to ≥ 0.9 (largest n). If not, the report's "elbow" claim is downgraded.
- [ ] Wall-clock recorded for every cell; the wall-clock-vs-n curve in §6 of the report is plottable.

Learn:

- The actual elbow locations (and whether they coincide with our 3- vs 4-node hypothesis).
- Whether `offgraph_rate` decays as we predict, or stays flat (which would be a *negative* result and an interesting finding).
- Whether wall-clock grows super-linearly under `nd` folding.

---

## 11. Connection to other experiments

- **Reuses:** E02's n=25 cells via the resume mechanism.
- **Feeds:** F4 (report §5.2.2) and indirectly F6 (E09's skeleton-vs-n curve uses the same Parquet).
- **Depends on:** E02 complete.
- **Blocks:** E09 (which assumes E03's per-n cells exist for the skeleton-vs-n analysis).

---

## 12. Risks & contingencies

| # | Risk | Mitigation |
|---|------|------------|
| R-E03-1 | n=200 column dominates wall-clock and runs out of time. | Lower `folding_steps` only for n=200; document the change. |
| R-E03-2 | Sample-consistency check fails. | This is a real determinism bug; halt downstream work, fix runner before continuing. |
| R-E03-3 | `body_parent_f1` curves are not monotone — surprising dips at intermediate n. | Investigate honestly in §6 of the report; do *not* smooth the curves. |
| R-E03-4 | E03 reveals that the n grid is too coarse around the elbow. | A small follow-up experiment `E03b` (extra n values) can be added; not in the interim scope. |

---

## 13. Open questions

- Should we add n = 400 if the n=200 results are still well below the asymptote? *Default: no for the interim; flag as a "next step" in §7 of the report.*
- Should we run a second pass with `noise_scale = 0.5` to see if the elbow shifts? *Default: no — that question lives in E05.*
- Should the wall-clock-vs-n curve be a separate figure in the report? *Default: no — inset of F4 or a discussion-only call-out.*

Resolutions append to the Decisions log in `EXPERIMENTS_PLAN.md`.
