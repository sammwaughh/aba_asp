# Research decisions

Recorded decisions that affect experiment direction. Evidence and interpretation remain in experiment records.

## 2026-07-31 — Lowercase learner identifiers for future causal fixtures

**Decision:** Future target-wise causal fixtures use safe lowercase internal variable
identifiers such as `a`, `b`, `c`, `d`, ... in YAML, CSV, ABA predicates, target names,
and output paths. Scientific descriptions may display the corresponding variables as
(A,B,C,D,\ldots). Existing `x0`, `x1`, ... fixtures, configurations, runs, and locked
evidence remain unchanged and supported.

**Prolog/ABA distinction:** In `c(A)`, `c/1` is the causal-variable predicate and `A` is
the Prolog variable for a row identifier. Learner-generated assumptions and contraries
use the separate `alpha_N` and `c_alpha_N` namespaces. Future fixture identifiers must
not use reserved ABA/learner names such as `assumption`, `contrary`, `not`, `alpha`,
`alpha_*`, `c_alpha`, or `c_alpha_*`.

**Implementation boundary:** Adapt only the Python fixture/reference/target-wise
encoding, diagnostics, tests, and documentation. Do not modify inherited `.pl` files or
the locked legacy metric parser. Target-wise body-variable inspection must use the
fixture's declared variable list rather than assume names of the form `xN`.

## 2026-07-31 — Bucket 3 immediate focus: deterministic mechanisms with root noise

**Decision:** Develop Bucket 3 one mechanism case at a time using binary causal models
whose root variables have mutually independent non-degenerate distributions and whose
non-root variables are deterministic functions of their causal parents. Before any
ABALearn run, derive the population, audit ordinary faithfulness for that exact fixture,
and record an evaluator-only mechanism/rule reference.

The reference distinguishes the complete structural truth table, population-supported
parent configurations, configurations observed in the frozen finite sample, and
canonical positive-state exact-value rules. Root targets are recorded as having no
deterministic causal rule over other observed variables. Exact rule-string equality is
not adopted as an automatic recovery verdict.

**Preservation:** The existing positive-stochastic binary diamond, its generated fixture
artefacts, configurations, and target-wise runs remain unchanged as pre-pivot
exploratory/infrastructure material. They do not yet support a Bucket 3 claim. M12x and
Buckets 1–2 remain locked.

**Sequencing:** The wider 22 July dimensions remain within the possible Bucket 3 scope
but are deferred. No deterministic research fixture, experiment matrix, or claim is
approved by this decision. The next research decision is the graph, root probabilities,
and deterministic functions for one first fixture.

**Open theory point:** For (A \to B\) with (B := A) and no other variables,
observational dependence does not orient the edge. Whether a copy edge can be oriented
inside a larger graph depends on the additional structure and is not settled here.

**Implementation boundary:** Extend only the generic fixture/certificate/sampling
infrastructure and documentation. Do not change inherited ABALearn semantics or create
the first deterministic research fixture without a further Samuel decision.

## 2026-07-30 — Target-wise checked ASP retained only as an artefact audit

**Decision:** For causal-fixture target-wise runs, retain outcome/failure/runtime,
learned rules and counts, assumptions/contraries, and rule-body variables/lengths.
Do not add Python-Horn, Prolog-query, independent per-example ASP, parent-set, or
graph-level coverage panels.

The inherited learner already emits `<BK>.sol_chk.asp` when
`set_lopt(check_ic)` is enabled. This file contains the final framework's ASP
serialization together with the joint positive/negative integrity constraints.
The target-wise runner will invoke Clingo directly on this saved file once and
record SAT/UNSAT/error/runtime only as a final-serialization integrity audit. It
will not reconstruct the same constraints around `<BK>.sol.asp`, and the audit
will not be interpreted as a separate coverage or learner-performance metric.

**Implementation boundary:** target-wise configurations must explicitly enable
`check_ic`. The inherited ABA Learning engine and completed earlier experiment
artefacts remain unchanged.

**Inspection convention:** Future target-wise cells retain unique execution
stems only internally. Their final output files use `bk.sol.aba`,
`bk.sol.asp`, and `bk.sol_chk.asp`. Each solved cell also writes `delta.aba`,
containing exactly the learned additions relative to its frozen input BK.

## 2026-07-22 — Close Bucket 2; expand M1.3 with supervisor-driven Bucket 3

**Decision:** M1.3 Bucket 2 is **locked / closed** with two claims supported by
M13-C1 and M13-C2. The proposed deterministic-target failure claim is parked and is not
part of Bucket 2. M12x and Buckets 1–2 remain fixed evidence and will not be redone.

Following Fabrizio's 22 July guidance, Milestone 1 continues for the coming week.
M1.3 will expand through a new Bucket 3 whose claims and experiments are not yet
decided. The planning scope includes target variation, partial data availability,
larger controlled graphs, explicit marginal/conditional-independence and Markov
equivalence analysis, graph–mechanism validity, and separation of learning-strategy
failures from information or data limitations. Category-count and non-discrete
extensions remain possible rather than committed.

**Guardrail:** this is a scope decision, not an experiment plan. Do not invent Bucket 3
claims, fixtures, or conclusions before the planned theory/evidence review and
Samuel's approval.

**Records:** `docs/research/supervisor_guidance.md` (22 July meeting);
`docs/experiments/qualitative/M1.3-bucket3-claims.md`;
`docs/research/milestone_plans/milestone1_part3/`.

**Next:** synchronise the ChatGPT context, then conduct the collaborative Bucket 3
planning process. Milestone 2 has not started.

## 2026-07-21 — Accept M13-C1/C2 evidence; proceed to Bucket 2 Claim 3 *(next-step superseded 22 July)*

**Decision:** Bucket 2 Claims 1–2 are written from analysed targeted controls.
M13-C1 establishes causal-role underdetermination under learner-input equivalence.
M13-C2 establishes the bounded ECAI/AAMAS contrast under exact-value BK
feature-block permutations. These claims remain scoped to their stated tasks and do not
assert full causal discovery or general greedy order-invariance.

**Evidence:** `M13-C1-causal-role-underdetermination/experiment.md`;
`M13-C2-bk-feature-order/experiment.md`; `M1.3-bucket2-claims.md`.

**Historical next step:** investigate Bucket 2 Claim 3 using the U6/U7 support contrast
and the new M13-C2 U7 order evidence. Superseded by the 22 July decision to close
Bucket 2 and open Bucket 3.

## 2026-07-21 — M1.3 Bucket 1 locked; commence Bucket 2

**Decision:** M1.3 Bucket 1 (four claims with Markdown record and TeX companion) is
**written / locked**. Bucket 2 claim drafting **commences** now. Bucket 2 claims are
those that need probes, controls, or interventions beyond the locked M12x Stage-3
package.

**Artefacts:**
- Bucket 1: `docs/experiments/qualitative/M1.3-bucket1-claims.md`;
  `docs/report/findings/milestone1_part3_bucket1_claims.tex`
- Bucket 2 stubs: `docs/experiments/qualitative/M1.3-bucket2-claims.md`;
  `docs/report/findings/milestone1_part3_bucket2_claims.tex`

**Next:** refine and write Bucket 2 claims one at a time per
`milestone1_part3_approach.md`.

## 2026-07-20 — M12x closed; commence M1.3 claim drafting

**Decision:** The expanded M1.2 (M12x) Stage-3 package is **closed** and locked as the
sole evidence base for M1.3. Claim drafting for M1.3 **commences** now from the 18/18
cell inspection and summary matrix. Prior provisional M1.3 claim drafts remain
withdrawn and must not be reused.

**Evidence package:**
- `docs/experiments/qualitative/M1.2-expanded.md`
- `docs/experiments/qualitative/M1.2-expanded-cell-inspection.md` (18/18)
- `causal/outputs/aba_learning/grid/M12x_summary.md`
- `causal/outputs/aba_learning/grid/M12x_cell_reports/`

**Next:** draft live claim list (3–10) → choose order → investigate claims one at a time
per `milestone1_part3_approach.md`.

## 2026-07-20 — Delete prior M12x outputs; fresh 18-cell run is sole evidence

**Decision:** Delete all prior M12x runner artefacts and the Stage-3 inspection stub.
Status resets to **`implemented`** (design locked; awaiting fresh run). Do not treat
any previous M12x grid (22-cell or redesign) as evidence for the locked design.

**Deleted:**
- `causal/outputs/aba_learning/grid/M12x_{ecai2024,aamas2025}/`
- `M12x_summary.md` / `.json`; `M12x_learned_rules.md`; `M12x_cell_reports/`
- `docs/experiments/qualitative/M1.2-expanded-cell-inspection.md`

**Next evidence:** `--no-resume` both arms → `m12x_summary` → new Stage-3 only.

## 2026-07-20 — Rename M12x fixture keys U4–U7 to match mechanisms

**Decision:** Rename keys (and mechanism card filenames) so names match the catalogue:

| Old | New |
|-----|-----|
| `m12_u4_fork_double_copy` | `m12_u4_fork_asymmetric` |
| `m12_u5_chain_double_copy` | `m12_u5_chain_curated` |
| `m12_u6_g1_and_cone` | `m12_u6_g1_min_diff` |
| `m12_u7_g1_or_cone` | `m12_u7_diamond_noisy` |

Also drop “all non-source targets” / “always full factorial” slogans where they conflict
with U5/U7 curated support and selective targets.

## 2026-07-20 — U5: drop intermediate \(x_1\) as learning target

**Decision:** U5 learning target is \(x_2\) only (2 cells). Do not learn \(x_1\):
on the pilot table \(x_2=\operatorname{copy}(x_1)\), so there is no parent-aligned
\(\mathcal{H}_{x_1}^\star\) and the descendant is the unique perfect separator in BK.
Descendant-citation failure mode remains covered by U6-\(x_2\). Grid size **18 cells**
(9 unit–target pairs × {ECAI, AAMAS}).

## 2026-07-20 — U7 diamond (noisy fork arms)

**Decision:** Replace U7 G1 OR cone with diamond
\(x_0\to x_1,\,x_0\to x_2,\,x_1\to x_3,\,x_2\to x_3\).
Curated support (U5-style): for each \(x_0\), \(x_1:=(x_0+1)\bmod 3\) and
\(x_2\in\{(x_0+2)\bmod 3,\,x_1\}\); \(x_3:=|x_1-x_2|\).
Nonzero-positive; `val`-only. Target \(x_3\) only (2 cells). Fixture key
`m12_u7_diamond_noisy`. Grid size was **20 cells** after this change (later 18 after
dropping U5-\(x_1\)). Root and each sibling fail as
`val`-union separators; \(\mathcal{H}^\star\) needs both \(\{x_1,x_2\}\).

## 2026-07-20 — U6 min then difference (not double-min)

**Decision:** Keep Fabrizio G1. Mechanisms: \(x_2:=\min(x_0,x_1)\), \(x_3:=x_1-x_2\).
Nonzero-positive labels; `val`-only BK/\(\mathcal{H}^\star\). Fixture key
`m12_u6_g1_min_diff`. Sink concept: \(x_3\neq 0\iff x_1>x_2\) (both parents required).
Rejects alternating min/max (projects to \(x_1\)) and double-min (\(x_3=x_2\)).

## 2026-07-20 — U5 pilot chain (correlated ancestor)

**Decision:** Replace U5 double copy with the pilot `m12_chain` 6-row support:
for each \(x_0\), pairs \((x_0,x_0)\) and \((x_0,(x_0+1)\bmod 3)\); \(x_2:=\operatorname{copy}(x_1)\).
Nonzero-positive labels; `val`-only BK/\(\mathcal{H}^\star\). Fixture key
`m12_u5_chain_curated`. Learning target \(x_2\) only
(\(\mathcal{H}_{x_2}^\star\): `x1_val_1`/`x1_val_2`). Intermediate \(x_1\) was briefly
retained then dropped the same day (see decision above).

## 2026-07-20 — U4 Option B fork (asymmetric maps)

**Decision:** Replace U4 double copy with
\(x_1 := 2\cdot\mathbf{1}_{x_0\neq 2}\), \(x_2 := 2\cdot\mathbf{1}_{x_0\neq 0}\).
Parent unique perfect separator; sibling imperfect. Nonzero-positive labels; `val`-only
\(\mathcal{H}^\star\). Fixture key `m12_u4_fork_asymmetric`.

## 2026-07-20 — M12x: val-only BK; keep nonzero-positive labels

**Decision:** Background knowledge uses exact-value (`val`) predicates only.
Labels remain \(E^+=\{t\neq 0\}\), \(E^-=\{t=0\}\) unless a unit card later overrides.
Reference \(\mathcal{H}^\star\) is written in `val` (U1: two `x1_val_1/2` rules).

**U1:** graph/mechanism/table unchanged; card, catalogue, summary H*, and configs updated.

## 2026-07-20 — Withdraw M1.3 claims; redesign M12x U4–U7

**Decision:** Provisional M1.3 claim drafting from the first M12x grid is **withdrawn**
and deleted (claim list + claim working doc). Double-copy fork/chain (U4/U5) and
double min/max cones (U6/U7) are uninformative. Priority returns to **getting M12x
right** (mechanisms → cards/catalogue → fixtures → re-run → Stage-3). M1.3 Approach
method is retained but paused.

**Fork intent (U4, agreed in discussion):**  
\(x_2 := 2\) iff \(x_0\neq 0\);  
\(x_1 := 2\) iff \(x_0\neq 2\) (case-based val \(\mathcal{H}^\star\)); imperfect sibling
confounds on both targets.

## 2026-07-16 — M1.2 closed; begin M1.3

**Decision:** Expanded M1.2 (M12x) is **closed** as an evidence package (22/22
`solved`; Stage-3 inspection; summary matrix). Experimental priority moves to
**M1.3**: draft candidate claims from Stage-3 patterns; design/run smallest probes;
keep survivors; write evidence-backed subsections.

**Primary inputs:** `M1.2-expanded-cell-inspection.md`; `M12x_summary.md`;
Approach vocabulary; `milestone1_part3/`.

**Superseded 2026-07-20:** see redesign decision above.
## 2026-07-16 — Optional grid.seed (no dummy seed for deterministic grids)

**Decision:** `grid.seed` is optional. Omit it for deterministic experiments
(M12x). Slug dirs then use `{dgp}__target-{t}` with no `__seed-` suffix.
`seed: []` is rejected; stochastic discrete/continuous cells still need a seed
at run time.

## 2026-07-16 — Expanded M1.2 (M12x) grid constructed

**Decision:** Implement U1–U7 as new experiment id **M12x** (pilot `M12_*` /
`m12_*` left unchanged). Nonzero-positive labels; `val`-only BK; multi-target cells
with `grid.cell_dir: slug`; **no** `grid.seed`.

**Artefacts:** `handcrafted_m12x.py`; `M12x_{ecai2024,aamas2025}.yaml`;
`docs/experiments/qualitative/M1.2-expanded.md`.

## 2026-07-16 — Expanded M1.2: descendants stay in BK as distractors

**Decision (correction):** When learning target \(t\), background knowledge includes
**all variables except \(t\)**, including **descendants** of \(t\). They are intentional
distractors. A good learned rule should ignore them and use ancestors only. Citing a
descendant in an intensional rule is an explicit failure mode Fabrizio wants tested.

**Was wrong:** treating descendants as excluded from BK (that would make the failure-mode
test impossible).

**Updates:** `milestone1_part2_expanded_approach.md` (Predictors section); unit-set card
checklist; part2 README; decisions Approach entry below; related pointers.

## 2026-07-16 — Expanded M1.2 Approach locked (design reference)

**Decision:** Lock the expanded M1.2 **Approach** before graph selection finishes and before
any new runs. Canonical doc:
`docs/research/milestone_plans/milestone1_part2/milestone1_part2_expanded_approach.md`.

**Locked choices:**

- Deterministic DGP: local mechanisms ∈ {copy, min, max}; copy only for unique parent;
  full source factorial; alphabet \(k=3\) always; nonzero-positive labelling.
- BK: exact-value (`val`) predicates only.
- Configs: ECAI and AAMAS only.
- Cells: (fixture, non-source target, config); BK includes **all non-target columns**
  (ancestors, siblings, **and descendants**). Only the target is excluded from BK.
  Descendant (and sibling) *citation in a learned rule* is a failure/divergence to
  inspect — distractors are left in BK so the learner can be tested on ignoring them.
- Good intensional rules should use ancestors of the target only.
- Reference \(\mathcal{H}_t^\star\) in the `val` language; no precisely pre-enumerated
  acceptable set — post-run semantic inspection.
- Original five pilot fixtures will be redesigned under this regime.

**Follow-on (same day):** unit set U1–U7 accepted — see
`docs/research/milestone_plans/milestone1_part2/milestone1_part2_expanded_unit_set.md`.
Mechanism cards U1–U7 written under
`docs/research/milestone_plans/milestone1_part2/mechanism_cards/`.

**Points to:** `milestone1_high_level_path.md` (M12x redesign; M1.3 paused).

## 2026-07-16 — Milestone 1 path restated: expand M1.2, then M1.3; no M1.4

**Decision:** Finish Milestone 1 by (1) expanding M1.2 beyond the pilot 10-cell grid,
then (2) running M1.3 on that expanded evidence. There is **no M1.4**. Large-graph /
bnlearn comparisons are deferred to a later evaluation phase against any Causal-ABA-
informed solution.

**Expanded M1.2 scope:**

- Graphs: Fabrizio’s usable small DAGs already in the repo; **exclude** random graphs,
  bnlearn networks, and cycles.
- DGPs: decide which generative regimes (and how many) before implementation; compare
  within-DGP first.
- Intended learned rules: locked per (graph, DGP, target) cell before any run.
- Arms: ECAI and AAMAS only (RuleML remains out).
- Criteria: intended-rule match and ASP coverage kept separate; primary instrument is
  qualitative trace inspection across graphs.

**M1.3 scope:** draft plain-English candidate claims from the expanded matrix; design
smallest probes; keep surviving claims; write evidence-backed subsections on recovery
patterns and limits. No forced taxonomy codes required.

**Primary path document:**
`docs/research/milestone_plans/milestone1_high_level_path.md` (other M1 plans point to it).

**Supersedes:** the “pilot M1.2 done → go straight to M1.3 taxonomy” next-step framing;
any implication that large-graph / bnlearn work is part of Milestone 1.

## 2026-07-13 — M1.2 reduced to ECAI and AAMAS only

**Decision:** Remove the RuleML/RASP arm from M1.2. The investigation now compares only
ASP-ABAlearnB (`M12_ecai2024`) and Greedy ABA Learning (`M12_aamas2025`) over the five
locked fixtures: 2 arms × 5 fixtures = 10 cells.

**Impact:** M1.2 records, plans, summaries, registers, handoffs, and report-support docs
must report 10/10 scoped cells solved, exact match 2/10 (ECAI/fork and AAMAS/conj), and
ASP sample coverage 10/10. Removed-arm construction and workflow details are not part of
M1.2. The inherited paper artefact directory remains on disk and is not modified.

**Supersedes:** every earlier wider-scope M1.2 statement and every removed-arm-specific
construction or workflow statement.

**Records:** `docs/experiments/qualitative/M1.2-config-comparison.md`;
`docs/experiments/qualitative/M1.2-config-comparison-cell-inspection.md`;
`docs/research/milestone_plans/milestone1_part2/milestone1_part2_config_comparison.md`.

## 2026-07-09 — M1.2 fixtures revised to minimal 3-variable design (pre-Stage-2 correction)

**Decision:** All five M1.2 fixtures are now minimal 3-variable categorical tables over
`x0, x1, x2` with `x2` the target, positive class `x2 == 2`, and no duplicate rows:

- `m12_sep` — 9 rows, factorial over (x0,x1), `x2 := x1`, `x0` isolated.
- `m12_conj` — 9 rows, collider `x0 -> x2 <- x1`, `x2 := min(x0,x1)` (single positive).
- `m12_disj` — 9 rows, collider `x0 -> x2 <- x1`, `x2 := max(x0,x1)` (5 pos / 4 neg).
- `m12_fork` — 3 rows, fork `x0 -> x1`, `x0 -> x2`, deterministic children (single positive).
- `m12_chain` — 6 rows, chain `x0 -> x1 -> x2`; ancestor dose P(pos|x0)=0, 1/2, 1/2.

**Supersedes:** the previous design in which `m12_conj` / `m12_disj` were 4-variable
(isolated `x2`, target `x3`, 27-row factorial over (x0,x1,x2)) and `m12_fork` /
`m12_chain` repeated rows (9 rows each). The change removes redundant rows and the extra
variable so every fixture is a minimal, duplicate-free 3-variable table. Single-positive
`m12_conj` and `m12_fork` are intentional (the global "≥2 positives" test check was
relaxed to "both E+ and E- non-empty").

**Impact:** `causal/experiments/handcrafted_m12.py`, `causal/experiments/m12_summary.py`
(`EXPECTED` heads x3 -> x2), the M12 tests, the two arm-YAML target comments, and the
M1.2 plan/record/registers were updated to the revised design. The 2026-07-08 Stage-2
outputs under `causal/outputs/aba_learning/grid/M12_*` (and `M12_summary.{md,json}`) are
STALE — generated from the superseded design — and must be regenerated by a fresh Stage-2
rerun (`--no-resume`). No fresh Stage-2 result is claimed by this correction. This is the
sole record of the superseded fixture design; method-describing docs describe only the
revised design.

**Records:** `docs/experiments/qualitative/M1.2-config-comparison.md`;
`docs/research/milestone_plans/milestone1_part2/milestone1_part2_config_comparison.md`.

## 2026-07-08 — M1.2 BK construction backtracked: casebase default-assumption → feature-BK

**Decision:** M1.2 Stages 0–2 are re-based from the AAMAS casebase default-assumption BK to
the feature-BK construction used by the shipped ECAI tabular benchmarks. Both scoped arms
use `xi_val_v(A) :- A=id.` with learning driven by `E+`/`E-`. No default rule and no
assumption/contrary are declared in either arm's input.

**Why (superseded approach):** Stage 1 had grafted the AA-CBR casebase idiom
(`t(X) :- domain(X), alpha(X)` + `assumption(alpha(X))` + `contrary(alpha(X), c_alpha(X))`)
onto both scoped arms. That pre-derived the target for every sample via the default `alpha`, so
the only learnable content was the contrary — producing contrary-only solutions across
the scoped arm/fixture cells, with no positive `t(A) :- xi_val_v(A)` rule. Survey of the example trees
showed the casebase idiom appears only in AA-CBR examples (`examples/aacbr2.bk.aba`,
`aacbr3`, `dislike`, `loan`), not in the ECAI tabular benchmarks, which learn positive
rules from `E+`/`E-` over plain feature-BK. The same engine on the same fixture
style without the casebase graft yields positive rules under both nd and greedy folding
(`causal/outputs/aba_learning/grid/M11_parent_position{,_greedy}/`).

**Impact:** `causal/argcausaldisco_integration.py`, `causal/experiments/run_grid.py`, the
two arm YAMLs, the M12 summary side-car, and the M1.2 plan/record/registers were rewritten
to the shared feature-BK approach; the Stage-2 grid was re-run. Locked expected outputs
(positive rules) are unchanged. Method-describing docs describe only the feature-BK
approach; this entry is the sole record of the superseded casebase construction.

**Records:** `docs/experiments/qualitative/M1.2-config-comparison.md`;
`docs/research/milestone_plans/milestone1_part2/milestone1_part2_config_comparison.md`.

## 2026-07-08 — Milestone 1 re-scoped: M1.2 published-configuration comparison; M1.3 failure-mode taxonomy; no M1.4 *(Bucket 3 scope restrictions superseded 22 July)*

**Decision:** Milestone 1's goal is a report-ready account of **when and how unguided ABA
Learning recovers mechanism-aligned rules from categorical tabular data**. Two remaining
parts:

- **M1.2** — one-shot comparison of the two scoped published configurations, consulted
  verbatim: ASP-ABAlearnB (`configs/ecai2024_config.pl`) and Greedy ABA Learning
  (`configs/aamas2025_config.pl`).
  Five divergence-designed categorical fixture families (k=3; p=2), each
  with a declared graph G and pre-specified expected output: separator anchor,
  conjunctive/disjunctive mechanisms on a collider, fork (correlated-sibling confound),
  correlated-ancestor chain (2 arms × 5 = 10 cells). Primary instrument: expected vs
  learned output per cell; metrics (table-relative outcome class, body-/framework-scope
  parent recovery, ASP `pos_covered`/`neg_rejected` fractions, framework complexity,
  trace line count) are at-a-glance divergence detectors only — no metric is sufficient
  to explain a failure.
- **M1.3** — for every M1.2 divergence: mandatory trace-level mechanism (why exactly) +
  L1 (paradigm) / L2 (published variant) / L3 (implementation/encoding) attribution +
  literature mapping. M1.1's BK-ordering mechanism is the first taxonomy entry. Targeted
  falsification ablations permitted, not promised.

**Scope restrictions:** categorical data only (k=3); no binary-only fixtures; no
continuous/noise investigation in Milestone 1 (**former Part 4 dropped** — continuous data
reduces to categorical after binning; revisit after a Causal ABA integration exists). No
σ/π grids in M1.2 (M1.1 owns that account). Both arms brave, `asm_intro(relto)`, `check_ic`
kept, timeout 60 s; `ecai2024ALL` config excluded (flagged for later). No
repeat-stability measurement (deterministic for fixed inputs).

**Supersedes:** the "broader nd vs greedy strategy review on QI fixtures" framing of M1.2
(next-step lines in the 2026-06-22 closure entry below and in M1.1-era docs), the old
Part 3 "qualitative failure analysis" framing, and Part 4 entirely.

**Plans:** `milestone_plans/milestone1-plan.md`;
`milestone_plans/milestone1_part2/milestone1_part2_config_comparison.md`;
`milestone_plans/milestone1_part3/milestone1_part3_failure_modes.md`.

**Note:** ChatGPT context mirrors (`docs/chatgpt_context/`) need re-sync via
`scripts/sync_chatgpt_context.sh` before next upload.

---

## 2026-07-08 — M1.2 fixture scope refined (incoherent removed; fork added)

**Decision:** Narrow the M1.2 grid from six to **five** fixture families (10 scoped cells):

- **Remove** `m12_incoh_pos` and `m12_incoh_neg` from the M1.2 grid; incoherent inputs
  are outside M1.2.
- **Add** `m12_fork` (fork topology `x0 -> x1`, `x0 -> x2`; mechanism `x2 := x0`;
  correlated-sibling confound; extends the QI-002 fork baseline to both scoped configs).
- **Clarify naming:** `m12_conj` / `m12_disj` are conjunctive/disjunctive **mechanisms on
  a collider**, not fork vs collider topology labels.

M1.2 contains only coherent fixtures with intensional expected outputs.

**Plan:** `milestone1_part2/milestone1_part2_config_comparison.md` Section 4.

---

## 2026-07-08 — M1.2 `m12_disj` harmonized with `m12_conj` (isolated x2; target x3)

**Decision:** Revise `m12_disj` to be a **symmetric twin** of `m12_conj`: same declared G
(`x0 -> x3`, `x1 -> x3`; `x2` isolated), same 27-row complete factorial over
`(x0,x1,x2)`, same three predictors in BK; differs only in mechanism (`x3 := max(x0,x1)`
vs `min`) and expected two-rule output. Fork and chain are **not** given isolated
variables — they probe correlated sibling and ancestor confounds respectively;
isolation remains `m12_sep`'s dedicated family.

**Evidence:** Stage-0 checks updated and re-run (`causal/tests/test_m12_fixtures.py`).

**Plan/record:** `milestone1_part2_config_comparison.md` Section 4; `M1.2-config-comparison.md`.

---

## 2026-06-22 — M1.1 closed (Stages 0–7)

**Decision:** Milestone 1 Part 1 (m1.1 / M11) is **closed** for report purposes. Status **`analysed`**. All planned stages complete: metamorphic nd grid (0–2), trace mechanism (4), ablations (6), greedy comparator (7). Optional Stage 5 runner doc remains non-blocking.

**Evidence:** nd ablations ABL-100–107; Stage 7 `M11_parent_position_greedy/`; findings `milestone1_part1_m11_findings.tex`; closure summary in `M1.1-parent-position.md` §Closure decision.

**Bounded conclusion:** QI-002 disambiguation achieved. Binary parent-role + σ/π under nd. Cat3 nd: conditional parent-role; σ failure ablation-supported. Greedy: distinct cat3 outcome (supersets); rule-level σ restored; not a singleton fix.

**Next step (historical; superseded by the 2026-07-08 re-scope above):** M1.2 — broader nd vs greedy strategy review on QI fixtures (not further m1.1 grid work). Optional: Stage 5 runner call-chain doc.

**Claims:** M11-C-001–007 active; M11-C-004 resolved (Stage 7).

---

## 2026-06-22 — M1.1 analysed after ablations (ABL-100–107)

**Decision:** Close Milestone 1 Part 1 nd mechanism (Stages 0–6) as **`analysed`**. Stage 4 mechanistic account and Stage 6 ablations meet closure criteria in `milestone1_part1/milestone1_part1_ablations.md` §8. *(Superseded for final closure by Stages 0–7 entry above.)*

**Evidence:** ABL-101 pass (BK flip on cat3 A → singleton); ABL-105 pass (engine mode alone insufficient); ABL-100/103/107 audits pass. Findings: `docs/report/findings/milestone1_part1_m11_findings.tex`. Artefacts: `M11_ablations/`.

**Bounded conclusion:** Binary — full parent-role tracking with σ/π invariance. Cat3 — parent-role tracking when parent feature wins first fold; σ-invariance fails under default pipeline but is accounted for by BK serialisation + entailment + assumption commitment (M11-C-007).

**Next step (historical):** Stage 7 greedy comparator; then M1.2.

**Supersedes for closure:** 2026-06-22 reopen decision below (retained for audit trail).

**Claims:** M11-C-003, M11-C-006 ablation-supported; M11-C-007 added.

---

## 2026-06-22 — M1.1 reopened; more work needed (supervisor review) *(superseded for closure by ablation completion above)*

**Decision:** Change Milestone 1 Part 1 (m1.1 / M11) status from `analysed` to **`more work needed`**. Expand m1.1 scope to investigate **why, when, and how** π/σ equivariance/invariance hold or fail. Complete granular qualitative inspection (trace + runner levels) **before** ablation runs. **Defer** full M1.2 greedy grid until mechanistic account is clearer.

**Evidence / trigger:** Fabrizio M1.1 review (June 2026). Stage 3 first-fold correlation is insufficient as a mechanistic explanation. Greedy smoke test on m1.1 differed materially from both nd cat3 A and B.

**Next step:** Stage 4 — line-by-line `prolog.stdout` audit (cat3 A vs B minimum); runner/bridge inspection; then hypothesis and ablations.

**Supersedes:** 2026-06-18 close-out decision below (retained for audit trail).

**Claims:** M11-C-001, M11-C-002, M11-C-005 active (first-run verdicts); M11-C-003 provisional only; M11-C-004 weakened.

---

## 2026-06-18 — M1.1 analysed; proceed to M1.2 *(superseded 2026-06-22)*

**Decision:** Close Milestone 1 Part 1 (m1.1 / M11) as `analysed`. Do not extend m1.1 with additional cells, seeds, or greedy runs without a new experiment ID.

**Evidence:** Eight-cell nd grid; transformation-square verdicts; Stage 3 prolog trace on cat3 σ-pair. See `docs/experiments/qualitative/M1.1-parent-position.md` and `docs/report/findings/milestone1_part1_m11_findings.tex`.

**Bounded conclusion:** Direct-parent tracking with σ-invariance holds for binary under fixed nd; cat3 does not (encoding-dependent representation-order sensitivity).

**Next step (was):** Milestone 1 Part 2 (M1.2) — rerun the m1.1 grid under `folding_mode: greedy` and compare to the M11 nd baseline.

**Superseded by:** 2026-06-22 supervisor review — mechanistic investigation required before M1.2.
