"""Run m1.1 ablation interventions (Stage 3 only).

See ``docs/research/milestone_plans/milestone1_part1_ablations.md`` and
``causal/configs/experiments/M11_ablations.yaml``.

Usage (from repo root):
    python -m causal.scripts.m11_ablation_run --abl ABL-101
    python -m causal.scripts.m11_ablation_run --tier 0,1
    python -m causal.scripts.m11_ablation_run --all-required
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

_REPO = Path(__file__).resolve().parents[2]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from causal.experiments.handcrafted import load_handcrafted
from causal.experiments.m11_ablation_bk import (
    bk_rule_multiset,
    build_intervened_bk,
    read_bk_text,
)
from causal.experiments.m11_ablation_inspect import (
    AblationExpected,
    inspect_ablation_dir,
    write_summary,
)
from causal.experiments.run_grid import _relocate_sol_artefacts
from causal.run_aba_asp import ABASPRunner

_CONFIG = _REPO / "causal/configs/experiments/M11_ablations.yaml"

INTERVENTION_ORDER = ["ABL-101", "ABL-102", "ABL-103", "ABL-105", "ABL-106"]
REQUIRED_AFTER_101 = ["ABL-102", "ABL-103", "ABL-105"]


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
    root = _resolve(cfg["defaults"]["grid_root"])
    return root / dgp


def ablation_root(cfg: dict[str, Any]) -> Path:
    return _resolve(cfg["defaults"]["ablation_root"])


def abl_dir_for(cfg: dict[str, Any], abl_id: str) -> Path:
    return ablation_root(cfg) / abl_id


def _learning_options(cfg: dict[str, Any], spec: dict[str, Any]) -> dict[str, str]:
    opts: dict[str, str] = {
        "folding_mode": cfg["defaults"]["folding_mode"],
        "folding_steps": str(cfg["defaults"]["folding_steps"]),
    }
    overrides = spec.get("learning_options") or {}
    for key, val in overrides.items():
        opts[key] = str(val)
    return opts


def run_intervention(abl_id: str, spec: dict[str, Any], cfg: dict[str, Any]) -> dict[str, Any]:
    if spec.get("type") != "intervention":
        raise ValueError(f"{abl_id} is not an intervention ablation")

    baseline_dgp = spec["baseline_dgp"]
    base_cell = cell_dir(cfg, baseline_dgp)
    out_dir = abl_dir_for(cfg, abl_id)
    out_dir.mkdir(parents=True, exist_ok=True)

    baseline_bk_path = base_cell / "bk.aba"
    baseline_data_path = base_cell / "data.csv"
    if not baseline_bk_path.is_file():
        raise FileNotFoundError(f"baseline BK missing: {baseline_bk_path}")
    if not baseline_data_path.is_file():
        raise FileNotFoundError(f"baseline data missing: {baseline_data_path}")

    baseline_bk = read_bk_text(baseline_bk_path)
    bk_mode = spec.get("bk_mode", "copy_baseline")
    source_text: str | None = None
    if bk_mode == "block_order_from":
        src_dgp = spec["bk_source_dgp"]
        source_text = read_bk_text(cell_dir(cfg, src_dgp) / "bk.aba")

    intervened = build_intervened_bk(
        baseline_bk,
        mode=bk_mode,
        source_text=source_text,
        prepend_rules=spec.get("prepend_rules"),
    )

    if bk_mode == "block_order_from" and not bk_rule_multiset(baseline_bk, intervened):
        raise ValueError(f"{abl_id}: block reorder changed rule multiset")

    shutil.copy2(baseline_data_path, out_dir / "data.csv")
    (out_dir / "bk.baseline.aba").write_text(baseline_bk, encoding="utf-8")
    bk_path = out_dir / "bk.aba"
    bk_path.write_text(intervened, encoding="utf-8")

    fx = load_handcrafted(baseline_dgp)
    pos = list(fx.pos_examples)
    neg = list(fx.neg_examples)

    learning_options = _learning_options(cfg, spec)
    timeout_s = float(cfg["defaults"]["prolog_timeout_s"])

    runner = ABASPRunner()
    if not runner.prolog_available:
        raise RuntimeError("SWI-Prolog not available")

    cmd_parts = [
        "python -m causal.scripts.m11_ablation_run",
        f"--abl {abl_id}",
    ]
    manifest: dict[str, Any] = {
        "abl_id": abl_id,
        "spec": spec,
        "baseline_dgp": baseline_dgp,
        "baseline_cell": str(base_cell.relative_to(_REPO)),
        "bk_mode": bk_mode,
        "learning_options": learning_options,
        "command": " ".join(cmd_parts),
        "git_commit": _git_commit(),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "intervention_summary": {
            "rule_multiset_preserved": bk_mode != "prepend_rules"
            and bk_rule_multiset(baseline_bk, intervened),
            "baseline_rule_count": len(
                [ln for ln in baseline_bk.splitlines() if ":-" in ln and ln.strip().endswith(".")]
            ),
        },
    }
    (out_dir / "abl_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )

    t0 = time.monotonic()
    result = runner.run_prolog_aba_asp(
        bk_path,
        positive_examples=pos,
        negative_examples=neg,
        learning_options=learning_options,
        timeout_s=timeout_s,
    )
    wall = time.monotonic() - t0

    stdout = result.get("stdout", "") or ""
    stderr = result.get("stderr", "") or ""
    (out_dir / "prolog.stdout").write_text(stdout, encoding="utf-8")
    (out_dir / "prolog.stderr").write_text(stderr, encoding="utf-8")

    _relocate_sol_artefacts(bk_path)

    expected = AblationExpected.from_dict(spec.get("expected"))
    summary = inspect_ablation_dir(
        out_dir,
        abl_id,
        expected,
        tests=spec.get("tests"),
    )
    write_summary(out_dir, summary)

    return {
        "abl_id": abl_id,
        "verdict": summary.verdict,
        "mismatches": summary.mismatches,
        "wall_clock_s": wall,
        "out_dir": str(out_dir.relative_to(_REPO)),
    }


def _append_decision_log(root: Path, line: str) -> None:
    summary_dir = root / "summary"
    summary_dir.mkdir(parents=True, exist_ok=True)
    log_path = summary_dir / "decision_log.md"
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(f"- [{stamp}] {line}\n")


def _write_results_table(cfg: dict[str, Any]) -> None:
    root = ablation_root(cfg)
    summary_dir = root / "summary"
    summary_dir.mkdir(parents=True, exist_ok=True)
    rows: list[str] = [
        "# M1.1 ablation results",
        "",
        "| ABL | type | verdict | first_fold | entailment | trace_lines | aba_rules | notes |",
        "|-----|------|---------|------------|------------|-------------|-----------|-------|",
    ]
    for abl_id in sorted((cfg.get("ablations") or {}).keys()):
        summ_path = root / abl_id / "abl_summary.json"
        if not summ_path.is_file():
            continue
        data = json.loads(summ_path.read_text(encoding="utf-8"))
        obs = data.get("observables", {})
        spec = cfg["ablations"][abl_id]
        notes = "; ".join(data.get("mismatches", [])[:2])
        rows.append(
            f"| {abl_id} | {spec.get('type', '?')} | {data.get('verdict', '?')} | "
            f"{obs.get('first_fold_pred', '')} | {obs.get('entailment', '')} | "
            f"{obs.get('trace_lines', '')} | {obs.get('aba_rules', '')} | {notes} |"
        )
    (summary_dir / "abl_results.md").write_text("\n".join(rows) + "\n", encoding="utf-8")


def run_gated_sequence(
    *,
    tiers: set[int] | None = None,
    all_required: bool = False,
    include_optional: bool = False,
    abl_ids: list[str] | None = None,
) -> int:
    cfg = load_config()
    root = ablation_root(cfg)
    root.mkdir(parents=True, exist_ok=True)

    if abl_ids:
        for abl_id in abl_ids:
            spec = cfg["ablations"][abl_id]
            if spec.get("type") == "audit":
                print(f"Skipping audit {abl_id} in run script; use m11_ablation_audit.py")
                continue
            print(f"Running {abl_id}...")
            res = run_intervention(abl_id, spec, cfg)
            print(json.dumps(res, indent=2))
        _write_results_table(cfg)
        return 0

    from causal.scripts.m11_ablation_audit import run_audit

    # Tier 0: ABL-100
    if tiers is None or 0 in tiers or all_required:
        print("Running ABL-100 audit...")
        audit_100 = run_audit("ABL-100", cfg)
        print(json.dumps(audit_100, indent=2))
        if audit_100.get("verdict") != "audit_pass":
            _append_decision_log(root, "ABL-100 audit_fail → STOP before Tier 1+")
            _write_results_table(cfg)
            return 1

    run_101 = tiers is None or 1 in tiers or all_required
    if not run_101:
        _write_results_table(cfg)
        return 0

    print("Running ABL-101...")
    res_101 = run_intervention("ABL-101", cfg["ablations"]["ABL-101"], cfg)
    print(json.dumps(res_101, indent=2))

    if res_101["verdict"] != "pass":
        print("ABL-101 failed → running ABL-104 audit and STOP")
        run_audit("ABL-104", cfg)
        _append_decision_log(
            root,
            f"ABL-101 {res_101['verdict']} → ABL-104 audit; STOP before Tier 2+",
        )
        _write_results_table(cfg)
        return 1

    _append_decision_log(root, "ABL-101 pass → continue Tier 2+")

    if not all_required and tiers == {0, 1}:
        _write_results_table(cfg)
        return 0

    to_run = list(REQUIRED_AFTER_101)
    if include_optional:
        to_run.append("ABL-106")
    elif all_required:
        # ABL-106 only if 105 inconclusive — handled below
        pass

    for abl_id in to_run:
        print(f"Running {abl_id}...")
        res = run_intervention(abl_id, cfg["ablations"][abl_id], cfg)
        print(json.dumps(res, indent=2))

    if all_required:
        print("Running ABL-107 audit...")
        from causal.scripts.m11_ablation_audit import run_audit as _audit

        _audit("ABL-107", cfg)

        summ_105_path = root / "ABL-105" / "abl_summary.json"
        if summ_105_path.is_file():
            s105 = json.loads(summ_105_path.read_text(encoding="utf-8"))
            inconclusive = s105.get("verdict") not in ("pass", "fail")
            if inconclusive or include_optional:
                spec106 = cfg["ablations"]["ABL-106"]
                if spec106.get("optional"):
                    print("Running optional ABL-106...")
                    run_intervention("ABL-106", spec106, cfg)

    _write_results_table(cfg)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run m1.1 ablation interventions")
    parser.add_argument("--abl", help="Single ablation id (e.g. ABL-101)")
    parser.add_argument(
        "--tier",
        help="Comma-separated tier numbers (e.g. 0,1) with gating",
    )
    parser.add_argument(
        "--all-required",
        action="store_true",
        help="Run closure set with gating (100 → 101 → 102/103/105 → 107)",
    )
    parser.add_argument(
        "--include-optional",
        action="store_true",
        help="Include optional ABL-106 when running full sequence",
    )
    args = parser.parse_args(argv)

    if args.abl:
        cfg = load_config()
        spec = cfg["ablations"][args.abl]
        if spec.get("type") == "audit":
            from causal.scripts.m11_ablation_audit import run_audit

            result = run_audit(args.abl, cfg)
            print(json.dumps(result, indent=2))
            return 0 if result.get("verdict") == "audit_pass" else 1
        result = run_intervention(args.abl, spec, cfg)
        print(json.dumps(result, indent=2))
        _write_results_table(cfg)
        return 0 if result["verdict"] == "pass" else 1

    tiers: set[int] | None = None
    if args.tier:
        tiers = {int(x.strip()) for x in args.tier.split(",")}

    return run_gated_sequence(
        tiers=tiers,
        all_required=args.all_required,
        include_optional=args.include_optional,
    )


if __name__ == "__main__":
    raise SystemExit(main())
