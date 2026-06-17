# ChatGPT context mirror

Upload-staging copy of the project-state and orientation docs for the **ChatGPT Project**.
The files here are **generated copies** of repo originals, kept under canonical (matching)
filenames so the repo and the ChatGPT Project use the same names 1:1.

## How to use

1. Cursor edits the **repo originals** (the source-of-truth column below), never the copies here.
2. Before re-uploading to ChatGPT, re-copy the originals into this folder (run
   `scripts/sync_chatgpt_context.sh`, or copy manually).
3. Upload everything in `governance/` and `repo_orientation/` to the ChatGPT Project,
   replacing the existing files.
4. In the ChatGPT Project, delete any old `*_current.md` files so names match exactly
   (the `_current` suffix has been dropped).

Do not edit files in this folder by hand; edits will be overwritten on the next sync.

## Manifest

### governance/ (7)

| Mirror file | Repo source (source of truth) |
|---|---|
| `governance/research_state.md` | `docs/research/research_state.md` |
| `governance/experiment_register.md` | `docs/research/experiment_register.md` |
| `governance/chatgpt_project_brief.md` | `docs/research/chatgpt_project_brief.md` |
| `governance/supervisor_guidance.md` | `docs/research/supervisor_guidance.md` |
| `governance/claims_ledger.md` | `docs/report/claims_ledger.md` |
| `governance/report_state.md` | `docs/report/report_state.md` |
| `governance/experiments_summary.md` | `docs/experiments/experiments_summary.md` |

### repo_orientation/ (7)

| Mirror file | Repo source (source of truth) |
|---|---|
| `repo_orientation/repo_map.md` | `docs/research/repo_map.md` |
| `repo_orientation/execution_guide.md` | `docs/research/execution_guide.md` |
| `repo_orientation/fabrizio_project_description.md` | `docs/research/fabrizio_project_description.md` |
| `repo_orientation/imperial_assessment_brief.md` | `docs/research/imperial_assessment_brief.md` |
| `repo_orientation/AGENTS.md` | `AGENTS.md` |
| `repo_orientation/environment_setup.md` | `docs/research/environment_setup.md` |
| `repo_orientation/PROJECT_README.md` | `PROJECT_README.md` |

## Renames behind this mirror

Three repo originals were renamed to canonical names; the ChatGPT `_current` suffix is dropped:

| Old repo name | Canonical name | Old ChatGPT name |
|---|---|---|
| `docs/research/supervisor_updates.md` | `supervisor_guidance.md` | `supervisor_guidance_current.md` |
| `docs/report/interim_section_plan.md` | `report_state.md` | `report_state_current.md` |
| `docs/experiments/experiment_index.md` | `experiments_summary.md` | `experiments_summary_current.md` |
| `docs/report/claims_ledger.md` (unchanged) | `claims_ledger.md` | `claims_ledger_current.md` |

The manuscript chapter mirrors (`docs/report/manuscript/*.md`) are intentionally **not**
included in this upload set.
