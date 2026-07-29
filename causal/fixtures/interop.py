"""Loss-aware pgmpy/BIF interoperability for exact causal fixtures."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import math
from pathlib import Path
import re
from typing import Any

from causal.fixtures.artifacts import file_sha256, write_text_once
from causal.fixtures.model import CausalFixture


_BIF_TOKEN_RE = re.compile(r"^[A-Za-z0-9_.+-]+$")


class BIFInteropError(ValueError):
    """Raised when a fixture cannot be exported or checked as BIF."""


@dataclass(frozen=True)
class BIFRoundTripReport:
    ok: bool
    max_absolute_probability_error: float
    tolerance: float
    errors: tuple[str, ...]
    pgmpy_version: str
    implementation_hash: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "max_absolute_probability_error": self.max_absolute_probability_error,
            "tolerance": self.tolerance,
            "errors": list(self.errors),
            "pgmpy_version": self.pgmpy_version,
            "implementation_hash": self.implementation_hash,
            "limitations": [
                "BIF probabilities are floating point rather than exact rationals",
                "BIF state labels are serialized as strings",
                "BIF does not preserve causal-sufficiency or IID-sampling declarations",
            ],
        }


def _require_bif_safe_states(fixture: CausalFixture) -> None:
    for variable in fixture.variables:
        for state in variable.states:
            token = str(state)
            if not _BIF_TOKEN_RE.fullmatch(token):
                raise BIFInteropError(
                    f"state {state!r} of {variable.name!r} is not a safe unquoted BIF token"
                )


def to_pgmpy_model(fixture: CausalFixture):
    """Convert an exact fixture to a checked pgmpy model.

    The conversion to pgmpy necessarily converts exact fractions to floats.
    """
    _require_bif_safe_states(fixture)
    try:
        from pgmpy.factors.discrete import TabularCPD
        from pgmpy.models import DiscreteBayesianNetwork
    except ImportError as exc:  # pragma: no cover - canonical env includes pgmpy
        raise BIFInteropError("pgmpy is required for BIF interoperability") from exc

    model = DiscreteBayesianNetwork()
    model.name = fixture.fixture_id
    model.add_nodes_from(fixture.variable_names)
    model.add_edges_from(fixture.edges)

    cpds = []
    for variable in fixture.variables:
        mechanism = fixture.mechanism_for(variable.name)
        parent_domains = [fixture.states_of(parent) for parent in mechanism.parents]
        parent_assignments = list(product(*parent_domains))
        values: list[list[float]] = []
        for child_state in variable.states:
            row: list[float] = []
            for parent_values in parent_assignments:
                parent_assignment = dict(zip(mechanism.parents, parent_values))
                row.append(
                    float(
                        fixture.conditional_probability(
                            variable.name, child_state, parent_assignment
                        )
                    )
                )
            values.append(row)

        state_names = {
            variable.name: [str(state) for state in variable.states],
            **{
                parent: [str(state) for state in fixture.states_of(parent)]
                for parent in mechanism.parents
            },
        }
        if mechanism.parents:
            cpd = TabularCPD(
                variable=variable.name,
                variable_card=len(variable.states),
                values=values,
                evidence=list(mechanism.parents),
                evidence_card=[
                    len(fixture.states_of(parent)) for parent in mechanism.parents
                ],
                state_names=state_names,
            )
        else:
            cpd = TabularCPD(
                variable=variable.name,
                variable_card=len(variable.states),
                values=values,
                state_names=state_names,
            )
        cpds.append(cpd)

    model.add_cpds(*cpds)
    try:
        checked = model.check_model()
    except Exception as exc:  # pragma: no cover - defensive against pgmpy changes
        raise BIFInteropError(f"pgmpy rejected converted fixture: {exc}") from exc
    if not checked:
        raise BIFInteropError("pgmpy rejected converted fixture")
    return model


def bif_text(fixture: CausalFixture) -> str:
    try:
        from pgmpy.readwrite import BIFWriter
    except ImportError as exc:  # pragma: no cover
        raise BIFInteropError("pgmpy is required for BIF interoperability") from exc
    return str(BIFWriter(to_pgmpy_model(fixture), round_values=None))


def _compare_imported_model(
    fixture: CausalFixture,
    imported_model,
    *,
    tolerance: float,
) -> BIFRoundTripReport:
    import pgmpy

    errors: list[str] = []
    max_error = 0.0
    try:
        if not imported_model.check_model():
            errors.append("pgmpy check_model returned false after BIF import")
    except Exception as exc:
        errors.append(f"pgmpy check_model failed after BIF import: {exc}")

    if set(imported_model.nodes()) != set(fixture.variable_names):
        errors.append(
            f"node mismatch: expected {sorted(fixture.variable_names)}, "
            f"got {sorted(imported_model.nodes())}"
        )
    if set(imported_model.edges()) != set(fixture.edges):
        errors.append(
            f"edge mismatch: expected {sorted(fixture.edges)}, "
            f"got {sorted(imported_model.edges())}"
        )

    for variable in fixture.variables:
        cpd = imported_model.get_cpds(variable.name)
        if cpd is None:
            errors.append(f"missing imported CPD for {variable.name}")
            continue
        mechanism = fixture.mechanism_for(variable.name)
        imported_parents = tuple(cpd.variables[1:])
        if imported_parents != mechanism.parents:
            errors.append(
                f"parent order mismatch for {variable.name}: expected "
                f"{mechanism.parents}, got {imported_parents}"
            )
        expected_child_states = [str(state) for state in variable.states]
        imported_child_states = list(cpd.state_names.get(variable.name, []))
        if imported_child_states != expected_child_states:
            errors.append(
                f"state order mismatch for {variable.name}: expected "
                f"{expected_child_states}, got {imported_child_states}"
            )
        for parent in mechanism.parents:
            expected_parent_states = [str(state) for state in fixture.states_of(parent)]
            imported_parent_states = list(cpd.state_names.get(parent, []))
            if imported_parent_states != expected_parent_states:
                errors.append(
                    f"state order mismatch for parent {parent} in {variable.name}: "
                    f"expected {expected_parent_states}, got {imported_parent_states}"
                )

        parent_domains = [fixture.states_of(parent) for parent in mechanism.parents]
        for parent_values in product(*parent_domains):
            original_parent_assignment = dict(zip(mechanism.parents, parent_values))
            imported_parent_assignment = {
                parent: str(value)
                for parent, value in original_parent_assignment.items()
            }
            for child_state in variable.states:
                expected = float(
                    fixture.conditional_probability(
                        variable.name, child_state, original_parent_assignment
                    )
                )
                try:
                    observed = float(
                        cpd.get_value(
                            **{
                                variable.name: str(child_state),
                                **imported_parent_assignment,
                            }
                        )
                    )
                except Exception as exc:
                    errors.append(
                        f"could not read imported probability for {variable.name}="
                        f"{child_state!r}, parents={original_parent_assignment!r}: {exc}"
                    )
                    continue
                error = abs(observed - expected)
                max_error = max(max_error, error)
                if not math.isclose(observed, expected, rel_tol=0.0, abs_tol=tolerance):
                    errors.append(
                        f"probability mismatch for {variable.name}={child_state!r}, "
                        f"parents={original_parent_assignment!r}: expected {expected}, "
                        f"got {observed}"
                    )

    return BIFRoundTripReport(
        ok=not errors,
        max_absolute_probability_error=max_error,
        tolerance=tolerance,
        errors=tuple(errors),
        pgmpy_version=pgmpy.__version__,
        implementation_hash=file_sha256(Path(__file__)),
    )


def validate_bif_text(
    fixture: CausalFixture, text: str, *, tolerance: float = 1e-12
) -> BIFRoundTripReport:
    try:
        from pgmpy.readwrite import BIFReader
    except ImportError as exc:  # pragma: no cover
        raise BIFInteropError("pgmpy is required for BIF interoperability") from exc
    try:
        imported = BIFReader(string=text).get_model(state_name_type=str)
    except Exception as exc:
        raise BIFInteropError(f"could not parse generated BIF: {exc}") from exc
    return _compare_imported_model(fixture, imported, tolerance=tolerance)


def validate_bif_file(
    fixture: CausalFixture, path: Path | str, *, tolerance: float = 1e-12
) -> BIFRoundTripReport:
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(source)
    try:
        from pgmpy.readwrite import BIFReader
    except ImportError as exc:  # pragma: no cover
        raise BIFInteropError("pgmpy is required for BIF interoperability") from exc
    try:
        imported = BIFReader(path=str(source)).get_model(state_name_type=str)
    except Exception as exc:
        raise BIFInteropError(f"could not parse generated BIF {source}: {exc}") from exc
    return _compare_imported_model(fixture, imported, tolerance=tolerance)


def export_bif(
    fixture: CausalFixture,
    path: Path | str,
    *,
    tolerance: float = 1e-12,
) -> BIFRoundTripReport:
    destination = Path(path)
    write_text_once(destination, bif_text(fixture))
    report = validate_bif_file(fixture, destination, tolerance=tolerance)
    if not report.ok:
        raise BIFInteropError(
            "generated BIF failed round-trip validation: " + "; ".join(report.errors)
        )
    return report
