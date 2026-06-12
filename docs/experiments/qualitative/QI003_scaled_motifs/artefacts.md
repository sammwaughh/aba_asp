# QI-003 artefact map (QI003_scaled_motifs)

> QI-003 is a scaled, confound-controlled parent-set recovery investigation using the current ABA Learning bridge. It is not full Russo-style Causal ABA.

## Inputs

| Artefact | Path |
|---|---|
| Config | `causal/configs/experiments/QI003_scaled_motifs.yaml` |
| Fixtures | `causal/experiments/handcrafted_qi003.py` |
| Fixture registration | `causal/experiments/handcrafted.py` |

## Per-cell run outputs (after the ABA Learning run)

Under `causal/outputs/aba_learning/grid/QI003_scaled_motifs/cells/<run_id>/`:

| File | Meaning |
|---|---|
| `bk.aba` | generated background knowledge + examples |
| `bk.sol.aba` | learner solution (delta rules) |
| `metrics.json` | per-cell metrics panel (incl. `clean_recovery`, `var_parent_*`) |
| `metrics.parquet` | per-cell metrics shard |

## Aggregated outputs

| Artefact | Path |
|---|---|
| Results parquet | `causal/outputs/aba_learning/grid/QI003_scaled_motifs/results.parquet` |
| Manifest | `causal/outputs/aba_learning/grid/QI003_scaled_motifs/manifest.json` |
| Generated summary | `docs/experiments/qualitative/QI003_scaled_motifs_summary.md` |

## Cell -> run_id map

Filled after the run from the manifest. 15 cells: chain/fork x {x0parent, x1parent} x {binary, cat3, cont3} plus collider x {binary, cat3, cont3}.
