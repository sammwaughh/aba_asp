# QI-002 greedy — interpretation

> Scope: target-wise parent-set recovery under the current `aba_asp/causal` implementation; **not** causal discovery. This compares two learning settings (nd vs greedy folding) on identical noiseless truth-table fixtures.

## Purpose

Greedy-folding rerun of QI-002 (`folding_mode: nd -> greedy`, all else identical) in the **noiseless best case**: complete factorial truth tables where the true parent of `x2` is the unique zero-error separator. This isolates whether the search strategy alone (not noise) changes whether the perfect target rule is found. 6 cells (3 motifs x {binary, cat3}), target `x2`, canonical orientation.

## Raw result summary

- Outcomes: **6/6 solved** (nd: 5/6 solved, 1 `completed_no_solution`).
- Clean-recovery rate: **0.667 (4/6)** — binary 3/3, cat3 1/3. nd rate: 0.500 (3/6).
- Total wall ≈ 2.5 s (per-cell 0.26–0.68 s). nd total ≈ 11.9 s, dominated by the nd `collider_binary` no-solution search at 7.73 s.
- 0 assumptions/contraries/folding-tokens reported on every cell.

## Cell-level table (greedy)

| Cell | Motif | Mode | Parents(x2) | Recovered | clean | Jacc | Outcome |
|---|---|---|---|---|---|---|---|
| qi002_chain_binary | chain | binary | {x1} | {x1} | 1 | 1.00 | solved |
| qi002_fork_binary | fork | binary | {x0} | {x0} | 1 | 1.00 | solved |
| qi002_collider_binary | collider | binary | {x0,x1} | {x0,x1} | 1 | 1.00 | solved |
| qi002_chain_cat3 | chain | cat3 | {x1} | {x0,x1} | 0 | 0.50 | solved |
| qi002_fork_cat3 | fork | cat3 | {x0} | {x0,x1} | 0 | 0.50 | solved |
| qi002_collider_cat3 | collider | cat3 | {x0,x1} | {x0,x1} | 1 | 1.00 | solved |

## Clean-recovery rate

4/6 (0.667). All three binary cells are exact. In cat3, only the collider is exact; chain and fork are `parent_superset` (recall 1.0, precision 0.5).

## Variable-level Jaccard summary

Mean Jaccard 0.83 (four cells 1.0, two cat3 cells 0.5). Recall is 1.0 on every cell.

## Outcome distribution

solved 6 / no-solution 0 / error 0 / timeout 0.

## Notable learned-rule patterns

Binary cells recover the minimal correct body exactly, e.g. `x2(A) :- x1(A).` (chain), `x2(A) :- x0(A), x1(A).` (collider). In cat3, greedy enumerates value-specific conjunctions that include both variables, e.g.:

```prolog
x2(A) :- x0_val_0(A), x1_val_2(A).   % qi002_chain_cat3 (parent x1, but x0 also cited)
x2(A) :- x0_val_1(A), x1_val_2(A).
x2(A) :- x0_val_2(A), x1_val_2(A).
```

The collider cat3 cell recovers the full correct OR-of-conjunctions over both parents (clean).

## Comparison to the non-deterministic QI-002 run

nd QI-002 (from `QI002_minimal_motifs_summary.md` + metrics): clean 3/6; `chain_binary` exact, `fork_binary` exact, `fork_cat3` exact; `collider_binary` **no_solution**; `chain_cat3` **non_parent_or_proxy** ({x0}, a non-parent in this orientation); `collider_cat3` **parent_subset** ({x0} only).

| Cell | nd | greedy | Change |
|---|---|---|---|
| chain_binary | exact (clean 1) | exact (clean 1) | unchanged |
| fork_binary | exact (clean 1) | exact (clean 1) | unchanged |
| collider_binary | **no_solution** (7.73 s) | **solved, exact (clean 1)** (0.26 s) | **improved**: solve rate + recovery + runtime |
| chain_cat3 | non_parent_proxy {x0} (clean 0) | parent_superset {x0,x1} (clean 0) | recovery still not clean, but greedy now **includes the true parent x1** (nd cited only a non-parent) |
| fork_cat3 | exact {x0} (clean 1) | parent_superset {x0,x1} (clean 0) | **worsened**: greedy added a spurious x1 |
| collider_cat3 | parent_subset {x0} (clean 0) | exact {x0,x1} (clean 1) | **improved**: full parent set recovered |

Separated by axis:

- **Runtime improvement**: clear and large in relative terms — total 11.9 s -> 2.5 s, driven by greedy solving `collider_binary` in 0.26 s vs nd's 7.73 s failed search.
- **Solve-rate improvement**: yes — 6/6 vs 5/6. Greedy found a stable solution for `collider_binary` where nd reported no solution.
- **Parent-set-recovery improvement**: net yes — clean 4/6 vs 3/6. Two cells improved (collider in both modes), one regressed (fork_cat3). Greedy's recall is 1.0 on every cell, so it never misses the true parent; nd's `chain_cat3` missed it entirely (pure proxy).
- **Interpretability**: mixed. Greedy bodies are more uniform and always contain the true parent, which aids interpretation; but greedy's tendency to add a second literal turns some otherwise-exact cat3 rules into supersets.
- **Collider/AND recovery**: greedy is clearly better — it recovers the collider (AND-type) target cleanly in **both** modes, where nd failed binary entirely and recovered only a subset in cat3.

**Headline:** in the ideal noiseless case greedy is at least as good as nd and strictly better overall (more solved, higher clean-recovery, faster), with the collider being the decisive win. The lone regression (fork_cat3) shows greedy can over-include literals.
