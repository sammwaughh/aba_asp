# Project Plan

> Markdown mirror of `docs/report/manuscript/project_plan.tex`, for ChatGPT Project context.
> The `.tex` file remains the authoritative source; this mirror is not for compilation. Wording is
> preserved; LaTeX headings are converted to Markdown headings, mathematical notation is kept as
> inline LaTeX, `\cite{key}` is rendered as `[cite: key]` (references not resolved), and the LaTeX
> schedule table is rendered as a Markdown table with all cell values preserved.

> **Live-status note (8 August 2026):** this chapter is an earlier project-plan draft, not
> the current Milestone 2 approach. Its bridge architecture, staged milestones, outputs,
> comparisons, and week allocations are historical proposals. The live M2 approach commits
> only to intimate study of the argumentative causal discovery paper and ArgCausalDisco
> code, followed by trying and testing possible integrations with ABA Learning; their form
> and sequence remain open. See
> `docs/research/milestone_plans/milestone2/README.md`.

## Purpose and Strategy

The remaining project investigates how ABA Learning and Causal ABA can be combined to learn causal relationships from data in an argumentative form. The experimentation so far provides a useful starting point: the current `aba_asp/causal` pipeline can learn target-wise ABA rules from controlled synthetic data, and the variables appearing in learnt rule bodies can be compared with known parent sets. However, those experiments only measure a proxy for causality. Learnt rules may recover a direct parent, but they may also recover an ancestor, a correlated proxy, a partial parent set, or no usable rule at all.

The next phase therefore treats parent-set recovery as groundwork, not as the main project. Its role is to characterise what unguided ABA Learning does before causal guidance is added. The main body of the remaining work asks whether Causal ABA ideas can guide, constrain or shape ABA Learning so that learnt rules become more causally meaningful.

The plan deliberately leaves some design choices open. At this stage it would be premature to commit to one exact integration. Instead, the project will investigate plausible ways of using causal information as background guidance for ABA Learning. Causal ABA supplies graph-level notions such as candidate arrows, no-edge claims, conditional-independence evidence, acyclicity and d-separation [cite: russo2024argumentative]. ABA Learning supplies transformation-based learning of ABA rules from examples [cite: proietti2022learning, de2023aba, de2024learning]. The research question is whether causal information can guide ABA Learning in a tractable implementation, what empirical benefit this provides, and how the resulting bridge compares with established causal-discovery methods.

## Research Questions

**RQ1** asks when unguided ABA Learning recovers direct-parent-like variables in learnt target rules, rather than ancestors, descendants, siblings, correlated non-parents or representation artefacts. **RQ2** asks whether Causal ABA-style evidence and graph constraints can guide ABA Learning. **RQ3** asks how the resulting causally guided ABA Learning bridge compares with representative state-of-the-art causal-discovery methods on canonical examples, and whether the comparison reveals a publishable contribution in interpretability, robustness, causal alignment or argumentative explanation.

RQ1 is the short diagnostic stage. RQ2 is the main project question because it tests whether Causal ABA can inform the background or search space of ABA Learning. RQ3 tests whether the resulting bridge should be understood only as an internal proof of concept, or as a method that can be meaningfully compared with existing approaches in the causal-discovery literature.

## Milestones

### Milestone 1: Parent-Set Diagnostic, Weeks 1--2

The first two weeks will close the initial parent-set investigation. For a target \(x_t\), let \(P_t\) be the true parent set and let \(R_t\) be the set of base variables recovered from non-trivial learnt rules for \(x_t\). The diagnostic will classify outcomes as exact recovery \((R_t=P_t)\), parent superset, parent subset, proxy recovery, no-solution, error or timeout. This will make the current results easier to discuss and will prevent parent recovery from becoming an open-ended subproject.

This milestone will include the immediate corrections and checks suggested by the existing experiments: parent-position controls, inspection of collider failures, a compact comparison between non-deterministic and greedy folding, and a small noise or hyperparameter check. Greedy learning is relevant because ABA Learning search can be highly nondeterministic, and recent work proposes greedy folding as one way to control this search space [cite: de2025greedy]. The metrics will include parent precision, recall and \(F_1\), proxy false-positive rate, solve rate, rule complexity and runtime.

The output will be a concise diagnostic conclusion: when does unguided ABA Learning appear to learn parent-like rules, what kinds of causal mistakes does it make, and which failures motivate Causal ABA guidance? This milestone should be completed by the end of Week~2. Wherever the investigation is by that point, its conclusions should inform how Causal ABA can be integrated intelligently.

### Milestone 2: Bridge Between ABA Learning and Causal ABA, Weeks 3--4

This milestone will design the bridge in the main project direction: Causal ABA-style information guiding ABA Learning. Causal information may shape the background knowledge, exclude implausible causes, prioritise possible parents, encode graph-informed constraints, or provide conditional-independence guidance. These are design options rather than fixed commitments. The implementation will start with the simplest version that can answer the research questions and will only become more detailed if the early results justify it.

The design will also prepare for later comparison with other causal-discovery methods. This requires specifying what the bridge outputs, how those outputs are converted into parent-set or graph-level predictions, and which metrics allow fair comparison with external baselines. The aim is to avoid evaluating the bridge only against itself.

The output will be a short formal design section identifying the variables, assumptions, evidence sources, guidance mechanisms and evaluation criteria used by the combined system. This design will determine which integration route is implemented in the following milestones.

### Milestone 3: Causal ABA-Guided ABA Learning, Weeks 5--6

The third milestone investigates the main proposed direction: using Causal ABA as background guidance for ABA Learning. The central hypothesis is that unguided ABA Learning may learn variables that are predictive but not directly causal, while causal guidance may reduce such proxy rules or make the learnt rules easier to interpret.

Several forms of guidance are plausible. A weak form may restrict the learner to variables adjacent to the target in some causal graph hypothesis. A stronger form may prioritise variables that are possible directed parents. Other forms may use conditional-independence evidence to demote candidate direct causes, or use oracle parent information only as an upper bound. The project will not assume in advance which form is best. The practical aim is to compare unguided ABA Learning with one or more causal-guided variants that are feasible within the implementation.

Evaluation will focus on whether guidance changes the learnt rules in the intended causal direction. Beyond parent recovery, rule-body length, assumptions introduced, runtime and stability across seeds or noise are all important metrics. Crucially, more nuanced bespoke metrics should be constructed for specific tests to judge whether causality is being learned. Parent recovery is only a proxy for this.

### Milestone 4: Scaling and Comparator Setup, Weeks 7--8

The fourth milestone will scale the causal-guided ABA Learning investigation beyond the initial three-node motifs and their composite structures. Milestone~3 tests whether causal guidance can improve ABA Learning in minimal settings where the relevant causal structure is easy to inspect. Milestone~4 asks whether the same direction remains plausible when the learner faces richer structures, more candidate variables and less isolated causal patterns.

The examples will be chosen to extend the motif results without becoming an uncontrolled benchmark study. Candidate families include embedded chains, embedded colliders, common-cause structures with downstream effects, two-parent mechanisms, diamond-shaped graphs and small canonical synthetic DAGs. These examples test different difficulties: indirect association, proxy variables, multi-parent recovery, irrelevant variables, and cases where local associations do not determine direct causation. The exact suite will be finalised after Milestone~3, so that the scaling stage builds on the guidance mechanisms that are actually feasible.

This milestone will also prepare the external comparison required for RQ3. The comparator set should be representative rather than exhaustive, and may include established constraint-based, score-based or argumentation/ASP-based causal-discovery methods discussed in the literature review, depending on what can be run fairly within the project environment. The comparison protocol will specify shared datasets, graph targets, metrics, sample sizes, noise conditions and any restrictions needed to make the comparison meaningful.

For each selected example, I will compare unguided ABA Learning with the strongest feasible causal-guided variants from Milestone~3. Where feasible, I will also run the selected external baselines on the same examples. The aim is to test whether the causal-guidance ideas developed survive beyond hand-inspected motifs and whether they have a distinctive advantage, such as interpretability, explicit argumentative structure, or robustness to conflicting evidence.

The main outputs will be a small canonical-example suite, a frozen evaluation protocol for Milestone~5, a selected comparator set, and preliminary results showing how guided and unguided ABA Learning compare on larger structures. By the end of Week~8, the project should have moved from motif-level evidence to a broader exploratory comparison. This will set up the final evaluation stage by identifying the examples, guidance variants, baseline methods, metrics and failure categories that should be reported systematically.

### Milestone 5: Evaluation and Full Draft, Weeks 9--10

Weeks~9--10 are reserved for evaluation and report consolidation. The evaluation will answer the three research questions directly. For RQ1, it will summarise the parent-set diagnostic. For RQ2, it will compare unguided and guided learning. For RQ3, it will compare the resulting causally guided ABA Learning bridge with selected external causal-discovery baselines on the canonical examples introduced in Milestone~4.

This stage will also include ablations where feasible: for example, guidance strength, noise level, folding strategy, sample size, or oracle versus empirical causal evidence. The report will record cases where guidance fails, creates ambiguity or reduces recall. This is important because the objective of the project is ultimately argumentative causal learning under uncertainty, not a deterministic pipeline that always returns the true graph. The comparison with external methods will be interpreted cautiously: a publishable contribution may come from competitive performance, but it may also come from clearer explanation, better handling of conflicting evidence, or a well-characterised niche where causally guided ABA Learning behaves differently from standard baselines.

The goal by the end of Week~10 is a complete supervisor-reviewable draft, including results, limitations, reproducibility notes and GenAI-use disclosure. No major experiment should be left dependent on post-break work. I will then take a 1-week holiday. This will give time for my supervisor to thoroughly critique my full draft in preparation for Weeks 12 and 13.

### Milestone 6: Finalisation and Presentation, Weeks 12--13

A non-working break is planned for 24--31 August. The two working weeks after the break will be used for supervisor-feedback edits, final report polishing and preparation of the final presentation. The presentation will focus on the research story mirroring the report. Presenting this work clearly requires a deliberately designed presentation and the two weeks to apply supervisor edits and prepare this presentation is justified.

## Schedule

*Table: Fourteen-calendar-week schedule. Week~11 is the 24--31 August family holiday.*

| Week | Week commencing | Focus | Main output |
|---|---|---|---|
| 1 | 15 June 2026 | Parent-set diagnostic I | Correct parent-position controls, inspect key failures and consolidate existing artefacts. |
| 2 | 22 June 2026 | Parent-set diagnostic II | Run compact strategy/noise checks and close the diagnostic baseline. |
| 3 | 29 June 2026 | Bridge design I | Define how Causal ABA-style information can guide ABA Learning. |
| 4 | 6 July 2026 | Bridge design II | Select the first feasible guidance route and define comparable outputs and metrics. |
| 5 | 13 July 2026 | Guided learning I | Implement or configure a causal-guided ABA Learning variant. |
| 6 | 20 July 2026 | Guided learning II | Compare guided and unguided learning on small motifs. |
| 7 | 27 July 2026 | Scaling and comparators I | Select canonical examples and candidate external baselines. |
| 8 | 3 August 2026 | Scaling and comparators II | Freeze the example suite, comparator set and final evaluation protocol. |
| 9 | 10 August 2026 | Evaluation I | Run final ablations and baseline comparisons; freeze result tables and figures. |
| 10 | 17 August 2026 | Evaluation II | Complete a supervisor-reviewable full draft before the break. |
| 11 | 24 August 2026 | Family holiday | Non-working week; no critical dependency scheduled. |
| 12 | 31 August 2026 | Feedback and presentation I | Apply supervisor feedback and prepare presentation structure. |
| 13 | 7 September 2026 | Final polish | Final report edit, claim audit, formatting and presentation rehearsal. |
| 14 | 14 September 2026 | Presentation week | Deliver the final presentation and complete any final report adjustments required after feedback. |

## Success Criteria and Risks

The minimum successful outcome is a rigorous account of unguided ABA Learning on causal motifs, plus a clear design and small demonstration of how Causal ABA concepts can guide ABA Learning. The target outcome is stronger: evidence that some form of Causal ABA guidance improves causal alignment, interpretability, robustness or efficiency in controlled settings. The stretch outcome is a publishable-style comparison showing that the causally guided ABA Learning bridge has a distinctive advantage or clearly characterised niche relative to representative causal-discovery baselines.

The main risk is that the causal guidance mechanism is too difficult to implement cleanly within the remaining time. To mitigate I'll strive to keep the bridge small, explicit and motif-driven at first, then scale only the most credible variant to canonical examples. A second risk is that the comparison with external methods is too limited to support strong claims. It should be described as a representative comparison (rather than a comprehensive benchmark) focusing on well-defined metrics and carefully selected examples. A third risk is that causal guidance does not improve learning. This would still be reportable if the evaluation explains why: the guidance may be statistically unreliable, mismatched to the ABA Learning representation, or useful only under specific structural conditions.

The intended final contribution is a scoped investigation of causally guided ABA Learning: an empirical account of what ABA Learning can learn from causal data, a principled exploration of whether Causal ABA-style background information can make that learning more causally meaningful, and a comparison with representative causal-discovery methods to assess whether the bridge offers a credible research contribution.
