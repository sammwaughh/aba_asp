# Target-complete ABA Learning over causal fixtures

This package reads one generated directory under
`causal/outputs/causal_fixtures/`, selects one frozen sample explicitly, and
runs ABA Learning once for every variable as target. It does not resample when
the target changes and does not expose graph metadata to the learner.

The initial supported learner-visible regime is:

- finite binary variables with declared state order `[0, 1]`;
- safe lowercase Prolog-atom variable names. Future fixtures use `a`, `b`, `c`,
  `d`, ...; the existing `x0`, `x1`, ... convention remains supported;
- exact-value predicates for every non-target observation;
- target value `1` as `E+` and target value `0` as `E-`;
- a Prolog configuration that explicitly selects either brave or cautious
  learning;
- a Prolog configuration that explicitly enables `set_lopt(check_ic)`, so the
  learner emits its checked final ASP artefact;
- one serial target cell per variable.

Non-binary target policies and learned-rule-to-graph decoding are outside this
initial implementation.

Learner-visible names must begin with a lowercase letter and then contain only
lowercase letters, digits, or underscores. `assumption`, `contrary`, `not`,
`alpha`, `alpha_*`, `c_alpha`, and `c_alpha_*` are reserved for ABA or
learner-generated symbols. A
mathematical node (C) is therefore written internally as `c`. In a learned
rule such as `c(A)`, lowercase `c` is the causal-variable predicate and uppercase
`A` is the Prolog variable ranging over table-row identifiers. The learner's
generated `alpha_1(A)` and `c_alpha_1(A)` predicates are distinct from `c(A)`.
This convention is enforced entirely by the Python bridge; no inherited `.pl`
file is changed.

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

### Learning modes

The selected learning mode is derived from the consulted Prolog configuration,
not duplicated as a YAML field. The validator accepts only an explicit
`learning_mode(brave)` or `learning_mode(cautious)` declaration. Manifests,
configuration hashes, reports, and output paths retain the resulting mode and
configuration identity.

`configs/baseline_cautious_config.pl` pins the learning-relevant defaults of
`aba_asp.pl`: non-deterministic folding, ten folding steps, `any` selection,
the full folding space, `relto` assumption introduction, post-folding
entailment checking, and cautious learning. It also enables `check_ic` solely
to retain the checked ASP artefact. This is the repository's cautious
ASP-ABAlearn baseline; it is not described as an ECAI configuration because
the ECAI 2024 configuration implements the published brave method.

H6 folding-budget ablations reuse that baseline except for `folding_steps`:
`baseline_cautious_steps1`, `baseline_cautious_steps2`, and
`baseline_cautious_steps5` (`configs/baseline_cautious_steps{1,2,5}_config.pl`).
The existing `baseline_cautious` identity remains the steps-10 reference and
must not be overwritten. These are not ECAI or AAMAS configurations.

Published `ecai2024` and `aamas2025` configurations and their existing outputs
remain unchanged. Experimental H5 uses a separate configuration identity
`greedy_cautious` (`configs/greedy_cautious_config.pl`): the Greedy / `mgr` /
`folding_space(bk)` / `relto` bundle from AAMAS with `learning_mode(cautious)`.
It is **not** a published AAMAS configuration and must not be named
`aamas_cautious`. It is distinct from repository-baseline `baseline_cautious`
(nd / any / all).

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

python -m causal.targetwise.cli validate \
  --config causal/configs/targetwise/m13_bucket3_binary_collider_and/baseline_cautious/n30_seed42.yaml
```

When the H4 scientific run is explicitly started, the corresponding all-target
command is:

```bash
python -m causal.targetwise.cli run \
  --config causal/configs/targetwise/m13_bucket3_binary_collider_and/baseline_cautious/n30_seed42.yaml
```

`prepare` writes all target inputs without invoking ABA Learning. `run` reuses
those byte-identical inputs, executes targets serially, and writes per-target
reports plus a collection summary.

Within each target cell, `data.csv` is a frozen inspection/provenance copy. The
ABA engine is given `bk.aba` and the positive/negative example arrays recorded
in `examples.json`; it does not read `data.csv` or `task_manifest.json`.
Generating edges and target parents appear only in evaluator fields of the task
manifest. They are not used by the target-wise diagnostics or reports.
The fixture-level `mechanism_reference.json` is likewise evaluator-only and is
never passed to ABA Learning. Its bytes are transitively pinned by the fixture
manifest hash used by the collection, so later inspection can identify the
exact reference without leaking it into learner-visible inputs.

The engine is invoked with a unique temporary BK stem so concurrently visible
engine artefacts can be attributed to the correct target. That identifier is an
execution detail only. After collection, the solution files are exposed under
the stable names `bk.sol.aba`, `bk.sol.asp`, and `bk.sol_chk.asp` inside the
target's own output directory.

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
model. Under brave learning this is the joint `E+`/`E-` witness condition used
by the learner, so the repeated invocation is retained only as a serialization
and artefact-integrity audit. Under cautious learning it is not a cautious-
consequence check: cautious acceptance instead requires every positive to hold
in every stable model and every negative not to be a cautious consequence. The
audit status therefore never determines the cautious learner outcome. It is
not counted as an additional coverage or learner-performance metric, and it is
not a set of independent per-example checks. Other possible audit statuses are
`UNSAT`, `TIMEOUT`, `ERROR`, and `UNAVAILABLE`.

The target-wise path does not calculate Python-Horn coverage, Prolog query
coverage, independent per-example ASP coverage, parent-set metrics, or
graph/CPDAG metrics. Those inherited panels remain unchanged for locked earlier
experiment infrastructure.

Body-variable diagnostics are matched against the fixture's declared variables.
They do not rely on the legacy `xN` parser and do not classify generated
`alpha_N` or `c_alpha_N` predicates as causal variables.

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
                    │   ├── bk.sol.aba
                    │   ├── bk.sol.asp
                    │   ├── bk.sol_chk.asp
                    │   ├── delta.aba
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

`delta.aba` contains exactly the ordered learned delta recorded in
`metrics.json["delta_rules"]`: solution lines absent from the frozen input BK,
after removing generated per-row indicator clauses. It therefore includes any
learned rules, assumptions, and contraries, but no original BK clauses.

`configuration_manifest.json` pins the encoding, Prolog configuration bytes,
learning mode, and timeouts shared by every sample below that configuration
directory. A conflicting execution contract is rejected rather than silently
mixing evidence. Each fixture/configuration/sample directory is independently
immutable and completed collections are idempotent: re-running the same command
does not invoke the learner again.
