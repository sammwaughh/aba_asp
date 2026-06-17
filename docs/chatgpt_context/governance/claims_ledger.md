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
| C-005 | On some simple motifs and encodings, the current target-wise ABA Learning bridge recovers the true direct parents of x2 in learned rule bodies. | bounded | `docs/report/manuscript/experimentation.md`; QI-001/QI-002/QI-004 records; `command_output`/`metric` in `causal/outputs/aba_learning/grid/` | Holds only in selected idealised cases (e.g. binary chain/fork, some colliders). Recovery is not robust across motifs, encodings or modest noisy scaling; it is target-wise parent-set recovery, not causal discovery. | Experimentation / Progress | active |
| C-006 | On these controlled tasks, greedy folding is faster than and at least as good as non-deterministic folding at parent-set recovery. | bounded | `docs/experiments/qualitative/greedy_vs_nd_qualitative_handoff.md` (QI-001/QI-002/QI-004 greedy reruns) | Faster (~120x at the QL3 scale), solve rate >= nd, net better clean recovery (colliders), with one cell regression (cat3 fork) and no recovery change at noisy n=20. Single seed/machine; not causal discovery; quantitative confirmation needs QN-001. | Experimentation / Progress | active |
| C-007 | Noise in generated data is represented by ABA Learning as exceptions. | tentative | Theoretical expectation; weak indicative evidence in the one solved QL3 cell (learned rule `x2(A) <- alpha_1(A), x0(A)` alongside `x2(A) <- x1(A)`) | Requires systematic inspection of learned assumptions/contraries across cells; a single cell is not sufficient. | TBD | blocked |
| C-008 | The current implementation performs Russo-style Causal ABA. | false_or_misleading | `research_state.md`; `repo_map.md` | Must not claim unless implementation changes substantially. | None | forbidden |
| C-009 | The current implementation recovers full causal DAGs. | unsupported | Current metrics are target-rule/body-level, not full DAG-level | Reserved skeleton/direction metrics are not computed. | None | forbidden |
| C-010 | Initial experiments are feasibility probes rather than final evaluation. | safe | Interim report context; experiment plan | Should be explicit in interim report. | Experimentation / Project Plan | active |

## Experiment-specific claims

Add claims after each experiment is analysed. Report labels: QL1 = QI-001, QL2 = QI-002, QL3 = QI-004. (The earlier n=100 scaled attempt was cut; only the n=20 study is canonical and is QL3.)

### QL1 (QI-001)

| Claim ID | Claim | Strength | Evidence | Caveats | Report location | Status |
|---|---|---|---|---|---|---|
| QL1-C-001 | All 9 cells (3 motifs x 3 modes) solved on tiny 4–5 row handcrafted tables. | safe | `docs/experiments/qualitative/QI-001.md`; grid outputs | Tiny tables; "solved" does not imply correct parent recovery. | Experimentation / Progress | active |
| QL1-C-002 | The fork motif was recovered exactly in all three encodings. | bounded | QI-001 record; `docs/report/manuscript/experimentation.md` | The fork's true parent is x0, so exact recovery is confounded with a first-column/x0 preference. | Experimentation / Progress | active |
| QL1-C-003 | In categorical/continuous chain cells the learner recovered the ancestor x0 rather than the direct parent x1. | safe | QI-001 record | An ancestor/proxy, not direct-parent recovery. | Experimentation / Progress | active |

### QL2 (QI-002)

| Claim ID | Claim | Strength | Evidence | Caveats | Report location | Status |
|---|---|---|---|---|---|---|
| QL2-C-001 | Under complete noiseless truth tables the binary chain and binary fork recovered the true parent exactly (`x2(A) <- x1(A)`, `x2(A) <- x0(A)`). | safe | QI-002 record; learned `.sol.aba`; `docs/report/manuscript/experimentation.md` | Best-case logical baseline; binary chain provides evidence against a pure always-prefer-x0 explanation. | Experimentation / Progress | active |
| QL2-C-002 | The binary collider returned no solution although the conjunctive parent rule `x2(A) <- x0(A), x1(A)` covers the truth table. | safe | QI-002 record; data.csv; prolog.stdout | A failure of the configured nd learner/representation, not proof that no parent-aligned rule exists. | Experimentation / Progress | active |
| QL2-C-003 | Ideal noiseless data is not sufficient for robust parent-set recovery (mean variable-level F1 ~ 0.61 over 6 cells). | bounded | QI-002 record/metrics | cat3 chain recovered non-parent x0; cat3 collider recovered only one of two parents. | Experimentation / Progress | active |

### QL3 (QI-004, n=20)

| Claim ID | Claim | Strength | Evidence | Caveats | Report location | Status |
|---|---|---|---|---|---|---|
| QL3-C-001 | The scaled noisy setting is computationally feasible at n=20: all 15 cells terminated without timeout. | safe | `docs/experiments/qualitative/QI-004.md`; run_log | Feasibility only; not a recovery claim. | Experimentation / Progress | active |
| QL3-C-002 | No QL3 cell achieved exact parent-set recovery; 1 solved (binary chain x1-parent, superset {x0,x1}, F1 0.67), 12 no-solution, 2 binary errors. | safe | QI-004 record/metrics | Noise hyper-parameters were chosen arbitrarily; a systematic noise sweep is required before drawing stronger conclusions. | Experimentation / Progress | active |
| QL3-C-003 | The 2 binary `unknown constant` errors are a BK-encoding limitation independent of folding mode. | bounded | QI-004 record; greedy-vs-nd handoff (errors persist under greedy) | Root cause not yet fixed. | Experimentation / Progress | active |

### Greedy vs non-deterministic folding (QI-001/QI-002/QI-004 greedy)

| Claim ID | Claim | Strength | Evidence | Caveats | Report location | Status |
|---|---|---|---|---|---|---|
| GVN-C-001 | Greedy folding is substantially faster than nd on these tasks (QL3 total wall ≈1233 s -> ≈10 s). | bounded | `docs/experiments/qualitative/greedy_vs_nd_qualitative_handoff.md` | Wall-clock, single run, one machine; not a controlled benchmark (QN-001). | Experimentation / Progress | active |
| GVN-C-002 | Greedy can solve a cell where nd reports no solution (QI-002 binary collider: nd no-solution -> greedy solved+exact). | bounded | greedy-vs-nd handoff | Single cell; noiseless complete-truth-table case. | Experimentation / Progress | active |
| GVN-C-003 | Greedy improves clean parent-set recovery overall but with one regression. | bounded | greedy-vs-nd handoff (QI-002 clean 3/6 -> 4/6; QI-001 colliders clean in all modes; QI-002 cat3 fork regressed exact -> superset) | Not graph recovery; QI-004 unchanged (0/15) at noisy n=20. | Experimentation / Progress | active |

### QN-001 (planned)

| Claim ID | Claim | Strength | Evidence | Caveats | Report location | Status |
|---|---|---|---|---|---|---|
| QN-001-C-001 | TBD — quantitative confirmation of the greedy-vs-nd signals. | TBD | `docs/experiments/QN-001.md` | Requires repeated seeds and proper timing methodology. | TBD | pending |

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