# QI-004 greedy — operational dossier (QI004_scaled_motifs_n20_greedy)

> Greedy-folding rerun of QI-004 (`QI004_scaled_motifs_n20`). Identical design — 15 handcrafted cells (5 structural configs x 3 data modes, parent-position variants, target `x2` only, `n=20`, `prolog_timeout_s=300`) — with the single conceptual change `folding_mode: nd -> folding_mode: greedy`. Scope: target-wise parent-set recovery under the current `aba_asp/causal` implementation. NOT Russo-style Causal ABA, graph recovery, d-separation, arr/noe/indep, or stable-extension-as-DAG.

## Purpose

Compare parent-set recovery, stability, runtime, and failure modes under **greedy folding** against the nd QI-004 baseline at the feasible scaled/noisy setting, including the position-controlled x0/x1 confound check.

## Only intended conceptual change

`defaults.folding_mode: greedy` (nd config uses `nd` with `folding_steps: 15`). `folding_steps` retained but ignored by greedy. All fixtures, motifs, targets, data modes, sample size (`n=20`), bins, seeds, and the 300s timeout identical to the nd config.

## Greedy cost caveat

Greedy folding is documented as potentially more expensive than nd. The nd QI-004 cat3 cell already took ~270s; greedy cat3/cont3 cells may hit the 300s timeout. If greedy QI-004 repeatedly times out, status is recorded and the run is stopped (no blind reruns).

## Fidelity note

Pipeline-greedy uses engine-default `folding_selection(any)` / `folding_space(all)` / `learning_mode(cautious)`; paper greedy configs additionally set `mgr`/`bk`/`brave`. Changing only `folding_mode` is the faithful single conceptual change at the YAML level.

## Cells

5 structural configs (chain x1parent, chain x0parent, fork x0parent, fork x1parent, collider) x 3 data modes (binary, cat3, cont3) = 15 cells, all target `x2`. Continuous cells binned into 3 uniform bins. The decision-critical comparison is `*_x1parent` vs `*_x0parent`.

## Key paths

| Item | Path |
|---|---|
| Greedy config | `causal/configs/experiments/QI004_scaled_motifs_n20_greedy.yaml` |
| nd config (baseline) | `causal/configs/experiments/QI004_scaled_motifs_n20.yaml` |
| Fixtures | `causal/experiments/handcrafted_qi004.py` |
| Summary script | `causal/scripts/motif_recovery_summary.py` |
| Generated summary | `docs/experiments/qualitative/QI004_scaled_motifs_n20_greedy_summary.md` |
| Output directory | `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20_greedy/` |

## Status

Config + dossier in place. Run, audit, and interpretation performed by this task. Interpretation status initially **pending**.
