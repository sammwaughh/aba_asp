# Research decisions

Recorded decisions that affect experiment direction. Evidence and interpretation remain in experiment records.

## 2026-07-20 — Withdraw M1.3 claims; redesign M12x U4–U7

**Decision:** Provisional M1.3 claim drafting from the first M12x grid is **withdrawn**
and deleted (claim list + claim working doc). Double-copy fork/chain (U4/U5) and
double min/max cones (U6/U7) are uninformative. Priority returns to **getting M12x
right** (mechanisms → cards/catalogue → fixtures → re-run → Stage-3). M1.3 Approach
method is retained but paused.

**Fork intent (U4, agreed in discussion):**  
\(x_2 := 2\) iff \(x_0\neq 0\) (nz \(\mathcal{H}^\star\));  
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
`m12_*` left unchanged). Nonzero labels; definitional `*_nz` BK via
`defaults.definitional_nz`; multi-target cells with `grid.cell_dir: slug`;
**no** `grid.seed`.

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
- BK: exact `val` predicates + definitional `nz` rules (facts, not assumptions/contraries).
- Configs: ECAI and AAMAS only.
- Cells: (fixture, non-source target, config); BK includes **all non-target columns**
  (ancestors, siblings, **and descendants**). Only the target is excluded from BK.
  Descendant (and sibling) *citation in a learned rule* is a failure/divergence to
  inspect — distractors are left in BK so the learner can be tested on ignoring them.
- Good intensional rules should use ancestors of the target only.
- Reference \(\mathcal{H}_t^\star\) in compact `nz` form; no precisely pre-enumerated
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

## 2026-07-08 — Milestone 1 re-scoped: M1.2 published-configuration comparison; M1.3 failure-mode taxonomy; no M1.4

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
