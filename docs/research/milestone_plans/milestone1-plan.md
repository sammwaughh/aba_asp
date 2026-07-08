# Milestone 1 Plan

## Purpose

Milestone 1 produces a **report-ready account of when and how unguided ABA Learning can
recover mechanism-aligned rules from categorical tabular data**. "Unguided" means the
inherited ABALearn engine as published, with no Causal ABA integrations (those are
Milestone 2 and beyond).

The organising question is: given a small categorical table generated from a known graph
\(G\) and mechanism, and a fixed encoding into an ABA learning problem, do the published
variants of ABA Learning return the rules that the mechanism warrants — and when they do
not, exactly why not?

Framing rules for the whole milestone:

- The primary comparison is always **expected learned output vs actual learned output**,
  per (configuration, fixture) cell, with expected outputs pre-specified from \(G\) and the
  mechanism before any run.
- Quantitative metrics (parent-set F1, coverage flags, complexity counts) are recorded as
  **at-a-glance divergence detectors only**. No metric in this milestone is sufficient to
  determine what happened; when a cell diverges from expectation, qualitative inspection of
  `bk.sol.aba` and `prolog.stdout` is the instrument.
- This is RQ1 groundwork, not causal discovery. The pipeline does not perform Causal ABA
  reasoning over `arr`/`noe`/`indep`, d-separation, acyclicity, or stable extensions as
  graph hypotheses. Say "recovery of mechanism-aligned rules", not "learning causality".

### Scope restrictions (fixed for the milestone)

- **Categorical data only**, with \(k = 3\) categories per predictor throughout.
  Continuous data is out of scope: it enters the learner only after binning into
  categorical indicators, so its subtleties are a preprocessing question deferred until a
  Causal ABA integration exists.
- **No binary-only fixtures.** The binary positive-only encoding gives each row a single
  candidate fold partner per variable and hides the interesting phenomena; categorical-3
  contains the mechanism classes of interest.
- The number of predictor variables \(p\) is fixture-dependent (most fixtures use
  \(p = 2\); the conjunctive family needs \(p = 3\)).

## Working Method

For each part:

1. Write a bespoke planning document defining:
   - the precise goal and research question;
   - the graph and mechanism behind every fixture;
   - how the data will be constructed;
   - the expected learned rule or structure per cell (pre-specified);
   - important alternative outcomes and what they would mean;
   - suitable metrics and qualitative inspections;
   - the smallest experiment capable of answering the question.

2. Use Cursor to implement and run the agreed experiment.

3. Compare the actual learned rules and behaviour with the pre-specified expectations.
   Inspect raw artefacts where needed. **Qualitative inspection before further tests**
   when discrepancies remain (supervisor guidance, June 2026).

4. Draw a bounded, evidence-supported conclusion. Distinguish learning behaviour from
   implementation errors. For failures, document **why, when, and how** at trace/runner
   level — not only that a check failed.

5. Write a concise `.tex` findings document covering design, results, interpretation,
   conclusion and limitations.

The process should remain rigorous but lightweight. Documentation and additional runs
should serve a specific research decision rather than becoming ends in themselves.

## Part 1: Parent-Position and Representation-Order Control — **closed**

Planning documents (folder [`milestone1_part1/`](milestone1_part1/README.md)):

- Main design: [`milestone1_part1_parent_position.md`](milestone1_part1/milestone1_part1_parent_position.md)
- Ablation plan: [`milestone1_part1_ablations.md`](milestone1_part1/milestone1_part1_ablations.md)
- Greedy comparator (Stage 7): [`milestone1_part1_greedy_comparator.md`](milestone1_part1/milestone1_part1_greedy_comparator.md)

Experiment record: `docs/experiments/qualitative/M1.1-parent-position.md`
Findings: `docs/report/findings/milestone1_part1_m11_findings.tex`

### What M1.1 established

M1.1 was the initial investigation: an eight-cell metamorphic control (2 encodings ×
cells A/B/C/D via σ predictor-order reversal and π identity swap) on QL2-style
target-mechanism tables under the engine-default `nd` pipeline, plus ablations
(ABL-100–107) and a greedy folding comparator (Stage 7).

Key results (Stages 0–7, closed June 2026):

- Binary: parent-role tracking with full σ/π invariance under nd.
- Cat3 under nd: parent-role tracking only when the parent feature wins the first fold;
  σ-invariance **fails**, with an ablation-supported mechanism: BK serialisation order →
  rule IDs → first fold-candidate selection → entailment pass/fail → irreversible
  assumption commitment.
- Cat3 under greedy folding: rule-level σ restored, but all cells return parent-superset
  rules rather than the expected singleton.

**Carry-forward:** BK/representation ordering is the first confirmed failure mode for
mechanism-aligned rule recovery, with a complete trace-level account. It seeds the Part 3
taxonomy. σ/π grids are not repeated in Part 2; ordering is revisited in Part 3 only if
implicated in new failures.

## Part 2: Published-Configuration Comparison (M1.2)

Planning document: [`milestone1_part2/milestone1_part2_config_comparison.md`](milestone1_part2/milestone1_part2_config_comparison.md)
**Status:** `planned`

Direct comparison of the three published ABA Learning configurations shipped with the
inherited engine, run one-shot on shared handcrafted categorical fixtures designed to
expose their divergence:

| Arm | Config file | Published system |
|-----|-------------|------------------|
| ECAI | `configs/ecai2024_config.pl` | ASP-ABAlearnB (De Angelis, Proietti & Toni, ECAI 2024) |
| RuleML | `ruleml2025/ruleml2025_config.pl` | RASP-ABAlearn (De Angelis, Proietti & Toni, RuleML 2025) |
| AAMAS | `configs/aamas2025_config.pl` | Greedy ABA Learning (De Angelis, Proietti & Toni, AAMAS 2025) |

Fixture families are minimal categorical tables, each with a declared graph \(G\),
mechanism, and pre-specified expected learned output: a separator anchor, conjunctive and
disjunctive **mechanisms on a collider**, a **fork** (correlated-sibling confound), and a
correlated-ancestor chain. Five families × three arms = **15 cells**. Minimally
incoherent tables (originally planned to probe the RuleML vs AAMAS entailment gate) and
the RASP redress workflow are **deferred** follow-ups (see Part 2 plan Section 4.1).

The intended outcome is a write-up clearly reporting, per configuration and per fixture
family, whether the expected mechanism-aligned output is learned, what is learned
instead, and which divergences between the three systems the data exposes.

## Part 3: Failure-Mode Investigation (M1.3)

Planning document: [`milestone1_part3/milestone1_part3_failure_modes.md`](milestone1_part3/milestone1_part3_failure_modes.md)
**Status:** `not started` (inputs: Part 2 outcome matrix; Part 1 ordering mechanism)

Thorough inspection of every failure mode exposed by Part 2. For each recurring
divergence between expected and learned output, Part 3 must produce:

1. a **trace-level mechanistic account of exactly why** the divergence occurs (M1.1
   Stage-4 discipline: which rule, which fold, which gate, which commitment);
2. an **attribution level**: inherent to unguided ABA Learning as a paradigm (L1),
   specific to one published variant's algorithmic choices (L2), or an artefact of this
   repository's implementation or encoding (L3);
3. a **literature mapping** connecting L1/L2 entries to the mechanism described in the
   backing paper.

Targeted falsification ablations are permitted where a stated hypothesis requires
evidence, but are not promised up front.

The intended outcome is an evidence-backed taxonomy stating clearly and succinctly when
and how mechanism-aligned rules **cannot** be learned by unguided ABA Learning — the
requirements input for Milestone 2 (L1/L2 entries are candidate intervention points for
Causal ABA guidance; L3 entries are pipeline fixes, not findings).

## Milestone Closure

After Parts 2–3, consolidate the `.tex` findings into a concise Milestone 1 conclusion
addressing:

1. when unguided ABA Learning recovers mechanism-aligned rules on categorical tables;
2. how the three published configurations differ, and on which data properties;
3. the failure-mode taxonomy, with each mode's trace-level mechanism and attribution;
4. which findings motivate Causal ABA-style guidance in Milestone 2, and which are
   pipeline fixes.

**Current progress:** Part 1 **closed** (Stages 0–7). Part 2 `planned`. Part 3 not
started.
