# Research log

Chronological notes on experiment progress, decisions, and milestones. Detailed evidence remains in experiment records and artefact paths cited below.

## 2026-06-22 — M1.1 (M11) closed (Stages 0–7)

- **Experiment:** M11_parent_position + M11_parent_position_greedy (Stage 7).
- **Status:** `analysed` / **closed** for report purposes.
- **Outcome (bounded):** QI-002 disambiguation complete. nd: binary σ/π pass; cat3 σ fails (ablation-supported BK→entailment→assumptions). Greedy: binary matches nd; cat3 uniform parent supersets; rule-level σ restored under greedy.
- **Records:** `M1.1-parent-position.md` §Closure decision; `milestone1_part1_m11_findings.tex`; claims M11-C-001–007; `decisions.md` (2026-06-22 Stages 0–7 entry).
- **Artefacts:** `M11_parent_position/cells/`; `M11_ablations/`; `M11_parent_position_greedy/` + `summary/compare_nd_greedy.md`.
- **Next:** M1.2 — broader nd vs greedy strategy review on QI fixtures. Optional: m1.1 Stage 5 runner doc.

## 2026-06-22 — M1.1 ablations + nd mechanism closure (Stages 4–6)

- ABL-100–107 executed (ABL-106 skipped). ABL-101 BK flip confirms causal BK-order account.
- Status moved from `more work needed` → `analysed` (nd mechanism). See `decisions.md`.

## 2026-06-18 — M1.1 (M11) initial grid (Stages 0–3)

- **Outcome (historical):** 8/8 solved under nd. Binary pass; cat3 σ fails. Stage 3 provisional — superseded by Stages 4–7.
- **Records:** `M1.1-parent-position.md`; interim findings tex (later rewritten).

## 2026-06-18 — Documentation tidy (M1.1 → M1.2 handoff)

- Updated navigation docs for milestone progression.
- Synced ChatGPT context mirrors via `scripts/sync_chatgpt_context.sh` (re-sync recommended after m1.1 closure).
