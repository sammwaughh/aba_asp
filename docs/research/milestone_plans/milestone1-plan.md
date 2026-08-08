# Milestone 1 Plan

**Primary working path:** [`milestone1_high_level_path.md`](milestone1_high_level_path.md)  
**Expanded M1.2 Approach:** [`milestone1_part2/milestone1_part2_expanded_approach.md`](milestone1_part2/milestone1_part2_expanded_approach.md)  

Milestone 1 is closed. Use the high-level path as its closure/navigation record and the
part approaches as historical method records. Active successor:
[`milestone2/README.md`](milestone2/README.md).

## Purpose

Milestone 1 produced a **report-ready account of what causal structure unguided ABA
Learning can recover from controlled tabular data, under which targets,
data-availability conditions, graph/mechanism structures, and learning strategies —
and which limitations are informational rather than strategic**. "Unguided" means the
inherited ABALearn engine as published, with no Causal ABA integrations (those are
Milestone 2 and beyond).

M1.1, M1.2, and M1.3 are complete. Fabrizio's 22 July review expanded M1.3; his
31 July review set the method as one root-stochastic, deterministic-non-root binary
mechanism case at a time, with expected mechanism rules fixed before ABALearn. H0–H7b
implemented that bounded investigation, and the cross-probe findings were consolidated
before closure on 8 August 2026.

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

### Closed scope and guardrails

- M12x and M1.3 Buckets 1–3 are closed and remain preserved.
- Categorical \(K=3\) remains a completed baseline. Additional category counts,
  non-discrete data, larger DAGs, and bnlearn-scale evaluation were not required for M1
  closure; any later use requires a new decision.
- ECAI and AAMAS are completed M1 comparison arms.
- Any later causal fixture must document graph–mechanism validity, support, expected outputs,
  and relevant marginal/conditional-independence and Markov-equivalence properties.
- The completed Bucket-3 fixture regime used mutually independent non-degenerate stochastic roots
  and deterministic non-root functions. Each fixture needs a full truth table, exact
  support/faithfulness certificate, and evaluator-only canonical rule reference before a
  sample or learning run is selected.
- New target-wise fixtures use lowercase internal identifiers `a`, `b`, `c`, ... and
  corresponding mathematical labels (A,B,C,\ldots); existing `xN` evidence is preserved.
- There is **no M1.4**; the supervisor-driven expansion closed within M1.3.

## Working method used

For each part, the project:

1. wrote or updated a bespoke planning document defining the goal, graphs/mechanisms, DGP(s),
   intended learned rules, and the smallest experiment that answers the question.
2. used the active implementation agent to implement and run the agreed experiment;
3. compared actual learned rules with pre-specified intentions and inspected raw artefacts;
4. drew bounded, evidence-supported conclusions, preferring plain-English pattern descriptions
   over invented taxonomies.
5. wrote a concise `.tex` findings document when the evidence for that part was ready.

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

## Part 3: Causal-recovery capabilities and limits (M1.3) — **closed**

Planning folder: [`milestone1_part3/`](milestone1_part3/README.md)  
Approach (method): [`milestone1_part3/milestone1_part3_approach.md`](milestone1_part3/milestone1_part3_approach.md)  
Detail plan: [`milestone1_part3/milestone1_part3_failure_modes.md`](milestone1_part3/milestone1_part3_failure_modes.md)  
Bucket 1 (**locked**): `docs/experiments/qualitative/M1.3-bucket1-claims.md`
(TeX: `docs/report/findings/milestone1_part3_bucket1_claims.tex`)  
Bucket 2 (**locked / closed; two claims**): `docs/experiments/qualitative/M1.3-bucket2-claims.md`
(TeX: `docs/report/findings/milestone1_part3_bucket2_claims.tex`)
Bucket 3 (**closed; H0–H7b complete / analysed incl. H4b**):
`docs/experiments/qualitative/M1.3-bucket3-claims.md`

Buckets 1–2 turn the locked M12x inspection and M13-C1/C2 controls into six
evidence-backed locked claims. Bucket 3 followed Fabrizio's 31 July
deterministic-mechanism direction through H0–H7b. Its six cross-cutting closure findings
are recorded in
`docs/experiments/qualitative/M13-C3-binary-collider-and/findings_for_fabrizio.tex`.
No separate locked Bucket-3 claim list was created.
Prior provisional claim
drafting from earlier M12x grids remains **withdrawn** (2026-07-20) and must not be
reused.

M1.3 closed after the synthesis stated what the tested unguided ABA Learning strategies
did, why the recorded outcomes arose, and which learner behaviours motivate Milestone 2.
See [`milestone1_high_level_path.md`](milestone1_high_level_path.md).

## Milestone closure — **complete**

The closure synthesis consolidates the evidence around:

1. when the tested target-wise ABA Learning configurations recover mechanism-aligned rules;
2. how target choice, data availability, graph/mechanism structure, and strategy affect
   recovery;
3. why the current collections of target-wise outputs do not themselves constitute graph
   or CPDAG recovery;
4. which failures are strategic, representational, data-driven, or
   identifiability-limited;
5. which diagnosed limitations may be relevant when possible integrations are considered
   in Milestone 2.

**Final status:** Part 1 closed. Part 2 (M12x) closed. Part 3 (M1.3) closed.
No Part 4 / M1.4. Milestone 2 is open under its deliberately agnostic approach; see
[`milestone2/README.md`](milestone2/README.md).
