# Paper summary: Li et al. 2024 — On Causal Discovery in the Presence of Deterministic Relations

## Bibliographic record

Loka Li, Haoyue Dai, Hanin Al Ghothani, Biwei Huang, Jiji Zhang, Shahar Harel,
Isaac Bentwich, Guangyi Chen, and Kun Zhang. *On Causal Discovery in the
Presence of Deterministic Relations*. Advances in Neural Information Processing
Systems 37 (NeurIPS 2024).

## Role in this project

This paper is the main current source for understanding how deterministic
relations alter observational causal discovery. It supports the M1.3 decision
to keep causal sufficiency and Markov factorisation while treating faithfulness
and the recovery object as fixture-specific questions.

The paper is not an ABA Learning paper and its proposed deterministic causal
discovery algorithms are not implemented in this repository.

## Setting

The paper studies structural causal models in which a deterministic variable
is an exact function of its parents and has no additional exogenous noise:

```text
V_i = f_i(PA_i).
```

Causal sufficiency is assumed. Deterministic conditional distributions are
point masses, so the induced joint distribution can contain structural zeros
even when the root distributions are non-degenerate.

## Main theoretical points relevant here

- Causal Markov factorisation can remain valid in the presence of deterministic
  relations.
- Ordinary faithfulness is not guaranteed. Determinism can create additional
  independences not represented by d-separation, including independences caused
  by variables becoming constant under conditioning.
- The paper introduces a weaker non-deterministic faithfulness condition that
  excludes specified determinism-induced violations. This project does not
  silently substitute that condition for ordinary faithfulness: fixtures are
  audited explicitly and the condition used must be named.
- Standard Markov-equivalence reasoning remains applicable to relevant
  non-deterministic or bridge parts of a graph, but the usual whole-graph MEC
  characterisation may not be adequate inside deterministic clusters.
- A deterministic two-variable relation may be recoverable only up to its
  observational equivalence class. Determinism alone does not identify the
  arrow direction.

## Consequences for M1.3 fixture design

For each proposed deterministic fixture, record separately:

1. the generating DAG and root distributions;
2. every non-root truth table;
3. the exact induced joint distribution and its structural zeros;
4. the population conditional independences and ordinary-faithfulness result;
5. the standard MEC/CPDAG as an ordinary conditional-independence reference;
6. any deterministic-relation identifiability caveat; and
7. the mechanism-aligned exact-value rules used only for evaluation.

The finite sample is a separate object. It may omit population-supported parent
configurations, and no learner can infer a rule branch that is absent from its
learner-visible evidence without additional bias or knowledge.

## Limits on project interpretation

A learned predictive rule is not automatically a recovered causal mechanism.
Agreement with evaluator-only mechanism rules is a bounded mechanism-alignment
observation. Graph identification, mechanism representation, finite-sample
availability, and ABA Learning strategy must be assessed separately.
