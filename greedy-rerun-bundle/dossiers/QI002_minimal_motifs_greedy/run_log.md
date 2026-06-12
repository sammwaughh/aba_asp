# QI-002 greedy — run log

Greedy-folding rerun of `QI002_minimal_motifs`. Single conceptual change: `folding_mode: greedy`.

## Run configuration

| Field | Value |
|---|---|
| Experiment id | `QI002_minimal_motifs_greedy` |
| Config | `causal/configs/experiments/QI002_minimal_motifs_greedy.yaml` |
| Folding mode | `greedy` (nd baseline: `nd`, `folding_steps: 15`) |
| Graph type | `handcrafted_table` |
| Bins / strategy | 3 / uniform |
| Prolog timeout | 120 s |
| Seed | 0 |
| Target | `x2` |
| Cells planned | 6 |

## Provenance

| Field | Value |
|---|---|
| Date | 2026-06-12 (~12:07 UTC+1) |
| Branch | `sam` |
| Commit (pre-run) | `0468207` |
| Dirty tree | yes (greedy configs/dossiers added this task) |

## Commands

```bash
python -m causal.experiments.run_grid --config causal/configs/experiments/QI002_minimal_motifs_greedy.yaml --dry-run
python -m causal.experiments.run_grid --config causal/configs/experiments/QI002_minimal_motifs_greedy.yaml --no-resume
python causal/scripts/motif_recovery_summary.py --experiment QI002_minimal_motifs_greedy
```

## Environment

- `py-env OK` (pandas, numpy, yaml, pyarrow import)
- SWI-Prolog 10.0.2 (fat-darwin)
- clingo 5.8.0

## Dry-run output

`6 cells planned for QI002_minimal_motifs_greedy`

## Grid output

`done: completed=6 skipped=0 outcomes={'solved': 6}`. No timeouts. Total wall ≈ 2.5 s (per-cell 0.26–0.68 s). Note: nd's `collider_binary` was `completed_no_solution` and took 7.73 s; greedy `solved` it in 0.26 s.

## Summary output

`6 cells: 0 pending, 6 with artefacts` → `docs/experiments/qualitative/QI002_minimal_motifs_greedy_summary.md`.

## Outcome distribution

- `solved`: 6/6 (nd: 5/6 solved, 1 `completed_no_solution`)
- `clean_recovery` = 1: 4/6 (chain_binary, fork_binary, collider_binary, collider_cat3); 0: 2/6 (chain_cat3, fork_cat3 — both `parent_superset`)
- overall clean-recovery rate 0.667 (binary 3/3, cat3 1/3); nd rate 0.500

## Factual status

Run complete; all artefacts present; summary generated. Interpretation: see `interpretation.md`.
