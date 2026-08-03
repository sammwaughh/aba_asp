# Milestone 1 Plan

**Primary working path:** [`milestone1_high_level_path.md`](milestone1_high_level_path.md)  
**Expanded M1.2 Approach:** [`milestone1_part2/milestone1_part2_expanded_approach.md`](milestone1_part2/milestone1_part2_expanded_approach.md)  

Use the high-level path for order of work, and the Approach while locking graphs/mechanisms. This file is the milestone index and part summaries.

## Purpose

Milestone 1 produces a **report-ready account of what causal structure unguided ABA
Learning can recover from controlled tabular data, under which targets,
data-availability conditions, graph/mechanism structures, and learning strategies —
and which limitations are informational rather than strategic**. "Unguided" means the
inherited ABALearn engine as published, with no Causal ABA integrations (those are
Milestone 2 and beyond).

The completed M1.1/M1.2 and M1.3 Buckets 1–2 answer this first for selected targets in
small categorical fixtures. Fabrizio's 22 July review expanded M1.3; his 31 July review
set the immediate method as one root-stochastic, deterministic-non-root binary mechanism
case at a time, with expected mechanism rules fixed before ABALearn. The other expanded
dimensions remain possible later work.

Framing rules for the whole milestone:

- The primary comparison is always **intended learned output vs actual learned output**,
  per (configuration, fixture) cell, with intended outputs pre-specified from \(G\) and the
  mechanism before any run.
- **ASP coverage** (E⁺ covered / E⁻ rejected) is recorded separately and must not be
  conflated with intended-rule match.
- Quantitative metrics are **at-a-glance detectors only**. The instrument is qualitative
  inspection of `bk.sol.aba` and `prolog.stdout` — what happens, why, and which patterns
  recur across graphs.
- This remains an investigation of the current target-wise ABA Learning bridge, not an
  implementation of Russo-style Causal ABA or a claim of full causal discovery.
- Claims must separate failures of a specified learning strategy from cases where the
  available observations do not identify the causal structure.

### Current scope and guardrails

- M12x and Buckets 1–2 remain locked; the new work is Bucket 3 within M1.3.
- Categorical \(K=3\) remains the completed baseline. Additional category counts and
  non-discrete data are possible Bucket 3 dimensions, not yet committed experiments.
- Larger **controlled** DAGs are in scope. Random graphs and bnlearn-scale evaluation
  remain outside the immediate Bucket 3 planning.
- ECAI and AAMAS are the completed comparison arms. Any Bucket 3 strategy set must be
  decided during planning.
- Future fixtures must document graph–mechanism validity, support, expected outputs,
  and relevant marginal/conditional-independence and Markov-equivalence properties.
- The immediate fixture regime uses mutually independent non-degenerate stochastic roots
  and deterministic non-root functions. Each fixture needs a full truth table, exact
  support/faithfulness certificate, and evaluator-only canonical rule reference before a
  sample or learning run is selected.
- New target-wise fixtures use lowercase internal identifiers `a`, `b`, `c`, ... and
  corresponding mathematical labels (A,B,C,\ldots); existing `xN` evidence is preserved.
- There is **no M1.4**; this supervisor-driven expansion remains M1.3.

## Working Method

For each part:

1. Write or update a bespoke planning document defining goal, graphs/mechanisms, DGP(s),
   intended learned rules, and the smallest experiment that answers the question.
2. Use Cursor to implement and run the agreed experiment.
3. Compare actual learned rules with pre-specified intentions; inspect raw artefacts.
4. Draw bounded, evidence-supported conclusions. Prefer plain-English pattern descriptions
   over invented taxonomies.
5. Write a concise `.tex` findings document when the evidence for that part is ready.

## Part 1: Parent-Position and Representation-Order Control — **closed**

Planning documents: [`milestone1_part1/`](milestone1_part1/README.md)

Experiment record: `docs/experiments/qualitative/M1.1-parent-position.md`  
Findings: `docs/report/findings/milestone1_part1_m11_findings.tex`

**Carry-forward:** BK/representation ordering is a confirmed limit on mechanism-aligned
recovery under nd, with a complete trace-level account. It remains available as an M1.3
claim with evidence; σ/π grids are not repeated in M1.2.

## Part 2: Published-Configuration Comparison (M1.2) — **closed / analysed**

Planning folder: [`milestone1_part2/`](milestone1_part2/README.md)  
**Approach:** [`milestone1_part2/milestone1_part2_expanded_approach.md`](milestone1_part2/milestone1_part2_expanded_approach.md)  
**Expanded record:** `docs/experiments/qualitative/M1.2-expanded.md`  
**Stage-3 inspection:** `docs/experiments/qualitative/M1.2-expanded-cell-inspection.md` (18/18)  
Pilot (historical): [`milestone1_part2/milestone1_part2_config_comparison.md`](milestone1_part2/milestone1_part2_config_comparison.md)

| Phase | Status | Content |
|-------|--------|---------|
| Pilot grid | Analysed (historical) | 10 cells; not the primary expanded evidence |
| Expanded design | Locked | U1–U7; 18 cells; nonzero-positive; `val`-only BK; ECAI+AAMAS |
| Expanded runs + inspection | **Done / closed** | Fresh 18/18 `solved` + Stage-3 18/18 (2026-07-20); evidence locked for M1.3 |

Configs: ECAI (`configs/ecai2024_config.pl`), AAMAS (`configs/aamas2025_config.pl`).

## Part 3: Causal-recovery capabilities and limits (M1.3) — **in progress** (Buckets 1–2 locked; Bucket 3 H0–H5 complete, including H4b)

Planning folder: [`milestone1_part3/`](milestone1_part3/README.md)  
Approach (method): [`milestone1_part3/milestone1_part3_approach.md`](milestone1_part3/milestone1_part3_approach.md)  
Detail plan: [`milestone1_part3/milestone1_part3_failure_modes.md`](milestone1_part3/milestone1_part3_failure_modes.md)  
Bucket 1 (**locked**): `docs/experiments/qualitative/M1.3-bucket1-claims.md`
(TeX: `docs/report/findings/milestone1_part3_bucket1_claims.tex`)  
Bucket 2 (**locked / closed; two claims**): `docs/experiments/qualitative/M1.3-bucket2-claims.md`
(TeX: `docs/report/findings/milestone1_part3_bucket2_claims.tex`)
Bucket 3 (**H0–H5 complete / analysed incl. H4b; no claim**):
`docs/experiments/qualitative/M1.3-bucket3-claims.md`

Buckets 1–2 turn the locked M12x inspection and M13-C1/C2 controls into six
evidence-backed claims. Bucket 3 now follows Fabrizio's 31 July deterministic-mechanism
direction one case at a time. Baseline H0 and probes H1–H5 are complete /
analysed (incl. H4b); H6/H7 signposted.
No Bucket 3 claim or broader comparative design is approved.
Prior provisional claim
drafting from earlier M12x grids remains **withdrawn** (2026-07-20) and must not be
reused.

M1.3 finishes when we can state what causal structure unguided ABA Learning can recover
under the approved controlled variations, why it succeeds or fails, and which limits
motivate Milestone 2 rather than merely reflecting observational non-identifiability.
See [`milestone1_high_level_path.md`](milestone1_high_level_path.md).

## Milestone Closure

After M1.3, consolidate findings into a Milestone 1 conclusion:

1. when target-wise ABA Learning recovers mechanism-aligned rules;
2. how target choice, data availability, graph/mechanism structure, and strategy affect
   recovery;
3. when collections of target-wise outputs support graph recovery;
4. which failures are strategic, representational, data-driven, or
   identifiability-limited;
5. which diagnosed limitations motivate Causal ABA-style guidance in Milestone 2.

**Current progress:** Part 1 closed. Part 2 (M12x) **closed**. Part 3 (M1.3) **in
progress** — Buckets 1–2 locked; Bucket 3 H0–H5 complete / analysed (including
H4b); H5 uses experimental `greedy_cautious` and is not an AAMAS-paper method;
H6/H7 signposted; no Bucket 3 claim.
No Part 4 / M1.4.
