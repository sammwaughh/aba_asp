from __future__ import annotations

from pathlib import Path


ROOT_STOCHASTIC_DETERMINISTIC_AND_YAML = """\
schema_version: 2
id: test_root_stochastic_deterministic_and
variables:
  - {name: x0, states: [0, 1]}
  - {name: x1, states: [0, 1]}
  - {name: x2, states: [0, 1]}
graph:
  edges: [[x0, x2], [x1, x2]]
mechanisms:
  x0:
    parents: []
    cpt: [{when: {}, probabilities: ["1/5", "4/5"]}]
  x1:
    parents: []
    cpt: [{when: {}, probabilities: ["3/10", "7/10"]}]
  x2:
    parents: [x0, x1]
    cpt:
      - {when: {x0: 0, x1: 0}, probabilities: [1, 0]}
      - {when: {x0: 0, x1: 1}, probabilities: [1, 0]}
      - {when: {x0: 1, x1: 0}, probabilities: [1, 0]}
      - {when: {x0: 1, x1: 1}, probabilities: [0, 1]}
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
