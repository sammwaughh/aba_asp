# Research log

Chronological notes on experiment progress, decisions, and milestones. Detailed evidence remains in experiment records and artefact paths cited below.

## 2026-06-18 — M1.1 (M11) close-out

- **Experiment:** M11_parent_position (Milestone 1 Part 1).
- **Status:** `analysed` (Stages 0–3 complete).
- **Outcome (bounded):** 8/8 solved under nd. Binary: exact expected rules; σ and π hold. Cat3: B/C exact; A/D assumption structures; σ fails on both tested pairs; π holds B↔C only. Stage 3: BK order → first nd-fold literal → entailment fork (cat3 A vs B; analogously D vs C).
- **Records:** `docs/experiments/qualitative/M1.1-parent-position.md`; `docs/report/findings/milestone1_part1_m11_findings.tex`; claims M11-C-001–004 in `docs/report/claims_ledger.md`.
- **Artefacts:** `causal/outputs/aba_learning/grid/M11_parent_position/cells/<dgp>/`; Stage-0 `causal/outputs/m11_parent_position/validation/`.
- **Next:** Milestone 1 Part 2 (M1.2) — greedy vs nd on the same eight-cell grid; planning doc to be written by Samuel (`milestone1_part2_greedy_vs_nondeterministic.md`).

## 2026-06-18 — Documentation tidy (M1.1 → M1.2 handoff)

- Updated navigation docs (`experiments_summary`, `research_state`, `report_state`, registers) to reflect M1.1 complete and M1.2 next.
- Removed obsolete QN-001 experiment plan and all references (superseded by Milestone 1 Part 2 framing).
- Synced ChatGPT context mirrors via `scripts/sync_chatgpt_context.sh`.
