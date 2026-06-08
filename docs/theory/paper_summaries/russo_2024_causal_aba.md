# Paper summary: Russo, Rapberger, Toni 2024 — Argumentative Causal Discovery

## Role in this project

This is the canonical Causal ABA paper for the project.

It provides the target representation for causal-discovery evidence inside Assumption-Based Argumentation (ABA). The central contribution is to formalise causal graph reasoning in ABA, using:

- assumptions for candidate causal relations and conditional-independence statements;
- rules for graph-theoretic constraints such as edge consistency, acyclicity and d-separation;
- argumentation semantics to compute compatible causal graph hypotheses.

The paper is directly relevant to the project because it gives one side of the intended integration:

text Causal ABA = represent and reason over causal-discovery evidence inside ABA. ABA Learning = learn or transform ABA frameworks from examples. Causal ABA Learning = investigate how these two can interact.

In this project, Causal ABA should be treated as the main formal source for:

- how causal graph hypotheses can be represented as ABA assumptions;
- how accepted assumptions induce DAGs;
- how conditional-independence claims correspond to d-separation;
- how external statistical or expert causal information can constrain extensions;
- how ASP can implement stable-extension reasoning for causal ABA.

This paper does not define ABA Learning. It constructs Causal ABA frameworks from externally supplied causal-discovery information and computes compatible graph hypotheses. It does not learn the ABA framework using transformation rules from examples.

## Core definitions

### Causal graph

A causal graph is a graph over a finite variable set V, where directed edges represent causal hypotheses.

The paper focuses on causal graphs admitting a DAG structure.

Important graph concepts:

- G = (V,E): graph over variables.
- x -> y: directed edge from x to y.
- DAG: directed graph with no directed cycles.
- path: sequence of adjacent nodes.
- directed path: path following arrow direction.
- v-structure: unshielded triple where two non-adjacent variables point into a common collider.
- Markov equivalence class: set of DAGs entailing the same conditional independences.
- CPDAG: completed partially directed acyclic graph representing a Markov equivalence class.

The paper assumes faithfulness and causal sufficiency in its main setting: all independencies in the data are compatible with some DAG structure, and there are no latent confounders.

### Conditional independence and dependence

For pairwise disjoint sets X, Y, Z:

text X *||* Y | Z

means that X and Y are conditionally independent given Z.

text X *not||* Y | Z

means that X and Y are conditionally dependent given Z.

For singleton variables, the paper writes expressions such as:

text x *||* y | Z

Conditional independence is symmetric, so:

text x *||* y | Z

and:

text y *||* x | Z

are identified.

### Active path and d-separation

A path between x and y is Z-active if:

- every non-collider on the path is outside Z;
- every collider on the path is in Z or has a descendant in Z.

Two nodes are d-connected given Z if there exists a Z-active path between them.

Two nodes are d-separated given Z if they are not d-connected.

The notation:

text x _||_G y | Z

means that x and y are d-separated in graph G given Z.

### ABA framework

The paper recalls an ABA framework as:

text D = (L, R, A, contrary)

where:

- L is a language;
- R is a set of rules;
- A is a set of assumptions;
- contrary maps each assumption to a sentence in the language.

For Causal ABA, assumptions are used for possible graph facts and conditional-independence claims.

### Edge assumptions

For distinct variables x,y in V, Causal ABA uses assumptions:

text arr_xy

meaning that the graph contains the directed edge x -> y.

For each pair of variables, it also uses a no-edge assumption:

text noe_xy

meaning that there is no edge between x and y.

For each unordered pair {x,y}, the possible edge states are:

text arr_xy arr_yx noe_xy

These are mutually incompatible.

### DAG framework D_dag

The first Causal ABA component captures DAG structure.

Its assumptions include:

text A_arr = {arr_xy | x,y in V, x != y}

and no-edge assumptions:

text noe_xy

The rules enforce:

1. Edge-status consistency
    
    The framework prevents accepting incompatible alternatives such as arr_xy and arr_yx, or arr_xy and noe_xy.
    
2. Acyclicity
    
    Directed cycles attack the arrows that form them. This prevents stable/preferred extensions from containing a full directed cycle.
    

For preferred and stable semantics, the paper proves a one-to-one correspondence between DAGs and extensions of this DAG-capturing ABA framework.

### Independence assumptions

The Causal ABA framework extends the DAG encoding with assumptions of the form:

text x *||* y | Z

These represent defeasible conditional-independence claims.

The set of independence assumptions is:

text A_ind = {(x *||* y | Z) | Z subseteq V, x,y in V \ Z, x != y}

### Directed-path and edge rules

The framework includes graph rules for deriving:

- directed paths;
- existence of an edge;
- no-edge contraries.

Typical derived predicates include:

text dpath_xy e_xy

where dpath_xy indicates a directed path from x to y, and e_xy indicates an edge between x and y.

### Collider-trees

The paper introduces collider-trees to encode d-separation in ABA.

A collider-tree generalises an ordinary path by including branches from collider nodes to conditioned descendants. This allows the ABA rules to capture the standard active-path condition for d-separation.

A collider-tree is Z-active when it witnesses that the relevant path is active given Z.

### Causal ABA framework D_ds

The Causal ABA framework for d-separation is:

text D_ds = (A_ds, R_ds, contrary)

where:

text A_ds = A_dag union A_ind R_ds = R_dag union R_graph union R_act

The rules in R_act derive the contrary of an independence assumption when there is a Z-active collider-tree between the variables.

For stable and preferred semantics, the paper proves:

text (x *||* y | Z) in S  iff  x _||_G y | Z

where:

- S is an extension;
- G is the graph induced by the accepted arrow assumptions in S.

This is the key representation theorem for the project.

### Integrating causal knowledge

External causal-discovery information can be integrated as facts.

Examples:

text x *||* y | Z <- arr_xy <-

Adding an independence or arrow fact can force extensions to respect that information.

Dependence information is more subtle. Adding the contrary of an independence statement is not enough to guarantee that the induced graph contains an active path. To integrate dependence facts soundly, the paper introduces blocked-path assumptions and additional rules.

### Blocked-path assumptions

For dependence evidence, the framework introduces assumptions such as:

text bp_p|Z

meaning that path p is blocked given Z.

The framework then uses rules ensuring that if variables are independent, all paths between them are blocked. Conversely, dependence requires at least one active path.

This distinction matters for implementation: dependence must be represented constructively, not simply as failure or rejection of independence.

### Extended causal ABA framework D_csl

The extended Causal ABA framework incorporates dependence facts using blocked-path assumptions and additional rules.

For a set T of independence, dependence and arrow facts, the resulting framework is written informally as:

text D_csl^T

The key guarantee is that, under preferred or stable semantics, accepted independence assumptions correspond to d-separation in the graph induced by the extension.

### ABA-PC

ABA-PC is the ASP implementation of the Causal ABA method.

It instantiates the Causal ABA algorithm using Majority-PC to source independence/dependence facts.

Input:

- variables;
- conditional-independence/dependence test results;
- possible domain/expert knowledge;
- weights or confidence information where used.

Output:

- candidate DAGs compatible with the selected causal information;
- stable extensions / answer sets corresponding to graph hypotheses.

The implementation uses ASP because the relevant Causal ABA frameworks may be non-flat and standard ABA solvers are not directly applicable.

## Implementation-relevant concepts

### Core data structures

A toy implementation should represent:

text Variable Arrow assumption: arr(x,y) No-edge assumption: noe(x,y) Independence assumption: indep(x,y,Z) Dependence evidence: dep(x,y,Z) Rule Contrary Extension Induced graph

For Python:

python @dataclass(frozen=True) class Arrow:     source: str     target: str  @dataclass(frozen=True) class NoEdge:     x: str     y: str  @dataclass(frozen=True) class Independence:     x: str     y: str     conditioning: frozenset[str]

Ensure symmetry for no-edge and independence statements.

### Edge-state alternatives

For every unordered pair {x,y}, exactly one of the following should be selected in a stable extension of the DAG layer:

text arr_xy arr_yx noe_xy

This is central for inducing a graph from a stable extension.

### Induced graph

Given an extension S, define the induced graph:

text G_S = (V, E_S) E_S = {(x,y) | arr_xy in S}

This notation may be implementation-defined; the paper phrases the correspondence in terms of extensions corresponding to DAGs.

### Acyclicity checking

Acyclicity can be implemented in two ways:

1. Directly in Python by checking whether accepted arrows contain a directed cycle.
2. In ASP/ABA by encoding cycle attacks or constraints.

For toy experiments, direct acyclicity checking is acceptable if the experiment is about representation or learning target design.

For faithful Causal ABA implementation, acyclicity should be encoded through the framework or ASP constraints in line with the paper.

### D-separation checking

For early experiments, d-separation can be implemented by:

- using a simple Python d-separation function;
- comparing accepted independence assumptions against d-separation in the induced graph;
- later replacing this with the paper’s collider-tree encoding or an ASP encoding.

The paper’s formal Causal ABA construction uses collider-trees to internalise active-path reasoning within ABA.

### Independence attacks

If an induced graph contains a Z-active path between x and y, then the corresponding independence assumption:

text x *||* y | Z

is attacked.

This is the main bridge from graph structure to argumentation.

### Dependence handling

Do not implement dependence as:

text dep(x,y,Z) = not indep(x,y,Z)

unless the experiment explicitly states this as a simplified approximation.

In the paper, dependence evidence requires ensuring that at least one active path remains. This requires blocked-path machinery in the full formal construction.

### External evidence

External information may include:

- statistical test outputs;
- Majority-PC outputs;
- expert arrow claims;
- expert no-edge claims;
- independence claims;
- dependence claims.

When treated as fixed input, such information can be imposed as facts or constraints.

When uncertain or conflicting, ABA-PC may use hard or weak constraints and weights.

### Hard and weak constraints

Hard constraints rule out extensions/answer sets violating the imposed evidence.

Weak constraints allow violations at a cost.

Weights guide which reported facts are retained when finite-sample test outputs are mutually inconsistent.

### ASP implementation

ABA-PC uses ASP because the Causal ABA framework can be non-flat: assumptions such as independence and arrow assumptions may appear in heads of rules after facts are added.

Implementation should keep separate:

- generated ASP from causal variables/facts;
- generic ASP encoding of causal ABA rules;
- experiment-specific input facts;
- solver configuration;
- output parsing.

### Useful debugging outputs

For each small experiment, output:

- variables;
- external facts;
- accepted arrow assumptions;
- accepted no-edge assumptions;
- accepted independence assumptions;
- induced graph;
- active paths or d-separation checks;
- stable extension / answer set;
- dropped or relaxed facts if weak constraints are used.

## What not to confuse

### Causal ABA is not ABA Learning

Causal ABA constructs an ABA framework from causal-discovery inputs and computes compatible graph hypotheses.

ABA Learning learns or transforms ABA frameworks from examples.

This paper provides the Causal ABA side of the project, not the ABA Learning side.

### Causal ABA is not merely PC

The paper may use Majority-PC to source facts in ABA-PC, but Causal ABA is not PC itself. It is an argumentation-based reasoning layer over causal-discovery evidence.

### ABA-PC is not identical to abstract Causal ABA

Causal ABA is the formal framework.

ABA-PC is the ASP implementation using Majority-PC facts, hard/weak constraints and weights.

### Dependence is not just rejection of independence

This is critical.

Rejecting or attacking:

text x *||* y | Z

does not automatically construct a graph with an active path between x and y given Z.

Dependence evidence requires at least one active path. The paper introduces blocked-path assumptions and extra rules for this.

### Statistical independence is not d-separation

Statistical conditional independence is a property of the distribution or test output.

D-separation is a graphical relation.

They are linked under Markov and faithfulness assumptions, but they are not the same object.

### Compatibility is not truth

A graph compatible with reported evidence is not necessarily the true causal graph. Finite-sample test errors may make reported evidence wrong or inconsistent.

### A stable extension is not just any graph

A stable extension is a set of accepted assumptions satisfying the ABA semantics. It induces a graph through accepted arrow assumptions.

### Complete semantics is not enough for the main correspondence

The paper proves the key one-to-one DAG correspondence for preferred and stable semantics. Complete semantics can admit extensions that do not include all independence assumptions corresponding to the disconnected graph.

For this project, stable semantics are the safest default.

### No-edge assumptions are not the same as absence from an extension

For complete semantics, an absent arrow assumption does not necessarily imply an accepted no-edge assumption. For stable/preferred semantics in the relevant construction, the correspondence is cleaner.

### Expert knowledge need not always be a hard fact

The paper integrates external information as facts in the formal development and uses hard/weak constraints in the implementation. In project experiments, decide explicitly whether expert/statistical information is hard, defeasible, weighted or relaxable.

### Causal sufficiency assumption matters

The paper’s main setting assumes no latent confounders. Do not silently extend the implementation to latent-variable causal discovery unless the representation has been changed.

## Relevant sections in the PDF

Use the following sections as reference points:

- Abstract
    
    States the high-level aim: use ABA and causality theories to learn graphs reflecting causal dependencies, with ASP experiments.
    
- Section 1: Introduction
    
    Motivates finite-data errors in causal discovery, introduces the rain/wet-roof/wet-street/watering-plants example, positions Bromberg and Margaritis as related work, and summarises the Causal ABA workflow.
    
- Figure 1
    
    Shows the overall workflow: statistical methods and expert domain knowledge feed into Causal ABA, which performs non-monotonic reasoning and outputs compatible causal graphs.
    
- Section 2: Preliminaries
    
    Defines graph terminology, conditional independence/dependence, d-separation, Markov/faithfulness assumptions, conditional-independence tests, and ABA preliminaries.
    
- Section 2.1: Causal Graphs
    
    Key source for d-separation, d-connection, conditional independence, Markov equivalence and CPDAG terminology.
    
- Section 2.2: Assumption-Based Argumentation
    
    Defines ABA frameworks, tree-derivability, attacks, conflict-free sets, closedness, admissibility and stable extensions as used by the paper.
    
- Section 3: Capturing Causal Graphs with ABA
    
    Main theoretical section. Defines Causal ABA.
    
- Section 3.1: Causal ABA
    
    Defines the DAG-capturing framework, arrow assumptions, no-edge assumptions, acyclicity rules, independence assumptions, collider-trees and the d-separation correspondence.
    
- Definition 3.1
    
    Defines D_dag, the ABA framework for edge choices and acyclicity.
    
- Example 3.2
    
    Concrete three-variable illustration of the acyclicity attack structure.
    
- Proposition 3.3, Lemma 3.5, Corollary 3.6
    
    Establish correspondence between extensions and DAGs, especially for preferred/stable semantics.
    
- Definition 3.7
    
    Defines collider-trees.
    
- Definition 3.9
    
    Defines the Causal ABA framework D_ds for d-separation.
    
- Proposition 3.11
    
    Key theorem: in preferred/stable extensions, accepted independence assumptions correspond to d-separation in the induced graph.
    
- Section 3.2: Integrating Causal Knowledge
    
    Explains how external causal information is integrated as facts and why dependence facts require additional blocked-path machinery.
    
- Definition 3.15
    
    Introduces extra rules for blocked paths and active paths.
    
- Definition 3.17
    
    Defines the extended Causal ABA framework for incorporating dependence facts.
    
- Proposition 3.18 and Corollary 3.19
    
    Establish that the extended framework preserves the independence/d-separation correspondence after integrating facts.
    
- Section 4: Implementation
    
    Explains the ABA-PC implementation in ASP.
    
- Section 4.1: Encoding Causal ABA in ASP
    
    Relevant for clingo/ASP implementation and non-flat ABA considerations.
    
- Remark 4.2
    
    Important warning: the causal ABAF may be non-flat, so standard ABA solvers are not directly applicable; the paper uses ASP under stable semantics.
    
- Later implementation and experiment sections
    
    Use when reproducing or comparing ABA-PC behaviour, especially Majority-PC input, hard/weak constraints, weights and benchmark results.
    

## Open questions for this project

This paper establishes Causal ABA, but it leaves open the learning-side questions that motivate this repository.

Key open questions:

- What exactly should ABA Learning learn in a Causal ABA setting?
    - edge assumptions?
    - no-edge assumptions?
    - independence assumptions?
    - dependence-supporting rules?
    - d-separation-related rules?
    - blocked-path machinery?
    - entire Causal ABA frameworks?
    - transformations of a fixed causal ABA background?
- Should the Causal ABA construction be treated as fixed background knowledge, with only facts/examples learnt?
- Can ABA Learning recover causal relations from positive/negative examples without hard-coding all graph constraints?
- Can ABA Learning induce rules whose stable extensions correspond to candidate causal graphs?
- How should conditional-independence and dependence test outputs be converted into ABA Learning examples?
- Should positive examples be:
    - accepted edges?
    - accepted independences?
    - accepted graph hypotheses?
    - accepted causal conclusions?
    - compatibility constraints?
- Should negative examples be:
    - forbidden edges?
    - forbidden independences?
    - incorrect graph hypotheses?
    - rejected causal conclusions?
- Can causal graph constraints such as acyclicity and d-separation restrict or guide ABA Learning transformations?
- Can Greedy ABA Learning’s search-control idea be adapted using causal structure rather than case-based feature structure?
- How should dependence be handled in a learning setting, given that dependence requires constructive active-path support rather than mere failure of independence?
- Should early experiments use the full blocked-path machinery, or a simplified dependence-free setting?
- Can the project begin with only independence and arrow facts before introducing dependence facts?
- Can the ASP implementation of Causal ABA be reused as a solver backend for ABA Learning experiments?
- How should learned frameworks be evaluated?
    - compatibility with intended graph;
    - edge precision/recall;
    - structural Hamming distance;
    - stability across noisy test outputs;
    - number of extensions;
    - interpretability of attacks;
    - transformation-rule count;
    - runtime and grounding size.
- How should finite-sample uncertainty be represented when the learning process itself may introduce defeasible structure?