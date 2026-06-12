# QI-001 greedy — artefacts

| Item | Path |
|---|---|
| Greedy config | `causal/configs/experiments/QI001_motifs_modes_greedy.yaml` |
| Output directory | `causal/outputs/aba_learning/grid/QI001_motifs_modes_greedy/` |
| Manifest | `causal/outputs/aba_learning/grid/QI001_motifs_modes_greedy/manifest.json` |
| Per-cell metrics | `causal/outputs/aba_learning/grid/QI001_motifs_modes_greedy/cells/<cell>/metrics.json` |
| Generated summary | `docs/experiments/qualitative/QI001_motifs_modes_greedy_summary.md` |

## Cell -> run_id map

| Cell (dgp) | run_id | Outcome | clean_recovery |
|---|---|---|---|
| qi001_chain_binary | `1880fb73b11c` | solved | 0 |
| qi001_fork_binary | `6cf436fdac47` | solved | 0 |
| qi001_collider_binary | `d9f6f951653e` | solved | 1 |
| qi001_chain_cat3 | `6d153efa06f7` | solved | 0 |
| qi001_fork_cat3 | `bb45b82de519` | solved | 0 |
| qi001_collider_cat3 | `40f7a0f10f80` | solved | 1 |
| qi001_chain_cont3 | `5828e8de706f` | solved | 0 |
| qi001_fork_cont3 | `fc07ec7aef7b` | solved | 0 |
| qi001_collider_cont3 | `2dfe8684b040` | solved | 1 |

Every cell has `metrics.json` and a `bk.sol.aba` solution file (all 9 solved).
