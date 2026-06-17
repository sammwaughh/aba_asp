# QI-004 greedy — run log

Greedy-folding rerun of `QI004_scaled_motifs_n20`. Single conceptual change: `folding_mode: greedy`.

## Run configuration

| Field | Value |
|---|---|
| Experiment id | `QI004_scaled_motifs_n20_greedy` |
| Config | `causal/configs/experiments/QI004_scaled_motifs_n20_greedy.yaml` |
| Folding mode | `greedy` (nd baseline: `nd`, `folding_steps: 15`) |
| Graph type | `handcrafted_table` |
| Bins / strategy | 3 / uniform |
| Sample size | 20 |
| Prolog timeout | 300 s |
| Seed | 0 (tables deterministic via per-fixture internal RNG) |
| Target | `x2` |
| Cells planned | 15 |

## Provenance

| Field | Value |
|---|---|
| Date | 2026-06-12 (~12:08 UTC+1) |
| Branch | `sam` |
| Commit (pre-run) | `0468207` |
| Dirty tree | yes (greedy configs/dossiers added this task) |

## Commands

```bash
python -m causal.experiments.run_grid --config causal/configs/experiments/QI004_scaled_motifs_n20_greedy.yaml --dry-run
python -m causal.experiments.run_grid --config causal/configs/experiments/QI004_scaled_motifs_n20_greedy.yaml --no-resume
python causal/scripts/motif_recovery_summary.py --experiment QI004_scaled_motifs_n20_greedy
```

## Environment

- `py-env OK` (pandas, numpy, yaml, pyarrow import)
- SWI-Prolog 10.0.2 (fat-darwin)
- clingo 5.8.0

## Dry-run output

`15 cells planned for QI004_scaled_motifs_n20_greedy`

## Grid output

`done: completed=15 skipped=0 outcomes={'solved': 1, 'completed_no_solution': 12, 'error': 2}`. **No timeouts.** Total wall ≈ 10.3 s (per-cell ≤ 1.15 s). For comparison, nd QI004 total wall ≈ 1233 s, with individual cat3/cont3 cells taking 50–273 s.

## Outcome distribution

- `solved`: 1/15 (`qi004_chain_x1parent_binary`, `parent_superset` {x0,x1}, clean_recovery 0)
- `completed_no_solution`: 12/15
- `error`: 2/15 (`qi004_fork_x0parent_binary`, `qi004_collider_binary` — `parser_or_metric_failure`; the binary all-zero-positive `unknown constant` encoding limitation, identical cells to nd QI004)
- `clean_recovery` = 0 for all 15 cells (binary 0/5, cat3 0/5, cont3 0/5)

This cell-by-cell distribution (same solved cell, same 2 error cells, same 12 no-solution cells) is **identical to nd QI004**; only runtime differs.

## Summary output

`15 cells: 0 pending, 15 with artefacts` → `docs/experiments/qualitative/QI004_scaled_motifs_n20_greedy_summary.md`.

## Factual status

Run complete; all 15 artefacts present; summary generated. The greedy cost caveat did **not** materialise — greedy was ~120x faster than nd here, with no timeouts. Interpretation: see `interpretation.md`.
