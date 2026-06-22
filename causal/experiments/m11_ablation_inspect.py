"""Trace and solution inspection for m1.1 ablation runs."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal

from causal.argcausaldisco_integration import _extract_learned_rules

Verdict = Literal["pass", "fail", "partial", "audit_pass", "audit_fail"]

_FIRST_FOLD_RE = re.compile(
    r"folding\s+\[A=\d+\]\s+with\s+([a-zA-Z0-9_]+)\(",
)
_BEGIN_FOLD_RE = re.compile(r"begin\s+(?:nd|all|greedy|lazy)\s+folding")
_GEN2_ENTAIL_PASS_RE = re.compile(
    r"gen2:\s+extended ABA entails\s+<E\+,E->",
)
_GEN2_ENTAIL_FAIL_RE = re.compile(
    r"gen2:\s+extended ABA does not entail\s+<E\+,E->",
)
_ABA_SIZE_RE = re.compile(r"ABA size \(rules\):\s+(\d+)")
_ASSUMPTION_NEW_RE = re.compile(r"gen2:\s+generating NEW assumption:")


@dataclass
class TraceObservables:
    first_fold_pred: str | None = None
    entailment: Literal["pass", "fail", "unknown"] = "unknown"
    trace_lines: int = 0
    aba_rules: int | None = None
    n_assumptions: int = 0
    folding_mode_line: str | None = None
    outcome: str | None = None


@dataclass
class AblationExpected:
    first_fold_pred: str | None = None
    entailment: Literal["pass", "fail"] | None = None
    target_rule: str | None = None
    max_trace_lines: int | None = None
    min_trace_lines: int | None = None
    max_aba_rules: int | None = None
    min_aba_rules: int | None = None
    n_assumptions_max: int | None = None
    singleton: bool | None = None

    @classmethod
    def from_dict(cls, d: dict[str, Any] | None) -> AblationExpected:
        if not d:
            return cls()
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class AblationSummary:
    abl_id: str
    observables: TraceObservables
    target_rules: list[str] = field(default_factory=list)
    normalised_target_rules: list[str] = field(default_factory=list)
    verdict: Verdict = "fail"
    mismatches: list[str] = field(default_factory=list)
    claim_impact: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "abl_id": self.abl_id,
            "observables": asdict(self.observables),
            "target_rules": self.target_rules,
            "normalised_target_rules": self.normalised_target_rules,
            "verdict": self.verdict,
            "mismatches": self.mismatches,
            "claim_impact": self.claim_impact,
        }


def _normalise_rule(rule: str) -> str:
    s = rule.strip().rstrip(".")
    s = re.sub(r"\s+", " ", s)
    s = s.replace(" :- ", "<-").replace(":- ", "<-")
    s = re.sub(r"\s*<-\s*", "<-", s)
    return s


def parse_trace_observables(stdout: str) -> TraceObservables:
    lines = stdout.splitlines()
    obs = TraceObservables(trace_lines=len(lines))

    m = _ABA_SIZE_RE.search(stdout)
    if m:
        obs.aba_rules = int(m.group(1))

    obs.n_assumptions = len(_ASSUMPTION_NEW_RE.findall(stdout))

    begin_idx = None
    for i, line in enumerate(lines):
        if _BEGIN_FOLD_RE.search(line):
            begin_idx = i
            obs.folding_mode_line = line.strip()
            break

    if begin_idx is not None:
        fold_line_idx: int | None = None
        for i, line in enumerate(lines[begin_idx:], start=begin_idx):
            fm = _FIRST_FOLD_RE.search(line)
            if fm:
                obs.first_fold_pred = fm.group(1)
                fold_line_idx = i
                break
        if fold_line_idx is not None:
            for line in lines[fold_line_idx:]:
                if _GEN2_ENTAIL_PASS_RE.search(line):
                    obs.entailment = "pass"
                    break
                if _GEN2_ENTAIL_FAIL_RE.search(line):
                    obs.entailment = "fail"
                    break

    if "Writing solution no." in stdout:
        obs.outcome = "solved"
    elif "No solution found" in stdout:
        obs.outcome = "no_solution"

    return obs


def parse_target_rules(sol_path: Path | None, bk_path: Path | None) -> tuple[list[str], list[str]]:
    if sol_path is None or not sol_path.is_file():
        if bk_path is not None:
            learned = _extract_learned_rules(bk_path)
            raw = [r for r in learned if r.strip().lower().startswith("x2(")]
            return raw, [_normalise_rule(r) for r in raw]
        return [], []

    text = sol_path.read_text(encoding="utf-8")
    raw: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("%") or line.startswith("assumption("):
            continue
        if line.startswith("contrary("):
            continue
        if line.startswith("x2(") and ":- " in line:
            raw.append(line)
    return raw, [_normalise_rule(r) for r in raw]


def compare_to_expected(
    abl_id: str,
    obs: TraceObservables,
    norm_rules: list[str],
    expected: AblationExpected,
    *,
    tests: list[str] | None = None,
) -> AblationSummary:
    mismatches: list[str] = []
    if expected.first_fold_pred and obs.first_fold_pred != expected.first_fold_pred:
        mismatches.append(
            f"first_fold_pred: got {obs.first_fold_pred!r}, "
            f"expected {expected.first_fold_pred!r}"
        )
    if expected.entailment and obs.entailment != expected.entailment:
        mismatches.append(
            f"entailment: got {obs.entailment!r}, expected {expected.entailment!r}"
        )
    if expected.target_rule:
        want = _normalise_rule(expected.target_rule)
        if want not in norm_rules:
            mismatches.append(f"target_rule: {want!r} not in {norm_rules!r}")
    if expected.max_trace_lines is not None and obs.trace_lines > expected.max_trace_lines:
        mismatches.append(
            f"trace_lines {obs.trace_lines} > max {expected.max_trace_lines}"
        )
    if expected.min_trace_lines is not None and obs.trace_lines < expected.min_trace_lines:
        mismatches.append(
            f"trace_lines {obs.trace_lines} < min {expected.min_trace_lines}"
        )
    if expected.max_aba_rules is not None and obs.aba_rules is not None:
        if obs.aba_rules > expected.max_aba_rules:
            mismatches.append(
                f"aba_rules {obs.aba_rules} > max {expected.max_aba_rules}"
            )
    if expected.min_aba_rules is not None and obs.aba_rules is not None:
        if obs.aba_rules < expected.min_aba_rules:
            mismatches.append(
                f"aba_rules {obs.aba_rules} < min {expected.min_aba_rules}"
            )
    if expected.n_assumptions_max is not None and obs.n_assumptions > expected.n_assumptions_max:
        mismatches.append(
            f"n_assumptions {obs.n_assumptions} > max {expected.n_assumptions_max}"
        )
    if expected.singleton is True and len(norm_rules) != 1:
        mismatches.append(f"singleton expected, got {len(norm_rules)} target rules")

    verdict: Verdict = "pass" if not mismatches else "fail"
    if mismatches and obs.outcome == "solved" and expected.singleton:
        verdict = "partial"

    summary = AblationSummary(
        abl_id=abl_id,
        observables=obs,
        normalised_target_rules=norm_rules,
        verdict=verdict,
        mismatches=mismatches,
        claim_impact=list(tests or []),
    )
    return summary


def inspect_ablation_dir(
    abl_dir: Path,
    abl_id: str,
    expected: AblationExpected,
    *,
    tests: list[str] | None = None,
) -> AblationSummary:
    stdout_path = abl_dir / "prolog.stdout"
    stdout = stdout_path.read_text(encoding="utf-8") if stdout_path.is_file() else ""
    obs = parse_trace_observables(stdout)
    sol_path = abl_dir / "bk.sol.aba"
    if not sol_path.is_file():
        for alt in ("bk.bk.sol.aba",):
            p = abl_dir / alt
            if p.is_file():
                sol_path = p
                break
    bk_path = abl_dir / "bk.aba"
    raw, norm = parse_target_rules(sol_path if sol_path.is_file() else None, bk_path)
    summary = compare_to_expected(abl_id, obs, norm, expected, tests=tests)
    summary.target_rules = raw
    return summary


def write_summary(abl_dir: Path, summary: AblationSummary) -> Path:
    out = abl_dir / "abl_summary.json"
    out.write_text(json.dumps(summary.to_dict(), indent=2) + "\n", encoding="utf-8")
    return out


def compare_audit_pair(
    abl_id: str,
    left_stdout: str,
    right_stdout: str,
    *,
    left_label: str,
    right_label: str,
    expected_left: AblationExpected,
    expected_right: AblationExpected,
    tests: list[str] | None = None,
) -> AblationSummary:
    left_obs = parse_trace_observables(left_stdout)
    right_obs = parse_trace_observables(right_stdout)
    left_sum = compare_to_expected(
        f"{abl_id}:{left_label}", left_obs, [], expected_left, tests=tests
    )
    right_sum = compare_to_expected(
        f"{abl_id}:{right_label}", right_obs, [], expected_right, tests=tests
    )
    mismatches = left_sum.mismatches + right_sum.mismatches
    verdict: Verdict = "audit_pass" if not mismatches else "audit_fail"
    return AblationSummary(
        abl_id=abl_id,
        observables=left_obs,
        verdict=verdict,
        mismatches=mismatches,
        claim_impact=list(tests or []),
        normalised_target_rules=[
            f"{left_label}:fold={left_obs.first_fold_pred},entail={left_obs.entailment}",
            f"{right_label}:fold={right_obs.first_fold_pred},entail={right_obs.entailment}",
        ],
    )
