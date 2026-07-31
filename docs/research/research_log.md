# Research log

Chronological notes on experiment progress, decisions, and milestones. Detailed evidence remains in experiment records and artefact paths cited below.

## 2026-07-31 — Fabrizio review; deterministic-mechanism Bucket 3 focus

- **Supervisor direction:** use non-degenerate stochastic root distributions with
  deterministic non-root mechanisms; establish the corresponding mechanism rules before
  running ABALearn; then describe what is learned and why across enough bounded cases to
  support a systematic account.
- **Scientific guardrail:** exact fixture-specific faithfulness and support checks remain
  required. Determinism does not itself establish faithfulness or causal orientation.
- **Preserved:** the positive-stochastic diamond and its AAMAS/ECAI target-wise outputs
  remain pre-pivot exploratory/infrastructure artefacts, not Bucket 3 claim evidence.
- **Deferred:** the remaining 22 July dimensions, including missingness and broader data
  types, remain possible later Bucket 3 work.
- **Approved infrastructure:** backwards-compatible deterministic fixture validation,
  root-only sampling, structural-support certification, and evaluator-only mechanism
  references. No deterministic research fixture or run is approved yet.
- **Implemented and verified:** schema-version-2 fixture support and the generic
  evaluator reference were added without changing the inherited learner or generated
  evidence. The expanded focused fixture/target-wise suite passed (`93 passed`), and both
  preserved stochastic-diamond target-wise configurations validated successfully.
- **Compatibility guard:** the existing schema-version-1 scientific semantic hash is
  pinned by test, and the upgraded builder refuses legacy output bundles before writing;
  preserved generated artefacts were not changed.
- **Naming adaptation:** future target-wise fixtures may use lowercase identifiers
  `a`, `b`, `c`, ... while existing `xN` fixtures remain supported. Fixture-aware
  diagnostics exclude `alpha_N`/`c_alpha_N` from causal body variables. Both AAMAS and
  ECAI completed a lowercase-predicate smoke test through the unchanged Prolog engine.
- **Guidance and decision:** `docs/research/supervisor_guidance.md` (31 July section) and
  `docs/research/decisions.md` (31 July entry).

## 2026-07-22 — Fabrizio scope review; M1.3 Bucket 3 pivot

- **Supervisor outcome:** existing M12x and M1.3 analysis accepted as a useful
  foundation; broader causal-discovery capability/limitation investigation required.
- **Closed:** Bucket 2 locked with Claims 1–2 (M13-C1/C2). Proposed Claim 3 parked.
- **Preserved:** M12x and Buckets 1–2 will not be redone.
- **New scope dimensions (planning pending):** varying targets; partial/missing
  tabular information; larger controlled graphs; explicit correlation,
  marginal/conditional independence, and Markov equivalence; graph–mechanism
  consistency; attribution of learning-strategy versus information/data limitations;
  possible additional categories or non-discrete data.
- **Status:** Milestone 1 / M1.3 continues for the coming week; Bucket 3 opened
  structurally but has no approved claims or experiment matrix yet. Milestone 2 not
  started.
- **Immediate next:** update/synchronise the ChatGPT context, then begin collaborative
  planning from the supervisor-defined scope.
- **Guidance:** `docs/research/supervisor_guidance.md` (22 July 2026).

## 2026-07-21 — M1.3 Bucket 2 Claims 1–2 analysed and written

- **M13-C1:** 4/4 cells `solved`; input-equivalent graph pair confirmed identical
  learner inputs/delta/coverage with different graph-relative verdicts.
- **M13-C2:** 20/20 cells `solved`; ECAI delta changed under every tested U2/U5/U7
  feature order, while AAMAS delta and coverage were invariant within each family.
- **Key C2 controls:** U5 parent-first order restored exact ECAI parent recovery; U7
  rejected \(0/3\) negatives exactly when required parent \(x_2\) was third and
  \(3/3\) otherwise.
- **Records:** `M13-C1-causal-role-underdetermination/experiment.md`;
  `M13-C2-bk-feature-order/experiment.md`; `M1.3-bucket2-claims.md`.
- **Next:** Bucket 2 Claim 3.

## 2026-07-21 — M1.3 Bucket 1 locked; Bucket 2 commencing

- **Decision:** Bucket 1 (four claims + TeX mirror) is **written / locked**.
- **Next:** commence Bucket 2 claim drafting (probes/controls as needed).
- **Records:** `M1.3-bucket1-claims.md` (locked);
  `M1.3-bucket2-claims.md` + `milestone1_part3_bucket2_claims.tex` (stubs);
  path: `milestone1_high_level_path.md`.

## 2026-07-20 — M12x closed; M1.3 claim drafting commencing

- **Decision:** M12x Stage-3 (18/18) is **closed** as the locked evidence base.
- **Next:** commence M1.3 claim drafting (live claim list 3–10 from Stage-3 patterns;
  then investigation order; then one claim at a time).
- **Do not** reuse withdrawn prior M1.3 claim drafts.
- **Records:** `M1.2-expanded.md` (closed); Bucket 1 stubs:
  `M1.3-bucket1-claims.md` + `milestone1_part3_bucket1_claims.tex`;
  path: `milestone1_high_level_path.md`.

## 2026-07-20 — Fresh M12x 18-cell run + summary (no Stage-3 yet)

- **Commands:** `run_grid` on `M12x_{ecai2024,aamas2025}.yaml` (`--no-resume`); then
  `python -m causal.experiments.m12x_summary`.
- **Result:** ECAI 9/9 `solved`; AAMAS 9/9 `solved`; 18 cell reports written.
- **Artefacts:** `M12x_{ecai2024,aamas2025}/`; `M12x_summary.md`/`.json`;
  `M12x_cell_reports/`.
- **Next:** Stage-3 qualitative inspection (no interpretation recorded in this entry).

## 2026-07-20 — Delete prior M12x outputs; reset to awaiting fresh run

- **Deleted:** `M12x_{ecai2024,aamas2025}/`, `M12x_summary.md`/`.json`,
  `M12x_learned_rules.md`, `M12x_cell_reports/`, and
  `M1.2-expanded-cell-inspection.md`.
- **Kept:** pilot `M12_*` artefacts; locked design (fixtures, YAMLs, cards, catalogue).
- **Status:** M12x → **`implemented`** (18-cell design locked; no live runner evidence).
- **Next:** `--no-resume` both arms → `m12x_summary` → Stage-3 → M1.3.

## 2026-07-20 — Withdraw M1.3 claim drafting; redesign M12x

- **Decision:** Delete provisional M1.3 claim analysis (claim list + claim working doc).
  U4/U5 double-copy and U6/U7 double min/max are uninformative; first M12x grid is
  historical only.
- **Kept:** `milestone1_part3_approach.md` (method only; status paused).
- **Current work:** redesign M12x mechanisms (fork first), then re-run and re-inspect.
- **Do not** draft M1.3 claims until redesigned M12x is locked.

## 2026-07-16 — M1.2 closed; documentation updated for M1.3

- **Decision:** M12x evidence package complete; Part 2 closed; **M1.3 starts**.
- **Updated:** `milestone1_high_level_path.md`; `milestone1-plan.md`;
  `milestone1_part2_expanded_approach.md` (design complete); `milestone1_part3/`;
  `experiments_summary.md`; `experiment_register.md` (M13 in progress);
  `research_state.md`; `report_state.md`; `AGENTS.md`; `PROJECT_README.md`;
  chatgpt_context governance / orientation mirrors.
- **Record opened:** `docs/experiments/qualitative/M1.3-failure-modes.md`
  (seed patterns listed; claims/probes still TBD).
- **Superseded 2026-07-20:** M1.3 claim drafting withdrawn; M12x redesign required.

## 2026-07-16 — M12x Stage-3 cell inspection (22 cells)

- **Doc:** `docs/experiments/qualitative/M1.2-expanded-cell-inspection.md`
  (historical first-grid write-up; stub later deleted with all prior M12x outputs
  on 2026-07-20).
- **Vocabulary:** Approach (`config`, \(\mathcal{H}_t^\star\), `val`, ancestors /
  distractors / descendant failure mode).
- **Headline (first grid, historical):** no exact \(\mathcal{H}^\star\) matches on that
  22-cell package; AAMAS cited descendants on several cells; ECAI often
  assumption-mediated.
- **Status:** voided — not evidence for the locked design.

## 2026-07-16 — M12x summary matrix + 22 cell reports

- **Command:** `python -m causal.experiments.m12x_summary`
- **Outputs:** `M12x_summary.md` / `.json`; `M12x_cell_reports/` (then 22 cells; now 20).
- **Detectors (first grid, historical):** no exact \(\mathcal{H}^\star\) matches; several
  descendant citations under AAMAS.
- **Next:** Stage-3 plain-English inspection write-up → M1.3.

## 2026-07-16 — M12x learning run: 22/22 solved

- **Commands:** `run_grid` on `M12x_ecai2024.yaml` and `M12x_aamas2025.yaml` (`--no-resume`).
- **Result:** ECAI 11/11 solved; AAMAS 11/11 solved; no timeouts/errors.
- **Artefacts:** `causal/outputs/aba_learning/grid/M12x_{ecai2024,aamas2025}/`;
  `M12x_learned_rules.md`.
- **Record:** `docs/experiments/qualitative/M1.2-expanded.md` status `run`.
- **Note:** `solved` ≠ \(\mathcal{H}^\star\) match. AAMAS deltas often cite
  descendants/siblings (failure modes to inspect). Next: cell inspection → M1.3.

## 2026-07-16 — Optional grid.seed; M12x slugs without __seed-

- **Change:** `grid.seed` optional; omit for M12x; slug = `{dgp}__target-{t}`.
- **Docs:** INFRA.md §3.2; decisions.md.

## 2026-07-16 — Expanded M1.2 (M12x) fixtures + 22-cell grid constructed

- **Fixtures:** `causal/experiments/handcrafted_m12x.py` (U1–U7; nonzero labels).
- **BK:** exact-value (`val`) predicates in `generate_aba_background_knowledge`
  (descendants stay in BK).
- **Configs:** `M12x_ecai2024.yaml`, `M12x_aamas2025.yaml` (`cell_dir: slug`; no `grid.seed`; 11 cells each).
- **Record:** `docs/experiments/qualitative/M1.2-expanded.md`.
- **Verified:** pytest (M12+M12x); dry-run 11+11 cells.
- **Next:** run both arms, then inspect.

## 2026-07-16 — Expanded M1.2 mechanism cards U1–U7 written

- **Folder:** `docs/research/milestone_plans/milestone1_part2/mechanism_cards/`
- **Contents:** README + one card per unit (full \(\mathcal{D}\), per-target BK including
  descendant distractors, \(E^\pm\), \(\mathcal{H}_t^\star\), semantic success).
- **Next:** implement fixtures/BK from cards → run 22-cell grid → inspect.

## 2026-07-16 — Expanded M1.2: descendants stay in BK (correction)

- **Correction:** When learning target \(t\), BK includes **all other columns**,
  including descendants. They are distractors; citing them in a learned rule is the
  failure mode under test. Only \(t\) itself is excluded from BK.
- **Was wrong:** wording that treated descendants as excluded from BK.
- **Docs:** Approach Predictors section; unit-set card checklist; part2 README;
  config-comparison header; `decisions.md`.

## 2026-07-16 — Expanded M1.2 Approach written

- **Doc:** `docs/research/milestone_plans/milestone1_part2/milestone1_part2_expanded_approach.md`
- **Status:** Approach locked (DGP/BK/labels/configs/predictor policy); still in
  “Lock the expanded M1.2 design”. Next: select graphs and write mechanism cards.
- **Pointers updated:** high-level path, part2 README, milestone1-plan, AGENTS.md,
  decisions.md, registers/summaries as needed.

## 2026-07-16 — Milestone 1 high-level path: expand M1.2, then M1.3; no M1.4

- **Decision:** see `decisions.md` (2026-07-16). Primary working reference:
  `docs/research/milestone_plans/milestone1_high_level_path.md`.
- **Done:** M1.1 closed; M1.2 pilot (10 cells) analysed.
- **Next:** lock expanded M1.2 design (Fabrizio small DAGs; DGP choice; intended rules;
  ECAI+AAMAS), then evidence collection; then M1.3 claims + probes.
- **Out of Milestone 1:** large-graph / bnlearn evaluation (later evaluation milestone).
  No M1.4.
- **Docs updated:** milestone1-plan.md, part2/part3 READMEs and detail plans,
  AGENTS.md, experiments_summary.md, experiment_register.md, report_state,
  chatgpt_project_brief, PROJECT_README.

## 2026-07-13 — M1.2 scope corrected to two arms

- **Decision:** M1.2 now contains only ECAI (`M12_ecai2024`) and AAMAS
  (`M12_aamas2025`) across the five locked fixtures: 10 scoped cells.
- **Retained results:** 10/10 solved; exact match 2/10 (ECAI/fork, AAMAS/conj); ASP
  sample coverage 10/10.
- **Documentation:** primary record, cell inspection, plans, registers, summaries,
  handoffs, and ChatGPT context mirrors re-scoped. Inherited paper artefacts remain on
  disk and were not modified.

## 2026-07-08 — Milestone 1 re-scoped (M1.2 config comparison; M1.3 failure modes; Part 4 dropped)

- **Decision:** see `decisions.md` (2026-07-08). Milestone 1 goal restated as a report-ready
  account of when/how unguided ABA Learning recovers mechanism-aligned rules from categorical
  data. M1.2 = two-config comparison (ASP-ABAlearnB / Greedy ABA Learning, configs
  consulted verbatim) on five divergence-designed categorical fixture families. M1.3 =
  failure-mode taxonomy (trace mechanism + L1/L2/L3 attribution +
  literature mapping). Former Part 4 (noise/continuous) dropped from Milestone 1.
- **Plans rewritten:** `milestone1-plan.md`; new
  `milestone1_part2/milestone1_part2_config_comparison.md` and
  `milestone1_part3/milestone1_part3_failure_modes.md`; Part 4 folder and old Part 2/3 stubs
  deleted; forward pointers updated across AGENTS.md, PROJECT_README.md, research_state.md,
  experiments_summary.md, experiment_register.md, supervisor_guidance.md, report_state.md,
  chatgpt_project_brief.md, QL_interim_handoff.md, M1.1 record, and the m1.1 findings tex.
- **Historical next at that date:** implement M1.2 Stage 0 (fixtures + validation) and
  Stage 1 (config-consulting runner, adapted metrics). These stages are now complete.

## 2026-06-22 — M1.1 (M11) closed (Stages 0–7)

- **Experiment:** M11_parent_position + M11_parent_position_greedy (Stage 7).
- **Status:** `analysed` / **closed** for report purposes.
- **Outcome (bounded):** QI-002 disambiguation complete. nd: binary σ/π pass; cat3 σ fails (ablation-supported BK→entailment→assumptions). Greedy: binary matches nd; cat3 uniform parent supersets; rule-level σ restored under greedy.
- **Records:** `M1.1-parent-position.md` §Closure decision; `milestone1_part1_m11_findings.tex`; claims M11-C-001–007; `decisions.md` (2026-06-22 Stages 0–7 entry).
- **Artefacts:** `M11_parent_position/cells/`; `M11_ablations/`; `M11_parent_position_greedy/` + `summary/compare_nd_greedy.md`.
- **Historical next (superseded):** broader nd vs greedy strategy review on QI fixtures.
  M1.2 was later re-scoped and completed as the two-config comparison. Optional: m1.1
  Stage 5 runner doc.

## 2026-06-22 — M1.1 ablations + nd mechanism closure (Stages 4–6)

- ABL-100–107 executed (ABL-106 skipped). ABL-101 BK flip confirms causal BK-order account.
- Status moved from `more work needed` → `analysed` (nd mechanism). See `decisions.md`.

## 2026-06-18 — M1.1 (M11) initial grid (Stages 0–3)

- **Outcome (historical):** 8/8 solved under nd. Binary pass; cat3 σ fails. Stage 3 provisional — superseded by Stages 4–7.
- **Records:** `M1.1-parent-position.md`; interim findings tex (later rewritten).

## 2026-06-18 — Documentation tidy (M1.1 → M1.2 handoff)

- Updated navigation docs for milestone progression.
- Synced ChatGPT context mirrors via `scripts/sync_chatgpt_context.sh` (re-sync recommended after m1.1 closure).
