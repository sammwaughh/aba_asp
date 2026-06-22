"""Read-only audits for m1.1 ablations (ABL-100, ABL-104, ABL-107).

Compares existing grid-cell ``prolog.stdout`` traces without running Prolog.

Usage (from repo root):
    python -m causal.scripts.m11_ablation_audit --abl ABL-100
    python -m causal.scripts.m11_ablation_audit --all
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

_REPO = Path(__file__).resolve().parents[2]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from causal.experiments.m11_ablation_inspect import (
    AblationExpected,
    compare_audit_pair,
    parse_trace_observables,
    write_summary,
)

_CONFIG = _REPO / "causal/configs/experiments/M11_ablations.yaml"
AUDIT_IDS = ("ABL-100", "ABL-104", "ABL-107")


def _git_commit() -> str | None:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            cwd=_REPO,
            check=True,
        )
        return out.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def load_config() -> dict[str, Any]:
    with _CONFIG.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _resolve(path_str: str) -> Path:
    p = Path(path_str)
    return p if p.is_absolute() else _REPO / p


def cell_dir(cfg: dict[str, Any], dgp: str) -> Path:
    return _resolve(cfg["defaults"]["grid_root"]) / dgp


def ablation_root(cfg: dict[str, Any]) -> Path:
    return _resolve(cfg["defaults"]["ablation_root"])


def run_audit(abl_id: str, cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    if cfg is None:
        cfg = load_config()
    spec = cfg["ablations"][abl_id]
    if spec.get("type") != "audit":
        raise ValueError(f"{abl_id} is not an audit ablation")

    audit = spec.get("audit") or {}
    left_dgp = audit["left_dgp"]
    right_dgp = audit["right_dgp"]
    left_path = cell_dir(cfg, left_dgp) / "prolog.stdout"
    right_path = cell_dir(cfg, right_dgp) / "prolog.stdout"

    if not left_path.is_file():
        raise FileNotFoundError(f"missing trace: {left_path}")
    if not right_path.is_file():
        raise FileNotFoundError(f"missing trace: {right_path}")

    left_stdout = left_path.read_text(encoding="utf-8")
    right_stdout = right_path.read_text(encoding="utf-8")

    expected_left = AblationExpected.from_dict(spec.get("expected_left"))
    expected_right = AblationExpected.from_dict(spec.get("expected_right"))

    summary = compare_audit_pair(
        abl_id,
        left_stdout,
        right_stdout,
        left_label=left_dgp,
        right_label=right_dgp,
        expected_left=expected_left,
        expected_right=expected_right,
        tests=spec.get("tests"),
    )

    out_dir = ablation_root(cfg) / abl_id
    out_dir.mkdir(parents=True, exist_ok=True)

    left_obs = parse_trace_observables(left_stdout)
    right_obs = parse_trace_observables(right_stdout)

    md_lines = [
        f"# {abl_id} audit",
        "",
        f"- left: `{left_dgp}` → `{left_path.relative_to(_REPO)}`",
        f"- right: `{right_dgp}` → `{right_path.relative_to(_REPO)}`",
        "",
        "## Side-by-side observables",
        "",
        "| cell | first_fold | entailment | trace_lines | aba_rules |",
        "|------|------------|------------|-------------|-----------|",
        f"| {left_dgp} | {left_obs.first_fold_pred} | {left_obs.entailment} | "
        f"{left_obs.trace_lines} | {left_obs.aba_rules} |",
        f"| {right_dgp} | {right_obs.first_fold_pred} | {right_obs.entailment} | "
        f"{right_obs.trace_lines} | {right_obs.aba_rules} |",
        "",
        f"**Verdict:** `{summary.verdict}`",
        "",
    ]
    if summary.mismatches:
        md_lines.append("## Mismatches")
        md_lines.append("")
        for m in summary.mismatches:
            md_lines.append(f"- {m}")
        md_lines.append("")

    if audit.get("note"):
        md_lines.extend(["## Note", "", audit["note"], ""])

    (out_dir / "audit_report.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    manifest = {
        "abl_id": abl_id,
        "type": "audit",
        "left_dgp": left_dgp,
        "right_dgp": right_dgp,
        "git_commit": _git_commit(),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    (out_dir / "abl_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )

    write_summary(out_dir, summary)

    return summary.to_dict()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="m1.1 ablation read-only audits")
    parser.add_argument("--abl", help="Audit id (ABL-100, ABL-104, ABL-107)")
    parser.add_argument("--all", action="store_true", help="Run all audit ablations")
    args = parser.parse_args(argv)

    cfg = load_config()
    ids = list(AUDIT_IDS) if args.all else ([args.abl] if args.abl else [])
    if not ids:
        parser.error("specify --abl or --all")

    rc = 0
    for abl_id in ids:
        result = run_audit(abl_id, cfg)
        print(json.dumps(result, indent=2))
        if result.get("verdict") != "audit_pass":
            rc = 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
