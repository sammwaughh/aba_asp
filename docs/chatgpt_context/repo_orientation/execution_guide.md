# Execution Guide

## Purpose

How to run the existing inherited system **after the environment is already set up**. This
guide covers verified execution workflows only; it does not duplicate environment setup
(see [`environment_setup.md`](environment_setup.md)) and does not propose new experiments
(see "Relationship to future experiments").

Scope reminder: what runs today is **target-wise ABA Learning over tabular data**, with
learned-rule inspection and, in older grid infrastructure, parent-set diagnostics.
Russo-style Causal ABA
(`arr_xy`/`noe_xy`/independence/d-separation) is **not implemented** — see
[`repo_map.md`](repo_map.md).

## Preconditions

- Full environment setup is documented in [`environment_setup.md`](environment_setup.md).
  Do not reproduce it here; complete it first.
- Conda env: **`aba-asp`** (Python 3.10). Older bridge notes saying `aba-env` are stale.
- Root directory for **all** commands:
  `/Users/samuelwaugh/Desktop/Causal ABA Learning/aba_asp`.
- **ArgCausalDisco is a sibling repo**, not inside `aba_asp/`:
  `/Users/samuelwaugh/Desktop/Causal ABA Learning/ArgCausalDisco`. It is used only as a
  data-generation library (`simulate_discrete_data`, `simulate_linear_continuous_data`).
- Verified local tool versions: SWI-Prolog `10.0.2 for fat-darwin`, clingo `5.8.0`.

## Working directory discipline

Run every command from the repo root with the env active:

```bash
conda activate aba-asp
cd "/Users/samuelwaugh/Desktop/Causal ABA Learning/aba_asp"
```

The grid harness and integration scripts resolve their own `sys.path` (repo root, workspace
root, and `ArgCausalDisco/`) relative to the repo, so they must be invoked from here. Do
**not** set a global `PYTHONPATH` (see troubleshooting: `utils` collision).

## Tool checks

```bash
python -c "import pandas, numpy, yaml, pyarrow; print('py-env OK')"   # -> py-env OK
swipl --version      # -> SWI-Prolog version 10.0.2 for fat-darwin (or similar)
clingo --version     # -> clingo version 5.8.0 (or similar)
```

Both `swipl` and `clingo` are required for learning runs. `clingo` must be on the `PATH`
inherited by SWI-Prolog (i.e. visible in the same activated environment).

## Core Python tests

No Prolog required. Verified passing:

```bash
python -m pytest causal/tests/test_config.py causal/tests/test_expand_cells.py \
  causal/tests/test_metrics.py causal/tests/test_results.py -q
```

Expected: `49 passed`.

## ArgCausalDisco simulator import smoke test

For ad-hoc checks only (grid/integration scripts set paths automatically). Inserts both the
workspace root and `ArgCausalDisco/` onto `sys.path`, then generates a tiny discrete dataset:

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

Expected: `argcausaldisco import OK (6, 3)`. A harmless pgmpy `FutureWarning` (about
`StructureScore`) may appear and can be ignored.

## Grid dry run

```bash
python -m causal.experiments.run_grid \
  --config causal/configs/experiments/E00_discrete_smoke.yaml \
  --dry-run
```

Expected: `36 cells planned for E00_discrete_smoke`.

Why 36 is correct, for this config:

- 3 DGPs: chain, fork, collider
- 4 seeds (0–3)
- 3 target variables via target expansion (`x0`, `x1`, `x2`)
- total: 3 × 4 × 3 = **36**

## Canonical Prolog learner smoke test

Runs the inherited learner end-to-end (exercises SWI-Prolog + clingo):

```bash
swipl -q -g "consult('aba_asp.pl'), aba_asp('./examples/flies_birds.bk', [flies(woodstock),flies(gwaihir),flies(x_pingu),flies(x_pinga)], [flies(pingu),flies(pinga)]), halt." -t "halt(1)"
```

Signs of success:

- a learning trace (folding, assumptions, contraries), then
- `checking entailment ... OK` (clingo invoked), and
- `Writing solution no. 1 to ./examples/flies_birds.bk.sol.aba`;
- the file `./examples/flies_birds.bk.sol.aba` is written.

The BK argument is the **stem without `.aba`** (`./examples/flies_birds.bk`); the engine
appends `.aba` itself.

## Expected output files

Engine learning run (per BK), written next to the BK / in the run cwd:

- `<BK>.sol.aba` — learnt ABA framework (rules + assumptions + contraries).
- `<BK>.sol.asp` — ASP encoding of the solution.
- `<BK>.sol_chk.asp` — only if `set_lopt(check_ic)` is enabled; this is the
  solution ASP together with the joint positive/negative integrity constraints.
- `aba_asp.csv` — appended run-log row (timestamp, BK, sizes, time).

The target-wise causal-fixture runner requires `check_ic`. Its post-run
invocation executes the learner-produced
`<BK>.sol_chk.asp` directly as a final-serialization integrity audit. It does
not reconstruct those constraints around `<BK>.sol.asp`, and the resulting
SAT/UNSAT status is not counted as an additional coverage metric.
Within each final target cell, temporary engine stems are replaced by the
stable names `bk.sol.aba`, `bk.sol.asp`, and `bk.sol_chk.asp`. The adjacent
`delta.aba` contains only the learned additions relative to that cell's frozen
`input/bk.aba`.

Engine scratch files (current working directory; see troubleshooting): `asp.clingo`,
`cc.clingo`, `cc.pl`, `clingo.stderr.log` (and/or `clingo.stderr.txt`).

Grid run, under `causal/outputs/aba_learning/grid/<experiment_id>/cells/<cell_dir_name>/`
(where `<cell_dir_name>` defaults to the hash `run_id`; M11 and M12 use `grid.cell_dir: dgp`
so dirs are named after the DGP, e.g. `cells/m11_binary_A/`, `cells/m12_sep/`):
`metrics.json`, `*.parquet`, run logs, per-cell BK/solution artefacts. Summaries:
`causal/experiments/figures/<experiment_id>_summary.{md,png}`.

## Exact causal-fixture workflow

The fixture source is authoritative and must be approved before sampling or learning.
Validate a proposed source without writing generated artefacts:

```bash
python -m causal.fixtures.cli validate \
  --fixture causal/fixtures/specs/<fixture-id>.yaml
```

After approval, build the exact population, certificate, BIF interoperability file,
evaluator-only mechanism reference, and one target-free sample:

```bash
python -m causal.fixtures.cli build \
  --fixture causal/fixtures/specs/<fixture-id>.yaml \
  --output-dir causal/outputs/causal_fixtures/<fixture-id> \
  --n <n> --seed 42
```

Schema version 1 is the preserved positive-stochastic regime. Schema version 2,
`root_stochastic_deterministic_nonroots`, requires non-degenerate stochastic roots and
point-mass conditional rows for every non-root. The sampler draws root values and
evaluates non-roots deterministically. The generated certificate reports exact support,
structural zeros, conditional independences, ordinary faithfulness, and the standard
MEC/CPDAG. `mechanism_reference.json` is evaluator-only and must not be copied into ABA
Learning inputs.

Do not rebuild the existing `m13_bucket3_binary_diamond` output directory. Its source,
sample, and target-wise AAMAS/ECAI outputs are preserved positive-stochastic pre-pivot
artefacts. Use a new fixture ID and empty output directory for an approved deterministic
fixture.

The target-wise run follows only after the built population/reference has been
inspected and the fixture approved. Its configuration selects one frozen sample and
one learner configuration; the runner automatically executes every variable as target.
See `causal/targetwise/README.md` for the validated commands and output hierarchy.

## Optional next checks (not yet validated)

These have **not** been run in verification; treat as unconfirmed until they pass locally.
Each needs `swipl` + `clingo` and may be slow:

```bash
python causal/test_data_utils_integration.py
python causal/test_aba_learning.py
python -m causal.experiments.run_grid \
  --config causal/configs/experiments/E00_discrete_smoke.yaml \
  --limit 1 --no-resume
```

(`--limit` and `--no-resume` are real flags in `causal/experiments/run_grid.py`.)

## Troubleshooting

- **`* No solution found!`** — most often a missing/unreachable `clingo` (the engine shells
  out via `shell/2` and may report no solution instead of a clear error). Check
  `clingo --version` and that clingo is on the PATH inherited by SWI-Prolog. Note: for root
  targets (no true parents), "no solution" can be the *correct* outcome.
- **`swipl` missing / wrong** — required for the learner. Verify `swipl --version`. On macOS
  Apple Silicon, conda-forge `swi-prolog` was unavailable; a system/Homebrew install on
  `PATH` is the working setup (see `environment_setup.md` §3).
- **`ModuleNotFoundError: utils.helpers`** — `ArgCausalDisco/` not on `sys.path`. Use the
  script entry points (which set paths themselves) or the full path setup shown in the
  simulator smoke test. Do **not** fix this with a global `PYTHONPATH`.
- **Why not a global `PYTHONPATH`** — there is a `utils` namespace collision:
  `aba_asp/utils/` (imported as `aba_asp.utils.*`) vs `ArgCausalDisco/utils/` (bare
  `from utils.helpers import ...`). A global `PYTHONPATH` makes which `utils` wins
  order-dependent and fragile. Scripts insert the needed roots locally instead.
- **Heavy ArgCausalDisco imports (`torch`, `cdt`, `castle`, notears)** — do **not**
  `pip install -r ArgCausalDisco/requirements.txt` for aba_asp work; that is for full paper
  reproduction. Only the simulators are needed (see `environment_setup.md` §5).
- **Python runner fails but shell `swipl` works** — `causal/run_aba_asp.py` may override
  `SWI_HOME_DIR` / `LD_LIBRARY_PATH` for a hard-coded cluster build tree (`_swipl_env`). If
  the Python runner fails while shell `swipl` is fine, this override is the likely cause.
  Do not change that code unless the Python runner actually fails (see
  `environment_setup.md` §3 caveat).
- **Scratch-file location / concurrency** — `asp.clingo`, `cc.clingo`, `cc.pl`, and clingo
  stderr files are written in the **current working directory** (filenames are hard-coded in
  `asp_engine.pl`). Run from a writable directory; avoid concurrent learning jobs in the same
  directory since they share these filenames.

## Known discrepancies and warnings

1. **`README.md` documents `aba_asp/4` (`aba_asp(+BK,+Ep,+En,-S)`), but no `aba_asp/4`
   clause exists** in `aba_asp.pl`. Use `aba_asp/3` for normal runs; use `aba_asp/6` if the
   solution term must be captured. (`aba_asp/5` also exists for already-covered examples.)
2. **`aba_asp/3` expects the BK path *stem without* `.aba`.** `read_bk/2` (`asp_utils.pl`)
   appends `.aba`. Pass `'./examples/flies_birds.bk'`, not `...bk.aba`.
3. **Generated BK comment lines may include the full `.aba` path.** Some generated
   `*.bk.aba` files embed a sample call whose path ends in `.aba`; copying it verbatim into
   `aba_asp(...)` makes the engine look for `...bk.aba.aba` and fail. Strip `.aba` first.
4. **E00 YAMLs do not set `learning_mode`; runs use the default `learning_mode(cautious)`**
   (set in `aba_asp.pl` initialization). Brave behaviour must be set explicitly; the configs
   do not.
5. **`subsumption/4` exists in `gen.pl`, but its caller in the default learning flow was not
   located** — reachability unconfirmed (unknown). The subsumption actually used during
   folding is `subsumed/6` (`asp_engine.pl`) via `select_foldable_aux/8`.
6. **Scratch files written in the cwd** — see the troubleshooting note above.

## Relationship to future experiments

This guide documents only verified execution of the existing system. New experiment design —
including QL-001 — should be planned separately, after this guide is committed, and recorded
under `docs/experiments/` per the research-logging rule. Do not add experiment hypotheses or
proposed Causal ABA encodings here.

## Related docs

- [`environment_setup.md`](environment_setup.md) — authoritative environment setup.
- [`repo_map.md`](repo_map.md) — repository structure and engine-vs-bridge distinction.
- Root [`README.md`](../../README.md) — inherited upstream engine (Prolog API, `set_lopt`).
- [`causal/README.md`](../../causal/README.md) — Python causal bridge.
