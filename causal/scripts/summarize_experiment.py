"""Summarise a grid experiment into a report-ready table and figure.

Reads ``grid/<experiment_id>/results.parquet`` and produces:

- ``<experiment_id>_summary.md`` : a markdown table (per DGP x target), annotated
  with whether the target truly has parents in the DGP, the dominant outcome,
  solve fraction across seeds, and median rule-body F1 on solved cells.
- ``<experiment_id>_summary.png`` : a two-panel figure
  (left: solve fraction heatmap; right: median body_parent_F1 heatmap).

The "has parents" annotation is the key interpretive lever for the interim
report: a *root* target (no parents) SHOULD yield no solution (correct
rejection), whereas a target *with* parents should be solved with a correct
rule body (F1 -> 1.0). Timeouts are flagged separately as search blow-ups.

Usage (from repo root, env with pandas/matplotlib, e.g. ``aba-env``):
    python -m causal.scripts.summarize_experiment --experiment E00_discrete_smoke
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from causal.experiments.dgp import get_dgp
from causal.experiments.paths import grid_root

_FIGURE_DIR = Path(__file__).resolve().parents[1] / "experiments" / "figures"

_OUTCOME_ORDER = ["solved", "completed_no_solution", "timeout", "error", "skipped"]


def _target_parents(dgp_id: str, target: str) -> tuple[str, ...] | None:
    """True parents of ``target`` in the DGP, or None if the DGP is unknown."""
    try:
        dgp = get_dgp(dgp_id)
    except KeyError:
        return None
    try:
        t_idx = int(target[1:])
    except (ValueError, IndexError):
        return None
    parents = sorted({f"x{s}" for (s, d) in dgp.edges if d == t_idx})
    return tuple(parents)


def _classify_cell(row: pd.Series, parents: tuple[str, ...] | None) -> str:
    """Interpretive label combining outcome and ground-truth role."""
    outcome = str(row["outcome"])
    if outcome == "timeout":
        return "timeout"
    if outcome == "error":
        return "error"
    has_parents = bool(parents)
    if outcome == "solved":
        return "solved"
    # completed_no_solution / skipped
    if not has_parents:
        return "correct_reject"  # root node -> no rule is the right answer
    return "miss"  # has parents but found nothing


def load_results(experiment_id: str) -> pd.DataFrame:
    path = grid_root() / experiment_id / "results.parquet"
    if not path.is_file():
        raise FileNotFoundError(f"No results.parquet for {experiment_id}: {path}")
    df = pd.read_parquet(path)
    if df.empty:
        raise ValueError(f"results.parquet for {experiment_id} is empty")
    return df


def build_cell_table(df: pd.DataFrame) -> pd.DataFrame:
    """One row per (dgp, target) aggregated across seeds."""
    rows: list[dict] = []
    for (dgp, target), grp in df.groupby(["dgp", "target"], sort=True):
        parents = _target_parents(str(dgp), str(target))
        labels = [_classify_cell(r, parents) for _, r in grp.iterrows()]
        n_seeds = len(grp)
        n_solved = sum(lbl == "solved" for lbl in labels)
        solved = grp[grp["outcome"] == "solved"]
        med_f1 = float(solved["body_parent_f1"].median()) if not solved.empty else np.nan
        rows.append(
            {
                "dgp": str(dgp),
                "target": str(target),
                "parents": ",".join(parents) if parents else "(none)",
                "is_root": parents is not None and len(parents) == 0,
                "n_seeds": n_seeds,
                "n_solved": n_solved,
                "solve_frac": n_solved / n_seeds if n_seeds else np.nan,
                "median_body_f1": med_f1,
                "n_timeout": sum(lbl == "timeout" for lbl in labels),
                "n_miss": sum(lbl == "miss" for lbl in labels),
                "n_correct_reject": sum(lbl == "correct_reject" for lbl in labels),
                "median_wall_s": float(grp["wall_clock_s"].median()),
            }
        )
    return pd.DataFrame(rows).sort_values(["dgp", "target"]).reset_index(drop=True)


def write_markdown(experiment_id: str, df: pd.DataFrame, table: pd.DataFrame) -> Path:
    out = _FIGURE_DIR / f"{experiment_id}_summary.md"
    counts = df["outcome"].value_counts().to_dict()
    total = int(len(df))
    n_solved = int(counts.get("solved", 0))

    # Headline numbers split by ground-truth role.
    with_parents = table[~table["is_root"]]
    roots = table[table["is_root"]]
    solve_rate_wp = (
        float(with_parents["n_solved"].sum() / with_parents["n_seeds"].sum())
        if not with_parents.empty and with_parents["n_seeds"].sum()
        else float("nan")
    )

    lines: list[str] = []
    lines.append(f"# {experiment_id} - results summary")
    lines.append("")
    lines.append(f"- Total cells: **{total}**")
    lines.append(
        "- Outcome counts: "
        + ", ".join(f"{k}={int(v)}" for k, v in sorted(counts.items()))
    )
    lines.append(f"- Overall solved: **{n_solved}/{total}** ({100*n_solved/total:.0f}%)")
    if not with_parents.empty:
        lines.append(
            "- Solve rate on targets **with true parents**: "
            f"**{100*solve_rate_wp:.0f}%** "
            f"({int(with_parents['n_solved'].sum())}/{int(with_parents['n_seeds'].sum())})"
        )
    if not roots.empty:
        cr = int(roots["n_correct_reject"].sum())
        rt = int(roots["n_seeds"].sum())
        lines.append(
            "- Root targets (no parents) correctly rejected (no spurious rule): "
            f"**{cr}/{rt}**"
        )
    lines.append("")
    lines.append(
        "| DGP | target | true parents | role | solved/seeds | median body-F1 | timeouts | median wall (s) |"
    )
    lines.append("|---|---|---|---|---|---|---|---|")
    for _, r in table.iterrows():
        role = "ROOT (expect none)" if r["is_root"] else "has parents"
        f1 = "-" if pd.isna(r["median_body_f1"]) else f"{r['median_body_f1']:.2f}"
        lines.append(
            f"| {r['dgp']} | {r['target']} | {r['parents']} | {role} | "
            f"{int(r['n_solved'])}/{int(r['n_seeds'])} | {f1} | "
            f"{int(r['n_timeout'])} | {r['median_wall_s']:.1f} |"
        )
    lines.append("")
    lines.append("## How to read this")
    lines.append("")
    lines.append(
        "- **Targets with parents** are the real learning task; solved + body-F1=1.00 "
        "means the learner recovered exactly the true parent set."
    )
    lines.append(
        "- **ROOT targets** have no parents, so `completed_no_solution` is the *correct* "
        "answer (the learner declines to invent a spurious rule)."
    )
    lines.append(
        "- **timeouts** are search blow-ups, not wrong answers; they should be ~0 in this "
        "small discrete regime."
    )
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def _pivot(table: pd.DataFrame, value: str) -> pd.DataFrame:
    return table.pivot(index="dgp", columns="target", values=value)


def make_figure(experiment_id: str, table: pd.DataFrame) -> Path:
    out = _FIGURE_DIR / f"{experiment_id}_summary.png"
    solve = _pivot(table, "solve_frac")
    f1 = _pivot(table, "median_body_f1")
    root = _pivot(table, "is_root")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), constrained_layout=True)

    def _heatmap(ax, data, title, cmap, vmin, vmax, fmt):
        arr = data.to_numpy(dtype=float)
        im = ax.imshow(arr, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")
        ax.set_xticks(range(len(data.columns)))
        ax.set_xticklabels(data.columns)
        ax.set_yticks(range(len(data.index)))
        ax.set_yticklabels(data.index)
        ax.set_title(title)
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                val = arr[i, j]
                is_root = bool(root.to_numpy()[i, j]) if root is not None else False
                if np.isnan(val):
                    txt = "root" if is_root else "-"
                else:
                    txt = fmt(val) + ("\n(root)" if is_root else "")
                ax.text(
                    j, i, txt, ha="center", va="center", fontsize=8,
                    color="black",
                )
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    _heatmap(
        axes[0], solve, "Solve fraction across seeds",
        "Greens", 0.0, 1.0, lambda v: f"{v:.2f}",
    )
    _heatmap(
        axes[1], f1, "Median rule-body F1 (solved cells)",
        "Blues", 0.0, 1.0, lambda v: f"{v:.2f}",
    )
    fig.suptitle(
        f"{experiment_id}: outcomes by DGP x target "
        "(root targets correctly have no rule)",
        fontsize=11,
    )
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Summarise a grid experiment for the report")
    p.add_argument("--experiment", required=True, help="experiment_id (grid dir name)")
    args = p.parse_args(argv)

    df = load_results(args.experiment)
    table = build_cell_table(df)
    md = write_markdown(args.experiment, df, table)
    fig = make_figure(args.experiment, table)
    print(f"wrote {md}")
    print(f"wrote {fig}")
    print()
    print(table.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
