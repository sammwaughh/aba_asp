# Paper summary: De Angelis, Proietti, Toni 2024 — Learning Brave Assumption-Based Argumentation Frameworks via ASP

## Role in this project

This paper is the main source for brave ABA Learning via Answer Set Programming (ASP).

It extends the ABA Learning line of work by formulating learning in terms of brave, or credulous, reasoning under stable extensions. Instead of requiring examples to be accepted sceptically across all stable extensions, the paper asks for a learnt ABA framework admitting at least one stable extension in which all positive examples are accepted and all negative examples are not accepted.

The paper’s role in this project is to provide a computationally executable form of ABA Learning that is closer to settings where multiple alternative extensions may exist. This matters for Causal ABA Learning because Causal ABA naturally produces multiple stable extensions corresponding to alternative compatible graph hypotheses.

Use this paper as the main reference for:

- brave ABA Learning under stable extensions;
- selected-extension learning;
- ASP-ABAlearnB;
- ASP-supported Rote Learning;
- Folding;
- Assumption Introduction;
- Fact Subsumption;
- the set T of learnable predicates;
- comparison with ILASP and related ASP-learning systems;
- the distinction between learning ABA frameworks and learning ASP programs directly.

This paper does not address causal discovery. It does not define Causal ABA, d-separation, DAG compatibility, or conditional-independence evidence. Its relevance to this project is methodological: it provides the brave/stable-extension learning machinery that may be adapted to causal-argumentative structures.

## Core definitions

### ASP program

The paper uses Answer Set Programming rules of the form:

text p :- q1, ..., qk, not qk+1, ..., not qn. 

and constraints of the form:

text :- q1, ..., qk, not qk+1, ..., not qn. 

where not denotes negation as failure.

An answer set of an ASP program is a set of ground atoms assigned by stable-model semantics.

An ASP program is satisfiable if it has at least one answer set.

An atom p is a brave consequence of an ASP program P if there exists an answer set A of P such that:

text p in A 

### ABA framework

The paper uses ABA frameworks of the form:

text <L, R, A, contrary> 

where:

- L is a language;
- R is a set of rules;
- A is a non-empty set of assumptions;
- contrary maps assumptions into the language.

A rule has the form:

text s0 <- s1, ..., sm 

If m = 0, the rule is a fact:

text s0 <- 

The paper focuses on flat ABA frameworks, where assumptions are not heads of rules.

The paper focuses on finite languages of ground atoms, but uses rule schemata with variables to compactly represent ground instances.

### Arguments and attacks

An argument for a claim s is a finite tree-derivation using rules and supported by assumptions.

An argument attacks another argument if its claim is the contrary of an assumption used in the support of the attacked argument.

### Stable extension

For a flat ABA framework, let:

text Args 

be the set of all arguments, and:

text Att 

be the attack relation.

A set of arguments Delta subseteq Args is a stable extension iff:

1. it is conflict-free;
2. it attacks every argument outside it.

The paper writes:

text <R, A, contrary> |=_Delta s 

to indicate that Delta is a stable extension of the ABA framework and s is the claim of an argument in Delta.

A sentence s is a brave consequence of an ABA framework when it is accepted in at least one stable extension.

### Brave ABA Learning problem

The paper defines brave ABA Learning as follows.

Input:

text (<R, A, contrary>, <E+, E->, T) 

where:

- <R, A, contrary> is satisfiable background knowledge;
- E+ is a set of positive examples;
- E- is a set of negative examples;
- E+ and E- are disjoint;
- examples are ground atoms;
- examples are non-assumptions in the background framework;
- T is a set of learnable predicates;
- T does not overlap with predicates of assumptions;
- predicates occurring in the examples are included in T.

Goal:

Construct a learnt ABA framework:

text <R', A', contrary'> 

such that:

1. R subseteq R';
2. for each learnt rule, if its head predicate is an old predicate, then it must be learnable via T;
3. A subseteq A';
4. old contraries are preserved;
5. the learnt framework is satisfiable and admits a stable extension Delta;
6. for all positive examples e in E+, e is accepted with respect to Delta;
7. for all negative examples e in E-, e is not accepted with respect to Delta.

The solution is therefore evaluated with respect to a selected stable extension.

The paper also says that <R', A', contrary'> bravely entails <E+, E-> when such a stable extension exists.

### Learnable predicates T

The set T restricts which existing predicates may appear in the heads of learnt rules.

If a learnt rule has a head predicate already occurring in the background knowledge or examples, that predicate must be in T.

New predicates, such as contraries of new assumptions introduced during learning, do not need to be in T.

This is important because Assumption Introduction may create new assumptions and new contrary predicates.

### Intensional solution

A solution is intensional when the newly learnt rules are non-ground rule schemata.

A non-intensional solution may use ground or example-specific facts.

For this project, intensionality matters because causal learning should avoid merely memorising individual edge claims or individual conditional-independence reports.

## Implementation-relevant concepts

### ASP-ABAlearnB

The main algorithm is:

text ASP-ABAlearnB 

It is the brave-learning counterpart of the earlier cautious ASP-ABAlearn strategy.

Its purpose is to derive an intensional solution for a brave ABA Learning problem.

It consists of two main procedures:

text RoLe Gen 

### RoLe

RoLe repeatedly applies Rote Learning to add a minimal set of facts to the background knowledge such that the resulting ABA framework is a non-intensional solution of the brave learning problem.

Operationally, it uses ASP to decide which facts should be added.

The ASP encoding introduces choice over learnable predicates in T and minimises the number of new facts added.

This gives a smallest or minimal rote solution, relative to the encoding.

### Gen

Gen transforms the non-intensional solution produced by RoLe into an intensional solution.

It processes learnt non-intensional rules by applying:

1. Folding;
2. Assumption Introduction if Folding breaks the brave solution;
3. Rote Learning to add exception facts for contraries of newly introduced assumptions;
4. Fact Subsumption to remove redundant rote facts.

Gen iterates until all learnt rules are intensional or failure is reported.

### Rote Learning

Rote Learning adds a fact-like rule for a target atom.

Given atom:

text p(t) 

Rote Learning adds:

text p(X) <- X = t 

The paper uses Rote Learning for:

- adding facts from positive examples;
- adding facts for contraries of assumptions.

This is the initial memorisation step.

### Folding

Folding generalises a rule using another rule.

Given distinct rules:

text rho1: H <- Eqs1, B1, B2 rho2: K <- Eqs1, Eqs2, B1 

Folding replaces rho1 with:

text rho3: H <- Eqs2, K, B2 

The result is:

text R' = (R \ {rho1}) union {rho3} 

Folding can preserve arguments, but it may introduce new arguments and attacks. Therefore it may destroy the property of being a brave learning solution.

### Assumption Introduction

Assumption Introduction makes a rule defeasible.

Given:

text rho1: H <- Eqs, B 

it can replace rho1 with:

text rho2: H <- Eqs, B, alpha(X) 

where:

- alpha(X) is a new assumption;
- c_alpha(X) is its contrary.

The new framework adds:

text alpha(X) to A contrary(alpha(X)) = c_alpha(X) 

This is used after Folding when the folded rule overgeneralises or introduces unwanted arguments. Exception facts for c_alpha can then block the default in specific cases.

### Fact Subsumption

Fact Subsumption removes redundant rote facts relative to the brave learning task.

Suppose the rule set contains:

text rho: p(X) <- X = t 

If removing rho still leaves a framework that bravely entails the positive/negative example pair, then Fact Subsumption deletes it:

text R' = R \ {rho} 

This prevents the final learnt framework from retaining unnecessary rote memorisation once a more general intensional rule explains the examples.

### Normalised rule form

The paper assumes rules are written in normalised form:

text p0(X0) <- eq1, ..., eqk, p1(X1), ..., pn(Xn) 

Ground facts are represented as:

text p(X) <- X = t 

This representation matters because the transformation rules, especially Folding and Fact Subsumption, operate over equality-normalised rules.

### ASP encoding

The paper defines:

text ASP(<R,A,contrary>, <E+,E->, T) 

This encoding includes:

1. background rules translated into ASP syntax;
2. assumptions encoded as default-available atoms unless their contrary holds;
3. constraints requiring positive examples;
4. constraints forbidding negative examples;
5. choice rules over learnable predicates in T;
6. minimisation over newly added facts.

For an assumption alpha(X) with contrary c_alpha(X), the ASP pattern is:

text alpha(X) :- dom(X), not c_alpha(X). 

For a positive example e, add:

text :- not e. 

For a negative example e, add:

text :- e. 

For learnable predicate p in T, introduce a fresh predicate p_prime and rules of the form:

text p(X) :- p_prime(X). {p_prime(X)} :- dom(X). 

with a minimisation directive to minimise newly added facts.

### Key ASP-theoretic results

The paper proves:

1. <R,A,contrary> bravely entails <E+,E-> iff the ASP encoding with empty T is satisfiable.
2. A solution to the brave learning problem exists iff the ASP encoding with T is satisfiable.
3. From an answer set, one can construct a solution by adding rote facts for selected p_prime(t) atoms.

These results justify using clingo to guide the construction of brave ABA Learning solutions.

### Soundness and termination

The paper states ASP-ABAlearnB is sound and terminating.

For implementation, this means the algorithm is intended to produce valid brave ABA Learning solutions when it succeeds, under the paper’s restrictions.

### Comparison with ILASP

The paper compares ASP-ABAlearnB with ILASP, a state-of-the-art system for learning ASP programs.

The distinction is important:

- ILASP learns ASP programs.
- ASP-ABAlearnB learns ABA frameworks using ASP as a computational backend.

This is a representational difference, not merely an implementation detail.

### Useful implementation outputs

For each experiment based on this paper, log:

- background framework;
- E+;
- E-;
- T;
- generated ASP encoding;
- clingo command;
- answer set selected by RoLe;
- facts added by Rote Learning;
- folded rules;
- assumptions introduced;
- contraries introduced;
- exception facts added;
- facts removed by Fact Subsumption;
- final learnt framework;
- selected stable extension satisfying the examples;
- whether positives are accepted in the selected extension;
- whether negatives are rejected in the selected extension.

## What not to confuse

### Brave learning is not cautious learning

Cautious learning evaluates examples across all stable extensions.

Brave learning requires the existence of a stable extension satisfying the examples.

Do not import the cautious acceptance condition from the 2023 paper.

### The examples are evaluated with respect to a selected stable extension

The paper’s definition requires a stable extension Delta such that:

text all positives are accepted in Delta all negatives are not accepted in Delta 

This differs from requiring positives to be accepted in every stable extension.

### Brave consequence is not arbitrary derivability

A claim is accepted only if it is the claim of an argument in the relevant stable extension.

Do not treat syntactic derivability from some rule as sufficient unless the supporting argument belongs to the selected stable extension.

### ASP is not the learned object

ASP is used to implement the learning process.

The learned object is still an ABA framework:

text <R', A', contrary'> 

Do not describe this as “learning an ASP program” unless explicitly comparing to ILASP.

### T is not just the set of example predicates

The set T must include predicates occurring in examples, but it may also include other learnable predicates.

The choice of T can affect whether a solution exists.

### New contrary predicates need not be in T

Contraries of newly introduced assumptions can be new predicates. These are not subject to the same T restriction as old predicates in learnt rule heads.

### Rote Learning is not the intended final representation

Rote Learning produces a non-intensional solution.

Gen is responsible for generalising and making the solution intensional.

### Folding may break a brave solution

Folding can introduce new arguments and attacks. It may make the current framework fail the brave learning task.

Always re-check the examples after Folding.

### Assumption Introduction repairs overgeneralisation

Assumption Introduction is used to make a folded/general rule defeasible. Exception facts for the contrary can then recover a valid solution.

Do not add assumptions randomly; they should serve the purpose of controlling a rule’s applicability.

### Fact Subsumption is relative to the learning task

A rote fact can be deleted only if the resulting framework still bravely entails the positive/negative examples.

It is not merely syntactic deletion.

### Flatness restriction matters

The paper focuses on flat ABA frameworks.

Do not assume the algorithm applies unchanged to arbitrary non-flat ABA frameworks or to all forms of Causal ABA.

### This paper does not solve search-control generally

ASP-ABAlearnB still relies on transformation choices. The later Greedy ABA Learning paper addresses search-control more directly in a case-based setting.

### This paper does not define causal learning

It is not a causal-discovery method.

Any use for Causal ABA Learning is a project-level adaptation.

## Relevant sections in the PDF

Use the following sections as reference points:

- Abstract  
  States the contribution: brave ABA Learning under stable extensions, transformation-rule algorithm, ASP implementation, and comparison with ILP systems.

- Section 1: Introduction  
  Explains the motivation, contrasts brave learning with prior cautious work, and states the three main contributions: definition, ASP-ABAlearnB, and empirical evaluation.

- Section 2: Related Work  
  Important for distinguishing this work from earlier ABA Learning, cautious ASP-based ABA Learning, ILASP and other ASP/ILP systems.

- Section 3.1: Answer Set Programs  
  Defines ASP syntax, answer sets, satisfiability and brave consequences.

- Section 3.2: Assumption-Based Argumentation  
  Defines ABA frameworks, facts, flatness, arguments, attacks, stable extensions and brave consequences.

- Section 4: Brave ABA Learning under Stable Extensions  
  Main formal definition of the brave ABA Learning problem. Defines input, learnable predicates T, solution conditions, selected stable extension and intensionality.

- Definition 1  
  Central definition of brave ABA Learning.

- Examples 3 and 4  
  Useful for understanding the role of T, new predicates and the existence of solutions.

- Section 5: Brave ABA Learning via Transformation Rules  
  Defines the transformation rules used: Rote Learning, Folding, Assumption Introduction and Fact Subsumption.

- R1: Rote Learning  
  Adds equality-specific rules for atoms.

- R2: Folding  
  Generalises rules using other rules.

- Proposition 1  
  Shows Folding preserves arguments but not necessarily extensions.

- R3: Assumption Introduction  
  Makes a rule defeasible by adding a new assumption and contrary.

- Proposition 2  
  Shows how Assumption Introduction plus Rote Learning can recover a solution after Folding under general conditions.

- R4: Fact Subsumption  
  Removes redundant rote facts relative to the brave learning task.

- Section 6: A Brave ABA Learning Algorithm  
  Defines ASP-ABAlearnB, with RoLe and Gen.

- Algorithm 1  
  Operational reference for the implementation.

- Definition 2  
  Defines the ASP encoding used by the algorithm.

- Theorem 1  
  Relates brave entailment of the example pair to satisfiability of the ASP encoding.

- Theorem 2  
  Relates existence of a brave learning solution to satisfiability of the ASP encoding with learnable predicates.

- Later empirical evaluation section  
  Use for benchmark information and comparison with ILASP.

- Appendix  
  Contains proofs of soundness, termination and supporting theorems.

## Open questions for this project

This paper gives a brave/stable-extension ABA Learning mechanism. It leaves open how that mechanism should interact with Causal ABA.

Project-specific open questions:

- Is brave ABA Learning more suitable than cautious ABA Learning for causal discovery, since Causal ABA often admits multiple compatible graph hypotheses?

- If a stable extension corresponds to a candidate graph, does brave learning correspond to learning a framework that has at least one graph satisfying the examples?

- Is that too weak for causal discovery, where we may want all compatible graphs to satisfy certain constraints?

- Should positive causal examples be accepted in one selected graph-extension or in all graph-extensions?

- Could cautious learning represent invariant causal claims, while brave learning represents existence of at least one compatible causal hypothesis?

- How should the selected stable extension be interpreted causally?
  - one candidate DAG;
  - one explanation of the examples;
  - one admissible causal hypothesis;
  - one solution among multiple graph-compatible alternatives?

- What should the learnable predicate set T contain in causal experiments?
  - arr;
  - noe;
  - indep;
  - dep;
  - derived predicates such as path;
  - exception predicates;
  - causal-classification predicates?

- Can RoLe add minimal causal facts such as arr_xy or indep(x,y,Z)?

- Can the minimisation in RoLe serve as a preference for sparse causal explanations?

- Would minimising added facts correspond to a causal sparsity bias, or would that be theoretically unjustified?

- Can Folding generalise edge-specific facts into reusable causal rules?

- What background predicates would make Folding meaningful in causal graph learning?

- Can Assumption Introduction represent defeasible causal relations?

- What would an exception to a causal edge rule mean?
  - finite-sample noise;
  - context-specific causality;
  - graph-theoretic incompatibility;
  - violation of acyclicity;
  - violation of d-separation constraints?

- Could Fact Subsumption remove rote edge facts once a more general causal rule explains them?

- How should negative examples be represented in causal discovery?
  - forbidden edge;
  - forbidden graph;
  - unwanted independence;
  - unwanted dependence;
  - rejected causal claim?

- Can the ASP encoding in this paper be composed with Causal ABA’s ASP encoding, or would the encodings need to be redesigned?

- Does the flatness restriction block direct reuse with Causal ABA, given that Causal ABA may become non-flat in some constructions?

- Should the first experiments use a simplified flat fragment of Causal ABA to remain compatible with this paper?

- Can the algorithm be used to learn only the input facts to a fixed Causal ABA framework, rather than learning the graph-theoretic rules themselves?

- How should learned frameworks be evaluated against causal ground truth?

- What is the smallest example where brave ABA Learning learns a causal structure that cautious ABA Learning would reject as too strong?