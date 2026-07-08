# Milestone 1, Part 2 (M1.2) — Published-configuration comparison on divergence-designed fixtures

**Status:** `planned`
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
  near-term follow-up after M1.2.
- **All arms are brave**, as published. No cautious arm; the published methods use brave
  for a reason. Comparisons against the cautious-default M1.1/QI results are therefore
  cross-configuration observations, not controlled comparisons.
- **No repeat-stability measurement.** The algorithms have no probabilistic component and
  clingo is deterministic for fixed input, flags, and version; identical reruns give
  identical output.
- **`asm_intro(relto)` in all arms** (as the config files specify). The repo's AA-CBR
  example (`examples/aacbr2.bk.aba:19`) suggests `sechk` for that example; the config
  files are treated as canonical. Recorded caveat: if M1.3 implicates
  assumption-introduction behaviour in a failure mode, a single `sechk` ablation on the
  implicated cell is the designated follow-up.
- **`ecai2024ALL_config.pl` (fold-all variant) is excluded** from M1.2; flagged for later
  consideration.
- **Honesty note for the write-up:** the RuleML and AAMAS configurations differ *only* in
  the post-folding entailment gate. The three-system comparison therefore factorises as
  {nd/any/all vs greedy/mgr/bk} × {gate on vs off}, and the report must not overstate the
  independence of the two greedy arms.

## 3. Encoding and the default-assumption construction

Shared encoding for all arms (inputs identical across arms, per fixture):

- rows are cases with numeric sample ids 1..N;
- each categorical predictor (\(k = 3\) values) is encoded as one-hot value predicates
  `xi_val_v(A) :- A=id.`;
- the target is excluded from the feature BK; \(E^+\) = target atoms of the designated
  positive class, \(E^-\) = the rest.

**Default assumption and contrary (AAMAS framing).** Following the Greedy ABA Learning
paper's casebase construction, the shared fixture BK additionally declares the default
rule and bogus assumption/contrary for the target, in the idiom of
`examples/aacbr2.bk.aba`:

```prolog
t(X) :- domain(X), alpha(X).
domain(1). ... domain(N).
assumption(alpha(X)).
contrary(alpha(X), c_alpha(X)) :- assumption(alpha(X)).
```

(with `t` the fixture's target predicate). This makes the learning problem well-posed in
the AAMAS casebase sense for the greedy arms. It is added to **all** arms so that every
configuration sees identical input; how the ECAI arm interacts with a pre-declared
assumption is itself an observation M1.2 records. The exact syntactic form is finalised at
implementation against the AAMAS paper's construction and validated in Stage 0.

## 4. Fixture families

All fixtures are minimal handcrafted categorical tables with \(k = 3\) values per
predictor; \(p\) (number of predictors) is fixture-dependent. **Every fixture must declare
its intended graph \(G\) (nodes, directed edges) and mechanism in three places: the
fixture code (docstring + machine-readable `edges` metadata), the run config/record, and
any findings `.tex`.**

Expected outputs are pre-specified per cell before any run, and are **table-relative**:
for coherent tables the expected output is an intensional rule (or rules); for incoherent
tables no perfect separator exists, so the *correct* output is a defeasible structure
(general rule + assumption + contrary aligned with the colliding rows), and an
assumption-free rule would be wrong.

| Family | Key | \(G\) (declared) | \(p\) | Table sketch | Expected learned output |
|--------|-----|------------------|------|--------------|--------------------------|
| Separator anchor | `m12_sep` | `x1 -> x2`; `x0` isolated | 2 | complete factorial over (x0,x1), 9 rows; `x2 := x1`; positive class `x2=2` | `x2(A) :- x1_val_2(A).` (M1.1-style anchor, retained as one family among several) |
| Conjunctive mechanism | `m12_conj` | `x0 -> x3`, `x1 -> x3`; `x2` isolated | 3 | complete factorial over (x0,x1,x2), 27 rows; `x3` positive iff `x0=2 ∧ x1=2` | `x3(A) :- x0_val_2(A), x1_val_2(A).` — no single literal separates |
| Disjunctive mechanism | `m12_disj` | `x0 -> x2`, `x1 -> x2` | 2 | complete factorial over (x0,x1), 9 rows; `x2` positive iff `x0=2 ∨ x1=2` | two rules: `x2(A) :- x0_val_2(A).` and `x2(A) :- x1_val_2(A).` |
| Incoherent, positive collision | `m12_incoh_pos` | as `m12_sep` | 2 | `m12_sep` table + one duplicated (x0,x1) row of a **positive** row with flipped (negative) class | general parent rule + assumption whose contrary fires exactly on the colliding negative sample |
| Incoherent, negative collision | `m12_incoh_neg` | as `m12_sep` | 2 | `m12_sep` table + one duplicated (x0,x1) row of a **negative** row with flipped (positive) class | parent rule + defeasible exception structure covering exactly the colliding positive sample |
| Correlated ancestor | `m12_chain` | `x0 -> x1 -> x2` | 2 | non-factorial table: `x1` correlated with `x0`; `x2 := x1`; constructed so the parent value predicate is the **unique** zero-error separator while the ancestor is strictly associated but imperfect | `x2(A) :- x1_val_2(A).` — failure mode of interest: ancestor (`x0`) citation |

Rationale per family: `m12_sep` anchors against M1.1; `m12_conj` probes exhaustive vs
token-bounded folding and `mgr` generalisation; `m12_disj` probes multi-rule learning and
subsumption; the `m12_incoh_*` pair probes assumption/attack machinery under brave
semantics and is where the entailment-gate difference (RuleML vs AAMAS) is predicted to
show; `m12_chain` is the genuinely causal discrimination test (parent vs correlated
ancestor) that the M1.1 isolated-non-parent tables could not provide.

Deliberately **out of scope** for M1.2 (decided at planning): σ/π order grids (M1.1
established ordering as a failure mode; revisit in M1.3 only if implicated), positive-class
sensitivity, support-vs-frequency designs, graded incoherence severity (deferred to M1.3
if incoherence handling emerges as a divergence point), binary encodings, continuous data.

Exact tables are finalised at implementation and locked by Stage-0 validation checks
(per family: row counts; declared \(G\) consistency; expected separator
existence/uniqueness; for `m12_conj`/`m12_disj`, non-existence of a smaller separating
rule; for `m12_incoh_*`, exactly one colliding pair at the intended row; for `m12_chain`,
parent unique zero-error separator + ancestor associated-but-imperfect).

## 5. Metrics and their role

**Framing rule (applies to all reporting):** no metric below is sufficient to determine
what happened; even taken together they do not explain a failure. Metrics are at-a-glance
detectors of where outputs differ from expectations. The primary instrument is the
qualitative comparison of the learned framework (`bk.sol.aba`, `prolog.stdout`) against
the pre-specified expected output, per (arm, fixture) cell.

Per cell, record:

1. **Outcome class** (categorical, table-relative): `exact expected match` /
   `correct defeasible structure` (incoherent families only) / `parent superset` /
   `misaligned assumption structure` / `non-parent rule` / `no solution` / `timeout` /
   `error`.
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
2. **BK writer extension** for the default rule / bogus assumption+contrary construction
   (Section 3), shared across arms.
3. **Metrics/outcome-classifier adaptation** (Section 5).
4. **Timeout:** `prolog_timeout_s: 60` for all cells. Small tabular data should not
   exceed this; any timeout is traced (what was the engine doing), not silently retried
   or pre-tuned away.
5. Engine files (`aba_asp.pl`, `gen.pl`, `folding.pl`, `configs/*.pl`, …) are **not**
   modified; all changes live under `causal/`.

## 7. Protocol (stages)

| Stage | Content | Gate |
|-------|---------|------|
| 0 | Implement fixtures (`causal/experiments/handcrafted_m12.py`) + Prolog-free validation checks (Section 4); write expected outputs into this plan's companion record before any learning run | all checks PASS |
| 1 | Runner/BK/metrics infrastructure (Section 6); smoke-test one arm on `m12_sep`; verify effective options from `listing(lopt/1)` | options match config file |
| 2 | Full grid: 3 arms × 6 fixtures (18 cells), serial | all cells produce classified outcomes |
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
| Arm configs | `causal/configs/experiments/M12_ecai2024.yaml`, `M12_ruleml2025.yaml`, `M12_aamas2025.yaml` |
| Grid outputs | `causal/outputs/aba_learning/grid/M12_<arm>/cells/<fixture>/` |
| Experiment record | `docs/experiments/qualitative/M1.2-config-comparison.md` (from `docs/experiments/TEMPLATE.md`) |
| Findings | `docs/report/findings/milestone1_part2_m12_findings.tex` |
| Registers to sync | `docs/experiments/experiments_summary.md`, `docs/research/experiment_register.md`, `docs/report/claims_ledger.md` |

## 9. Interpretation rules and caveats

- Success in a cell = the learned framework matches the pre-specified expected output up
  to harmless syntactic variation (variable naming, literal order, rule order).
- A `correct defeasible structure` verdict in the incoherent families requires the
  exception to align with the actual colliding row(s), verified by inspection — not
  merely the presence of assumptions.
- Divergence between arms on a fixture is the unit of finding: report *which* data
  property exposed it and *which* configuration difference plausibly drives it
  (mechanistic confirmation is M1.3's job, not M1.2's).
- What M1.2 does **not** show: causal discovery; Russo-style Causal ABA behaviour;
  performance of the redress workflow; behaviour under cautious semantics; robustness to
  representation order (established separately by M1.1).
