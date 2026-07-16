# Milestone 1, Part 2 (M1.2) — Published-configuration comparison on divergence-designed fixtures

**Primary path:** [`../milestone1_high_level_path.md`](../milestone1_high_level_path.md)  
**Expanded Approach:** [`milestone1_part2_expanded_approach.md`](milestone1_part2_expanded_approach.md)

**Status:** pilot `analysed` (Stages 0–3); **expanded Approach locked**; graph/mechanism
cards next. Pilot: 10/10 scoped cells `solved` (2026-07-09, commit `9123af7`); cell
inspection 2026-07-13. Pilot fixtures/labels will be redesigned under the Approach;
Stage 4 findings tex deferred until the expanded grid is done.
**Experiment ID:** `M12_config_comparison` (configs `M12_ecai2024`, `M12_aamas2025`)
**Parent index:** [milestone1-plan.md](../milestone1-plan.md) (Part 2 section)

**Expansion:** follow the Approach doc (deterministic copy/min/max; \(k=3\); nonzero-
positive; `val`+`nz` BK; ECAI+AAMAS; all non-source targets; descendant exclusion).

## 1. Goal and research question

Compare the two published ABA Learning configurations in M1.2 scope, shipped with the inherited
engine, run one-shot on shared handcrafted categorical fixtures, and report clearly when
and how each recovers the **mechanism-aligned rules** warranted by the fixture's declared
graph and mechanism.

> **RQ (M1.2).** For a fixed encoding of small categorical tables (each generated from a
> declared graph \(G\) and mechanism, with a pre-specified expected learned output), how do
> ASP-ABAlearnB and Greedy ABA Learning differ in (a) whether the expected
> output is learned, (b) the structural class of what is learned instead, and (c) which
> data properties expose divergence between the two systems?

This is unguided ABA Learning only: no Causal ABA machinery (`arr`/`noe`/`indep`,
d-separation, stable-extension-as-DAG) is exercised. Results characterise recovery of
mechanism-aligned rules, not causal discovery.

## 2. Systems under comparison

The two arms are the engine's shipped configuration files, consulted **verbatim** for
provenance:

| Arm | Config file | Published system | Verified option content |
|-----|-------------|------------------|--------------------------|
| ECAI | `configs/ecai2024_config.pl` | ASP-ABAlearnB (ECAI 2024, "Learning Brave ABA Frameworks via ASP") | brave; `nd` folding, `folding_steps(10)`; selection `any`; space `all`; `asm_intro(relto)`; `check_ic` |
| AAMAS | `configs/aamas2025_config.pl` | Greedy ABA Learning for CBR (AAMAS 2025) | brave; `greedy` folding; selection `mgr`; space `bk`; `asm_intro(relto)`; `check_ic`; post-folding entailment gate at engine default (`true`) |

Design decisions fixed at planning time:

- **Scope correction (2026-07-13):** the RuleML/RASP arm was removed from M1.2. Its
  redress workflow is outside this investigation rather than a deferred M1.2 follow-up.
- **Both arms are brave**, as published. No cautious arm; the published methods use brave
  for a reason. Comparisons against the cautious-default M1.1/QI results are therefore
  cross-configuration observations, not controlled comparisons.
- **No repeat-stability measurement.** The algorithms have no probabilistic component and
  clingo is deterministic for fixed input, flags, and version; identical reruns give
  identical output.
- **`asm_intro(relto)` in both arms** (as the config files specify); the config files are
  treated as canonical. Recorded caveat: if M1.3 implicates assumption-introduction
  behaviour in a failure mode, a single `sechk` ablation on the implicated cell is the
  designated follow-up.
- **`ecai2024ALL_config.pl` (fold-all variant) is excluded** from M1.2; flagged for later
  consideration.
- **Comparison boundary:** the scoped arms differ in folding mode, selection, and search
  space (`nd`/`any`/`all` vs `greedy`/`mgr`/`bk`). Both use the post-folding entailment
  gate, so M1.2 does not treat that gate as an arm-level explanatory variable.

## 3. Encoding

Feature encoding (identical across both arms, per fixture), matching the feature-BK
construction used by the published ECAI tabular benchmarks:

- rows are cases with numeric sample ids 1..N;
- each categorical predictor (\(k = 3\) values) is encoded as one-hot value predicates
  `xi_val_v(A) :- A=id.`;
- the target is excluded from the feature BK; \(E^+\) = target atoms of the designated
  positive class, \(E^-\) = the rest;
- learning is driven by `E^+`/`E^-` only: the engine rote-learns the target atoms and
  folds them into intensional target rules (`t(A) :- xi_val_v(A)`), the same path the
  shipped ECAI tabular benchmarks use.

No default rule and no assumption/contrary are declared in the input. ECAI and AAMAS use
the same feature encoding, so the comparison isolates their scoped configuration
differences. Validated in Stage 0/1.

## 4. Fixture families

All fixtures are minimal handcrafted categorical tables with \(k = 3\) values per
predictor and two predictors (`x0`, `x1`). **Every fixture must declare
its intended graph \(G\) (nodes, directed edges) and mechanism in three places: the
fixture code (docstring + machine-readable `edges` metadata), the run config/record, and
any findings `.tex`.**

Expected outputs are pre-specified per cell before any run. All M1.2 fixtures are
**coherent** tables with intensional expected rules (or a small rule set). Incoherent
tables and defeasible expected outputs are outside this investigation.

All five fixtures are minimal **3-variable** categorical tables (`x0, x1, x2`), target
`x2`, positive class `x2 = 2`, with no duplicate rows.

| Family | Key | \(G\) (declared topology) | Table sketch | Expected learned output |
|--------|-----|---------------------------|--------------|--------------------------|
| Separator anchor | `m12_sep` | `x1 -> x2`; `x0` isolated (non-parent) | complete factorial over (x0,x1), 9 rows; `x2 := x1` | `x2(A) :- x1_val_2(A).` (M1.1-style anchor) |
| Conjunctive collider | `m12_conj` | **Collider:** `x0 -> x2`, `x1 -> x2` | complete factorial over (x0,x1), 9 rows; **conjunctive mechanism:** `x2 := min(x0,x1)`, positive iff `x0=2 ∧ x1=2` (single positive row) | `x2(A) :- x0_val_2(A), x1_val_2(A).` — no single literal separates |
| Disjunctive collider | `m12_disj` | **Collider:** `x0 -> x2`, `x1 -> x2` (same topology as `m12_conj`) | complete factorial over (x0,x1), 9 rows; **disjunctive mechanism:** `x2 := max(x0,x1)`, positive iff `x0=2 ∨ x1=2` (5 pos / 4 neg) | two rules: `x2(A) :- x0_val_2(A).` and `x2(A) :- x1_val_2(A).` |
| Fork (correlated sibling) | `m12_fork` | **Fork:** `x0 -> x1`, `x0 -> x2` | **deterministic two-child fork**, 3 rows (one each): (x0,x1,x2) = (0,0,0), (1,2,0), (2,0,2); mechanisms `x1 := 2 if x0=1 else 0`, `x2 := 2 if x0=2 else 0`; positive iff `x0=2` (single positive row) | `x2(A) :- x0_val_2(A).` |
| Correlated ancestor | `m12_chain` | **Chain:** `x0 -> x1 -> x2` | non-factorial, 6 rows: for each `x0`, `x1 := x0` and `x1 := (x0+1) mod 3`; `x2 := x1`; parent value predicate is the **unique** zero-error separator; ancestor associated (P(pos\|x0)=0, 1/2, 1/2) but imperfect | `x2(A) :- x1_val_2(A).` — failure mode of interest: ancestor (`x0`) citation |

**Naming note:** `m12_conj` and `m12_disj` are named for their **mechanism** (conjunctive
vs disjunctive positive class) on a **collider** topology (two directed edges into the
target `x2`). They are twins: same declared G (`x0 -> x2`, `x1 -> x2`), same 9-row
factorial over (x0,x1); they differ only in mechanism (`min` vs `max`) and expected rule
shape. They are not fork topologies. `m12_fork` is the fork-topology family (shared cause
`x0`, two effects `x1` and `x2`).

Rationale per family:

- **`m12_sep`** — anchors against M1.1; isolated non-parent vs direct parent (unique
  separator).
- **`m12_conj`** — collider with conjunctive mechanism; probes `mgr` generalisation when
  no single literal separates (a single positive row).
- **`m12_disj`** — collider with disjunctive mechanism (twin of `m12_conj`); differs only
  in mechanism (`max` vs `min`) and expected two-rule output. Probes multi-rule learning
  and subsumption.
- **`m12_fork`** — fork topology; probes **correlated-sibling confound**: `x1` is
  associated with `x2` via shared cause `x0` but is **not** a zero-error separator.
  Distinct from `m12_sep` (isolated noise variable) and `m12_chain` (ancestor vs parent
  on a chain). Both children are deterministic functions of `x0`, so the edge
  `x0 -> x1` leaves a data-level trace. Two design notes: `x1` takes exactly two values
  (a deterministic imperfect separator of a 3-valued cause cannot be injective), and its
  alphabet is {0,2} rather than {0,1} so it stays on the `x1_val_v` value-predicate
  encoding path (value-set-{0,1} columns are emitted as bare binary predicates).
- **`m12_chain`** — chain topology; parent vs correlated-ancestor discrimination (parent
  is unique separator; ancestor associated but imperfect).

**Grid size:** 2 arms × 5 fixtures = **10 cells**.

Deliberately **out of scope** for M1.2 (decided at planning): σ/π order grids (M1.1
established ordering as a failure mode; revisit in M1.3 only if implicated), positive-class
sensitivity, support-vs-frequency designs, binary encodings, continuous data, incoherent
tables.

Exact tables are finalised at implementation and locked by Stage-0 validation checks
(per family: row counts; declared \(G\) consistency; expected separator
existence/uniqueness; for `m12_conj`/`m12_disj`, non-existence of a smaller separating
rule; for `m12_fork`, see fork checks below; for `m12_chain`, parent unique zero-error
separator + ancestor associated-but-imperfect). Exact tables, E+/E-, and locked expected
outputs: `docs/experiments/qualitative/M1.2-config-comparison.md`; fixtures in
`causal/experiments/handcrafted_m12.py`; checks in `causal/tests/test_m12_fixtures.py`.

**Stage-0 validation — `m12_fork` (Prolog-free):**

- 3 rows: three distinct deterministic rows (0,0,0), (1,2,0), (2,0,2), one each (no
  repetition);
- `x0` is the unique zero-error separator for the positive class (`x0` takes all 3
  values);
- `x1` is associated with `x2` but is **not** a zero-error separator;
- declared edges match fork topology (`x0 -> x1`, `x0 -> x2`);
- no column has value set exactly {0,1} (bare-binary encoding guard).

### 4.1 Items outside the M1.2 grid

The following is explicitly **out of the M1.2 grid** and would require its own experiment
ID and plan if scheduled.

| Item | Scope | Rationale | When |
|---------------|---------------------|-----------|------|
| `ecai2024ALL_config.pl` | fold-all variant | Excluded from M1.2; flagged for later consideration. | TBD |

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
   (`correct defeasible structure` is outside the M1.2 grid; it is not an expected
   primary outcome class here.)
2. **Parent-recovery F1** on the **body-scope** variable set (base variables in
   target-rule bodies; continuity with M1.1), plus the **framework-scope** variable set
   (base variables anywhere in the learned delta, contraries included) recorded as a
   second column. Divergence between the two sets is itself a qualitative flag (M1.1 cat3
   A/D put the parent in contraries only).
3. **ASP sample-coverage fractions:** `pos_covered` and `neg_rejected`, computed by brave
   clingo checks against each learned `bk.sol.asp`. These replace the earlier Horn replay
   flags; the qualitative expected-structure comparison remains authoritative for
   intensional match.
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
2. **Shared feature-BK construction** for both scoped arms (Section 3).
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
| 1 | **DONE (2026-07-08).** Config-consulting runner (`prolog_config`), shared feature-BK construction, two arm YAMLs, and M12 summary side-car (`causal/experiments/m12_summary.py`) built + unit-tested (Prolog-free tests PASS); smoke test `M12_ecai2024`/`m12_sep` -> effective `listing(lopt/1)` matches `configs/ecai2024_config.pl` | options match config file ✓ |
| 2 | **DONE (2026-07-09, commit `9123af7`).** Scoped grid on revised minimal fixtures (2 arms × 5 fixtures, `--no-resume`); 10/10 `solved`; `M12_summary.md` rebuilt. Exact-match detector: 2/10 (ECAI/fork, AAMAS/conj) | all cells produce classified outcomes ✓ |
| 3 | **DONE (2026-07-13).** Pilot outcome matrix + per-cell expected-vs-learned comparison | pilot record complete ✓ |
| E | **NEXT.** Expand M1.2 per [`../milestone1_high_level_path.md`](../milestone1_high_level_path.md): lock Fabrizio small-DAG set + DGP(s) + intended rules; implement; run ECAI+AAMAS; inspect | every new cell has intended output + inspection |
| 4 | Findings write-up (`.tex`) after expansion (pilot may be an appendix); registers synced | Samuel review |

Commands (Stage 2 form):

```bash
conda activate aba-asp
cd "/Users/samuelwaugh/Desktop/Causal ABA Learning/aba_asp"
python -m causal.experiments.run_grid --config causal/configs/experiments/M12_ecai2024.yaml --no-resume
python -m causal.experiments.run_grid --config causal/configs/experiments/M12_aamas2025.yaml --no-resume
```

## 8. Artefact and documentation layout

| Artefact | Path |
|----------|------|
| Fixtures | `causal/experiments/handcrafted_m12.py` |
| Arm configs | `causal/configs/experiments/M12_ecai2024.yaml`, `M12_aamas2025.yaml` (`grid.cell_dir: dgp`) |
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
- Divergence between arms on a fixture is the unit of finding: report *which* data
  property exposed it and *which* configuration difference plausibly drives it
  (mechanistic confirmation is M1.3's job, not M1.2's).
- **`m12_fork`:** a failure citing `x1` instead of `x0` is a correlated-sibling confound
  (associated non-separator), distinct from `m12_sep` (isolated noise) and `m12_chain`
  (ancestor vs parent).
- What M1.2 does **not** show: causal discovery; Russo-style Causal ABA behaviour;
  behaviour under cautious semantics; robustness to representation order (established
  separately by M1.1).
