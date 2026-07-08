# Research decisions

Recorded decisions that affect experiment direction. Evidence and interpretation remain in experiment records.

## 2026-07-08 — M1.2 BK construction backtracked: casebase default-assumption → feature-BK

**Decision:** M1.2 Stages 0–2 are re-based from the AAMAS casebase default-assumption BK to
the construction the shipped benchmarks actually use. All three arms now use feature-BK
(`xi_val_v(A) :- A=id.`) with learning driven by `E+`/`E-`, matching
`ecai2024/ASP-ABAlearn_B/*.csv.bk.aba`. The RuleML arm additionally emits the `domain/1`
element (`domain(default).` + `domain(1..N).`) that ships with `ruleml2025/*.scratch.aba`
for construction fidelity; that `domain(default)` element supports RASP-ABAlearn's
incremental redress workflow, which M1.2 does **not** run (one-shot only). No default rule
and no assumption/contrary are declared on any arm.

**Why (superseded approach):** Stage 1 had grafted the AA-CBR casebase idiom
(`t(X) :- domain(X), alpha(X)` + `assumption(alpha(X))` + `contrary(alpha(X), c_alpha(X))`)
onto every arm. That pre-derived the target for every sample via the default `alpha`, so
the only learnable content was the contrary — producing contrary-only solutions in all 15
Stage-2 cells, with no positive `t(A) :- xi_val_v(A)` rule. Survey of the example trees
showed the casebase idiom appears only in AA-CBR examples (`examples/aacbr2.bk.aba`,
`aacbr3`, `dislike`, `loan`), never in the ECAI or RuleML tabular benchmarks, which learn
positive rules from `E+`/`E-` over plain feature-BK. The same engine on the same fixture
style without the casebase graft yields positive rules under both nd and greedy folding
(`causal/outputs/aba_learning/grid/M11_parent_position{,_greedy}/`).

**Impact:** `causal/argcausaldisco_integration.py` (`default_assumption_target` →
`domain_predicate`), `causal/experiments/run_grid.py` threading, the three arm YAMLs, the
M12 summary side-car, and the M1.2 plan/record/registers were rewritten to the feature-BK
approach; the Stage-2 grid was re-run. Locked expected outputs (positive rules) are
unchanged. Method-describing docs describe only the feature-BK approach; this entry is the
sole record of the superseded casebase construction.

**Records:** `docs/experiments/qualitative/M1.2-config-comparison.md`;
`docs/research/milestone_plans/milestone1_part2/milestone1_part2_config_comparison.md`.

## 2026-07-08 — Milestone 1 re-scoped: M1.2 published-configuration comparison; M1.3 failure-mode taxonomy; no M1.4

**Decision:** Milestone 1's goal is a report-ready account of **when and how unguided ABA
Learning recovers mechanism-aligned rules from categorical tabular data**. Two remaining
parts:

- **M1.2** — one-shot comparison of the three published configurations, consulted verbatim:
  ASP-ABAlearnB (`configs/ecai2024_config.pl`), RASP-ABAlearn
  (`ruleml2025/ruleml2025_config.pl`; incremental-redress workflow **not** exercised,
  flagged as near-term follow-up), Greedy ABA Learning (`configs/aamas2025_config.pl`).
  Five divergence-designed categorical fixture families (k=3; p fixture-dependent), each
  with a declared graph G and pre-specified expected output: separator anchor,
  conjunctive/disjunctive mechanisms on a collider, fork (correlated-sibling confound),
  correlated-ancestor chain (3 arms × 5 = 15 cells). Minimally incoherent tables
  (`m12_incoh_pos` / `m12_incoh_neg`; entailment-gate probe) deferred to a follow-up
  experiment. Primary instrument: expected vs learned output per cell; metrics (table-relative
  outcome class, body-/framework-scope parent recovery, `covers_all_pos`/`rejects_all_neg`
  flags, framework complexity, trace line count) are at-a-glance divergence detectors only
  — no metric is sufficient to explain a failure.
- **M1.3** — for every M1.2 divergence: mandatory trace-level mechanism (why exactly) +
  L1 (paradigm) / L2 (published variant) / L3 (implementation/encoding) attribution +
  literature mapping. M1.1's BK-ordering mechanism is the first taxonomy entry. Targeted
  falsification ablations permitted, not promised.

**Scope restrictions:** categorical data only (k=3); no binary-only fixtures; no
continuous/noise investigation in Milestone 1 (**former Part 4 dropped** — continuous data
reduces to categorical after binning; revisit after a Causal ABA integration exists). No
σ/π grids in M1.2 (M1.1 owns that account). All arms brave, `asm_intro(relto)`, `check_ic`
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

## 2026-07-08 — M1.2 fixture scope refined (incoherent deferred; fork added)

**Decision:** Narrow the M1.2 grid from six to **five** fixture families (15 cells):

- **Remove** `m12_incoh_pos` and `m12_incoh_neg` from the M1.2 grid; defer as a
  follow-up experiment probing RuleML vs AAMAS on brave defeasible structure /
  post-folding entailment gate.
- **Add** `m12_fork` (fork topology `x0 -> x1`, `x0 -> x2`; mechanism `x2 := x0`;
  correlated-sibling confound; extends QI-002 fork baseline to three published configs).
- **Clarify naming:** `m12_conj` / `m12_disj` are conjunctive/disjunctive **mechanisms on
  a collider**, not fork vs collider topology labels.

M1.2 no longer exercises the main predicted RuleML-vs-AAMAS divergence from the original
plan. RASP redress workflow remains deferred (Section 4.1 of the M1.2 plan).

**Plan:** `milestone1_part2/milestone1_part2_config_comparison.md` Section 4 and 4.1.

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
