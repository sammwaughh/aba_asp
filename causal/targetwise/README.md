# Target-complete ABA Learning over causal fixtures

This package reads one generated directory under
`causal/outputs/causal_fixtures/`, selects one frozen sample explicitly, and
runs ABA Learning once for every variable as target. It does not resample when
the target changes and does not expose graph metadata to the learner.

The initial supported learner-visible regime is:

- finite binary variables with declared state order `[0, 1]`;
- variables named `x0`, `x1`, ... under the initial predicate and rule-body
  inspection contract;
- exact-value predicates for every non-target observation;
- target value `1` as `E+` and target value `0` as `E-`;
- a Prolog configuration that explicitly selects brave learning;
- a Prolog configuration that explicitly enables `set_lopt(check_ic)`, so the
  learner emits its checked final ASP artefact;
- one serial target cell per variable.

Non-binary target policies and learned-rule-to-graph decoding are outside this
initial implementation.

## Configuration

Target-wise YAML files require an explicit `configuration.id`. This stable,
safe path component identifies the non-sample execution contract. The selected
sample path is relative to the fixture directory, and targets are always
discovered from validated fixture/sample metadata.

The current bounded files mirror the generated hierarchy:

```text
causal/configs/targetwise/
└── m13_bucket3_binary_diamond/
    ├── aamas2025/
    │   └── n50_seed42.yaml
    └── ecai2024/
        └── n50_seed42.yaml
```

YAML filenames and parent directories are organisational. Output identity is
derived from the validated fixture ID, explicit `configuration.id`, and
selected CSV stem.

`learner.joint_check_timeout_s` bounds the final `.sol_chk.asp` artefact audit.
The established key is retained so existing configurations and their hashes
remain stable; it does not denote an additional coverage metric.

## Commands

Run from the repository root in the canonical `aba-asp` environment:

```bash
python -m causal.targetwise.cli validate \
  --config causal/configs/targetwise/m13_bucket3_binary_diamond/aamas2025/n50_seed42.yaml

python -m causal.targetwise.cli prepare \
  --config causal/configs/targetwise/m13_bucket3_binary_diamond/aamas2025/n50_seed42.yaml

python -m causal.targetwise.cli run \
  --config causal/configs/targetwise/m13_bucket3_binary_diamond/aamas2025/n50_seed42.yaml

python -m causal.targetwise.cli run \
  --config causal/configs/targetwise/m13_bucket3_binary_diamond/ecai2024/n50_seed42.yaml
```

`prepare` writes all target inputs without invoking ABA Learning. `run` reuses
those byte-identical inputs, executes targets serially, and writes per-target
reports plus a collection summary.

Within each target cell, `data.csv` is a frozen inspection/provenance copy. The
ABA engine is given `bk.aba` and the positive/negative example arrays recorded
in `examples.json`; it does not read `data.csv` or `task_manifest.json`.
Generating edges and target parents appear only in evaluator fields of the task
manifest. They are not used by the target-wise diagnostics or reports.

## Retained diagnostics

Each completed target cell records:

- learner outcome, failure reason, and ABA Learning runtime;
- the complete learned delta, target rules, and their counts;
- assumptions and contraries, including their counts;
- target-rule body literals, base variables, and lengths;
- basic solution/parser integrity;
- one final-artefact integrity audit and its runtime.

With `check_ic` enabled, the inherited learner emits `.sol_chk.asp`: the final
framework's ASP serialization together with integrity constraints requiring
one stable model to contain every `E+` atom and no `E-` atom. The target-wise
post-run layer invokes Clingo directly on that saved file. It does not rebuild
the constraints around `.sol.asp`.

`SAT` confirms that the final saved checked artefact has a witnessing stable
model. Because the learner already applies the corresponding condition during
learning, this invocation is retained only as a serialization and
artefact-integrity audit. It is not counted as an additional coverage or
learner-performance metric, and it is not a set of independent per-example
checks. Other possible audit statuses are `UNSAT`, `TIMEOUT`, `ERROR`, and
`UNAVAILABLE`.

The target-wise path does not calculate Python-Horn coverage, Prolog query
coverage, independent per-example ASP coverage, parent-set metrics, or
graph/CPDAG metrics. Those inherited panels remain unchanged for locked earlier
experiment infrastructure.

## Output hierarchy

```text
causal/outputs/aba_learning/targetwise/
└── <fixture-id>/
    └── <configuration-id>/
        ├── configuration_manifest.json
        └── <sample-stem>/
            ├── manifest.json
            ├── run.log
            ├── results.parquet
            ├── summary.md
            ├── summary.json
            └── cells/
                └── target-<variable>/
                    ├── input/
                    │   ├── data.csv
                    │   ├── bk.aba
                    │   ├── examples.json
                    │   └── task_manifest.json
                    ├── output/
                    │   ├── targetwise_<run-id>.aba
                    │   ├── targetwise_<run-id>.sol.aba
                    │   ├── targetwise_<run-id>.sol.asp  (when emitted)
                    │   ├── targetwise_<run-id>.sol_chk.asp
                    │   ├── prolog.stdout
                    │   ├── prolog.stderr
                    │   └── engine artefacts
                    ├── metrics.json
                    ├── metrics.parquet
                    └── report.md
```

`metrics.json` retains rule and ABA-component lists for direct inspection.
`metrics.parquet` and root `results.parquet` contain the same approved
diagnostic family in aggregation-safe scalar/JSON-string columns.

`configuration_manifest.json` pins the encoding, Prolog configuration bytes,
learning mode, and timeouts shared by every sample below that configuration
directory. A conflicting execution contract is rejected rather than silently
mixing evidence. Each fixture/configuration/sample directory is independently
immutable and completed collections are idempotent: re-running the same command
does not invoke the learner again.
