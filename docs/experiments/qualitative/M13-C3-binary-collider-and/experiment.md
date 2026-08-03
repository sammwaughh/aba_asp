# M13-C3 — Binary deterministic AND collider (Bucket 3)

## Status

`proposed | planned | implemented | run | analysed | reported`

Current status: **`H0 closed / analysed`; H1–H3 run / analysed** — M1.3 Bucket 3
baseline complete; H1–H3 probes documented; H4 cautious infrastructure ready
but unrun; H5 cautious Greedy deferred; **no Bucket 3 claim**.

### H0 versus H1–H5

| Label | Meaning |
|-------|---------|
| **H0** | Closed baseline: fixture `m13_bucket3_binary_collider_and`; frozen sample `n30_seed42`; AAMAS and ECAI arms on all targets `a`, `b`, `c`; Trace + fixture integration; documented in `learning_analysis.md` / `.tex`. |
| **H1** | Nested-prefix AAMAS support ablation (`n25_seed42`). **Run / analysed.** Record: `h1_support_ablation.md` / `.tex`. **Not a claim.** |
| **H2** | Isolated-\(D\) AND collider; AAMAS target `c` retains irrelevant `d`. **Run / analysed.** Record: `h2_irrelevant_covariate.md` / `.tex`. **Not a claim.** |
| **H3** | BK-leading isolated `a` on BD AND; ECAI distracts first fold for `c`. **Run / analysed.** Record: `h3_bk_leading_distractor.md` / `.tex`. **Not a claim.** |
| **H4** | Repository-baseline cautious vs locked ECAI brave on the H0 table. **Infrastructure ready / not run.** Roots `a`/`b` primary; `c` control. |
| **H5** | Cautious Greedy ABA Learning. **Deferred theory/design question; no config or run.** |

**H0 close means:** baseline learning analysis finished.  
**H1–H3 complete means:** those approved probes are run and documented.
**Does not mean:** a Bucket 3 claim is locked. Still **no Bucket 3 claim**.

Working mathematical dossier (pre-run): `fixture_dossier.tex`.  
Closed H0 learning record: `learning_analysis.md` / `learning_analysis.tex`.  
**H1 record:** `h1_support_ablation.md` / `h1_support_ablation.tex`.  
**H2 record:** `h2_irrelevant_covariate.md` / `h2_irrelevant_covariate.tex`.  
**H3 record:** `h3_bk_leading_distractor.md` / `h3_bk_leading_distractor.tex`.  
**Remaining probes:** `future_probes.md` / `future_probes.tex`
(H4 infrastructure ready/unrun; H5 deferred).

## Purpose

Record and interpret what target-wise ABALearn does on the approved binary
AND collider under AAMAS and ECAI configurations on one frozen IID table,
relative to the evaluator-only mechanism reference — without elevating
observations to Bucket 3 claims.

## Research question

> For the approved binary collider \(A \rightarrow C \leftarrow B\) with
> mutually independent non-degenerate roots and deterministic \(C=A\land B\),
> what does target-wise ABALearn recover from one frozen IID table for every
> variable as target, and how do any learned rules relate to the evaluator-only
> mechanism reference and to the information present in the population versus
> the finite sample?

**Six-cell answer (bounded; not a claim):** see `learning_analysis.md`.
Briefly: AAMAS solves `c` with an assumption-free AND conjunction
(syntactic coincidence with the evaluator reference) and fails on roots
`a`/`b` via both-0 / contrary KO on rows 26–30; ECAI solves all three targets,
with `c` via under-fold to `a` plus `b_val_0` contrary, and roots via a brave
choice gadget on the ambiguous `(0,0)` cell. Neither arm recovers a root
mechanism.


## Theoretical motivation

### ABA foundations

Any later learned object will be an ABA framework (rules, assumptions,
contraries, attacks, and acceptance under the chosen semantics). Causal roles
are not intrinsic properties of exact-value predicates in that framework.

### ABA Learning / ABALearn

ABALearn will receive, per target, table-derived background knowledge and
positive/negative examples only. Graph edges, population certificates, and the
mechanism reference must not enter the learning input.

### Causal ABA / argumentative causal discovery

This investigation does **not** exercise Russo-style `arr`/`noe`/`indep`
assumptions, d-separation reasoning inside ABA, or stable extensions as
candidate DAGs. The generating DAG and CI/CPDAG certificates are evaluator
infrastructure for controlled interpretation of ABALearn outputs.

### Current `aba_asp/causal` implementation

Target-wise bridge (`causal/targetwise/`): one frozen sample, every variable as
target, binary exact-value BK, target value `1` as \(E^+\) and `0` as \(E^-\).
AAMAS and ECAI collections for this fixture are complete under
`causal/outputs/aba_learning/targetwise/m13_bucket3_binary_collider_and/`.
The stochastic diamond under `m13_bucket3_binary_diamond` remains pre-pivot
provenance only.

## Relation to ABA Learning

**Executed** on frozen `n30_seed42` for all targets under both published arms:

- AAMAS: `configs/aamas2025_config.pl` (brave, greedy, mgr, `folding_space(bk)`)
- ECAI: `configs/ecai2024_config.pl` (brave, nd, any, all)

Learner-visible regime: exact-value BK for non-targets; positives = target
value `1`; negatives = value `0`. Realised \(E^\pm\) counts:

| Target | \(E^+\) | \(E^-\) |
|--------|--------:|--------:|
| `a` | 24 | 6 |
| `b` | 21 | 9 |
| `c` | 17 | 13 |

Full six-cell narrative: `learning_analysis.md`.

## Relation to Causal ABA

The investigation uses an observational causal Bayesian network and its
ordinary CI structure as evaluator context. It does not implement or test
Russo-style Causal ABA.

## Implementation scope

### Code/config paths

- Authoritative fixture YAML:
  `causal/fixtures/specs/m13_bucket3_binary_collider_and.yaml`
- H2 fixture YAML:
  `causal/fixtures/specs/m13_bucket3_binary_collider_and_iso_d.yaml`
- Fixture toolkit: `causal/fixtures/README.md`
- Target-wise: `causal/targetwise/README.md`
- Target-wise configs:
  `causal/configs/targetwise/m13_bucket3_binary_collider_and/aamas2025/{n30_seed42,n25_seed42}.yaml`
  and `.../ecai2024/n30_seed42.yaml`; prepared H4:
  `.../baseline_cautious/n30_seed42.yaml`
- H2 target-wise configs:
  `causal/configs/targetwise/m13_bucket3_binary_collider_and_iso_d/aamas2025/{n30_seed42,n2_seed42}.yaml`
- Learning outputs:
  `causal/outputs/aba_learning/targetwise/m13_bucket3_binary_collider_and/{aamas2025,ecai2024}/n30_seed42/`
  and H1 AAMAS `.../aamas2025/n25_seed42/`
- H2 learning outputs:
  `causal/outputs/aba_learning/targetwise/m13_bucket3_binary_collider_and_iso_d/aamas2025/{n30_seed42,n2_seed42}/`

### Documentation files for this investigation

- `learning_analysis.md` / `learning_analysis.tex` — **closed H0** six-cell record
- `h1_support_ablation.md` / `h1_support_ablation.tex` — **H1** nested-prefix record
- `h2_irrelevant_covariate.md` / `h2_irrelevant_covariate.tex` — **H2** isolated-\(D\) record
- `h3_bk_leading_distractor.md` / `h3_bk_leading_distractor.tex` — **H3** BK-leading record
- `experiment.md` (status / outcome pointer)
- `fixture_dossier.tex` (pre-run mathematical account)
- `future_probes.md` / `.tex` (probe catalogue; H1–H3 analysed; H4 infra
  ready/unrun; H5 deferred)
- `M1.3-bucket3-claims.md`, `experiments_summary.md`, `experiment_register.md`,
  `research_state.md` as needed for factual status

### Files / artefacts inspected (not modified)

Pre-run fixture bundle under
`causal/outputs/causal_fixtures/m13_bucket3_binary_collider_and/`
plus AAMAS/ECAI target-wise cells under
`causal/outputs/aba_learning/targetwise/m13_bucket3_binary_collider_and/`.
H2 fixture bundle under
`causal/outputs/causal_fixtures/m13_bucket3_binary_collider_and_iso_d/`
plus its AAMAS `n30_seed42` and `n2_seed42` target-wise collections.
Preserved pre-pivot diamond artefacts unchanged.

## Dataset / data-generating process

### Source

Exact finite-discrete causal Bayesian network, schema version 2,
`mechanism_regime: root_stochastic_deterministic_nonroots`.

Authoritative specification:
`causal/fixtures/specs/m13_bucket3_binary_collider_and.yaml`.

Provenance hashes (`fixture_manifest.json` / certificate):

| Hash basis | Value |
|---|---|
| Source UTF-8 bytes | `sha256:4ec5bb5726f4359a6b347e519ebcdbf1ef79a945ccd54a40d601dad240d824f8` |
| Canonical parsed YAML document | `sha256:f061e29abc8ba8bc1fcd8630ef1f79e38c8171b36b6ee09afb5f88e94eac4298` |
| Semantic model | `sha256:e76c1ff5b849cf6f11ec161e4dbd23573fb39891d846596b155bf047fd687731` |

### Graph / structure

```text
a → c ← b
(no a–b edge)
```

Display: \(A \rightarrow C \leftarrow B\). Unshielded collider at \(c\).
MEC size 1; ordinary CI CPDAG uniquely orients both edges
(`certificate.json`).

### Variables

| Internal | Display | Role | Mechanism |
|---|---|---|---|
| `a` | \(A\) | root / source | \(\mathrm{Bernoulli}(4/5)\); CPT \([1/5, 4/5]\) |
| `b` | \(B\) | root / source | \(\mathrm{Bernoulli}(7/10)\); CPT \([3/10, 7/10]\) |
| `c` | \(C\) | sink / collider | deterministic \(C=A\land B\) |

Roots are mutually independent by fixture design
(`exogenous_noise: mutually_independent_root_exogenous_noise`).

### Sample sizes

- Population: exact joint over 8 assignments (support size 4).
- Frozen baseline sample: \(n=30\), seed `42` (**approved**).

### Seeds

- Sample seed: `42`
- Sampler: `row_major_ancestral_inverse_cdf` v2; NumPy `PCG64`
- Randomness confined to roots; deterministic non-roots consume no draw
  (`n30_seed42.manifest.json`)

### Noise / stochasticity

Non-degenerate stochasticity only at roots. Non-root `c` is a point-mass CPT
on every parent assignment. Ordinary faithfulness is **not** inferred from
determinism; it is certified by the exhaustive singleton-pair CI ↔ d-separation
audit (`ordinary_faithfulness.status: verified_exactly`).

## Encoding

### Target variable(s)

Executed all-target investigation on the same frozen table:

| Target | True parents | Target type | Evaluator reference status |
|---|---|---|---|
| `a` | \(\emptyset\) | stochastic root | `no_observed_parent_deterministic_rule` |
| `b` | \(\emptyset\) | stochastic root | `no_observed_parent_deterministic_rule` |
| `c` | `{a,b}` | deterministic non-root collider | canonical rule available |

### Positive / negative examples

Constructed separately for each target from the same frozen table under the
binary exact-value policy (target value `1` positive, `0` negative). The realised
arrays are stored in each cell's `input/examples.json`; their counts are listed
in the ABA Learning section above. Changing the target did not resample the
table.

### Background knowledge

Generated independently for each target in `input/bk.aba`, using exact-value
predicates for the two non-target columns only. The graph, certificate, and
mechanism reference remained evaluator-only and were not included in BK or the
example arrays.

## Commands run

Pre-run fixture build / certification was performed before this documentation
pass (artefacts already present). Documentation inspection did not re-run the
CLI. Canonical build form (from `causal/fixtures/README.md`):

```bash
python -m causal.fixtures.cli build \
  --fixture causal/fixtures/specs/m13_bucket3_binary_collider_and.yaml \
  --output-dir causal/outputs/causal_fixtures/m13_bucket3_binary_collider_and \
  --n 30 --seed 42
```

The completed target-wise collections correspond to these entry points:

```bash
python -m causal.targetwise.cli run \
  --config causal/configs/targetwise/m13_bucket3_binary_collider_and/aamas2025/n30_seed42.yaml

python -m causal.targetwise.cli run \
  --config causal/configs/targetwise/m13_bucket3_binary_collider_and/ecai2024/n30_seed42.yaml
```

The arm `run.log` and `summary.md` files record the realised execution sequence
and outcomes. This documentation reconciliation did not rerun either collection.

## Environment

Recorded in `n30_seed42.manifest.json` for the frozen sample:

- Python: `3.10.20`
- NumPy: `2.2.6`
- pandas: `2.3.3`
- Fixture toolkit version: `2`
- Git commit at documentation write: `b534fd5` (working tree may differ after
  this documentation edit)

SWI-Prolog / clingo: invoked for AAMAS and ECAI target-wise collections
(see arm manifests / run logs under the target-wise output trees).

## Artefact paths

| Artefact | Path | Notes |
|---|---|---|
| Spec (authoritative) | `causal/fixtures/specs/m13_bucket3_binary_collider_and.yaml` | schema v2 |
| Population / certificate / mechanism reference | `causal/outputs/causal_fixtures/m13_bucket3_binary_collider_and/` | evaluator-only |
| Sample (H0) | `.../samples/n30_seed42.csv` | target-free |
| Sample (H1) | `.../samples/n25_seed42.csv` | nested prefix of H0 |
| AAMAS H0 collection | `.../targetwise/.../aamas2025/n30_seed42/` | `summary.md` + 3 cells |
| AAMAS H1 collection | `.../targetwise/.../aamas2025/n25_seed42/` | nested-prefix ablation |
| ECAI collection | `.../targetwise/.../ecai2024/n30_seed42/` | `summary.md` + 3 cells |
| H2 spec / fixture bundle | `causal/fixtures/specs/m13_bucket3_binary_collider_and_iso_d.yaml`; `causal/outputs/causal_fixtures/m13_bucket3_binary_collider_and_iso_d/` | isolated-(D) fixture |
| H2 AAMAS collections | `.../targetwise/m13_bucket3_binary_collider_and_iso_d/aamas2025/{n30_seed42,n2_seed42}/` | main H2 + secondary H2c |
| Pre-run LaTeX dossier | `fixture_dossier.tex` | population / certificates |
| Learning analysis | `learning_analysis.md` / `.tex` | **closed H0** six-cell narrative |
| H1 record | `h1_support_ablation.md` / `.tex` | nested-prefix AAMAS ablation |
| H2 record | `h2_irrelevant_covariate.md` / `.tex` | isolated-\(D\) AAMAS target `c` |
| H3 record | `h3_bk_leading_distractor.md` / `.tex` | BK-leading ECAI target `c` |
| Future probes | `future_probes.md` / `.tex` | H1–H3 analysed; H4 infra ready/unrun; H5 deferred |

## Outcome summary

### Pre-run (unchanged)

Population support size 4; ordinary faithfulness `verified_exactly`; MEC size 1;
evaluator ref `c(A) :- a_val_1(A), b_val_1(A).`; roots
`no_observed_parent_deterministic_rule`; sample joints
\((1,1,1):17\), \((1,0,0):7\), \((0,1,0):4\), \((0,0,0):2\).

### Learning (H0 — six cells, closed)

| Arm | `a` | `b` | `c` |
|-----|-----|-----|-----|
| AAMAS | `completed_no_solution` | `completed_no_solution` | `solved` — `c :- a_val_1, b_val_1` |
| ECAI | `solved` (α-framework on `b`) | `solved` (mirror) | `solved` — `c :- α₁, a_val_1` + contrary `b_val_0` |

Full narrative, geometry, and non-claims: `learning_analysis.md`.

### H1 (AAMAS nested prefix \(n{=}25\), analysed)

| Target | H0 \(n{=}30\) | H1 \(n{=}25\) | H1 reading |
|--------|---------------|---------------|------------|
| `a` | no-solution (**correct**) | **solved** (**incorrect**) | spurious both-0 Horn |
| `b` | no-solution (**correct**) | **solved** (**incorrect**) | mirror |
| `c` | solved AND | solved AND | control |

Full H1 record and evaluative stance: `h1_support_ablation.md`.

### H2 (AAMAS isolated-\(D\) target `c`, analysed)

On fixture `m13_bucket3_binary_collider_and_iso_d` / `n30_seed42`, AAMAS
**solves** `c` with bodies that **include irrelevant `d_val_*`**, not the
evaluator \(D\)-free AND. Full record: `h2_irrelevant_covariate.md`.

### H3 (ECAI BK-leading `a` on BD AND, analysed)

On fixture `m13_bucket3_binary_bd_and_lead_a` / `n30_seed42`, ECAI first-folds
to `a_val_*` and retains `a` in the theory for `c` (not the evaluator BD AND).
AAMAS contrast also retains `a_val_*`. Full record:
`h3_bk_leading_distractor.md`.

## Quantitative results

Arm summaries record outcomes, delta/assumption counts, body variables, and
artefact-audit status. No parent-set F1 or graph decoder is applied (target-wise
interpretation boundary).

## Qualitative learned-rule inspection

See `learning_analysis.md` (AAMAS `c` conjunction; AAMAS root both-0 KO;
ECAI `c` under-fold; ECAI root brave choice gadget on rows 9 vs 26).

## Failure modes

Distinctions preserved in the learning analysis:

- population vs finite sample;
- evaluator-only metadata vs learner-visible BK/\(E^\pm\);
- predictive covering vs mechanism-aligned interpretation;
- strategy / entailment semantics vs informational limits;
- AAMAS root no-solution vs ECAI brave non-functional covering of the same
  ambiguous cell.

## Interpretation notes

**Pre-run facts** remain as certified in `fixture_dossier.tex`.

**H0 bounded reading (not a claim).** Same frozen `n30` table; AAMAS and ECAI
differ by strategy. AAMAS recovers an assumption-free AND conjunction for `c`
(syntactic coincidence with the evaluator reference) and fails on roots. ECAI
solves all targets with different ABA shapes; root `solved` is brave coverage
via a choice gadget, not functional root-mechanism recovery. Under the H1
evaluative stance, AAMAS root `completed_no_solution` is the **correct**
outcome for roots. See `learning_analysis.md`.

**H1 bounded reading (not a claim).** On nested prefix \(n{=}25\), AAMAS
**incorrectly** solves roots with spurious both-0 Horn rules after omitting
rare \((0,0,0)\). See `h1_support_ablation.md`.

**H2 bounded reading (not a claim).** On the isolated-\(D\) fixture, AAMAS
target `c` retains irrelevant `d_val_*` rather than the evaluator \(D\)-free
AND. See `h2_irrelevant_covariate.md`.

**H3 bounded reading (not a claim).** On the BD AND fixture with BK-leading
isolated `a`, ECAI pulls `a` into the learned theory for `c` (first-fold
distraction). Brave residual splits remain possible. See
`h3_bk_leading_distractor.md`. **No Bucket 3 claim.**

## Claims supported

None. Evidence record and bounded interpretation only.

## Claims not supported / not claimed

As in `learning_analysis.md`, `h1_support_ablation.md`,
`h2_irrelevant_covariate.md`, and `h3_bk_leading_distractor.md` non-claims
sections. H4/H5 have no result.

## Report relevance

Interim Experimentation / Progress (Milestone 1 Part 3 / Bucket 3). Working
evidence only; **not** report-facing claim prose.

## Future probes

H1–H3 are **run / analysed**. H4 cautious target-wise infrastructure is ready,
but the collection has not been run; H5 cautious Greedy is deferred:
`future_probes.md` / `.tex`. Still **no Bucket 3 claim**.

## Next decision

1. When to start, run, and trace the prepared H4 cautious baseline.
2. Keep Bucket 3 free of a claim until inspected probe evidence warrants a
   separate decision.
