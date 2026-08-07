#!/usr/bin/env python3
"""Audit which observed variables appear in the target rules of a solved nd delta.

Supports Finding 2 of the M13-C3 synthesis. Target-specific background knowledge
serialises one predictor block per non-target column, in column order. For every
solved cell run under `folding_mode(nd)`, this script compares the observed
variables cited by the *ordinary target rules* of `delta.aba` against that BK
order, and separately records the variables that appear only inside contrary
definitions.

Checks reported:

1. Do the target rules cite exactly the first BK predictor and no later one?
2. Does each target rule carry exactly one observed value literal?
3. Does the number of target rules equal the number of values the first BK
   predictor takes among the positive rows, and do the cited values match?

Usage (from the repository root):

    python docs/experiments/qualitative/M13-C3-binary-collider-and/nd_first_predictor_audit.py
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

TARGETWISE = Path("causal/outputs/aba_learning/targetwise")
RE_PREDICTOR_BLOCK = re.compile(r"% Predictor block: (\w+)")
RE_RULE = re.compile(r"^([a-z]\w*)\(A\)\s*:-\s*(.+)\.$")
RE_VALUE_LITERAL = re.compile(r"^([a-z]\w*)_val_(\w+)$")
RE_ND = re.compile(r"^lopt\(folding_mode\(nd\)\)\.", re.M)

# Every trace opens with a dump of the default options, which include
# folding_mode(nd) even for a Greedy run. Only the block after this banner
# reports the options the run actually used.
EFFECTIVE_OPTIONS_BANNER = "Current learning options:"


def ran_under_nd(stdout: Path) -> bool:
    _, _, effective = stdout.read_text().partition(EFFECTIVE_OPTIONS_BANNER)
    return bool(RE_ND.search(effective))


def parse_delta(path: Path, target: str) -> tuple[list[dict], set[str]]:
    """Return (target rules as {variable: value}, variables seen only in contraries)."""
    target_rules: list[dict] = []
    contrary_variables: set[str] = set()
    for line in path.read_text().split("\n"):
        line = line.strip()
        if not line or line.startswith(("assumption(", "contrary(")):
            continue
        match = RE_RULE.match(line)
        if not match:
            continue
        head = match.group(1)
        body = [x.strip().removesuffix("(A)") for x in match.group(2).split(",")]
        observed = {m.group(1): m.group(2)
                    for m in (RE_VALUE_LITERAL.match(b) for b in body) if m}
        if head == target:
            target_rules.append(observed)
        else:
            contrary_variables |= set(observed)
    return target_rules, contrary_variables


def audit_cell(cell: Path) -> dict | None:
    metrics, bk = cell / "metrics.json", cell / "input" / "bk.aba"
    delta, stdout = cell / "output" / "delta.aba", cell / "output" / "prolog.stdout"
    if not (metrics.exists() and bk.exists() and delta.exists() and stdout.exists()):
        return None
    if json.loads(metrics.read_text()).get("outcome") != "solved":
        return None
    if not ran_under_nd(stdout):
        return None

    target = cell.name.removeprefix("target-")
    order = RE_PREDICTOR_BLOCK.findall(bk.read_text())
    if not order:
        return None
    first = order[0]
    target_rules, contrary_variables = parse_delta(delta, target)
    cited_variables = set().union(*[set(r) for r in target_rules]) if target_rules else set()
    cited_values = {r[first] for r in target_rules if first in r}

    with (cell / "input" / "data.csv").open() as handle:
        table = list(csv.DictReader(handle))
    positive_values = {row[first] for row in table if row[target] == "1"}

    return {
        "cell": str(cell.relative_to(TARGETWISE)),
        "target": target,
        "bk_order": order,
        "first": first,
        "target_rules": len(target_rules),
        "cited_variables": sorted(cited_variables),
        "contrary_variables": sorted(contrary_variables),
        "cited_values": sorted(cited_values),
        "positive_values_of_first": sorted(positive_values),
        "cites_only_first": cited_variables == {first},
        "one_value_literal_per_rule": all(len(r) == 1 for r in target_rules),
        "values_match_positive_rows": cited_values == positive_values,
        "rule_count_matches_values": len(target_rules) == len(positive_values),
    }


def main() -> int:
    if not TARGETWISE.is_dir():
        print(f"run from the repository root; {TARGETWISE} not found", file=sys.stderr)
        return 1

    results = [r for cell in sorted(TARGETWISE.glob("*/*/*/cells/target-*"))
               if (r := audit_cell(cell)) is not None]
    if not results:
        print("no solved nd cells found", file=sys.stderr)
        return 1

    header = (f"{'cell':<58}{'BK order':<12}{'rules':>6}{'cited':<8}{'values':<8}"
              f"{'only 1st':>9}{'1 lit':>6}{'vals=pos':>9}  {'in contraries':<14}")
    print(header)
    print("-" * len(header))
    for r in results:
        short = (r["cell"].replace("m13_bucket3_binary_", "")
                 .replace("/cells", "").replace("_seed42", ""))
        print(f"{short[:58]:<58}{','.join(r['bk_order'])[:12]:<12}{r['target_rules']:>6}"
              f"{','.join(r['cited_variables']):<8}{','.join(r['cited_values']):<8}"
              f"{str(r['cites_only_first']):>9}{str(r['one_value_literal_per_rule']):>6}"
              f"{str(r['values_match_positive_rows']):>9}  "
              f"{','.join(r['contrary_variables']):<14}")

    n = len(results)
    print(f"\nsolved nd cells audited: {n}")
    print(f"  target rules cite exactly the first BK predictor:  "
          f"{sum(r['cites_only_first'] for r in results)}/{n}")
    print(f"  exactly one observed value literal per rule:       "
          f"{sum(r['one_value_literal_per_rule'] for r in results)}/{n}")
    print(f"  cited values == values of first among positives:   "
          f"{sum(r['values_match_positive_rows'] for r in results)}/{n}")
    print(f"  rule count == that number of values:              "
          f"{sum(r['rule_count_matches_values'] for r in results)}/{n}")
    print(f"  target-rule count distribution: "
          f"{dict(Counter(r['target_rules'] for r in results))}")
    both = [r for r in results if len(r["cited_values"]) > 1]
    print(f"  cells whose target rules cover every observed value of the first\n"
          f"    predictor, and so constrain it not at all: {len(both)}/{n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
