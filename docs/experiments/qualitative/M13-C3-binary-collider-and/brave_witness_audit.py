#!/usr/bin/env python3
"""Count the stable extensions of a learned framework and locate its free choices.

Supports Finding 3 of the M13-C3 synthesis. A cell's `output/asp.clingo` holds the
learned framework together with one integrity constraint per example. This script
separates the two parts and asks clingo three questions per solved nd cell:

1. How many stable extensions does the framework alone admit?
2. How many survive the example constraints?
3. At which rows does the framework leave the target undetermined, meaning the
   target holds in some extension and fails in another?

These are compared against the *conflicted rows* of the input table: rows sharing a
complete predictor value pattern with a row carrying the opposite label. A target
that is a deterministic function of its predictors has none.

Requires `clingo` on PATH. Reads existing artefacts only and runs no learner.

Usage (from the repository root):

    python docs/experiments/qualitative/M13-C3-binary-collider-and/brave_witness_audit.py
"""

from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from pathlib import Path

TARGETWISE = Path("causal/outputs/aba_learning/targetwise")
RE_MODELS = re.compile(r"Models\s*:\s*(\d+)\+?")

# A framework can carry free choices beyond the conflicted rows, so the number of
# extensions is not bounded by the conflict count alone. Counting is attempted
# under a wall-clock limit and reported as unavailable when it is not reached.
CLINGO_TIMEOUT_S = 30
RE_ND = re.compile(r"^lopt\(folding_mode\(nd\)\)\.", re.M)
RE_EXAMPLE_CONSTRAINT = re.compile(r"^\s*:-\s*(not\s+)?\w+\(\d+\)\s*\.\s*$")
EFFECTIVE_OPTIONS_BANNER = "Current learning options:"


def ran_under_nd(stdout: Path) -> bool:
    _, _, effective = stdout.read_text().partition(EFFECTIVE_OPTIONS_BANNER)
    return bool(RE_ND.search(effective))


def split_program(asp: Path) -> tuple[str, str]:
    """Return (framework without any constraint, the example constraints)."""
    framework, examples = [], []
    for line in asp.read_text().split("\n"):
        if RE_EXAMPLE_CONSTRAINT.match(line):
            examples.append(line)
        elif line.strip().startswith(":-"):
            continue  # other integrity constraints, excluded from both parts
        else:
            framework.append(line)
    return "\n".join(framework), "\n".join(examples)


def clingo(program: str, extra_args: list[str] | None = None) -> str | None:
    """Run clingo on stdin, returning None if it does not finish in time."""
    try:
        result = subprocess.run(["clingo", "0", "-", *(extra_args or [])],
                                input=program, capture_output=True, text=True,
                                timeout=CLINGO_TIMEOUT_S)
    except subprocess.TimeoutExpired:
        return None
    return result.stdout


def count_models(program: str) -> int | None:
    output = clingo(program, ["-q"])
    if output is None:
        return None
    match = RE_MODELS.search(output)
    return int(match.group(1)) if match else None


def consequences(program: str, target: str, mode: str) -> set[int] | None:
    output = clingo(program, [f"--enum-mode={mode}"])
    if output is None:
        return None
    pattern = re.compile(rf"(?:^|\s){re.escape(target)}\((\d+)\)")
    atoms: set[int] = set()
    for line in output.split("\n"):
        if line and not line.startswith(("Answer", "clingo", "Reading", "Solving")):
            atoms |= {int(m) for m in pattern.findall(line)}
    return atoms


def conflicted_rows(table: list[dict], target: str) -> list[int]:
    """Rows whose full predictor pattern also occurs with the opposite label."""
    columns = [c for c in table[0] if c != target]
    groups: dict[tuple, list[tuple[int, str]]] = {}
    for index, row in enumerate(table, 1):
        groups.setdefault(tuple(row[c] for c in columns), []).append((index, row[target]))
    return sorted(index for group in groups.values()
                  if len({label for _, label in group}) > 1
                  for index, _ in group)


def audit_cell(cell: Path) -> dict | None:
    metrics, asp = cell / "metrics.json", cell / "output" / "asp.clingo"
    stdout, data = cell / "output" / "prolog.stdout", cell / "input" / "data.csv"
    if not all(p.exists() for p in (metrics, asp, stdout, data)):
        return None
    if json.loads(metrics.read_text()).get("outcome") != "solved":
        return None
    if not ran_under_nd(stdout):
        return None

    target = cell.name.removeprefix("target-")
    framework, examples = split_program(asp)
    with data.open() as handle:
        table = list(csv.DictReader(handle))

    conflicted = conflicted_rows(table, target)
    can_hold = consequences(framework, target, "brave")
    must_hold = consequences(framework, target, "cautious")
    undetermined = (None if can_hold is None or must_hold is None
                    else sorted(can_hold - must_hold))
    free_extensions = count_models(framework)
    with_examples = count_models(framework + "\n" + examples)

    return {
        "cell": str(cell.relative_to(TARGETWISE)),
        "target": target,
        "conflicted_rows": len(conflicted),
        "framework_extensions": free_extensions,
        "extensions_with_examples": with_examples,
        "undetermined_rows": None if undetermined is None else len(undetermined),
        "undetermined_equals_conflicted":
            None if undetermined is None else undetermined == conflicted,
        "extensions_equal_two_to_the_conflicted":
            None if free_extensions is None else free_extensions == 2 ** len(conflicted),
    }


def main() -> int:
    if not TARGETWISE.is_dir():
        print(f"run from the repository root; {TARGETWISE} not found", file=sys.stderr)
        return 1
    if subprocess.run(["which", "clingo"], capture_output=True).returncode != 0:
        print("clingo not found on PATH", file=sys.stderr)
        return 1

    results = [r for cell in sorted(TARGETWISE.glob("*/*/*/cells/target-*"))
               if (r := audit_cell(cell)) is not None]

    header = (f"{'cell':<56}{'conflicted':>11}{'extensions':>11}{'2^k?':>6}"
              f"{'undet':>7}{'undet=confl':>12}{'with examples':>14}")
    print(header)
    print("-" * len(header))
    dash = lambda v: "-" if v is None else str(v)
    for r in results:
        short = (r["cell"].replace("m13_bucket3_binary_", "")
                 .replace("/cells", "").replace("_seed42", ""))
        print(f"{short[:56]:<56}{r['conflicted_rows']:>11}"
              f"{dash(r['framework_extensions']):>11}"
              f"{dash(r['extensions_equal_two_to_the_conflicted']):>6}"
              f"{dash(r['undetermined_rows']):>7}"
              f"{dash(r['undetermined_equals_conflicted']):>12}"
              f"{dash(r['extensions_with_examples']):>14}")

    n = len(results)
    located = [r for r in results if r["undetermined_equals_conflicted"] is not None]
    counted = [r for r in results if r["framework_extensions"] is not None]
    print(f"\nsolved nd cells audited: {n}   (clingo timeout "
          f"{CLINGO_TIMEOUT_S}s per query, '-' means not reached)")
    print(f"\ncells where the undetermined rows were located: {len(located)}")
    print(f"  they are exactly the conflicted rows:                   "
          f"{sum(bool(r['undetermined_equals_conflicted']) for r in located)}/{len(located)}")
    print(f"\ncells where the extensions were counted: {len(counted)}")
    print(f"  framework extensions == 2^(conflicted rows):            "
          f"{sum(bool(r['extensions_equal_two_to_the_conflicted']) for r in counted)}"
          f"/{len(counted)}")
    print(f"  exactly one extension survives the example constraints: "
          f"{sum(r['extensions_with_examples'] == 1 for r in counted)}/{len(counted)}")
    print(f"\ncells whose target is not a function of its predictors: "
          f"{sum(r['conflicted_rows'] > 0 for r in results)}/{n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
