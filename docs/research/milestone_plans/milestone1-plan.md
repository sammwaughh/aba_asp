# Milestone 1 Plan

## Purpose

Milestone 1 will close the **unguided causal-role diagnostic** for the current target-wise ABA Learning pipeline. Parent-set recovery remains the main organising proxy, but the purpose is broader than parent F1: each investigation should assess whether the learnt rules correspond to direct parents, ancestor or sibling proxies, partial parent sets, representation/order artefacts, search-strategy effects, no-solution behaviour, or implementation failures.

This is still RQ1 groundwork, not causal discovery. The current implementation does not yet perform full Causal ABA reasoning over `arr`/`noe`/`indep`, d-separation, acyclicity, or stable extensions as graph hypotheses. The aim is to understand what unguided ABA Learning does before Causal ABA-style guidance is introduced.

The four investigations will be completed sequentially. Detailed decisions will be made immediately before each investigation rather than fixed prematurely here.

## Working Method

For each investigation:

1. Write a bespoke planning document defining:
   - the precise goal and research question;
   - the graph and DGP;
   - how the data will be constructed;
   - the expected learned rule or outcome;
   - important alternative outcomes and what they would mean;
   - suitable metrics and qualitative inspections;
   - the smallest experiment capable of answering the question.

2. Use Cursor to implement and run the agreed experiment.

3. Compare the actual learned rules and behaviour with the pre-specified expectations. Inspect raw artefacts where needed. **Qualitative inspection before further tests** when discrepancies remain (supervisor guidance, June 2026). Expand only when initial evidence is genuinely ambiguous or when a stated hypothesis requires ablation.

4. Draw a bounded, evidence-supported conclusion. Distinguish learning behaviour from implementation errors and avoid causal-discovery claims. For failures, document **why, when, and how** at trace/runner level where required — not only that a metamorphic check failed.

5. Write a concise `.tex` findings document covering the design, results, interpretation, conclusion and limitations (update when extended investigation phases complete).

The process should remain rigorous but lightweight. Documentation and additional runs should serve a specific research decision rather than becoming ends in themselves.

## Part 1: Parent-Position and Representation-Order Control

Planning document: `milestone1_part1_parent_position.md`  
**Ablation plan:** `milestone1_part1_ablations.md`  
Experiment record: `docs/experiments/qualitative/M1.1-parent-position.md`  
Interim findings: `docs/report/findings/milestone1_part1_m11_findings.tex`

### Goal

Address the unresolved weakness in QL2 by testing whether learned rules follow the true parent when parent and non-parent positions are exchanged, or whether recovery is affected by variable identity or representation order — and, where π/σ fail, **explain why/when/how** at granular trace and runner level.

### DGP (clarified)

Small, clean **target-mechanism tables**: one predictor is a deterministic direct cause of `x2` (`x2 := parent`), the other is statistically isolated in a complete factorial. **Not** chain SCM sampling; chain-style labels in fixtures annotate parent vs non-parent roles for the π swap only.

### Two phases

| Phase | Content | Status (June 2026) |
|-------|---------|-------------------|
| **A — Metamorphic grid** | Stages 0–3: fixtures, eight-cell nd run, σ/π square, triggered cat3 A vs B trace | **Done** (Stage 3 provisional) |
| **B — Mechanistic account** | Stages 4–6: trace mechanism + ablations | **Done** |

### Phase A — what was done

- Implemented eight fixtures (binary + cat3; cells A/B/C/D via σ and π).
- Stage 0: all fixtures PASS; BK order verified.
- Stage 1: 8/8 cells `solved` under nd (`M11_parent_position.yaml`).
- Stage 2: binary passes all σ and π checks; cat3 fails σ-invariance (A↔B, D↔C); π holds B↔C only.
- Stage 3: first-fold trace correlation on cat3 A vs B recorded — **insufficient for closure**.
- Interim findings `.tex` written for supervisor review.

### Phase B — what was done

- Stage 4: granular trace audit cat3 A vs B (BK order → `select_rule` → entailment → assumptions).
- Stage 6: ablations ABL-100–107 (ABL-106 skipped); artefacts `M11_ablations/`.
- Findings `.tex` rewritten with integrated ablation-supported conclusion.
- Optional: Stage 5 runner call-chain doc.

### Status

**`analysed`** — Part 1 complete (Stages 0–6). Fabrizio review requirements addressed.

### Part 2 dependency

**M1.2 full greedy grid** is the **next comparator experiment**; not required to explain cat3 σ failure.

## Part 2: Greedy Versus Non-Deterministic ABA Learning

Planning document: `milestone1_part2_greedy_vs_nondeterministic.md`  
**Status:** `planned` — **blocked** on m1.1 Phase B progress

Determine which currently implemented folding strategy should be the operational default for the remaining Milestone 1 work.

**Dependency:** Part 2 assumes a clearer mechanistic account of m1.1 cat3 σ failure (Part 1 Phase B). A quick greedy smoke test on the m1.1 grid produced an outcome materially different from both nd cat3 A and B — strategy comparison alone does not explain the divergence.

The investigation should compare greedy and non-deterministic learning on controlled fixtures, assessing both computational behaviour and agreement with expected learned rules. It should test whether greedy is faster, more reliable or more causally aligned, while allowing for the possibility that its advantages are conditional rather than universal.

The intended outcome is a supported strategy decision, including any limitations and the circumstances in which the alternative strategy should remain a comparator.

## Part 3: Qualitative Failure Analysis

Planning document: `milestone1_part3_failure_analysis.md`

Investigate a small number of informative discrepancies from the improved QL2 experiments and the strategy comparison.

Priority should be given to:

- failures that remain under the selected default strategy; and
- paired cases where greedy and non-deterministic learning produce materially different outcomes.

The investigation should compare the graph- and DGP-derived expected rules with the actual learned rules and relevant execution artefacts. Possible explanations may involve data construction, representation, transformation search, hypothesis-space restrictions, entailment or solver behaviour, but conclusions must follow from inspected evidence.

The intended outcome is an evidence-backed account of representative failure mechanisms. It is not necessary to inspect every cell or repair every failure.

**Note:** m1.1 cat3 σ failure may overlap Part 3 thematically; Part 1 Phase B owns the primary mechanistic account for that specific grid.

## Part 4: Noise and Continuous-DGP Investigation

Planning document: `milestone1_part4_noise_and_continuous.md`

Conduct a principled investigation of how the current pipeline behaves when data are sampled from noisy continuous DGPs and then encoded for ABA Learning.

The investigation must distinguish:

- the continuous causal DGP;
- finite-sample effects;
- discretisation and target construction;
- ABA Learning behaviour.

A sensible progression is to establish whether the expected relationship survives the representation pipeline under a low-noise baseline before varying noise or other factors. The exact DGP, noise model, sample sizes, discretisation choices and metrics will be decided during bespoke planning.

The intended outcome is a bounded conclusion about the tested conditions under which parent-aligned rules remain recoverable, the failure modes that emerge with noise, and the implications for later Causal ABA guidance.

The previous binary `unknown constant` issue will not be treated as a separate investigation. It will be examined only if it recurs and prevents valid interpretation of this study.

## Milestone Closure

After all four investigations, consolidate their `.tex` findings into a concise Milestone 1 conclusion addressing:

1. when unguided ABA Learning recovers expected parent-aligned rules;
2. which mistakes and failure mechanisms recur;
3. what greedy learning improves and does not improve;
4. how the current system behaves on noisy continuous-derived data; and
5. which findings motivate Causal ABA-style guidance in Milestone 2.

**Current progress:** Part 1 **analysed**; Part 2 (M1.2) next comparator. Parts 3–4 not started.
