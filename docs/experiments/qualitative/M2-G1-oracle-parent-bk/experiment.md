# M2-G1 — ABALearnG vs ABALearnU on oracle-parent BK (metrics 2 and 3)

## Status

**run** (14 August 2026). Two child-`c` cells executed. U artefacts reused, not
rerun. Not a locked claim. Not a Causal ABA integration result. Metric 1
(runtime including ABA-PC) was not scored.

## Purpose

Compare unguided target-wise ABA Learning (**ABALearnU**: every non-target
column in BK) with oracle-parent-masked ABA Learning (**ABALearnG**: BK
restricted to \(\mathrm{Pa}(X)\)). The mask uses the fixture graph as an
evaluator-only parent set. Graph edges are not written into `bk.aba` as ABA
facts.

## Research question

On the same frozen support tables and the same `baseline_cautious` learner,
does oracle-parent BK yield:

- **Metric 2:** a more succinct delta (fewer rules / assumptions / literals)?
- **Metric 3:** a delta whose exact-value vocabulary is a subset of
  \(\mathrm{Pa}(X)\)?

Metric 3 inspects **the whole delta**, including contrary rules, not only
heads `c(A) :- ...`.

## Setup

- Learner: `configs/baseline_cautious_config.pl` (cautious nd, `relto`,
  `folding_steps(10)`).
- Encoding: exact-value, binary 1-vs-0.
- U: `encoding.predictor_policy` default `all_except_target` (existing
  `baseline_cautious` collections).
- G: `encoding.predictor_policy: oracle_parents` under configuration id
  `baseline_cautious_oracle_parents`.
- Only target `c` was executed for G. Roots were not run.
- U cells were not overwritten.

### Cells

| Role | Fixture | Target | \(\mathrm{Pa}(C)\) | Why this cell |
|---|---|---|---|---|
| Metrics 2 and 3 (flagship) | `m2_support_and3_lead_iso` | `c` | \(\{b,d,e\}\) | Isolated \(A\) is in U BK but not a parent. \(C := B \land D \land E\). |
| Metric 3 only | `m2_support_copy_chain` | `c` | \(\{b\}\) | U can recover ancestor \(A\) at the same length as a parent rule. |

A three-variable AND collider was not run: there U BK is already parent-only,
so G = U.

## Commands

From the `aba_asp` root in `aba-asp`:

```bash
python -m causal.targetwise.cli run \
  --config causal/configs/targetwise/m2_support_and3_lead_iso/baseline_cautious_oracle_parents/support.yaml \
  --targets c

python -m causal.targetwise.cli run \
  --config causal/configs/targetwise/m2_support_copy_chain/baseline_cautious_oracle_parents/support.yaml \
  --targets c
```

U artefacts already existed under `.../baseline_cautious/support/cells/target-c/`.

## Size and vocabulary

`n_delta` counts every learned line (ordinary rules, assumptions, and
contraries). `delta vars` are fixture variables appearing as `*_val_*` anywhere
in that delta. Metric 3 passes iff `delta vars` \(\subseteq \mathrm{Pa}(C)\).
Times are `aba_learning_runtime_s` (not Metric 1).

| Fixture | System | BK predictors | outcome | n_delta | n_asm | n_contraries | n_target | delta vars | runtime (s) | M2 | M3 |
|---|---|---|---|---:|---:|---:|---:|---|---:|---|---|
| 3-AND + isolated \(A\) | U | `a,b,d,e` | solved | 20 | 5 | 5 | 2 | `{a,b,d,e}` | 2.62 | — | fail |
| 3-AND + isolated \(A\) | G | `b,d,e` | solved | 8 | 2 | 2 | 1 | `{b,d,e}` | 1.19 | pass | pass |
| Copy chain | U | `a,b` | solved | 1 | 0 | 0 | 1 | `{a}` | 0.24 | — | fail |
| Copy chain | G | `b` | solved | 1 | 0 | 0 | 1 | `{b}` | 0.27 | tie | pass |

## Learned deltas

### Flagship: `m2_support_and3_lead_iso`, target `c`

U (`baseline_cautious`):

```prolog
c(A) :- alpha_1(A), a_val_0(A).
c(A) :- alpha_2(A), a_val_1(A).
c_alpha_1(A) :- b_val_0(A).
c_alpha_1(A) :- alpha_3(A), b_val_1(A).
c_alpha_2(A) :- b_val_0(A).
c_alpha_2(A) :- d_val_0(A).
c_alpha_2(A) :- alpha_4(A), d_val_1(A).
c_alpha_3(A) :- alpha_5(A), e_val_1(A).
c_alpha_4(A) :- e_val_1(A).
c_alpha_5(A) :- d_val_0(A).
```

plus five `assumption/1` and five `contrary/2` lines. Ordinary rules latch onto
the isolate `a`; parents enter through \(\alpha\)-contraries.

G (`baseline_cautious_oracle_parents`):

```prolog
c(A) :- alpha_1(A), b_val_1(A).
c_alpha_1(A) :- d_val_0(A).
c_alpha_1(A) :- alpha_2(A), d_val_1(A).
c_alpha_2(A) :- e_val_1(A).
assumption(alpha_1(A)).
assumption(alpha_2(A)).
contrary(alpha_1(A),c_alpha_1(A)) :- assumption(alpha_1(A)).
contrary(alpha_2(A),c_alpha_2(A)) :- assumption(alpha_2(A)).
```

This is the same 3-AND child shape as `m2_support_and3` target `c`, with the
first remaining BK block `b` as the latch (Finding 2). No `a_val_*`.

### Metric 3: `m2_support_copy_chain`, target `c`

U: `c(A) :- a_val_1(A).` (ancestor, not parent). Same length as G, so Metric 2
does not apply.

G: `c(A) :- b_val_1(A).` (the unique parent). Metric 3 passes.

## Artefacts

G collections (partial; only `c` executed):

`causal/outputs/aba_learning/targetwise/<fixture>/baseline_cautious_oracle_parents/support/cells/target-c/`

U collections (reused):

`causal/outputs/aba_learning/targetwise/<fixture>/baseline_cautious/support/cells/target-c/`

G configs:

`causal/configs/targetwise/<fixture>/baseline_cautious_oracle_parents/support.yaml`

## Interpretation boundary

This record compares two BK **predictor masks** on two child targets. It does
not use Causal ABA, Majority-PC, or ABA-PC output. Oracle parents come from the
fixture graph. It does not show that a CPDAG-derived parent set would produce
the same deltas. Metric 1 is out of scope. G is not expected to emit an
evaluator-style conjunctive rule `c(A) :- b_val_1(A), d_val_1(A), e_val_1(A).`
under nd/`relto`.
