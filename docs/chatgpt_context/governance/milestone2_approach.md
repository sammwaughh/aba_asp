# Milestone 2 — Causal ABA and ABA Learning integration

**Status:** opened on 8 August 2026; orientation stage active. No integration design,
prototype, or M2 experiment is yet approved or run.

**Predecessor:** Milestone 1 is closed. Its canonical closure synthesis is
`docs/experiments/qualitative/M13-C3-binary-collider-and/findings_for_fabrizio.tex`.

## Purpose

Milestone 2 investigates how Causal ABA and ABA Learning can be combined in a
theoretically coherent, implementable, and testable system. It begins from the limits of
unguided target-wise ABA Learning established in Milestone 1, but it does not assume in
advance what the integration should learn or how the two systems should be connected.

The milestone has three ordered stages:

1. understand the Causal ABA paper and implementation closely;
2. formulate and compare proper integration designs;
3. implement and test Samuel-approved designs through bounded experiments.

These are stages of one milestone, not an approved experiment matrix.

## Stage 1 — Theory and implementation orientation (current)

Read the Causal ABA theory and inspect its executable implementation before proposing an
integration. The orientation must establish, with precise paper and code references:

- the formal inputs, ABA language, assumptions, rules, contraries, attacks, and semantics;
- how arrow, no-edge, independence, dependence, acyclicity, collider-tree, and
  d-separation machinery are represented;
- how statistical or expert evidence enters the framework;
- how stable extensions are computed and converted into candidate causal graphs;
- which parts belong to abstract Causal ABA and which belong to the ABA-PC
  instantiation;
- the implementation entry points, data formats, dependencies, commands, generated
  artefacts, and practical limitations;
- which outputs or intermediate objects could in principle be consumed by ABA Learning;
- any incompatibility between the Causal ABA representation and the inherited ABALearn
  engine, including flatness, semantics, grounding, and target/example representation.

Canonical theory inputs begin with:

- `docs/papers/core/2024_Russo-Rapberger-Toni_Argumentative-Causal-Discovery_KR.pdf`;
- `docs/theory/paper_summaries/russo_2024_causal_aba.md`;
- `docs/theory/theory_primer.md`;
- `docs/theory/background.tex` and `docs/theory/literature_review.tex`.

Repository boundary at opening: no verified Russo-style Causal ABA implementation was
located inside this `aba_asp` checkout. The code location and version must therefore be
established before code-level findings are recorded. Do not infer implementation details
from the paper, the target-wise `causal/` bridge, ArgCausalDisco, or the presence of words
such as `collider` in fixture names.

**Stage-1 output:** a repository-grounded theory/implementation map that Samuel can check.
It should distinguish paper claims, inspected code facts, executable behaviour, and open
questions. Stage 1 is read-only unless Samuel separately approves setup or compatibility
work.

## Stage 2 — Integration design (after Stage 1)

Use the verified Stage-1 map and the closed Milestone-1 findings to formulate a small set
of genuinely distinct integration possibilities. For each candidate, define:

- the scientific question and intended contribution;
- which system produces and consumes each object;
- the learning target, learner-visible inputs, and recovery object;
- the role of Causal ABA evidence or constraints;
- the role of ABALearn transformations;
- the semantics and graph interpretation;
- controls, competing explanations, success criteria, and failure attribution;
- the smallest implementation change and experiment that could answer the question.

Samuel and the supervisors own the research choice and validation. Existing brainstorming,
including root `first-ideas.md`, is historical input only and is not an approved M2 plan.

## Stage 3 — Bounded implementation and testing

Implement one approved integration idea at a time. Each test must have its own experiment
ID and evidence record, preserve the unguided comparator where relevant, and separate:

- causal-information quality from learner-search behaviour;
- graph or equivalence-class recovery from local predictive-rule recovery;
- population information from finite-sample evidence;
- evaluator-only graph/mechanism truth from learner-visible information;
- procedural completion from semantic, mechanism-aligned, and causal success.

Do not begin with a broad benchmark grid. Inspect the first bounded result, document it,
and reassess before expanding.

## Milestone 1 evidence carried forward

M1.3 Bucket 3 closed with six cross-cutting findings under the exact-value deterministic
fixture regime:

1. completed Greedy solutions enumerate distinct positive value patterns and retain every
   measured predictor in those patterns;
2. nd solutions latch onto the first background-knowledge predictor;
3. brave nd can accept non-functional targets through row-ground assumption choices,
   while cautious nd blocks that construction on the tested tables;
4. the folding-token ceiling replays the same failed search under the current unary
   exact-value BK encoding;
5. distinct sample value patterns fix the search path, while repeated rows add grounded
   cost without changing it in the tested nested samples;
6. `sechk` confines brave nd to the first predictor on the tested cells and makes cautious
   search more expensive than `relto` without improving the recorded outcomes.

These findings motivate, but do not validate, any particular M2 integration. The bounded
working ABALearn baseline carried forward is cautious nd with `asm_intro(relto)`, support
compression only after frequency-sensitive information has been extracted, and
`folding_steps(1)` for the current exact-value encoding. These choices must be revisited if
M2 changes the background language or learning object.

## Guardrails and non-decisions

- Milestone 1, M12x, and M1.3 Buckets 1–3 are closed and are not rerun merely because M2
  begins.
- There is no M1.4.
- The current `causal/` package is not full Causal ABA.
- No Causal ABA code path, integration architecture, experiment fixture, metric, or run
  matrix is approved at milestone opening.
- Do not call an oracle-graph restriction causal discovery unless the learner-visible
  information and evaluation support that interpretation.
- Markov-equivalent structures remain observationally indistinguishable without additional
  information; integration cannot manufacture identifiability.
- Any changes to the inherited Prolog ABA Learning engine require Samuel's explicit
  approval.

## Documentation discipline

- Record theory/code orientation under `docs/research/`.
- Record each implemented M2 investigation under `docs/experiments/` using
  `docs/experiments/TEMPLATE.md`.
- Update `docs/experiments/experiments_summary.md`,
  `docs/research/experiment_register.md`, and `docs/report/claims_ledger.md` as evidence
  develops.
- Keep proposals, implementation facts, experiment observations, and report claims
  separate.

## Immediate next action

Locate the exact Causal ABA implementation and version to inspect, then undertake Stage 1:
read the paper and trace the implementation from inputs through ASP solving to candidate
graph outputs. Do not design or test an integration until that map has been reviewed by
Samuel.
