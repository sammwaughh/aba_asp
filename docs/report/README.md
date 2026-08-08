# Report writing

This directory holds **report planning and guardrails** (`docs/report/`) and the **manuscript
sources** (`docs/report/manuscript/`).

## Quick map

| Path | Role |
|---|---|
| `manuscript/*.tex` | Authoritative report chapters (LaTeX; Samuel-authored) |
| `manuscript/*.md` | Markdown mirrors of each chapter for ChatGPT Project context |
| `report_state.md` | Section status, evidence map, writing workflow |
| `claims_ledger.md` | Evidence-to-claim guardrail |
| `figure_table_index.md` | Figure/table provenance |
| `genai_use_log.md` | Factual log of AI-agent assistance |
| `findings/` | Supervisor-facing milestone findings logs (`.tex`; not manuscript chapters) |

## Manuscript chapters

Expected LaTeX sources (copy or edit under `manuscript/`):

| Chapter | `.tex` | `.md` mirror |
|---|---|---|
| Introduction | `introduction.tex` | `introduction.md` |
| Literature review | `literature_review.tex` | `literature_review.md` |
| Background | `background.tex` | `background.md` |
| Experimentation | `experimentation.tex` | `experimentation.md` |
| Project plan | `project_plan.tex` | `project_plan.md` |

See `manuscript/README.md` for the `.tex` / `.md` pairing rule and compilation notes.

## Relationship to other docs

- **Theory canon** (`docs/theory/`) — background and literature `.tex` files may have started
  here; report chapters in `manuscript/` are the submitted-report sources once copied in.
- **Experiment evidence** (`docs/experiments/`) — facts, commands, artefacts; not polished
  report prose. Check claims against `claims_ledger.md` before citing in the manuscript.
- **Milestone findings** (`findings/`) — standalone supervisor logs per milestone part; compile
  with `pdflatex` or share source. Not part of `manuscript/`.
- **M1.3 Bucket-3 / Milestone-1 closure synthesis** —
  `docs/experiments/qualitative/M13-C3-binary-collider-and/findings_for_fabrizio.tex`;
  six bounded findings from H0–H7b. It is supervisor-facing support, not automatically a
  submitted manuscript chapter.
- **Research state** (`docs/research/`) — project state, supervisor context, experiment
  register; supports the project-plan chapter but is not the manuscript itself.

## Workflow (from `AGENTS.md`)

1. The responsible implementation or evidence agent records experiment evidence in
   `docs/experiments/<ID>.md`.
2. Samuel reviews and corrects the experiment record.
3. The Orchestrator or a named writing agent drafts candidate report prose from reviewed
   records and manuscript mirrors when Samuel requests it.
4. Samuel verifies, edits, and authors the final `.tex`.
5. Claims are checked against `claims_ledger.md`.

Agents should not write polished report prose unless explicitly asked.
