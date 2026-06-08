# Environment setup (aba-asp)

Canonical record of the **working local environment** for this repository, verified on macOS Apple Silicon (June 2026). For how to run pipelines after setup, see [`execution_guide.md`](execution_guide.md).

## Workspace layout

| Path | Role |
|------|------|
| `/Users/samuelwaugh/Desktop/Causal ABA Learning/aba_asp` | Main project — run all commands from here |
| `/Users/samuelwaugh/Desktop/Causal ABA Learning/ArgCausalDisco` | Sibling dependency — data generation only |

ArgCausalDisco is **not** inside `aba_asp`. Do not install `ArgCausalDisco/requirements.txt` for aba_asp work; that file is for full paper reproduction (torch, gcastle, notears, cdt/R, etc.).

---

## 1. Conda environment

```bash
conda create -n aba-asp -y python=3.10
conda activate aba-asp
cd "/Users/samuelwaugh/Desktop/Causal ABA Learning/aba_asp"
```

- **Name:** `aba-asp` (not `aba-env` — older docs used the wrong name).
- **Python:** 3.10.

---

## 2. Python packages (pip)

Minimal stack for the causal bridge and grid harness:

```bash
pip install pandas numpy pyyaml pyarrow matplotlib networkx igraph pgmpy scikit-learn pillow pytest
```

| Package | Used for |
|---------|----------|
| `pandas`, `numpy` | Bridge, simulators, metrics |
| `pyyaml` | Experiment YAML configs |
| `pyarrow` | Grid `metrics.parquet` / `results.parquet` |
| `matplotlib` | `causal/scripts/summarize_experiment.py` |
| `networkx`, `igraph`, `pgmpy`, `scikit-learn`, `pillow` | ArgCausalDisco `data_utils` module-level imports |
| `pytest` | `causal/tests/` |

---

## 3. SWI-Prolog

**Required** for all ABA learning runs.

On macOS Apple Silicon, `conda install -c conda-forge swi-prolog` **failed** (`PackagesNotFoundError` — package not on conda-forge for `osx-arm64`).

**Working setup:** system/Homebrew SWI-Prolog on `PATH`:

```bash
swipl --version
# SWI-Prolog version 10.0.2 for fat-darwin
```

Ensure `swipl` is visible whenever `aba-asp` is active. The inherited root `README.md` describes building SWI-Prolog from source; that is optional if a system install works.

**Caveat:** `causal/run_aba_asp.py` may override `SWI_HOME_DIR` / `LD_LIBRARY_PATH` for a hard-coded cluster build tree. If the **Python** runner fails while `swipl --version` works in the shell, the likely fix is to gate `_swipl_env()` so Homebrew/system swipl can self-locate. Do not change that code unless the Python runner actually fails.

---

## 4. Clingo

**Required** — not optional. Earlier notes that clingo was only needed for an alternate ASP path were wrong.

Normal `aba_asp/3` learning loads `asp_engine.pl`, which shells out via SWI-Prolog `shell/2`:

```text
clingo asp.clingo --out-ifs=, ...
```

RoLe and GEN/folding call `compute_conseq/2`, `entails/5`, and `subsumed/6`, all of which depend on clingo output. If clingo is missing, runs may print `* No solution found!` rather than a clear “clingo not found” error.

**Working setup:**

```bash
clingo --version
# clingo version 5.8.0
```

Install into the conda env if not already on `PATH`:

```bash
conda install -n aba-asp -y -c conda-forge clingo
```

Clingo must be on the `PATH` inherited by SWI-Prolog subprocesses (same activated environment or system PATH).

---

## 5. ArgCausalDisco dependency

aba_asp uses ArgCausalDisco **only as a data-generation library**.

**Relevant imports:**

```python
from ArgCausalDisco.utils.data_utils import (
    simulate_discrete_data,
    simulate_linear_continuous_data,
)
```

`simulate_dag` may be imported by integration code but is not central to current smoke-tested workflows.

**Do not** `pip install -r ArgCausalDisco/requirements.txt` for aba_asp.

### Path / import rules

- **Do not** set a global `PYTHONPATH`.
- **Do not** add `aba_asp/` globally to `PYTHONPATH`.

There is a **`utils` namespace collision**:

- `aba_asp/utils/` — imported as `aba_asp.utils.*`
- `ArgCausalDisco/utils/` — ArgCausalDisco uses bare `from utils.helpers import ...`

Scripts such as `causal/experiments/run_grid.py` and `causal/argcausaldisco_integration.py` add to `sys.path`:

1. `aba_asp/` repo root  
2. Workspace root (`Causal ABA Learning/`)  
3. `ArgCausalDisco/` root (required for bare `utils.*` imports)

For **manual one-liners**, insert both workspace root and `ArgCausalDisco/` — see smoke tests below.

### Compatibility edit (applied)

In `ArgCausalDisco/utils/data_utils.py`, heavy baseline imports were moved **inside** the functions that use them:

- `from cd_algorithms.models import pc` → inside `simulate_data_and_run_PC`
- `from utils.graph_utils import is_dag` → inside `simulate_dag`

This avoids pulling in gcastle/castle, notears, cdt/R, causal-learn, etc. when importing the simulators. Simulator behaviour is unchanged.

**Remaining module-level import:** `from utils.helpers import random_stability` (used by BN-loading helpers, not by the simulators). Manual imports still need `ArgCausalDisco/` on `sys.path`.

---

## 6. Smoke tests (verified)

Run from `aba_asp/` with `conda activate aba-asp`.

### Python environment

```bash
python -c "import pandas, numpy, yaml, pyarrow; print('py-env OK')"
```

Expected: `py-env OK`

### SWI-Prolog

```bash
swipl --version
```

Expected: `SWI-Prolog version 10.0.2 for fat-darwin` (or similar)

### Clingo

```bash
clingo --version
```

Expected: `clingo version 5.8.0` (or similar)

### Core Python tests (no Prolog)

```bash
python -m pytest causal/tests/test_config.py causal/tests/test_expand_cells.py \
  causal/tests/test_metrics.py causal/tests/test_results.py -q
```

Expected: `49 passed`

### ArgCausalDisco simulator import

Requires **both** workspace root and `ArgCausalDisco/` on `sys.path`:

```bash
python -c "
import sys
from pathlib import Path
ws = Path('..').resolve()
sys.path.insert(0, str(ws / 'ArgCausalDisco'))
sys.path.insert(0, str(ws))
from ArgCausalDisco.utils.data_utils import simulate_discrete_data
import numpy as np
d = simulate_discrete_data(3, 6, {(0,1),(1,2)}, random_seed=42)
print('argcausaldisco import OK', np.asarray(d).shape)
"
```

Expected: `argcausaldisco import OK (6, 3)`  
A harmless pgmpy `FutureWarning` about `StructureScore` may appear.

Grid and integration scripts set paths automatically; use the one-liner only for ad-hoc checks.

### Grid dry-run

```bash
python -m causal.experiments.run_grid \
  --config causal/configs/experiments/E00_discrete_smoke.yaml \
  --dry-run
```

Expected: `36 cells planned for E00_discrete_smoke`

Cell count: 3 DGPs (chain, fork, collider) × 4 seeds (0–3) × 3 targets (`x0`, `x1`, `x2`) = **36**.

### Canonical Prolog learner (`flies_birds`)

```bash
swipl -q -g "consult('aba_asp.pl'), \
aba_asp('./examples/flies_birds.bk', \
  [flies(woodstock),flies(gwaihir),flies(x_pingu),flies(x_pinga)], \
  [flies(pingu),flies(pinga)]), halt." -t "halt(1)"
```

Expected:

- Learning trace (folding, assumptions, contraries)
- `checking entailment ... OK` (clingo)
- `Writing solution no. 1 to ./examples/flies_birds.bk.sol.aba`

BK argument is the **stem without `.aba`** (`./examples/flies_birds.bk`).

---

## 7. Optional next checks (not yet run in verification)

```bash
python causal/test_data_utils_integration.py
python causal/test_aba_learning.py   # needs swipl + clingo; longer
python -m causal.experiments.run_grid \
  --config causal/configs/experiments/E00_discrete_smoke.yaml \
  --limit 1 --no-resume
```

---

## 8. Quick troubleshooting

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| `ModuleNotFoundError: utils.helpers` | Missing `ArgCausalDisco/` on `sys.path` | Use script entry points or full path setup in §6 |
| `* No solution found!` | Missing or unreachable `clingo` | `clingo --version`; install via conda-forge |
| Python runner fails, shell `swipl` OK | `_swipl_env()` override | See §3 caveat |
| Import errors for `torch`, `cdt`, `castle` | Full ArgCausalDisco stack pulled in | Confirm lazy-import edit in §5; do not install full `requirements.txt` |

---

## Related docs

- [`execution_guide.md`](execution_guide.md) — run pipelines, expected outputs, failure modes  
- [`causal/README.md`](../../causal/README.md) — causal bridge overview  
- Root [`README.md`](../../README.md) — inherited upstream ABA Learning engine (Prolog API, `set_lopt`)
