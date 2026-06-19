# Milestone 1, Part 1: Parent-Position and Representation-Order Control

**Short name:** m1.1  
**Planned path:** `docs/research/milestone_plans/milestone1_part1_parent_position.md`  
**Status:** Design agreed; ready for implementation  
**Research stage:** RQ1 — unguided causal-role diagnostic  
**Primary baseline:** QL2 / QI-002  
**Target:** `x2`

## 1. Purpose

This investigation addresses an unresolved validity weakness in the existing QL2 parent-recovery results.

QL2 used complete, noiseless truth tables so that the true direct-parent predicate was the intended zero-error general rule for `x2`. This corrected some weaknesses of the earlier handcrafted tables, but it did not fully separate three possible explanations of a learnt rule:

1. the learner followed the variable occupying the direct-parent role;
2. the learner preferred a fixed variable identity or index, such as `x0`;
3. the learner preferred a fixed representation position, such as the first predictor presented to folding.

The distinction matters particularly for the categorical chain result, where the expected direct-parent rule referred to `x1` but the returned rule referred to `x0`.

m1.1 will therefore exchange the direct-parent and non-parent roles between `x0` and `x1`, while independently reversing their learner-visible representation order. The investigation is designed as a small transformation-based, or metamorphic, validity control.

The decision to be made is:

> Can the existing parent-recovery behaviour be interpreted as tracking the direct-parent role independently of variable identity and learner-visible predictor order?

## 2. Scope and claim boundary

The current implementation performs target-wise ABA Learning over a tabular representation and compares observable variables in learnt target rules with a known parent set. It does not implement the Russo-style Causal ABA machinery of `arr`, `noe`, or `indep` assumptions, d-separation, acyclicity constraints, or stable extensions interpreted as DAG hypotheses.

Accordingly, this investigation tests the validity of a local parent-rule recovery proxy. It does not test causal discovery or whole-graph recovery.

The investigation will:

- use clean, deterministic QL2-style fixtures;
- learn rules for target `x2`;
- compare returned rules with pre-specified expected rules;
- test parent-role equivariance;
- test representation-order invariance;
- distinguish learner outcomes from preprocessing, execution, and parsing errors.

The investigation will not:

- compare greedy and non-deterministic folding;
- introduce noise, finite-sample variation, or continuous data;
- test collider recovery;
- recover a complete graph;
- vary learning semantics, folding budgets, timeouts, or other hyperparameters;
- attribute a result to a search strategy by comparison with another strategy.

The ABA Learning strategy is held fixed because strategy comparison is the subject of Milestone 1, Part 2.

## 3. Precise research question

The primary research question is:

> Under complete, noiseless QL2-style target-mechanism tables, when the direct-parent and ancestor roles are exchanged between `x0` and `x1`, and learner-visible predictor order is independently reversed, does the learnt `x2` rule follow the variable occupying the direct-parent role?

This question decomposes into two required properties.

### 3.1 Parent-role equivariance

Let $\pi$ exchange the variable identities `x0` and `x1` throughout a fixture:

$$
\pi(x_0)=x_1,
\qquad
\pi(x_1)=x_0,
\qquad
\pi(x_2)=x_2.
$$

The transformation applies consistently to:

- graph labels and causal-role annotations;
- source-table column names and values;
- learner-visible feature predicates;
- expected rules;
- returned observable rule literals.

Let $\mathcal{L}(D,\rho)$ denote the target-rule set returned by the fixed learning pipeline for data $D$ under learner-visible predictor order $\rho$. Parent-role equivariance requires:

$$
\mathcal{L}(\pi D,\pi\rho)
\simeq
\pi\bigl(\mathcal{L}(D,\rho)\bigr),
$$

where $\simeq$ denotes equivalence after the rule normalisation defined in Section 9.

Intuitively, when the direct-parent role moves from `x1` to `x0`, the corresponding observable literal in the learnt rule should move from `x1` to `x0`.

### 3.2 Representation-order invariance

Let $\sigma$ reverse the order in which the two named predictors are presented to the learner, without renaming the variables or changing any values, examples, graph roles, or target labels:

$$
\sigma([x_0,x_1])=[x_1,x_0].
$$

Representation-order invariance requires:

$$
\mathcal{L}(D,\sigma\rho)
\simeq
\mathcal{L}(D,\rho).
$$

Intuitively, a rule should not change merely because the same named predictors are serialised in a different order.

### 3.3 Primary evidential standard

The strongest evidence for direct-parent tracking is obtained when:

1. the expected parent rule is returned in every cell;
2. the two $\pi$-comparisons satisfy parent-role equivariance;
3. the two $\sigma$-comparisons satisfy representation-order invariance;
4. the returned frameworks cover all positive examples and no negative examples;
5. all manipulations are verified in the actual learner input.

Rule-level comparisons are primary. Base-variable signatures are retained as a secondary diagnostic so that role tracking can be distinguished from structural differences between rules.

## 4. Motif selection

### 4.1 Primary motif: reversed chain pair

The initial and intended complete experiment uses two chain orientations.

The first is:

$$
G_{x_1\text{-parent}}:
\qquad
x_0 \rightarrow x_1 \rightarrow x_2,
$$

where:

- the direct parent of `x2` is `x1`;
- `x0` has the structural role of an upstream ancestor and non-parent.

The reversed chain is:

$$
G_{x_0\text{-parent}}:
\qquad
x_1 \rightarrow x_0 \rightarrow x_2,
$$

where:

- the direct parent of `x2` is `x0`;
- `x1` has the structural role of an upstream ancestor and non-parent.

This motif is selected because it:

- directly targets the unresolved categorical-chain discrepancy from QL2;
- gives `x2` exactly one direct parent;
- gives an unambiguous one-literal expected target rule;
- exchanges parent and ancestor roles between the two named variables;
- allows fixed-name, fixed-position, and parent-role behaviour to be separated.

### 4.2 Motifs excluded from the initial experiment

The fork is not required initially. It would duplicate the one-parent structure without addressing the existing categorical-chain discrepancy more directly.

The collider is excluded because its parent set is $\{x_0,x_1\}$. Exchanging `x0` and `x1` does not change the expected parent set, and collider fixtures introduce multi-parent rule structure and known solve/search complications that would obscure the parent-position question.

No additional motif will be added unless the eight planned cells remain genuinely ambiguous after the staged inspection in Section 12.

## 5. Factorial design

The experiment crosses two factors:

1. **Direct-parent identity**
   - `x1` is the direct parent;
   - `x0` is the direct parent.

2. **Learner-visible predictor order**
   - `[x0, x1]`;
   - `[x1, x0]`.

This gives four cells per encoding.

| Cell | Structural graph | Direct parent | Ancestor non-parent | Learner-visible predictor order | Expected selected variable |
|---|---|---|---|---|---|
| A | $x_0\rightarrow x_1\rightarrow x_2$ | `x1` | `x0` | `[x0, x1]` | `x1` |
| B | $x_0\rightarrow x_1\rightarrow x_2$ | `x1` | `x0` | `[x1, x0]` | `x1` |
| C | $x_1\rightarrow x_0\rightarrow x_2$ | `x0` | `x1` | `[x0, x1]` | `x0` |
| D | $x_1\rightarrow x_0\rightarrow x_2$ | `x0` | `x1` | `[x1, x0]` | `x0` |

The transformation square is:

$$
\begin{array}{ccc}
A & \xrightarrow{\sigma} & B\\
\downarrow\pi && \downarrow\pi\\
D & \xrightarrow{\sigma} & C
\end{array}
$$

This square gives four direct comparisons.

For representation-order invariance:

$$
\mathcal{L}(B)\simeq\mathcal{L}(A),
\qquad
\mathcal{L}(C)\simeq\mathcal{L}(D).
$$

For parent-role equivariance:

$$
\mathcal{L}(D)\simeq\pi\bigl(\mathcal{L}(A)\bigr),
\qquad
\mathcal{L}(C)\simeq\pi\bigl(\mathcal{L}(B)\bigr).
$$

The pairings have useful controlled interpretations:

- $A\leftrightarrow B$ changes parent position while holding the parent identity `x1` fixed;
- $D\leftrightarrow C$ changes parent position while holding the parent identity `x0` fixed;
- $A\leftrightarrow D$ changes parent identity while holding the parent in the second represented position;
- $B\leftrightarrow C$ changes parent identity while holding the parent in the first represented position.

This is why a four-cell design is necessary. A two-cell parent swap would leave variable identity and representation position coupled.

## 6. Encodings and experiment size

The factorial design will be run under two existing QL2 encodings:

1. binary;
2. categorical with three values.

The complete experiment therefore contains:

$$
2\text{ encodings}
\times
2\text{ parent identities}
\times
2\text{ predictor orders}
=
8\text{ cells}.
$$

The binary encoding acts as the clean positive control because QL2 previously returned the expected binary chain rule. The categorical-3 encoding is necessary because it contains the unresolved QL2 discrepancy.

Each encoding must be analysed separately before comparing their conclusions. A binary success and categorical failure is an encoding-dependent finding, not an inconclusive average.

A single run per deterministic cell is sufficient initially. Repeated identical runs are added only if the implementation is shown to contain run-time randomisation or repeated executions produce different solutions.

## 7. Graph, local mechanism, and data construction

### 7.1 Structural-role graph versus table construction

The two chain graphs define the causal roles being tested: direct parent and upstream ancestor.

The learning tables are deliberately not passive observational samples from the full chain distribution. Instead, they are exhaustive local target-mechanism controls in which both candidate predictors are varied factorially and `x2` is generated deterministically from its designated direct parent.

This distinction is essential.

The upstream chain edge supplies the structural role annotation. The exhaustive table deliberately removes the ancestor–parent association that would occur in a passive chain sample. This ensures that the non-parent cannot succeed merely by being correlated with the direct parent.

The experiment therefore tests whether the learner returns the known local parent rule under identity and representation transformations. It does not test whether a chain can be identified from observational conditional-independence information.

### 7.2 Binary construction

Let:

$$
\mathcal{V}_{\mathrm{bin}}=\{0,1\}.
$$

Enumerate every assignment:

$$
(x_0,x_1)\in\mathcal{V}_{\mathrm{bin}}^2.
$$

Each assignment is represented once (minimal complete factorial). The resulting table has:

$$
2^2=4
$$

rows.

The complete factorial once per assignment is the principled minimum: the true
parent is the unique zero-error one-literal separator and the $\pi$/$\sigma$ orbit
relations are independent of row multiplicity, so no per-row repeat is required.
The learner imposes no $|E^+|\ge 2$ requirement (no example-count guard in the
engine; QI-001 ran a 4-row factorial), and even at one row per assignment the
`x1`-parent binary cell has $|E^+|=2$. A replicate index $k$ may optionally be
reintroduced (`_REPEATS` in `handcrafted_m11.py`) but is not the default and does
not change the design.

For `x1`-parent cells:

$$
x_2 := x_1.
$$

For `x0`-parent cells:

$$
x_2 := x_0.
$$

The positive examples are the rows for which:

$$
x_2=1.
$$

The negative examples are the remaining rows.

### 7.3 Categorical-3 construction

Let:

$$
\mathcal{V}_{\mathrm{cat3}}=\{0,1,2\}.
$$

Enumerate every assignment:

$$
(x_0,x_1)\in\mathcal{V}_{\mathrm{cat3}}^2.
$$

Each assignment is represented once (minimal complete factorial). The resulting table has:

$$
3^2=9
$$

rows. As in the binary case, no per-assignment repeat is used; the `x1`-parent
cat3 cell has $|E^+|=3$.

For `x1`-parent cells:

$$
x_2 := x_1.
$$

For `x0`-parent cells:

$$
x_2 := x_0.
$$

The positive examples are the rows for which:

$$
x_2=2.
$$

The negative examples are the remaining rows.

### 7.4 Constructing the transformation orbit

For each encoding, the four fixtures should be derived from one canonical base table rather than generated independently.

Let a base row in cell A be indexed by:

$$
r_{a,b},
$$

with:

$$
x_0=a,
\qquad
x_1=b,
\qquad
x_2=b.
$$

Then:

- cell B is constructed by applying $\sigma$ to A: values and names remain unchanged, but predictor representation order is reversed;
- cell D is constructed by applying $\pi$ to A: `x0` and `x1` names and values are exchanged while `x2` and the sample identity remain fixed;
- cell C is constructed by applying $\sigma$ to D, equivalently by applying $\pi$ to B.

Constructing the fixtures through explicit transformations makes the intended relations testable by automated assertions.

### 7.5 Sample identity and row order

Sample identifiers must remain stable across the four related fixtures. The same base identifier $r_{a,b}$ should denote corresponding transformed rows.

Row order must also be held fixed. Row-order sensitivity is not a factor in m1.1.

### 7.6 ABA representation

The target remains `x2`, and the target column must be excluded from the background knowledge.

For binary predictors:

- value `1` is represented using the existing bare predicate convention, such as `x0(A)` or `x1(A)`;
- the expected target head remains `x2(A)`.

For categorical-3 predictors:

- values are represented using value-specific predicates such as `x0_val_0(A)`, `x0_val_1(A)`, and `x0_val_2(A)`;
- the complete predicate or fact group belonging to one variable must move together when representation order is reversed;
- value order within each variable must remain fixed as `0, 1, 2`.

The positive and negative examples must be identical across a $\sigma$-pair and must be exact $\pi$-transforms across a $\pi$-pair.

## 8. Controls held fixed

The following must remain fixed across all eight cells:

- target variable: `x2`;
- target exclusion from background knowledge;
- replicate count;
- sample identifiers;
- row order;
- target-class definition;
- binary and categorical encoding conventions;
- ABA Learning semantics and all resolved learner options;
- `folding_mode: nd`;
- folding budget or `folding_steps: 15`;
- primary learning timeout of 120 seconds;
- solver versions and execution environment;
- parser and metric implementation;
- returned-solution selection behaviour;
- execution order or isolated working directories sufficient to avoid shared scratch-file interference.

The experiment should inherit the resolved QI-002 configuration wherever possible. The implementation record must state the actual resolved learning mode and options rather than relying on defaults silently.

The only intended differences between paired cells are those induced by $\pi$ or $\sigma$.

## 9. Pre-specified expected rules

### 9.1 Strict expected target rules

The expected target rule depends only on the direct-parent identity and encoding. It does not depend on representation order.

| Encoding | Direct parent | Expected target-rule set |
|---|---|---|
| Binary | `x1` | $\{\,x_2(A)\leftarrow x_1(A)\,\}$ |
| Binary | `x0` | $\{\,x_2(A)\leftarrow x_0(A)\,\}$ |
| Categorical-3 | `x1` | $\{\,x_2(A)\leftarrow \texttt{x1\_val\_2}(A)\,\}$ |
| Categorical-3 | `x0` | $\{\,x_2(A)\leftarrow \texttt{x0\_val\_2}(A)\,\}$ |

By cell:

| Cell | Binary expected rule | Categorical-3 expected rule |
|---|---|---|
| A | $x_2(A)\leftarrow x_1(A)$ | $x_2(A)\leftarrow \texttt{x1\_val\_2}(A)$ |
| B | $x_2(A)\leftarrow x_1(A)$ | $x_2(A)\leftarrow \texttt{x1\_val\_2}(A)$ |
| C | $x_2(A)\leftarrow x_0(A)$ | $x_2(A)\leftarrow \texttt{x0\_val\_2}(A)$ |
| D | $x_2(A)\leftarrow x_0(A)$ | $x_2(A)\leftarrow \texttt{x0\_val\_2}(A)$ |

These rules are the unique intended one-literal, observable-feature separators among the candidate feature predicates. This does not imply uniqueness over the learner's complete hypothesis space: equality-specific rote rules and more complex ABA structures may also cover the examples.

### 9.2 Strict expected-rule match

A cell is a strict expected-rule match when:

- its normalised target-headed learnt rule set is the expected singleton rule;
- no non-parent observable predicate occurs in the target rule or its relevant exception structure;
- no row-specific equality literal is needed;
- no unnecessary additional target rule is present;
- positive examples are covered;
- negative examples are not covered.

The comparison concerns the learnt target-rule delta and any directly relevant assumptions or contrary rules. It does not require the whole returned ABA framework to be textually identical to a hand-written framework.

### 9.3 Rule normalisation

Before pairwise comparison, returned rules should be normalised conservatively.

Normalisation may:

- remove formatting and whitespace differences;
- alpha-rename logical variables;
- alpha-rename generated assumption identifiers consistently within a framework;
- canonicalise the order of conjunctive body literals;
- remove exact duplicate copies of a rule while recording the duplicate count separately;
- sort the normalised target-rule set for deterministic comparison.

Normalisation must preserve:

- observable predicate names;
- variable identity;
- categorical value suffixes;
- equality and sample-specific literals;
- rule boundaries;
- multiplicity before de-duplication;
- assumptions and their contrary links;
- exception-rule structure;
- whether several target rules rather than one rule were learnt.

For example, `x1_val_2(A)` must not be reduced to `x1` for the primary rule comparison. Base-variable stripping is used only for secondary parent-set metrics.

## 10. Outcome measures

### 10.1 Primary cell-level measure

Each cell receives one descriptive classification:

1. **Exact expected-rule match**
2. **Parent-aligned but structurally non-exact**
3. **Discrepant learnt rule**
4. **No returned solution**
5. **Invalid execution or artefact**

“Parent-aligned but structurally non-exact” requires correct coverage and no observable dependence on the non-parent in the target rule or its relevant support or exception chain. It is used only after the additional rule structure has been inspected.

“No returned solution” is intentionally descriptive. Its raw execution subtype must also be recorded, for example:

- learner-reported no solution;
- timeout;
- solver process failure;
- missing output.

An invalid execution or artefact is not treated as evidence about learning.

### 10.2 Primary transformation-level measures

For each encoding, report:

$$
\pi\text{-equivariance}
\in
\{\text{holds},\text{fails},\text{undefined}\},
$$

and:

$$
\sigma\text{-invariance}
\in
\{\text{holds},\text{fails},\text{undefined}\}.
$$

The verdicts are evaluated separately for each required edge of the transformation square.

At rule level:

- $\sigma$-invariance compares A with B and D with C;
- $\pi$-equivariance compares A with D and B with C after applying the corresponding renaming to the rule.

A comparison is:

- **holds** when both cells are valid and their normalised rules satisfy the expected relation;
- **fails** when both cells are valid but their normalised rules do not satisfy the relation;
- **undefined** when a required cell has no valid learnt result or the intended transformation was not successfully instantiated.

### 10.3 Secondary role-level comparison

A secondary comparison may be made using the observable base-variable signatures extracted from the target rules.

This records whether the correct named variable follows the parent role even when the full learnt rule structure changes. It must not replace the rule-level verdict.

The report should therefore distinguish statements such as:

- rule-level $\sigma$-invariance holds;
- role-level $\sigma$-invariance holds but rule-level invariance fails;
- both fail.

### 10.4 Secondary metrics

The following should be recorded for compatibility with earlier experiments and to enrich interpretation:

- recovered observable base-variable set;
- position of each recovered variable in the learner-visible order;
- variable-level precision;
- variable-level recall;
- variable-level $F_1$;
- Jaccard similarity;
- positive-example coverage;
- negative-example rejection;
- number of target-headed rules;
- number of observable feature literals;
- target-rule body length;
- number of row-specific equality literals;
- number of assumptions occurring in relevant target rules;
- number of relevant contrary or exception rules;
- returned-solution status;
- number of solutions reported, if exposed;
- runtime;
- folding tokens or step counts, only if already available without new instrumentation.

Parent $F_1$ is secondary. In this one-parent design, $F_1=1$ cannot distinguish the expected general rule from an exception-heavy rule, multiple redundant target rules, or a mixture of parent-based and rote clauses whose stripped variable signature happens to be correct.

No aggregate score should replace the paired comparisons. Counts such as “four of four exact cells” may be reported, but binary and categorical results must first be interpreted separately.

## 11. Validation of the representation-order manipulation

An apparent order-control experiment is invalid unless the intended order reaches the learner.

### 11.1 Required source-table checks

For every cell, record and assert:

- requested predictor order;
- actual table column order;
- stable sample identifier and row order;
- target column and target values;
- target exclusion setting.

For a $\sigma$-pair, assert that values, names, examples, and row identities are identical and that only predictor order differs.

For a $\pi$-pair, assert exact equivalence after exchanging `x0` and `x1`.

### 11.2 Required background-knowledge checks

Inspect the generated `*.bk.aba` files and record:

- the order in which `x0` and `x1` feature facts or predicate groups occur;
- whether the requested reversal is preserved;
- whether the categorical predicates for a variable move as one complete group;
- whether value order within a categorical variable remains fixed;
- whether a converter, parser, or sorting operation restores a canonical order;
- whether `x0` and `x1` receive symmetric representations apart from the intended role and order changes;
- confirmation that `x2` is absent from the predictor background knowledge.

The exact serialisation unit may be a predicate block, a feature-fact group, or row-wise feature order. The implementation must identify and document the order that is actually visible to folding rather than assume that DataFrame column order is sufficient.

### 11.3 Downstream order validation

If code inspection or an existing trace makes it inexpensive, confirm that the reordered representation affects the list or sequence from which foldable candidates are selected.

This deeper check is mandatory when:

- the generated BKs appear different but a later stage may sort them;
- a $\sigma$-pair produces different outputs;
- the claimed level of invariance would otherwise be ambiguous.

If both requested source orders produce an identical canonical learner input, then $\sigma$ has not been instantiated. The result cannot be interpreted as order invariance. The implementation must expose the smallest explicit learner-visible feature-order control and rerun the planned cells.

Canonicalisation itself should be recorded as a preprocessing finding, but it does not complete the order-sensitivity test.

## 12. Staged inspection protocol

Inspection should proceed from the smallest universal evidence core to discrepancy-specific evidence.

### Stage 0: Validate the fixtures and execution environment

Before learning, perform automated assertions for each encoding:

- binary row count is 4;
- categorical-3 row count is 9;
- every predictor assignment occurs exactly once;
- `x2` equals the designated parent in every row;
- A and B are exact $\sigma$-pairs;
- D and C are exact $\sigma$-pairs;
- A and D are exact $\pi$-pairs;
- B and C are exact $\pi$-pairs;
- row identifiers and replicate structure are preserved;
- positive and negative example sets are correct;
- the expected parent predicate covers every positive and no negative example;
- no predicate derived from the non-parent alone is a zero-error one-literal separator;
- `x2` is excluded from background features.

The expected-rule check should be described as uniqueness among intended observable one-literal feature rules, not uniqueness over all possible ABA hypotheses.

Run the existing learner and solver smoke checks once before the experiment. This prevents an unavailable `clingo` process or other environment failure from being misreported as a substantive no-solution result.

Validate the generated BK order as specified in Section 11 before interpreting any learning output.

### Stage 1: Inspect the minimum evidence for all eight cells

For every cell, inspect:

1. raw execution status;
2. raw target-headed rule block in `*.sol.aba`, when present;
3. normalised target-rule set;
4. pre-specified expected rule;
5. expected-versus-actual classification;
6. positive and negative coverage;
7. observable base-variable signature;
8. recovered predictor position;
9. agreement between raw rules and parsed metrics.

Because there are only eight cells, the raw target-rule block should be read for every cell.

Do not initially read every complete solver log, every background fact, or every assumption and contrary in the framework.

### Stage 2: Analyse the transformation square

For each encoding, evaluate:

#### Representation-order invariance

$$
A \xleftrightarrow{\sigma} B,
\qquad
D \xleftrightarrow{\sigma} C.
$$

#### Parent-role equivariance

$$
A \xleftrightarrow{\pi} D,
\qquad
B \xleftrightarrow{\pi} C.
$$

Record both:

- strict rule-level verdict;
- secondary observable-role verdict.

If all four cells return the strict expected rules with valid coverage and all four square edges satisfy their expected relation, the primary question has been answered for that encoding. No full dossier or complete trace inspection is required.

### Stage 3: Triggered inspection

Deeper inspection is performed only for the cells involved in a failed or undefined comparison.

#### Case A: Parent-aligned but structurally non-exact output

Inspect:

- all target-headed rules;
- assumptions occurring in those rules;
- the contraries of those assumptions;
- auxiliary rules directly supporting or defeating those assumptions;
- row-specific equality literals;
- whether the additional structure changes coverage;
- whether any non-parent predicate occurs in the relevant dependency or exception chain.

The purpose is to determine whether the result is a harmless structural elaboration, a meaningful exception-based rule, or a disguised reliance on the non-parent.

#### Case B: A $\sigma$-comparison fails

Inspect, in order:

1. paired source tables;
2. requested and actual table order;
3. generated BK serialisation;
4. downstream sorting or canonicalisation;
5. raw target rules;
6. folding candidate order or transformation trace, if exposed.

Only after the representation manipulation is verified should the result be described as order-sensitive behaviour.

A failure supports the statement that the returned result is sensitive to the tested representation order under the fixed non-deterministic configuration. It does not by itself establish that non-deterministic folding is worse than another strategy.

#### Case C: A $\pi$-comparison fails

Inspect, in order:

1. exact fixture equivalence under $\pi$;
2. target and example generation;
3. symmetry of the generated `x0` and `x1` representations;
4. expected-rule coverage in both cells;
5. raw target rules;
6. transformation trace, if required.

If these checks pass and a named variable persists when its causal role changes, the result is evidence consistent with a fixed variable-name, index, or lexical preference. The precise internal mechanism should be named only when code or trace evidence identifies it.

#### Case D: No returned solution

Inspect, in order:

1. direct table-level coverage of the pre-specified expected rule;
2. whether the expected rule is expressible in the generated predicate vocabulary;
3. where possible, an entailment check on a diagnostic copy of the framework with the expected rule supplied explicitly;
4. target predicate and example configuration;
5. constant and domain generation;
6. background-knowledge syntax;
7. target exclusion;
8. process exit status;
9. timeout status;
10. folding budget;
11. `prolog.stdout` and stderr;
12. clingo logs.

The result should then be classified more precisely as one of:

- learner-reported no solution under the configured search;
- timeout;
- solver or environment failure;
- malformed input;
- representational incompatibility;
- unresolved.

The existence of a correct table-level rule does not prove that the configured learner can reach it. Conversely, a learner no-solution message does not prove that no parent-aligned rule exists.

#### Case E: Raw-rule and metric disagreement

Inspect the raw solution and parser immediately.

A parser, normalisation, or metric discrepancy is an implementation-validity issue. The cell must not be used in the $\pi$- or $\sigma$-assessment until the discrepancy is resolved or the cell is marked invalid.

#### Case F: Invalid execution or artefact

Localise the error and record it separately from learning behaviour.

Examples include:

- malformed or missing BK;
- target leakage;
- incorrect target examples;
- incomplete solution file;
- unknown constant caused by encoding;
- shared scratch-file interference;
- parser failure;
- inconsistent metadata.

Repair and rerun the cell when the correction is local and necessary to instantiate the planned experiment. Do not reinterpret an implementation error as search failure or parent-recovery failure.

## 13. Diagnostic comparisons and interpretation guardrails

This plan does not assign an exhaustive mechanistic interpretation to every possible output pattern. Unexpected results will be interpreted case by case after the smallest relevant artefacts have been inspected.

The investigation separates observations from explanations.

### 13.1 Direct-parent tracking

Strong evidence for direct-parent tracking requires:

- valid $\pi$-equivariance;
- valid $\sigma$-invariance;
- expected parent-only rules;
- correct positive and negative coverage.

If only observable base-variable signatures satisfy these properties while full rule structures differ, the result is weaker role-level evidence and must be reported as such.

### 13.2 Variable-name or index preference

A result may be described as consistent with a fixed-name, index, or lexical preference when:

- the same named variable persists across a valid $\pi$-comparison;
- the causal role has moved;
- parent position is controlled;
- the fixture and encoding are symmetric;
- no implementation error explains the persistence.

The experiment alone should not claim the exact source of the preference unless a trace or code inspection identifies it.

### 13.3 Representation-order artefact

A result may be described as representation-order sensitive when:

- a valid $\sigma$-pair differs;
- variable names, values, examples, and causal roles are fixed;
- the requested order is verified in the learner-visible representation;
- no parser or execution error explains the difference.

The conclusion is restricted to the tested serialisation or candidate order.

### 13.4 Search-strategy effect

m1.1 cannot establish a comparative search-strategy effect because the strategy is fixed.

Permitted statements include:

- the fixed non-deterministic configuration returned different rules under the tested representation orders;
- the configured search did not return a verified available expected rule;
- the transformation trace followed different paths after reordering.

Statements that greedy or another strategy would avoid the problem belong to Part 2 and require direct comparison.

### 13.5 No-solution behaviour

“No returned solution” is not interpreted until environment, input, expected-rule coverage, timeout, and solver evidence have been checked.

A verified available expected rule combined with a valid no-solution result supports a bounded conclusion about the configured learner or search. It does not support a conclusion that the parent mechanism is absent from the data.

### 13.6 Implementation error

Implementation errors are excluded from substantive claims about ABA Learning. They remain important engineering findings and should be documented, but they make the affected transformation comparison undefined until repaired.

### 13.7 Multiple solutions

This investigation evaluates the solution returned by the fixed current pipeline. It does not claim that every possible ABA Learning solution has the same invariance properties.

If the engine reports or exposes multiple valid solutions, record this. A difference caused by first-solution selection should be discussed as returned-solution sensitivity rather than as proof that no equivariant solution exists.

## 14. Smallest experiment and stopping rule

The planned eight-cell matrix is the smallest principled project-level experiment.

A four-cell matrix under one encoding is logically sufficient to separate parent identity from representation position. However:

- binary provides the existing clean positive control;
- categorical-3 contains the unresolved QL2 discrepancy;
- comparing the two encodings determines whether the result is encoding-dependent.

Therefore, four categorical cells alone would be too narrow, while a larger motif or parameter grid is unnecessary.

The initial experiment must not add:

- fork cells;
- collider cells;
- continuous data;
- noise;
- sample-size variation;
- random seeds;
- row-order permutations;
- greedy folding;
- hyperparameter sweeps;
- alternative semantics.

The investigation stops after the eight cells when the result supports a clear bounded classification, including an encoding-dependent classification.

A reversed-fork control may be considered only when:

- the complete chain matrix remains genuinely ambiguous;
- the ambiguity survives raw-artifact inspection;
- the fork control would distinguish two remaining explanations;
- the additional cells are specified before they are run.

A fork is not added merely to increase the experiment count.

## 15. Completion criteria

m1.1 is complete when all of the following hold:

1. The expected rules are recorded before execution.
2. The eight fixtures are generated through verified $\pi$ and $\sigma$ transformations.
3. The binary and categorical table assertions pass.
4. The intended predictor order is verified in the learner-visible representation.
5. All eight primary cells have complete raw artefacts or a precisely classified invalid outcome.
6. Every valid cell has a raw-rule quotation, normalised rule, coverage result, and expected-rule classification.
7. Every required edge of the transformation square has a rule-level and role-level verdict.
8. Failed or undefined comparisons have received only the triggered inspection required to interpret them.
9. Implementation errors are separated from learner outcomes.
10. Binary and categorical conclusions are stated separately before any overall synthesis.
11. A bounded conclusion answers whether the returned rules track the direct-parent role independently of the tested variable identities and representation orders.
12. No claim of causal discovery or complete graph recovery is made.
13. Additional motifs or grids have not been run unless the stopping rule justified them.
14. The findings are written into a concise `.tex` document covering design, results, interpretation, limitations, and conclusion.

Completion does not require a positive result. A valid finding of name sensitivity, order sensitivity, verified no-solution behaviour, or encoding dependence completes the investigation if the evidence is sufficient.

## 16. Success criteria

### 16.1 Strongest positive result

The strongest result is obtained when all eight cells:

- return the strict expected singleton rule;
- cover every positive and no negative example;
- contain no non-parent observable predicate;
- satisfy every $\pi$-equivariance comparison;
- satisfy every $\sigma$-invariance comparison;
- have no order-dependent solve status.

This supports direct-parent tracking under the tested binary and categorical truth-table fixtures.

### 16.2 Weaker positive result

A weaker result occurs when:

- the observable rule dependence tracks the direct parent;
- role-level $\pi$-equivariance and $\sigma$-invariance hold;
- coverage is correct;
- but full rule structure differs because of additional assumptions, exceptions, or redundant rules.

This must be described as role-level parent tracking rather than strict expected-rule recovery.

### 16.3 Mixed result

Binary and categorical outcomes may differ. For example:

- binary may satisfy both properties;
- categorical-3 may exhibit name sensitivity, order sensitivity, or structural non-invariance.

Such a result is complete and informative. It should be reported as encoding-dependent rather than averaged into a single parent $F_1$.

### 16.4 Inconclusive result

The investigation is inconclusive only when the research question cannot be adjudicated after the required validity checks, for example because:

- learner-visible order cannot be manipulated;
- most required cells remain invalid for unresolved implementation reasons;
- no returned solutions prevent both paired comparisons and cannot be classified;
- the normalisation or parser cannot support a trustworthy rule comparison.

An inconclusive result must state exactly which comparison remains undefined and why.

## 17. Required artefacts

Each cell should retain:

- source table or Parquet file;
- fixture metadata;
- sample identifiers;
- parent identity;
- requested predictor order;
- observed table order;
- generated positive examples;
- generated negative examples;
- generated `*.bk.aba`;
- raw `*.sol.aba`, when present;
- normalised target-rule representation;
- `metrics.json`;
- run log;
- `prolog.stdout`;
- stderr;
- clingo logs for no-solution or error cells;
- validation assertion results;
- resolved learner configuration.

The experiment must use a new output directory and must not overwrite QI-002 artefacts.

A compact validation manifest should record, per cell:

| Encoding | Cell | Parent | Requested order | Table order | BK order | Target excluded | Fixture checks |
|---|---|---|---|---|---|---|---|

## 18. Results tables

### 18.1 Cell-level results

| Encoding | Cell | Parent | Predictor order | Expected rule | Raw/normalised actual rule | Selected names | Selected positions | Coverage | Classification |
|---|---|---|---|---|---|---|---|---|---|
| Binary | A | `x1` | `[x0,x1]` | `x2(A) <- x1(A)` | — | — | — | — | — |
| Binary | B | `x1` | `[x1,x0]` | `x2(A) <- x1(A)` | — | — | — | — | — |
| Binary | C | `x0` | `[x0,x1]` | `x2(A) <- x0(A)` | — | — | — | — | — |
| Binary | D | `x0` | `[x1,x0]` | `x2(A) <- x0(A)` | — | — | — | — | — |
| Cat3 | A | `x1` | `[x0,x1]` | `x2(A) <- x1_val_2(A)` | — | — | — | — | — |
| Cat3 | B | `x1` | `[x1,x0]` | `x2(A) <- x1_val_2(A)` | — | — | — | — | — |
| Cat3 | C | `x0` | `[x0,x1]` | `x2(A) <- x0_val_2(A)` | — | — | — | — | — |
| Cat3 | D | `x0` | `[x1,x0]` | `x2(A) <- x0_val_2(A)` | — | — | — | — | — |

### 18.2 Transformation-level results

| Encoding | Property | Comparison | Expected relation | Rule-level verdict | Role-level verdict | Evidence note |
|---|---|---|---|---|---|---|
| Binary | $\sigma$-invariance | A vs B | $\mathcal{L}(A)\simeq\mathcal{L}(B)$ | — | — | — |
| Binary | $\sigma$-invariance | D vs C | $\mathcal{L}(D)\simeq\mathcal{L}(C)$ | — | — | — |
| Binary | $\pi$-equivariance | A vs D | $\mathcal{L}(D)\simeq\pi(\mathcal{L}(A))$ | — | — | — |
| Binary | $\pi$-equivariance | B vs C | $\mathcal{L}(C)\simeq\pi(\mathcal{L}(B))$ | — | — | — |
| Cat3 | $\sigma$-invariance | A vs B | $\mathcal{L}(A)\simeq\mathcal{L}(B)$ | — | — | — |
| Cat3 | $\sigma$-invariance | D vs C | $\mathcal{L}(D)\simeq\mathcal{L}(C)$ | — | — | — |
| Cat3 | $\pi$-equivariance | A vs D | $\mathcal{L}(D)\simeq\pi(\mathcal{L}(A))$ | — | — | — |
| Cat3 | $\pi$-equivariance | B vs C | $\mathcal{L}(C)\simeq\pi(\mathcal{L}(B))$ | — | — | — |

## 19. Permissible conclusion form

A strong positive conclusion should be bounded approximately as follows:

> Under the tested complete, noiseless QL2-style chain controls and fixed non-deterministic ABA Learning configuration, the returned target rules tracked the variable occupying the direct-parent role across exchanges of `x0` and `x1` and were invariant to the tested learner-visible predictor order. This provides evidence against a fixed `x0` or tested representation-position artefact in these fixtures. It does not establish causal discovery.

A role-level but structurally mixed conclusion should distinguish the two levels:

> The observable variables in the returned rules tracked the direct-parent role and were invariant to the tested predictor order, but the full learnt rule structures were not invariant. The result therefore supports role-level parent tracking under these fixtures, not strict expected-rule recovery.

A negative conclusion should describe the observed relation before proposing an explanation:

> Under the tested categorical-3 fixtures, exchanging the direct-parent role did not produce the corresponding exchange in the returned target rule.

or:

> Reversing learner-visible predictor order changed the returned rule while variable names, target labels, and table semantics were fixed.

Mechanistic language such as “name bias”, “position bias”, or “search-path effect” should be used only at the strength supported by the inspected artefacts.

## 20. Final decision rule

The investigation answers its central question positively for an encoding only when both parent-role equivariance and representation-order invariance hold for valid returned rules, with correct coverage and parent-aligned observable structure.

If either property fails, the result must be reported as the specific failed transformation relation and then interpreted using the staged evidence.

The expected-vs-actual learnt rule comparison remains the primary evidence throughout. Parent-set $F_1$ is supporting information only.