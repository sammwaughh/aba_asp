# Exact causal fixtures

This package defines small finite-discrete causal Bayesian networks before any
ABA Learning target is selected. It does not implement Russo-style Causal ABA,
decode learned rules into a graph, or run ABA Learning.

## Scientific source and derived artefacts

- `specs/*.yaml` is the authoritative fixture definition. Probabilities are
  exact integers or rational strings; YAML floats are rejected.
- `population.csv` is the exact joint distribution derived by Bayesian-network
  factorisation.
- `certificate.json` records graph structure, edge activity, an exhaustive
  singleton conditional-independence audit, ordinary faithfulness, the MEC,
  and the CPDAG.
- `model.bif` is a derived pgmpy/BIF interoperability file. BIF probabilities
  are floats and BIF does not preserve causal-sufficiency or sampling metadata,
  so it is never the authoritative source.
- `samples/*.csv` contains one target-free IID table. Re-selecting a target must
  not resample the table.

Three hashes keep provenance distinctions explicit: the exact UTF-8 source-file
bytes, the canonical parsed YAML document, and the normalized scientific model.
Certificate, BIF, and sampler manifests also identify their implementation and
tool versions.

The current model class requires strictly positive local probabilities. A
deterministic-mechanism regime would require a separate model and certificate.

## Reproducible sampling

Sampling uses a repository-owned row-major ancestral inverse-CDF algorithm and
NumPy `PCG64`. For a fixed fixture and seed, requesting a larger `n` reproduces
the smaller table as an exact prefix. CSV row number is the example identifier;
every CSV column is a causal variable.

## CLI

Run from the repository root in the canonical `aba-asp` environment:

```bash
python -m causal.fixtures.cli validate \
  --fixture causal/fixtures/specs/m13_bucket3_binary_diamond.yaml

python -m causal.fixtures.cli build \
  --fixture causal/fixtures/specs/m13_bucket3_binary_diamond.yaml \
  --output-dir causal/outputs/causal_fixtures/m13_bucket3_binary_diamond \
  --n 50 --seed 42
```

The `build` command derives and checks the population certificate, exports and
round-trips BIF, and samples the one approved baseline table. These are fixture
artefacts, not ABA Learning experiment cells or evidence-backed claims.

Generated files are frozen by default. Repeating an identical build is
idempotent; attempting to write different bytes to an existing artefact raises
an error instead of silently replacing the table or certificate. Use a new,
empty output directory when deliberately changing a fixture or sample request.
