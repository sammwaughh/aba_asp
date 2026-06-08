# Paper summary: De Angelis, Proietti, Toni 2025 — Greedy ABA Learning for Case-Based Reasoning

## Role in this project

This paper is the main source for search control in ABA Learning.

It introduces Greedy ABA Learning, a deterministic variant of ABA Learning for case-based reasoning. Its central motivation is that ordinary ABA Learning can be highly nondeterministic: Rote Learning, Folding and Assumption Introduction may each be applicable in many alternative ways, producing a very large search space.

The paper’s role in this project is not that the project is about case-based reasoning. Its relevance is methodological:

text Greedy ABA Learning shows that ABA Learning may need domain-specific restrictions on transformation-rule application. 

For Causal ABA Learning, causal graph structure may play an analogous role to casebase structure. Possible sources of causal guidance include:

- acyclicity;
- causal ordering;
- graph compatibility;
- d-separation;
- known absence of edges;
- conditional-independence/dependence evidence;
- restrictions on which rules may be transformed;
- restrictions on when assumptions may be introduced.

Use this paper as the main reference for:

- why unconstrained ABA Learning search is difficult;
- how transformation-rule search can be made deterministic in a structured domain;
- the order “generalise first, introduce attacks later”;
- coherent vs incoherent casebases;
- using grounded reasoning for coherent cases;
- using stable/brave reasoning for incoherent cases;
- the relationship between Greedy ABA Learning and AA-CBR.

This paper does not address causal discovery. It does not define Causal ABA, DAGs, conditional independence, d-separation, or ABA-PC. Its relevance is to the second direction of this project: using causal structure to guide ABA Learning.

## Core definitions

### ABA Learning

The paper treats ABA Learning as a form of logic-based learning that produces symbolic representations in the form of ABA frameworks from:

- an initial ABA framework, representing background knowledge;
- positive examples;
- negative examples.

ABA Learning applies transformation rules to progressively refine the initial ABA framework, guided by examples.

The learnt ABA framework can naturally encode:

- conflicts created by generalising examples;
- resolution of these conflicts using assumptions, contraries and attacks.

### Search-control problem

Ordinary ABA Learning is highly nondeterministic because transformation rules may be applicable in many alternative ways.

Examples:

- Rote Learning can be applied to any positive example.
- Folding can be applied to any two rules whose premises match.
- Assumption Introduction can be applied to many possible rules.
- Different transformation orders can produce different frameworks.

The paper identifies control of this nondeterminism as a major issue for effective ABA Learning.

### Greedy ABA Learning

Greedy ABA Learning is a deterministic variant of ABA Learning for case-based reasoning.

It applies transformation rules in a fixed, domain-specific order:

1. exhaustively generalise examples using Rote Learning and Folding;
2. only afterwards introduce attacks using Assumption Introduction where needed.

This greedy structure reduces the search space by removing many choices about which transformation to apply next.

### Casebase

The paper focuses on categorical casebases.

A casebase contains cases, each with:

- a set of binary features;
- a binary label.

A case can be represented as:

text case c has features F case c has label delta or not-delta 

The paper considers a new case N whose outcome is to be predicted.

### Coherent casebase

A casebase is coherent when no two cases have the same features but different labels.

In a coherent casebase, there are no direct conflicts between cases with identical feature descriptions.

For coherent casebases, Greedy ABA Learning corresponds exactly with AA-CBR, another argumentation-based method for case-based reasoning.

### Incoherent casebase

A casebase is incoherent when there exist two cases with the same features but different labels.

Incoherent casebases create conflicts that cannot be resolved by a unique grounded outcome in the same way.

The paper extends Greedy ABA Learning to incoherent casebases using credulous/brave reasoning under stable extensions.

### Background ABA framework for casebases

In the case-based setting, the background knowledge is a simple ABA framework consisting mainly of facts.

These facts represent:

- features of cases;
- default information;
- case identifiers;
- potentially labels or example information depending on the construction.

The simplicity of the background framework is important: Greedy ABA Learning is tailored to casebases, not arbitrary ABA frameworks.

### Positive and negative examples

For a casebase and target new case, the learning problem generates positive and negative examples associated with the intended outcome.

In the coherent setting, the learning problem is constructed so that examples guide learning towards a prediction for the new case.

In the incoherent setting, conflicts may produce multiple stable extensions, and prediction is made using a brave/selected-extension condition.

### Grounded extension

For coherent casebases, Greedy ABA Learning uses grounded reasoning.

The grounded extension is unique. This supports deterministic prediction in coherent settings.

### Stable extension

For incoherent casebases, the learnt ABA framework may admit several stable extensions.

Prediction can then use a selected stable extension satisfying the required positive and negative examples.

The paper defines outcome prediction for a new case using existence of a stable extension Delta such that:

- all positive examples and the default for the new case are covered in Delta;
- no negative examples are covered in Delta.

### AA-CBR

AA-CBR is an abstract-argumentation approach to case-based reasoning.

The paper proves that, for coherent casebases, Greedy ABA Learning corresponds exactly with AA-CBR.

This shows that Greedy ABA Learning generalises an existing argumentation-based CBR method while using ABA rather than abstract argumentation.

## Implementation-relevant concepts

### Greedy transformation order

The most implementation-relevant feature is the deterministic transformation order:

text 1. Apply Rote Learning. 2. Apply Folding exhaustively to generalise examples. 3. Apply Assumption Introduction only after generalisation, where attacks are needed. 

For this project, the key methodological lesson is that transformation-rule application can be constrained by domain structure.

### Rote Learning in casebases

Rote Learning introduces example-specific rules corresponding to cases.

These rules initially memorise individual cases.

In a simplified implementation, each case can generate rules tied to a case identifier or feature set.

### Folding in casebases

Folding generalises from individual cases to feature-based rules.

The goal is to derive general rules from case facts and feature predicates.

Example pattern:

text label(X) <- feature1(X), feature2(X) 

rather than isolated rules for individual cases.

Folding is applied exhaustively before attacks are introduced.

### Assumption Introduction in Greedy ABA Learning

Assumption Introduction is applied after generalisation to introduce defeasibility and handle conflicts.

A rule such as:

text label(X) <- feature(X) 

may become:

text label(X) <- feature(X), alpha(X) 

where alpha(X) is a new assumption.

A contrary rule can then attack alpha(X) when an exception condition holds.

This allows the learnt framework to encode conflicts caused by overgeneralisation.

### Exhaustive generalisation first

A key implementation principle:

text Do not introduce assumptions/attacks before attempting maximal generalisation. 

In the paper’s setting, examples are first generalised as far as the deterministic strategy allows. Attacks are introduced only afterwards.

For Causal ABA Learning, this suggests an experimental heuristic:

text First derive candidate causal generalisations. Then introduce defeasible assumptions/attacks only where causal constraints or examples create conflict. 

This is a project-level adaptation, not a result of the paper.

### Coherent vs incoherent control flow

Implementation should distinguish:

text coherent casebase -> grounded-style deterministic reasoning incoherent casebase -> stable/brave reasoning with possible multiple extensions 

This distinction may inspire causal experiments:

text consistent causal evidence -> unique or grounded-style reasoning inconsistent causal evidence -> multiple stable extensions / brave reasoning 

Again, this is an analogy, not a formal result.

### Prediction from a learnt ABA framework

For a new case N, the paper defines prediction using the output of the ABA Learning derivation.

In the stable/brave setting, outcome delta is predicted if there exists a stable extension Delta of the learnt framework such that:

- all positive examples plus the default for the new case are covered in Delta;
- no negative examples are covered in Delta.

This selected-extension idea is relevant to causal discovery because a stable extension in Causal ABA may correspond to a candidate graph.

### Implementation outputs to log

For experiments inspired by this paper, log:

- input cases;
- features;
- labels;
- whether the casebase is coherent;
- positive examples;
- negative examples;
- Rote Learning outputs;
- Folding outputs;
- Assumption Introduction steps;
- assumptions introduced;
- contraries introduced;
- attacks created;
- final learnt ABA framework;
- grounded extension, if used;
- stable extensions, if used;
- selected extension used for prediction;
- predicted outcome;
- conflicts or incoherences.

### Relevance to causal experiments

Do not directly copy the casebase construction into causal discovery unless the experiment explicitly maps causal objects to cases/features/labels.

Useful analogies:

text casebase structure -> causal graph structure feature-based restrictions -> graph-theoretic restrictions label conflicts -> conflicting causal evidence deterministic transformation strategy -> causal-guided transformation strategy 

The implementation should document any such mapping explicitly.

## What not to confuse

### Greedy ABA Learning is not general ABA Learning

Greedy ABA Learning is a specific deterministic variant tailored to case-based reasoning.

Do not treat it as the default or complete ABA Learning method.

### Greedy ABA Learning is not Causal ABA

The paper does not represent DAGs, conditional independences, d-separation or causal graph hypotheses.

Its relevance to Causal ABA Learning is the search-control idea.

### Casebase structure is not causal structure

Binary features and labels are not the same as variables, edges, conditional-independence facts or DAGs.

Any use of Greedy ABA Learning for causal discovery requires a new modelling step.

### The deterministic strategy depends on the domain

The greedy order works because of the casebase setting.

It is not guaranteed to work unchanged for causal discovery.

### Generalise-first is a strategy, not a theorem for causality

The paper supports generalise-first for case-based reasoning.

For causal discovery, generalise-first must be tested experimentally and justified separately.

### Coherence is casebase-specific

Coherence means no two cases have the same features but different labels.

It is not the same as consistency of conditional-independence constraints, satisfiability of a Causal ABA framework, or graph compatibility.

A causal analogue of coherence would need to be defined explicitly.

### Incoherence is not merely statistical noise

In the paper, incoherence is conflicting labels for identical features.

In causal discovery, conflicting conditional-independence/dependence evidence may arise from finite-sample errors, hidden assumptions, or incompatible constraints. This is analogous but not identical.

### Stable-extension prediction is not automatically graph selection

In Greedy ABA Learning, stable extensions support case prediction.

In Causal ABA, stable extensions can induce graphs.

Combining these interpretations requires care.

### Greedy ABA Learning does not remove all theoretical choices

It restricts transformation-rule application in a particular setting. It does not answer what the learning target should be for Causal ABA Learning.

### AA-CBR correspondence is limited

The exact correspondence with AA-CBR holds for coherent casebases under the paper’s construction.

Do not generalise this correspondence to causal discovery or arbitrary ABA Learning tasks.

## Relevant sections in the PDF

Use the following sections as reference points:

- Abstract  
  States the main contribution: Greedy ABA Learning, deterministic transformation-rule application, correspondence with AA-CBR for coherent casebases, and extension to incoherent casebases.

- Section 1: Introduction  
  Explains ABA Learning, the nondeterminism/search-space problem, and the motivation for a greedy deterministic variant. It also states the generalise-first-then-attack strategy.

- Section 2: Related Work  
  Positions the paper against AA-CBR, other case-based reasoning approaches, ABA Learning, ILASP and related logic-based learning methods.

- Section 3: Background  
  Provides the required background on abstract argumentation, ABA, ABA Learning and case-based reasoning.

- Section 4: Learning Problems and Solutions  
  Defines the casebase-based learning problem, positive and negative examples, and the notion of solution used in the paper.

- Section 5: Greedy ABA Learning from Coherent Casebases  
  Main section for the coherent casebase setting. Defines the deterministic transformation strategy and proves correspondence with AA-CBR.

- Section 6: Greedy ABA Learning from Incoherent Casebases  
  Extends the method beyond coherent casebases. Uses stable-extension/brave reasoning to handle conflicts.

- Definition 8  
  Important for prediction under stable extensions: the outcome for a new case is defined by existence of a stable extension covering positives/default and not covering negatives.

- Example 7: Nixon Diamond  
  Useful example of incoherence, multiple stable extensions, and brave prediction.

- Section 7: Conclusion  
  Summarises Greedy ABA Learning as a method for reducing ABA Learning nondeterminism and lists future work, including experiments, comparison with other ABA Learning systems, neuro-symbolic pipelines and preferences.

## Open questions for this project

This paper suggests a way to control ABA Learning search, but it does not define Causal ABA Learning.

Project-specific open questions:

- What is the causal analogue of the casebase structure used by Greedy ABA Learning?

- Can causal graph structure provide deterministic restrictions on transformation-rule application?

- Can the greedy principle “generalise first, introduce attacks later” be useful for causal-discovery examples?

- Should causal constraints be used before or after generalisation?

- Could acyclicity act like a structural restriction on which folded rules are allowed?

- Could d-separation act as a test for whether a transformed framework is still graph-compatible?

- Could conditional-independence evidence play the role of labels or examples?

- Could variables, edges, paths or triples be treated as cases with features?

- Would such a case-based representation distort causal meaning?

- Can conflicting causal evidence be treated analogously to incoherent casebases?

- What is the right causal analogue of “same features, different labels”?

- Can stable-extension/brave reasoning over incoherent casebases inform how to handle incompatible causal constraints?

- If multiple stable extensions correspond to multiple candidate graphs, how should a selected extension be interpreted?

- Can Greedy ABA Learning reduce the transformation search space in causal settings without hard-coding the target graph?

- Which transformation choices should causal structure restrict?
  - Rote Learning targets?
  - Folding candidates?
  - Assumption Introduction locations?
  - Subsumption/deletion decisions?

- Can Greedy-style deterministic transformation be compared against unconstrained ABA Learning on the same causal toy cases?

- Can causal ordering information be used to define an order over transformations?

- Can graph-theoretic compatibility be used as a pruning criterion during learning?

- Can causal constraints improve interpretability, robustness or efficiency of learnt ABA frameworks?

- What metrics should test the usefulness of causal guidance?
  - number of candidate transformations;
  - number of generated frameworks;
  - runtime;
  - number of stable extensions;
  - edge accuracy;
  - accepted/rejected examples;
  - size of learnt framework;
  - explanation quality.

- What is the smallest causal experiment that demonstrates the value of a greedy, causal-guided transformation strategy?