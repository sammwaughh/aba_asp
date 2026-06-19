# Greedy vs non-deterministic folding — qualitative handoff (QI-001 / QI-002 / QI-004)

> **Caution.** This document compares two ABA Learning **folding settings** (non-deterministic vs greedy) on identical controlled fixtures, measuring **target-wise parent-set recovery** under the current `aba_asp/causal` implementation. It does **not** establish that either setting performs causal discovery. It does not exercise full Russo-style Causal ABA, graph recovery, d-separation, arr/noe/indep, or stable-extension-as-DAG machinery. "Recovery" means: do the learned `x2` target-rule bodies cite exactly the known direct parents of `x2`.

## Scope and label mapping

This document refers to experiments by repo id (QI-001 / QI-002 / QI-004). For cross-reference, the report-side labels map as QL1 = QI-001, QL2 = QI-002, QL3 = QI-004; the cut `n=100` attempt (QI-003) carries no report label. The greedy reruns are `QI001_motifs_modes_greedy`, `QI002_minimal_motifs_greedy`, `QI004_scaled_motifs_n20_greedy`. QI-003 is **excluded** (cut feasibility attempt, superseded by QI-004). The single conceptual change between each nd run and its greedy counterpart is `defaults.folding_mode: nd -> greedy`; all fixtures, motifs, targets, data modes, sample sizes, bins, seeds, and timeouts are identical.

### Fidelity note

Pipeline-greedy uses the engine-default `folding_selection(any)` / `folding_space(all)` / `learning_mode(cautious)`. The AAMAS paper greedy configs additionally set `mgr`/`bk`/`brave`; those are not exposed in the experiment YAML and were not altered. Changing only `folding_mode` is the faithful single-conceptual-change comparison at the YAML level.

## Run-level comparison

| Investigation | Mode | Folding | Cells | Solved | No solution | Errors | Timeouts | Clean recoveries | Total wall | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| QI-001 | binary/cat3/cont3 | nd | 9 | 9 | 0 | 0 | 0 | n/a* | ≈ 4.0 s | nd predates clean_recovery field |
| QI-001 | binary/cat3/cont3 | greedy | 9 | 9 | 0 | 0 | 0 | 3/9 | ≈ 2.9 s | all 3 colliders clean; chain/fork superset |
| QI-002 | binary/cat3 | nd | 6 | 5 | 1 | 0 | 0 | 3/6 | ≈ 11.9 s | collider_binary no-solution (7.7 s) |
| QI-002 | binary/cat3 | greedy | 6 | 6 | 0 | 0 | 0 | 4/6 | ≈ 2.5 s | collider_binary now solved+clean |
| QI-004 | binary/cat3/cont3, n=20 | nd | 15 | 1 | 12 | 2 | 0 | 0/15 | ≈ 1233 s | cat3/cont3 cells 50–273 s each |
| QI-004 | binary/cat3/cont3, n=20 | greedy | 15 | 1 | 12 | 2 | 0 | 0/15 | ≈ 10.3 s | identical outcomes; ~120x faster |

*QI-001 nd `metrics.json` has `clean_recovery=None` (older schema); its recovery is described qualitatively below.

## Recovery comparison (cell family)

| Cell family | ND recovered | Greedy recovered | Change / interpretation |
|---|---|---|---|
| QI-001 chain (all modes) | cites x0 (non-parent in this orientation); never clean | {x0,x1} `parent_superset` (recall 1.0) | greedy now always includes the true parent x1; still not exact |
| QI-001 fork (all modes) | {x0} clean (parent *is* x0) | {x0,x1} `parent_superset` | greedy adds spurious x1; loses exactness but parent still recovered |
| QI-001 collider (binary) | {x0,x1} clean | {x0,x1} clean | unchanged (both exact) |
| QI-001 collider (cat3, cont3) | partial (clean only in binary) | {x0,x1} clean in all 3 modes | **greedy improved**: collider clean across modes |
| QI-002 chain_binary / fork_binary | exact, clean | exact, clean | unchanged |
| QI-002 collider_binary | **no solution** | **solved, exact, clean** | **greedy improved** (solve rate + recovery + runtime) |
| QI-002 chain_cat3 | non-parent proxy {x0} (clean 0) | {x0,x1} superset (clean 0) | greedy now includes true parent x1 (nd had a pure proxy) |
| QI-002 fork_cat3 | exact {x0}, clean | {x0,x1} superset (clean 0) | **greedy worsened** (spurious x1) |
| QI-002 collider_cat3 | subset {x0} (clean 0) | exact {x0,x1}, clean | **greedy improved** (full parent set) |
| QI-004 chain_x1parent_binary | {x0,x1} superset (clean 0) | {x0,x1} superset (clean 0) | unchanged |
| QI-004 all other cells | no solution / 2 binary errors; clean 0 | identical (no solution / same 2 errors); clean 0 | unchanged recovery; **only runtime differs (~120x)** |

## Headline interpretation

Across QI-001/QI-002/QI-004, switching nd -> greedy is **better or equal on every axis, with one local recovery regression**:

1. **Runtime**: greedy is faster everywhere, and the gap explodes at scale — QI-004 total wall 1233 s -> 10 s (~120x), with no timeouts. The documented "greedy is more expensive" caveat did not materialise on these tasks; greedy was consistently cheaper.
2. **Solve rate**: greedy ≥ nd. The one concrete gain is QI-002 `collider_binary` (nd no-solution -> greedy solved). QI-001 and QI-004 solve counts are unchanged.
3. **Parent-set recovery**: net improvement. QI-002 clean 3/6 -> 4/6; QI-001 colliders become clean in all modes. Greedy's recall is 1.0 on every solved cell (it never drops the true parent), whereas nd sometimes recovered a pure non-parent proxy (QI-002 chain_cat3). The cost is greedy's tendency to add a second literal, which turned QI-002 `fork_cat3` from exact into a superset and keeps QI-001 chain/fork as supersets.
4. **Interpretability**: greedy bodies are more uniform and consistently contain the true parent; nd was more variable and occasionally proxy-only.
5. **Collider/AND-type targets**: greedy is clearly stronger — it recovers the collider cleanly where nd failed (QI-002 binary no-solution; QI-001 collider beyond binary).
6. **At the noisy n=20 scale (QI-004)**: greedy changes *only* runtime. It does not rescue recovery (still 0/15) and the binary `unknown constant` encoding errors persist (an engine BK-encoding issue, folding-mode-independent).

**Verdict: mixed-leaning-better.** Greedy is strictly better on runtime and solve rate, net better on clean recovery (driven by colliders), with a single cell regression (QI-002 fork_cat3) and no change at the hard noisy scale.

## Claim table

| Claim candidate | Supported? | Evidence | Caveat |
|---|---|---|---|
| Greedy folding is substantially faster than nd on these tasks | Yes | QI-004 total wall 1233 s -> 10.3 s; QI-002 11.9 s -> 2.5 s; QI-001 4.0 s -> 2.9 s | Wall-clock on one machine, single run; not a controlled benchmark |
| Greedy can find a stable solution where nd reports none | Yes (one case) | QI-002 `collider_binary`: nd no-solution -> greedy solved+exact | Single cell; noiseless complete-truth-table case |
| Greedy improves clean parent-set recovery overall | Partially | QI-002 clean 3/6 -> 4/6; QI-001 collider clean in all modes | Not graph recovery; QI-001 nd lacks clean_recovery field; one cell regressed |
| Greedy reliably recovers exact minimal parent sets | No | QI-001/QI-002 cat3 chain/fork are supersets; QI-004 0/15 | Greedy tends to over-include a literal |
| Greedy rescues recovery at the noisy n=20 scale | No | QI-004 greedy identical to nd: 0/15 clean, same errors | Only runtime improved |
| Either setting performs causal discovery | No | All metrics are target-rule-body vs known parents | Out of scope by construction |

## Claims not supported (with reasons)

| Claim not supported | Reason |
|---|---|
| Greedy enables causal/graph discovery | No graph-level skeleton/direction metrics computed; scope is target-wise rule-body recovery |
| Greedy fixes the binary encoding errors | The 2 QI-004 binary `unknown constant` errors persist identically under greedy (BK-encoding limitation, not folding-mode) |
| Greedy uniformly improves recovery cell-by-cell | QI-002 `fork_cat3` regressed (exact -> superset); QI-004 unchanged |
| The runtime advantage generalises to all settings | Observed on small handcrafted motifs only; single run, single machine |

## Limitations

- Target-wise parent-set recovery, not causal discovery; single seed; tiny/small samples (QI-001 4–5 rows, QI-002 complete tables, QI-004 n=20).
- Continuous variables are binned (3 uniform bins) before ABA Learning.
- QI-001 nd lacks the `clean_recovery`/`var_parent_*` fields, so its recovery comparison is qualitative.
- Wall-clock figures are from single runs on one machine; treat the runtime story as a strong qualitative signal on the QI fixtures.
- Fidelity caveat: only `folding_mode` was changed; the paper greedy configs additionally set selection/space/learning-mode options not exposed in the YAML.

## Implications for Milestone 1 Part 2 (M1.2)

These qualitative results motivate comparing greedy vs nd on the **m1.1 eight-cell grid** (M11 nd baseline already recorded). The runtime advantage and collider solve/recovery gains on QI fixtures are precedent only; whether greedy changes cat3 σ behaviour on m1.1 is an M1.2 question (claim M11-C-004, tentative). The QI-004 result (greedy = nd in recovery but far cheaper) suggests greedy is worth using for scaling experiments, independent of any recovery claim.

## Artefact paths

| Item | Path |
|---|---|
| Greedy configs | `causal/configs/experiments/QI001_motifs_modes_greedy.yaml`, `QI002_minimal_motifs_greedy.yaml`, `QI004_scaled_motifs_n20_greedy.yaml` |
| Greedy outputs | `causal/outputs/aba_learning/grid/QI001_motifs_modes_greedy/`, `.../QI002_minimal_motifs_greedy/`, `.../QI004_scaled_motifs_n20_greedy/` |
| Greedy summaries | `docs/experiments/qualitative/QI001_motifs_modes_greedy_summary.md`, `QI002_minimal_motifs_greedy_summary.md`, `QI004_scaled_motifs_n20_greedy_summary.md` |
| Greedy dossiers | `docs/experiments/qualitative/QI001_motifs_modes_greedy/`, `QI002_minimal_motifs_greedy/`, `QI004_scaled_motifs_n20_greedy/` |
| nd baselines | `docs/experiments/qualitative/QI002_minimal_motifs_summary.md`, `QI004_scaled_motifs_n20_summary.md`, `QL_interim_handoff.md` (QI-001 nd qualitative) |
| Metrics reference | `causal/aa-plans/METRICS.md` |
