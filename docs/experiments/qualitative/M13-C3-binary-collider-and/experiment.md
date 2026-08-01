# M13-C3 — Binary deterministic AND collider (Bucket 3 pre-run)

## Status

`proposed | planned | implemented | run | analysed | reported`

Current status: **`implemented` (pre-run only)** — active M1.3 Bucket 3
investigation; fixture approved and certified; frozen sample `n30_seed42`
inspected; **ABALearn not yet run**; **no Bucket 3 claim**.

Working mathematical dossier (not report prose):
`docs/experiments/qualitative/M13-C3-binary-collider-and/fixture_dossier.tex`.

**Future probes:** `future_probes.md` / `future_probes.tex` —
H1–H3 **designs approved** for investigation (not yet run; not claims);
H4 **proposed** (cautious vs brave on ECAI roots; **blocked** on target-wise
cautious support; not a claim). H3 fixture id:
`m13_bucket3_binary_bd_and_lead_a`.

## Purpose

Record the first approved Bucket 3 deterministic research fixture before any
ABALearn execution: generating DAG, root-stochastic / non-root-deterministic
mechanisms, exact population certificate, evaluator-only mechanism reference,
and one frozen IID sample. The record preserves the pre-learning boundary so
later target-wise outputs can be interpreted against known generating structure
without conflating evaluator metadata with learner-visible inputs.

## Research question

> For the approved binary collider \(A \rightarrow C \leftarrow B\) with
> mutually independent non-degenerate roots and deterministic \(C=A\land B\),
> what does target-wise ABALearn recover from one frozen IID table for every
> variable as target, and how do any learned rules relate to the evaluator-only
> mechanism reference and to the information present in the population versus
> the finite sample?

At this documentation stage the question is **open**: only the pre-run objects
are certified. No learning outcomes exist yet.

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

The intended next stage is the target-wise bridge
(`causal/targetwise/`): one frozen sample, every variable as target, binary
exact-value BK, target value `1` as \(E^+\) and `0` as \(E^-\). No target-wise
configuration or output hierarchy yet exists for this fixture. The stochastic
diamond under `m13_bucket3_binary_diamond` remains pre-pivot provenance only.

## Relation to ABA Learning

**Not yet executed.** Planned learner-visible regime (from
`causal/targetwise/README.md`, not yet instantiated for this fixture):

- binary variables with state order `[0, 1]`;
- internal names `a`, `b`, `c` (display \(A,B,C\));
- exact-value predicates for every non-target column;
- positives = rows with target value `1`; negatives = rows with target value `0`;
- brave learning with `check_ic` enabled in the chosen Prolog configuration.

Implied positive/negative **counts** on the frozen sample under that planned
policy (derived from sample marginals; **not** generated example arrays; **not**
supplied to ABALearn):

| Target | \(E^+\) (value 1) | \(E^-\) (value 0) |
|--------|------------------:|------------------:|
| `a` | 24 | 6 |
| `b` | 21 | 9 |
| `c` | 17 | 13 |

## Relation to Causal ABA

This pre-run stage certifies an observational causal Bayesian network and its
ordinary CI structure. It does not implement or test Russo-style Causal ABA.

## Implementation scope

### Code/config paths

- Authoritative fixture YAML:
  `causal/fixtures/specs/m13_bucket3_binary_collider_and.yaml`
- Fixture toolkit boundary: `causal/fixtures/README.md`
- Target-wise boundary (next stage only): `causal/targetwise/README.md`
- Target-wise configs for this fixture: **none yet**
- Learning outputs for this fixture: **none yet**

### Files changed for this documentation stage

- `docs/experiments/qualitative/M13-C3-binary-collider-and/experiment.md`
- `docs/experiments/qualitative/M13-C3-binary-collider-and/fixture_dossier.tex`
- `docs/experiments/qualitative/M1.3-bucket3-claims.md` (status only)
- `docs/experiments/experiments_summary.md`
- `docs/research/experiment_register.md`
- `docs/research/research_state.md` (first-fixture language)

### Files / artefacts inspected (not modified)

- `causal/fixtures/specs/m13_bucket3_binary_collider_and.yaml`
- `causal/outputs/causal_fixtures/m13_bucket3_binary_collider_and/population.csv`
- `causal/outputs/causal_fixtures/m13_bucket3_binary_collider_and/certificate.json`
- `causal/outputs/causal_fixtures/m13_bucket3_binary_collider_and/mechanism_reference.json`
- `causal/outputs/causal_fixtures/m13_bucket3_binary_collider_and/fixture_manifest.json`
- `causal/outputs/causal_fixtures/m13_bucket3_binary_collider_and/model.bif` (interop only)
- `causal/outputs/causal_fixtures/m13_bucket3_binary_collider_and/samples/n30_seed42.csv`
- `causal/outputs/causal_fixtures/m13_bucket3_binary_collider_and/samples/n30_seed42.manifest.json`
- Preserved pre-pivot diamond paths under
  `causal/fixtures/specs/m13_bucket3_binary_diamond.yaml`,
  `causal/outputs/causal_fixtures/m13_bucket3_binary_diamond/`,
  and `causal/outputs/aba_learning/targetwise/m13_bucket3_binary_diamond/`
  (not reinterpreted as deterministic claim evidence)

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

Planned all-target investigation on the same frozen table:

| Target | True parents | Target type | Evaluator reference status |
|---|---|---|---|
| `a` | \(\emptyset\) | stochastic root | `no_observed_parent_deterministic_rule` |
| `b` | \(\emptyset\) | stochastic root | `no_observed_parent_deterministic_rule` |
| `c` | `{a,b}` | deterministic non-root collider | canonical rule available |

### Positive / negative examples

**Not yet constructed as learner arrays.** Under the planned binary exact-value
policy (target value `1` positive, `0` negative), the frozen sample implies the
counts in the ABA Learning section above.

### Background knowledge

**Not yet generated.** Planned: exact-value predicates for non-target columns
only; graph/certificate/mechanism reference remain evaluator-only.

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

ABALearn / target-wise collection: **not run**.

## Environment

Recorded in `n30_seed42.manifest.json` for the frozen sample:

- Python: `3.10.20`
- NumPy: `2.2.6`
- pandas: `2.3.3`
- Fixture toolkit version: `2`
- Git commit at documentation write: `b534fd5` (working tree may differ after
  this documentation edit)

SWI-Prolog / clingo: not invoked for this pre-run stage.

## Artefact paths

| Artefact | Path | Notes |
|---|---|---|
| Spec (authoritative) | `causal/fixtures/specs/m13_bucket3_binary_collider_and.yaml` | schema v2 |
| Population | `.../population.csv` | exact rationals |
| Certificate | `.../certificate.json` | support, CI, faithfulness, MEC/CPDAG |
| Mechanism reference | `.../mechanism_reference.json` | evaluator-only |
| Fixture manifest | `.../fixture_manifest.json` | hashes + boundaries |
| BIF | `.../model.bif` | derived interop; not authoritative |
| Sample CSV | `.../samples/n30_seed42.csv` | target-free |
| Sample manifest | `.../samples/n30_seed42.manifest.json` | counts + sampler metadata |
| Working LaTeX dossier | `docs/experiments/qualitative/M13-C3-binary-collider-and/fixture_dossier.tex` | mathematical account |
| Target-wise learning outputs | — | **none yet** |

Base directory for generated pre-run artefacts:
`causal/outputs/causal_fixtures/m13_bucket3_binary_collider_and/`.

## Outcome summary

No ABALearn outcomes. Pre-run certification facts verified against primary
artefacts:

| Check | Result |
|---|---|
| Exact population atoms | \(P(1,1,1)=14/25=0.56\); \(P(1,0,0)=6/25=0.24\); \(P(0,1,0)=7/50=0.14\); \(P(0,0,0)=3/50=0.06\) |
| Support | size 4; 4 structural zeros; `full_support: false` |
| Causal sufficiency | `declared_satisfied_by_fixture_design` (`mutually_independent_root_exogenous_noise`); not inferred from the joint |
| Causal Markov condition | `verified` via CPT factorisation over the DAG |
| Ordinary faithfulness | `verified_exactly` by exhaustive singleton-pair CI ↔ d-separation audit; not implied by determinism alone |
| Population independences | only \(A \perp B\); dependence given \(C\); \(A\)–\(C\) and \(B\)–\(C\) dependent |
| Edge activity | both `a→c` and `b→c` active |
| MEC / CPDAG | MEC size 1; ordinary CI CPDAG orients `a→c`, `b→c`; deterministic-relation boundary note recorded |
| Mechanism reference for `c` | `c(A) :- a_val_1(A), b_val_1(A).` (formal = population_supported = sample_observed) |
| Root references | `no_observed_parent_deterministic_rule` for `a` and `b` |
| Frozen sample joint counts | \((1,1,1):17\), \((1,0,0):7\), \((0,1,0):4\), \((0,0,0):2\); all four population atoms observed |
| Deterministic assignment checks | 30/30 verified on the sample |

## Quantitative results

None from ABALearn. Sample marginals and implied planned \(E^\pm\) counts are
recorded above. No body-parent F1, coverage, or solve metrics exist for this
fixture.

## Qualitative learned-rule inspection

Not applicable: learning not run.

Evaluator-only reference for later comparison (`mechanism_reference.json`):

- Target `c`: `c(A) :- a_val_1(A), b_val_1(A).`
- Boundaries recorded in the artefact: syntactic rule equality is not an
  automatic causal-recovery verdict; predictive rules for root targets do not
  constitute root-mechanism recovery; formal / population-supported /
  sample-observed configurations remain distinct.

## Failure modes

No learning failure modes yet. Pre-run distinctions to preserve when learning
begins:

- population properties vs finite-sample observations;
- evaluator-only graph/certificate/reference vs learner-visible BK and \(E^\pm\);
- predictive covering rules vs mechanism-aligned causal interpretation;
- strategy failure vs informational / identifiability limits.

## Interpretation notes

**Verified facts (pre-run).** The fixture is a three-variable observational
collider with independent Bernoulli roots and deterministic AND at the sink.
The exact population has incomplete support because \(C\) is a deterministic
function of \((A,B)\). Ordinary faithfulness holds for this population under the
certificate’s exhaustive singleton-pair audit. The ordinary CI CPDAG recovers
the generating orientations; the certificate explicitly warns that deterministic
functional constraints may change what is identifiable beyond ordinary CI, and
no extended recovery object is asserted.

**Accepted distinctions.** Causal sufficiency is declared by design, not read
off the joint. Active edges are a local mechanism/minimality check, not a
faithfulness proof. The mechanism reference for \(C\) is evaluator-only and must
not be described as an ABALearn input. Root targets have no observed-parent
deterministic rule in the reference.

**No claim.** These pre-run facts do not establish what ABALearn will recover.
No Bucket 3 claim is approved.

## Claims supported

None. Pre-run documentation only.

## Claims not supported / not claimed

- Any statement that ABALearn recovers the AND mechanism, parent set, or CPDAG.
- Any reinterpretation of the preserved stochastic diamond artefacts as
  deterministic Bucket 3 claim evidence.
- Equating syntactic match to `c(A) :- a_val_1(A), b_val_1(A).` with automatic
  recovery success (explicitly disclaimed by the mechanism reference).
- Treating planned/implied \(E^\pm\) counts as already-generated learner inputs.

## Report relevance

Interim Experimentation / Progress (Milestone 1 Part 3 / Bucket 3). Working
evidence and mathematical dossier only; **not** report-facing claim prose.
Do not place this dossier under `docs/report/findings/`.

## Future probes

`future_probes.md` and `future_probes.tex`.
H1–H3: **design approved** / not yet implemented / not tested / **not claims**.
H4: **proposed** / blocked on target-wise cautious support / **not a claim**.
Order: H1 → H2 → H3 → H4 (infra then run).

## Next decision

1. **H1 (approved):** implement/run the nested-prefix AAMAS ablation.
2. **H2 (design approved):** author `m13_bucket3_binary_collider_and_iso_d`,
   lock sample, certify, run AAMAS with H2a/H2b/H2c.
3. **H3 (design approved):** author `m13_bucket3_binary_bd_and_lead_a`;
   build planned `n30_seed42`; run ECAI (primary) and AAMAS (contrast).
4. **H4:** do **not** decide infra/config details now. When H4 is opened,
   resolve the deferred checklist in `future_probes.md` (cautious `.pl` name,
   `configuration.id`, validator, audit semantics, H4a/optional `c`).
5. Keep Bucket 3 free of a claim or expanded run matrix until inspected probe
   evidence warrants a separate decision.

Recorded H1–H3 approvals: `future_probes.md` and `docs/research/decisions.md`.
H4 remains proposed / infra-blocked; open decisions are flagged there only.
