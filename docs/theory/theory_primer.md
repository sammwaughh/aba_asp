# **Causal ABA Learning Theory Primer**

## **Project aim**

This repository supports experimentation for the Causal ABA Learning project.

The project investigates how two lines of work can interact:

1. **Causal ABA**: representing causal-discovery evidence inside Assumption-Based Argumentation (ABA), so that stable extensions correspond to candidate causal graph hypotheses.
2. **ABA Learning**: learning or transforming ABA frameworks from background knowledge and positive/negative examples using transformation rules.

The core research question is not fixed as a single implementation target. The project explores what it could mean to combine these methods. In particular, it asks what learning should operate on in a causal ABA setting: causal relations, conditional-independence evidence, assumptions, rules, constraints, examples, graph hypotheses, or transformation choices.

The agent should not decide this theoretical direction independently. Its role is to help inspect code, implement small experiments, run tests, document results, and expose consequences of modelling choices.

## **Direction 1: Apply ABA Learning to causal discovery**

The first direction is to apply ABA Learning techniques to causal discovery.

Causal discovery aims to infer causal graph structure from data. In a Causal ABA setting, candidate graph statements can be represented by ABA assumptions, and graph-theoretic constraints can be represented by ABA rules. This suggests studying causal discovery as a structured rule-learning or framework-learning problem.

Possible experimental interpretations include:

- learning causal assumptions corresponding to candidate edges;
- learning rules that support or defeat causal claims;
- learning ABA structures whose accepted extensions correspond to candidate DAGs;
- using positive and negative examples to constrain which causal claims or graph structures should be accepted;
- testing whether transformation rules such as Rote Learning, Folding, Assumption Introduction, or Subsumption can recover useful causal-argumentative structure in small cases.

This direction should begin with very small controlled examples. The first experiments should not aim to solve general causal discovery. They should test whether a proposed learning target is coherent.

## **Direction 2: Use causal structure to guide ABA Learning**

The second direction is to use causal structure to guide ABA Learning.

ABA Learning can have a large and highly nondeterministic transformation space. Transformation rules may be applicable in many alternative ways, and different transformation sequences may produce different learnt ABA frameworks. Greedy ABA Learning shows one way to control this problem in case-based reasoning by imposing a deterministic transformation strategy.

Causal discovery provides possible sources of domain-specific structure that may guide ABA Learning. Examples include:

- causal ordering constraints;
- acyclicity constraints;
- graph-compatibility constraints;
- prior causal assumptions;
- known absence of edges;
- conditional-independence or dependence evidence;
- restrictions on which transformations are allowed;
- preferences over simpler or more graph-compatible learnt frameworks.

This direction should test whether causal information can reduce ambiguity or search complexity in ABA Learning, while preserving interpretability and correctness.

## **Causal graph essentials**

A causal graph represents variables as nodes and causal hypotheses as directed edges. In the setting used here, the primary graphical object is a directed acyclic graph (DAG).

Core terminology:

- `V`: finite set of variables.
- `G = (V,E)`: graph over variables.
- `x -> y`: directed edge from `x` to `y`, interpreted as the hypothesis that `x` is a direct cause of `y`, relative to the variables included.
- `DAG`: directed graph with no directed cycles.
- `x _||_G y | Z`: `x` and `y` are d-separated in graph `G` given conditioning set `Z`.
- `x _not||_G y | Z`: `x` and `y` are d-connected in graph `G` given `Z`.
- `x _||_ y | Z`: statistical conditional independence in the distribution.
- `x _not||_ y | Z`: statistical conditional dependence in the distribution.

The Markov condition links graph to distribution:

- if `x _||_G y | Z`, then `x _||_ y | Z`.

Faithfulness gives the converse direction:

- if `x _||_ y | Z`, then `x _||_G y | Z`.

Together, these assumptions allow conditional-independence evidence to be treated as constraints on possible causal graphs.

Important limitation: conditional-independence information may identify only a Markov equivalence class rather than a unique DAG.

## **Deterministic causal mechanisms**

For the current M1.3 Bucket 3 investigation, a fixture may place all exogenous
randomness in the root variables and define every non-root variable as a
deterministic function of its parents. In structural-equation notation,

```text
R_i = f_i(U_i)                 for a root R_i
V_j = f_j(PA_j)               for a non-root V_j
```

where the root noise variables are mutually independent and have non-degenerate
distributions. Equivalently, each non-root conditional-probability-table row is
a point mass. Such a model can still satisfy causal sufficiency and the causal
Markov factorisation. Its observational distribution generally has structural
zeros, however, so it is not strictly positive.

Determinism does not by itself prove ordinary faithfulness. A deterministic
relation can induce additional distributional independences that are not
d-separations in the generating DAG, including independences that arise because
a variable becomes constant after conditioning. Therefore each concrete
fixture must be audited against its exact induced population distribution. A
fixture certificate should distinguish:

- graph-implied d-separations;
- statistical independences in the exact population;
- parent configurations that are formally defined by the mechanism;
- configurations with positive population probability; and
- configurations observed in a particular finite sample.

For discrete variables, conditional independence must be tested only on
conditioning assignments of positive probability. Zero-probability assignments
do not supply observational evidence about the corresponding conditional.

The standard Markov-equivalence class and CPDAG remain useful references for
what ordinary conditional-independence information can identify. They are not
automatically the final recovery object for deterministic models: deterministic
clusters may require a modified equivalence-class characterisation or additional
assumptions. In particular, if the only relation is (A \to B) with (B:=A),
observational data do not orient that two-node edge. A larger graph may orient
it through other structure, but that must be justified fixture by fixture.

Three recovery questions must remain separate:

1. whether the graph is identifiable from the population distribution;
2. whether the deterministic mechanism has a rule representation corresponding
   to the generating parents; and
3. whether ABA Learning recovers such rules from its encoded finite sample.

The current repository implements exact fixture analysis and target-wise ABA
Learning. It does not implement deterministic causal discovery algorithms or a
learned-rule-to-CPDAG decoder.

## **ABA essentials**

Assumption-Based Argumentation (ABA) is a structured argumentation formalism.

An ABA framework is usually written as:

```
F = <L, R, A, contrary>
```

where:

- `L` is a formal language;
- `R` is a set of rules;
- `A` is a set of assumptions;
- `contrary` maps each assumption to a sentence that attacks it.

A rule has the form:

```
head <- body_1, ..., body_n
```

A fact is a rule with empty body:

```
head <-
```

Assumptions are defeasible premises. They may be used in arguments, but they can be attacked if their contraries are derived.

An argument is a derivation of a claim from rules and assumptions.

A set of assumptions attacks an assumption `alpha` when it derives the contrary of `alpha`.

A stable extension is a coherent set of accepted assumptions that attacks every assumption outside it. In this project, stable extensions are especially important because both Causal ABA and the ASP-based ABA Learning work use stable-extension reasoning.

Accepted claims are claims derivable from the assumptions in an extension.

Cautious acceptance means accepted with respect to every stable extension.

Brave acceptance means accepted with respect to at least one stable extension, or in selected-extension presentations, accepted with respect to a chosen stable extension satisfying the learning task.

## **Causal ABA essentials**

Causal ABA instantiates ABA for causal-graph reasoning.

The base framework contains defeasible assumptions for possible graph statements.

Typical assumptions include:

```
arr_xy
```

meaning that the graph contains the directed edge `x -> y`, and:

```
noe_xy
```

meaning that there is no edge between `x` and `y`.

For each unordered pair `{x,y}`, the alternatives are:

```
arr_xy
arr_yx
noe_xy
```

These alternatives are mutually incompatible. The framework contains rules deriving contraries when incompatible edge-status assumptions are accepted together.

Acyclicity is enforced by rules that attack arrow assumptions forming directed cycles. Stable extensions therefore exclude accepted arrow sets that form directed cycles.

A stable extension determines a graph:

```
G_Delta = (V, E_Delta)
E_Delta = {(x,y) | arr_xy is in Delta}
```

where `Delta` is a stable extension.

Under the Causal ABA construction, accepted independence assumptions correspond to d-separation in the graph induced by the same extension:

```
(x _||_ y | Z) in Delta  iff  x _||_G_Delta y | Z
```

Independence assumptions are defeated when the accepted arrows support an active path between the variables given the conditioning set.

Dependence information is more subtle. Dependence is not merely the rejection of independence. A dependence fact `x _not||_ y | Z` requires the induced graph to contain at least one active path between `x` and `y` given `Z`. In the full construction, this requires additional machinery, such as blocked-path assumptions and rules.

External statistical or expert information can be imposed as facts or constraints when it is to be treated as fixed input. If such information is uncertain or conflicting, it may instead be treated defeasibly or relaxed through weak constraints in an ASP implementation.

ABA-PC is the ASP implementation of the Causal ABA approach. It uses conditional-independence/dependence information from Majority-PC and can handle hard or weak constraints. It should not be confused with the abstract Causal ABA formalism itself.

## **ABA Learning essentials**

ABA Learning studies how to transform or extend an ABA framework from background knowledge and positive/negative examples.

Input:

- an initial ABA framework representing background knowledge;
- positive examples `E+`;
- negative examples `E-`;
- a chosen semantics or reasoning mode.

Output:

- a learnt ABA framework that accepts positive examples and does not accept negative examples under the chosen consequence relation.

The learnt framework may contain:

- new rules;
- new assumptions;
- new contraries;
- transformed or generalised rules;
- deleted or subsumed rote rules.

ABA Learning is not ordinary parameter fitting. It is symbolic framework transformation.

Important transformation rules:

### **Rote Learning**

Adds example-specific rules, often to ensure that positive examples become derivable.

Example:

```
p(X) <- X = a
```

for positive example `p(a)`.

Rote Learning can solve examples directly, but tends to memorise rather than generalise.

### **Folding**

Generalises rules by replacing a body fragment with an existing background predicate.

Schematically:

```
H <- B1, B2
K <- B1
```

may allow:

```
H <- K, B2
```

Folding supports intensional learning by reusing background concepts.

### **Assumption Introduction**

Makes a rule defeasible by adding a new assumption to its body.

```
H <- B
```

may become:

```
H <- B, alpha
```

where `alpha` is a new assumption.

Exceptions can then be represented by rules deriving the contrary of `alpha`.

This introduces undercutting attacks into the learnt framework.

### **Subsumption / Fact Subsumption**

Removes rules made redundant by more general rules.

Fact Subsumption removes rote or example-specific facts when the learning task is still solved without them.

This prevents the learnt framework from retaining unnecessary memorisation once general rules explain the examples.

## **ASP and implementation essentials**

Answer Set Programming (ASP) is a declarative logic-programming paradigm based on stable-model semantics.

In this project, ASP is primarily an implementation route. It may be used to:

- compute stable extensions;
- encode ABA frameworks;
- encode Causal ABA constraints;
- search for candidate learnt frameworks;
- impose hard constraints;
- impose weak constraints with optimisation;
- run small controlled experiments.

Do not confuse ASP implementation with the theory being learnt.

ABA Learning via ASP uses the correspondence between stable extensions of suitable ABA frameworks and answer sets of logic programs.

Causal ABA/ABA-PC uses ASP to compute graph-compatible stable extensions and handle inconsistent test information through hard or weak constraints.

For implementation:

- keep handwritten ASP separate from generated ASP;
- comment the logical role of each rule;
- include tiny examples with expected answer sets;
- use deterministic toy cases before quantitative experiments;
- record exact commands and outputs.

## **What not to confuse**

Do not confuse:

- Causal ABA with ABA Learning.
- ABA-PC with Causal ABA as an abstract framework.
- assumptions with facts.
- rules with assumptions.
- contraries with negation-as-failure.
- attacks with ordinary logical contradiction.
- rejection of an independence assumption with proof of dependence.
- d-separation in a graph with statistical independence in data.
- graph compatibility with statistical truth.
- learning graph output with learning ABA transformation rules.
- learning causal edges with learning an ABA framework whose extensions correspond to graphs.
- ASP encodings with the formal objects they implement.
- Greedy ABA Learning with general ABA Learning.
- qualitative toy-case exploration with quantitative benchmarking.

Critical modelling distinction:

```
Causal ABA asks:
Given causal-discovery evidence, which graph hypotheses are compatible under ABA semantics?

ABA Learning asks:
Given background knowledge and examples, how can an ABA framework be transformed so that examples are accepted or rejected as required?

Causal ABA Learning asks:
How can these two processes interact?
```

## **Likely experiment types**

### **Qualitative toy-case experiments**

Purpose: understand modelling possibilities.

Examples:

- three-variable chain: `x -> y -> z`;
- fork: `x <- z -> y`;
- collider: `x -> z <- y`;
- rain/wet-roof/wet-street/watering-plants example;
- inconsistent conditional-independence reports;
- simple graph where one edge must be learnt;
- simple ABA Learning task where causal constraints restrict transformations.

Expected outputs:

- accepted assumptions;
- stable extensions;
- induced graphs;
- accepted/rejected examples;
- explanation of why one graph/framework is selected.

### **Structural representation experiments**

Purpose: test how causal objects should be represented as ABA Learning examples.

Possible questions:

- Should examples be edge claims?
- Should examples be independence/dependence claims?
- Should examples be graph-level compatibility claims?
- Should examples be accepted/rejected causal conclusions?
- Should learning target rules, assumptions, or constraints?

Expected outputs:

- candidate representation;
- smallest example showing it works or fails;
- clear interpretation of failure modes.

### **Search-control experiments**

Purpose: test whether causal constraints reduce ABA Learning ambiguity.

Possible questions:

- Does acyclicity rule out transformation outputs?
- Does a causal order reduce the hypothesis space?
- Do graph constraints prevent negative examples from becoming accepted?
- Does causal information make Greedy-style learning more controlled?

Expected outputs:

- number of candidate frameworks;
- number of stable extensions;
- runtime;
- accepted/rejected examples;
- qualitative explanation of reduced ambiguity.

### **Quantitative experiments**

Purpose: benchmark once a modelling choice is coherent.

Possible inputs:

- synthetic DAGs;
- sampled conditional-independence/dependence reports;
- noisy finite-sample test outputs;
- small benchmark datasets.

Possible metrics:

- structural Hamming distance;
- precision/recall/F1 for edges;
- number of compatible graphs;
- stability across random seeds;
- runtime;
- number of transformations;
- number of stable extensions;
- number of facts/constraints dropped or relaxed.

Quantitative experiments should come after qualitative toy cases.

## **Expected terminology**

Use these terms consistently:

- variable;
- graph;
- DAG;
- edge;
- arrow;
- no-edge;
- conditional independence;
- conditional dependence;
- d-separation;
- d-connection;
- active path;
- stable extension;
- assumption;
- contrary;
- rule;
- fact;
- attack;
- accepted claim;
- cautious acceptance;
- brave acceptance;
- ABA framework;
- Causal ABA framework;
- ABA Learning task;
- transformation rule;
- Rote Learning;
- Folding;
- Assumption Introduction;
- Subsumption;
- Fact Subsumption;
- ASP encoding;
- answer set;
- hard constraint;
- weak constraint;
- induced graph;
- compatible graph;
- learnt framework.

Avoid vague phrases such as:

- “the AI learns causality”;
- “the framework learns a graph” unless the exact learning target is specified;
- “the rule discovers the cause”;
- “independence is false, so dependence is proved”;
- “ASP learns the framework” unless the implementation really performs the search.

## **Current experimental priority**

The immediate priority is to investigate whether ABA Learning techniques can be applied to causal discovery in small controlled cases.

Initial work should focus on qualitative experiments.

The first useful experiment should answer a minimal modelling question, not solve the whole project. For example:

```
Can we formulate a three-variable causal-discovery toy problem as an ABA Learning task such that the learnt or transformed ABA framework accepts the intended causal claims and rejects the unintended ones?
```

The agent should help by:

1. mapping the existing repo;
2. identifying existing Causal ABA, ABA Learning, ASP/clingo, example, and test code;
3. proposing the smallest experiment that can run;
4. implementing only after the user approves the plan;
5. recording the experiment before and after execution;
6. reporting exact commands and outputs;
7. avoiding unsupported theoretical interpretation.

The user is responsible for deciding whether an experimental result is theoretically meaningful.
