"""Verify appendix.md CSV blocks match fixture exports."""

from __future__ import annotations

import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO))

from causal.experiments.handcrafted import load_handcrafted

APPENDIX = _REPO.parent / "appendix.md"


def main() -> None:
    text = APPENDIX.read_text(encoding="utf-8")
    pattern = re.compile(
        r"### QL\d cell \d+/\d+ — `(qi\d+[^`]+)`\s*\n(?:.*?\n)*?```csv\n(.*?)```",
        re.DOTALL,
    )
    blocks = pattern.findall(text)
    print(f"Found {len(blocks)} tables")
    mismatches: list[str] = []
    for key, csv in blocks:
        expected = load_handcrafted(key).df.to_csv(index=False).rstrip("\n")
        actual = csv.rstrip("\n")
        if expected != actual:
            mismatches.append(key)
    if mismatches:
        print("MISMATCH:", mismatches)
        raise SystemExit(1)
    print("All tables match fixtures verbatim.")


if __name__ == "__main__":
    main()
