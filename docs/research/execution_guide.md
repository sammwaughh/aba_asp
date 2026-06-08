# Execution guide

How to run the existing, already-implemented pipelines, what success looks like, and the
discrepancies to avoid. Operational only; see `repo_map.md` for structure and
`docs/theory/` for theory.

Scope reminder: what runs today is **parent-set recovery via ABA Learning** (does the
learned rule body for target `xk` match `xk`'s true parents). Russo-style Causal ABA
(`arr_xy`/`noe_xy`/independence/d-separation) is **not implemented** — see `repo_map.md`.

## Environment assumptions

Two READMEs are authoritative for two different layers; use both:

- **`README.md` (root)** — authoritative for the inherited **upstream ABA Learning engine**:
  SWI-Prolog setup, loading `aba_asp.pl`, the Prolog examples, and the ABA Learning options
  (`set_lopt(...)`).
- **`causal/README.md`** — authoritative for the **Python causal bridge** (the MSc project
  work): `argcausaldisco_integration.py`, `run_aba_asp.py`, data generation and BK
  generation, the Python tests, the grid harness, and the causal outputs. It is **essential
  for the bridge**, but **not** authoritative for the upstream Prolog/SWI-Prolog setup.

Use the inherited root `README.md` for the upstream ABA Learning engine setup and the
`causal/README.md` for the Python causal bridge. For local work, prefer **one** conda
environment named **`aba-asp`** containing both the upstream engine requirements and the
Python bridge dependencies. Older bridge notes may refer to `aba-env`; treat that as an
environment-name inconsistency, not as a reason to ignore `causal/README.md`.

- macOS/Linux shell, repository root: `aba_asp/`.
- Preferred environment: a single **`aba-asp`** conda environment. Set up the engine per
  `README.md` (see "Preferred setup path from inherited README" below), then install the
  bridge dependencies into the **same** environment per `causal/README.md`, unless there is a
  local reason to maintain a separate bridge environment.
- Environment-name conflict (the only real conflict between the two READMEs): root
  `README.md` uses **`aba-asp`**; `causal/README.md` uses **`aba-env`**. Prefer `aba-asp`
  for this project. This is a documentation inconsistency to reconcile in the source READMEs
  later; it is flagged here, and the `causal/README.md` note is not removed.
- Python deps for the bridge (see `causal/README.md`): `pandas`, `numpy`, ArgCausalDisco;
  `pyarrow` for grid parquet output (grid tests `importorskip("pyarrow")`).
- `causal/run_aba_asp.py` first probes hard-coded cluster paths
  (`/vol/bitbucket/fr920/swipl/...`) and then falls back to `swipl` on `PATH`
  (`_find_swipl`). On a local machine, having `swipl` on `PATH` is sufficient.

## Preferred setup path from inherited README

Follow `README.md` first for the engine. It uses an `aba-asp` conda environment and builds
SWI-Prolog from source. The commands below are reproduced from `README.md` (only commands
present there or verified by code inspection are used). Note: the inherited `README.md`
appears to omit the `conda` prefix on the env-creation line (it shows
`create -n aba-asp python=3.12`); the corrected command is `conda create -n aba-asp
python=3.12`.

```bash
# 1. Create/activate the aba-asp conda environment (corrected from README.md)
conda create -n aba-asp python=3.12
conda activate aba-asp

# 2. Install build dependencies (per README.md)
conda install -c conda-forge cmake ninja compilers pkg-config gmp zlib \
  libuuid libedit readline openssl libarchive libxcrypt

# 3. Build/install SWI-Prolog from source if needed
#    (clone https://github.com/SWI-Prolog/swipl.git, then in its build dir):
export PKG_CONFIG_PATH="$CONDA_PREFIX/lib/pkgconfig:$CONDA_PREFIX/share/pkgconfig"
export CMAKE_PREFIX_PATH="$CONDA_PREFIX"
rm -rf CMakeCache.txt CMakeFiles
cmake -G Ninja -DCMAKE_INSTALL_PREFIX=$HOME -DCMAKE_BUILD_TYPE=PGO \
  -DCMAKE_PREFIX_PATH="$CONDA_PREFIX" -DINSTALL_DOCUMENTATION=OFF \
  -DEMACS_INCLUDE_DIR="$PWD/../packages/sweep" ..
ninja -j"$(nproc)" && ninja install

# 4. Confirm swipl works
swipl --version
```

`README.md` does not list a clingo install command; clingo must be present separately (see
"Required tools"). System SWI-Prolog packages also work as long as `swipl` is on `PATH` —
the source build is the README's route, not a hard requirement.

## Required tools

- **SWI-Prolog (`swipl`)** — required to run the ABA Learning engine.
- **clingo** — **also required for learning runs**, not optional. The engine shells out to
  clingo during learning (`asp_engine.pl`: `compute_conseq/2`, `entails/5`, `subsumed/6`).
  A run can start in `swipl` but will fail to produce solutions if `clingo` is missing.
- The working directory must be **writable** (engine writes scratch files there).

Quick checks:

```bash
swipl --version
clingo --version
```

## Run the canonical Prolog example

The canonical, documented, self-contained example is `examples/flies_birds.bk.aba`.

```bash
cd "/Users/samuelwaugh/Desktop/Causal ABA Learning/aba_asp"
swipl
```

```prolog
?- consult('aba_asp.pl').
?- aba_asp('./examples/flies_birds.bk',
     [flies(woodstock),flies(gwaihir),flies(x_pingu),flies(x_pinga)],
     [flies(pingu),flies(pinga)]).
```

Note the BK argument is the **stem without `.aba`** (`./examples/flies_birds.bk`); the
engine appends `.aba` itself.

## Run the smallest Python / unit baseline

Pure unit tests (no `swipl`/`clingo` needed):

```bash
# from repo root, with the project env active
pytest causal/tests/test_config.py
```

These exercise config loading/validation and the DGP registry. Solver-gated tests
(`causal/tests/test_prolog_query.py`, `test_runner_stage4.py`) auto-skip when tools or
fixtures are absent — a skip is expected, not a failure.

## Run / dry-run the grid harness

Dry-run (counts cells only, no solving):

```bash
python -m causal.experiments.run_grid \
  --config causal/configs/experiments/E00_discrete_smoke.yaml \
  --dry-run
```

Full grid (requires `swipl` + `clingo`):

```bash
python -m causal.experiments.run_grid \
  --config causal/configs/experiments/E00_discrete_smoke.yaml
# continuous mirror:
python -m causal.experiments.run_grid \
  --config causal/configs/experiments/E00_continuous_smoke.yaml
```

Summarise (report-ready table + heatmap):

```bash
python causal/scripts/summarize_experiment.py --experiment E00_discrete_smoke
```

Prefer dry-run first; for a minimal real run, consult `run_grid.py --help` for a
cell-limiting flag rather than running the whole grid.

## Expected output files

Engine learning run (per BK), written next to the BK / in the run cwd:

- `<BK>.sol.aba` — learnt ABA framework (rules + assumptions + contraries).
- `<BK>.sol.asp` — ASP encoding of the solution.
- `<BK>.sol_chk.asp` — only if `set_lopt(check_ic)` is enabled.
- `aba_asp.csv` — appended run-log row (timestamp, BK, sizes, time).

Engine scratch files (in the current working directory; see warning #6):

- `asp.clingo`, `cc.clingo`, `cc.pl`, `clingo.stderr.log` (and/or `clingo.stderr.txt`).

Grid run, under `causal/outputs/aba_learning/grid/<experiment_id>/cells/<run_id>/`:

- `metrics.json`, `*.parquet`, run logs, and per-cell BK/solution artefacts.
  Summaries: `causal/experiments/figures/<experiment_id>_summary.{md,png}`.

## Success indicators

- **Prolog learning run:** stdout prints `BK size (rules):`, example counts,
  `ABA size (rules):`, learning time, then `Writing solution no. 1 to <BK>.sol.aba`; the
  `.sol.aba`/`.sol.asp` files exist; process exit code 0.
  - Example (parent recovery): for the `simple_4` fixture (true edge `x0 -> x2`), the
    learned delta is `x2(A) :- x0(A).` in `*.sol.aba`.
- **Python single call (`ABASPRunner.run_prolog_aba_asp`):** returns a dict with
  `status='completed'` and `return_code == 0`; learned delta via `_extract_learned_rules()`.
- **Grid cell:** `metrics.json` with `outcome="solved"`; for targets with true parents,
  body-F1 = 1.0 indicates the parent set was recovered exactly. Root targets (no parents)
  correctly produce `completed_no_solution` (the learner declines to invent a rule).
- **pytest:** selected tests pass; skips for missing tools/fixtures are expected.

## Common failure modes

- **No solution:** stdout shows `* No solution found!` or `* There are no more solutions!`
  (the latter after enumerating). For root targets, no solution is the correct outcome.
- **`clingo` not found:** learning starts in `swipl` but cannot compute consequences;
  expect failures/empty results. Install/expose `clingo` on `PATH`.
- **`ERROR: unknown constant`:** an example atom uses a constant (sample id) not present in
  any BK rule body. `check_aba/3` (`aba_asp.pl`) halts. Ensure example ids match generated
  BK ids.
- **Range-restriction / `not range restricted!`:** an assumption’s arguments are not bound
  by the rule body (`check_asm_dom/2`, `asp_utils.pl`). Indicates a malformed framework.
- **Timeouts / search blow-up:** large `folding_steps` or hard cells; the Python runner
  enforces `prolog_timeout_s` and records `timeout` outcomes. Reduce scope before retrying.
- **Path mistakes when calling the engine:** see warnings #2 and #3 below.

## Known discrepancies and warnings

1. **`README.md` documents `aba_asp/4` (`aba_asp(+BK,+Ep,+En,-S)`), but no `aba_asp/4`
   clause exists.** The real predicates are `aba_asp/3`, `aba_asp/5`, `aba_asp/6`
   (`aba_asp.pl`). To capture the solution term, use `aba_asp/6`.
2. **`aba_asp/3` expects the BK path *stem without* `.aba`.** `read_bk/2`
   (`asp_utils.pl`) appends `.aba`. Pass `'./examples/flies_birds.bk'`, not
   `'./examples/flies_birds.bk.aba'`.
3. **Generated BK comment lines may include the full `.aba` path.** Some generated
   `*.bk.aba` files embed a sample call whose path ends in `.aba`; copying it verbatim into
   `aba_asp(...)` would make the engine look for `...bk.aba.aba` and fail. Strip the `.aba`
   suffix before use.
4. **The E00 YAMLs do not set `learning_mode`; runs use the file default
   `learning_mode(cautious)`** (set in `aba_asp.pl` initialization). If brave behaviour is
   wanted, it must be set explicitly; the configs do not.
5. **`subsumption/4` exists in `gen.pl`, but its caller in the default learning flow was
   not located** — reachability unconfirmed (mark as unknown). The subsumption actually used
   during folding is `subsumed/6` (`asp_engine.pl`) via `select_foldable_aux/8`.
6. **`asp.clingo`, `cc.clingo`, `cc.pl`, and clingo stderr files are written in the current
   working directory** (the engine hard-codes these filenames in `shell/2` calls). When
   driven from Python, cwd is the BK’s parent directory. Run from a writable directory and
   expect these scratch files to appear there; avoid running concurrent learning jobs in the
   same directory (they share these filenames).

## Future notes (not experiments)

- If/when Russo-style Causal ABA is implemented, keep the new `arr/noe/independence`
  encoding separate from this parent-set-recovery pipeline and document it here.
- Resolve the conda env name inconsistency (`aba-asp` vs `aba-env`) in the source READMEs
  (outside the scope of these two docs).
