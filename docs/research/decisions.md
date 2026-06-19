# Research decisions

Recorded decisions that affect experiment direction. Evidence and interpretation remain in experiment records.

## 2026-06-18 — M1.1 analysed; proceed to M1.2

**Decision:** Close Milestone 1 Part 1 (m1.1 / M11) as `analysed`. Do not extend m1.1 with additional cells, seeds, or greedy runs without a new experiment ID.

**Evidence:** Eight-cell nd grid; transformation-square verdicts; Stage 3 prolog trace on cat3 σ-pair. See `docs/experiments/qualitative/M1.1-parent-position.md` and `docs/report/findings/milestone1_part1_m11_findings.tex`.

**Bounded conclusion:** Direct-parent tracking with σ-invariance holds for binary under fixed nd; cat3 does not (encoding-dependent representation-order sensitivity).

**Next step:** Milestone 1 Part 2 (M1.2) — rerun the m1.1 grid under `folding_mode: greedy` and compare to the M11 nd baseline. Samuel to write `docs/research/milestone_plans/milestone1_part2_greedy_vs_nondeterministic.md`.

**Claims:** M11-C-001–003 active; M11-C-004 (greedy may help cat3 σ) remains tentative until M1.2 runs.

## 2026-06-18 — Retire QN-001 experiment plan

**Decision:** Remove the QN-001 experiment ID and planning record. Strategy comparison on controlled fixtures is covered by Milestone 1 Part 2 (M1.2) and the existing qualitative greedy reruns (QI-* greedy), not a separate quantitative grid experiment.

**Rationale:** QN-001 duplicated M1.2 intent and caused navigation confusion between “next experiment” entries.
