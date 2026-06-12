# QI-001 artefact map (QI001_motifs_modes)

> QI-001 is a qualitative parent-set recovery investigation using the current ABA Learning bridge. It is not full Russo-style Causal ABA, graph recovery, d-separation reasoning, or stable-extension-as-DAG machinery.

Maps the inputs and the expected run outputs for QI-001. Run artefacts do not exist yet; they will be produced by the ABALearn/grid run (see `run_log.md`).

## Inputs (exist now)

| Item | Path |
|---|---|
| Config | `causal/configs/experiments/QI001_motifs_modes.yaml` |
| Fixtures | `causal/experiments/handcrafted_qi001.py` |
| Fixture registration | `causal/experiments/handcrafted.py` |
| Fixture tests | `causal/tests/test_qi001_fixtures.py` |
| Summary script | `causal/scripts/qi001_qualitative_summary.py` |
| Summary tests | `causal/tests/test_qi001_summary.py` |
| Generated summary | `docs/experiments/qualitative/QI-001_summary.md` |

## Output directory (pending)

```text
causal/outputs/aba_learning/grid/QI001_motifs_modes/
  manifest.json            # run manifest (config hash, timing, outcome counts)
  results.parquet          # concatenated per-cell metrics across the 9 cells
  run.log                  # grid run log
  cells/<run_id>/          # one directory per cell (9 total)
```

Each cell's `<run_id>` is derived deterministically by the config expansion (`expand_cells`); the generated summary lists the run_id per cell.

## Expected per-cell artefacts

Under `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/<run_id>/`:

| Artefact | Description |
|---|---|
| `data.csv` | the fixture table written for the cell (the handcrafted table). |
| `bk.aba` | generated ABA background knowledge (feature predicates for non-target columns; `x2` excluded). |
| `bk.sol.aba` | learned solution framework (BK + learned delta rules, assumptions, contraries). Present only if the learner produced a solution. |
| `metrics.json` | per-cell metric panel (outcome, delta/target rule counts, body-parent precision/recall/F1, Python and Prolog-aware coverage, assumptions/contraries counts). |
| `metrics.parquet` | single-row Parquet shard mirroring `metrics.json`. |
| `prolog.stdout` / `prolog.stderr` | captured SWI-Prolog stdout/stderr for the learning run. |

## Encoding per data mode (for reading `bk.aba`)

- binary 0/1 → bare predicates, e.g. `x0(A) :- A=n.`
- categorical (3 values) → value predicates, e.g. `x0_val_2(A) :- A=n.`
- continuous (3 uniform bins) → bin predicates, e.g. `x0_bin2(A) :- A=n.`

In all cells the target `x2` is excluded from BK (`bk.aba` shows `% Skipping excluded variable: x2`).

## Continuous binned-CSV caveat

For the continuous cells (`qi001_chain_cont3`, `qi001_fork_cont3`, `qi001_collider_cont3`), the BK generator writes a binned CSV named `{run_id}.binned.csv`, but the runner only normalizes it to `data.binned.csv` for the `continuous` graph type, not for `handcrafted_table`. So a continuous QI-001 cell may leave a `{run_id}.binned.csv` file un-renamed in its cell directory. This is cosmetic only: the metrics do not read the binned CSV, and parent-set recovery is unaffected.
