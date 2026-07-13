"""ASP answer-set coverage via clingo on ``bk.sol.asp``.

Brave entailment of an example atom ``T(id)``: ``clingo(P ∪ {:- not T(id).})``
is SAT iff some answer set of ``P`` contains ``T(id)``.

Used as the authoritative post-hoc coverage layer for M1.2 (and available on the
shared metrics panel). Does not use leftover ``asp.clingo`` scratch files.
"""

from __future__ import annotations

import logging
import math
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Sequence

logger = logging.getLogger(__name__)

_CLINGO_BIN = shutil.which("clingo")


def clingo_available() -> bool:
    """True if a ``clingo`` executable is on PATH."""
    return _CLINGO_BIN is not None


def resolve_sol_asp_path(bk_path: Path, sol_path: Path | None) -> Path | None:
    """Locate ``bk.sol.asp`` beside the ABA solution / BK files."""
    candidates: list[Path] = []
    if sol_path is not None:
        parent = Path(sol_path).parent
        stem = Path(sol_path).name
        # bk.sol.aba -> bk.sol.asp; foo.sol.aba -> foo.sol.asp
        if stem.endswith(".sol.aba"):
            candidates.append(parent / (stem[: -len(".aba")] + ".asp"))
        candidates.append(parent / "bk.sol.asp")
    if bk_path is not None:
        candidates.append(Path(bk_path).parent / "bk.sol.asp")
    seen: set[Path] = set()
    for path in candidates:
        resolved = path.resolve() if path.exists() else path
        if resolved in seen:
            continue
        seen.add(resolved)
        if path.is_file():
            return path
    return None


def _normalize_atom(atom: str) -> str:
    return atom.strip().rstrip(".")


def atom_bravely_entailed(
    sol_asp_path: Path,
    atom: str,
    *,
    timeout_s: float = 5.0,
) -> bool | None:
    """Return whether ``atom`` is bravely entailed by ``sol_asp_path``.

    Returns ``None`` if clingo is unavailable or the run fails/times out.
    """
    if not clingo_available():
        return None
    sol_asp_path = Path(sol_asp_path)
    if not sol_asp_path.is_file():
        return None

    atom_norm = _normalize_atom(atom)
    base = sol_asp_path.read_text(encoding="utf-8")
    program = base.rstrip() + f"\n:- not {atom_norm}.\n"

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".lp",
        encoding="utf-8",
        delete=False,
    ) as tmp:
        tmp.write(program)
        tmp_path = Path(tmp.name)

    try:
        completed = subprocess.run(
            [
                _CLINGO_BIN,
                str(tmp_path),
                "--out-ifs=,",
                "--opt-mode=ignore",
                "--quiet=2,1",
            ],
            capture_output=True,
            text=True,
            timeout=timeout_s,
            check=False,
        )
    except subprocess.TimeoutExpired:
        logger.warning("clingo timed out for atom %s on %s", atom_norm, sol_asp_path)
        return None
    except OSError as exc:
        logger.warning("clingo failed for atom %s: %s", atom_norm, exc)
        return None
    finally:
        try:
            tmp_path.unlink(missing_ok=True)
        except OSError:
            pass

    # clingo: 10 = SAT (models found), 20 = UNSAT, 30 = SAT with interrupted search, etc.
    # Treat returncode 10 (and stdout containing SATISFIABLE) as entailed.
    out = (completed.stdout or "") + (completed.stderr or "")
    if "UNSATISFIABLE" in out and "SATISFIABLE" not in out.replace("UNSATISFIABLE", ""):
        return False
    if completed.returncode == 20:
        return False
    if completed.returncode == 10 or "SATISFIABLE" in out:
        return True
    # Ambiguous / error
    logger.warning(
        "clingo unexpected rc=%s for atom %s: %s",
        completed.returncode,
        atom_norm,
        out[:300],
    )
    return None


def _placeholder(*, nan_reason: str) -> dict[str, float | int | str]:
    nan = math.nan
    return {
        "cov_asp_accuracy": nan,
        "cov_asp_pos": nan,
        "cov_asp_neg": nan,
        "cov_asp_tp": 0,
        "cov_asp_fp": 0,
        "cov_asp_tn": 0,
        "cov_asp_fn": 0,
        "cov_asp_n_pos": 0,
        "cov_asp_n_neg": 0,
        "_cov_asp_nan_reason": nan_reason,
    }


def asp_answer_set_coverage(
    sol_asp_path: Path | None,
    pos: Sequence[str],
    neg: Sequence[str],
    *,
    timeout_s: float = 5.0,
) -> dict[str, float | int | str]:
    """Brave ASP coverage of E+/E− against ``bk.sol.asp`` (METRICS.md §3.5).

    ``cov_asp_pos`` = TP/|E+| (fraction of positives bravely entailed).
    ``cov_asp_neg`` = TN/|E−| (fraction of negatives *not* bravely entailed).
    Also returns ``cov_asp_n_pos`` / ``cov_asp_n_neg`` for ``k/n`` display.
    """
    n_pos = len(pos)
    n_neg = len(neg)
    if sol_asp_path is None or not Path(sol_asp_path).is_file():
        out = _placeholder(nan_reason="sol_asp_missing")
        out["cov_asp_n_pos"] = n_pos
        out["cov_asp_n_neg"] = n_neg
        return out
    if not clingo_available():
        out = _placeholder(nan_reason="clingo_unavailable")
        out["cov_asp_n_pos"] = n_pos
        out["cov_asp_n_neg"] = n_neg
        return out
    if n_pos == 0 and n_neg == 0:
        out = _placeholder(nan_reason="no_examples")
        return out

    tp = fp = tn = fn = 0
    for atom in pos:
        entailed = atom_bravely_entailed(Path(sol_asp_path), atom, timeout_s=timeout_s)
        if entailed is None:
            out = _placeholder(nan_reason="clingo_failed")
            out["cov_asp_n_pos"] = n_pos
            out["cov_asp_n_neg"] = n_neg
            return out
        if entailed:
            tp += 1
        else:
            fn += 1
    for atom in neg:
        entailed = atom_bravely_entailed(Path(sol_asp_path), atom, timeout_s=timeout_s)
        if entailed is None:
            out = _placeholder(nan_reason="clingo_failed")
            out["cov_asp_n_pos"] = n_pos
            out["cov_asp_n_neg"] = n_neg
            return out
        if entailed:
            fp += 1
        else:
            tn += 1

    total = n_pos + n_neg
    accuracy = (tp + tn) / total if total else 0.0
    pos_cov = tp / n_pos if n_pos else 0.0
    neg_cov = tn / n_neg if n_neg else 0.0
    return {
        "cov_asp_tp": tp,
        "cov_asp_fp": fp,
        "cov_asp_tn": tn,
        "cov_asp_fn": fn,
        "cov_asp_accuracy": accuracy,
        "cov_asp_pos": pos_cov,
        "cov_asp_neg": neg_cov,
        "cov_asp_n_pos": n_pos,
        "cov_asp_n_neg": n_neg,
    }
