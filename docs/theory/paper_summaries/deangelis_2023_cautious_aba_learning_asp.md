# Paper summary: De Angelis, Proietti, Toni 2023 — ABA Learning via ASP

## Role in this project

This paper is the main source for cautious ABA Learning via Answer Set Programming (ASP).

It takes the general ABA Learning idea from Proietti and Toni and focuses on a specific computational setting:

- ABA frameworks corresponding to logic programs;
- flat ABA frameworks;
- stable-extension semantics;
- cautious or sceptical acceptance;
- ASP as an implementation route.

The paper’s role in this project is to show how ABA Learning can be made executable under stable-extension reasoning. This is directly relevant because Causal ABA also uses stable-extension reasoning and has an ASP implementation. The paper therefore provides one possible computational bridge between ABA Learning and Causal ABA.

For this project, use this paper as the main reference for:

- cautious ABA Learning under stable extensions;
- mapping suitable ABA frameworks to ASP;
- using cautious consequences of ASP programs to guide learning;
- using ASP to guide Rote Learning and generalisation;
- the ASP-ABAlearn strategy;
- restrictions needed to make ABA Learning implementable in ASP.

This paper does not address causal discovery. It does not learn causal graphs. It learns ABA frameworks from background knowledge and positive/negative examples.

## Core definitions

### ASP program

The paper uses Answer Set Programs consisting of rules of the form:

text p :- q1, ..., qk, not qk+1, ..., not qn. 

or constraints of the form:

text :- q1, ..., qk, not qk+1, ..., not qm. 

where not is negation as failure.

Given an ASP program P, the paper writes:

text ans(P) 

for an answer set of P.

If P has answer sets:

text ans1(P), ..., ansl(P) 

then the cautious consequences of P are:

text C(P) = intersection_i ansi(P) 

A sentence is a cautious consequence of P if it belongs to every answer set of P.

### ABA framework

The paper uses ABA frameworks of the form:

text <L, R, A, contrary> 

where:

- L is a language;
- R is a set of rules;
- A is a non-empty set of assumptions;
- contrary maps each assumption into L.

Rules have the form:

text s0 <- s1, ..., sm 

A rule with empty body is a fact:

text s0 <- 

The paper focuses on flat ABA frameworks, where assumptions are not heads of rules.

The paper also focuses on languages consisting of ground atoms, while allowing rule schemata with variables as compact representations of their ground instances.

### Stable extension

For flat ABA frameworks, the paper recalls stable extensions at the argument level.

Let:

text Args 

be the set of all arguments, and:

text Att 

be the attack relation.

A set of arguments Delta subseteq Args is a stable extension iff:

1. it is conflict-free;
2. it attacks every argument outside it.

The paper then considers cautious consequences of flat ABA frameworks under stable extensions.

A sentence s is a cautious consequence of an ABA framework if s is the claim of arguments in all stable extensions.

The paper writes:

text <R, A, contrary> |= s 

to indicate that s is a cautious consequence of the ABA framework.

### Cautious ABA Learning problem

Input:

text (<R, A, contrary>, <E+, E->) 

where:

- <R, A, contrary> is the background ABA framework;
- E+ is a set of positive examples;
- E- is a set of negative examples;
- examples are ground atoms;
- examples are non-assumptions in the background framework.

Goal:

Construct a flat ABA framework:

text <R', A', contrary'> 

such that:

- the learnt framework admits at least one stable extension;
- all positive examples are cautious consequences;
- no negative example is a cautious consequence.

The paper states this as:

text Existence: <R', A', contrary'> admits at least one stable extension.  Completeness: for all e in E+, <R', A', contrary'> |= e.  Consistency: for all e in E-, <R', A', contrary'> not |= e. 

A framework satisfying these conditions is a solution of the ABA Learning problem.

### Intensional solution

The paper distinguishes between:

- non-intensional solutions;
- intensional solutions.

A non-intensional solution may simply add rote facts that cover the positive examples and avoid the negative examples.

An intensional solution contains more general rule schemata, avoiding or limiting lazy memorisation of examples.

This distinction is important for this project because learning causal structure should not reduce to memorising individual observed cases or isolated test outputs.

### Restrictions used in this paper

The paper imposes restrictions needed for the ASP implementation.

Important restrictions include:

- focus on flat ABA frameworks;
- examples are ground atoms;
- examples are non-assumptions;
- each fact in the background framework is ground;
- assumptions appearing in rule bodies satisfy safety-style conditions through non-assumption atoms containing their variables;
- the framework admits at least one stable extension.

These restrictions matter for implementation. Do not silently assume this paper covers arbitrary ABA frameworks.

## Implementation-relevant concepts

### ASP-ABAlearn

The main algorithmic strategy is called:

text ASP-ABAlearn 

It has two main stages:

text RoLe GEN 

where:

- RoLe uses ASP to guide Rote Learning;
- GEN transforms rote/non-intensional rules into more intensional rules using Folding, Assumption Introduction, further Rote Learning and Subsumption.

### RoLe procedure

RoLe aims to add suitable facts to the initial framework so that the resulting framework becomes a non-intensional solution.

It computes an ASP encoding:

text ASP*(<R, A, contrary>, <E+, E->, A) 

If the ASP program is unsatisfiable, learning fails.

Otherwise, the cautious consequences of this ASP program identify atoms that should be added through Rote Learning, including:

- facts for positive examples not already cautiously entailed;
- facts for contraries of assumptions when needed to block negative examples or restore consistency.

Operationally:

text If p(t) is needed, add: p(X) <- X = t 

This gives a direct, example-specific rule.

### GEN procedure

GEN aims to transform a non-intensional solution into an intensional solution.

It repeatedly considers non-intensional learnt rules and applies:

1. Folding;
2. Assumption Introduction if Folding breaks the learning solution;
3. Rote Learning to learn exception facts for new contraries;
4. Subsumption to remove redundant rote facts.

### Rote Learning

Rote Learning adds rules of the form:

text p(X) <- X = t 

These rules are useful for ensuring that examples become derivable, but they are not general.

In implementation, Rote Learning is the simplest transformation to test first.

### Folding

Folding generalises a rule using existing rules.

The paper presents Folding schematically as replacing a body fragment with a predicate that entails it.

Given:

text rho1: H <- Eqs1, B1, B2 rho2: K <- Eqs1, Eqs2, B1 

Folding can replace rho1 with:

text rho3: H <- Eqs2, K, B2 

The purpose is to replace equality-specific or example-specific bodies with more general background predicates.

In implementation, Folding is nondeterministic because there may be multiple possible rules to fold with.

### Assumption Introduction

If Folding produces a framework that no longer solves the learning problem, Assumption Introduction can make the folded rule defeasible.

Given a rule:

text H <- B 

Assumption Introduction replaces it with:

text H <- B, alpha(X) 

where:

- alpha(X) is a new assumption;
- its contrary is a new atom such as c_alpha(X).

Then Rote Learning may add facts for the contrary:

text c_alpha(X) <- X = t 

These contrary facts represent exceptions to the defeasible rule.

This is central to ABA Learning: it turns overgeneralised rules into defeasible rules whose exceptions can be attacked.

### Subsumption

Subsumption removes redundant rote facts.

If the framework contains:

text rho: p(X) <- X = t 

and after removing rho, the framework still cautiously entails p(t), then rho can be deleted.

The paper checks this by testing whether:

text p(t) in C(ASP(<R \ {rho}, A, contrary>)) 

If yes, delete rho.

This prevents unnecessary memorisation once general rules explain the example.

### ASP encodings

The paper defines several ASP encodings.

#### ASP(<R,A,contrary>)

Encodes the ABA framework so that cautious consequences of the ABA framework correspond to cautious consequences of the ASP program.

This encoding includes:

- translated rules;
- ASP rules for assumptions and their contraries.

For an assumption alpha_i occurring in a rule body, it uses an ASP pattern like:

text alpha_i :- dom(X), not c_alpha_i. 

This captures the defeasible availability of the assumption unless its contrary is derived.

#### ASP+(<R,A,contrary>, <E+,E->, K)

Extends the ASP encoding with constraints for examples.

Positive examples are encoded as constraints requiring them:

text :- not e. 

Negative examples are encoded as constraints forbidding them:

text :- e. 

This program is used to generate facts for contraries of assumptions in K.

#### ASP*(<R,A,contrary>, <E+,E->, K)

Extends ASP+ further so that it can also generate facts for positive examples that cannot already be obtained.

It introduces complementary atoms such as neg_p to force a choice between p(X) and neg_p(X) when needed.

This encoding is used by RoLe.

### Implementation architecture

The paper reports a proof-of-concept implementation using:

- SWI-Prolog;
- clingo;
- modules for RoLe;
- modules for GEN;
- modules for ASP, ASP+ and ASP* encodings;
- an API to invoke clingo and collect cautious consequences.

For this repo, the relevant architecture is:

text ABA framework representation -> ASP encoding -> clingo call -> cautious consequence extraction -> transformation-rule application -> updated ABA framework 

### Useful implementation outputs

For experiments using this paper, log:

- background rules;
- assumptions;
- contraries;
- positive examples;
- negative examples;
- generated ASP program;
- answer sets;
- cautious consequences;
- rote rules added;
- folded rules;
- assumptions introduced;
- contraries introduced;
- subsumed/deleted rules;
- final learnt framework;
- whether positives are cautiously entailed;
- whether negatives are not cautiously entailed.

## What not to confuse

### This is cautious learning, not brave learning

This paper focuses on cautious or sceptical reasoning under stable extensions.

Positive examples must be cautious consequences.

Negative examples must not be cautious consequences.

Do not treat this paper as the brave ABA Learning formulation. The brave version is developed in the later 2024 paper.

### ASP is an implementation route, not the learned object

The system uses ASP to implement reasoning tasks involved in ABA Learning.

It does not mean that the learning target is an ASP program in the same sense as ILASP.

The target remains an ABA framework:

text <R', A', contrary'> 

### ABA Learning is not ordinary supervised ML

The learnt object is symbolic:

- rules;
- assumptions;
- contraries.

The learning process transforms a symbolic framework. It is not parameter fitting.

### Flat ABA restriction matters

The paper focuses on flat ABA frameworks.

Do not assume the strategy applies unchanged to non-flat frameworks, especially because Causal ABA may become non-flat in some constructions when facts are added.

### Cautious consequence is not derivability from one extension

A positive example being derivable in some stable extension is not enough for this paper’s setting.

It must be a cautious consequence: accepted under all stable extensions.

### Rote Learning is not the final goal

Rote Learning creates a non-intensional solution by adding example-specific facts.

The intended aim is to generalise using GEN.

For this project, rote-only solutions should be treated as baselines or intermediate states, not as satisfying evidence of meaningful causal learning.

### Folding can break the solution

Folding generalises rules but may make the framework stop satisfying the examples.

The paper handles this by using Assumption Introduction and Rote Learning of exception facts.

In experiments, always re-check the learning task after Folding.

### Assumption Introduction is not arbitrary assumption creation

Assumption Introduction is applied to a rule to make it defeasible.

The new assumption must have a contrary.

Exception rules for the contrary may then be learnt.

### Subsumption deletes rote redundancy

Subsumption is a clean-up rule.

It should not delete rules from the original background knowledge unless the implementation explicitly allows this and the theory supports it.

### Negative examples are not attacked directly

Negative examples are excluded by ensuring they are not cautious consequences. This may require adding contraries of assumptions, exceptions, or other rules.

Do not model every negative example as a direct contrary unless that modelling choice is explicit.

### Causal discovery is not covered

This paper does not discuss:

- DAGs;
- d-separation;
- conditional independence;
- causal sufficiency;
- Markov equivalence;
- ABA-PC.

Any use for causal discovery is a project-level adaptation.

## Relevant sections in the PDF

Use the following sections as reference points:

- Abstract  
  States the paper’s purpose: implementing ABA Learning using ASP to help guide Rote Learning and generalisation.

- Section 1: Introduction  
  Defines the high-level goal of ABA Learning from background knowledge and positive/negative examples. States the paper’s focus on cautious reasoning under stable extensions and the correspondence with answer set programs.

- Section 2: Background  
  Defines ASP syntax, answer sets, cautious consequences, ABA frameworks, facts, flatness, arguments, attacks and stable extensions.

- Section 3: Preliminaries: Cautious ABA Learning under Stable Extensions  
  Main source for the cautious ABA Learning problem definition, restrictions imposed for ASP implementation, examples as ground non-assumption atoms, and the solution conditions: existence, completeness and consistency.

- Example 2  
  Useful running example showing background knowledge, assumptions, positive examples, negative examples, and the distinction between non-intensional and intensional solutions.

- Section 4: Learning ABA Frameworks via Transformation Rules and ASP Solving  
  Main algorithmic section. Defines the transformation-rule subset used and the ASP-ABAlearn strategy.

- Figure 1: ASP-ABAlearn strategy  
  Operational reference for RoLe and GEN.

- Figure 2: ASP encodings  
  Defines the ASP, ASP+ and ASP* encodings used for cautious consequence checking and fact generation.

- Examples 3–7  
  Show the learning strategy in action:
  - Rote Learning adds facts;
  - Folding generalises;
  - Assumption Introduction makes rules defeasible;
  - Rote Learning adds exception facts;
  - Subsumption removes redundant rote rules.

- Section 5: Discussion and Conclusion  
  Important for implementation limitations. Notes that Folding is nondeterministic, a proof-of-concept implementation is ongoing, and further work is needed on completeness and controlling search.

## Open questions for this project

This paper provides an ASP-supported cautious ABA Learning mechanism. It leaves open how this mechanism should interact with Causal ABA.

Project-specific open questions:

- Can Causal ABA components be represented as the background ABA framework for cautious ABA Learning?

- What should positive examples be in a causal-discovery setting?
  - edge claims?
  - no-edge claims?
  - conditional-independence claims?
  - dependence claims?
  - graph-level compatibility claims?
  - accepted causal conclusions?

- What should negative examples be?
  - forbidden edges?
  - false causal claims?
  - incompatible graph hypotheses?
  - unwanted independences?
  - unwanted dependences?

- Is cautious acceptance too strong for causal discovery, where multiple compatible graphs may exist?

- Would requiring positive causal claims to hold in all stable extensions correspond to invariant causal features across a Markov equivalence class?

- Could cautious ABA Learning learn only those causal features common to all compatible graphs?

- How should the paper’s flatness restrictions interact with Causal ABA, where some constructions may be non-flat?

- Can the ASP-ABAlearn strategy be reused with Causal ABA’s ASP encoding, or would the encodings conflict?

- Can Rote Learning add causal facts such as arr_xy, noe_xy, or indep(x,y,Z)?

- Can Folding generalise from individual causal facts to reusable causal rules?

- What would Assumption Introduction mean in a causal setting?
  - defeasible edge rule?
  - defeasible independence rule?
  - exception to a causal generalisation?
  - exception to a transformation step?

- Can Subsumption remove rote causal facts after more general causal-argumentative rules explain them?

- Does cautious ABA Learning overfit less than brave ABA Learning in small causal-discovery cases, or is it too restrictive?

- How should finite-sample uncertainty be represented in the examples or background framework?

- Can causal constraints such as acyclicity guide or restrict Folding choices?

- Can d-separation constraints be used to test whether learnt rules produce graph-compatible extensions?

- How should quantitative evaluation compare:
  - rote-only solution;
  - folded/generalised solution;
  - defeasible solution with assumptions;
  - Causal ABA baseline;
  - ABA-PC baseline?

- What is the smallest causal toy case where cautious ABA Learning produces a nontrivial intensional solution rather than mere memorisation?