from __future__ import annotations

from dataclasses import dataclass

from causal.metrics import GroundTruth


@dataclass(frozen=True)
class DGPDefinition:
    id: str
    nodes: int
    edges: tuple[tuple[int, int], ...]

    def ground_truth(self) -> GroundTruth:
        names = tuple(f"x{i}" for i in range(self.nodes))
        edge_names = frozenset((f"x{s}", f"x{t}") for s, t in self.edges)
        return GroundTruth(nodes=names, edges=edge_names)


def dgp_zoo() -> tuple[DGPDefinition, ...]:
    """Return the canonical DGP zoo.

    Five synthetic ground-truth graphs used to build experiment grids: three
    3-node graphs (chain, fork, collider) and two 4-node graphs (fork-chain,
    hub). Each carries its node count and directed edges so the runner can both
    simulate data and score learned rules against the true parents.
    """
    return (
        DGPDefinition(id="G3-chain", nodes=3, edges=((0, 1), (1, 2))),
        DGPDefinition(id="G3-fork", nodes=3, edges=((0, 1), (0, 2))),
        DGPDefinition(id="G3-collider", nodes=3, edges=((0, 2), (1, 2))),
        DGPDefinition(id="G4-forkchain", nodes=4, edges=((0, 1), (0, 2), (2, 3))),
        DGPDefinition(id="G4-hub", nodes=4, edges=((0, 1), (0, 2), (0, 3))),
    )


def get_dgp(dgp_id: str) -> DGPDefinition:
    for d in dgp_zoo():
        if d.id == dgp_id:
            return d
    raise KeyError(f"Unknown DGP id: {dgp_id}")

