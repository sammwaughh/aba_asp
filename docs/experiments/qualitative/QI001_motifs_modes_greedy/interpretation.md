# QI-001 greedy — interpretation

> Scope: target-wise parent-set recovery under the current `aba_asp/causal` implementation; **not** causal discovery (no graph recovery, d-separation, arr/noe/indep, or stable-extension-as-DAG). This compares two learning settings (nd vs greedy folding) on identical fixtures.

## Purpose

Greedy-folding rerun of QI-001 (`folding_mode: nd -> greedy`, all else identical) to test whether greedy learning changes parent-set recovery, stability, runtime, or failure modes on the 9 motif x data-mode cells (3 motifs x {binary, cat3, cont3}, target `x2`).

## Raw result summary

- Outcomes: **9/9 solved**, no timeouts, no errors.
- Clean-recovery rate: **0.333 (3/9)** — binary 1/3, cat3 1/3, cont3 1/3.
- The 3 clean cells are exactly the three **collider** cells (all modes); all chain and fork cells are `parent_superset` (recovered {x0,x1} where the true parent is a single variable).
- Total wall ≈ 2.9 s (per-cell 0.30–0.38 s); 0 assumptions/contraries/folding-tokens reported on every cell.

## Cell-level table

| Cell | Motif | Mode | Parents(x2) | Recovered | clean | Jacc | P | R | Outcome |
|---|---|---|---|---|---|---|---|---|---|
| qi001_chain_binary | chain | binary | {x1} | {x0,x1} | 0 | 0.50 | 0.50 | 1.00 | solved |
| qi001_fork_binary | fork | binary | {x0} | {x0,x1} | 0 | 0.50 | 0.50 | 1.00 | solved |
| qi001_collider_binary | collider | binary | {x0,x1} | {x0,x1} | 1 | 1.00 | 1.00 | 1.00 | solved |
| qi001_chain_cat3 | chain | cat3 | {x1} | {x0,x1} | 0 | 0.50 | 0.50 | 1.00 | solved |
| qi001_fork_cat3 | fork | cat3 | {x0} | {x0,x1} | 0 | 0.50 | 0.50 | 1.00 | solved |
| qi001_collider_cat3 | collider | cat3 | {x0,x1} | {x0,x1} | 1 | 1.00 | 1.00 | 1.00 | solved |
| qi001_chain_cont3 | chain | cont3 | {x1} | {x0,x1} | 0 | 0.50 | 0.50 | 1.00 | solved |
| qi001_fork_cont3 | fork | cont3 | {x0} | {x0,x1} | 0 | 0.50 | 0.50 | 1.00 | solved |
| qi001_collider_cont3 | collider | cont3 | {x0,x1} | {x0,x1} | 1 | 1.00 | 1.00 | 1.00 | solved |

## Clean-recovery rate

3/9 (0.333), uniform across data modes. Every miss is a `parent_superset` (recall 1.0, precision 0.5): the true parent is always cited, but a non-parent is also included.

## Variable-level Jaccard summary

Mean Jaccard 0.67 (collider cells 1.0; chain/fork cells 0.5). Recall is 1.0 on every solved cell (greedy never drops the true parent); precision is the limiting factor on chain/fork (0.5).

## Outcome distribution

solved 9 / no-solution 0 / error 0 / timeout 0.

## Notable learned-rule patterns

Greedy consistently learns 2-variable conjunctive bodies even when the true parent set is a singleton, e.g.:

```prolog
x2(A) :- x1(A).            % qi001_chain_binary (also keeps x2(A) :- x0(A), x1(A).)
x2(A) :- x0(A), x1(A).
```

For colliders the 2-variable body is exactly correct, so colliders recover cleanly in all three modes. For chain/fork the extra literal makes the body a superset. The tiny QI-001 tables (4–5 rows) under-constrain the search, so adding the second variable is consistent with the data.

## Comparison to the non-deterministic QI-001 run

**Important caveat:** the nd QI-001 run predates the `clean_recovery` / `var_parent_*` metric fields (its `metrics.json` has `clean_recovery=None`), so a strict numeric clean-recovery comparison is not available from stored nd artefacts. The nd qualitative description (from `QL_interim_handoff.md`) is: fork recovered cleanly in every mode, collider recovered fully only in binary, chain essentially never recovered its true parent.

| Axis | nd QI-001 (qualitative) | greedy QI-001 | Change |
|---|---|---|---|
| Solve rate | 9/9 solved | 9/9 solved | unchanged |
| Runtime | ≈ 4.0 s total | ≈ 2.9 s total | slightly faster |
| Error/timeout | none | none | unchanged |
| Recovery pattern | fork clean (all modes), collider clean (binary only), chain never clean | **collider clean (all modes)**; chain/fork `parent_superset` (recall 1.0) | shifted: collider improved across modes; fork no longer "clean" but its parent is still recovered (superset) |
| Interpretability | nd chain cited `x0` (a non-parent proxy in this orientation) | greedy always includes the true parent (superset), never a pure proxy | greedy bodies are arguably more faithful (always contain the parent) |

- **Runtime improvement**: marginal here (both runs are sub-second per cell).
- **Solve-rate improvement**: none (both 9/9).
- **Parent-set-recovery change**: greedy makes colliders clean in all modes (nd was binary-only) but turns fork from clean into a superset. Net clean count is similar; the *distribution* differs. Greedy's recall is 1.0 everywhere, so it never misses the true parent — unlike nd's chain, which cited a non-parent.
- **Interpretability**: greedy is more uniform/predictable (always a 2-literal body, always containing the parent); nd was more variable.

Caveat on the confound: QI-001 has the unbroken x0/first-column confound (fork's parent *is* x0), so neither run distinguishes "recovers the parent" from "prefers x0" here. That separation is the job of QI-004 (parent-position variants).
