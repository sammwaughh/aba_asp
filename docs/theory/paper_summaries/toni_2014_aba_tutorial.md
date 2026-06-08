# Paper summary: Toni 2014 — A tutorial on Assumption-Based Argumentation

## Role in this project

This paper is the main tutorial reference for Assumption-Based Argumentation (ABA). It should be treated as the canonical source for the basic ABA concepts used throughout the project.

Its role is to ground the implementation and terminology for:

- ABA frameworks;
- rules;
- assumptions;
- contraries;
- arguments;
- attacks;
- ABA semantics;
- accepted or “winning” sets of assumptions;
- the relationship between assumption-level and argument-level reasoning.

For this project, the paper is not primarily a learning paper and not a causal-discovery paper. It provides the formal argumentation foundation on which both Causal ABA and ABA Learning build.

Use this paper when checking whether code or documentation correctly distinguishes:

- rules from assumptions;
- assumptions from ordinary facts;
- contraries from negation;
- derivability from acceptability;
- argument-level attacks from assumption-level attacks;
- semantic acceptance from mere syntactic derivability.

## Core definitions

### ABA framework

An ABA framework is a tuple:

text F = <L, R, A, contrary>

where:

- L is a formal language;
- R is a set of rules in a deductive system;
- A is a non-empty set of assumptions, with A subseteq L;
- contrary is a total mapping from assumptions into the language.

A rule has the form:

text s0 <- s1, ..., sm

where:

- s0 is the head;
- s1, ..., sm are the body;
- if m = 0, the rule has empty body and is a fact.

The language L may be propositional, first-order, modal, or otherwise specified by the ABA instance. ABA does not require a specific object language.

### Assumptions

Assumptions are special sentences in the language. They are defeasible premises: they may be hypothesised in arguments, but they can be attacked through derivations of their contraries.

Assumptions are the weak points of arguments. ABA semantics operate by determining which sets of assumptions can be accepted.

A flat ABA framework is one in which no assumption occurs as the head of a rule. In flat ABA, assumptions can be hypothesised but not derived by rules.

### Contraries

Each assumption has a contrary.

If a is an assumption, its contrary is written informally as:

text contrary(a)

or mathematically as:

text \bar{a}

The contrary of an assumption is the claim that attacks the assumption when derived.

Important: contrary is not the same as classical negation. The language may not even contain a negation symbol. The contrary mapping is a flexible attack interface.

Contraries are:

- defined only for assumptions;
- not necessarily symmetric;
- not necessarily classical negations;
- not necessarily assumptions themselves.

### Arguments

An argument is a deduction of a claim from rules, supported by a set of assumptions.

Informally:

text A |- s

means that claim s is derivable using rules and assumptions from A.

In ABA, arguments are not primitive objects. They are generated from:

- rules;
- assumptions;
- deductions.

This distinguishes ABA from abstract argumentation, where arguments and attacks are given directly.

### Attacks

An argument attacks another argument when its claim is the contrary of an assumption used in the support of the attacked argument.

At the assumption-set level:

text A attacks B

when some argument supported by assumptions in A derives the contrary of some assumption in B.

The tutorial emphasises that ABA can be viewed equivalently at:

- the argument level;
- the assumption-set level;
- a hybrid level where arguments attack assumptions or assumption sets.

For implementation in this project, the assumption-set view is usually the most useful, because Causal ABA and ABA Learning operate naturally over sets of accepted assumptions.

### Semantics

ABA semantics determine which sets of assumptions or arguments are “winning” or acceptable.

The tutorial discusses standard semantics including:

- admissible;
- preferred;
- sceptically preferred;
- complete;
- grounded;
- ideal;
- stable.

For this project, stable semantics are especially important because Causal ABA and the ASP-based ABA Learning papers use stable-extension reasoning.

At the assumption level, a stable set of assumptions is conflict-free and attacks every assumption outside it.

At the argument level, a stable set of arguments does not attack itself and attacks every argument outside it.

The assumption-level and argument-level views are equivalent in ABA.

### Acceptance of claims

A claim is accepted when it is supported by an acceptable or winning set of assumptions/arguments under the chosen semantics.

In this project, use:

- cautious acceptance for acceptance with respect to all relevant extensions;
- brave or credulous acceptance for acceptance with respect to at least one relevant extension, or a selected extension depending on the learning formulation.

## Implementation-relevant concepts

### ABA objects to represent

An implementation should represent at least:

- language atoms or sentences;
- rules;
- assumptions;
- contrary mapping;
- derivability relation;
- attack relation;
- extensions under a chosen semantics;
- accepted claims.

For small experiments, it may be enough to represent sentences as strings or structured atoms. For larger experiments, use explicit dataclasses or typed structures for rules, assumptions and contraries.

### Rule representation

A rule can be represented as:

python Rule(head: Atom, body: tuple[Atom, ...])

A fact is a rule with empty body:

python Rule(head=p, body=())

Do not represent facts as assumptions unless they are genuinely defeasible. Facts are strict derivable information; assumptions are defeasible commitments.

### Assumption representation

An assumption should be distinguishable from an ordinary atom.

For example:

python Assumption(atom=Atom("arr", "x", "y"))

or:

python assumptions = {Atom("arr", "x", "y"), Atom("noe", "x", "y")}

provided the code clearly tracks which atoms are assumptions.

### Contrary mapping

The contrary mapping should be explicit.

Example:

python contrary[assumption] = contrary_atom

Do not infer contraries automatically using string negation unless the formal encoding has defined them that way.

### Attack computation

Attack computation should follow the ABA definition:

1. derive claims from assumptions using rules;
2. check whether any derived claim is the contrary of an assumption in another set;
3. if so, record an attack.

For Causal ABA, this is crucial because attacks on edge assumptions, no-edge assumptions and independence assumptions enforce graph consistency, acyclicity and d-separation behaviour.

### Extension computation

Stable-extension computation may be implemented directly for toy cases or delegated to ASP/clingo.

For toy cases, direct enumeration may be clearer:

1. enumerate subsets of assumptions;
2. check conflict-freeness;
3. check whether the set attacks every assumption outside it;
4. collect stable extensions.

For ASP-based experiments, preserve the mapping between:

- ABA assumptions;
- ASP atoms;
- rules;
- attacks;
- answer sets;
- stable extensions.

### Explanation

Because ABA has an argumentation structure, implementation should try to expose why a claim is accepted or rejected.

Useful debugging outputs:

- accepted assumptions;
- rejected assumptions;
- derived claims;
- attacks;
- stable extensions;
- accepted claims per extension;
- reason why a candidate set fails to be stable.

## What not to confuse

### ABA vs abstract argumentation

Abstract argumentation takes arguments and attacks as primitive.

ABA derives arguments and attacks from:

- rules;
- assumptions;
- contraries.

Do not implement Causal ABA or ABA Learning as arbitrary argument graphs unless the translation from ABA to abstract argumentation is explicit.

### Assumptions vs facts

Assumptions are defeasible. They can be attacked.

Facts are rules with empty body. They are strictly derivable.

Example:

text a

as an assumption means a may be accepted if defensible.

text a <-

as a fact means a is derivable without relying on assumptions.

### Contraries vs negation

A contrary is not necessarily classical negation or negation-as-failure.

The contrary of a may be any sentence in the language.

Do not assume:

text contrary(a) = not a

unless the framework defines that mapping.

### Derivability vs acceptability

A claim being derivable from some assumptions does not by itself mean the claim is accepted.

Acceptance depends on whether the supporting assumptions belong to an acceptable extension under the chosen semantics.

### Argument-level vs assumption-level semantics

ABA can be viewed at both levels.

The assumption-level view is usually more implementation-friendly for this project, because stable extensions are sets of assumptions.

### Stable extension vs arbitrary consistent set

A stable extension is not merely a consistent or conflict-free set.

It must also attack every assumption outside it.

### ABA foundations vs ABA Learning

Toni 2014 explains ABA. It does not define ABA Learning.

ABA Learning uses ABA as the target formalism and learns/transforms ABA frameworks from examples.

### ABA foundations vs Causal ABA

Toni 2014 does not define causal graphs, d-separation or Causal ABA.

Causal ABA instantiates ABA for causal-discovery reasoning.

## Relevant sections in the PDF

Use the following sections as reference points:

- Section 1: Introduction
    
    Explains the role of argumentation in AI, ABA’s relationship to non-monotonic reasoning, and the distinction between ABA and abstract argumentation.
    
- Section 2: A simple illustrative example
    
    Useful for intuition about arguments, attacks, defence and dialectical justification.
    
- Section 3: ABA frameworks
    
    Defines ABA frameworks, rules, assumptions, contraries, flatness and deductions.
    
- Section 4: ABA arguments and attacks
    
    Defines arguments as deductions supported by assumptions and attacks via contraries.
    
- Section 5: ABA semantics
    
    Defines main ABA semantics and explains the argument-level and assumption-level views.
    
- Section 6: Examples of ABA
    
    Gives examples of ABA applied to different reasoning settings.
    
- Section 7: Computational machinery
    
    Describes dispute-based computational techniques for ABA reasoning.
    
- Section 8: FAQs on ABA
    
    Useful for clarifying design choices and common misunderstandings.
    
- Section 9: Conclusion
    
    Summarises the tutorial’s role and scope.
    

## Open questions for this project

This tutorial gives the ABA foundation, but it does not answer the project-specific questions.

Open questions include:

- How should causal-discovery objects be represented as ABA Learning examples?
- Should the learning target be causal assumptions, rules, contraries, facts, constraints, or whole frameworks?
- How should stable extensions be interpreted when a learnt ABA framework is intended to represent causal graph hypotheses?
- How much of the Causal ABA construction should be fixed as background knowledge before learning begins?
- Which parts of Causal ABA, if any, should be learnable?
- Can causal constraints such as acyclicity and d-separation guide transformation-rule application?
- Should experiments use direct ABA extension computation or ASP/clingo from the start?
- How should explanations of accepted/rejected causal claims be surfaced from learnt ABA frameworks?
- How should the implementation distinguish between derivability, attack, acceptance and graph compatibility?
- How should non-flat ABA be handled if generated by learning, given that many computational treatments focus on flat ABA?