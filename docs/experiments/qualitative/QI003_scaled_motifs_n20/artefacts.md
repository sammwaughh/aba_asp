# QI-004 artefact map (QI004_scaled_motifs_n20)

> QI-004 is the feasible (`n=20`, `prolog_timeout_s=300`) follow-up to QI-003. It is an ABA Learning-based parent-set recovery investigation, NOT full Russo-style Causal ABA.

## Inputs

| Artefact | Path |
|---|---|
| Config | `causal/configs/experiments/QI004_scaled_motifs_n20.yaml` |
| Fixtures | `causal/experiments/handcrafted_qi004.py` |
| Fixture registration | `causal/experiments/handcrafted.py` |

## Per-cell run outputs

Under `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20/cells/<run_id>/`:

| File | Meaning |
|---|---|
| `bk.aba` | generated background knowledge + examples |
| `bk.sol.aba` | learner solution (delta rules) |
| `metrics.json` | per-cell metrics panel (incl. `clean_recovery`, `var_parent_*`) |
| `metrics.parquet` | per-cell metrics shard |

## Aggregated outputs

| Artefact | Path |
|---|---|
| Results parquet | `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20/results.parquet` |
| Manifest | `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20/manifest.json` |
| Generated summary | `docs/experiments/qualitative/QI004_scaled_motifs_n20_summary.md` |

## Cell -> run_id map

15 cells (from the run; outcomes shown for reference):

| Cell source | run_id | outcome |
|---|---|---|
| `qi004_chain_x0parent_binary` | `545c94e295e2` | completed_no_solution |
| `qi004_chain_x0parent_cat3` | `949bebb31b93` | completed_no_solution |
| `qi004_chain_x0parent_cont3` | `b0eba6936c1c` | completed_no_solution |
| `qi004_chain_x1parent_binary` | `d97c1b0c8c7c` | solved |
| `qi004_chain_x1parent_cat3` | `02db3ecc32e7` | completed_no_solution |
| `qi004_chain_x1parent_cont3` | `907c13b72728` | completed_no_solution |
| `qi004_fork_x0parent_binary` | `853b906f8559` | error (`unknown constant`) |
| `qi004_fork_x0parent_cat3` | `afa56c4e22f6` | completed_no_solution |
| `qi004_fork_x0parent_cont3` | `db3c4aeedc1a` | completed_no_solution |
| `qi004_fork_x1parent_binary` | `50407b0ed3b6` | completed_no_solution |
| `qi004_fork_x1parent_cat3` | `539fc7c15c42` | completed_no_solution |
| `qi004_fork_x1parent_cont3` | `4807c2e15eb8` | completed_no_solution |
| `qi004_collider_binary` | `c3f09aa40a7d` | error (`unknown constant`) |
| `qi004_collider_cat3` | `47e4cdaac0eb` | completed_no_solution |
| `qi004_collider_cont3` | `8d7a241463e1` | completed_no_solution |

Only `d97c1b0c8c7c` (the single `solved` cell) wrote a `bk.sol.aba` solution file. The full per-cell metric table lives in `run_log.md`.
