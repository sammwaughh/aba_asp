# M13-C2 — Comparative sensitivity to BK feature-block order

## Status

`proposed | planned | implemented | run | analysed | reported`

Current status: `analysed` — Stage 0 passed; both ten-cell published-configuration
arms ran; all 20/20 cells were runner-`solved`; learned frameworks, traces, and ASP
coverage were inspected; the comparative claim is supported on all three families.

## Purpose

Compare how the published ECAI and AAMAS configurations respond when complete
exact-value predictor blocks are permuted without changing the named data, graph,
target, examples, or set of BK rules. U5 is the decisive parent-versus-ancestor case;
U2 is a both-parent control; U7 tests whether order can expose or repair a covering
failure requiring two parents.

## Research question

> Under `val`-only categorical BK, does predictor-block order change ECAI's learned
> target-rule backbone, assumption structure, semantic success, or ASP coverage, while
> AAMAS preserves its normalised row-wise conjunctions and coverage?

## Theoretical motivation

### ABA foundations

The learned framework must be interpreted through its ordinary rules, assumptions,
contraries, attacks, and stable-extension consequences. Structural change is meaningful
even where two frameworks have identical sample coverage.

### ABA Learning / ABALearn

ABA Learning permits different sequences of Folding and Assumption Introduction to
produce different learned frameworks. Transformation and folding order are therefore
potentially substantive search parameters rather than harmless textual details.

### Causal ABA / argumentative causal discovery

This experiment does not use Russo-style arrow/no-edge/independence assumptions,
d-separation, or stable extensions as candidate DAGs. The graph is external evaluation
metadata.

### Current implementation

Generated BK follows DataFrame column order. BK rules receive identifiers in file order,
and the folding lookup table preserves that order. Under ECAI, one-token
non-deterministic folding can commit to the first successful matching predicate and
repair that body through assumptions. Under AAMAS, greedy folding considers every
matching original-BK predicate for the row and sorts the accumulated heads.

## Relation to prior evidence

- M1.1 categorical-three \(\sigma\)-controls and ABL-101 established that BK order can
  change the first fold and learned framework under non-deterministic folding.
- The existing chain order-regression test records a changed non-deterministic delta and
  unchanged greedy delta for one simulated case, but does not compare the complete
  published configurations.
- M12x Bucket 1 Claim 2 records \(x_0\)-keyed target rules in all nine ECAI cells under
  the fixed \(x_0\)-first order.
- M12x Bucket 1 Claim 1 records full-row exact-value conjunctions in all nine AAMAS
  cells.
- M13-C1 reproduces the same contrast on an input-equivalent pair, without reordering
  BK.

## Implementation scope

### Code/config paths

- Fixtures: `causal/experiments/handcrafted_m13.py`
- Registry: `causal/experiments/handcrafted.py`
- Tests: `causal/tests/test_m13_c2_fixtures.py`
- ECAI config: `causal/configs/experiments/M13_c2_bk_order_ecai2024.yaml`
- AAMAS config: `causal/configs/experiments/M13_c2_bk_order_aamas2025.yaml`
- Comparison generator: `causal/experiments/m13_c2_summary.py`
- Outputs:
  `causal/outputs/aba_learning/grid/M13_c2_bk_order_{ecai2024,aamas2025}/`
- Summary: `causal/outputs/aba_learning/grid/M13_c2_bk_order_summary.{md,json}`

### Files changed for this experiment

- `causal/experiments/handcrafted_m13.py`
- `causal/tests/test_m13_c1_fixtures.py` (registry assertion generalised)
- `causal/tests/test_m13_c2_fixtures.py`
- `causal/configs/experiments/M13_c2_bk_order_ecai2024.yaml`
- `causal/configs/experiments/M13_c2_bk_order_aamas2025.yaml`
- `causal/experiments/m13_c2_summary.py`
- `docs/experiments/qualitative/M13-C2-bk-feature-order/experiment.md`

### Files inspected before implementation

- `docs/theory/background.tex`
- `docs/experiments/qualitative/M1.1-parent-position.md`
- `docs/experiments/qualitative/M1.2-expanded-cell-inspection.md`
- `docs/experiments/qualitative/M1.3-bucket1-claims.md`
- `folding.pl`
- `gen.pl`
- `causal/argcausaldisco_integration.py`
- `causal/experiments/handcrafted_m12x.py`
- `causal/test_aba_learning.py`
- `configs/ecai2024_config.pl`
- `configs/aamas2025_config.pl`

## Dataset and representation interventions

Every variant retains its M12x graph, named values, row identifiers, target, and
\(E^\pm\). The target remains the final column. Only the order of non-target DataFrame
columns changes, which changes the corresponding order of complete BK feature blocks.

### U5: decisive parent-versus-ancestor pair

Graph \(x_0\to x_1\to x_2\), target \(x_2:=x_1\), with
\(\mathrm{Pa}(x_2)=\{x_1\}\).

- `m13_c2_u5_x0_x1`: predictor order \(x_0,x_1\) (locked M12x order).
- `m13_c2_u5_x1_x0`: predictor order \(x_1,x_0\).

### U2: both-parent control

Graph \(x_0\to x_2\leftarrow x_1\), target \(x_2:=\min(x_0,x_1)\).

- `m13_c2_u2_x0_x1`
- `m13_c2_u2_x1_x0`

### U7: required-two-parent order sweep

Diamond graph with \(\mathrm{Pa}(x_3)=\{x_1,x_2\}\) and
\(x_3:=|x_1-x_2|\). Run all six permutations of \(x_0,x_1,x_2\), with target \(x_3\)
last:

- `m13_c2_u7_x0_x1_x2`
- `m13_c2_u7_x0_x2_x1`
- `m13_c2_u7_x1_x0_x2`
- `m13_c2_u7_x1_x2_x0`
- `m13_c2_u7_x2_x0_x1`
- `m13_c2_u7_x2_x1_x0`

## Stage-0 invariants

Within each family, tests must establish:

1. equality of named values after canonicalising column order;
2. identical graphs, targets, row identifiers, and \(E^\pm\);
3. identical sets of BK rules after ignoring block order;
4. the requested and only the requested feature-block order;
5. identical locked \(\mathcal H_t^\star\) and semantic-success criterion.

## Locked expected outcomes

### U5

ECAI with \(x_0\) first should reproduce the M12x grandparent-backed assumption
framework. With \(x_1\) first, it should learn the exact parent rules

```prolog
x2(A) :- x1_val_1(A).
x2(A) :- x1_val_2(A).
```

without assumptions or contraries. ASP coverage is expected to remain full, while the
semantic verdict changes.

AAMAS is expected to return the same four normalised parent-plus-grandparent
conjunctions under both orders.

### U2

ECAI is expected to change which parent forms the ordinary target-rule backbone, while
remaining a semantically successful assumption-mediated encoding of
both-parents-nonzero. AAMAS is expected to preserve the same exact four both-parent
conjunctions.

### U7

ECAI is expected to follow the leading feature block. Orders in which \(x_0\) precedes
both parents may preserve the locked covering failure. Parent-first orders may allow
both \(x_1\) and \(x_2\) to enter the target-relevant framework and may restore negative
rejection; this is deliberately not locked more strongly before execution.

AAMAS is expected to preserve its normalised \(x_0,x_1,x_2\) row conjunctions and full
coverage under all six permutations.

## Commands run

```bash
conda run -n aba-asp python -m pytest \
  causal/tests/test_m13_c1_fixtures.py \
  causal/tests/test_m13_c2_fixtures.py -q
# → 16 passed in 1.67s

conda run -n aba-asp python -m causal.experiments.run_grid \
  --config causal/configs/experiments/M13_c2_bk_order_ecai2024.yaml --dry-run
# → 10 cells planned for M13_c2_bk_order_ecai2024

conda run -n aba-asp python -m causal.experiments.run_grid \
  --config causal/configs/experiments/M13_c2_bk_order_aamas2025.yaml --dry-run
# → 10 cells planned for M13_c2_bk_order_aamas2025

conda run -n aba-asp python -m causal.experiments.run_grid \
  --config causal/configs/experiments/M13_c2_bk_order_ecai2024.yaml --no-resume
# → done: completed=10 skipped=0 outcomes={'solved': 10}

conda run -n aba-asp python -m causal.experiments.run_grid \
  --config causal/configs/experiments/M13_c2_bk_order_aamas2025.yaml --no-resume
# → done: completed=10 skipped=0 outcomes={'solved': 10}

conda run -n aba-asp python -m causal.experiments.m13_c2_summary
# → wrote M13_c2_bk_order_summary.md
# → wrote M13_c2_bk_order_summary.json

conda run -n aba-asp python -m pytest \
  causal/tests/test_m13_c1_fixtures.py \
  causal/tests/test_m13_c2_fixtures.py \
  causal/tests/test_m12x_fixtures.py \
  causal/tests/test_config.py -q
# → 47 passed in 1.64s
```

## Environment

- Conda environment: `aba-asp`
- Python: `3.10.20`
- SWI-Prolog: `10.0.2`
- clingo: `5.8.0`
- Git base commit: `83a8e4a41b57d4b5127386d0189e5531366a89e3`
- Dirty tree: yes; M13-C1/C2 work uncommitted at run time.

## Artefact paths

- ECAI arm: `causal/outputs/aba_learning/grid/M13_c2_bk_order_ecai2024/`
- AAMAS arm: `causal/outputs/aba_learning/grid/M13_c2_bk_order_aamas2025/`
- Final summary: `causal/outputs/aba_learning/grid/M13_c2_bk_order_summary.md`
- Machine-readable summary:
  `causal/outputs/aba_learning/grid/M13_c2_bk_order_summary.json`
- Per-cell artefacts: `{arm}/cells/{fixture}__target-{target}/`

## Outcome summary

All 20 cells were runner-`solved`. Stage-0 tests confirmed that named data, graphs,
targets, examples, and BK rule sets were invariant within each family, and that only
complete feature-block order changed.

ECAI produced two distinct normalised deltas across the two U2 orders, two across the
two U5 orders, and six across the six U7 orders. AAMAS produced one normalised delta per
family across all corresponding orders.

### U5: decisive semantic contrast

With order \(x_0\prec_{\mathrm{BK}}x_1\), ECAI reproduced the locked M12x result:

```prolog
x2(A) :- alpha_1(A), x0_val_0(A).
x2(A) :- x0_val_1(A).
x2(A) :- alpha_2(A), x0_val_2(A).
c_alpha_1(A) :- x1_val_0(A).
c_alpha_2(A) :- x1_val_0(A).
```

The target-rule body variable was the non-parent ancestor \(x_0\); two assumptions and
two contraries were introduced. ASP coverage was full, but the result was not an exact
or mechanism-aligned parent-copy intension.

With order \(x_1\prec_{\mathrm{BK}}x_0\), ECAI learned:

```prolog
x2(A) :- x1_val_1(A).
x2(A) :- x1_val_2(A).
```

The first parent folds passed entailment immediately. No assumptions or contraries were
introduced; the result exactly matched \(\mathcal H_{x_2}^\star\), achieved
`clean_recovery=1`, and retained full ASP coverage.

AAMAS returned the same four normalised \(x_0,x_1\) positive-row conjunctions under
both orders, with no assumptions and full coverage. Its output remained a
parent-plus-grandparent superset.

### U2: both-parent control

ECAI followed the leading parent in each order. The ordinary target-rule backbone used
\(x_0\) under \(x_0\prec x_1\) and \(x_1\) under \(x_1\prec x_0\); the other parent
appeared in two contrary rules. Both deltas contained two assumptions and expressed
the same both-parents-nonzero mechanism with full coverage, but the normalised deltas
were not identical.

AAMAS returned the same exact four both-parent conjunctions under both orders, with no
assumptions and full coverage.

### U7: six-order sweep

For every ECAI cell, the first target fold used the first feature block. The ordinary
target bodies therefore used \(x_0\), \(x_1\), or \(x_2\) according to the leading
variable. Contrary repair then used the next available informative block. The complete
normalised delta differed under all six orders.

The two orders with \(x_2\) third,

\[
x_0\prec x_1\prec x_2
\quad\text{and}\quad
x_1\prec x_0\prec x_2,
\]

introduced six assumptions, omitted \(x_2\) from the framework, covered all positives,
and rejected \(0/3\) negatives. In every order placing \(x_2\) in the first two blocks,
ECAI introduced three assumptions and rejected all \(3/3\) negatives.

The parent-only orders \(x_1\prec x_2\prec x_0\) and
\(x_2\prec x_1\prec x_0\) produced assumption-mediated frameworks over
\(\{x_1,x_2\}\) and expressed the intended \(x_1\neq x_2\) mechanism without citing
\(x_0\). Orders pairing \(x_0\) with \(x_2\) achieved full coverage through the
ancestor proxy but remained intensionally misaligned.

AAMAS returned the same three normalised \(x_0,x_1,x_2\) positive-row conjunctions
under all six orders. It introduced no assumptions and retained full coverage
throughout. The trace traversal order changed, but the sorted learned rules did not.

## Interpretation

The observed contrast follows the engine paths identified before the run. BK order
determines rule identifiers and first matches. Under ECAI, one-token
non-deterministic folding commits to the first successful predicate. If that fold
overgeneralises, Assumption Introduction preserves the selected body, and contrary
learning proceeds through subsequent BK candidates. The U7 sweep shows that this
ordering can determine not only the learned representation but whether a required
parent is reached before the procedure terminates.

Under AAMAS, greedy folding traverses every matching original-BK rule for the positive
row and sorts the accumulated heads. Consequently, the traversal sequence followed BK
order while the normalised conjunctions, assumptions, and coverage remained invariant.

The claim is therefore structural and configuration-specific. It does not assert
general order-invariance of greedy ABA Learning. It establishes that, on all tested
exact-value M13-C2 families, ECAI's learned framework depended on feature-block order,
whereas AAMAS's normalised learned framework and coverage did not.

## Claims supported

- Across U2, U5, and U7 under the published configurations, complete BK feature-block
  permutations changed every ECAI normalised delta but left the AAMAS normalised delta
  and coverage invariant within each family.
- ECAI's order sensitivity follows the observed first-fold variable and subsequent
  Assumption Introduction/contrary-repair path.
- On U5, a representation-only swap changed ECAI from a fully covering non-parent
  assumption framework to exact assumption-free parent recovery.
- On U7, putting the required parent \(x_2\) third produced covering failure, while
  placing it in either of the first two blocks restored full negative rejection.

## Claims not supported

- General order-invariance of greedy ABA Learning on arbitrary ABA frameworks.
- A claim that BK order is the only difference between ECAI and AAMAS.
- Causal discovery or full Russo-style Causal ABA.
- A claim that structural order sensitivity must always change sample coverage.

## Report relevance

- Milestone: M1.3 Bucket 2, Claim 2.
- Narrative role: controlled comparison of search sensitivity to a representation-only
  change.

## Next decision

None for M13-C2. Its evidence is incorporated into locked Bucket 2 Claim 2. The proposed
support-mediated Bucket 2 Claim 3 was parked on 22 July; preserve the U7 evidence for
possible relevance to Milestone 2. It does not prescribe how argumentative causal
discovery and ABA Learning should be integrated. Bucket 3 and M1.3 are now closed.
