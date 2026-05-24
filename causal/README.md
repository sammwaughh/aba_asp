# ABA-ASP Causal Integration

Bridge between **ArgCausalDisco** data generation and the **ABA-ASP** learner (SWI-Prolog/Clingo).

## Overview
End-to-end pipeline for small, reproducible experiments:
- Data Generation: ArgCausalDisco `simulate_discrete_data` / `simulate_linear_continuous_data` produce tabular datasets.
- Predicate Conversion: `aba_asp.utils.data_utils` emits ABA predicates from DataFrames.
- Background Knowledge (BK): `generate_aba_background_knowledge()` writes foldable BK and companion CSVs.
- ABA Learning: `run_aba_asp.ABASPRunner` runs SWI-Prolog/Clingo to learn delta rules; `_extract_learned_rules()` parses them.

## Quick Start
- Env: `conda run -n aba-env …` with pandas, numpy, ArgCausalDisco; SWI-Prolog at `../swipl/build/src/swipl`.
- Run data-utils tests: `python causal/test_data_utils_integration.py`
- Run ABA learning tests: `python causal/test_aba_learning.py`
- Demo pipeline: `python causal/argcausaldisco_integration.py`

## Environment & Setup
- Requirements: Python 3.9+, conda env (named `aba-env` here), pandas, numpy, ArgCausalDisco (present in repo), optional Clingo.
- SWI-Prolog (for learning): binary at `../swipl/build/src/swipl` or on PATH. The runner auto-configures `SWI_HOME_DIR`/`LD_LIBRARY_PATH` for the Bitbucket build tree.

Create/activate env and install basics:
```bash
conda create -n aba-env -y python=3.9
conda activate aba-env
pip install pandas numpy
```

Optional: verify SWI-Prolog and configure environment (Bitbucket tree):
```bash
/vol/bitbucket/fr920/swipl/build/src/swipl --version
export SWI_HOME_DIR=/vol/bitbucket/fr920/swipl/build/home
export LD_LIBRARY_PATH=/vol/bitbucket/fr920/swipl/build/src:$LD_LIBRARY_PATH
```

Optional: Clingo
```bash
clingo --version
```

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
- `outputs/aba_learning/`: solution files from `test_aba_learning.py`.

## Running Tests
```bash
# From repo root
conda run -n aba-env python causal/test_data_utils_integration.py
conda run -n aba-env python causal/test_aba_learning.py

# Demo pipeline
conda run -n aba-env python causal/argcausaldisco_integration.py
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

