# Research decisions

Recorded decisions that affect experiment direction. Evidence and interpretation remain in experiment records.

## 2026-06-22 — M1.1 closed (Stages 0–7)

**Decision:** Milestone 1 Part 1 (m1.1 / M11) is **closed** for report purposes. Status **`analysed`**. All planned stages complete: metamorphic nd grid (0–2), trace mechanism (4), ablations (6), greedy comparator (7). Optional Stage 5 runner doc remains non-blocking.

**Evidence:** nd ablations ABL-100–107; Stage 7 `M11_parent_position_greedy/`; findings `milestone1_part1_m11_findings.tex`; closure summary in `M1.1-parent-position.md` §Closure decision.

**Bounded conclusion:** QI-002 disambiguation achieved. Binary parent-role + σ/π under nd. Cat3 nd: conditional parent-role; σ failure ablation-supported. Greedy: distinct cat3 outcome (supersets); rule-level σ restored; not a singleton fix.

**Next step:** M1.2 — broader nd vs greedy strategy review on QI fixtures (not further m1.1 grid work). Optional: Stage 5 runner call-chain doc.

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
