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
  ecai2024/, ruleml2025/    # inherited paper artefacts; retained, not M1.2 arm inputs
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

- `fixtures/` — exact finite-discrete causal-BN fixture layer. The YAML
  specification is authoritative. Schema version 1 retains the original
  positive-stochastic regime; schema version 2 supports non-degenerate stochastic
  roots with deterministic non-roots. Exact population support/CI/faithfulness,
  standard MEC/CPDAG certificates, evaluator-only mechanism references, checked
  BIF exports, and target-free nested-prefix samples are derived from it. This is
  pre-learning evaluator infrastructure, not Russo-style Causal ABA or a
  learned-rule graph decoder.
- `targetwise/` — target-complete runner over one explicitly selected frozen
  causal-fixture sample. It validates fixture/sample hashes and metadata,
  constructs symmetric binary exact-value BK and E+/E− for every variable,
  executes target cells serially, and writes inspectable per-target and
  collection artefacts. Temporary engine stems are canonicalised to
  `bk.sol.aba`, `bk.sol.asp`, and `bk.sol_chk.asp` within each target output;
  `delta.aba` contains the learned additions relative to the frozen input BK.
  Graph metadata is evaluator-only and no cross-target graph/CPDAG decoder is
  applied. Configuration schema:
  `causal/configs/targetwise/m13_bucket3_binary_diamond/{aamas2025,ecai2024}/n50_seed42.yaml`;
  compact diagnostics and the final checked-ASP artefact audit are implemented
  in `causal/targetwise/diagnostics.py` and
  `causal/targetwise/semantics.py`; focused tests:
  `causal/tests/test_targetwise_collection.py` and
  `causal/tests/test_predicate_naming.py`.
- `predicate_naming.py` — shared learner-visible naming contract. It accepts safe
  lowercase Prolog atoms, reserves ABA/learner namespaces, and extracts exact-value
  body variables against fixture metadata. Future fixtures use `a`, `b`, `c`, ...;
  existing `xN` names remain valid. No inherited Prolog file depends on this module.
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

## Milestone 1.2 expanded (M12x): documents, code and cells

M12x is the **closed / locked 18-cell evidence package** for Milestone 1 Part 2
expanded. Do not confuse it with the earlier 10-cell M12 pilot, whose fixtures,
configs and summaries use `M12_*` rather than `M12x_*`.

### Design and evidence documents

- Primary M1.2 expanded approach:
  `docs/research/milestone_plans/milestone1_part2/milestone1_part2_expanded_approach.md`.
- Unit-set overview:
  `docs/research/milestone_plans/milestone1_part2/milestone1_part2_expanded_unit_set.md`.
- Per-unit mechanism cards:
  `docs/research/milestone_plans/milestone1_part2/mechanism_cards/U1_*.md`
  through `U7_*.md`; the directory `README.md` is their index.
- Consolidated unit catalogue:
  `docs/research/milestone_plans/milestone1_part2/m12x_units_reference.tex`
  (with generated PDF beside it).
- Experiment record:
  `docs/experiments/qualitative/M1.2-expanded.md`.
- Authoritative 18-cell qualitative inspection:
  `docs/experiments/qualitative/M1.2-expanded-cell-inspection.md`.
- Report-facing copy of the inspection:
  `docs/report/findings/milestone1_part2_m12x_cell_inspection.tex`
  (with generated PDF beside it).

### Fixture, configuration, summary and test code

- Seven U1–U7 fixture builders:
  `causal/experiments/handcrafted_m12x.py`.
- Shared fixture registry:
  `causal/experiments/handcrafted.py` (registers `M12X_BUILDERS`).
- Published-configuration grid arms:
  `causal/configs/experiments/M12x_ecai2024.yaml` and
  `causal/configs/experiments/M12x_aamas2025.yaml`.
- Summary and detector generator:
  `causal/experiments/m12x_summary.py`.
- Relevant tests:
  `causal/tests/test_m12x_fixtures.py`,
  `causal/tests/test_m12x_configs.py`, and
  `causal/tests/test_m12x_summary.py`.

### M12x output and cell layout

- ECAI arm:
  `causal/outputs/aba_learning/grid/M12x_ecai2024/`.
- AAMAS arm:
  `causal/outputs/aba_learning/grid/M12x_aamas2025/`.
- Each arm has nine cell directories under `cells/`, using
  `{fixture}__target-{target}`:
  - `m12_u1_separator_copy__target-x2`
  - `m12_u2_collider_min__target-x2`
  - `m12_u3_collider_max__target-x2`
  - `m12_u4_fork_asymmetric__target-x1`
  - `m12_u4_fork_asymmetric__target-x2`
  - `m12_u5_chain_curated__target-x2`
  - `m12_u6_g1_min_diff__target-x2`
  - `m12_u6_g1_min_diff__target-x3`
  - `m12_u7_diamond_noisy__target-x3`
- A cell directory contains the generated table and learner artefacts, including
  `data.csv`, `bk.aba`, `bk.sol.aba`, `bk.sol.asp`, `prolog.stdout`, and
  `metrics.json`. Arm-level run metadata includes `manifest.json`,
  `results.parquet`, and `run.log`.
- Cross-arm summaries:
  `causal/outputs/aba_learning/grid/M12x_summary.md` and
  `M12x_summary.json`.
- Generated per-cell detector reports:
  `causal/outputs/aba_learning/grid/M12x_cell_reports/`, split into
  `M12x_ecai2024/` and `M12x_aamas2025/`.

The generated output tree is evidence and must not be hand-edited. The experiment
record and cell-inspection document explain which artefacts are authoritative and how
runner `solved`, ASP coverage, exact \(\mathcal H_t^\star\) match, and semantic
judgement differ.

## Milestone 1.3: claims, probes and future work

M1.3 currently has two locked claim buckets and one active investigation bucket. Its
shared method and terminology live in
`docs/research/milestone_plans/milestone1_part3/milestone1_part3_approach.md`;
`milestone1_part3_failure_modes.md` records the failure-mode vocabulary.

### Claim and findings documents

- Bucket 1 (four locked claims):
  `docs/experiments/qualitative/M1.3-bucket1-claims.md`.
- Bucket 1 report companion:
  `docs/report/findings/milestone1_part3_bucket1_claims.tex`
  (with generated PDF beside it).
- Bucket 2 (two locked claims):
  `docs/experiments/qualitative/M1.3-bucket2-claims.md`.
- Bucket 2 report companion:
  `docs/report/findings/milestone1_part3_bucket2_claims.tex`
  (with generated PDF beside it).
- Bucket 3 investigation and claims record:
  `docs/experiments/qualitative/M1.3-bucket3-claims.md`.
  It records the supervisor-defined planning dimensions and current M13-C3 status:
  H0–H4+H4b complete / analysed, H5
  cautious Greedy deferred, and no Bucket 3 claim or run matrix.

### M13-C1 probe: causal-role underdetermination

- Evidence record:
  `docs/experiments/qualitative/M13-C1-causal-role-underdetermination/experiment.md`.
- Fixtures and registry:
  `causal/experiments/handcrafted_m13.py` and
  `causal/experiments/handcrafted.py`.
- Two arm configs:
  `causal/configs/experiments/M13_c1_role_equivalence_ecai2024.yaml` and
  `M13_c1_role_equivalence_aamas2025.yaml`.
- Summary generator and tests:
  `causal/experiments/m13_c1_summary.py` and
  `causal/tests/test_m13_c1_fixtures.py`.
- Four generated cells (two graph-labelled fixtures in each arm):
  `causal/outputs/aba_learning/grid/M13_c1_role_equivalence_{ecai2024,aamas2025}/cells/`
  with slugs `m13_c1_parent_x0__target-x2` and
  `m13_c1_parent_x1__target-x2`.
- Cross-arm outputs:
  `causal/outputs/aba_learning/grid/M13_c1_role_equivalence_summary.md`
  and `.json`.

### M13-C2 probe: BK feature-block order

- Evidence record:
  `docs/experiments/qualitative/M13-C2-bk-feature-order/experiment.md`.
- Order-variant fixtures:
  `causal/experiments/handcrafted_m13.py`.
- Two arm configs:
  `causal/configs/experiments/M13_c2_bk_order_ecai2024.yaml` and
  `M13_c2_bk_order_aamas2025.yaml`.
- Summary generator and tests:
  `causal/experiments/m13_c2_summary.py` and
  `causal/tests/test_m13_c2_fixtures.py`.
- Twenty generated cells (ten order variants in each arm):
  `causal/outputs/aba_learning/grid/M13_c2_bk_order_{ecai2024,aamas2025}/cells/`.
  The ten fixture slugs comprise two U2 orders, two U5 orders, and all six U7
  predictor-block permutations; each cell adds `__target-x2` (U2/U5) or
  `__target-x3` (U7).
- Cross-arm outputs:
  `causal/outputs/aba_learning/grid/M13_c2_bk_order_summary.md` and `.json`.

M13-C1 and M13-C2 are completed evidence for locked Bucket 2. They are not a generic
directory for all future M1.3 work.

### Bucket 3 infrastructure and current boundary

Bucket 3 follows the approved one-case-at-a-time deterministic-mechanism direction.
H0–H4+H4b are complete / analysed; H5 cautious Greedy is deferred; H6/H7 are
signposted only; no Bucket 3 claim is approved. The status sources
are its investigation record, the 22 and 31 July sections of
`docs/research/supervisor_guidance.md`, `docs/research/research_state.md`, and the
M13-C3 records below.

Current deterministic M13-C3 evidence:

- hub: `docs/experiments/qualitative/M13-C3-binary-collider-and/experiment.md`;
- H0 closed baseline: `learning_analysis.md` / `.tex` on
  `m13_bucket3_binary_collider_and` / `n30_seed42` under AAMAS and ECAI;
- H1 analysed support ablation: `h1_support_ablation.md` / `.tex` and AAMAS
  `n25_seed42` on the same three-variable fixture;
- H2 analysed irrelevant-covariate probe: `h2_irrelevant_covariate.md` / `.tex` on
  `m13_bucket3_binary_collider_and_iso_d`, with AAMAS collections for
  `n30_seed42` and the secondary H2c prefix `n2_seed42`;
- H3 analysed BK-leading-distractor probe: `h3_bk_leading_distractor.md` / `.tex` on
  `m13_bucket3_binary_bd_and_lead_a`, with ECAI-primary and AAMAS-contrast
  `n30_seed42` collections;
- H4 analysed cautious-versus-brave probe: `h4_cautious_vs_brave.md` / `.tex` on
  the H0 fixture and frozen `n30_seed42` sample, contrasting locked ECAI brave
  with repository `baseline_cautious`;
- H4b analysed cautious split probe: `h4b_cautious_split_under_a.md` / `.tex`
  on H3 fixture `m13_bucket3_binary_bd_and_lead_a` / `n30_seed42`, target `c`;
  Layer A is shared with H3 and Layer B changes only the `c_alpha_3` close to
  `d_val_1`;
- remaining probe catalogue: `future_probes.md` / `.tex` (H1–H4+H4b complete; H5
  deferred; H6/H7 signposted only).
- H4 config:
  `causal/configs/targetwise/m13_bucket3_binary_collider_and/baseline_cautious/n30_seed42.yaml`;
  collection:
  `causal/outputs/aba_learning/targetwise/m13_bucket3_binary_collider_and/baseline_cautious/n30_seed42/`.
- H4b config:
  `causal/configs/targetwise/m13_bucket3_binary_bd_and_lead_a/baseline_cautious/n30_seed42.yaml`;
  collection:
  `causal/outputs/aba_learning/targetwise/m13_bucket3_binary_bd_and_lead_a/baseline_cautious/n30_seed42/`.

Authoritative fixture specifications and outputs for completed H0–H4+H4b:

- `causal/fixtures/specs/m13_bucket3_binary_collider_and.yaml` and
  `causal/outputs/causal_fixtures/m13_bucket3_binary_collider_and/`;
- `causal/fixtures/specs/m13_bucket3_binary_collider_and_iso_d.yaml` and
  `causal/outputs/causal_fixtures/m13_bucket3_binary_collider_and_iso_d/`;
- `causal/fixtures/specs/m13_bucket3_binary_bd_and_lead_a.yaml` and
  `causal/outputs/causal_fixtures/m13_bucket3_binary_bd_and_lead_a/`;
- target-wise collections under
  `causal/outputs/aba_learning/targetwise/{m13_bucket3_binary_collider_and,m13_bucket3_binary_collider_and_iso_d,m13_bucket3_binary_bd_and_lead_a}/`.

The pre-learning construction and certification tooling remains reusable:

- exact fixture package and usage boundary: `causal/fixtures/` and its `README.md`;
- authoritative binary-diamond definition:
  `causal/fixtures/specs/m13_bucket3_binary_diamond.yaml`;
- focused tests: `causal/tests/test_causal_fixture_*.py`;
- derived fixture-only artefacts:
  `causal/outputs/causal_fixtures/m13_bucket3_binary_diamond/`.

These files establish the generating DAG, exact population, assumptions, standard
MEC/CPDAG, and one target-free IID table. The diamond remains a
**positive-stochastic pre-pivot artefact**; neither its fixture nor its generated
outputs are deterministic-mechanism evidence. They must remain unchanged.

Reusable target-wise execution infrastructure now exists. The stochastic diamond has
already produced AAMAS/ECAI target-wise collections for exploratory inspection, but
those collections pre-date the 31 July direction and do not constitute an approved
deterministic Bucket 3 investigation:

- implementation and usage boundary: `causal/targetwise/` and its `README.md`;
- bounded configurations:
  `causal/configs/targetwise/m13_bucket3_binary_diamond/{aamas2025,ecai2024}/n50_seed42.yaml`;
- focused tests: `causal/tests/test_targetwise_collection.py`;
- intended generated hierarchy:
  `causal/outputs/aba_learning/targetwise/<fixture-id>/<configuration-id>/<sample-stem>/`,
  with a configuration-level contract manifest and one
  `cells/target-<variable>/` directory per automatically discovered target.

The fixture toolkit now also supports schema version 2 sources with non-degenerate
stochastic roots and deterministic non-roots. It samples randomness at roots only,
checks every deterministic assignment, records structural zeros, and emits
`mechanism_reference.json`. For supported binary fixture variable names, that
evaluator-only reference records full truth tables, root distributions,
formal/population-supported/sample-observed parent configurations, and canonical
unsimplified target-value-1 rules. It is never learner-visible and exact syntax match
is not an automatic success criterion.

The runner keeps a byte-identical table copy in every cell for inspection, but passes
only the exact-value BK and recorded E+/E− arrays to ABA Learning. It preserves raw
engine output, compact target-wise diagnostics, target reports, and a collection
summary. The diagnostics retain rules, ABA components, body variables/lengths,
outcome/runtime, and one final-artefact integrity audit. The audit runs Clingo
directly on the learner-produced `.sol_chk.asp` emitted under `check_ic`; it does not
reconstruct example constraints around `.sol.asp` and is not treated as a separate
coverage metric. Each target output also exposes a stable `delta.aba` containing
exactly the learned delta already recorded in its metrics. The target-wise diagnostics
omit inherited coverage panels and parent/graph proxies. The summary explicitly does
not union learned rules into a graph or assess CPDAG recovery.

For each later approved fixture, add its source specification, build and inspect its
population/reference artefacts, then add the learning configuration and evidence record
and run the target-wise collection. For a target-wise collection the generated cells
belong under the hierarchy above; grid experiments retain
`causal/outputs/aba_learning/grid/<experiment-id-or-arm>/`. H0–H4+H4b are
complete / analysed. H5 has no configuration; H6/H7 are signposted only.

Also update `docs/experiments/experiments_summary.md` and
`docs/research/experiment_register.md`. The wider 22 July dimensions remain deferred;
do not create fixtures or cells merely from that list.

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
  - `qualitative/M1.2-expanded.md` and
    `qualitative/M1.2-expanded-cell-inspection.md` — locked M12x evidence.
  - `qualitative/M1.3-bucket1-claims.md` — locked Bucket 1 claim record.
  - `qualitative/M1.3-bucket2-claims.md` — locked Bucket 2 claim record
    (M13-C1/C2).
  - `qualitative/M1.3-bucket3-claims.md` — Bucket 3 direction/planning record;
    H0–H4+H4b complete / analysed, H5 deferred, H6/H7 signposted,
    and no claim.
  - `qualitative/M13-C3-binary-collider-and/` — M13-C3 hub plus H0–H4+H4b evidence
    records and H5–H7 planning boundaries.
  - `qualitative/M13-C1-causal-role-underdetermination/` and
    `qualitative/M13-C2-bk-feature-order/` — analysed Bucket 2 probe records.
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
  configs/tests. The inherited paper artefact trees remain on disk but are not M1.2 arm
  inputs.
- Generated outputs under `causal/outputs/` and engine working files.

## Known unknowns (verify before relying on)

- `gen.pl` defines `subsumption/4`, but its caller in the default learning flow was not
  located; reachability is unconfirmed. The inline subsumption actually used during folding
  is `subsumed/6` (`asp_engine.pl`) via `select_foldable_aux/8` (`gen.pl`).
- See `execution_guide.md` for path/option discrepancies affecting how the engine is called.
