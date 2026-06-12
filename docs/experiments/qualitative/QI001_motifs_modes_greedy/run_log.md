# QI-001 greedy — run log

Greedy-folding rerun of `QI001_motifs_modes`. Single conceptual change: `folding_mode: greedy`.

## Run configuration

| Field | Value |
|---|---|
| Experiment id | `QI001_motifs_modes_greedy` |
| Config | `causal/configs/experiments/QI001_motifs_modes_greedy.yaml` |
| Folding mode | `greedy` (nd baseline: `nd`, `folding_steps: 15`) |
| Graph type | `handcrafted_table` |
| Bins / strategy | 3 / uniform |
| Sample size | per-fixture (qi001 builders) |
| Prolog timeout | 120 s |
| Seed | 0 |
| Target | `x2` |
| Cells planned | 9 |

## Provenance

| Field | Value |
|---|---|
| Date | 2026-06-12 (~12:07 UTC+1) |
| Branch | `sam` |
| Commit (pre-run) | `0468207` |
| Dirty tree | yes (greedy configs/dossiers added this task) |

## Commands

```bash
python -m causal.experiments.run_grid --config causal/configs/experiments/QI001_motifs_modes_greedy.yaml --dry-run
python -m causal.experiments.run_grid --config causal/configs/experiments/QI001_motifs_modes_greedy.yaml --no-resume
python causal/scripts/motif_recovery_summary.py --experiment QI001_motifs_modes_greedy
```

## Environment

- `py-env OK` (pandas, numpy, yaml, pyarrow import)
- SWI-Prolog 10.0.2 (fat-darwin)
- clingo 5.8.0

## Dry-run output

`9 cells planned for QI001_motifs_modes_greedy`

## Grid output

`done: completed=9 skipped=0 outcomes={'solved': 9}`. No timeouts. Total wall ≈ 2.9 s across 9 cells (per-cell 0.30–0.38 s).

## Summary output

`9 cells: 0 pending, 9 with artefacts` → `docs/experiments/qualitative/QI001_motifs_modes_greedy_summary.md`.

## Outcome distribution

- `solved`: 9/9
- `clean_recovery` = 1: 3/9 (all three collider cells); 0: 6/9 (all chain + fork cells, `parent_superset`)
- overall clean-recovery rate 0.333 (binary 1/3, cat3 1/3, cont3 1/3)

## Factual status

Run complete; all artefacts present; summary generated. Interpretation: see `interpretation.md`.
