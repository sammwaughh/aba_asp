"""Exact finite-discrete causal fixture definitions and derived artefacts.

The fixture YAML is the authoritative scientific source. Population tables,
certificates, BIF files, and finite samples are derived from it.
"""

from causal.fixtures.io import LoadedFixture, load_fixture
from causal.fixtures.model import CausalFixture, FixtureValidationError

__all__ = [
    "CausalFixture",
    "FixtureValidationError",
    "LoadedFixture",
    "load_fixture",
]
