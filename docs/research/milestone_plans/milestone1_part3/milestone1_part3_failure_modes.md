# Milestone 1, Part 3 (M1.3) — Failure-mode investigation

**Status:** `not started` — M1.2 outcome matrix and cell inspection are available.
**Parent index:** [milestone1-plan.md](../milestone1-plan.md) (Part 3 section)

## 1. Goal and research question

Produce an evidence-backed account of **when and how mechanism-aligned rules cannot be
learned** by unguided ABA Learning, grounded in the M1.2 results and the academic
literature backing the two scoped configurations. The output informs the start of
Milestone 2 (Causal ABA integration).

> **RQ (M1.3).** For each failure or divergence class observed in M1.2, what is the exact
> mechanism that produces it, at which level does the cause live (paradigm, published
> variant, or implementation/encoding), and what does the backing literature say about
> it?

## 2. Inputs

- The M1.2 config × fixture outcome matrix and all per-cell artefacts
  (`bk.sol.aba`, `prolog.stdout`, metrics).
- The M1.1 record: BK/representation ordering is the first confirmed failure mode, with a
  complete trace-level mechanism (BK serialisation order → rule IDs → first-fold
  selection → entailment gate → assumption commitment). It enters the taxonomy directly.
- The backing papers: De Angelis, Proietti & Toni ECAI 2024 (ASP-ABAlearnB) and AAMAS
  2025 (Greedy ABA Learning); plus Proietti & Toni 2024 for the
  transformation-rule foundations. Summaries: `docs/theory/paper_summaries/`.

## 3. Method

For **each** failure mode (recurring divergence between pre-specified expected output and
learned output), produce all three of:

1. **Trace-level mechanistic account — mandatory.** Classification alone is not
   sufficient: every failure mode must be traced to exactly why it occurs, at the
   granularity of the M1.1 Stage-4 discipline — which rote rule was selected, which fold
   candidate was chosen and why, which gate (entailment / subsumption / assumption
   introduction) fired, and where the derivation committed. Evidence: line-referenced
   `prolog.stdout` excerpts and the relevant engine predicates
   (`gen.pl`, `folding.pl`, `asp_utils.pl`, `asp_engine.pl`).

2. **Attribution level** (the L1/L2/L3 scheme), with the matching evidence standard:

   | Level | Cause lives in | Evidence standard |
   |-------|----------------|-------------------|
   | **L1** | Unguided ABA Learning as a paradigm: both scoped systems fail the same way because the objective (cover \(E^+\), exclude \(E^-\)) carries no causal information | Argument from the papers' problem definitions; cross-arm uniformity in the M1.2 matrix |
   | **L2** | A specific published variant's algorithmic choices; a different published variant demonstrably avoids it | Cross-arm divergence in the M1.2 matrix + the paper's description of the differing mechanism |
   | **L3** | This repository's implementation or our encoding; implied by no paper | Trace-level account and/or targeted ablation |

3. **Literature mapping.** For L1/L2 entries, the specific paper mechanism (e.g.
   token-bounded nd search; greedy fold-with-all-partners; `mgr` selection; post-folding
   entailment gate; brave stable-model semantics) that explains the behaviour, with the
   citation.

**Ablations.** Targeted falsification ablations (M1.1 Stage-6 style: state hypothesis →
minimal intervention → predicted observable) are permitted where a stated hypothesis
requires evidence, but are not promised up front. Designated candidates, triggered only
if implicated: `asm_intro(sechk)` on an assumption-introduction-implicated ECAI cell;
folding-mode/selection probes for disjunctive compression; representation-order
interventions if ordering resurfaces beyond the M1.1 account.

## 4. Deliverable

A failure-mode taxonomy in the experiment record, one section per mode:

```text
FM-<n> — <short name>
  Observed in: <arms × fixtures>
  Expected vs learned: <one-line contrast>
  Mechanism (traced): <why exactly, with artefact line references>
  Attribution: L1 | L2 | L3 (+ justification)
  Literature: <paper + mechanism> (L1/L2) | — (L3)
  M2 relevance: <candidate Causal ABA intervention point> (L1/L2)
                | <pipeline fix, not a finding> (L3)
```

plus a findings write-up stating clearly and succinctly when and how mechanism-aligned
rules cannot be learned by unguided ABA Learning, and which of those limits Milestone 2's
Causal ABA guidance should target.

## 5. Artefact and documentation layout

| Artefact | Path |
|----------|------|
| Experiment record (taxonomy) | `docs/experiments/qualitative/M1.3-failure-modes.md` |
| Ablation artefacts (if any) | `causal/outputs/aba_learning/grid/M13_<ablation-id>/` |
| Findings | `docs/report/findings/milestone1_part3_m13_failure_taxonomy.tex` |
| Registers to sync | `docs/experiments/experiments_summary.md`, `docs/research/experiment_register.md`, `docs/report/claims_ledger.md` |

## 6. Interpretation rules and caveats

- Every "cannot be learned" claim must carry its attribution level and scope; L3 entries
  must not be presented as findings about ABA Learning.
- Distinguish what the papers prove from what this implementation does; where they
  differ, the divergence itself is an L3 observation.
- Preserve the standing distinctions: ABA foundations / ABA Learning / Causal ABA /
  current `causal/` bridge. M1.3 makes no causal-discovery claims.
