# M2-S1 — `baseline_cautious` solved vs no-solution on exhaustive-support mechanisms

## Status

**run** (14 August 2026). Outcome grid filled. Deltas retained. Not analysed as
a locked claim. Not a Causal ABA integration result.

## Purpose

Record whether `baseline_cautious` returns `solved` or `completed_no_solution`
for every variable on seven deterministic-mechanism truth tables. The intended
use is to see which targets would emit an `ext_source` fact under the proposed
rule: `completed_no_solution` only.

## Setup

- Learner: `configs/baseline_cautious_config.pl` (cautious nd, `relto`,
  `folding_steps(10)`).
- Encoding: exact-value, binary 1-vs-0.
- Tables: handwritten exhaustive combinations of **root** assignments only.
  Non-roots are the deterministic mechanism values. Not IID samples.
- The target-wise loader requires `iid_observational_rows: true` on the sample
  manifest; that flag is a loader contract, not a description of how the rows
  were obtained.
- Every fixture variable is a learning target.

### Fixtures and tables

| Fixture id | Mechanism | Roots | Rows |
|---|---|---|---|
| `m2_support_and_collider` | \(C := A \land B\) | \(A,B\) | `(0,0,0)`, `(0,1,0)`, `(1,0,0)`, `(1,1,1)` |
| `m2_support_or_collider` | \(C := A \lor B\) | \(A,B\) | `(0,0,0)`, `(0,1,1)`, `(1,0,1)`, `(1,1,1)` |
| `m2_support_xor_collider` | \(C := A \oplus B\) | \(A,B\) | `(0,0,0)`, `(0,1,1)`, `(1,0,1)`, `(1,1,0)` |
| `m2_support_copy` | \(B := A\) | \(A\) | `(0,0)`, `(1,1)` |
| `m2_support_not` | \(B := \lnot A\) | \(A\) | `(0,1)`, `(1,0)` |
| `m2_support_copy_chain` | \(B := A\), \(C := B\) | \(A\) | `(0,0,0)`, `(1,1,1)` |
| `m2_support_fork_copy_not` | \(B := A\), \(C := \lnot A\) | \(A\) | `(0,0,1)`, `(1,1,0)` |

Specs: `causal/fixtures/specs/m2_support_*.yaml`.  
Source tables: `causal/fixtures/handwritten_tables/`.  
Bundles: `causal/outputs/causal_fixtures/m2_support_*/`.  
Configs: `causal/configs/targetwise/m2_support_*/baseline_cautious/support.yaml`.

## Commands

From the `aba_asp` root in `aba-asp`:

```bash
python -m causal.fixtures.assemble_m2_support_bundles

python -m causal.targetwise.cli validate \
  --config causal/configs/targetwise/<fixture>/baseline_cautious/support.yaml

python -m causal.targetwise.cli run \
  --config causal/configs/targetwise/<fixture>/baseline_cautious/support.yaml
```

The seven `<fixture>` ids are those in the table above. All seven `run` commands
completed on 14 August 2026.

## Outcome grid

`solved` = a delta was accepted. `no-sol` = `completed_no_solution`. Empty
cells are variables that do not exist in that fixture.

| Fixture | `a` | `b` | `c` |
|---|---|---|---|
| AND collider | no-sol | no-sol | solved |
| OR collider | no-sol | no-sol | solved |
| XOR collider | solved | solved | solved |
| Copy | solved | solved | — |
| NOT | solved | solved | — |
| Copy chain | solved | solved | solved |
| Fork copy+NOT | solved | solved | solved |

Collections:

`causal/outputs/aba_learning/targetwise/<fixture>/baseline_cautious/support/`

Per-target `delta.aba` is present for every `solved` cell under
`cells/target-<var>/output/`. No-solution cells have no delta.

## Observations (not claims)

1. **AND and OR** match the H0 pattern on this four-row support: roots no-sol,
   child solved. Under the proposed compiler, only `a` and `b` would be
   `ext_source` facts.
2. **XOR** solved on **all three** targets, including the DAG roots. That is
   not a surprise once the truth table is read as functions: \(A = B \oplus C\)
   and \(B = A \oplus C\). The child also solved, so this is not failure mode 2
   (non-root no-solution). It is failure mode 1 on the roots (a root solves,
   so no source fact is emitted).
3. **Copy, NOT, copy chain, and the copy/NOT fork** solved on every target,
   including true roots. Invertible mechanisms make each node a function of
   another. Again mode 1, not mode 2.
4. On these seven tables, **no non-root returned `completed_no_solution`**.

Deltas were not inspected beyond confirming they exist for solved cells. A
later pass can read them.

## Interpretation boundary

This record only answers which targets `baseline_cautious` solves on these
handwritten support tables. It does not evaluate Causal ABA, Majority-PC,
weighting, or an `ext_source` pipeline.

Non-root follow-up (3-AND, 3-OR, leading-isolated 3-AND):
`docs/experiments/qualitative/M2-S2-mode2-nonroot-outcomes/experiment.md`.
