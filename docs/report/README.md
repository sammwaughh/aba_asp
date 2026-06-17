# Report writing

This directory holds **report planning and guardrails** (`docs/report/`) and the **manuscript
sources** (`docs/report/manuscript/`).

## Quick map

| Path | Role |
|---|---|
| `manuscript/*.tex` | Authoritative report chapters (LaTeX; Samuel-authored) |
| `manuscript/*.md` | Markdown mirrors of each chapter for ChatGPT Project context |
| `interim_section_plan.md` | Section status, evidence map, writing workflow |
| `claims_ledger.md` | Evidence-to-claim guardrail |
| `figure_table_index.md` | Figure/table provenance |
| `genai_use_log.md` | Factual log of ChatGPT/Cursor assistance |

## Manuscript chapters

Expected LaTeX sources (copy or edit under `manuscript/`):

| Chapter | `.tex` | `.md` mirror |
|---|---|---|
| Introduction | `introduction.tex` | `introduction.md` |
| Literature review | `literature-review.tex` | `literature-review.md` |
| Background | `background.tex` | `background.md` |
| Experimentation | `experimentation.tex` | `experimentation.md` |
| Project plan | `project_plan.tex` | `project_plan.md` |

See `manuscript/README.md` for the `.tex` / `.md` pairing rule and compilation notes.

## Relationship to other docs

- **Theory canon** (`docs/theory/`) — background and literature `.tex` files may have started
  here; report chapters in `manuscript/` are the submitted-report sources once copied in.
- **Experiment evidence** (`docs/experiments/`) — facts, commands, artefacts; not polished
  report prose. Check claims against `claims_ledger.md` before citing in the manuscript.
- **Research state** (`docs/research/`) — project state, supervisor context, experiment
  register; supports the project-plan chapter but is not the manuscript itself.

## Workflow (from `AGENTS.md`)

1. Cursor records experiment evidence in `docs/experiments/<ID>.md`.
2. Samuel reviews and corrects the experiment record.
3. ChatGPT drafts candidate report prose from reviewed records + manuscript mirrors.
4. Samuel verifies, edits, and authors the final `.tex`.
5. Claims are checked against `claims_ledger.md`.

Cursor should not write polished report prose unless explicitly asked.
