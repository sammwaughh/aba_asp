# Claims Ledger

## Purpose

This file records which report claims are supported by which project evidence.

It exists to prevent overclaiming and to make report writing auditable. It should be updated whenever an experiment is analysed, a figure/table is selected for the report, or a substantive interpretation is proposed.

Cursor may update factual evidence fields. Samuel must review any claim before it is used in submitted report prose.

## Claim strength categories

Use one of the following labels.

| Strength | Meaning | Report use |
|---|---|---|
| `safe` | Directly supported by project files, code, or observed experiment output. | Can be used in report, with citation/evidence. |
| `bounded` | Supported under explicit conditions or for a limited setting. | Can be used with caveats. |
| `tentative` | Plausible interpretation, but evidence is incomplete. | Use cautiously or reserve for future work. |
| `unsupported` | Not established by current evidence. | Do not claim. |
| `false_or_misleading` | Contradicted by project evidence or likely to misrepresent the system. | Must not claim. |

## Evidence types

| Evidence type | Description |
|---|---|
| `repo_doc` | Project documentation or experiment record. |
| `code` | Direct code inspection. |
| `command_output` | Exact command output, log, or result file. |
| `metric` | Computed metric from `metrics.json`, `metrics.parquet`, or `results.parquet`. |
| `learned_rule` | Specific rule from a learned `.sol.aba` or parsed delta. |
| `paper` | Published paper used for theoretical support. |
| `supervisor_guidance` | Advice from Fabrizio, recorded as meeting guidance. |
| `interpretation` | Human interpretation of evidence; must be marked as such. |

## Global caution

The current `aba_asp/causal` bridge should be described as an ABA Learning-based parent-set or learned-rule recovery pipeline unless direct implementation evidence shows that it implements full Russo-style Causal ABA.

Do not claim full Causal ABA unless the implementation uses, at minimum:

- arrow/no-edge assumptions such as `arr_xy` and `noe_xy`;
- independence assumptions such as `indep(x,y,Z)`;
- d-separation reasoning;
- stable-extension-as-DAG machinery.

## Claim table

| Claim ID | Claim | Strength | Evidence | Caveats | Report location | Status |
|---|---|---|---|---|---|---|
| C-001 | The project distinguishes ABA foundations, ABA Learning, Causal ABA, and the current `aba_asp/causal` bridge. | safe | `research_state.md`; `chatgpt_project_brief.md`; `repo_map.md` | Must be preserved in all writing. | Background / Experimentation / Project Plan | active |
| C-002 | The current implementation uses an inherited ABA Learning engine with a Python causal bridge over tabular data. | safe | `repo_map.md`; `execution_guide.md`; code inspection records | Does not imply full Causal ABA. | Experimentation / Progress | active |
| C-003 | The current bridge evaluates whether learned target-rule bodies recover known parent sets in generated data. | safe | `METRICS.md` summary; `metrics.py`; experiment records | Parent-set recovery is not full causal discovery. | Experimentation / Progress | active |
| C-004 | The infrastructure supports YAML-configured experiment grids with per-cell artefacts and summary metrics. | safe | `INFRA.md` summary; `run_grid.py`; output artefacts once produced | Must cite exact config/output when used. | Experimentation / Progress | active |
| C-005 | On simple motifs, ABA Learning can recover true causal parents. | unsupported | Requires QL-001/QN-001 results | Do not claim until experiments support it. | TBD | blocked |
| C-006 | Greedy ABA Learning is better than non-deterministic ABA Learning for learning causal rules. | tentative | Supervisor guidance says this was observed informally; requires experiment | May become bounded after QN-001. | TBD | blocked |
| C-007 | Noise in generated data is represented by ABA Learning as exceptions. | tentative | Theoretical expectation only at present | Requires learned assumptions/contraries or rule inspection. | TBD | blocked |
| C-008 | The current implementation performs Russo-style Causal ABA. | false_or_misleading | `research_state.md`; `repo_map.md` | Must not claim unless implementation changes substantially. | None | forbidden |
| C-009 | The current implementation recovers full causal DAGs. | unsupported | Current metrics are target-rule/body-level, not full DAG-level | Reserved skeleton/direction metrics are not computed. | None | forbidden |
| C-010 | Initial experiments are feasibility probes rather than final evaluation. | safe | Interim report context; experiment plan | Should be explicit in interim report. | Experimentation / Project Plan | active |

## Experiment-specific claims

Add claims after each experiment is analysed.

### QL-001

| Claim ID | Claim | Strength | Evidence | Caveats | Report location | Status |
|---|---|---|---|---|---|---|
| QL-001-C-001 | TBD | TBD | `docs/experiments/QL-001.md` | TBD | TBD | pending |

### QN-001

| Claim ID | Claim | Strength | Evidence | Caveats | Report location | Status |
|---|---|---|---|---|---|---|
| QN-001-C-001 | TBD | TBD | `docs/experiments/QN-001.md` | TBD | TBD | pending |

## Claims not to make

These claims should not appear in report prose unless later evidence explicitly changes their status.

- The current bridge is a full implementation of Causal ABA.
- The current experiments prove causal discovery.
- A learned predictive rule is necessarily a causal rule.
- Parent-set F1 is a complete measure of causal graph recovery.
- Reserved skeleton/direction metrics have been computed.
- Noise is definitely represented as exceptions without inspecting learned assumptions, contraries, and rules.
- Greedy is better than non-deterministic ABA Learning without a controlled comparison.

## Procedure for adding a claim

1. Write the claim in one sentence.
2. Identify exact evidence.
3. Assign a strength category.
4. Add caveats.
5. Mark where it may appear in the report.
6. Samuel reviews before the claim is used in submitted text.

## Review checklist before report drafting

- [ ] Every substantive claim has a Claim ID.
- [ ] Every Claim ID has evidence.
- [ ] Every causal claim has a caveat if based only on parent-set recovery.
- [ ] Unsupported and forbidden claims are excluded.
- [ ] The distinction between ABA Learning and Causal ABA is explicit.
- [ ] Claims based on supervisor guidance are not presented as experimental results.