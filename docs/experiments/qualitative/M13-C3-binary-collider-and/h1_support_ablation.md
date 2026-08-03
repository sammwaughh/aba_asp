# M13-C3 — H1 support ablation (AAMAS nested prefix)

## Status

**H1 run / analysed.** Nested-prefix AAMAS ablation on fixture
`m13_bucket3_binary_collider_and` is complete and documented here
(Markdown) and in `h1_support_ablation.tex`.

- Closed H0 baseline preserved (`n30_seed42`; see `learning_analysis.md`)
- H1 intervention: nested seed-42 prefix `n=25` (exact first 25 rows of H0)
- AAMAS only; all targets `a`, `b`, `c`
- **Not a Bucket 3 claim**
- H2 and H3 are documented in `h2_irrelevant_covariate.md` and
  `h3_bk_leading_distractor.md`; H4 and H4b are run / analysed
  (`h4_cautious_vs_brave.md`, `h4b_cautious_split_under_a.md`); H5 deferred; H6/H7 signposted
  (see `future_probes.md`)

Companion records: `experiment.md` (hub); `future_probes.md` (probe catalogue);
`learning_analysis.md` (closed H0).

---

## Research question

> On the closed H0 AND-collider fixture under AAMAS, if a nested seed-42 prefix
> omits the only sample atoms \((0,0,0)\), do root targets flip from the H0
> outcome `completed_no_solution` to a `solved` delta that includes a spurious
> both-0 co-occurrence Horn rule?

## Evaluative stance (do not invert)

For this fixture, roots `a` and `b` have **no** deterministic causal rule over
the other observed variables. The evaluator-only reference records
`no_observed_parent_deterministic_rule` for those targets.

Therefore, under the H1 research reading:

| Outcome | Reading |
|---------|---------|
| H0 AAMAS root `completed_no_solution` | **Desired / correct** for those targets |
| H1 AAMAS root `solved` with co-occurrence Horn rules | **Incorrect / spurious** — a finite-sample mistake, **not** successful mechanism recovery |

H1 demonstrates that **AAMAS can incorrectly return a solution for a root
target when the sample undersamples rare joint assignments that would have
blocked an over-general rule**, especially when that assignment has **low
population probability** (\(P(A{=}0,B{=}0,C{=}0)=3/50=0.06\)) and **\(n\) is
small** (here \(n=25\)).

Do **not** frame H1 as “AAMAS learns roots better with less data”. Do **not**
treat root `solved` as progress.

---

## Design

### Intervention

Nested seed-42 prefix `n=25` of the closed H0 sample `n30_seed42` (exact first
25 rows). That prefix omits the only H0 \((0,0,0)\) rows (CSV rows **26** and
**30**). Fixture, encoding, AAMAS configuration, and seed sequence are otherwise
unchanged.

Verified controls:

- `n25_seed42.csv` is a row-for-row prefix of `n30_seed42.csv`
- No \((0,0,0)\) atom appears in `n25` (joint counts:
  \((1,1,1):14\), \((1,0,0):7\), \((0,1,0):4\))
- Same AAMAS `configuration.id` (`aamas2025`) and configuration hash as H0
  (`sha256:93ee2bb829096988ba7b84a7ef2f0247e0cfd8a069909a5146500be9d10e7407`).
  Only the sample (`n`, CSV hash) changes
- The population still assigns positive mass to \((0,0,0)\). Only the finite
  table omits it

### Paths

| Role | Path |
|------|------|
| Sample CSV | `causal/outputs/causal_fixtures/m13_bucket3_binary_collider_and/samples/n25_seed42.csv` |
| Sample manifest | `.../samples/n25_seed42.manifest.json` |
| Target-wise config | `causal/configs/targetwise/m13_bucket3_binary_collider_and/aamas2025/n25_seed42.yaml` |
| H1 collection | `causal/outputs/aba_learning/targetwise/m13_bucket3_binary_collider_and/aamas2025/n25_seed42/` |
| H0 AAMAS comparison (unchanged) | `.../aamas2025/n30_seed42/` |

Sample hash (H1):
`sha256:c7ccf94c10a7862f34b7eeedb61529cf60ac0b13b932ac608beaea1a6d17fdd4`.

### Commands (reproducible form)

From the repository root, with the project environment active:

```bash
python -m causal.targetwise.cli run \
  --config causal/configs/targetwise/m13_bucket3_binary_collider_and/aamas2025/n25_seed42.yaml
```

(Validate/prepare variants follow the same config path as in
`causal/targetwise/README.md`.)

Learner options remain those of `configs/aamas2025_config.pl`: brave, greedy,
mgr, `folding_space(bk)`, relto, `check_ic`.

---

## Results (AAMAS)

Authoritative outcome table: H1 arm `summary.md`. Comparison uses closed H0
AAMAS `summary.md` under `n30_seed42`.

| Target | H0 \(n{=}30\) | H1 \(n{=}25\) | H1 delta (if any) | H1 reading |
|--------|---------------|---------------|-------------------|------------|
| `a` | `completed_no_solution` (**correct**) | **`solved`** (**incorrect**) | `a :- b_val_1, c_val_1` and `a :- b_val_0, c_val_0` | spurious root solve |
| `b` | `completed_no_solution` (**correct**) | **`solved`** (**incorrect**) | mirror with `a`/`c` | spurious root solve |
| `c` | `solved` AND (control) | `solved` AND | `c :- a_val_1, b_val_1` | control unchanged in kind |

H1 \(E^\pm\) sizes from the arm summary: `a` 21/4, `b` 18/7, `c` 14/11.
Artefact audit SAT on all three H1 cells. Zero assumptions on all three H1
deltas.

### Root deltas (verified)

Target `a` (`.../n25_seed42/cells/target-a/output/delta.aba`):

```prolog
a(A) :- b_val_1(A), c_val_1(A).
a(A) :- b_val_0(A), c_val_0(A).
```

Target `b` (`.../cells/target-b/output/delta.aba`):

```prolog
b(A) :- a_val_1(A), c_val_1(A).
b(A) :- a_val_0(A), c_val_0(A).
```

Target `c` (`.../cells/target-c/output/delta.aba`):

```prolog
c(A) :- a_val_1(A), b_val_1(A).
```

The both-0 root rules are **false** as population implications. They are
sample-adequate only because the H1 table contains no opposite-label witness
in that predictor cell.

---

## Trace / fixture reading

Procedural comparison uses
`.../aamas2025/n25_seed42/cells/target-a/output/prolog.stdout` against the
closed H0 trace
`.../aamas2025/n30_seed42/cells/target-a/output/prolog.stdout`
(target `b` is symmetric).

Under AAMAS greedy folding, both runs build maximal co-occurrence bodies from
BK. The both-1 body

```prolog
a(A) :- b_val_1(A), c_val_1(A).
```

is accepted under brave entailment on both tables.

The both-0 body

```prolog
a(A) :- b_val_0(A), c_val_0(A).
```

is then proposed from an early both-0 positive (row~8 on both traces).

- On **H1** (\(n=25\)): brave entailment of \(\langle E^+,E^-\rangle\)
  **succeeds** immediately after that fold. No assumption is introduced. The
  queue empties. The run terminates as `solved` with the two Horn rules above.
- On **H0** (\(n=30\)): the same both-0 body fails brave entailment because
  rows~**26** and~**30** are \(E^-\) examples that share
  \(\mathtt{b\_val\_0}\) and \(\mathtt{c\_val\_0}\). Assumption/contrary repair
  reconstructs the same both-0 body for the contrary. Relto cannot introduce a
  further assumption. The engine reports KO and `* No solution found!`.

The AAMAS search procedure is therefore the same until the both-0 commit. What
flips the outcome is the **absence versus presence of a label conflict inside
that greedy candidate body cell**. The missing conflict is exactly the rare
joint \((0,0,0)\), which has population probability \(3/50=0.06\) and appears
only twice in the H0 table of size 30.

Child target `c` remains a control: both H0 and H1 emit the assumption-free
AND conjunction. That does not change the root evaluative stance.

---

## Bounded interpretation

On this fixture and AAMAS configuration, omitting the rare conflicting joint
from a small nested prefix converts the **correct** root outcome
(`completed_no_solution`) into an **incorrect** spurious Horn covering of the
ambiguous both-0 cell. That is a finite-sample / support-sensitivity effect for
greedy maximal co-occurrence search. It is **not** evidence that shorter tables
recover root mechanisms.

Roots remain non-mechanistic under the evaluator reference. Predictive
co-occurrence covering is not mechanism recovery.

---

## Explicit non-claims

- Not a Bucket 3 claim.
- Not Russo-style Causal ABA, DAG recovery, or CPDAG recovery.
- Not “AAMAS recovered the root mechanism” on \(n=25\).
- Not “AAMAS learns roots better with less data”.
- Not a claim that every seed or every \(n\) behaves identically.
- Not a claim that omitting \((0,0,0)\) is the only way AAMAS can emit a
  spurious root rule.
- Later probes H2–H4 and H4b are separate records.

---

## Cross-links

- Investigation hub: `experiment.md`
- Closed H0 learning record: `learning_analysis.md` / `.tex`
- Probe catalogue: `future_probes.md` / `.tex`
- Bucket 3 planning hub: `../M1.3-bucket3-claims.md` (still **no claim**)

## Next step

H1 documentation is complete. Probes **H2–H4+H4b** are documented in
`h2_irrelevant_covariate.md`, `h3_bk_leading_distractor.md`, and
`h4_cautious_vs_brave.md`, with H4b in `h4b_cautious_split_under_a.md`. H5
remains deferred and H6/H7 are signposted only
in `future_probes.md`. Still **no Bucket 3 claim**.
