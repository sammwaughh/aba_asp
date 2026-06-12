# QI-002 artefact map (QI002_minimal_motifs)

> QI-002 is a minimal-baseline parent-set recovery investigation using the current ABA Learning bridge. It is not full Russo-style Causal ABA.

## Inputs

| Artefact | Path |
|---|---|
| Config | `causal/configs/experiments/QI002_minimal_motifs.yaml` |
| Fixtures | `causal/experiments/handcrafted_qi002.py` |
| Fixture registration | `causal/experiments/handcrafted.py` |

## Per-cell run outputs (after the ABA Learning run)

Under `causal/outputs/aba_learning/grid/QI002_minimal_motifs/cells/<run_id>/`:

| File | Meaning |
|---|---|
| `bk.aba` | generated background knowledge + examples |
| `bk.sol.aba` | learner solution (delta rules) |
| `metrics.json` | per-cell metrics panel (incl. `clean_recovery`, `var_parent_*`) |
| `metrics.parquet` | per-cell metrics shard |

## Aggregated outputs

| Artefact | Path |
|---|---|
| Results parquet | `causal/outputs/aba_learning/grid/QI002_minimal_motifs/results.parquet` |
| Manifest | `causal/outputs/aba_learning/grid/QI002_minimal_motifs/manifest.json` |
| Generated summary | `docs/experiments/qualitative/QI002_minimal_motifs_summary.md` |

## Cell -> run_id map

Filled after the run from the manifest. Cells: `qi002_chain_binary`, `qi002_fork_binary`, `qi002_collider_binary`, `qi002_chain_cat3`, `qi002_fork_cat3`, `qi002_collider_cat3`.
