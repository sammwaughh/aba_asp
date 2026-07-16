# Milestone 1 Plan

**Primary working path:** [`milestone1_high_level_path.md`](milestone1_high_level_path.md)  
Use that document as the day-to-day reference for what is done, what remains, and the order of work. This file is the milestone index and part summaries.

## Purpose

Milestone 1 produces a **report-ready account of when and how unguided ABA Learning can
recover mechanism-aligned rules from categorical tabular data** — and what is recovered
instead. "Unguided" means the inherited ABALearn engine as published, with no Causal ABA
integrations (those are Milestone 2 and beyond).

The organising question is: given a small categorical table generated from a known graph
\(G\) and mechanism, and a fixed encoding into an ABA learning problem, do the published
variants of ABA Learning return the rules that the mechanism warrants — and when they do
not, what happens and why?

Framing rules for the whole milestone:

- The primary comparison is always **intended learned output vs actual learned output**,
  per (configuration, fixture) cell, with intended outputs pre-specified from \(G\) and the
  mechanism before any run.
- **ASP coverage** (E⁺ covered / E⁻ rejected) is recorded separately and must not be
  conflated with intended-rule match.
- Quantitative metrics are **at-a-glance detectors only**. The instrument is qualitative
  inspection of `bk.sol.aba` and `prolog.stdout` — what happens, why, and which patterns
  recur across graphs.
- This is RQ1 groundwork, not causal discovery. Say "recovery of mechanism-aligned rules",
  not "learning causality".

### Scope restrictions (fixed for the milestone)

- **Categorical data only.** Continuous / large-scale bnlearn comparisons are out of
  Milestone 1 (reserved for a later evaluation phase against any Causal-ABA-informed
  solution). There is **no M1.4**.
- **No binary-only fixtures** as the primary evidence base (categorical encodings expose
  the mechanism classes of interest).
- **Arms:** ECAI and AAMAS only (no RuleML).
- **Graphs for the expanded M1.2:** Fabrizio’s usable small DAGs in the repo; exclude
  random graphs, bnlearn networks, and cycles.

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

## Part 2: Published-Configuration Comparison (M1.2) — **expanding**

Planning folder: [`milestone1_part2/`](milestone1_part2/README.md)  
Detail plan: [`milestone1_part2/milestone1_part2_config_comparison.md`](milestone1_part2/milestone1_part2_config_comparison.md)

| Phase | Status | Content |
|-------|--------|---------|
| Pilot grid | Analysed (Stages 0–3) | 2 arms × 5 minimal handcrafted fixtures (10 cells); locked intended rules; cell inspection |
| Expanded grid | Next | Fabrizio small DAGs × chosen DGP(s); intended rules locked before runs; same two arms |

Arms:

| Arm | Config file | Published system |
|-----|-------------|------------------|
| ECAI | `configs/ecai2024_config.pl` | ASP-ABAlearnB (ECAI 2024) |
| AAMAS | `configs/aamas2025_config.pl` | Greedy ABA Learning (AAMAS 2025) |

Expanded M1.2 finishes when fixtures/simulators exist, the grid is run, artefacts and a
summary matrix exist, and every cell has a plain-English intended-vs-learned inspection.
See [`milestone1_high_level_path.md`](milestone1_high_level_path.md) §1–2.

## Part 3: Recovery patterns and limits (M1.3) — **after expanded M1.2**

Planning folder: [`milestone1_part3/`](milestone1_part3/README.md)  
Detail plan: [`milestone1_part3/milestone1_part3_failure_modes.md`](milestone1_part3/milestone1_part3_failure_modes.md)

M1.3 turns the expanded M1.2 matrix into evidence-backed claims: draft candidate claims in
plain English; design the smallest probes that would support or kill each claim; run those
probes; write subsections describing each recovery pattern / limit with experimental
evidence. No forced category scheme required.

M1.3 finishes when we can state succinctly what unguided ABA Learning does on these
graphs/DGPs, why, and what remains open for Milestone 2.
See [`milestone1_high_level_path.md`](milestone1_high_level_path.md) §3.

## Milestone Closure

After expanded M1.2 and M1.3, consolidate findings into a Milestone 1 conclusion:

1. when unguided ABA Learning recovers mechanism-aligned rules on categorical tables;
2. how the two published configurations differ, and on which data properties;
3. what is systematically recovered instead, with evidence;
4. which findings motivate Causal ABA-style guidance in Milestone 2, and which are
   pipeline or encoding issues.

**Current progress:** Part 1 closed. Part 2 pilot analysed; Part 2 expansion next.
Part 3 waits on expanded Part 2. No Part 4 / M1.4.
