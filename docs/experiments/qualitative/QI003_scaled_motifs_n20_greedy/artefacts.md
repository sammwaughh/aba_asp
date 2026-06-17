# QI-004 greedy — artefacts

| Item | Path |
|---|---|
| Greedy config | `causal/configs/experiments/QI004_scaled_motifs_n20_greedy.yaml` |
| Output directory | `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20_greedy/` |
| Manifest | `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20_greedy/manifest.json` |
| Per-cell metrics | `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20_greedy/cells/<cell>/metrics.json` |
| Generated summary | `docs/experiments/qualitative/QI004_scaled_motifs_n20_greedy_summary.md` |

## Cell -> run_id map

| Cell (dgp) | run_id | Outcome | clean_recovery | wall_s |
|---|---|---|---|---|
| qi004_chain_x1parent_binary | `34cb7dc162d4` | solved | 0 | 0.54 |
| qi004_chain_x1parent_cat3 | `4d12a21aff90` | completed_no_solution | 0 | 0.76 |
| qi004_chain_x1parent_cont3 | `2f9727611d49` | completed_no_solution | 0 | 0.88 |
| qi004_chain_x0parent_binary | `a9a29cfd0182` | completed_no_solution | 0 | 0.97 |
| qi004_chain_x0parent_cat3 | `b87948a29834` | completed_no_solution | 0 | 0.67 |
| qi004_chain_x0parent_cont3 | `7998f97b0dc2` | completed_no_solution | 0 | 0.76 |
| qi004_fork_x0parent_binary | `ea216a6f0a77` | error | 0 | 0.05 |
| qi004_fork_x0parent_cat3 | `741c998a06e8` | completed_no_solution | 0 | 0.77 |
| qi004_fork_x0parent_cont3 | `649f1c294e68` | completed_no_solution | 0 | 0.73 |
| qi004_fork_x1parent_binary | `1a4632a5897c` | completed_no_solution | 0 | 1.15 |
| qi004_fork_x1parent_cat3 | `a5e30417c45a` | completed_no_solution | 0 | 0.57 |
| qi004_fork_x1parent_cont3 | `a60974b69490` | completed_no_solution | 0 | 0.73 |
| qi004_collider_binary | `644721f488da` | error | 0 | 0.05 |
| qi004_collider_cat3 | `ab531f5536c3` | completed_no_solution | 0 | 0.95 |
| qi004_collider_cont3 | `fbc19a5e15cc` | completed_no_solution | 0 | 0.74 |

Solution file (`bk.sol.aba`) present only for the 1 solved cell (`qi004_chain_x1parent_binary`). The 2 `error` cells produced no solution (binary `unknown constant`); the 12 `completed_no_solution` cells ran to completion with no stable solution.
