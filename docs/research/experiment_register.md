# Experiment Register

Lightweight index of experiments and a reusable template. Detailed records live under
`docs/experiments/` per the research-logging rule; this register is the at-a-glance view for
project framing and reporting.

## Status categories

- `proposed` — idea noted; not yet designed in full.
- `planned` — design agreed (question, setup, metrics, interpretation rule).
- `implemented` — code in place (by Cursor); not yet run.
- `run` — executed; raw artefacts produced.
- `analysed` — results interpreted against the interpretation rule.
- `reported` — written into an interim/final report section.

## Register

| ID | Title | Status |
|----|-------|--------|
| QL-001 | Minimal synthetic parent-set recovery (toy) | proposed |

## Template

Copy this block per experiment.

```
### <ID> — <short title>
- Status: proposed | planned | implemented | run | analysed | reported
- Research question:
- Theoretical motivation:
- Relation to ABA Learning:
- Relation to Causal ABA:
- Code path:
- Dataset / DGP:
- Target variable(s):
- Metrics:
- Baseline / comparator:
- Expected result:
- Interpretation rule:        # what each outcome would and would NOT show
- Failure modes:
- Cursor implementation plan / prompt:   # link or prompt text
- Commit hash / run artifact path:
- Report relevance:
```

## Entries

### QL-001 — Minimal synthetic parent-set recovery (toy)
- Status: **proposed** (design still to be reviewed; do not implement yet).
- Research question: TBD — likely "On a minimal synthetic case, can the existing ABA
  Learning bridge recover a target variable's true parent set?"
- Theoretical motivation: TBD — feasibility/coherence probe for applying ABA Learning to
  causal discovery (Direction 1); see `research_state.md`.
- Relation to ABA Learning: uses the inherited transformation-rule learner via the
  `causal/` bridge.
- Relation to Causal ABA: **does not** exercise Russo-style `arr/noe/indep` or
  d-separation; parent-set recovery only. Keep this distinction in any write-up.
- Code path: existing `causal/` bridge (no new encoding planned for QL-001).
- Dataset / DGP: TBD — likely a small synthetic DGP (e.g. 3-variable chain/fork/collider).
- Target variable(s): TBD.
- Metrics: TBD — likely parent-set / body-F1 style recovery already in `causal/metrics.py`.
- Baseline / comparator: TBD.
- Expected result: not asserted (experiment not run).
- Interpretation rule: must separate empirical parent recovery from causal-argumentative
  discovery; recovery would be evidence of feasibility, not of full Causal ABA.
- Failure modes: TBD (e.g. no solution, clingo/path issues — see `execution_guide.md`).
- Cursor implementation plan / prompt: TBD (after design review).
- Commit hash / run artifact path: —
- Report relevance: would support the "applying ABA Learning to causal discovery" section.

Note: QL-001 is intentionally minimal and under-specified here. Design it fully (and review
conceptual well-posedness) before promoting it to `planned` and handing to Cursor.
