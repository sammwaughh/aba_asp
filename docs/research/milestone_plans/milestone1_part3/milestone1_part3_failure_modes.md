# Milestone 1, Part 3 (M1.3) — Recovery patterns and limits

**Status:** `not started` — starts after expanded M1.2 is complete.  
**Primary path:** [`../milestone1_high_level_path.md`](../milestone1_high_level_path.md)  
**Parent index:** [`../milestone1-plan.md`](../milestone1-plan.md)

Filename retained for continuity; the work is **not** required to use a fixed “failure
mode” taxonomy. Prefer plain-English descriptions of recovery patterns and limits.

## 1. Goal and research question

Produce an evidence-backed account of **when and how mechanism-aligned rules are
recovered** by unguided ABA Learning — and **what is recovered instead** — grounded in
the expanded M1.2 results (and the M1.1 ordering account where still relevant). The
output informs Milestone 2 (Causal ABA integration).

> **RQ (M1.3).** Across the expanded M1.2 graphs and DGP(s), when does unguided ABA
> Learning recover the intended mechanism-aligned rules, what does it recover instead
> when it does not, and what evidence explains those patterns?

## 2. Inputs

- Expanded M1.2 outcome matrix and per-cell artefacts (`bk.sol.aba`, `prolog.stdout`,
  metrics), plus the pilot M1.2 inspection.
- M1.1 record: BK/representation ordering as one established limit under nd.
- Backing papers: ECAI 2024 (ASP-ABAlearnB), AAMAS 2025 (Greedy ABA Learning), and
  Proietti & Toni 2024. Summaries: `docs/theory/paper_summaries/`.

## 3. Method

1. **Draft candidate claims** in plain English from the expanded M1.2 matrix (and pilot
   patterns that still hold). Separate observational claims from mechanism claims.
2. **For each claim that matters**, design the smallest follow-up probe that would
   support or kill it (trace reading; option flip; correlation ladder; success-boundary
   fixture; etc.). Targeted ablations are permitted where a hypothesis needs evidence;
   they are not promised up front.
3. **Run probes; keep only surviving claims.**
4. **Write subsections** in ordinary language: describe the pattern → present the
   experimental evidence → state what is supported, what remains open, and (if anything)
   what it suggests for later Causal ABA guidance.

Attribution language (shared across both arms vs specific to one published strategy vs
encoding/pipeline) is useful when the evidence supports it; it is not a mandatory coding
scheme for every subsection.

Success criteria from M1.2 remain separate: intended-rule match vs ASP coverage. M1.3
must not redefine success as coverage alone.

## 4. Deliverable

- Experiment record with evidence-backed subsections:
  `docs/experiments/qualitative/M1.3-failure-modes.md` (name retained; content =
  recovery patterns and limits).
- Findings write-up:
  `docs/report/findings/milestone1_part3_m13_failure_taxonomy.tex` (or renamed when
  drafting if a clearer title is preferred).
- Registers and claims ledger synced.

M1.3 is done when Milestone 1 can answer succinctly: what unguided ABA Learning does on
these graphs/DGPs, why (with evidence), and what remains open for Milestone 2.

## 5. Artefact layout

| Artefact | Path |
|----------|------|
| Experiment record | `docs/experiments/qualitative/M1.3-failure-modes.md` |
| Ablation artefacts (if any) | `causal/outputs/aba_learning/grid/M13_<ablation-id>/` |
| Findings | `docs/report/findings/milestone1_part3_m13_failure_taxonomy.tex` |
| Registers | `docs/experiments/experiments_summary.md`, `docs/research/experiment_register.md`, `docs/report/claims_ledger.md` |

## 6. Caveats

- Scope claims carefully (graph, DGP, arm, encoding).
- Distinguish paper claims from this repository’s pipeline behaviour.
- Preserve ABA foundations / ABA Learning / Causal ABA / current `causal/` bridge.
- M1.3 makes no causal-discovery claims and does not include large-graph / bnlearn
  evaluation (deferred to a later milestone’s evaluation phase).
