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

### TAB-002 — QN-001 strategy comparison

- Type: `table`
- Status: `candidate`
- Source experiment: `QN-001`
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
Experimentation / Progress or Project Plan
```

- Intended message:

```text
Compare greedy and non-deterministic ABA Learning strategies on minimal causal motifs, if the comparison is implemented and run.
```

- Draft structure:

| Motif / target group | Strategy | Solve fraction | Median body-parent F1 | Offgraph rate | Timeout rate | Efficiency metric |
|---|---|---:|---:|---:|---:|---:|
| TBD | greedy | TBD | TBD | TBD | TBD | TBD |
| TBD | non-deterministic | TBD | TBD | TBD | TBD | TBD |

- Caption draft:

```text
TBD
```

- Caveats:

```text
This table should only be used if the strategy settings are confirmed comparable.
```

- Claims supported:

```text
TBD
```

- Claims not supported:

```text
The table does not establish general superiority of one strategy for causal discovery unless the evidence is broad enough and explicitly caveated.
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