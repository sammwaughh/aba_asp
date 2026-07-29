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
- one serial target cell per variable.

Non-binary target policies and learned-rule-to-graph decoding are outside this
initial implementation.

## Configuration

The current bounded configuration is
`causal/configs/targetwise/M13_b3_binary_diamond_n50_seed42_aamas2025.yaml`.
The selected sample path is relative to the fixture directory. Targets are
always discovered from the validated fixture/sample metadata.

## Commands

Run from the repository root in the canonical `aba-asp` environment:

```bash
python -m causal.targetwise.cli validate \
  --config causal/configs/targetwise/M13_b3_binary_diamond_n50_seed42_aamas2025.yaml

python -m causal.targetwise.cli prepare \
  --config causal/configs/targetwise/M13_b3_binary_diamond_n50_seed42_aamas2025.yaml

python -m causal.targetwise.cli run \
  --config causal/configs/targetwise/M13_b3_binary_diamond_n50_seed42_aamas2025.yaml
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
- one joint brave-task check and its runtime.

The joint check invokes Clingo once on the final `.sol.asp`, with all positive
and negative constraints present simultaneously. `SAT` means that at least one
stable model contains every `E+` atom and no `E-` atom. It is not a set of
independent per-example brave-entailment checks. Other possible statuses are
`UNSAT`, `TIMEOUT`, `ERROR`, and `UNAVAILABLE`.

The target-wise path does not calculate Python-Horn coverage, Prolog query
coverage, independent per-example ASP coverage, parent-set metrics, or
graph/CPDAG metrics. Those inherited panels remain unchanged for locked earlier
experiment infrastructure.

## Output hierarchy

```text
causal/outputs/aba_learning/targetwise/
└── <fixture-id>/
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

One fixture/sample output directory represents one canonical learner
configuration. A different configuration is rejected rather than silently
overwriting or mixing the evidence. Completed collections are idempotent:
re-running the same command does not invoke the learner again.
