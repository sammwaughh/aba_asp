# M13-C3 — Binary deterministic AND collider (Bucket 3)

## Status

`proposed | planned | implemented | run | analysed | reported`

Current status: **`H0 closed / analysed`** — M1.3 Bucket 3 baseline
investigation complete; probes H1–H4 deferred; **no Bucket 3 claim**.

### H0 versus H1–H4

| Label | Meaning |
|-------|---------|
| **H0** | Closed baseline: fixture `m13_bucket3_binary_collider_and`; frozen sample `n30_seed42`; AAMAS and ECAI arms on all targets `a`, `b`, `c`; Trace + fixture integration; documented in `learning_analysis.md` / `.tex`. |
| **H1–H4** | Deferred follow-up probes motivated by H0 (not part of H0). Designs and status in `future_probes.md` / `.tex`. |

**Close means:** baseline learning analysis finished. Move on to the deferred
probes subject to their recorded status: H1 precedes H2, H3 may be selected
independently, and H4 remains proposed / infrastructure-blocked.
**Does not mean:** a Bucket 3 claim is locked, or that H1–H4 are cancelled.
Still **no Bucket 3 claim**.

Working mathematical dossier (pre-run): `fixture_dossier.tex`.  
Closed H0 learning record: `learning_analysis.md` / `learning_analysis.tex`.  
**Future probes (deferred, outside H0):** `future_probes.md` / `future_probes.tex`
(H1–H3 designs approved; H4 proposed / infra-blocked).

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
- Fixture toolkit: `causal/fixtures/README.md`
- Target-wise: `causal/targetwise/README.md`
- Target-wise configs:
  `causal/configs/targetwise/m13_bucket3_binary_collider_and/{aamas2025,ecai2024}/n30_seed42.yaml`
- Learning outputs:
  `causal/outputs/aba_learning/targetwise/m13_bucket3_binary_collider_and/{aamas2025,ecai2024}/n30_seed42/`

### Documentation files for this investigation

- `learning_analysis.md` / `learning_analysis.tex` — **closed H0** six-cell record
- `experiment.md` (status / outcome pointer; H0 closed)
- `fixture_dossier.tex` (pre-run mathematical account)
- `future_probes.md` / `.tex` (H1–H4 deferred, outside H0)
- `M1.3-bucket3-claims.md`, `experiments_summary.md`, `experiment_register.md`,
  `research_state.md` as needed for factual status

### Files / artefacts inspected (not modified)

Pre-run fixture bundle under
`causal/outputs/causal_fixtures/m13_bucket3_binary_collider_and/`
plus AAMAS/ECAI target-wise cells under
`causal/outputs/aba_learning/targetwise/m13_bucket3_binary_collider_and/`.
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
| Sample | `.../samples/n30_seed42.csv` | target-free |
| AAMAS collection | `.../targetwise/.../aamas2025/n30_seed42/` | `summary.md` + 3 cells |
| ECAI collection | `.../targetwise/.../ecai2024/n30_seed42/` | `summary.md` + 3 cells |
| Pre-run LaTeX dossier | `fixture_dossier.tex` | population / certificates |
| Learning analysis | `learning_analysis.md` / `.tex` | **closed H0** six-cell narrative |
| Future probes | `future_probes.md` / `.tex` | H1–H4 deferred (motivated by H0) |

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

**Learning-stage bounded reading (not a claim).** Same frozen table; AAMAS and
ECAI differ by strategy. AAMAS recovers an assumption-free AND conjunction for
`c` (syntactic coincidence with the evaluator reference) and fails on roots.
ECAI solves all targets with different ABA shapes; root `solved` is brave
coverage via a choice gadget, not functional root-mechanism recovery.
**No Bucket 3 claim.**

## Claims supported

None. Evidence record and bounded interpretation only.

## Claims not supported / not claimed

As in `learning_analysis.md` non-claims section (no Russo Causal ABA; no
mechanism recovery from string match; no ECAI-AND claim; no root parent-set
scoring without brave caveat; H1–H4 not results of this pass).

## Report relevance

Interim Experimentation / Progress (Milestone 1 Part 3 / Bucket 3). Working
evidence only; **not** report-facing claim prose.

## Future probes

Deferred outside H0: `future_probes.md` / `.tex` (H1–H4). Motivated by the
closed H0 baseline. Not part of the H0 six-cell result.

## Next decision

1. Open a deferred probe consistently with `future_probes.md`: H1 precedes H2;
   H3 may be selected independently; H4 remains proposed / infrastructure-blocked.
2. Keep Bucket 3 free of a claim until inspected probe evidence warrants a
   separate decision.
