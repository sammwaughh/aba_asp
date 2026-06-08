# ABA-ASP Causal Integration

Bridge between **ArgCausalDisco** data generation and the **ABA-ASP** learner (SWI-Prolog/Clingo).

## Overview
End-to-end pipeline for small, reproducible experiments:
- Data Generation: ArgCausalDisco `simulate_discrete_data` / `simulate_linear_continuous_data` produce tabular datasets.
- Predicate Conversion: `aba_asp.utils.data_utils` emits ABA predicates from DataFrames.
- Background Knowledge (BK): `generate_aba_background_knowledge()` writes foldable BK and companion CSVs.
- ABA Learning: `run_aba_asp.ABASPRunner` runs SWI-Prolog/Clingo to learn delta rules; `_extract_learned_rules()` parses them.

## Quick Start
- **Environment:** see [`docs/research/environment_setup.md`](../docs/research/environment_setup.md) (conda env `aba-asp`, pip deps, SWI-Prolog + **clingo** on PATH, ArgCausalDisco sibling repo).
- **Experiment grid** (preferred for scaled runs): see `causal/aa-plans/INFRA.md`.
- Legacy smoke tests: `python causal/test_data_utils_integration.py`, `python causal/test_aba_learning.py`
- Demo pipeline: `python causal/argcausaldisco_integration.py`

### Experiment grid (run_grid)

```bash
conda activate aba-asp
cd "/Users/samuelwaugh/Desktop/Causal ABA Learning/aba_asp"

# Dry-run cell count
python -m causal.experiments.run_grid \
  --config causal/configs/experiments/E00_discrete_smoke.yaml \
  --dry-run

# Full grids: discrete baseline, then continuous mirror
python -m causal.experiments.run_grid \
  --config causal/configs/experiments/E00_discrete_smoke.yaml
python -m causal.experiments.run_grid \
  --config causal/configs/experiments/E00_continuous_smoke.yaml

# Report-ready summary table + heatmap (per experiment)
python causal/scripts/summarize_experiment.py --experiment E00_discrete_smoke
python causal/scripts/summarize_experiment.py --experiment E00_continuous_smoke
```

Outputs: `causal/outputs/aba_learning/grid/<experiment_id>/` (`cells/<run_id>/metrics.json`, `results.parquet`, `run.log`). Summaries are written to `causal/experiments/figures/<experiment_id>_summary.{md,png}`.

## Environment & Setup

Full setup (verified locally): [`docs/research/environment_setup.md`](../docs/research/environment_setup.md).

- Conda env **`aba-asp`**, Python 3.10, pip stack including `pandas`, `numpy`, `pyyaml`, `pyarrow`, `pgmpy`, etc.
- **SWI-Prolog** and **clingo** on `PATH` — both required for learning (clingo is not optional).
- ArgCausalDisco is a **sibling repo**; scripts add its root to `sys.path` automatically. Do not install full `ArgCausalDisco/requirements.txt`.

## What Lives Here
- `argcausaldisco_integration.py`: generate data → predicates → BK → optional ABA-ASP run.
	- Functions: `generate_aba_background_knowledge()`, `pick_target_variable()`, `_extract_learned_rules()`.
- `run_aba_asp.py`: wrapper for SWI-Prolog/Clingo; class `ABASPRunner` executes learning runs.
- `test_data_utils_integration.py`: currently 15 tests covering predicate conversion (discrete/continuous), binary positive-only encoding, counts, and type inference.
- `test_aba_learning.py`: integration runs on handcrafted and ArgCausalDisco datasets (discrete/continuous/folding modes) with target exclusion in BK.

## Background Knowledge (BK)
- Built via `generate_aba_background_knowledge()` (used by both tests and demos).
- Binary 0/1 → only positive cases emit (`x0(A)` when value==1).
- Non-binary discrete → value-specific predicates (`x0_val_7(A)`).
- Continuous → quantile/uniform bins (`x0_binK(A)`).
- `exclude_cols` skips target columns.
- Outputs: `{name}.bk.aba` + `{name}.csv` (+ `{name}.binned.csv` if continuous vars).

### Key Functions
- `generate_aba_background_knowledge(df, var_types, name, output_dir, exclude_cols=None, continuous_bins=2, bin_strategy='quantile')`: writes foldable BK and CSVs.
- `pick_target_variable(df, target_col=None)`: selects target and splits E+/E- atoms using numeric sample IDs.
- `_extract_learned_rules(predicate_file)`: returns delta rules (solution minus BK).

## Typical Flow
1) Generate data with ArgCausalDisco (`simulate_discrete_data` / `simulate_linear_continuous_data`).
2) Map column types (categorical/discrete/binary/continuous).
3) Call `generate_aba_background_knowledge()` to write BK + CSVs.
4) Pick a target and E+/E- with `pick_target_variable()`.
5) Run ABA-ASP via `ABASPRunner.run_prolog_aba_asp()`; inspect learned delta rules with `_extract_learned_rules()`.

## Outputs
- `outputs/argcausaldisco/`: demo pipeline artifacts.
- `outputs/aba_learning/grid/<experiment_id>/`: per-cell metrics and parquet from `run_grid` (do not commit).
- `outputs/aba_learning/`: legacy solution files from `test_aba_learning.py`.

## Running Tests
```bash
# From repo root (aba-asp env active)
python causal/test_data_utils_integration.py
python causal/test_aba_learning.py

# Demo pipeline
python causal/argcausaldisco_integration.py
```

## Tests Overview
- `test_data_utils_integration.py` (purpose: predicate conversion correctness)
	- Discrete and continuous predicate generation
	- Binary variables: positive-only predicate emission
	- Predicate count prediction and type inference
- `test_aba_learning.py` (purpose: end-to-end learning on small datasets)
	- Handcrafted perfect-correlation case (4 samples)
	- ArgCausalDisco discrete chain (6 samples)
	- ArgCausalDisco continuous chain (8 samples), confounder (6), collider (8); median E+/E−; folding mode comparisons

