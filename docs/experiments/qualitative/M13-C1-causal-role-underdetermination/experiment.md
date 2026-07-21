# M13-C1 — Causal-role underdetermination under learner-input equivalence

## Status

`proposed | planned | implemented | run | analysed | reported`

Current status: `analysed` — Stage 0 passed; both two-cell published-configuration
arms ran; all 4/4 cells were runner-`solved`; pair invariants and learned rules were
inspected; the outcome matched the locked expectations.

## Purpose

Demonstrate, with the smallest controlled example, that unguided ABA Learning cannot
prefer a direct parent over an extensionally equivalent non-parent when the causal graph
is not part of the learner-visible task. The experiment uses two valid causal models
that induce identical tabular BK and examples but assign the direct-parent role of the
target to different predictors.

## Research question

> If two causal models induce identical
> \(\mathcal{T}=(\mathcal{F}_{\mathrm{BK}},E^+,E^-,C)\) for a fixed ABA Learning
> configuration \(C\), but disagree about whether \(x_0\) or \(x_1\) is the direct
> parent of \(x_2\), does the implementation return the same learned framework while
> its graph-relative semantic verdict changes?

## Theoretical motivation

### ABA foundations

The learned object is an ABA framework whose rules, assumptions, contraries, attacks,
and stable-extension consequences determine acceptance. Graph roles are not intrinsic
properties of ordinary `val` predicates in that framework.

### ABA Learning / ABALearn

An ABA Learning task receives an initial framework, positive examples, negative
examples, and a chosen reasoning mode. Its formal solution condition concerns acceptance
of \(E^+\) and rejection of \(E^-\); it does not prefer a predicate because an external
graph labels its variable as a direct parent.

### Causal ABA / argumentative causal discovery

This experiment does not exercise Russo-style arrow/no-edge/independence assumptions,
d-separation reasoning, or stable extensions as candidate DAGs. It illustrates why
additional causal information would be needed for a later guided integration.

### Current `aba_asp/causal` implementation

The current bridge serialises non-target table columns into exact-value BK and passes BK
and \(E^\pm\) to ABA Learning. Handcrafted graph edges are used for graph-relative
evaluation metrics; they are not serialised into the Prolog learning input.

## Relation to ABA Learning

The target is \(x_2\). The background contains exact-value predicates for \(x_0\) and
\(x_1\), in that fixed order. The positive examples are the rows on which \(x_2\neq0\);
the negative example is the row on which \(x_2=0\). Both published configurations are
run:

- ECAI: brave learning, non-deterministic folding, initial token budget 1,
  `folding_selection(any)`, `folding_space(all)`, and `asm_intro(relto)`;
- AAMAS: brave learning, greedy folding, `folding_selection(mgr)`,
  `folding_space(bk)`, and `asm_intro(relto)`.

## Relation to Causal ABA

The experiment tests an information limit of unguided ABA Learning under an external
causal evaluation. It does not perform causal discovery and does not test full Causal
ABA.

## Implementation scope

### Code/config paths

- Fixtures: `causal/experiments/handcrafted_m13.py`
- Registry: `causal/experiments/handcrafted.py`
- Tests: `causal/tests/test_m13_c1_fixtures.py`
- ECAI config:
  `causal/configs/experiments/M13_c1_role_equivalence_ecai2024.yaml`
- AAMAS config:
  `causal/configs/experiments/M13_c1_role_equivalence_aamas2025.yaml`
- Comparison generator: `causal/experiments/m13_c1_summary.py`
- Outputs:
  `causal/outputs/aba_learning/grid/M13_c1_role_equivalence_{ecai2024,aamas2025}/`
- Summary:
  `causal/outputs/aba_learning/grid/M13_c1_role_equivalence_summary.{md,json}`

### Files changed for this experiment

- `causal/experiments/handcrafted_m13.py`
- `causal/experiments/handcrafted.py`
- `causal/tests/test_m13_c1_fixtures.py`
- `causal/configs/experiments/M13_c1_role_equivalence_ecai2024.yaml`
- `causal/configs/experiments/M13_c1_role_equivalence_aamas2025.yaml`
- `causal/experiments/m13_c1_summary.py`
- `docs/experiments/qualitative/M13-C1-causal-role-underdetermination/experiment.md`

### Files inspected before implementation

- `docs/theory/background.tex`
- `docs/theory/theory_primer.md`
- `docs/experiments/qualitative/M1.2-expanded-cell-inspection.md`
- `docs/experiments/qualitative/M1.3-bucket1-claims.md`
- `causal/argcausaldisco_integration.py`
- `causal/experiments/handcrafted.py`
- `causal/experiments/handcrafted_m12x.py`
- `causal/experiments/config.py`
- `causal/experiments/run_grid.py`
- `causal/metrics.py`
- `configs/ecai2024_config.pl`
- `configs/aamas2025_config.pl`

## Dataset / data-generating process

### Shared table

Alphabet \(K=\{0,1,2\}\):

| id | \(x_0\) | \(x_1\) | \(x_2\) |
|---:|--------:|--------:|--------:|
| 1 | 0 | 0 | 0 |
| 2 | 1 | 1 | 1 |
| 3 | 2 | 2 | 2 |

There is no stochastic sampling and no seed dimension.

### Model \(G_0\): parent \(x_0\)

\[
x_0:=u,\qquad x_1:=x_0,\qquad x_2:=x_0,
\]

with edges \(x_0\to x_1\) and \(x_0\to x_2\). Therefore
\(\mathrm{Pa}_{G_0}(x_2)=\{x_0\}\), while \(x_1\) is an extensionally equivalent
sibling.

### Model \(G_1\): parent \(x_1\)

\[
x_1:=u,\qquad x_0:=x_1,\qquad x_2:=x_1,
\]

with edges \(x_1\to x_0\) and \(x_1\to x_2\). Therefore
\(\mathrm{Pa}_{G_1}(x_2)=\{x_1\}\), while \(x_0\) is an extensionally equivalent
sibling.

Both models induce the same ordered table, BK, sample identifiers, target, and
examples. Only the external edge set differs.

## Encoding

### Target variable

Target \(x_2\) is excluded from BK.

### Examples

\[
E^+=\{x_2(2),x_2(3)\},\qquad E^-=\{x_2(1)\}.
\]

### Background knowledge

The learner receives exact-value predicates for \(x_0\) followed by exact-value
predicates for \(x_1\). The BK text must be byte-identical between \(G_0\) and \(G_1\).

## Locked reference hypotheses

For \(G_0\):

```prolog
x2(A) :- x0_val_1(A).
x2(A) :- x0_val_2(A).
```

For \(G_1\):

```prolog
x2(A) :- x1_val_1(A).
x2(A) :- x1_val_2(A).
```

## Expected observable output (locked before runs)

### Input-equivalence invariant

Within each configuration, the two graph-labelled cells must have:

- byte-identical `data.csv`;
- byte-identical `bk.aba`;
- identical \(E^+\) and \(E^-\);
- identical normalised learned \(\delta\);
- identical ASP coverage.

Raw traces may contain cell-specific paths and are therefore compared only after
normalisation. Graph-relative metrics are expected to differ and must not be treated as
learner outputs.

### ECAI expectation

Because the \(x_0\) BK block is first, ECAI is expected to learn the two unary
`x0_val_*` target rules without assumptions. The framework should be an exact
parent-based solution under \(G_0\) and a sibling substitution under \(G_1\).

### AAMAS expectation

AAMAS is expected to learn two positive-row conjunctions containing both \(x_0\) and
\(x_1\), without assumptions. The same parent-plus-sibling rules should occur under both
graphs.

## Commands run

```bash
conda run -n aba-asp python -m pytest \
  causal/tests/test_m13_c1_fixtures.py -q
# → 7 passed in 2.90s

conda run -n aba-asp python -m causal.experiments.run_grid \
  --config causal/configs/experiments/M13_c1_role_equivalence_ecai2024.yaml --dry-run
# → 2 cells planned for M13_c1_role_equivalence_ecai2024

conda run -n aba-asp python -m causal.experiments.run_grid \
  --config causal/configs/experiments/M13_c1_role_equivalence_aamas2025.yaml --dry-run
# → 2 cells planned for M13_c1_role_equivalence_aamas2025

conda run -n aba-asp python -m causal.experiments.run_grid \
  --config causal/configs/experiments/M13_c1_role_equivalence_ecai2024.yaml --no-resume
# → done: completed=2 skipped=0 outcomes={'solved': 2}

conda run -n aba-asp python -m causal.experiments.run_grid \
  --config causal/configs/experiments/M13_c1_role_equivalence_aamas2025.yaml --no-resume
# → done: completed=2 skipped=0 outcomes={'solved': 2}

conda run -n aba-asp python -m causal.experiments.m13_c1_summary
# → wrote M13_c1_role_equivalence_summary.md
# → wrote M13_c1_role_equivalence_summary.json

conda run -n aba-asp python -m pytest \
  causal/tests/test_m13_c1_fixtures.py \
  causal/tests/test_m12x_fixtures.py \
  causal/tests/test_config.py -q
# → 38 passed in 1.66s
```

## Environment

- Conda environment: `aba-asp`
- Python: `3.10.20`
- SWI-Prolog: `10.0.2`
- clingo: `5.8.0`
- Git base commit: `83a8e4a41b57d4b5127386d0189e5531366a89e3`
- Dirty tree: yes; M13-C1 implementation and record uncommitted at run time.

## Artefact paths

- ECAI arm:
  `causal/outputs/aba_learning/grid/M13_c1_role_equivalence_ecai2024/`
- AAMAS arm:
  `causal/outputs/aba_learning/grid/M13_c1_role_equivalence_aamas2025/`
- Final summary:
  `causal/outputs/aba_learning/grid/M13_c1_role_equivalence_summary.md`
- Machine-readable summary:
  `causal/outputs/aba_learning/grid/M13_c1_role_equivalence_summary.json`
- Per-cell artefacts:
  `{arm}/cells/{m13_c1_parent_x0,m13_c1_parent_x1}__target-x2/`

## Outcome summary

All four cells were runner-`solved`. Every cell achieved ASP positive coverage
\(2/2\) and negative rejection \(1/1\). No learned framework contained assumptions or
contraries.

For both configurations, the paired cells had identical data hash
`d4e8f29049d132d129a11be127f91d596d50a4dbbd5321e8cdbbf0de4d18bf60` and
identical BK hash
`18212f71b3e14e76b3635d09eff94d46230679c3ae1fa9887463f42539a11ccc`.
The positive and negative examples, normalised learned \(\delta\), and ASP coverage
were also identical within each pair.

## Quantitative and structural results

### ECAI pair

Both graph-labelled cells learned:

```prolog
x2(A) :- x0_val_1(A).
x2(A) :- x0_val_2(A).
```

Under \(G_0\), where \(\mathrm{Pa}(x_2)=\{x_0\}\), this was an exact
\(\mathcal H_{x_2}^{\star,G_0}\) match with variable-level parent precision and recall
both \(1\), and `clean_recovery=1`. Under \(G_1\), where
\(\mathrm{Pa}(x_2)=\{x_1\}\), the identical learned rules cited only the
extensionally equivalent sibling: variable-level parent precision and recall were both
\(0\), and `clean_recovery=0`.

The traces were identical apart from timing. For each positive, one-token
non-deterministic folding selected the first matching `x0_val_*` predicate and passed
the entailment check without Assumption Introduction.

### AAMAS pair

Both graph-labelled cells learned:

```prolog
x2(A) :- x0_val_1(A), x1_val_1(A).
x2(A) :- x0_val_2(A), x1_val_2(A).
```

Under either graph, the normalised body-variable set was \(\{x_0,x_1\}\): the direct
parent and its extensionally equivalent sibling. Variable-level parent precision was
\(1/2\), recall was \(1\), and `clean_recovery=0` in both cells. The traces show greedy
folding accumulating the matching \(x_0\) and \(x_1\) predicates for each positive row.

## Interpretation

The implementation received identical learner-visible tasks and returned identical
learned frameworks within each arm. Changing only the external causal model could
therefore change the graph-relative verdict, but not the learned object.

ECAI supplied the sharpest demonstration: the same two rules were an exact parent
solution under \(G_0\) and a non-parent sibling solution under \(G_1\), despite full
coverage in both. AAMAS demonstrated the complementary behaviour: it retained both
extensionally equivalent predictors and therefore expressed no preference between their
causal roles.

This is consistent with the ABA Learning task definition and the inspected pipeline.
The formal task evaluates acceptance of \(E^\pm\), while the graph roles used for
semantic assessment are external. The result is also consistent with M12x Bucket 1:
coverage and exact sample separation do not establish that selected variables were
causally privileged.

## Claims supported

- For a fixed configuration, two graph-labelled designs that induce identical
  \((\mathcal F_{\mathrm{BK}},E^+,E^-)\) provide no learner-visible basis for
  preferring a direct parent over an extensionally equivalent non-parent.
- In this paired control, both ECAI and AAMAS returned graph-invariant learned
  frameworks, while graph-relative parent recovery and semantic evaluation differed.
- Full ASP coverage did not distinguish the exact parent solution from the
  extensionally equivalent sibling solution.

## Claims not supported

- Causal discovery or full-DAG recovery.
- Full Russo-style Causal ABA.
- A general claim that extensionally equivalent predictors are common in arbitrary
  data.
- A claim that either ECAI or AAMAS is invariant to BK reorderings.

## Report relevance

- Milestone: M1.3 Bucket 2, Claim 1.
- Narrative role: a minimal constructive demonstration of why causal-role preference
  cannot arise from learner-input-equivalent ABA Learning tasks.

## Next decision

Write M1.3 Bucket 2 Claim 1 from this analysed record and its locked theory/engine
context. Then proceed to the separate BK-order comparison; do not treat this experiment
as an order-invariance test.

## Samuel review checklist

- [ ] Commands are exact.
- [ ] Artefact paths exist.
- [ ] Learner-visible inputs are byte-identical across \(G_0/G_1\).
- [ ] Learned-rule comparisons use normalised \(\delta\), not raw path-bearing traces.
- [ ] Graph-relative metric differences are not mistaken for learner-output differences.
- [ ] Learned-rule examples are copied accurately.
- [ ] Unsupported claims are explicitly excluded.
- [ ] The ABA Learning / Causal ABA distinction is preserved.
