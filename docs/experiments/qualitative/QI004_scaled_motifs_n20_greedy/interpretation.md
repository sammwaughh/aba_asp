# QI-004 greedy — interpretation

> Scope: target-wise parent-set recovery under the current `aba_asp/causal` implementation; **not** causal discovery. This compares two learning settings (nd vs greedy folding) on identical scaled/noisy (`n=20`) fixtures.

## Purpose

Greedy-folding rerun of QI-004 (`folding_mode: nd -> greedy`, all else identical) at the feasible scaled/noisy setting: 15 cells (5 structural configs x {binary, cat3, cont3}), `n=20`, parent-position variants, target `x2`, 300s timeout. Tests whether greedy changes recovery, the x0/x1 confound behaviour, runtime, solve rate, error rate, or interpretability — and whether the documented greedy cost caveat materialises.

## Raw result summary

- Outcomes: **1 solved, 12 completed_no_solution, 2 error** — clean_recovery **0/15** (binary 0/5, cat3 0/5, cont3 0/5).
- The single solved cell is `qi004_chain_x1parent_binary`: body `{x0,x1}`, `parent_superset` (parent is {x1}), clean_recovery 0.
- The 2 errors are `qi004_fork_x0parent_binary` and `qi004_collider_binary` — the binary all-zero-positive `unknown constant` encoding limitation (an engine BK-encoding issue, independent of folding mode).
- **No timeouts.** Total wall ≈ 10.3 s (per-cell ≤ 1.15 s).

## Cell-level table (greedy)

| Cell | Motif/variant | Mode | Parents | Recovered | clean | Outcome | wall_s |
|---|---|---|---|---|---|---|---|
| qi004_chain_x1parent_binary | chain x1 | binary | {x1} | {x0,x1} | 0 | solved | 0.54 |
| qi004_chain_x1parent_cat3 | chain x1 | cat3 | {x1} | {} | 0 | no_solution | 0.76 |
| qi004_chain_x1parent_cont3 | chain x1 | cont3 | {x1} | {} | 0 | no_solution | 0.88 |
| qi004_chain_x0parent_binary | chain x0 | binary | {x0} | {} | 0 | no_solution | 0.97 |
| qi004_chain_x0parent_cat3 | chain x0 | cat3 | {x0} | {} | 0 | no_solution | 0.67 |
| qi004_chain_x0parent_cont3 | chain x0 | cont3 | {x0} | {} | 0 | no_solution | 0.76 |
| qi004_fork_x0parent_binary | fork x0 | binary | {x0} | {} | 0 | error | 0.05 |
| qi004_fork_x0parent_cat3 | fork x0 | cat3 | {x0} | {} | 0 | no_solution | 0.77 |
| qi004_fork_x0parent_cont3 | fork x0 | cont3 | {x0} | {} | 0 | no_solution | 0.73 |
| qi004_fork_x1parent_binary | fork x1 | binary | {x1} | {} | 0 | no_solution | 1.15 |
| qi004_fork_x1parent_cat3 | fork x1 | cat3 | {x1} | {} | 0 | no_solution | 0.57 |
| qi004_fork_x1parent_cont3 | fork x1 | cont3 | {x1} | {} | 0 | no_solution | 0.73 |
| qi004_collider_binary | collider | binary | {x0,x1} | {} | 0 | error | 0.05 |
| qi004_collider_cat3 | collider | cat3 | {x0,x1} | {} | 0 | no_solution | 0.95 |
| qi004_collider_cont3 | collider | cont3 | {x0,x1} | {} | 0 | no_solution | 0.74 |

Continuous bin-health: cont3 cells use the same `n=20`, 3-uniform-bin fixtures as nd QI-004 (pre-verified all bins non-empty); binning is not the proximate cause of the no-solutions here.

## Clean-recovery rate

0/15 (0.000) in every data mode — identical to nd QI-004.

## Variable-level Jaccard summary

Defined only for the 1 solved cell: Jaccard 0.50 (recall 1.0, precision 0.5; `parent_superset`). All other cells have no recovered variables.

## Outcome distribution

solved 1 / no-solution 12 / error 2 / timeout 0.

## Notable learned-rule patterns

Only one cell yields any `x2` rule:

```prolog
x2(A) :- x0(A), x1(A).   % qi004_chain_x1parent_binary
x2(A) :- x1(A).
```

The true parent (x1) is recovered, but x0 is also cited (superset). Every other cell produces no `x2`-headed target rule under the noisy `n=20` tables.

## Comparison to the non-deterministic QI-004 run

The per-cell outcome and recovery map is **identical** to nd QI-004: same single solved cell (`chain_x1parent_binary`, `parent_superset`), same 2 binary error cells (`fork_x0parent_binary`, `collider_binary`), same 12 `completed_no_solution`, clean_recovery 0 everywhere. The **only** material difference is runtime.

| Axis | nd QI-004 | greedy QI-004 | Change |
|---|---|---|---|
| Solve rate | 1/15 | 1/15 | unchanged |
| No-solution | 12/15 | 12/15 | unchanged |
| Errors | 2/15 (binary unknown-constant) | 2/15 (same cells) | unchanged |
| Timeouts | 0 | 0 | unchanged |
| Clean recovery | 0/15 | 0/15 | unchanged |
| Runtime (total wall) | ≈ 1233 s (cat3/cont3 cells 50–273 s) | ≈ 10.3 s (all ≤ 1.15 s) | **~120x faster** |

Separated by axis:

- **Runtime improvement**: dramatic and unambiguous — the expensive nd cat3/cont3 searches (e.g. `collider_cat3` 272.8 s, `chain_x1parent_cat3` 196.8 s) collapse to <1 s under greedy. The documented "greedy is more expensive" caveat **did not** apply at this scale; greedy was far cheaper.
- **Solve-rate improvement**: none.
- **Parent-set-recovery improvement**: none (0/15 both).
- **Interpretability**: unchanged (only the same one superset rule).
- **Collider/AND recovery**: neither setting recovers the collider at `n=20` (no-solution in cat3/cont3; binary errors out).
- **Categorical/continuous cases**: both settings fail to find a stable solution; greedy simply fails *faster*.

**Headline:** at the scaled/noisy setting greedy changes **only runtime** — a large win in compute (no timeouts, ~120x faster) but **no improvement in recovery, solve rate, or error rate**. The 0/15 clean-recovery and the binary encoding errors are properties of the data/encoding at `n=20`, not of the folding strategy. This is consistent with the nd QI-004 conclusion: at this scale the current implementation does not recover parent sets, and greedy does not rescue it.
