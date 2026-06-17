"""Generate appendix-ql3.tex: QL1 + QL2 + QL3 tabular data.

Report-label mapping (settled): QL1 = QI-001, QL2 = QI-002, QL3 = QI-004 (the feasible
n=20 scaled study). The earlier n=100 attempt (QI-003) was cut as infeasible and carries
no report label, so it does not appear in this appendix.
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from causal.experiments.handcrafted import load_handcrafted
from causal.experiments.handcrafted_qi004 import QI004_BUILDERS

OUT = _REPO.parent / "appendix-ql3.tex"

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

POS_RULE = {"binary": r"$x_2 = 1$", "cat3": r"$x_2 = 2$", "cont3": r"$x_2 \geq 0$"}
_MODES = ("binary", "cat3", "cont3")
_QL3_BASE_SEED = 20040002


def _motif_mode(key: str) -> tuple[str, str]:
    motif = "chain" if "chain" in key else "fork" if "fork" in key else "collider"
    if key.endswith("_binary"):
        mode = "binary"
    elif key.endswith("_cat3"):
        mode = "cat3"
    else:
        mode = "cont3"
    return motif, mode


def _tex_escape(s: str) -> str:
    return (
        s.replace("\\", "\\textbackslash{}")
        .replace("_", "\\_")
        .replace("&", "\\&")
        .replace("%", "\\%")
    )


def _fmt_val(v: float) -> str:
    x = float(v)
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    return f"{x:.3f}"


def _meta_lines_ql1_ql2(key: str, fx) -> list[str]:
    motif, mode = _motif_mode(key)
    edges, parents = MOTIF_INFO[motif]
    return [
        f"\\textbf{{Motif:}} {motif}; "
        f"\\textbf{{Mode:}} {mode}; "
        f"\\textbf{{Rows:}} {len(fx.df)}; "
        f"\\textbf{{Edges:}} \\texttt{{{_tex_escape(edges)}}}; "
        f"\\textbf{{Parents($x_2$):}} \\texttt{{{_tex_escape(parents)}}}; "
        f"\\textbf{{Positive:}} {POS_RULE[mode]}.",
    ]


def _meta_lines_ql3(key: str, fx) -> list[str]:
    base = key.rsplit("_", 1)[0]
    mode = key.rsplit("_", 1)[1]
    label, edges, parents = QL3_INFO[base]
    cfg_idx = list(QL3_INFO.keys()).index(base)
    seed = _QL3_BASE_SEED + cfg_idx * 10 + _MODES.index(mode)
    return [
        f"\\textbf{{Config:}} {label}; "
        f"\\textbf{{Mode:}} {mode}; "
        f"\\textbf{{Rows:}} {len(fx.df)}; "
        f"\\textbf{{Edges:}} \\texttt{{{_tex_escape(edges)}}}; "
        f"\\textbf{{Parents($x_2$):}} \\texttt{{{_tex_escape(parents)}}}; "
        f"\\textbf{{Positive:}} {POS_RULE[mode]}; "
        f"\\textbf{{RNG seed:}} {seed}.",
    ]


def _longtable(key: str, fx, label_prefix: str) -> list[str]:
    label = f"app:{label_prefix}:{key.replace('_', ':')}"
    lines = [
        "\\begin{longtable}{rrrr}",
        f"\\caption{{Tabular input for \\texttt{{{_tex_escape(key)}}}.}} "
        f"\\label{{{label}}} \\\\",
        "\\toprule",
        "$id$ & $x_0$ & $x_1$ & $x_2$ \\\\",
        "\\midrule",
        "\\endfirsthead",
        "\\multicolumn{4}{c}{{\\tablename\\ \\thetable{} -- continued from previous page}} \\\\",
        "\\toprule",
        "$id$ & $x_0$ & $x_1$ & $x_2$ \\\\",
        "\\midrule",
        "\\endhead",
        "\\midrule",
        "\\multicolumn{4}{r}{{Continued on next page}} \\\\",
        "\\endfoot",
        "\\bottomrule",
        "\\endlastfoot",
    ]
    for i, row in fx.df.iterrows():
        rid = i + 1
        x0, x1, x2 = (_fmt_val(row["x0"]), _fmt_val(row["x1"]), _fmt_val(row["x2"]))
        lines.append(f"{rid} & {x0} & {x1} & {x2} \\\\")
    lines.append("\\end{longtable}")
    lines.append("")
    return lines


def main() -> None:
    ql1_rows = sum(len(load_handcrafted(k).df) for k in QL1_ORDER)
    ql2_rows = sum(len(load_handcrafted(k).df) for k in QL2_ORDER)
    ql3_rows = sum(len(load_handcrafted(k).df) for k in QL3_ORDER)

    lines: list[str] = [
        "% appendix-ql3.tex — tabular input data for QL1, QL2, QL3",
        "% Requires in main.tex:",
        "%   \\usepackage{booktabs,longtable,geometry}",
        "% Include with: \\input{appendix-ql3}",
        "",
        "\\section{Tabular data for QL1, QL2, and QL3}",
        "\\label{app:tabular-data}",
        "",
        "{\\footnotesize",
        "This appendix lists the exact $(x_0, x_1, x_2)$ tables fed to the ABA Learning",
        "pipeline for each qualitative cell. Values are exported from the registered",
        "handcrafted fixtures (\\texttt{handcrafted\\_qi001.py}, \\texttt{handcrafted\\_qi002.py},",
        "\\texttt{handcrafted\\_qi004.py}) and match the per-cell \\texttt{data.csv} files",
        "written at run time. Row \\emph{id} is 1-based (learner atoms \\texttt{x2(1)}\\ldots\\texttt{x2(n)}).",
        "Target~$x_2$ is excluded from background knowledge. Continuous values are rounded",
        "to three decimal places in this appendix; integer binary/categorical cells are shown",
        "without decimals. QL3 (repo id QI-004) uses these structural configs at $n=20$; the",
        "earlier $n=100$ attempt (QI-003) was cut as computationally infeasible and carries no",
        "report label.",
        "",
        "\\begin{table}[htbp]",
        "\\centering",
        "\\caption{Summary of appendix tabular data.}",
        "\\label{app:tabular-summary}",
        "\\begin{tabular}{@{}llrr@{}}",
        "\\toprule",
        "Investigation & Experiment id & Cells & Total rows \\\\",
        "\\midrule",
        f"QL1 & \\texttt{{QI001\\_motifs\\_modes}} & 9 & {ql1_rows} \\\\",
        f"QL2 & \\texttt{{QI002\\_minimal\\_motifs}} & 6 & {ql2_rows} \\\\",
        f"QL3 & \\texttt{{QI004\\_scaled\\_motifs\\_n20}} & 15 & {ql3_rows} \\\\",
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{table}",
        "",
        "\\scriptsize",
        "\\setlength{\\tabcolsep}{3pt}",
        "\\renewcommand{\\arraystretch}{0.85}",
        "",
        "\\subsection{QL1 (QI-001): \\texttt{QI001\\_motifs\\_modes}}",
        "\\label{app:ql1}",
        "Nine cells: three motifs $\\times$ three data modes (binary, categorical-3, continuous-3-bin).",
        "Hand-picked small tables (4--5 rows).",
        "",
    ]

    for i, key in enumerate(QL1_ORDER, 1):
        fx = load_handcrafted(key)
        lines.append(f"\\subsubsection{{QL1 cell {i}/9: \\texttt{{{_tex_escape(key)}}}}}")
        lines.append(f"\\label{{app:ql1:{key.replace('_', '-')}}}")
        lines.extend(_meta_lines_ql1_ql2(key, fx))
        lines.append("")
        lines.extend(_longtable(key, fx, "ql1"))

    lines.extend(
        [
            "\\subsection{QL2 (QI-002): \\texttt{QI002\\_minimal\\_motifs}}",
            "\\label{app:ql2}",
            "Six cells: three motifs $\\times$ two data modes (binary, categorical-3).",
            "Complete factorial over $(x_0, x_1)$ repeated $\\times 2$; noiseless targets.",
            "",
        ]
    )

    for i, key in enumerate(QL2_ORDER, 1):
        fx = load_handcrafted(key)
        lines.append(f"\\subsubsection{{QL2 cell {i}/6: \\texttt{{{_tex_escape(key)}}}}}")
        lines.append(f"\\label{{app:ql2:{key.replace('_', '-')}}}")
        lines.extend(_meta_lines_ql1_ql2(key, fx))
        lines.append("")
        lines.extend(_longtable(key, fx, "ql2"))

    lines.extend(
        [
            "\\subsection{QL3 (QI-004): \\texttt{QI004\\_scaled\\_motifs\\_n20}}",
            "\\label{app:ql3}",
            "Fifteen cells: five structural configs $\\times$ three data modes.",
            "$n = 20$ per cell; mild stochastic noise; deterministic per-fixture RNG seed",
            f"(\\texttt{{\\_BASE\\_SEED = {_QL3_BASE_SEED}}}).",
            "",
        ]
    )

    for i, key in enumerate(QL3_ORDER, 1):
        fx = load_handcrafted(key)
        lines.append(f"\\subsubsection{{QL3 cell {i}/15: \\texttt{{{_tex_escape(key)}}}}}")
        lines.append(f"\\label{{app:ql3:{key.replace('_', '-')}}}")
        lines.extend(_meta_lines_ql3(key, fx))
        lines.append("")
        lines.extend(_longtable(key, fx, "ql3"))

    lines.extend(["}", "}", ""])

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes, {len(lines)} lines)")


if __name__ == "__main__":
    main()
