#!/usr/bin/env python3
"""Audit the nd folding-token ladder in target-wise ABALearn traces.

Supports Finding 4 of the M13-C3 five-findings synthesis. Two questions:

1. Token saturation. Does any nd folding call ever consume more than one
   folding token? `fold_nd_wtc/7` prints ` C: folding ...` before each step and
   ` C: DONE` on completion, so a call that consumed exactly one token prints
   `folding` at the current allowance T and `DONE` at T-1. A call that
   exhausted the allowance prints ` 0: FAIL - No more folding tokens left`.

2. Band replay. `genT/6` raises `tokens(T)` and restarts the whole search while
   T+1 =< M, printing `* Increasing folding tokens to: T+1`. Splitting a trace
   at those lines yields one band per permitted token. A trace of M bands is
   a fixed preamble, M search attempts separated by the M-1 restart lines, and
   the closing `* No solution found!` line. Attempts are compared after
   normalising away the three things that must differ between restarts:
   generated assumption indices (`alpha_N`), Prolog internal variable numbers
   (`_N`), and the printed token counter. The attempt block is located by the
   longest suffix of band 1 that matches the head of band 2, which fixes the
   preamble and closing lengths without assuming them.

Usage (from the repository root):

    python docs/experiments/qualitative/M13-C3-binary-collider-and/band_replay_audit.py
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

TARGETWISE = Path("causal/outputs/aba_learning/targetwise")

RE_INCREASE = re.compile(r"^\* Increasing folding tokens to: (\d+)")
RE_FOLD = re.compile(r"^\s*(\d+): folding (.*?) with ", re.M)
RE_DONE = re.compile(r"^\s*(\d+): DONE", re.M)
RE_FAIL = re.compile(r"^\s*(\d+): FAIL - No more folding tokens", re.M)
RE_ND = re.compile(r"^lopt\(folding_mode\(nd\)\)\.", re.M)

# Every trace opens with a dump of the default options (which include
# folding_mode(nd)) before the configuration is applied. Only the block after
# this banner reports the options the run actually used.
EFFECTIVE_OPTIONS_BANNER = "Current learning options:"


def normalise_line(line: str) -> str:
    line = re.sub(r"alpha_\d+", "alpha_#", line)
    line = re.sub(r"_\d+", "_V", line)
    line = re.sub(r"^\s*\d+: ", " T: ", line)
    return re.sub(r"^\* Increasing folding tokens to: \d+$", "* INC", line)


def normalise(band: list[str]) -> str:
    out = [normalise_line(line) for line in band]
    return hashlib.sha256("\n".join(out).encode()).hexdigest()


def split_bands(lines: list[str]) -> list[list[str]]:
    cuts = [i for i, l in enumerate(lines) if RE_INCREASE.match(l)]
    edges = [0] + cuts + [len(lines)]
    return [lines[edges[i] : edges[i + 1]] for i in range(len(edges) - 1)]


def compare_attempts(bands: list[list[str]]) -> dict:
    """Check that every search attempt in a multi-band trace is identical.

    Bands 2..M each open with the restart line. Band 1 opens with the run
    preamble and the final band ends with the closing line, so the attempt
    block is recovered as the longest suffix of band 1 that matches the head of
    band 2. Returns the attempt length, the preamble and closing lengths, and
    whether all M attempts agree.
    """
    norm = [[normalise_line(line) for line in band] for band in bands]
    first, second = norm[0], norm[1]
    attempt_len = 0
    for cand in range(min(len(first), len(second) - 1), 0, -1):
        if first[-cand:] == second[1 : 1 + cand]:
            attempt_len = cand
            break
    if attempt_len == 0:
        return {"attempt_lines": 0, "attempts_identical": False}
    reference = second[1 : 1 + attempt_len]
    identical = all(
        band[1 : 1 + attempt_len] == reference and len(band) == attempt_len + 1
        for band in norm[1:-1]
    ) and norm[-1][1 : 1 + attempt_len] == reference
    return {
        "attempt_lines": attempt_len,
        "preamble_lines": len(first) - attempt_len,
        "closing_lines": len(norm[-1]) - 1 - attempt_len,
        "attempts_identical": identical,
    }


def audit(path: Path) -> dict | None:
    text = path.read_text(errors="replace")
    _, _, effective = text.partition(EFFECTIVE_OPTIONS_BANNER)
    if not RE_ND.search(effective):
        return None
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()  # some traces end with a newline, some do not
    bands = split_bands(lines)
    result = {
        "path": str(path.relative_to(TARGETWISE)),
        "lines": len(lines),
        "bands": len(bands),
        "band_lengths": [len(b) for b in bands],
        "band_hashes": [normalise(b) for b in bands],
        "fold_counters": sorted({int(c) for c, _ in RE_FOLD.findall(text)}),
        "done_counters": sorted({int(c) for c in RE_DONE.findall(text)}),
        "token_exhaustion_failures": len(RE_FAIL.findall(text)),
        "multi_atom_fold_lists": sum(1 for _, b in RE_FOLD.findall(text) if "," in b),
    }
    if len(bands) > 1:
        result.update(compare_attempts(bands))
    return result


def main() -> int:
    if not TARGETWISE.is_dir():
        print(f"run from the repository root; {TARGETWISE} not found", file=sys.stderr)
        return 1

    results = []
    for path in sorted(TARGETWISE.glob("**/prolog.stdout")):
        r = audit(path)
        if r is not None:
            results.append(r)

    print(f"nd traces audited: {len(results)}\n")
    hdr = (f"{'trace':70s} {'lines':>6} {'bands':>5} {'attempt':>7} {'pre':>4} "
           f"{'close':>5} {'same':>5} {'fold@':>10} {'done@':>10} {'FAIL':>5} {'multi':>5}")
    print(hdr)
    print("-" * len(hdr))
    for r in results:
        fold = f"{min(r['fold_counters'])}..{max(r['fold_counters'])}" if r["fold_counters"] else "-"
        done = f"{min(r['done_counters'])}..{max(r['done_counters'])}" if r["done_counters"] else "-"
        multi = r["bands"] > 1
        print(
            f"{r['path'][:70]:70s} {r['lines']:6d} {r['bands']:5d} "
            f"{(r['attempt_lines'] if multi else 0):7d} "
            f"{(r.get('preamble_lines', 0)):4d} {(r.get('closing_lines', 0)):5d} "
            f"{(('yes' if r['attempts_identical'] else 'NO') if multi else '-'):>5} "
            f"{fold:>10} {done:>10} {r['token_exhaustion_failures']:5d} "
            f"{r['multi_atom_fold_lists']:5d}"
        )

    print()
    saturated = all(
        r["done_counters"] == [c - 1 for c in r["fold_counters"]]
        for r in results
        if r["fold_counters"]
    )
    multi = [r for r in results if r["bands"] > 1]
    print(f"every folding call consumed exactly one token: {saturated}")
    print(f"total token-exhaustion failures across all nd traces: "
          f"{sum(r['token_exhaustion_failures'] for r in results)}")
    print(f"total multi-atom to-be-folded lists: "
          f"{sum(r['multi_atom_fold_lists'] for r in results)}")
    print(f"traces that raised the token allowance: {len(multi)}")
    print(f"  of those, every search attempt identical after normalisation: "
          f"{sum(1 for r in multi if r['attempts_identical'])}")
    if multi:
        sizes = [r["attempt_lines"] for r in multi]
        print(f"  per-attempt size range: {min(sizes)}..{max(sizes)} lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
