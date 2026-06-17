"""Generate appendix.md with verbatim QL1/QL2/QL3 tabular data from fixtures."""

from __future__ import annotations

from pathlib import Path
import sys

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from causal.experiments.handcrafted import load_handcrafted
from causal.experiments.handcrafted_qi001 import QI001_BUILDERS
from causal.experiments.handcrafted_qi002 import QI002_BUILDERS
from causal.experiments.handcrafted_qi004 import QI004_BUILDERS

OUT = _REPO.parent / "appendix.md"

QL1_ORDER = [
    "qi001_chain_binary",
    "qi001_fork_binary",
    "qi001_collider_binary",
    "qi001_chain_cat3",
    "qi001_fork_cat3",
    "qi001_collider_cat3",
    "qi001_chain_cont3",
    "qi001_fork_cont3",
    "qi001_collider_cont3",
]
QL2_ORDER = [
    "qi002_chain_binary",
    "qi002_fork_binary",
    "qi002_collider_binary",
    "qi002_chain_cat3",
    "qi002_fork_cat3",
    "qi002_collider_cat3",
]
QL3_ORDER = sorted(QI004_BUILDERS.keys())

MOTIF_INFO = {
    "chain": ("x0 -> x1 -> x2", "{x1}"),
    "fork": ("x0 -> x1, x0 -> x2", "{x0}"),
    "collider": ("x0 -> x2, x1 -> x2", "{x0, x1}"),
}

QL3_INFO = {
    "qi004_chain_x1parent": ("chain (parent in x1)", "x0 -> x1 -> x2", "{x1}"),
    "qi004_chain_x0parent": ("chain (parent in x0)", "x1 -> x0 -> x2", "{x0}"),
    "qi004_fork_x0parent": ("fork (parent in x0)", "x0 -> x1, x0 -> x2", "{x0}"),
    "qi004_fork_x1parent": ("fork (parent in x1)", "x1 -> x0, x1 -> x2", "{x1}"),
    "qi004_collider": ("collider", "x0 -> x2, x1 -> x2", "{x0, x1}"),
}

POS_RULE = {
    "binary": "x2 == 1",
    "cat3": "x2 == 2",
    "cont3": "x2 >= 0",
}

_MODES = ("binary", "cat3", "cont3")


def _motif_mode_from_key(key: str) -> tuple[str, str]:
    motif = "chain" if "chain" in key else "fork" if "fork" in key else "collider"
    if key.endswith("_binary"):
        mode = "binary"
    elif key.endswith("_cat3"):
        mode = "cat3"
    else:
        mode = "cont3"
    return motif, mode


def cell_meta_ql1(key: str, fx) -> dict:
    motif, mode = _motif_mode_from_key(key)
    edges, parents = MOTIF_INFO[motif]
    return {
        "fixture_id": key,
        "motif": motif,
        "data_mode": mode,
        "n_rows": len(fx.df),
        "graph_edges": edges,
        "expected_parents_x2": parents,
        "positive_class": POS_RULE[mode],
        "var_types": dict(fx.var_types),
    }


def cell_meta_ql3(key: str, fx) -> dict:
    base = key.rsplit("_", 1)[0]
    mode = key.rsplit("_", 1)[1]
    label, edges, parents = QL3_INFO[base]
    cfg_idx = list(QL3_INFO.keys()).index(base)
    seed = 20040002 + cfg_idx * 10 + _MODES.index(mode)
    return {
        "fixture_id": key,
        "structural_config": label,
        "data_mode": mode,
        "n_rows": len(fx.df),
        "graph_edges": edges,
        "expected_parents_x2": parents,
        "positive_class": POS_RULE[mode],
        "var_types": dict(fx.var_types),
        "rng_seed": seed,
    }


def write_cell(lines: list[str], ql_label: str, meta: dict, csv_text: str) -> None:
    lines.append(f"### {ql_label} — `{meta['fixture_id']}`")
    lines.append("")
    for k, v in meta.items():
        if k == "fixture_id":
            continue
        lines.append(f"- **{k}:** `{v}`")
    lines.append("")
    lines.append("```csv")
    lines.append(csv_text.rstrip("\n"))
    lines.append("```")
    lines.append("")


def main() -> None:
    lines: list[str] = []
    lines.append("# Appendix: full tabular data for QL1, QL2, and QL3")
    lines.append("")
    lines.append(
        "> **Provenance.** Every table below is the exact `x0,x1,x2` data fed to the ABA Learning"
    )
    lines.append(
        "> pipeline for that cell. Values are exported verbatim from the registered handcrafted"
    )
    lines.append(
        "> fixtures (`causal/experiments/handcrafted_qi001.py`, `handcrafted_qi002.py`,"
    )
    lines.append(
        "> `handcrafted_qi004.py`) via `HandcraftedFixture.df.to_csv(index=False)`, which matches"
    )
    lines.append(
        "> the per-cell `data.csv` files written at run time (cross-checked against on-disk"
    )
    lines.append("> artefacts for all cells that completed stage-1 data export).")
    lines.append("")
    lines.append(
        "> **Columns.** All tables have header `x0,x1,x2`. Row index is 1-based in the learner"
    )
    lines.append("> (`x2(1)` … `x2(n)`). Target variable `x2` is excluded from background knowledge.")
    lines.append("")
    lines.append(
        "> **Formatting note for LaTeX conversion.** Integer cells (binary, cat3) have no decimal"
    )
    lines.append("> points. Continuous (cont3) cells use full floating-point values as stored.")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## QL1 (QI-001): `QI001_motifs_modes` — 9 cells")
    lines.append("")
    lines.append(
        "3 motifs (chain, fork, collider) × 3 data modes (binary, categorical-3, continuous-3-bin)."
    )
    lines.append("Hand-picked small tables (4–5 rows); not complete factorials.")
    lines.append("")
    for i, key in enumerate(QL1_ORDER, 1):
        fx = load_handcrafted(key)
        write_cell(lines, f"QL1 cell {i}/9", cell_meta_ql1(key, fx), fx.df.to_csv(index=False))

    lines.append("---")
    lines.append("")
    lines.append("## QL2 (QI-002): `QI002_minimal_motifs` — 6 cells")
    lines.append("")
    lines.append("3 motifs × 2 data modes (binary, categorical-3). Complete factorial over `(x0,x1)`")
    lines.append("repeated ×2; noiseless deterministic targets.")
    lines.append("")
    for i, key in enumerate(QL2_ORDER, 1):
        fx = load_handcrafted(key)
        motif, mode = _motif_mode_from_key(key)
        edges, parents = MOTIF_INFO[motif]
        meta = {
            "fixture_id": key,
            "motif": motif,
            "data_mode": mode,
            "n_rows": len(fx.df),
            "graph_edges": edges,
            "expected_parents_x2": parents,
            "positive_class": POS_RULE[mode],
            "var_types": dict(fx.var_types),
        }
        write_cell(lines, f"QL2 cell {i}/6", meta, fx.df.to_csv(index=False))

    lines.append("---")
    lines.append("")
    lines.append("## QL3 (QI-004): `QI004_scaled_motifs_n20` — 15 cells")
    lines.append("")
    lines.append("5 structural configs × 3 data modes. `n = 20` per cell; mild stochastic noise;")
    lines.append(
        "deterministic per-fixture RNG seed (`_BASE_SEED = 20040002` in `handcrafted_qi004.py`)."
    )
    lines.append("")
    for i, key in enumerate(QL3_ORDER, 1):
        fx = load_handcrafted(key)
        write_cell(lines, f"QL3 cell {i}/15", cell_meta_ql3(key, fx), fx.df.to_csv(index=False))

    ql1_rows = sum(len(load_handcrafted(k).df) for k in QL1_ORDER)
    ql2_rows = sum(len(load_handcrafted(k).df) for k in QL2_ORDER)
    ql3_rows = sum(len(load_handcrafted(k).df) for k in QL3_ORDER)

    lines.append("---")
    lines.append("")
    lines.append("## Summary counts")
    lines.append("")
    lines.append("| Investigation | Experiment id | Cells | Total data rows |")
    lines.append("|---|---|---:|---:|")
    lines.append(f"| QL1 | QI001_motifs_modes | 9 | {ql1_rows} |")
    lines.append(f"| QL2 | QI002_minimal_motifs | 6 | {ql2_rows} |")
    lines.append(f"| QL3 | QI004_scaled_motifs_n20 | 15 | {ql3_rows} |")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Lines: {len(lines)}, bytes: {OUT.stat().st_size}")


if __name__ == "__main__":
    main()
