# Figure and Table Index

## Purpose

This file tracks figures and tables used or considered for the interim and final reports.

It records where each figure/table came from, how it was generated, what artefact supports it, and whether it has been used in report prose.

This is a report hygiene file. It should prevent figures and tables from becoming detached from their source commands and experiment records.

## Figure/table status categories

| Status | Meaning |
|---|---|
| `candidate` | May be useful, but not yet selected. |
| `selected` | Intended for report inclusion. |
| `drafted` | Caption/prose drafted. |
| `used` | Included in report source. |
| `rejected` | Not used. |
| `superseded` | Replaced by a newer figure/table. |

## Index

| ID | Type | Title / description | Status | Source experiment | Source command | Source artefact | Report section | Caption/prose status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| FIG-001 | figure | TBD | candidate | TBD | TBD | TBD | TBD | TBD | Placeholder. |
| TAB-001 | table | TBD | candidate | TBD | TBD | TBD | TBD | TBD | Placeholder. |

## Candidate figures

### FIG-001 — TBD

- Type: `figure`
- Status: `candidate`
- Source experiment: `TBD`
- Source command:

```bash
TBD
```

- Source artefact path:

```text
TBD
```

- Intended report section: `TBD`
- Intended message:

```text
TBD
```

- Caption draft:

```text
TBD
```

- Caveats:

```text
TBD
```

- Claims supported:

```text
TBD
```

- Claims not supported:

```text
TBD
```

### FIG-002 — TBD

- Type: `figure`
- Status: `candidate`
- Source experiment: `TBD`
- Source command:

```bash
TBD
```

- Source artefact path:

```text
TBD
```

- Intended report section: `TBD`
- Intended message:

```text
TBD
```

- Caption draft:

```text
TBD
```

- Caveats:

```text
TBD
```

- Claims supported:

```text
TBD
```

- Claims not supported:

```text
TBD
```

## Candidate tables

### TAB-001 — QL-001 qualitative learned-rule examples

- Type: `table`
- Status: `candidate`
- Source experiment: `QL-001`
- Source command:

```bash
TBD
```

- Source artefact path:

```text
TBD
```

- Intended report section:

```text
Experimentation / Progress
```

- Intended message:

```text
Show selected examples of learned target rules on minimal causal motifs, comparing true parents with learned body variables.
```

- Draft structure:

| Motif | Target | True parents | Learned body variables | Classification | Notes |
|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD |

- Caption draft:

```text
TBD
```

- Caveats:

```text
This table concerns target-wise learned-rule/body recovery, not full causal graph recovery or full Causal ABA.
```

- Claims supported:

```text
TBD
```

- Claims not supported:

```text
The table does not by itself establish causal discovery or full DAG recovery.
```

### TAB-002 — M1.1 cell-level results (candidate)

- Type: `table`
- Status: `candidate`
- Source experiment: `M11` (m1.1)
- Source command:

```bash
python -m causal.experiments.run_grid --config causal/configs/experiments/M11_parent_position.yaml --no-resume
```

- Source artefact path:

```text
docs/experiments/qualitative/M1.1-parent-position.md (cell-level table)
docs/report/findings/milestone1_part1_m11_findings.tex
causal/outputs/aba_learning/grid/M11_parent_position/cells/<dgp>/
```

- Intended report section:

```text
Experimentation / Progress (Milestone 1)
```

- Intended message:

```text
Eight-cell metamorphic grid: expected vs actual rules; binary σ/π hold; cat3 σ fails under nd.
```

- Draft structure:

| Encoding | Cell | Expected rule | Classification | σ/π note |
|---|---|---|---|---|
| (from M1.1 record) | | | | |

- Caption draft:

```text
M1.1 parent-position control under fixed nd folding (M11). Parent-set / learned-rule proxy, not causal discovery.
```

- Caveats:

```text
Square verdicts on cat3 A/D use sol files and prolog traces where cov_py and cov_pl disagree on assumption rules.
```

- Claims supported:

```text
M11-C-001, M11-C-002 (bounded)
```

- Claims not supported:

```text
Greedy fixes cat3 σ failure (M11-C-004 tentative until M1.2)
```

## Caption rules

Captions should state:

- what is shown;
- what experiment produced it;
- what the metric or example means;
- the main limitation.

Captions should not overclaim.

Avoid:

- “causal discovery performance” unless the experiment really evaluates causal discovery;
- “DAG recovery” unless graph-level metrics are computed;
- “Causal ABA result” unless full Causal ABA machinery is used.

Prefer:

- “parent-set recovery”;
- “learned-rule body recovery”;
- “target-wise rule learning”;
- “minimal motif diagnostic”.

## Figure/table review checklist

Before a figure/table enters the report:

- [ ] Source experiment record exists.
- [ ] Source command is recorded.
- [ ] Source artefact path exists.
- [ ] Caption is drafted.
- [ ] Caption is caveated.
- [ ] Claims supported are listed.
- [ ] Claims not supported are listed.
- [ ] Claims are checked against `docs/report/claims_ledger.md`.
- [ ] Samuel has reviewed the figure/table.