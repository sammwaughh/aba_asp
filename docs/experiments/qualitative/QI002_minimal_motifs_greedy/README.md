# QI-002 greedy — operational dossier (QI002_minimal_motifs_greedy)

> Greedy-folding rerun of QI-002 (`QI002_minimal_motifs`). Identical design — 6 handcrafted cells (3 motifs x 2 data modes, target `x2` only; complete factorial over (x0,x1) repeated so the true parent is the unique zero-error separator) — with the single conceptual change `folding_mode: nd -> folding_mode: greedy`. Scope: target-wise parent-set recovery under the current `aba_asp/causal` implementation. NOT Russo-style Causal ABA, graph recovery, d-separation, arr/noe/indep, or stable-extension-as-DAG.

## Purpose

Compare parent-set recovery, stability, runtime, and failure modes under **greedy folding** against the nd QI-002 baseline in the noiseless best case (where the perfect target rule is realisable).

## Only intended conceptual change

`defaults.folding_mode: greedy` (nd config uses `nd` with `folding_steps: 15`). `folding_steps` retained but ignored by greedy. All fixtures, motifs, targets, data modes, bins, seeds, and timeouts identical to the nd config.

## Fidelity note

Pipeline-greedy uses engine-default `folding_selection(any)` / `folding_space(all)` / `learning_mode(cautious)`; paper greedy configs additionally set `mgr`/`bk`/`brave`. Changing only `folding_mode` is the faithful single conceptual change at the YAML level.

## Cells

3 motifs (chain, fork, collider) x 2 data modes (binary, cat3) = 6 cells, all target `x2`. Single seed `0`. (Same complete-factorial design as the nd QI-002: this is a principled **data-level** correction against the x0 confound — non-parents are decorrelated from `x2`, so the chain cell is a positional-bias probe — but it does NOT provide the full *symmetric* break via a parent-position swap; that is QI-004 greedy's job. See `QI-002.md` → "Confound treatment (corrected framing)".)

## Key paths

| Item | Path |
|---|---|
| Greedy config | `causal/configs/experiments/QI002_minimal_motifs_greedy.yaml` |
| nd config (baseline) | `causal/configs/experiments/QI002_minimal_motifs.yaml` |
| Fixtures | `causal/experiments/handcrafted.py` (`qi002_*`) |
| Summary script | `causal/scripts/motif_recovery_summary.py` |
| Generated summary | `docs/experiments/qualitative/QI002_minimal_motifs_greedy_summary.md` |
| Output directory | `causal/outputs/aba_learning/grid/QI002_minimal_motifs_greedy/` |

## Status

Config + dossier in place. Run, audit, and interpretation performed by this task. Interpretation status initially **pending**.
