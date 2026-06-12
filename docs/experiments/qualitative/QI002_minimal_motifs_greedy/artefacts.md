# QI-002 greedy — artefacts

| Item | Path |
|---|---|
| Greedy config | `causal/configs/experiments/QI002_minimal_motifs_greedy.yaml` |
| Output directory | `causal/outputs/aba_learning/grid/QI002_minimal_motifs_greedy/` |
| Manifest | `causal/outputs/aba_learning/grid/QI002_minimal_motifs_greedy/manifest.json` |
| Per-cell metrics | `causal/outputs/aba_learning/grid/QI002_minimal_motifs_greedy/cells/<cell>/metrics.json` |
| Generated summary | `docs/experiments/qualitative/QI002_minimal_motifs_greedy_summary.md` |

## Cell -> run_id map

| Cell (dgp) | run_id | Outcome | clean_recovery |
|---|---|---|---|
| qi002_chain_binary | `2d9a62a1fdb8` | solved | 1 |
| qi002_fork_binary | `a0b74ca06a56` | solved | 1 |
| qi002_collider_binary | `2888186cd619` | solved | 1 |
| qi002_chain_cat3 | `0792aa803222` | solved | 0 |
| qi002_fork_cat3 | `9eefa19b70b7` | solved | 0 |
| qi002_collider_cat3 | `9d8ca2b892cc` | solved | 1 |

Every cell has `metrics.json` and a `bk.sol.aba` solution file (all 6 solved).
