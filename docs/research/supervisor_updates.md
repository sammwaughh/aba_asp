# Supervisor Guidance

Structured record of supervisor guidance for the Causal ABA Learning project. This is the repo
source for the ChatGPT-facing `supervisor_guidance_current.md` mirror. It records guidance as
received; it is not experiment evidence and not report prose.

Supervisors: **Fabrizio** (primary) and **Francesco**.

---

## Meeting with Francesco

- **Do not use AI for idea generation.** Using AI for validation is also very risky because it
  cannot reason and cannot actually validate the ideas. Ideas and their validation must come from
  Samuel and the supervisors.
- **The project mark depends a lot on the presentation.** It is correct to allocate proper time
  to it. Presenting well is very important for a PhD, so use this as genuine practice and do the
  best possible job.
- **Writing should progress linearly, not uniformly.** Logging progress and keeping a record of
  what was done and why is important, but the actual report writing should progress linearly over
  the weeks rather than being spread evenly across all 10 weeks.

---

## Meeting with Fabrizio (June 12th)

### Core points

- **Know the rules that will come out.** Be clear about which ABA rules the learner is expected
  to produce.
- **Construct inputs carefully (graph + DGP -> table) with expected outputs (learned rules).**
  This is the more nuanced way to measure whether what we want ABA Learn to learn is actually
  being learnt: actual outputs can be compared directly against expected outputs, and we can then
  dig into *why* they differ. It also lets us set success metrics that are more nuanced than
  "parents appear as members of a rule body".
- **The DGP is a very important part; describing the DGP clearly is important.** Do this for the
  experimentation. Soon, take what Fabrizio has done (linear-with-noise work — find this) and
  make it clear and improve it.
- **Set clear expectations of what should come out, so success metrics can be defined.** This is
  much more nuanced than parent membership of the rule body.
- **ABA rules constraining Causal ABA is a direction of work.**
- **Ultimate goal:** learn causal relationships from data in an argumentative fashion — i.e.
  learn ABA rules that reflect that causality. There are several possible routes. One route is to
  use insights from Causal ABA to improve ABA Learn; Causal ABA could inform the background of an
  ABA framework for ABA Learning (causal guidance).

### Advice from the meeting

- Reasoning about the discrepancy between the expected outputs from a hand-crafted DGP and the
  actual results is how we investigate properly.
- Presented results should have an interpretation and a conclusion to earn their place in a
  report.
- Constructing inputs (graph + DGP -> table) carefully from which we expect certain outputs
  (learned rules) is the more nuanced way to measure if what we want ABA Learn to learn is being
  learnt, because actual outputs can be compared directly against expected outputs and we can dig
  into why they differ. This also lets us set success metrics more nuanced than parents as
  members of the body of a rule.
- The DGP is very important; describe it clearly. Do this for the experimentation, and find out
  where the noise comes from for QL3 and describe it.
- Set clear expectations of what should come out, so success metrics can be set. This is much
  more nuanced than parent membership of the body.

### Actions from the meeting

- Improve QL2 by including a comparison showing order dependence (the parent-position swap of
  `(x0, x1)` that was not implemented in QL2).
- Change the "clean" score to an F1 metric.
- Describe the DGP clearly.
  - Find out where the noise comes from for QL3 and describe it.
- Be very sceptical of the reasons AI gave for what happened. Actually look into them closely.

---

## Fabrizio's guidance (June 5th)

- The main thing to investigate first is the **when, how, why and what** of whether ABA Learn can
  learn causal rules.
- **Simple 3-node graphical structures** and ABA Learn's learning methods are the main variables
  (verticals) to judge to get going. Qualitative investigation is a good first step: try small
  examples and inspect what ABA Learn can recover.
- In some basic work, Fabrizio found that **greedy is better than non-deterministic** for ABA
  Learn learning causality, but he did not demonstrate it properly. Establishing this is another
  good first thing to try.
- Think up **principled metrics from first principles** — for example, how many folds ABA Learn
  does as a measure of efficiency. This requires thought and should be tailored to each
  experiment.
- For the report section on these experiments, **narrating simple examples** is a good way to
  demonstrate qualitatively what happened.
- Presenting some **quantitative findings** is good too — this is what the metrics and infra
  frameworks already support to some extent.
- As an **extension**, go beyond the 3-node composite structures.
- Understanding the **data-generating process from ArgCausalDisco** (the sister repo) is
  important for getting started, because it is used to generate the samples ABA Learn encodes.
- Overall expectation: if a chosen causal graph is used to generate data with ArgCausalDisco's
  implementation, this produces tabular data relating the graph's variables. This data contains
  some noise which, in theory, ABA Learn should be able to represent as exceptions in the
  argumentation framework and so derive the correct rules to represent the causality. Our goal is
  to establish the extent to which ABA Learning can do this, and the when, why and how of its
  attempts to learn causal rules.

### Model-use policy (for Samuel's AI workflow)

Shortcut: **Thinking for work. Pro for judgement.** Use Thinking by default; use Pro for
judgement-heavy moments; use fast/Instant only for trivial formatting.

- **Use Pro for:** first orientation of a major new chat; final approval of an experiment design
  before handing to Cursor; interpreting results into formal research claims; checking "what can
  we legitimately claim?"; resolving ABA Learning vs Causal ABA vs current-implementation
  distinctions; reviewing theory-sensitive Cursor plans/diffs; final review of major report
  sections (Introduction / Literature Review / Methodology / Evaluation); cross-paper synthesis;
  deciding project framing/contribution/direction; preparing material for Fabrizio / the second
  marker; reviewing the GenAI-use declaration; major milestone checks.
- **Use Thinking for:** main hub coordination; ordinary experiment ideation; first-pass design;
  Cursor prompt drafting; normal plan review; single-paper explanation; ordinary report drafting;
  updating experiment-register text; routine strategic questions; most day-to-day work.
- **Use fast/Instant for:** formatting commands; naming chats; short checklists; simple rewrites;
  Notion organisation.

---

## Implications already actioned / in progress

- Report labels fixed as **QL1 = QI-001, QL2 = QI-002, QL3 = QI-004**; the earlier n=100 scaled
  attempt was cut and is not part of the canonical set.
- The Experimentation chapter (`docs/report/manuscript/experimentation.md`) describes the QL3 DGP
  explicitly (binary flip, categorical noise, Gaussian continuous; positive-class definitions;
  three uniform bins) and reports variable-level F1 in place of the clean score.
- Greedy-vs-nd was investigated qualitatively
  (`docs/experiments/qualitative/greedy_vs_nd_qualitative_handoff.md`); a controlled quantitative
  comparison (QN-001) remains to confirm it.

## Outstanding actions

- Implement the QL2 parent-position swap to demonstrate order dependence.
- Give each presented result an interpretation and a conclusion; reason explicitly about
  DGP-expected vs actual learned rules.
- Define first-principles success metrics beyond parent membership (e.g. fold count for
  efficiency; expected-rule comparison for correctness).
- Find, clarify and improve Fabrizio's linear-with-noise DGP work.
- Be sceptical of AI-given explanations for experimental outcomes; verify them against the
  artefacts.
