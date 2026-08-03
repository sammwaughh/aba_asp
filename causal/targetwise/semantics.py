"""Final-artefact integrity checks for target-wise ABA Learning tasks."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import shutil
import subprocess
import time
from typing import Any, Callable


ARTIFACT_CHECK_STATUSES = frozenset(
    {"SAT", "UNSAT", "ERROR", "TIMEOUT", "UNAVAILABLE"}
)


@dataclass(frozen=True)
class ArtifactIntegrityCheckResult:
    """Result of executing one learner-produced ``.sol_chk.asp`` artefact."""

    status: str
    runtime_s: float
    failure_reason: str | None
    checked_asp_path: str | None
    clingo_path: str | None
    returncode: int | None

    def __post_init__(self) -> None:
        if self.status not in ARTIFACT_CHECK_STATUSES:
            raise ValueError(f"unknown artefact-check status: {self.status!r}")

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def unavailable_artifact_integrity_check(reason: str) -> ArtifactIntegrityCheckResult:
    """Return an explicit unavailable result without invoking Clingo."""

    return ArtifactIntegrityCheckResult(
        status="UNAVAILABLE",
        runtime_s=0.0,
        failure_reason=reason,
        checked_asp_path=None,
        clingo_path=None,
        returncode=None,
    )


def resolve_solution_asp_path(
    solution_aba_path: Path | None,
    output_dir: Path,
) -> Path | None:
    """Resolve the plain ASP serialization paired with one ABA solution."""

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


def resolve_solution_check_asp_path(
    solution_aba_path: Path | None,
    output_dir: Path,
) -> Path | None:
    """Resolve the learner-produced checked ASP paired with an ABA solution."""

    if solution_aba_path is not None:
        solution = Path(solution_aba_path)
        if solution.name.endswith(".sol.aba"):
            paired = solution.with_name(
                solution.name[: -len(".sol.aba")] + ".sol_chk.asp"
            )
            if paired.is_file():
                return paired

    matches = sorted(Path(output_dir).glob("*.sol_chk.asp"))
    if len(matches) == 1:
        return matches[0]
    return None


def final_artifact_integrity_check(
    solution_check_asp_path: Path | None,
    *,
    timeout_s: float,
    clingo_path: str | None = None,
    command_runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
) -> ArtifactIntegrityCheckResult:
    """Execute the final ``.sol_chk.asp`` emitted under ``check_ic``.

    The learner-produced file already combines the serialized final framework
    with joint E+/E- integrity constraints requiring one witnessing stable
    model.  This invocation is therefore a serialization/integrity audit, not a
    new coverage metric.  It matches the brave joint-witness condition, but it
    is not a cautious-consequence check when the learner runs in cautious mode.
    """

    if solution_check_asp_path is None or not Path(solution_check_asp_path).is_file():
        return unavailable_artifact_integrity_check(
            "learner-produced solution check ASP is missing"
        )

    resolved_clingo = clingo_path or shutil.which("clingo")
    if resolved_clingo is None:
        return ArtifactIntegrityCheckResult(
            status="UNAVAILABLE",
            runtime_s=0.0,
            failure_reason="clingo executable is not available on PATH",
            checked_asp_path=str(Path(solution_check_asp_path)),
            clingo_path=None,
            returncode=None,
        )

    run = command_runner or subprocess.run
    started = time.monotonic()
    try:
        completed = run(
            [
                str(resolved_clingo),
                str(Path(solution_check_asp_path)),
                "--models=1",
                "--opt-mode=ignore",
                "--quiet=2,1",
            ],
            capture_output=True,
            text=True,
            timeout=timeout_s,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return ArtifactIntegrityCheckResult(
            status="TIMEOUT",
            runtime_s=time.monotonic() - started,
            failure_reason=f"artefact Clingo check exceeded timeout_s={timeout_s:g}",
            checked_asp_path=str(Path(solution_check_asp_path)),
            clingo_path=str(resolved_clingo),
            returncode=None,
        )
    except OSError as exc:
        return ArtifactIntegrityCheckResult(
            status="ERROR",
            runtime_s=time.monotonic() - started,
            failure_reason=f"could not execute Clingo: {exc}",
            checked_asp_path=str(Path(solution_check_asp_path)),
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

    return ArtifactIntegrityCheckResult(
        status=status,
        runtime_s=runtime_s,
        failure_reason=failure_reason,
        checked_asp_path=str(Path(solution_check_asp_path)),
        clingo_path=str(resolved_clingo),
        returncode=completed.returncode,
    )
