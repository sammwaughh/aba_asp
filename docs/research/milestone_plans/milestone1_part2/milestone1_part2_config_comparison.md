# Milestone 1, Part 2 (M1.2) — Published-configuration comparison on divergence-designed fixtures

**Status:** `run` — Stages 0–2 complete (2026-07-08): fixtures + validation checks + locked expected outputs (Stage 0); config-consulting runner + feature-BK construction + arm YAMLs + summary side-car + smoke test (Stage 1); 15-cell grid run, outcome matrix built (Stage 2). Stages 3–4 not started
**Experiment ID:** `M12_config_comparison` (arms `M12_ecai2024`, `M12_ruleml2025`, `M12_aamas2025`)
**Parent index:** [milestone1-plan.md](../milestone1-plan.md) (Part 2 section)

## 1. Goal and research question

Compare the three published ABA Learning configurations shipped with the inherited
engine, run one-shot on shared handcrafted categorical fixtures, and report clearly when
and how each recovers the **mechanism-aligned rules** warranted by the fixture's declared
graph and mechanism.

> **RQ (M1.2).** For a fixed encoding of small categorical tables (each generated from a
> declared graph \(G\) and mechanism, with a pre-specified expected learned output), how do
> ASP-ABAlearnB, RASP-ABAlearn, and Greedy ABA Learning differ in (a) whether the expected
> output is learned, (b) the structural class of what is learned instead, and (c) which
> data properties expose divergence between the three systems?

This is unguided ABA Learning only: no Causal ABA machinery (`arr`/`noe`/`indep`,
d-separation, stable-extension-as-DAG) is exercised. Results characterise recovery of
mechanism-aligned rules, not causal discovery.

## 2. Systems under comparison

The three arms are the engine's shipped configuration files, consulted **verbatim** for
provenance:

| Arm | Config file | Published system | Verified option content |
|-----|-------------|------------------|--------------------------|
| ECAI | `configs/ecai2024_config.pl` | ASP-ABAlearnB (ECAI 2024, "Learning Brave ABA Frameworks via ASP") | brave; `nd` folding, `folding_steps(10)`; selection `any`; space `all`; `asm_intro(relto)`; `check_ic` |
| RuleML | `ruleml2025/ruleml2025_config.pl` | RASP-ABAlearn (RuleML 2025, "Learning to Contest Argumentative Claims") | brave; `greedy` folding; selection `mgr`; space `bk`; `asm_intro(relto)`; `check_ic`; `post_folding_test_entailment(false)` |
| AAMAS | `configs/aamas2025_config.pl` | Greedy ABA Learning for CBR (AAMAS 2025) | brave; `greedy` folding; selection `mgr`; space `bk`; `asm_intro(relto)`; `check_ic`; post-folding entailment gate at engine default (`true`) |

Design decisions fixed at planning time:

- **One-shot runs only.** RASP-ABAlearn's distinctive *incremental redress* workflow
  (sequential `aba_asp/5` calls feeding each solution forward, cf. `ruleml2025/README.txt`
  and the `.goal` files) is **not exercised**; the RuleML arm tests that system's
  configuration on a single learning problem. This must be stated explicitly in the
  write-up. Exercising redress (e.g. learning targets sequentially) is flagged as a
  near-term follow-up after M1.2 (Section 4.1).
- **All arms are brave**, as published. No cautious arm; the published methods use brave
  for a reason. Comparisons against the cautious-default M1.1/QI results are therefore
  cross-configuration observations, not controlled comparisons.
- **No repeat-stability measurement.** The algorithms have no probabilistic component and
  clingo is deterministic for fixed input, flags, and version; identical reruns give
  identical output.
- **`asm_intro(relto)` in all arms** (as the config files specify); the config files are
  treated as canonical. Recorded caveat: if M1.3 implicates assumption-introduction
  behaviour in a failure mode, a single `sechk` ablation on the implicated cell is the
  designated follow-up.
- **`ecai2024ALL_config.pl` (fold-all variant) is excluded** from M1.2; flagged for later
  consideration.
- **Honesty note for the write-up:** the RuleML and AAMAS configurations differ *only* in
  the post-folding entailment gate. The three-system comparison therefore factorises as
  {nd/any/all vs greedy/mgr/bk} × {gate on vs off}, and the report must not overstate the
  independence of the two greedy arms. **Scope note (July 2026):** the incoherent-table
  families that were originally planned to expose this gate difference (`m12_incoh_pos`,
  `m12_incoh_neg`) are **deferred** (Section 4.1). M1.2 therefore does **not** exercise
  the main predicted RuleML-vs-AAMAS divergence from the original plan; any gate-related
  observations in M1.2 are incidental only.

## 3. Encoding

Feature encoding (identical across arms, per fixture), matching how the published tabular
benchmarks construct BK (`ecai2024/ASP-ABAlearn_B/*.csv.bk.aba`, `ruleml2025/*.scratch.aba`):

- rows are cases with numeric sample ids 1..N;
- each categorical predictor (\(k = 3\) values) is encoded as one-hot value predicates
  `xi_val_v(A) :- A=id.`;
- the target is excluded from the feature BK; \(E^+\) = target atoms of the designated
  positive class, \(E^-\) = the rest;
- learning is driven by `E^+`/`E^-` only: the engine rote-learns the target atoms and
  folds them into intensional target rules (`t(A) :- xi_val_v(A)`), the same path the
  shipped ECAI/RuleML tabular benchmarks use.

**RuleML `domain/1` element.** The RuleML arm additionally emits the `domain/1` predicate
that ships with `ruleml2025/*.scratch.aba`, for construction fidelity to that system:

```prolog
domain(default).
domain(1). ... domain(N).
```

No default rule and no assumption/contrary are declared (that `domain(default)` element
supports RASP-ABAlearn's incremental redress workflow, which M1.2 does **not** run — one
shot only). The ECAI and AAMAS arms use feature-BK with no `domain/1`. The feature
encoding is otherwise shared across all three arms so the comparison isolates the folding
configuration (plus RuleML's `domain/1`). Validated in Stage 0/1.

## 4. Fixture families

All fixtures are minimal handcrafted categorical tables with \(k = 3\) values per
predictor; \(p\) (number of predictors) is fixture-dependent. **Every fixture must declare
its intended graph \(G\) (nodes, directed edges) and mechanism in three places: the
fixture code (docstring + machine-readable `edges` metadata), the run config/record, and
any findings `.tex`.**

Expected outputs are pre-specified per cell before any run. All M1.2 fixtures are
**coherent** tables with intensional expected rules (or a small rule set). Incoherent
tables and defeasible expected outputs are **deferred** (Section 4.1).

| Family | Key | \(G\) (declared topology) | \(p\) | Table sketch | Expected learned output |
|--------|-----|---------------------------|------|--------------|--------------------------|
| Separator anchor | `m12_sep` | `x1 -> x2`; `x0` isolated (non-parent) | 2 | complete factorial over (x0,x1), 9 rows; `x2 := x1`; positive class `x2=2` | `x2(A) :- x1_val_2(A).` (M1.1-style anchor) |
| Conjunctive collider | `m12_conj` | **Collider:** `x0 -> x3`, `x1 -> x3`; `x2` isolated | 3 | complete factorial over (x0,x1,x2), 27 rows; **conjunctive mechanism:** `x3 := min(x0,x1)`, positive `x3=2` iff `x0=2 ∧ x1=2` | `x3(A) :- x0_val_2(A), x1_val_2(A).` — no single literal separates |
| Disjunctive collider | `m12_disj` | **Collider:** `x0 -> x3`, `x1 -> x3`; `x2` isolated (symmetric twin of `m12_conj`) | 3 | complete factorial over (x0,x1,x2), 27 rows; **disjunctive mechanism:** `x3 := max(x0,x1)`, positive `x3=2` iff `x0=2 ∨ x1=2` | two rules: `x3(A) :- x0_val_2(A).` and `x3(A) :- x1_val_2(A).` |
| Fork (correlated sibling) | `m12_fork` | **Fork:** `x0 -> x1`, `x0 -> x2` | 2 | **deterministic two-child fork**, 9 rows: three assignments (x0,x1,x2) = (0,0,0), (1,2,0), (2,0,2), each ×3; mechanisms `x1 := 2 if x0=1 else 0`, `x2 := 2 if x0=2 else 0`; positive class `x2=2` (iff `x0=2`) | `x2(A) :- x0_val_2(A).` |
| Correlated ancestor | `m12_chain` | **Chain:** `x0 -> x1 -> x2` | 2 | non-factorial, 9 rows: per `x0` block of 3, `x1 := x0` twice + one cyclic deviation `x1 := (x0+1) mod 3`; `x2 := x1`; parent value predicate is the **unique** zero-error separator; ancestor strictly associated (P(pos\|x0)=0, 1/3, 2/3) but imperfect | `x2(A) :- x1_val_2(A).` — failure mode of interest: ancestor (`x0`) citation |

**Naming note:** `m12_conj` and `m12_disj` are named for their **mechanism** (conjunctive
vs disjunctive positive class) on a **collider** topology (two directed edges into the
target). They are symmetric twins: same declared G (`x0 -> x3`, `x1 -> x3`; `x2`
isolated), same 27-row factorial, same three predictors in BK; they differ only in
mechanism (`min` vs `max`) and expected rule shape. They are not fork topologies.
`m12_fork` is the fork-topology family (shared cause `x0`, two effects `x1` and `x2`).
**Isolated-variable policy:** only `m12_sep`, `m12_conj`, and `m12_disj` include an
explicit isolated non-parent column; `m12_fork` and `m12_chain` use correlated sibling
and ancestor confounds instead (see rationale below).

Rationale per family:

- **`m12_sep`** — anchors against M1.1; isolated non-parent vs direct parent (unique
  separator).
- **`m12_conj`** — collider with conjunctive mechanism; probes exhaustive vs
  token-bounded folding and `mgr` generalisation when no single literal separates.
- **`m12_disj`** — collider with disjunctive mechanism; **symmetric twin of
  `m12_conj`** (same declared G shape, isolated `x2`, target `x3`, 27-row factorial,
  three predictors in BK); differs only in mechanism (`max` vs `min`) and expected
  two-rule output. Probes multi-rule learning and subsumption.
- **`m12_fork`** — fork topology; probes **correlated-sibling confound**: `x1` is
  associated with `x2` via shared cause `x0` but is **not** a zero-error separator.
  Distinct from `m12_sep` (isolated noise variable) and `m12_chain` (ancestor vs parent
  on a chain). Extends the QI-002 fork baseline (`qi002_fork_cat3`) to the three published
  configurations under the shared M1.2 encoding (feature-BK, config-file arms),
  with a **different table**: QI-002's factorial fork decorrelated the sibling; here both
  children are deterministic functions of `x0` (Samuel's design, 2026-07-08), so the edge
  `x0 -> x1` leaves a data-level trace. Two design notes: `x1` takes exactly two values
  (a deterministic imperfect separator of a 3-valued cause cannot be injective), and its
  alphabet is {0,2} rather than {0,1} so it stays on the `x1_val_v` value-predicate
  encoding path (value-set-{0,1} columns are emitted as bare binary predicates).
- **`m12_chain`** — chain topology; parent vs correlated-ancestor discrimination (parent
  is unique separator; ancestor associated but imperfect).

**Grid size:** 3 arms × 5 fixtures = **15 cells**.

Deliberately **out of scope** for M1.2 (decided at planning): σ/π order grids (M1.1
established ordering as a failure mode; revisit in M1.3 only if implicated), positive-class
sensitivity, support-vs-frequency designs, binary encodings, continuous data, incoherent
tables (Section 4.1).

Exact tables are finalised at implementation and locked by Stage-0 validation checks
(per family: row counts; declared \(G\) consistency; expected separator
existence/uniqueness; for `m12_conj`/`m12_disj`, non-existence of a smaller separating
rule; for `m12_fork`, see fork checks below; for `m12_chain`, parent unique zero-error
separator + ancestor associated-but-imperfect). Exact tables, E+/E-, and locked expected
outputs: `docs/experiments/qualitative/M1.2-config-comparison.md`; fixtures in
`causal/experiments/handcrafted_m12.py`; checks in `causal/tests/test_m12_fixtures.py`.

**Stage-0 validation — `m12_fork` (Prolog-free):**

- 9 rows (\(p=2\)): three distinct deterministic assignments, each repeated 3× in block
  order (*amended from the original "complete factorial" draft, which was unsatisfiable
  together with the association check below: a factorial forces `x1` independent of
  `x2` in-sample*);
- `x0` is the unique zero-error separator for the positive class (`x0` takes all 3
  values);
- `x1` is associated with `x2` but is **not** a zero-error separator;
- declared edges match fork topology (`x0 -> x1`, `x0 -> x2`);
- no column has value set exactly {0,1} (bare-binary encoding guard).

### 4.1 Deferred follow-up experiments (not in M1.2 grid)

The following are explicitly **out of the M1.2 grid** but recorded here so they are not
lost. Each should get its own experiment ID and plan when scheduled.

| Deferred item | Planned keys / scope | Rationale | When |
|---------------|---------------------|-----------|------|
| Incoherent tables (entailment-gate probe) | `m12_incoh_pos`, `m12_incoh_neg` | Minimal single-collision tables derived from `m12_sep`; positive vs negative collision sub-variants. Expected output is a **defeasible structure** (general rule + assumption + contrary aligned with colliding rows). This is where the **RuleML vs AAMAS post-folding entailment gate** difference (`post_folding_test_entailment(false)` vs default `true`) was originally predicted to diverge under brave semantics. | After M1.2, or as a dedicated follow-up experiment (e.g. `M12b_incoherent` or similar) |
| RASP-ABAlearn redress workflow | incremental `aba_asp/5` sequence per `ruleml2025/*.goal` | Tests RASP-ABAlearn's distinctive incremental-redress protocol, not just its config file on a one-shot problem. Natural causal reading: learn targets sequentially, feeding each solution forward. | Near-term follow-up after M1.2 one-shot grid |
| `ecai2024ALL_config.pl` | fold-all variant | Excluded from M1.2; flagged for later consideration. | TBD |
| Graded incoherence severity | ladder of 1/2/3 colliding pairs | Dose-response on assumption count / termination; only if incoherent follow-up warrants it. | M1.3 or post-M1.2, if implicated |

## 5. Metrics and their role

**Framing rule (applies to all reporting):** no metric below is sufficient to determine
what happened; even taken together they do not explain a failure. Metrics are at-a-glance
detectors of where outputs differ from expectations. The primary instrument is the
qualitative comparison of the learned framework (`bk.sol.aba`, `prolog.stdout`) against
the pre-specified expected output, per (arm, fixture) cell.

Per cell, record:

1. **Outcome class** (categorical, table-relative): `exact expected match` /
   `parent superset` / `misaligned assumption structure` / `non-parent rule` /
   `ancestor citation` (chain family) / `no solution` / `timeout` / `error`.
   (`correct defeasible structure` is retained in the classifier for **deferred**
   incoherent follow-up only; it is not an expected primary outcome class in the M1.2
   grid.)
2. **Parent-recovery F1** on the **body-scope** variable set (base variables in
   target-rule bodies; continuity with M1.1), plus the **framework-scope** variable set
   (base variables anywhere in the learned delta, contraries included) recorded as a
   second column. Divergence between the two sets is itself a qualitative flag (M1.1 cat3
   A/D put the parent in contraries only).
3. **Two binary coverage flags**, derived from the existing coverage infrastructure:
   `covers_all_pos` (every \(E^+\) atom covered) and `rejects_all_neg` (no \(E^-\) atom
   covered). **Validity boundary (documented):** the existing coverage checks (`cov_py`
   replay, `cov_pl` Prolog re-query) are exact and agree on assumption-free solutions; on
   assumption-bearing solutions they bracket the truth (replay over-approximates by
   ignoring assumption guards; re-query under-approximates because assumptions have no
   defining clause in the solution file). The flags are computed from the coverage pass
   with both sources recorded; on assumption-bearing solutions the qualitative
   expected-structure comparison is authoritative.
4. **Framework complexity:** number of learned rules, assumptions, contraries; max/mean
   body length. Minimality matters: more minimal solutions are preferred.
5. **Trace line count** of `prolog.stdout`, as the reproducible runtime proxy (wall-clock
   is recorded but treated as unreliable for reproducibility).
6. **Effective configuration provenance:** the `listing(lopt/1)` block that the engine
   prints at the start of every run, captured from `prolog.stdout` and checked against the
   consulted config file.

Adapting `causal/metrics.py` and the outcome classifier to items 1–5 is in-scope
implementation work for this part.

## 6. Infrastructure changes (in-scope work)

1. **Runner consults config files.** Extend the grid runner / `ABASPRunner` path so an
   experiment YAML can specify `prolog_config: <path>.pl`; the generated Prolog program
   then consults that file (after `aba_asp.pl`, before the BK) instead of emitting
   individual `set_lopt` directives. This is the only way to express the 0-ary
   `check_ic` flag and guarantees the published configuration is run verbatim
   (`check_ic` is kept). `folding_steps` is **not** harmonised across arms: the ECAI
   config fixes `folding_steps(10)` and fidelity wins over harmonisation (recorded
   caveat).
2. **BK writer extension** for the RuleML `domain/1` element (Section 3), on the RuleML
   arm only; ECAI/AAMAS use plain feature-BK.
3. **Metrics/outcome-classifier adaptation** (Section 5).
4. **Timeout:** `prolog_timeout_s: 60` for all cells. Small tabular data should not
   exceed this; any timeout is traced (what was the engine doing), not silently retried
   or pre-tuned away.
5. Engine files (`aba_asp.pl`, `gen.pl`, `folding.pl`, `configs/*.pl`, …) are **not**
   modified; all changes live under `causal/`.

## 7. Protocol (stages)

| Stage | Content | Gate |
|-------|---------|------|
| 0 | **DONE (2026-07-08).** Fixtures (`causal/experiments/handcrafted_m12.py`) + Prolog-free validation checks (`causal/tests/test_m12_fixtures.py`, 59 tests, all PASS); expected outputs locked in `docs/experiments/qualitative/M1.2-config-comparison.md` before any learning run | all checks PASS ✓ |
| 1 | **DONE (2026-07-08).** Config-consulting runner (`prolog_config`), feature-BK construction (+ RuleML `domain/1`), three arm YAMLs, and M12 summary side-car (`causal/experiments/m12_summary.py`) built + unit-tested (Prolog-free tests PASS); smoke test `M12_ecai2024`/`m12_sep` -> effective `listing(lopt/1)` matches `configs/ecai2024_config.pl` | options match config file ✓ |
| 2 | **DONE (2026-07-08).** Full grid 3 arms × 5 fixtures (15 cells), serial, timeout 60 s; all 15 cells `solved` (0 timeout/error); each config applied verbatim + distinct per arm; outcome matrix `M12_summary.md` built | all cells produce classified outcomes ✓ |
| 3 | Outcome matrix + per-cell expected-vs-learned comparison; qualitative inspection of every divergent cell | record complete |
| 4 | Findings write-up (`.tex`); registers and claims ledger synced | Samuel review |

Commands (Stage 2 form):

```bash
conda activate aba-asp
cd "/Users/samuelwaugh/Desktop/Causal ABA Learning/aba_asp"
python -m causal.experiments.run_grid --config causal/configs/experiments/M12_ecai2024.yaml --no-resume
python -m causal.experiments.run_grid --config causal/configs/experiments/M12_ruleml2025.yaml --no-resume
python -m causal.experiments.run_grid --config causal/configs/experiments/M12_aamas2025.yaml --no-resume
```

## 8. Artefact and documentation layout

| Artefact | Path |
|----------|------|
| Fixtures | `causal/experiments/handcrafted_m12.py` |
| Arm configs | `causal/configs/experiments/M12_ecai2024.yaml`, `M12_ruleml2025.yaml`, `M12_aamas2025.yaml` (`grid.cell_dir: dgp`) |
| Grid outputs | `causal/outputs/aba_learning/grid/M12_<arm>/cells/<fixture>/` |
| Experiment record | `docs/experiments/qualitative/M1.2-config-comparison.md` (from `docs/experiments/TEMPLATE.md`) |
| Findings | `docs/report/findings/milestone1_part2_m12_findings.tex` |
| Registers to sync | `docs/experiments/experiments_summary.md`, `docs/research/experiment_register.md`, `docs/report/claims_ledger.md` |

## 9. Interpretation rules and caveats

- Success in a cell = the learned framework matches the pre-specified expected output up
  to harmless syntactic variation (variable naming, literal order, rule order).
- All M1.2 fixtures are coherent; success is an intensional rule (or small rule set)
  matching the declared mechanism. Do not treat assumption-bearing solutions as success
  unless they match the pre-specified expected output for that fixture.
- **Entailment-gate divergence (RuleML vs AAMAS)** was the main predicted difference
  between the two greedy arms on minimally incoherent tables; those families are
  **deferred** (Section 4.1). M1.2 must not claim to have tested that divergence unless
  a follow-up experiment is run.
- Divergence between arms on a fixture is the unit of finding: report *which* data
  property exposed it and *which* configuration difference plausibly drives it
  (mechanistic confirmation is M1.3's job, not M1.2's).
- **`m12_fork`:** a failure citing `x1` instead of `x0` is a correlated-sibling confound
  (associated non-separator), distinct from `m12_sep` (isolated noise) and `m12_chain`
  (ancestor vs parent).
- What M1.2 does **not** show: causal discovery; Russo-style Causal ABA behaviour;
  assumption/entailment-gate behaviour on incoherent tables (deferred); performance of
  the redress workflow (deferred); behaviour under cautious semantics; robustness to
  representation order (established separately by M1.1).
