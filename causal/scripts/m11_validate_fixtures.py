"""Validate the m1.1 parent-position fixtures and emit a validation manifest.

Runs the Stage-0 (pre-learning) validation for the eight metamorphic chain
fixtures of Milestone 1, Part 1
(``docs/research/milestone_plans/milestone1_part1_parent_position.md``):

- structural (table-only) checks per cell;
- generated background knowledge (BK) via ``execute_cell_stage2`` (no Prolog);
- the BK predictor-group order against the requested order;
- the sigma / pi orbit relations (A/B, D/C sigma-pairs; A/D, B/C pi-pairs).

It writes, into a NEW output directory (it does not touch QI-002 artefacts):

- ``cells/<cell>/bk.aba`` and ``cells/<cell>/data.csv`` for each cell;
- ``manifest.md`` (the human-readable manifest table);
- ``manifest.json`` (machine-readable manifest + check results).

Scope: parent-set / learned-rule recovery proxy via ABA Learning, NOT
Russo-style Causal ABA. This script does NOT run ABA Learning (no swipl/clingo).

Usage (Prolog-free; from repo root):
    python causal/scripts/m11_validate_fixtures.py
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_THIS = Path(__file__).resolve()
_REPO_ROOT = _THIS.parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from causal.experiments.config import CellSpec
from causal.experiments.handcrafted import load_handcrafted
from causal.experiments.handcrafted_m11 import (
    M11_CELLS,
    M11CellMeta,
    bk_predictor_order,
    is_pi_pair,
    is_sigma_pair,
    predictor_columns,
    structural_checks,
)
from causal.experiments.run_grid import execute_cell_stage2

_DEFAULT_OUT = _REPO_ROOT / "causal/outputs/m11_parent_position/validation"


def _cell_spec(meta: M11CellMeta) -> CellSpec:
    fx = load_handcrafted(meta.key)
    return CellSpec(
        experiment_id="M11_parent_position",
        dgp=meta.key,
        nodes=fx.nodes,
        edges=fx.edges,
        n=len(fx.df),
        seed=0,
        target="x2",
        config_hash="sha256:validation",
        run_id=meta.key,
        cell_dir_name=meta.key,
        graph_type="handcrafted_table",
        example_split="handcrafted",
        handcrafted_source=meta.key,
    )


def _target_excluded(bk_text: str) -> bool:
    return (
        "Skipping excluded variable: x2" in bk_text
        and "x2(A) :-" not in bk_text
        and "x2_val_" not in bk_text
    )


def _generate_bk(meta: M11CellMeta, out_dir: Path) -> str:
    """Generate BK + data.csv for one cell (stage 2 only, no Prolog)."""
    cell_dir = out_dir / "cells" / meta.key
    out = execute_cell_stage2(
        _cell_spec(meta),
        cell_dir,
        graph_type="handcrafted_table",
        bins=3,
        bin_strategy="uniform",
        example_split="handcrafted",
    )
    if out.outcome != "ok" or out.bk_path is None or not out.bk_path.is_file():
        raise RuntimeError(f"{meta.key}: stage2 failed (outcome={out.outcome})")
    return out.bk_path.read_text(encoding="utf-8")


def _orbit_relations() -> dict[str, bool]:
    """sigma-pairs (A/B, D/C) and pi-pairs (A/D, B/C) per encoding."""
    relations: dict[str, bool] = {}
    for encoding in ("binary", "cat3"):
        a = load_handcrafted(f"m11_{encoding}_A")
        b = load_handcrafted(f"m11_{encoding}_B")
        c = load_handcrafted(f"m11_{encoding}_C")
        d = load_handcrafted(f"m11_{encoding}_D")
        relations[f"{encoding}:sigma(A->B)"] = is_sigma_pair(a, b)
        relations[f"{encoding}:sigma(D->C)"] = is_sigma_pair(d, c)
        relations[f"{encoding}:pi(A->D)"] = is_pi_pair(a, d)
        relations[f"{encoding}:pi(B->C)"] = is_pi_pair(b, c)
    return relations


def build_manifest(out_dir: Path) -> dict[str, Any]:
    """Generate BK, run checks, and assemble the manifest payload."""
    rows: list[dict[str, Any]] = []
    for meta in M11_CELLS:
        fx = load_handcrafted(meta.key)
        bk_text = _generate_bk(meta, out_dir)

        checks = structural_checks(meta.key)
        bk_order = bk_predictor_order(bk_text)
        target_excluded = _target_excluded(bk_text)

        checks["bk_order_matches_requested"] = bk_order == list(meta.requested_order)
        checks["target_excluded_from_bk"] = target_excluded

        rows.append(
            {
                "encoding": meta.encoding,
                "cell": meta.cell,
                "parent": meta.parent,
                "requested_order": list(meta.requested_order),
                "table_order": list(predictor_columns(fx)),
                "bk_order": bk_order,
                "target_excluded": target_excluded,
                "checks": checks,
                "all_checks_pass": all(checks.values()),
            }
        )

    relations = _orbit_relations()
    return {
        "experiment_id": "M11_parent_position",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Stage-0 fixture validation (pre-learning); parent-set recovery proxy, not Russo-style Causal ABA.",
        "cells": rows,
        "orbit_relations": relations,
        "all_cells_pass": all(r["all_checks_pass"] for r in rows),
        "all_relations_pass": all(relations.values()),
    }


def _fmt_order(order: list[str]) -> str:
    return "[" + ", ".join(order) + "]"


def render_markdown(manifest: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# m1.1 fixture validation manifest")
    lines.append("")
    lines.append(f"- Experiment: `{manifest['experiment_id']}`")
    lines.append(f"- Generated (UTC): {manifest['generated_utc']}")
    lines.append(f"- Scope: {manifest['scope']}")
    lines.append(
        f"- All cells pass: **{manifest['all_cells_pass']}**; "
        f"all orbit relations pass: **{manifest['all_relations_pass']}**"
    )
    lines.append("")
    lines.append(
        "| Encoding | Cell | Parent | Requested order | Table order | "
        "BK order | Target excluded | Fixture checks |"
    )
    lines.append("|---|---|---|---|---|---|---|---|")
    for r in manifest["cells"]:
        checks_str = "PASS" if r["all_checks_pass"] else (
            "FAIL: " + ", ".join(n for n, ok in r["checks"].items() if not ok)
        )
        lines.append(
            f"| {r['encoding']} | {r['cell']} | `{r['parent']}` | "
            f"{_fmt_order(r['requested_order'])} | {_fmt_order(r['table_order'])} | "
            f"{_fmt_order(r['bk_order'])} | {r['target_excluded']} | {checks_str} |"
        )
    lines.append("")
    lines.append("## Orbit relations")
    lines.append("")
    lines.append("| Relation | Holds |")
    lines.append("|---|---|")
    for name, ok in manifest["orbit_relations"].items():
        lines.append(f"| `{name}` | {ok} |")
    lines.append("")
    lines.append("## Per-cell check detail")
    lines.append("")
    for r in manifest["cells"]:
        lines.append(f"### {r['encoding']} cell {r['cell']}")
        lines.append("")
        for name, ok in r["checks"].items():
            lines.append(f"- {'PASS' if ok else 'FAIL'} `{name}`")
        lines.append("")
    return "\n".join(lines)


def write_manifest(manifest: dict[str, Any], out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "manifest.json"
    md_path = out_dir / "manifest.md"
    json_path.write_text(json.dumps(manifest, indent=2, sort_keys=False), encoding="utf-8")
    md_path.write_text(render_markdown(manifest), encoding="utf-8")
    return json_path, md_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate m1.1 fixtures (Prolog-free)")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=_DEFAULT_OUT,
        help=f"Output directory (default: {_DEFAULT_OUT})",
    )
    args = parser.parse_args(argv)
    out_dir = Path(args.out_dir)

    manifest = build_manifest(out_dir)
    json_path, md_path = write_manifest(manifest, out_dir)

    print(render_markdown(manifest))
    print(f"\nWrote: {md_path}")
    print(f"Wrote: {json_path}")

    ok = manifest["all_cells_pass"] and manifest["all_relations_pass"]
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
