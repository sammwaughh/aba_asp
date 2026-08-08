# Milestone 1, Part 3 (M1.3) — Recovery patterns and limits

**Status:** historical detail plan; M1.3 is **closed**. Bucket 1 and Bucket 2 are
locked; Bucket 3 H0–H7b are complete / analysed and consolidated in
`docs/experiments/qualitative/M13-C3-binary-collider-and/findings_for_fabrizio.tex`.
**Primary path:** [`../milestone1_high_level_path.md`](../milestone1_high_level_path.md)  
**Parent index:** [`../milestone1-plan.md`](../milestone1-plan.md)  
**Approach (method):** [`milestone1_part3_approach.md`](milestone1_part3_approach.md)  
**Primary evidence (locked):** `docs/experiments/qualitative/M1.2-expanded-cell-inspection.md`;
`causal/outputs/aba_learning/grid/M12x_summary.md`

Filename retained for continuity; the work is **not** required to use a fixed “failure
mode” taxonomy. Prefer plain-English descriptions of recovery patterns and limits.

The method below describes the completed M12x-centred Bucket 1/2 phase. It is not a
next-step guide. See `docs/experiments/qualitative/M1.3-bucket3-claims.md` and the
part-3 `README.md` for closure; active work is in Milestone 2.

## 1. Goal and research question

Produce an evidence-backed account of **when and how mechanism-aligned rules are
recovered** by unguided ABA Learning — and **what is recovered instead** — grounded in
the expanded M1.2 results (and the M1.1 ordering account where still relevant). The
output informs Milestone 2 (Causal ABA integration).

> **RQ (M1.3).** Across the expanded M1.2 graphs and DGP(s), when does unguided ABA
> Learning recover the intended mechanism-aligned rules, what does it recover instead
> when it does not, and what evidence explains those patterns?

## 2. Inputs

- **M12x (completed input):** Stage-3 inspection (18/18);
  summary matrix (`M12x_summary.md`); cell reports; runner cells under
  `causal/outputs/aba_learning/grid/M12x_{ecai2024,aamas2025}/`.
  Prior superseded M12x outputs were deleted (2026-07-20); the fresh locked package
  replaced them.
- Pilot M1.2 inspection (optional provenance).
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

- Bucket 1 claims (**locked**):
  `docs/experiments/qualitative/M1.3-bucket1-claims.md` and
  `docs/report/findings/milestone1_part3_bucket1_claims.tex`.
- Bucket 2 claims (**locked**):
  `docs/experiments/qualitative/M1.3-bucket2-claims.md` and
  `docs/report/findings/milestone1_part3_bucket2_claims.tex`.
- Bucket 3 investigation/closure:
  `docs/experiments/qualitative/M1.3-bucket3-claims.md` and
  `docs/experiments/qualitative/M13-C3-binary-collider-and/findings_for_fabrizio.tex`.
- Registers and claims ledger synced.

M1.3 met this closure condition on 8 August 2026.

## 5. Artefact layout

| Artefact | Path |
|----------|------|
| Bucket 1 claims (MD) | `docs/experiments/qualitative/M1.3-bucket1-claims.md` (locked) |
| Bucket 1 claims (TeX) | `docs/report/findings/milestone1_part3_bucket1_claims.tex` |
| Bucket 2 claims (MD) | `docs/experiments/qualitative/M1.3-bucket2-claims.md` |
| Bucket 2 claims (TeX) | `docs/report/findings/milestone1_part3_bucket2_claims.tex` |
| Bucket 3 closure (MD) | `docs/experiments/qualitative/M1.3-bucket3-claims.md` |
| Bucket 3 synthesis (TeX) | `docs/experiments/qualitative/M13-C3-binary-collider-and/findings_for_fabrizio.tex` |
| Ablation artefacts (if any) | `causal/outputs/aba_learning/grid/M13_<ablation-id>/` |
| Findings (Bucket 1 TeX) | `docs/report/findings/milestone1_part3_bucket1_claims.tex` |
| Registers | `docs/experiments/experiments_summary.md`, `docs/research/experiment_register.md`, `docs/report/claims_ledger.md` |

## 6. Caveats

- Scope claims carefully (graph, DGP, arm, encoding).
- Distinguish paper claims from this repository’s pipeline behaviour.
- Preserve ABA foundations / ABA Learning / Causal ABA / current `causal/` bridge.
- The current bridge remains target-wise ABA Learning, not full causal discovery.
  Bucket 3 investigates capabilities, limitations, and identifiability under controlled
  extensions; large-scale external evaluation remains a later phase.
