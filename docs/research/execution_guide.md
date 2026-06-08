# Execution guide

How to run the existing, already-implemented pipelines, what success looks like, and the
discrepancies to avoid. Operational only; see `repo_map.md` for structure and
`docs/theory/` for theory.

Scope reminder: what runs today is **parent-set recovery via ABA Learning** (does the
learned rule body for target `xk` match `xk`'s true parents). Russo-style Causal ABA
(`arr_xy`/`noe_xy`/independence/d-separation) is **not implemented** — see `repo_map.md`.

## Environment assumptions

**Canonical setup:** [`environment_setup.md`](environment_setup.md) — verified conda env
`aba-asp`, pip packages, SWI-Prolog, clingo, ArgCausalDisco paths, and smoke tests.

Summary for runs:

- Work from repository root: `aba_asp/`.
- Conda env: **`aba-asp`** (Python 3.10).
- **`swipl`** and **`clingo`** must both be on `PATH`; clingo is required for all learning
  runs (see environment doc — not optional).
- On macOS Apple Silicon, use system/Homebrew `swipl` if conda-forge `swi-prolog` is
  unavailable; install clingo via `conda install -c conda-forge clingo` if needed.
- `causal/run_aba_asp.py` probes cluster paths then falls back to `swipl` on `PATH`; see
  environment doc if the Python runner misbehaves with a Homebrew swipl.

Other references:

- **`README.md` (root)** — inherited upstream engine: Prolog API, `set_lopt(...)`, optional
  source build of SWI-Prolog.
- **`causal/README.md`** — Python causal bridge overview (not the canonical env record).

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
- Conda env name is documented as **`aba-asp`** in `environment_setup.md`; older `aba-env`
  references in bridge notes are stale.
