# Research log

Chronological notes on experiment progress, decisions, and milestones. Detailed evidence remains in experiment records and artefact paths cited below.

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
- **Vocabulary:** Approach (`config`, \(\mathcal{H}_t^\star\), `nz`/`val`, ancestors /
  distractors / descendant failure mode).
- **Headline:** 0/22 exact compact-`nz` \(\mathcal{H}^\star\); AAMAS cites descendants
  on U5-x1, U6-x2, U7-x2; ECAI often assumption-mediated or inferior `val`-expansions.
- **Status:** expanded M1.2 `analysed`. Next: M1.3 claims + probes.

## 2026-07-16 — M12x summary matrix + 22 cell reports

- **Command:** `python -m causal.experiments.m12x_summary`
- **Outputs:** `M12x_summary.md` / `.json`; `M12x_cell_reports/` (22 cells).
- **Detectors:** 0/22 exact compact-nz H*; ECAI 3 val-expansions; AAMAS 3 descendant
  citations (U5-x1, U6-x2, U7-x2).
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
- **BK:** `definitional_nz` gated in `generate_aba_background_knowledge` (descendants stay in BK).
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
