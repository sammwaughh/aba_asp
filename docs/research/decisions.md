# Research decisions

Recorded decisions that affect experiment direction. Evidence and interpretation remain in experiment records.

## 2026-06-22 — M1.1 reopened; more work needed (supervisor review)

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
