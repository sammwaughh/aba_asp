from __future__ import annotations

from pathlib import Path


ROOT_STOCHASTIC_DETERMINISTIC_AND_YAML = """\
schema_version: 2
id: test_root_stochastic_deterministic_and
variables:
  - {name: a, states: [0, 1]}
  - {name: b, states: [0, 1]}
  - {name: c, states: [0, 1]}
graph:
  edges: [[a, c], [b, c]]
mechanisms:
  a:
    parents: []
    cpt: [{when: {}, probabilities: ["1/5", "4/5"]}]
  b:
    parents: []
    cpt: [{when: {}, probabilities: ["3/10", "7/10"]}]
  c:
    parents: [a, b]
    cpt:
      - {when: {a: 0, b: 0}, probabilities: [1, 0]}
      - {when: {a: 0, b: 1}, probabilities: [1, 0]}
      - {when: {a: 1, b: 0}, probabilities: [1, 0]}
      - {when: {a: 1, b: 1}, probabilities: [0, 1]}
assumptions:
  mechanism_regime: root_stochastic_deterministic_nonroots
  causal_sufficiency:
    declared: true
    exogenous_noise: mutually_independent_root_exogenous_noise
  observational_sampling: {regime: observational_iid}
"""


def write_root_stochastic_deterministic_and(tmp_path: Path) -> Path:
    path = tmp_path / "root_stochastic_deterministic_and.yaml"
    path.write_text(ROOT_STOCHASTIC_DETERMINISTIC_AND_YAML, encoding="utf-8")
    return path
