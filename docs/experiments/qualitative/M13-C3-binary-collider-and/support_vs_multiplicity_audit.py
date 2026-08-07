#!/usr/bin/env python3
"""Audit what changes in a cautious-nd trace when only row multiplicities grow.

Supports Finding 5 of the M13-C3 synthesis. H6b enlarges the H0 sample through
nested seed-42 prefixes n = 30, 60, 90 at fixed `folding_steps(2)`. All four
population atoms are already present at n = 30, so the prefixes change
multiplicities without adding joint value patterns. Two questions:

1. Decision identity. Is the ordered sequence of learner decisions the same at
   every n? Decisions are the `gen1`..`gen6` steps, folding results, assumption
   introductions, entailment checks, and token increases, compared after
   normalising Prolog variable numbers and row identifiers.

2. Where cost goes. Grouping trace lines into categories under the same
   normalisation, which categories hold a constant number of lines across n, and
   which grow?

Usage (from the repository root):

    python docs/experiments/qualitative/M13-C3-binary-collider-and/support_vs_multiplicity_audit.py
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

COLLECTION = Path(
    "causal/outputs/aba_learning/targetwise/"
    "m13_bucket3_binary_collider_and/baseline_cautious_steps2"
)
SAMPLE_SIZES = (30, 60, 90)
TARGETS = ("a", "b", "c")

# Lines recording a learner decision, as opposed to per-row bookkeeping.
RE_DECISION = re.compile(
    r"^(gen\d:"
    r"|\s*folding result:"
    r"|\s*found:"
    r"|\s*generating NEW assumption:"
    r"|checking entailment"
    r"|\* Increasing folding tokens"
    r"|\* No solution found)"
)


def trace_lines(n: int, target: str) -> list[str]:
    path = COLLECTION / f"n{n}_seed42" / "cells" / f"target-{target}" / "output" / "prolog.stdout"
    lines = path.read_text(errors="replace").split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def category(line: str) -> str:
    """Collapse a trace line to its category by removing run-specific detail."""
    text = re.sub(r"\s+", " ", line).strip()
    text = re.sub(r"_\d+", "_N", text)      # alpha_1 / _7934 -> alpha_N / _N
    text = re.sub(r"\bA=\d+\b", "A=_", text)  # row identifier in a rule body
    return re.sub(r"\b\d+\b", "#", text)      # any remaining literal number


def decision_sequence(n: int, target: str) -> list[str]:
    return [category(l) for l in trace_lines(n, target) if RE_DECISION.match(l)]


def category_counts(n: int, target: str) -> Counter:
    return Counter(category(l) for l in trace_lines(n, target))


def main() -> int:
    if not COLLECTION.is_dir():
        print(f"run from the repository root; {COLLECTION} not found", file=sys.stderr)
        return 1

    print("Decision-sequence identity across nested sample sizes")
    print(f"{'target':>7} {'decisions':>28} {'identical':>10}")
    for target in TARGETS:
        seqs = {n: decision_sequence(n, target) for n in SAMPLE_SIZES}
        lengths = [len(seqs[n]) for n in SAMPLE_SIZES]
        identical = len({tuple(s) for s in seqs.values()}) == 1
        print(f"{target:>7} {str(lengths):>28} {('yes' if identical else 'NO'):>10}")

    for target in TARGETS:
        counts = {n: category_counts(n, target) for n in SAMPLE_SIZES}
        keys = set().union(*(set(c) for c in counts.values()))
        constant, growing = [], []
        for key in keys:
            per_n = tuple(counts[n][key] for n in SAMPLE_SIZES)
            (constant if len(set(per_n)) == 1 else growing).append((per_n, key))

        print(f"\nTarget {target}: total trace lines "
              f"{[len(trace_lines(n, target)) for n in SAMPLE_SIZES]}")
        print(f"  constant categories: {len(constant):>3}, holding "
              f"{[sum(v[i] for v, _ in constant) for i in range(3)]} lines")
        print(f"  growing categories:  {len(growing):>3}, holding "
              f"{[sum(v[i] for v, _ in growing) for i in range(3)]} lines")
        for per_n, key in sorted(growing, key=lambda item: -item[0][-1]):
            print(f"    {str(list(per_n)):>18}  {key[:70]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
