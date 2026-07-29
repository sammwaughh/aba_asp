"""Joint stable-model checks for target-wise brave ABA Learning tasks."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import re
import shutil
import subprocess
import time
from typing import Any, Callable, Sequence


JOINT_BRAVE_STATUSES = frozenset({"SAT", "UNSAT", "ERROR", "TIMEOUT", "UNAVAILABLE"})

_GROUND_UNARY_ATOM_RE = re.compile(r"^[a-z][A-Za-z0-9_]*\([0-9]+\)$")


@dataclass(frozen=True)
class JointBraveCheckResult:
    """Result of one joint brave-task stable-model check."""

    status: str
    runtime_s: float
    failure_reason: str | None
    solution_asp_path: str | None
    clingo_path: str | None
    returncode: int | None

    def __post_init__(self) -> None:
        if self.status not in JOINT_BRAVE_STATUSES:
            raise ValueError(f"unknown joint brave status: {self.status!r}")

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def unavailable_joint_brave_check(reason: str) -> JointBraveCheckResult:
    """Return an explicit unavailable result without invoking Clingo."""

    return JointBraveCheckResult(
        status="UNAVAILABLE",
        runtime_s=0.0,
        failure_reason=reason,
        solution_asp_path=None,
        clingo_path=None,
        returncode=None,
    )


def resolve_solution_asp_path(
    solution_aba_path: Path | None,
    output_dir: Path,
) -> Path | None:
    """Resolve the ASP serialization paired with one learned ABA solution."""

    if solution_aba_path is not None:
        solution = Path(solution_aba_path)
        if solution.name.endswith(".sol.aba"):
            paired = solution.with_name(solution.name[: -len(".aba")] + ".asp")
            if paired.is_file():
                return paired

    matches = sorted(Path(output_dir).glob("*.sol.asp"))
    if len(matches) == 1:
        return matches[0]
    return None


def _normalise_example_atom(atom: str) -> str:
    normalised = atom.strip().rstrip(".")
    if not _GROUND_UNARY_ATOM_RE.fullmatch(normalised):
        raise ValueError(
            "joint brave checks require ground unary example atoms of the form "
            f"predicate(integer); got {atom!r}"
        )
    return normalised


def build_joint_brave_constraints(
    positive_examples: Sequence[str],
    negative_examples: Sequence[str],
) -> str:
    """Build the joint integrity constraints used by brave ABA Learning."""

    positive = [_normalise_example_atom(atom) for atom in positive_examples]
    negative = [_normalise_example_atom(atom) for atom in negative_examples]
    lines = [
        "% Joint post-hoc brave-task check.",
        "% One stable model must contain every E+ atom and no E- atom.",
    ]
    lines.extend(f":- not {atom}." for atom in positive)
    lines.extend(f":- {atom}." for atom in negative)
    return "\n".join(lines) + "\n"


def joint_brave_task_check(
    solution_asp_path: Path | None,
    positive_examples: Sequence[str],
    negative_examples: Sequence[str],
    *,
    timeout_s: float,
    clingo_path: str | None = None,
    command_runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
) -> JointBraveCheckResult:
    """Check whether one stable model jointly satisfies all E+/E- constraints.

    This is one satisfiability query over the final serialized learned framework.
    It is not a collection of independent per-example brave-entailment queries.
    """

    if solution_asp_path is None or not Path(solution_asp_path).is_file():
        return unavailable_joint_brave_check("solution ASP serialization is missing")

    resolved_clingo = clingo_path or shutil.which("clingo")
    if resolved_clingo is None:
        return JointBraveCheckResult(
            status="UNAVAILABLE",
            runtime_s=0.0,
            failure_reason="clingo executable is not available on PATH",
            solution_asp_path=str(Path(solution_asp_path)),
            clingo_path=None,
            returncode=None,
        )

    try:
        constraints = build_joint_brave_constraints(
            positive_examples,
            negative_examples,
        )
    except ValueError as exc:
        return JointBraveCheckResult(
            status="ERROR",
            runtime_s=0.0,
            failure_reason=str(exc),
            solution_asp_path=str(Path(solution_asp_path)),
            clingo_path=str(resolved_clingo),
            returncode=None,
        )

    run = command_runner or subprocess.run
    started = time.monotonic()
    try:
        completed = run(
            [
                str(resolved_clingo),
                str(Path(solution_asp_path)),
                "-",
                "--models=1",
                "--opt-mode=ignore",
                "--quiet=2,1",
            ],
            input=constraints,
            capture_output=True,
            text=True,
            timeout=timeout_s,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return JointBraveCheckResult(
            status="TIMEOUT",
            runtime_s=time.monotonic() - started,
            failure_reason=f"joint Clingo check exceeded timeout_s={timeout_s:g}",
            solution_asp_path=str(Path(solution_asp_path)),
            clingo_path=str(resolved_clingo),
            returncode=None,
        )
    except OSError as exc:
        return JointBraveCheckResult(
            status="ERROR",
            runtime_s=time.monotonic() - started,
            failure_reason=f"could not execute Clingo: {exc}",
            solution_asp_path=str(Path(solution_asp_path)),
            clingo_path=str(resolved_clingo),
            returncode=None,
        )

    runtime_s = time.monotonic() - started
    output = f"{completed.stdout or ''}\n{completed.stderr or ''}"
    if completed.returncode == 20 or "UNSATISFIABLE" in output:
        status = "UNSAT"
        failure_reason = None
    elif completed.returncode == 10 or (
        "SATISFIABLE" in output and "UNSATISFIABLE" not in output
    ):
        status = "SAT"
        failure_reason = None
    else:
        status = "ERROR"
        excerpt = " ".join(output.split())[:300]
        failure_reason = f"unexpected Clingo return code {completed.returncode}" + (
            f": {excerpt}" if excerpt else ""
        )

    return JointBraveCheckResult(
        status=status,
        runtime_s=runtime_s,
        failure_reason=failure_reason,
        solution_asp_path=str(Path(solution_asp_path)),
        clingo_path=str(resolved_clingo),
        returncode=completed.returncode,
    )
