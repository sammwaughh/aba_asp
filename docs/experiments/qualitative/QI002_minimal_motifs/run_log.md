# QI-002 run log (QI002_minimal_motifs)

> QI-002 is a minimal-baseline parent-set recovery investigation using the current ABA Learning bridge. It is not full Russo-style Causal ABA, graph recovery, d-separation reasoning, or stable-extension-as-DAG machinery.

Factual log of commands. The ABA Learning / grid run is pending.

## Environment / provenance

- Conda environment: `aba-asp`
- SWI-Prolog / clingo: not invoked yet (fixtures/config/summary are Prolog-free).

## Commands run (implemented stage; Prolog-free)

| Command | Status | Output |
|---|---|---|
| `python -m pytest causal/tests/test_qi002_fixtures.py -q` | TBD | TBD |
| `python -m causal.experiments.run_grid --config causal/configs/experiments/QI002_minimal_motifs.yaml --dry-run` | TBD | expect `6 cells planned` |
| `python causal/scripts/motif_recovery_summary.py --experiment QI002_minimal_motifs` | TBD | expect `6 cells: 6 pending, 0 with artefacts` |

(Statuses filled by the validation step; see the implementation report.)

## First ABA Learning run

- Status: pending.
- Command (not yet run): `python -m causal.experiments.run_grid --config causal/configs/experiments/QI002_minimal_motifs.yaml --no-resume`

## Output paths

- Run output directory: `causal/outputs/aba_learning/grid/QI002_minimal_motifs/`
- Per-cell directories: `causal/outputs/aba_learning/grid/QI002_minimal_motifs/cells/<run_id>/`
- Generated summary: `docs/experiments/qualitative/QI002_minimal_motifs_summary.md`
