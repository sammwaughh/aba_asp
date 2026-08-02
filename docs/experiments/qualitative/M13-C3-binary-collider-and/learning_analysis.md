# M13-C3 — Learning-stage analysis (six-cell AAMAS + ECAI)

## Status

**H0 closed.** This document is the closed learning-stage record for baseline
investigation **H0** on fixture `m13_bucket3_binary_collider_and`, frozen sample
`n30_seed42`.

- Fixture certified; sample frozen; AAMAS and ECAI arms run on all targets
  `a`, `b`, `c`
- Trace + fixture integration completed
- Six-cell narrative documented here (Markdown) and in `learning_analysis.tex`
- **No Bucket 3 claim approved**
- Follow-up probe **H1** is documented separately in `h1_support_ablation.md` /
  `.tex` (not part of H0). Remaining probes H2–H4: `future_probes.md`

Companion records: `experiment.md` (investigation hub); `fixture_dossier.tex`
(pre-run mathematical account).

## Scope

This document is the **learning-stage evidence narrative** for:

| Arm | Config | Targets |
|-----|--------|---------|
| `aamas2025` | `configs/aamas2025_config.pl` — brave, greedy, mgr, `folding_space(bk)`, relto, `check_ic` | `a`, `b`, `c` |
| `ecai2024` | `configs/ecai2024_config.pl` — brave, nd, any, all, relto, `check_ic` | `a`, `b`, `c` |

Same frozen table for all six cells. Encoding: exact-value BK; binary 1-vs-0
examples. Graph, certificate, and `mechanism_reference.json` are
**evaluator-only** (not learner-visible).

Not in scope here: Russo-style Causal ABA; claim drafting; H1–H4 execution.

---

## Fixture / sample / config contract

| Field | Value |
|-------|--------|
| Fixture ID | `m13_bucket3_binary_collider_and` |
| Names | `a`,`b`,`c` (display \(A,B,C\)) |
| DAG | \(A \rightarrow C \leftarrow B\) |
| Mechanisms | \(A\sim\mathrm{Bernoulli}(4/5)\), \(B\sim\mathrm{Bernoulli}(7/10)\), independent; \(C=A\land B\) |
| Sample | `n=30`, seed `42` |
| Sample CSV | `causal/outputs/causal_fixtures/m13_bucket3_binary_collider_and/samples/n30_seed42.csv` |
| Sample hash | `sha256:1edae465d0f6b6b662b3c4ed4863af21c1d9b0c1cf428774731dd3f43282a8ca` |
| Evaluator ref for `c` | `c(A) :- a_val_1(A), b_val_1(A).` |
| Roots in reference | `no_observed_parent_deterministic_rule` |

### Collection roots

```text
causal/outputs/aba_learning/targetwise/m13_bucket3_binary_collider_and/aamas2025/n30_seed42/
causal/outputs/aba_learning/targetwise/m13_bucket3_binary_collider_and/ecai2024/n30_seed42/
```

Per cell: `cells/target-{a|b|c}/input/{bk.aba,examples.json,data.csv,task_manifest.json}`
and `output/{prolog.stdout,delta.aba?,bk.sol.*,...}` plus `metrics.json` /
`report.md`. Arm `summary.md` files are the authoritative outcome tables.

---

## Population / sample geometry relevant to learning

Exact population support (four atoms) and frozen counts:

| \((A,B,C)\) | Population \(P\) | Sample count | Notes |
|-------------|-----------------:|-------------:|-------|
| \((1,1,1)\) | \(14/25\) | 17 | only E+ family for target `c` |
| \((1,0,0)\) | \(6/25\) | 7 | includes row **9**; E+ for `a`, E− for `c` when \(A=1,B=0\) |
| \((0,1,0)\) | \(7/50\) | 4 | E+ for `b` when \(A=0,B=1\) |
| \((0,0,0)\) | \(3/50\) | 2 | rows **26**, **30** only |

Implied \(E^\pm\) under binary 1-vs-0 (matches arm summaries):

| Target | \(E^+\) | \(E^-\) |
|--------|--------:|--------:|
| `a` | 24 | 6 |
| `b` | 21 | 9 |
| `c` | 17 | 13 |

### Shared geometry under \(C=A\land B\)

1. **Target `c`:** every E+ row has \((A,B)=(1,1)\). One predictor family only.
2. **Root `a`:** E+ splits into \((B,C)=(1,1)\) and \((B,C)=(0,0)\); likewise
   root `b` with \((A,C)\).
3. **Label ambiguity:** cell \((\textit{other root},C)=(0,0)\) is not a function
   of the BK literals alone. Example for target `a`: row **9** `(1,0,0)` is E+
   and row **26** `(0,0,0)` is E−, yet both share BK literals `b_val_0`,
   `c_val_0`.
4. Roots have **no** deterministic causal rule over other observed variables
   (evaluator reference). Predictive covering ≠ mechanism recovery.
5. Syntactic match of a delta to the evaluator `c` reference is **not**
   automatic causal success.

---

## Outcome snapshot (verified)

| Arm | Target | Outcome | Surface delta (abbreviated) |
|-----|--------|---------|------------------------------|
| AAMAS | `a` | `completed_no_solution` | no delta / no `bk.sol.*` |
| AAMAS | `b` | `completed_no_solution` | same, predictors swapped |
| AAMAS | `c` | `solved` (audit SAT) | `c(A) :- a_val_1(A), b_val_1(A).` |
| ECAI | `a` | `solved` (audit SAT) | 11-clause assumption framework; body vars involve `b` |
| ECAI | `b` | `solved` (audit SAT) | mirror of `a` with `a`↔`b` |
| ECAI | `c` | `solved` (audit SAT) | `c :- alpha_1, a_val_1` + `c_alpha_1 :- b_val_0` |

Sources: arm `summary.md` files; per-cell `delta.aba` / `report.md`.

---

## AAMAS narrative (`aamas2025`)

The AAMAS arm uses `configs/aamas2025_config.pl`. The active options for these
cells are `learning_mode(brave)`, `folding_mode(greedy)`,
`folding_selection(mgr)`, `folding_space(bk)`, `asm_intro(relto)`, and
`check_ic`. Under greedy folding with BK space, each positive example is
replaced by a **maximal co-occurrence body** assembled from background
predicates that hold of that row. The mgr selection step then keeps a
most-general representative among duplicate bodies. Brave entailment is the
acceptance test for each candidate extension. Authoritative traces are the
per-cell `prolog.stdout` files under
`.../aamas2025/n30_seed42/cells/target-{a,b,c}/output/`, together with the arm
`summary.md`.

### Target `c` — solved with an assumption-free conjunction

For target \(c\), every positive example lies in the single joint cell
\((A,B)=(1,1)\). There are seventeen such rows, and each therefore admits the
same maximal BK body \(\{\mathtt{a\_val\_1},\mathtt{b\_val\_1}\}\). After mgr
deduplication, the learner retains one live candidate,

```prolog
c(A) :- a_val_1(A), b_val_1(A).
```

Brave entailment of \(\langle E^+,E^-\rangle\) succeeds immediately. No negative
example shares that body, so no assumption is introduced. The folding queue is
empty, and the run terminates as `solved` with zero assumptions and zero
contraries. The post-run artefact audit on `bk.sol_chk.asp` reports SAT.

The emitted delta string is identical to the evaluator-only positive-state
reference for \(c\) in `mechanism_reference.json`. That match is recorded here
as a **syntactic coincidence**. It is not by itself a causal-recovery verdict.
The same configuration and sample can fail on the root targets, as the next
subsection shows.

Authoritative artefacts:
`.../aamas2025/n30_seed42/cells/target-c/output/{delta.aba,prolog.stdout}` and
the arm `summary.md`.

### Targets `a` / `b` — `completed_no_solution` (symmetric)

The story for root \(a\) is verified in
`.../aamas2025/n30_seed42/cells/target-a/output/prolog.stdout`. Target \(b\) is
the same procedure with the roles of \(A\) and \(B\) swapped.

Positive examples for \(a\) fall into two BK co-occurrence families. The first
is \((B,C)=(1,1)\), which arises on every row where \(A=1\) and the AND child
fires. The second is \((B,C)=(0,0)\), which arises on rows such as row~9 where
\(A=1\) yet \(B=C=0\). Greedy folding therefore proposes two distinct bodies.

The both-1 rule

```prolog
a(A) :- b_val_1(A), c_val_1(A).
```

is accepted under brave entailment. It covers the \((1,1)\) positives without
touching any negative example.

The both-0 rule

```prolog
a(A) :- b_val_0(A), c_val_0(A).
```

is then proposed from an early both-0 positive (the trace folds row~8). That
body is **not** a function of the root. It also holds of the negative examples
in rows~**26** and~**30**, which are the only sample atoms \((0,0,0)\). Brave
entailment therefore fails. The learner introduces an assumption
\(\alpha_1\) relative to the offending body, yielding

```prolog
a(A) :- alpha_1(A), b_val_0(A), c_val_0(A).
```

Contrary rote learning then cites exactly rows~26 and~30 as grounds for
\(\mathtt{c\_alpha\_1}\). Greedy folding of those contrary examples reconstructs
the **same** both-0 body for the contrary,

```prolog
c_alpha_1(A) :- b_val_0(A), c_val_0(A).
```

Under `asm_intro(relto)`, a further assumption cannot be introduced for that
body because \(\alpha_1\) is already present. The engine reports KO and ends
with `* No solution found!`. The cell outcome is `completed_no_solution`. No
`delta.aba` and no `bk.sol.*` artefacts are emitted.

This is a **search and repair dead-end** on this example geometry under
greedy, mgr, and relto. It is not a runner failure. The folding procedure is
the same as for target \(c\). What differs is the split of \(E^+\) across two
predictor cells and the presence of opposite labels inside the both-0 cell.

---

## ECAI narrative (`ecai2024`)

The ECAI arm uses `configs/ecai2024_config.pl`. The active options are
`learning_mode(brave)`, `folding_mode(nd)`, `folding_selection(any)`,
`folding_space(all)`, `asm_intro(relto)`, and `check_ic`. Unlike AAMAS, nd
folding takes **one** predicate replacement per fold step and does not build a
maximal co-occurrence catalogue. The first BK predicate that matches a selected
example is typically the one that appears earliest in the declared predictor
order. Authoritative traces are under
`.../ecai2024/n30_seed42/cells/target-{a,b,c}/output/`.

### Target `c` — solved by under-folding and a contrary

The path is verified in
`.../ecai2024/n30_seed42/cells/target-c/output/prolog.stdout` and in the
corresponding `delta.aba`.

Learning begins from rote positive rules indexed by sample id. The first
selected positive is row~1. Nd folding replaces that id by
\(\mathtt{a\_val\_1}\), which is the first BK predictor under the declared order
\(a\), then \(b\). The resulting unary rule is

```prolog
c(A) :- a_val_1(A).
```

That body is too strong for the AND child. Every row with \(A=1\) and \(B=0\)
is an \(E^-\) example for \(c\), yet satisfies \(\mathtt{a\_val\_1}\). Brave
entailment fails, and the learner introduces \(\alpha_1\), giving

```prolog
c(A) :- alpha_1(A), a_val_1(A).
```

Contrary rote learning then records \(\mathtt{c\_alpha\_1}\) on the seven
\((1,0,0)\) negatives that remain uncovered attacks, namely rows~**8, 9, 13,
14, 18, 24,** and **25**.

The first contrary fold attempt replaces row~8 by \(\mathtt{a\_val\_1}\). That
candidate fails, and relto cannot introduce a second assumption for that body.
A subsequent fold replaces the same contrary example by \(\mathtt{b\_val\_0}\).
Brave entailment then succeeds. All remaining contrary rotes are subsumed, and
the queue empties.

The final delta is

```prolog
c(A) :- alpha_1(A), a_val_1(A).
c_alpha_1(A) :- b_val_0(A).
assumption(alpha_1(A)).
contrary(alpha_1(A),c_alpha_1(A)) :- assumption(alpha_1(A)).
```

On this sample, the framework behaves extensionally like “derive \(c\) when
\(a=1\), unless the assumption is attacked when \(b=0\)”. Under brave checking
of the observed \(E^\pm\), that presentation is aligned with \(C=A\land B\). The
ABA **shape** is nevertheless different from the AAMAS conjunction. In
particular, the delta string does **not** match the evaluator reference
`c(A) :- a_val_1(A), b_val_1(A).`. The run reports `solved` with artefact-audit
SAT.

### Targets `a` / `b` — solved by a brave choice gadget

The path for root \(a\) is verified in
`.../ecai2024/n30_seed42/cells/target-a/output/{prolog.stdout,delta.aba}`.
Target \(b\) is the mirror with \(a\leftrightarrow b\). The arm summary records
eleven delta rules, three assumptions, and three contraries for each root, with
artefact-audit SAT.

Nd folding again takes one step at a time. From an early \((B,C)=(1,1)\)
positive (row~1), the first fold yields the unary body \(\mathtt{b\_val\_1}\).
That rule over-generalises onto \(E^-\) rows where \(B=1\) and \(C=0\) (the
trace cites rows~3, 5, 15, and~19 for the first contrary). Assumption
\(\alpha_1\) is introduced, and the contrary later folds successfully to
\(\mathtt{c\_val\_0}\). The resulting block separates the safe both-1 positives
from the \(B=1,C=0\) negatives:

```prolog
a(A) :- alpha_1(A), b_val_1(A).
c_alpha_1(A) :- c_val_0(A).
```

A second ordinary target rule is then required for the remaining both-0
positives. Folding an early both-0 positive (row~8) yields
\(\mathtt{b\_val\_0}\). Brave entailment fails because the same BK literals hold
of the \(E^-\) atoms in rows~**26** and~**30**. Assumption \(\alpha_2\) is
introduced on that body. Contrary rote cites those two negatives. Folding the
contrary first attempts \(\mathtt{b\_val\_0}\) (KO under relto against
\(\alpha_2\)), then \(\mathtt{c\_val\_0}\). Even the unary \(\mathtt{c\_val\_0}\)
contrary is still too strong for brave entailment of the joint example set, so
a further assumption \(\alpha_3\) appears on the contrary. Rote learning of
\(\mathtt{c\_alpha\_3}\) then cites the both-0 **positives** (rows~8, 9, 13,
14, 18, 24, and~25). That contrary folds by re-using \(\alpha_2\) together with
\(\mathtt{b\_val\_0}\). The resulting nest is

```prolog
a(A) :- alpha_2(A), b_val_0(A).
c_alpha_2(A) :- alpha_3(A), c_val_0(A).
c_alpha_3(A) :- alpha_2(A), b_val_0(A).
```

together with the corresponding `assumption` and `contrary` declarations.

The important geometric point is the ambiguous cell \((B,C)=(0,0)\). Row~**9**
is an \(E^+\) example for \(a\) with joint values \((1,0,0)\). Row~**26** is an
\(E^-\) example with joint values \((0,0,0)\). Both rows share the BK literals
\(\mathtt{b\_val\_0}\) and \(\mathtt{c\_val\_0}\). No deterministic rule over
\((B,C)\) can assign both labels. The \(\alpha_2\)/\(\alpha_3\) nest is a
**per-row assumption choice gadget**. Within one witnessing stable model, the
ground assumption atoms for different row identifiers can take different
statuses, permitting \(a\) to hold at row~9 while being rejected at row~26.
Other stable models may make different choices. Brave entailment requires the
existence of at least one stable model that meets the **joint** \(E^\pm\)
constraints; it does not use a separate witness for each example and does
**not** require a unique determination of \(a\) from \((b,c)\).

The runner outcome `solved` therefore means that a serialized ABA framework
passed brave entailment and that the artefact audit reported SAT. That outcome
is **misleading** if it is read as recovery of a functional root mechanism.
The evaluator reference for roots remains
`no_observed_parent_deterministic_rule`.
---

## Cross-arm / cross-target synthesis

| | Child `c` | Roots `a` / `b` |
|--|-----------|-----------------|
| **AAMAS** | Solved with an assumption-free AND conjunction. The delta string coincides with the evaluator reference. | No solution. The greedy both-0 body and contrary repair fail on rows 26 and 30. |
| **ECAI** | Solved with \(\alpha_1\) and a `b_val_0` contrary after under-folding to `a`. | Solved with a brave choice gadget on the ambiguous `(0,0)` cell. |

**Arm slogan for roots.** AAMAS fails to emit a false functional both-0 Horn
rule and fails entirely. ECAI emits a **non-functional brave covering** of the
same ambiguous cell. Neither recovers a root mechanism.

**Same frozen table.** The differences are strategy, entailment semantics, and
target geometry, not resampling. The AAMAS `c` string match is not causal
discovery. The ECAI assumed form for `c` is not “recovered AND” as a claim.

The `sol_chk` SAT result is a final-artefact integrity audit under `check_ic`,
not a separate coverage metric (arm `summary.md` interpretation boundary).

---

## Authoritative artefact pointers

| Role | Path |
|------|------|
| AAMAS summary | `.../aamas2025/n30_seed42/summary.md` |
| ECAI summary | `.../ecai2024/n30_seed42/summary.md` |
| AAMAS `c` delta | `.../aamas2025/.../cells/target-c/output/delta.aba` |
| AAMAS `a` trace (no-solution) | `.../aamas2025/.../cells/target-a/output/prolog.stdout` |
| ECAI `c` delta / trace | `.../ecai2024/.../cells/target-c/output/{delta.aba,prolog.stdout}` |
| ECAI `a` / `b` deltas | `.../ecai2024/.../cells/target-{a,b}/output/delta.aba` |
| Mechanism reference | `causal/outputs/causal_fixtures/m13_bucket3_binary_collider_and/mechanism_reference.json` |
| Frozen sample | `.../samples/n30_seed42.csv` |

---

## Explicit non-claims

- Not Russo-style Causal ABA, DAG recovery, or CPDAG recovery.
- Not “ABALearn recovered the causal mechanism” merely from AAMAS `c` string
  match to the evaluator reference.
- Not “ECAI recovered AND in assumed form” as a project claim.
- Not parent-set scoring of root deltas without the brave / non-functional
  caveat.
- Not that `sol_chk` SAT is a separate coverage or recovery metric.
- H1–H4 follow-ups are outside this H0 record. H1 is documented in
  `h1_support_ablation.md`. Remaining probes: `future_probes.md`.

## Next step

H0 is closed. Probe **H1** is documented in `h1_support_ablation.md`. Remaining
deferred probes H2–H4 are recorded in `future_probes.md`. Still **no Bucket 3
claim**.
