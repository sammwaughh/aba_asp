# Paper summary: Proietti, Toni 2024 — Learning Assumption-Based Argumentation Frameworks

## Role in this project

This is the canonical paper for the original ABA Learning formulation.

It introduces ABA Learning as a form of symbolic, logic-based learning that generates Assumption-Based Argumentation (ABA) frameworks from:

- background knowledge;
- positive examples;
- negative examples.

Its main role in this project is to define the learning side of Causal ABA Learning.

Where Causal ABA explains how causal-discovery evidence can be represented and evaluated within ABA, this paper explains how ABA frameworks can be learnt or transformed from examples. It is therefore the primary source for:

- the general ABA Learning problem;
- learning rules, assumptions and contraries;
- transformation-rule-based learning;
- Rote Learning;
- Folding;
- Equality Removal;
- Assumption Introduction;
- undercutting attacks;
- stratified and non-stratified learnt frameworks;
- intensional learning rather than mere example memorisation.

The paper does not address causal discovery. It does not discuss DAGs, d-separation, conditional-independence tests, or Causal ABA. Its relevance to this project is methodological: it supplies the learning machinery that might be adapted to causal-discovery representations.

## Core definitions

### ABA framework

An ABA framework is a tuple:

text <L, R, A, contrary> 

where:

- L is a language;
- R is a set of inference rules;
- A is a set of assumptions;
- contrary maps assumptions to their contraries.

A rule has the form:

text s0 <- s1, ..., sm 

Rules are used to construct arguments. Assumptions may appear in supports of arguments. Attacks arise when an argument derives the contrary of an assumption used by another argument.

### ABA Learning problem

ABA Learning aims to generate an ABA framework from examples and background knowledge.

Input:

text Background ABA framework: <L, R, A, contrary>  Positive examples: E+  Negative examples: E- 

Goal:

Identify rules, assumptions and contraries, adding to those in the background knowledge, such that:

- positive examples are argumentatively covered;
- negative examples are not argumentatively covered;
- acceptance is evaluated under a chosen ABA semantics.

The paper presents ABA Learning as learning an ABA framework, not merely classifying examples.

### Background knowledge

Background knowledge is itself given in ABA format.

This is important: ABA Learning does not start from unstructured data alone. It starts from an initial symbolic framework and transforms or extends it.

### Positive and negative examples

Positive examples are target claims that the learnt ABA framework should support or accept.

Negative examples are target claims that the learnt ABA framework should not support or accept.

The examples guide the transformation process.

### Argumentative coverage

The paper frames learning as covering examples argumentatively.

A learnt framework should support arguments for positives and avoid accepted arguments for negatives, according to the selected semantics.

The exact acceptance condition depends on the chosen semantics and the later variants of ABA Learning.

### Transformation rules

The paper’s learning strategy is based on transformation rules applied to ABA frameworks.

Main transformation rules:

- Rote Learning;
- Folding;
- Equality Removal;
- Assumption Introduction.

Some of these are adapted from logic program transformation, especially Folding. Others, such as Rote Learning and Assumption Introduction, are specific to the ABA Learning strategy.

### Rote Learning

Rote Learning introduces rules directly tied to examples.

For a positive example such as:

text p(t) 

Rote Learning may introduce a rule of the form:

text p(X) <- X = t 

This makes the example derivable, but it is example-specific.

Rote Learning is useful as an initial step, but by itself it tends to memorise examples rather than produce general knowledge.

### Folding

Folding generalises rules by using existing background predicates or rules.

The purpose of Folding is to replace specific conditions, often equalities or concrete example structure, with more abstract predicates already available in the background knowledge.

Schematic form:

text H <- Eqs, B K <- Eqs 

can support a transformed rule where the body uses K instead of the more specific conditions.

Folding is the main transformation for moving from rote, example-specific rules to intensional rules.

### Equality Removal

Equality Removal removes equality constraints when they are no longer needed after Folding or when variables can be generalised.

In the paper’s robot example, Rote Learning first introduces an equality-specific rule, Folding abstracts it, and Equality Removal yields a more general rule.

Operationally, Equality Removal is part of the route from memorisation to generalisation.

### Assumption Introduction

Assumption Introduction makes a rule defeasible.

Given a rule:

text H <- B 

Assumption Introduction can transform it into:

text H <- B, alpha(...) 

where alpha(...) is a new assumption.

The new assumption has a contrary:

text c_alpha(...) 

The assumption represents the condition under which the default rule is allowed to apply. The contrary represents an exception.

This allows the learnt framework to encode exceptions through undercutting attacks.

### Undercutting attacks

A central contribution of the paper is that exceptions to general rules are represented as undercutting attacks.

Instead of learning a competing rule with the opposite conclusion, ABA Learning introduces an assumption into the body of the default rule and then learns rules deriving the contrary of that assumption.

Example pattern:

text default: H <- B, alpha  exception: c_alpha <- ExceptionCondition 

The exception attacks the assumption alpha needed to use the default rule. It does not need to derive the negation of H.

This distinguishes the method from approaches where exceptions are represented as rebuttal attacks between conflicting conclusions.

### Rebuttal vs undercutting

Rebuttal attack:

text default derives H exception derives not H 

Undercutting attack:

text default derives H using assumption alpha exception derives contrary(alpha) 

The paper argues that undercutting can represent some exception-learning problems more naturally than rebuttal.

### Stratified and non-stratified frameworks

The paper presents:

- a general strategy for learning stratified frameworks;
- a variant for non-stratified cases.

ABA frameworks can be mapped to logic programs with negation as failure in certain cases. These logic programs may be non-stratified.

This matters because ABA Learning can represent recursive or mutually dependent defeasible patterns that are difficult for purely stratified approaches.

### Intensional learning

An intensional solution expresses reusable patterns through rules, variables, background predicates, assumptions and contraries.

This contrasts with rote learning, which merely memorises individual examples through constant-specific rules.

For this project, intensional learning is the relevant ideal. Learning causal structure should not reduce to memorising individual conditional-independence reports or individual edge labels.

## Implementation-relevant concepts

### Core implementation objects

An implementation should represent:

text Rule Assumption Contrary ABA framework Positive examples Negative examples Transformation step Learnt framework 

A useful Python structure:

python @dataclass(frozen=True) class Rule:     head: Atom     body: tuple[Atom, ...]  @dataclass(frozen=True) class ABAFramework:     rules: frozenset[Rule]     assumptions: frozenset[Atom]     contraries: Mapping[Atom, Atom] 

Transformation rules should be implemented as explicit operations producing a new framework or a new working framework.

### Transformation trace

For experimentation, every transformation should be logged.

Record:

- input rule;
- transformation type;
- output rule;
- assumptions added;
- contraries added;
- examples newly covered;
- examples incorrectly covered;
- whether the learning task remains solved.

This is essential for later report writing and supervisor review.

### Rote Learning implementation

Input:

text positive example p(t) 

Output:

text p(X) <- X = t 

For a simplified implementation, constants may be handled directly:

text p(t) <- 

but this loses the paper’s generalisation route. Use equality-based rules if Folding and Equality Removal are being tested.

### Folding implementation

Folding is the most complex transformation operationally because there may be many possible rules to fold with.

Implementation should start with restricted toy cases:

- one candidate rule to fold;
- one background rule;
- one expected folded output.

Do not implement broad automatic Folding before the simplest examples work.

### Equality Removal implementation

Equality Removal can be implemented later.

For initial experiments, it is acceptable to simulate the effect of Equality Removal manually or use a simplified generalisation rule, provided the experiment records this as a simplification.

### Assumption Introduction implementation

Given:

text H <- B 

generate:

text H <- B, alpha(args) 

and add:

text alpha(args) to assumptions contrary(alpha(args)) = c_alpha(args) 

The implementation must ensure that:

- the new assumption is tracked explicitly;
- the contrary mapping is updated;
- exception rules can target the contrary.

### Exception learning

After Assumption Introduction, learn rules for the contrary of the new assumption.

Example:

text c_alpha(X,Y) <- X = 4, Y = 6 

This allows the framework to block overgeneralised default rules in specific cases.

### Semantics check after each transformation

Every transformation can change which examples are accepted.

After each transformation, recompute or verify:

- all positive examples are accepted;
- no negative examples are accepted;
- under the chosen semantics.

For early implementation, direct checks on toy cases may be sufficient. Later, use an ABA solver or ASP/clingo.

### Search control

The paper’s transformation-based approach creates search choices.

The implementation should avoid unrestricted search initially. Use:

- hand-specified candidate transformations;
- deterministic ordering;
- small toy cases;
- explicit expected outputs;
- exhaustive logging.

Search-control is a central issue for the later Greedy ABA Learning paper and for this project’s causal-guidance direction.

### Useful experiment outputs

For each ABA Learning experiment, output:

- background framework;
- positive examples;
- negative examples;
- sequence of transformations;
- learnt rules;
- learnt assumptions;
- learnt contraries;
- accepted positive examples;
- rejected negative examples;
- any overgeneralisation;
- any exception rules;
- final framework.

## What not to confuse

### This is the general ABA Learning paper, not the ASP implementation paper

This paper introduces the transformation-rule-based ABA Learning approach.

The later De Angelis, Proietti and Toni papers develop ASP-based cautious and brave implementations.

Do not treat this paper as defining the final ASP encoding.

### ABA Learning is not Causal ABA

ABA Learning learns ABA frameworks from examples.

Causal ABA constructs ABA frameworks for causal-discovery reasoning.

This project investigates whether and how these can interact.

### ABA Learning is not ordinary ILP over ASP programs

The target is an ABA framework containing rules, assumptions and contraries.

Although some ABA frameworks can be mapped to logic programs, the learnt object is not simply an ASP program in the ILASP sense.

### Rote Learning is not sufficient

Rote Learning can cover examples directly, but it does not produce a meaningful general theory by itself.

For this project, rote-only causal learning would usually be weak evidence unless used as a baseline.

### Folding is not arbitrary abstraction

Folding uses existing rules/background predicates to generalise. It is not a free licence to invent arbitrary predicates unless the learning strategy has explicitly introduced them.

### Assumption Introduction is not just adding noise

Assumption Introduction has a precise purpose: make an overgeneralised rule defeasible by adding a new assumption and contrary.

The new assumption represents normal applicability; the contrary represents exceptions.

### Undercutting is not rebuttal

The paper’s distinctive exception mechanism is undercutting.

Do not implement exceptions only as rules deriving an opposite target label unless the experiment explicitly compares rebuttal and undercutting.

### Equality Removal should not be ignored if reproducing the paper’s examples

The original strategy uses Equality Removal in the path from rote examples to general rules.

It can be omitted in simplified project experiments only if explicitly documented.

### Stratified and non-stratified settings differ

The paper proposes both a strategy for stratified frameworks and a variant for non-stratified cases.

Do not silently assume results for one setting apply to the other.

### Learning rules does not automatically mean learning causal rules

In this project, if transformation rules produce an ABA framework, it still needs to be shown that the learnt framework has a coherent causal interpretation.

### Positive/negative examples require careful causal interpretation

In a causal setting, it is not obvious whether examples should be:

- edge claims;
- no-edge claims;
- independence claims;
- dependence claims;
- graph hypotheses;
- accepted causal conclusions;
- transformation choices.

This is a project-level modelling decision.

## Relevant sections in the PDF

Use the following sections as reference points:

- Abstract  
  States the core contribution: learning ABA frameworks from positive/negative examples and background knowledge using transformation rules, with undercutting attacks for exceptions.

- Section 1: Introduction  
  Motivates ABA Learning as a logic-based learning approach and explains why learning ABA frameworks is distinct from learning ordinary logic programs. It also states the link between ABA and logic programs with negation as failure.

- Section 2: Background: Assumption-Based Argumentation  
  Defines ABA frameworks, rules, assumptions, contraries, arguments, attacks and semantics.

- Section 3: Learning ABA Frameworks  
  Defines the ABA Learning problem: learn rules, assumptions and contraries extending background knowledge so that positive examples are covered and negative examples are not.

- Section 4: Transformation Rules  
  Main technical section for implementation. Defines Rote Learning, Folding, Equality Removal and Assumption Introduction.

- Section 5: Examples  
  Shows how transformation rules operate on concrete learning problems.

- Robot/free example  
  Especially useful for understanding the pipeline:
  Rote Learning -> Folding -> Equality Removal -> Assumption Introduction -> exception learning.

- Section 6: Strategy for Learning Stratified ABA Frameworks  
  Presents an ordered strategy for applying the transformation rules.

- Section 7: Non-stratified Case  
  Discusses the variant for learning non-stratified frameworks.

- Related work discussion  
  Useful for distinguishing ABA Learning from methods that learn exceptions through rebuttal attacks or learn other non-monotonic formalisms.

## Open questions for this project

This paper defines ABA Learning, but it leaves open how to apply it to causal discovery.

Project-specific open questions:

- What is the correct causal analogue of a positive example?

- What is the correct causal analogue of a negative example?

- Should examples be individual causal statements such as arr_xy, graph-level structures, or conditional-independence statements?

- Can Rote Learning add causal facts such as:
  - arr_xy;
  - noe_xy;
  - indep(x,y,Z);
  - dep(x,y,Z)?

- Can Folding generalise individual causal facts into reusable causal rules?

- What background predicates would make Folding meaningful in causal discovery?

- Can Assumption Introduction represent defeasible causal rules?

- What would an exception to a causal rule mean?
  - finite-sample test error;
  - context-specific causal relation;
  - graph-incompatibility;
  - violation of an assumed causal pattern;
  - exception to an edge-generalisation rule?

- Should causal graph constraints such as acyclicity be fixed background rules before learning starts?

- Should d-separation rules be fixed background rules, or can parts of them be learnt?

- Can transformation-rule search be constrained by causal structure?

- Can undercutting attacks represent unreliable conditional-independence evidence more naturally than rebuttal-style conflicts?

- How can a learnt ABA framework be evaluated as a causal-discovery output?

- Should a learnt framework output:
  - a single graph;
  - a set of compatible graphs;
  - accepted causal claims common to all extensions;
  - argumentative explanations for graph hypotheses?

- Can this paper’s transformation strategy scale beyond hand-crafted toy cases without Greedy-style restrictions?

- What is the smallest causal toy case where Assumption Introduction produces a meaningful causal exception rather than an arbitrary technical device?

- Can non-stratified ABA Learning be useful for causal graph reasoning, or would it create interpretation problems?

- How should the project distinguish useful causal generalisation from mere symbolic overfitting?