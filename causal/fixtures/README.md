# Exact causal fixtures

This package defines small finite-discrete causal Bayesian networks before any
ABA Learning target is selected. It does not implement Russo-style Causal ABA,
decode learned rules into a graph, or run ABA Learning.

## Scientific source and derived artefacts

- `specs/*.yaml` is the authoritative fixture definition. Probabilities are
  exact integers or rational strings; YAML floats are rejected.
- `population.csv` is the exact joint distribution derived by Bayesian-network
  factorisation.
- `certificate.json` records graph structure, edge activity, exact joint
  support (including structural zeros), an exhaustive singleton
  conditional-independence audit, ordinary faithfulness, the MEC, and the
  standard CPDAG.
- `mechanism_reference.json` is evaluator-only ground truth. For supported
  binary deterministic fixtures it records root distributions, complete
  non-root truth tables, formal/population-supported/sample-observed parent
  configurations, and canonical unsimplified rules for target value `1`.
- `model.bif` is a derived pgmpy/BIF interoperability file. BIF probabilities
  are floats and BIF does not preserve causal-sufficiency or sampling metadata,
  so it is never the authoritative source.
- `samples/*.csv` contains one target-free IID table. Re-selecting a target must
  not resample the table.

For future target-wise fixtures, use safe lowercase learner identifiers such as
`a`, `b`, `c`, `d`, ... as the YAML variable names and CSV columns. Mathematical
descriptions may display these as (A,B,C,D,\ldots). Uppercase identifiers are
not passed directly to Prolog because Prolog reserves an initial uppercase
letter for logical variables. Existing `x0`, `x1`, ... fixtures remain valid and
unchanged.

Three hashes keep provenance distinctions explicit: the exact UTF-8 source-file
bytes, the canonical parsed YAML document, and the normalized scientific model.
Certificate, BIF, and sampler manifests also identify their implementation and
tool versions.

Two explicitly named source regimes are supported:

- schema version 1, `positive_stochastic`: every local conditional probability
  is strictly between zero and one;
- schema version 2, `root_stochastic_deterministic_nonroots`: roots have
  non-degenerate full-support distributions and every non-root conditional row
  is a point mass.

Schema version 2 represents randomness only in the roots and deterministic
propagation below them. It does not make faithfulness automatic. Every fixture
still receives an exact fixture-specific support, conditional-independence, MEC,
and ordinary-faithfulness audit. The standard CPDAG is recorded as a reference
for ordinary conditional-independence recovery; deterministic relations may
require a different equivalence-class analysis for stronger recovery claims.

## Reproducible sampling

Sampling uses a repository-owned row-major ancestral inverse-CDF algorithm and
NumPy `PCG64`. For schema version 2, random draws are made for stochastic roots
only; deterministic non-roots are evaluated exactly from their parent values.
For a fixed fixture and seed, requesting a larger `n` reproduces the smaller
table as an exact prefix. CSV row number is the example identifier; every CSV
column is a causal variable.

## CLI

Run from the repository root in the canonical `aba-asp` environment:

```bash
python -m causal.fixtures.cli validate \
  --fixture causal/fixtures/specs/<fixture-id>.yaml

python -m causal.fixtures.cli build \
  --fixture causal/fixtures/specs/<fixture-id>.yaml \
  --output-dir causal/outputs/causal_fixtures/<fixture-id> \
  --n <n> --seed 42
```

The `build` command derives and checks the population certificate, exports and
round-trips BIF, and samples the one approved baseline table. These are fixture
artefacts, not ABA Learning experiment cells or evidence-backed claims.

The existing `m13_bucket3_binary_diamond` source and generated files use the
earlier positive-stochastic regime. They are preserved as pre-pivot exploratory
and infrastructure artefacts and must not be rebuilt, edited, or reinterpreted
as evidence for the deterministic-mechanism investigation.

Generated files are frozen by default. Repeating an identical build is
idempotent; attempting to write different bytes to an existing artefact raises
an error instead of silently replacing the table or certificate. Use a new,
empty output directory when deliberately changing a fixture or sample request.
