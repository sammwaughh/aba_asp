# Repository map

Operational map of this repository for future experimentation and future Cursor sessions.
Canonical theory lives in `docs/theory/`; this file is orientation only, not theory.

## Purpose

This repository supports an MSc project on **Causal ABA Learning**: investigating how
**Causal ABA** (representing causal-discovery evidence inside Assumption-Based Argumentation)
and **ABA Learning** (transforming/learning ABA frameworks from background knowledge and
positive/negative examples) can interact. See `docs/theory/theory_primer.md` for the
canonical framing.

## Two layers: engine vs bridge

The repo contains two distinct codebases that must not be conflated.

1. **Upstream ABA Learning engine (Prolog + ASP), repo root.**
   The "ABALearn" tool (De Angelis / Proietti / Toni lineage). General-purpose ABA Learning
   via transformation rules with a clingo backend. Not causal-specific. Treat as a vendored
   dependency: prefer not to modify it.

2. **Project-specific causal bridge (Python), `causal/`.**
   The MSc work. Turns tabular data into ABA background knowledge, drives the Prolog engine
   per target variable, and measures whether the learned rule body recovers the target's
   true parent set. This is the layer to extend.

## Top-level structure

```
aba_asp/
  aba_asp.pl, gen.pl, folding.pl, rote_learning.pl, io.pl,   # engine (Prolog)
  asp_engine.pl, asp_utils.pl, cc.pl
  asp.clingo, cc.clingo, cc.pl, aba_asp.csv, *.stderr.log     # engine working/output files
  configs/                  # Prolog option presets (.pl)
  examples/                 # hand-written .bk.aba frameworks
  examples-wip/             # work-in-progress example frameworks
  ecai2024/, ruleml2025/    # paper artefact trees (ILASP, benchmarks)
  utils/                    # table -> predicate helpers (data_utils.py, examples.py)
  causal/                   # PROJECT causal bridge (Python)
  docs/                     # theory, papers, experiments, research record
```

## Main Prolog files (engine)

- `aba_asp.pl` — entry point. Predicates `aba_asp/3`, `aba_asp/5`, `aba_asp/6`
  (there is **no** `aba_asp/4`). Sets default learning options via
  `:- initialization(set_lopt(...))`; orchestrates Rote Learning then Generalisation
  (`aba_asp_proc/7`); writes `*.sol.aba` / `*.sol.asp`; appends a run log to `aba_asp.csv`.
- `rote_learning.pl` — Rote Learning (`roLe/7`, `roLe_aux/7`, `e_rote_learn/2`); brave vs
  cautious branches.
- `gen.pl` — Generalisation driver: folding selection (`genT/6`, `gen1/6`,
  `select_foldable/7`) and Assumption Introduction (`new_assumption/9`, `relto`/`sechk`
  paths). Also defines `subsumption/4` (see "Known unknowns").
- `folding.pl` — folding algorithms: `fold_nd` (token-bounded, default), `fold_greedy`,
  `fold_all`, `fold_lazy`.
- `asp_engine.pl` — module `clingo`. Invokes the clingo solver via `shell/2`:
  `compute_conseq/2`, `entails/5`, `subsumed/6`. This is where ASP solving actually happens.
- `asp_utils.pl` — module `asp_utils`. Rule representation (`rule/3`), BK reading
  (`read_bk/2`, `bk_term/2`), ASP generation (`asp/7`, `dump_rules/1,2`, `dump_rule/1`,
  `ic/3`), and the `aba_enc/5` framework accessors.
- `io.pl` — logging (`abalearn_log/2`) and error handling (`abalearn_error/1`).
- `cc.pl` — clingo consequence helper artefact.

## Main Python causal bridge files (`causal/`)

- `argcausaldisco_integration.py` — data → ABA pipeline.
  `generate_aba_background_knowledge()` (table → feature predicates → `.bk.aba`),
  `pick_target_variable()` (target + E+/E− split), `_extract_learned_rules()` (solution − BK).
- `run_aba_asp.py` — `ABASPRunner` subprocess wrapper around SWI-Prolog/clingo
  (`run_prolog_aba_asp`, `run_clingo_asp`) plus `query_examples()` (entailment checks).
  Holds SWI-Prolog discovery logic (`_find_swipl`, `_swipl_env`).
- `metrics.py` — scoring: `GroundTruth`, `parse_delta_rules`, `compute_cell_metrics`
  (body-F1, coverage gaps, parent-set recovery).
- `test_aba_learning.py`, `test_data_utils_integration.py` — legacy end-to-end / conversion
  suites (large; runnable as scripts).

## Experiment harness files (`causal/experiments/`)

- `run_grid.py` — grid runner (CLI: `--config`, `--dry-run`, etc.).
- `config.py` — YAML config loading/validation (`load_config`, `ExperimentConfig`).
- `dgp.py` — data-generating processes (`dgp_zoo`, `get_dgp`; G3-chain/fork/collider, etc.).
- `handcrafted.py` — fixed toy tables (`simple_4`, `exception_5`) with pinned E+/E−.
- `manifest.py`, `results.py`, `paths.py` — run manifest, result shards, path layout.
- `figures/` — generated summaries (e.g. `E00_discrete_smoke_summary.{md,png}`).
- Configs: `causal/configs/experiments/E00_discrete_smoke.yaml`,
  `E00_continuous_smoke.yaml`.
- Tests: `causal/tests/` (config/dgp unit tests; solver-gated runner/query tests that
  auto-skip when `swipl`/`clingo`/`pyarrow`/fixtures are absent).

## Documentation / theory files (`docs/`)

- `docs/theory/` — **canonical**: `theory_primer.md`, `background.tex`,
  `literature_review.tex`, `paper_summaries/*.md`.
- `docs/papers/core/` — source PDFs (reference only; use summaries first).
- `docs/experiments/` — experiment records and supporting structure:
  - `TEMPLATE.md` — canonical template for every experiment record.
  - `experiments_summary.md` — at-a-glance index of experiments (status, artefacts,
    report relevance).
  - `qualitative/QL-001.md` — first qualitative record (ABA Learning on minimal causal
    motifs).
  - `qualitative/M1.1-parent-position.md` — Milestone 1 Part 1 (M11) metamorphic
    control; **closed** (Stages 0–7, June 2026)
    parent-position control.
  - `report/findings/` — supervisor-facing milestone findings logs (`.tex`).
  - `templates/` — older copy templates retained for reference.
- `docs/report/` — report-support docs (evidence-to-prose guardrails, not report prose):
  - `README.md` — index for report layout and manuscript pairing.
  - `manuscript/` — report chapter `.tex` sources and `.md` ChatGPT mirrors (`introduction`,
    `literature_review`, `background`, `experimentation`, `project_plan`; `main.tex` driver).
  - `claims_ledger.md` — evidence-to-claim guardrail.
  - `report_state.md` — interim report section/evidence plan.
  - `figure_table_index.md` — figure/table provenance.
  - `genai_use_log.md` — factual log of ChatGPT/Cursor assistance.
- `docs/research/` — research record: `ideas.md`, `decisions.md`, `research_log.md`,
  `supervisor_guidance.md` (supervisor meeting guidance), `experiment_register.md` (lightweight
  register mirroring the experiments summary), plus this `repo_map.md` and
  `execution_guide.md`.
- `docs/chatgpt_context/` — upload-staging mirror of the governance and repo-orientation
  docs (canonical matching filenames) for the ChatGPT Project; see its `README.md`.

## Experiment/report documentation workflow

Experiment records under `docs/experiments/` are **evidence records, not polished report
prose**. Polished prose is written separately (by Samuel/ChatGPT) from these records.

1. Design the experiment conceptually before implementation.
2. Use Cursor plan-only inspection where the implementation path is uncertain.
3. Record detailed evidence in `docs/experiments/<ID>.md` using `docs/experiments/TEMPLATE.md`.
4. Update `docs/experiments/experiments_summary.md` and `docs/research/experiment_register.md`.
5. Track candidate figures/tables in `docs/report/figure_table_index.md`.
6. Check claims against `docs/report/claims_ledger.md`.
7. Record meaningful ChatGPT/Cursor assistance in `docs/report/genai_use_log.md`.

## Where examples and generated outputs live

- Hand-written example frameworks: `examples/*.bk.aba` (canonical: `flies_birds.bk.aba`),
  `examples-wip/`.
- Generated BK + solutions from the bridge: `causal/outputs/aba_learning/<TestClass>/`
  (`*.bk.aba`, `*.bk.sol.aba`, `*.bk.sol.asp`, `*.csv`) and grid output under
  `causal/outputs/aba_learning/grid/<experiment_id>/cells/<cell_dir_name>/`
  (defaults to hash `run_id`; M11 and M12 use `grid.cell_dir: dgp` → `cells/m11_binary_A/`,
  `cells/m12_sep/`, etc.)
  (`metrics.json`, `*.parquet`, logs). Outputs are generated; do not hand-edit.
- Engine working files (`asp.clingo`, `cc.clingo`, `cc.pl`, clingo stderr logs,
  `aba_asp.csv`) are written in the **current working directory** of the run (see
  `execution_guide.md`).

## Implemented vs theory-only

- **Implemented and runnable:** the ABA Learning engine (transformation rules + clingo
  backend); the Python bridge that builds feature-predicate BK, runs per-target learning,
  and measures **parent-set recovery** (does the learned rule body for target `xk` match
  `xk`'s true parents). This is the current operationalisation of "apply ABA Learning to
  causal discovery".
- **Theory-only (NOT implemented in code):** Russo-style **Causal ABA** — arrow/no-edge
  assumptions (`arr_xy`, `noe_xy`), independence assumptions, d-separation / collider-trees,
  acyclicity-as-attacks, and the stable-extension ↔ DAG correspondence. These appear only in
  `docs/theory/` (and as substrings in DGP/test names such as "collider", which refer to the
  data-generating graph, not to an ABA encoding). Do not assume the repo computes
  graph-compatible stable extensions.

Keep the distinction explicit: **implemented = parent-set recovery via ABA Learning**;
**not yet implemented = Russo-style Causal ABA representation**.

## Files that should not be modified casually

- The Prolog engine: `aba_asp.pl`, `gen.pl`, `folding.pl`, `rote_learning.pl`,
  `asp_engine.pl`, `asp_utils.pl`, `io.pl`, `cc.pl`, and `configs/*.pl`. Treat as vendored.
- Theory files in `docs/theory/` (canonical; do not invent theory).
- `.cursor/rules/*.mdc`, `AGENTS.md`, `README.md`, `PROJECT_README.md`.
- `examples/`, `examples-wip/`, `ecai2024/`, `ruleml2025/`, and existing experiment
  configs/tests.
- Generated outputs under `causal/outputs/` and engine working files.

## Known unknowns (verify before relying on)

- `gen.pl` defines `subsumption/4`, but its caller in the default learning flow was not
  located; reachability is unconfirmed. The inline subsumption actually used during folding
  is `subsumed/6` (`asp_engine.pl`) via `select_foldable_aux/8` (`gen.pl`).
- See `execution_guide.md` for path/option discrepancies affecting how the engine is called.
