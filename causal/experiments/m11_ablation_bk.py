"""BK file interventions for m1.1 ablation experiments (M11).

Pure Prolog-free helpers: parse cat3 feature-predicate blocks, reorder,
prepend rules, and verify rule multisets. See
``docs/research/milestone_plans/milestone1_part1_ablations.md``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

RuleKind = Literal["comment", "rule"]

_BLOCK_HEADER_RE = re.compile(
    r"^%\s*Feature predicates for variable:\s*(x[01])\s*$", re.MULTILINE
)
_RULE_LINE_RE = re.compile(r"^[a-zA-Z0-9_]+\([^)]*\)\s*:-\s*.+\.\s*$")


@dataclass(frozen=True)
class BkLine:
    kind: RuleKind
    text: str

    @property
    def is_rule(self) -> bool:
        return self.kind == "rule"

    @property
    def rule_key(self) -> str | None:
        if not self.is_rule:
            return None
        return self.text.strip()


def read_bk_text(path: Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def parse_bk_lines(text: str) -> list[BkLine]:
    """Split BK into comment and rule lines preserving order."""
    out: list[BkLine] = []
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        if _RULE_LINE_RE.match(line.strip()):
            out.append(BkLine("rule", line.strip()))
        else:
            out.append(BkLine("comment", line))
    return out


def rule_multiset(lines: list[BkLine]) -> frozenset[str]:
    return frozenset(ln.rule_key for ln in lines if ln.is_rule and ln.rule_key)


def bk_rule_multiset(a: str, b: str) -> bool:
    """True if both BK texts contain the same set of rule lines (order ignored)."""
    return rule_multiset(parse_bk_lines(a)) == rule_multiset(parse_bk_lines(b))


def _variable_from_block_header(comment: str) -> str | None:
    m = _BLOCK_HEADER_RE.match(comment.strip())
    return m.group(1) if m else None


def _split_into_blocks(lines: list[BkLine]) -> list[tuple[str | None, list[BkLine]]]:
    """Group lines into (variable_name, lines) blocks separated by feature headers."""
    blocks: list[tuple[str | None, list[BkLine]]] = []
    current_var: str | None = None
    current: list[BkLine] = []

    def flush() -> None:
        nonlocal current, current_var
        if current:
            blocks.append((current_var, current))
        current = []
        current_var = None

    for ln in lines:
        var = _variable_from_block_header(ln.text) if ln.kind == "comment" else None
        if var is not None:
            flush()
            current_var = var
            current.append(ln)
        else:
            current.append(ln)
    flush()
    return blocks


def _leading_preamble(lines: list[BkLine]) -> list[BkLine]:
    """Lines before the first feature block header."""
    for i, ln in enumerate(lines):
        if ln.kind == "comment" and _variable_from_block_header(ln.text):
            return lines[:i]
    return []


def reorder_bk_blocks(text: str, *, block_order: tuple[str, ...]) -> str:
    """Permute x0/x1 feature blocks; preserve within-block line order and preamble."""
    lines = parse_bk_lines(text)
    preamble = _leading_preamble(lines)
    blocks = _split_into_blocks(lines)
    by_var: dict[str, list[BkLine]] = {}
    trailing: list[BkLine] = []
    for var, blines in blocks:
        if var is None:
            trailing.extend(blines)
        else:
            by_var[var] = blines

    missing = [v for v in block_order if v not in by_var]
    if missing:
        raise ValueError(f"block_order references missing variables: {missing}")

    out_lines: list[BkLine] = list(preamble)
    for var in block_order:
        out_lines.extend(by_var[var])
    out_lines.extend(trailing)
    return "\n".join(ln.text for ln in out_lines) + "\n"


def block_order_from_source(source_text: str) -> tuple[str, ...]:
    """Return variable block order as declared in source BK headers."""
    order: list[str] = []
    for ln in parse_bk_lines(source_text):
        if ln.kind == "comment":
            var = _variable_from_block_header(ln.text)
            if var and var not in order:
                order.append(var)
    return tuple(order)


def reorder_bk_blocks_from(source_text: str, baseline_text: str) -> str:
    """Apply source BK's block order to baseline rule content."""
    order = block_order_from_source(source_text)
    if not order:
        raise ValueError("source BK has no feature block headers")
    return reorder_bk_blocks(baseline_text, block_order=order)


def prepend_bk_rules(text: str, rule_lines: list[str]) -> str:
    """Insert rules immediately after the preamble (before first feature block)."""
    lines = parse_bk_lines(text)
    preamble = _leading_preamble(lines)
    rest_start = len(preamble)
    for i, ln in enumerate(lines):
        if ln.kind == "comment" and _variable_from_block_header(ln.text):
            rest_start = i
            break
    else:
        rest_start = len(preamble)

    new_rules = [BkLine("rule", r.strip()) for r in rule_lines]
    out = list(preamble) + new_rules + lines[rest_start:]
    return "\n".join(ln.text for ln in out) + "\n"


def build_intervened_bk(
    baseline_text: str,
    *,
    mode: str,
    source_text: str | None = None,
    prepend_rules: list[str] | None = None,
) -> str:
    """Build intervened BK from baseline according to ablation mode."""
    if mode == "copy_baseline":
        return baseline_text if baseline_text.endswith("\n") else baseline_text + "\n"
    if mode == "block_order_from":
        if source_text is None:
            raise ValueError("block_order_from requires source_text")
        result = reorder_bk_blocks_from(source_text, baseline_text)
        if not bk_rule_multiset(baseline_text, result):
            raise ValueError("block reorder changed rule multiset")
        return result
    if mode == "prepend_rules":
        if not prepend_rules:
            raise ValueError("prepend_rules requires prepend_rules list")
        return prepend_bk_rules(baseline_text, prepend_rules)
    raise ValueError(f"unknown bk_mode: {mode!r}")
