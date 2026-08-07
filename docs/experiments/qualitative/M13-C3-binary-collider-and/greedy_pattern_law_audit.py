#!/usr/bin/env python3
"""Audit what a completed Greedy solution contains under the exact-value encoding.

Supports Finding 1 of the M13-C3 synthesis. For each target-wise `aamas2025`
cell, the positive rows induce a set of *value patterns*: one pattern per row,
listing every non-target column at its observed value. Two questions:

1. Does a solved Greedy delta consist of exactly those distinct positive
   patterns, one rule each, with no assumptions or contraries?

2. Does the solved / `completed_no_solution` split coincide with disjointness of
   the distinct positive and negative pattern sets?

A rule whose body is a full pattern is satisfied by exactly the rows carrying
that pattern, so it covers a negative example precisely when a negative row
shares the pattern. Question 2 tests that reading against every recorded cell.

Usage (from the repository root):

    python docs/experiments/qualitative/M13-C3-binary-collider-and/greedy_pattern_law_audit.py
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

TARGETWISE = Path("causal/outputs/aba_learning/targetwise")
RE_TARGET_RULE = re.compile(r"^(\w+)\(A\)\s*:-\s*(.+)\.$")


def value_patterns(table: list[dict], target: str, label: str) -> set[frozenset[str]]:
    columns = [c for c in table[0] if c != target]
    return {
        frozenset(f"{c}_val_{row[c]}" for c in columns)
        for row in table
        if row[target] == label
    }


def delta_bodies(path: Path, target: str) -> tuple[set[frozenset[str]], int]:
    """Return the target-rule bodies and the count of any other delta lines."""
    bodies: set[frozenset[str]] = set()
    other = 0
    if not path.exists():
        return bodies, other
    for line in path.read_text().split("\n"):
        line = line.strip()
        if not line:
            continue
        match = RE_TARGET_RULE.match(line)
        if match and match.group(1) == target:
            bodies.add(frozenset(x.strip().removesuffix("(A)") for x in match.group(2).split(",")))
        else:
            other += 1
    return bodies, other


def audit_cell(cell: Path) -> dict | None:
    data = cell / "input" / "data.csv"
    metrics = cell / "metrics.json"
    if not (data.exists() and metrics.exists()):
        return None
    target = cell.name.removeprefix("target-")
    with data.open() as handle:
        table = list(csv.DictReader(handle))
    if not table:
        return None
    columns = [c for c in table[0] if c != target]
    positives = value_patterns(table, target, "1")
    negatives = value_patterns(table, target, "0")
    bodies, other_lines = delta_bodies(cell / "output" / "delta.aba", target)
    return {
        "cell": str(cell.relative_to(TARGETWISE)),
        "target": target,
        "outcome": json.loads(metrics.read_text()).get("outcome"),
        "rows": len(table),
        "predictors": len(columns),
        "positive_patterns": len(positives),
        "negative_patterns": len(negatives),
        "shared_patterns": len(positives & negatives),
        "rules": len(bodies),
        "delta_is_positive_patterns": bodies == positives,
        # Vacuously true without rules, so report it as unavailable in that case.
        "every_body_cites_every_predictor":
            all(len(b) == len(columns) for b in bodies) if bodies else None,
        "other_delta_lines": other_lines,
    }


def main() -> int:
    if not TARGETWISE.is_dir():
        print(f"run from the repository root; {TARGETWISE} not found", file=sys.stderr)
        return 1

    results = [r for c in sorted(TARGETWISE.glob("*/aamas2025/*/cells/target-*"))
               if (r := audit_cell(c)) is not None]

    header = (f"{'cell':<48}{'outcome':<24}{'rows':>5}{'|P|':>5}{'|N|':>5}"
              f"{'shared':>7}{'rules':>6}{'delta=P':>9}{'allpred':>9}{'other':>6}")
    print(header)
    print("-" * len(header))
    for r in results:
        short = (r["cell"].replace("m13_bucket3_binary_", "")
                 .replace("/aamas2025", "").replace("/cells", ""))
        print(f"{short[:48]:<48}{str(r['outcome']):<24}{r['rows']:>5}"
              f"{r['positive_patterns']:>5}{r['negative_patterns']:>5}"
              f"{r['shared_patterns']:>7}{r['rules']:>6}"
              f"{str(r['delta_is_positive_patterns']):>9}"
              f"{('-' if r['every_body_cites_every_predictor'] is None
                  else str(r['every_body_cites_every_predictor'])):>9}"
              f"{r['other_delta_lines']:>6}")

    print(f"\ncells by outcome: {dict(Counter(r['outcome'] for r in results))}")
    solved = [r for r in results if r["outcome"] == "solved"]
    nosol = [r for r in results if r["outcome"] == "completed_no_solution"]
    print(f"\nsolved cells: {len(solved)}")
    print(f"  delta equals the distinct positive pattern set:   "
          f"{sum(r['delta_is_positive_patterns'] for r in solved)}/{len(solved)}")
    print(f"  every rule body cites every predictor column:     "
          f"{sum(r['every_body_cites_every_predictor'] for r in solved)}/{len(solved)}")
    print(f"  deltas containing an assumption or contrary line: "
          f"{sum(r['other_delta_lines'] > 0 for r in solved)}/{len(solved)}")
    print(f"  positive and negative pattern sets disjoint:      "
          f"{sum(r['shared_patterns'] == 0 for r in solved)}/{len(solved)}")
    print(f"\ncompleted_no_solution cells: {len(nosol)}")
    print(f"  sharing at least one pattern between labels:      "
          f"{sum(r['shared_patterns'] > 0 for r in nosol)}/{len(nosol)}")
    skipped = [r for r in results if r["outcome"] not in ("solved", "completed_no_solution")]
    for r in skipped:
        print(f"\n{r['outcome']}: {r['cell']} "
              f"(rows={r['rows']}, negative patterns={r['negative_patterns']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
