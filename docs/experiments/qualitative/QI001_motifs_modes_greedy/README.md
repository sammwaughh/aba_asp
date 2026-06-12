# QI-001 greedy — operational dossier (QI001_motifs_modes_greedy)

> Greedy-folding rerun of QI-001 (`QI001_motifs_modes`). Identical design — 9 handcrafted cells (3 motifs x 3 data modes, target `x2` only) — with the single conceptual change `folding_mode: nd -> folding_mode: greedy`. Scope: target-wise parent-set recovery under the current `aba_asp/causal` implementation. NOT Russo-style Causal ABA, graph recovery, d-separation, arr/noe/indep, or stable-extension-as-DAG.

## Purpose

Compare parent-set recovery, stability, runtime, and failure modes under **greedy folding** against the non-deterministic (nd) QI-001 baseline, on the same controlled motif-by-data-mode tasks.

## Only intended conceptual change

`defaults.folding_mode: greedy` (the nd config uses `nd` with `folding_steps: 15`). `folding_steps` is retained but ignored by greedy folding. All fixtures, motifs, targets, data modes, sample sizes, bins/bin strategy, seeds, and timeouts are identical to the nd config.

## Fidelity note

Pipeline-greedy uses the engine-default `folding_selection(any)` / `folding_space(all)` / `learning_mode(cautious)`; the paper greedy configs additionally set `mgr`/`bk`/`brave`. Changing only `folding_mode` is the faithful single conceptual change at the YAML level; `folding_selection`/`folding_space` are not YAML-exposed and were not altered.

## Cells

3 motifs (chain, fork, collider) x 3 data modes (binary, cat3, cont3) = 9 cells, all target `x2`. Continuous fixtures binned into 3 uniform bins. Single seed `0`.

## Key paths

| Item | Path |
|---|---|
| Greedy config | `causal/configs/experiments/QI001_motifs_modes_greedy.yaml` |
| nd config (baseline) | `causal/configs/experiments/QI001_motifs_modes.yaml` |
| Fixtures | `causal/experiments/handcrafted.py` (`qi001_*`) |
| Summary script | `causal/scripts/motif_recovery_summary.py` |
| Generated summary | `docs/experiments/qualitative/QI001_motifs_modes_greedy_summary.md` |
| Output directory | `causal/outputs/aba_learning/grid/QI001_motifs_modes_greedy/` |

## Status

Config + dossier in place. Run, audit, and interpretation performed by this task — see `run_log.md`, `interpretation.md`, `decision_record.md`. Interpretation status initially **pending**.
