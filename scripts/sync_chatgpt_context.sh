#!/usr/bin/env bash
# Re-copy the repo source-of-truth docs into docs/chatgpt_context/ for ChatGPT Project upload.
# Idempotent: overwrites the mirror copies with the current repo originals.
# Run from anywhere; paths are resolved relative to the repo root.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

DEST="docs/chatgpt_context"
mkdir -p "$DEST/governance" "$DEST/repo_orientation"

# governance/ : "<source>=<dest-name>"
governance=(
  "docs/research/research_state.md=research_state.md"
  "docs/research/experiment_register.md=experiment_register.md"
  "docs/research/chatgpt_project_brief.md=chatgpt_project_brief.md"
  "docs/research/supervisor_guidance.md=supervisor_guidance.md"
  "docs/report/claims_ledger.md=claims_ledger.md"
  "docs/report/report_state.md=report_state.md"
  "docs/experiments/experiments_summary.md=experiments_summary.md"
)

# repo_orientation/ : "<source>=<dest-name>"
repo_orientation=(
  "docs/research/repo_map.md=repo_map.md"
  "docs/research/execution_guide.md=execution_guide.md"
  "docs/research/fabrizio_project_description.md=fabrizio_project_description.md"
  "docs/research/imperial_assessment_brief.md=imperial_assessment_brief.md"
  "AGENTS.md=AGENTS.md"
  "docs/research/environment_setup.md=environment_setup.md"
  "PROJECT_README.md=PROJECT_README.md"
)

copy_pair() {
  local group_dir="$1"
  local pair="$2"
  local src="${pair%%=*}"
  local name="${pair##*=}"
  if [[ ! -f "$src" ]]; then
    echo "ERROR: missing source $src" >&2
    exit 1
  fi
  cp "$src" "$DEST/$group_dir/$name"
  echo "  $src -> $DEST/$group_dir/$name"
}

echo "Syncing ChatGPT context mirror..."
for pair in "${governance[@]}"; do
  copy_pair "governance" "$pair"
done
for pair in "${repo_orientation[@]}"; do
  copy_pair "repo_orientation" "$pair"
done
echo "Done. Upload $DEST/governance/* and $DEST/repo_orientation/* to the ChatGPT Project."
