from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml


class ConfigError(ValueError):
    """Raised when an experiment YAML config fails validation."""


@dataclass(frozen=True)
class DGPSpec:
    id: str
    nodes: int
    edges: tuple[tuple[int, int], ...]
    n: int | None = None
    graph_type: str | None = None
    example_split: str | None = None
    source: str | None = None
    targets: tuple[str, ...] | None = None


_CELL_DIR_MODES = frozenset({"hash", "dgp", "slug"})


@dataclass(frozen=True)
class GridSpec:
    # Empty when ``grid.seed`` is omitted (deterministic / no-seed experiments).
    seeds: tuple[int, ...]
    target: str | tuple[str, ...]  # "all" or explicit targets
    n: tuple[int, ...] | None = None  # used when DGP entries omit per-dgp ``n``
    cell_dir: str = "hash"  # hash | dgp | slug — filesystem name under cells/


@dataclass(frozen=True)
class ExperimentConfig:
    experiment_id: str
    description: str | None
    defaults: Mapping[str, Any]
    dgps: tuple[DGPSpec, ...]
    grid: GridSpec
    provenance: Mapping[str, Any] | None = None


@dataclass(frozen=True)
class CellSpec:
    experiment_id: str
    dgp: str
    nodes: int
    edges: tuple[tuple[int, int], ...]
    n: int
    seed: int | None  # None when ``grid.seed`` omitted (no seed dimension)
    target: str
    config_hash: str
    run_id: str
    cell_dir_name: str
    graph_type: str
    example_split: str
    handcrafted_source: str | None = None


def _require_dict(obj: Any, *, where: str) -> Mapping[str, Any]:
    """Return ``obj`` if it is a mapping, else raise ConfigError naming ``where``."""
    if not isinstance(obj, dict):
        raise ConfigError(f"{where} must be a mapping")
    return obj


def _require_list(obj: Any, *, where: str) -> Sequence[Any]:
    """Return ``obj`` if it is a list, else raise ConfigError naming ``where``."""
    if not isinstance(obj, list):
        raise ConfigError(f"{where} must be a list")
    return obj


def _require_str(obj: Any, *, where: str) -> str:
    """Return ``obj`` if it is a non-empty string, else raise ConfigError."""
    if not isinstance(obj, str) or not obj.strip():
        raise ConfigError(f"{where} must be a non-empty string")
    return obj


def _require_int(obj: Any, *, where: str) -> int:
    """Return ``obj`` if it is an int, else raise ConfigError naming ``where``."""
    if not isinstance(obj, int):
        raise ConfigError(f"{where} must be an int")
    return obj


def _parse_edges(
    edges_obj: Any, *, nodes: int, where: str, required: bool = True
) -> tuple[tuple[int, int], ...]:
    """Parse and validate a list of ``[src, dst]`` directed edges.

    Each edge must be a pair of ints inside ``range(nodes)``. Returns the edges
    as a tuple of pairs. If ``required`` is False, a missing list yields ``()``.
    """
    if edges_obj is None:
        if required:
            raise ConfigError(f"{where} is required")
        return ()
    edges_list = _require_list(edges_obj, where=where)
    parsed: list[tuple[int, int]] = []
    for i, e in enumerate(edges_list):
        if (
            not isinstance(e, (list, tuple))
            or len(e) != 2
            or not isinstance(e[0], int)
            or not isinstance(e[1], int)
        ):
            raise ConfigError(f"{where}[{i}] must be a pair of ints [src,dst]")
        src, dst = int(e[0]), int(e[1])
        if src < 0 or dst < 0 or src >= nodes or dst >= nodes:
            raise ConfigError(
                f"{where}[{i}] edge indices out of range for nodes={nodes}: {e}"
            )
        parsed.append((src, dst))
    return tuple(parsed)


def _parse_seeds(seed_obj: Any, *, where: str) -> tuple[int, ...]:
    """Parse the ``grid.seed`` field into an explicit tuple of seeds.

    Accepts either an explicit non-empty list of ints, or a mapping
    ``{range: [start, end]}`` which expands to ``range(start, end)``.
    Callers that omit ``grid.seed`` entirely should pass ``None`` and treat the
    result as “no seed dimension” (empty tuple), not call this helper.
    """
    if isinstance(seed_obj, list):
        if not seed_obj:
            raise ConfigError(
                f"{where} must be non-empty when present; omit grid.seed for "
                "deterministic / no-seed experiments"
            )
        return tuple(_require_int(s, where=f"{where}[{i}]") for i, s in enumerate(seed_obj))
    if isinstance(seed_obj, dict):
        d = _require_dict(seed_obj, where=where)
        r = d.get("range")
        if not isinstance(r, (list, tuple)) or len(r) != 2:
            raise ConfigError(f"{where}.range must be [start, end]")
        start = _require_int(r[0], where=f"{where}.range[0]")
        end = _require_int(r[1], where=f"{where}.range[1]")
        if end <= start:
            raise ConfigError(f"{where}.range must satisfy end > start")
        return tuple(range(start, end))
    raise ConfigError(f"{where} must be a list of ints or {{range: [start, end]}}")


def _validate_defaults(defaults: Mapping[str, Any]) -> None:
    """Range-check the numeric knobs in ``defaults`` (bins, folding, timeouts)."""
    if "bins" in defaults and isinstance(defaults["bins"], int) and defaults["bins"] < 2:
        raise ConfigError("defaults.bins must be >= 2")
    if (
        "folding_steps" in defaults
        and isinstance(defaults["folding_steps"], int)
        and defaults["folding_steps"] < 1
    ):
        raise ConfigError("defaults.folding_steps must be >= 1")
    for key in ("prolog_timeout_s", "query_timeout_s"):
        if key in defaults:
            val = defaults[key]
            if not isinstance(val, (int, float)) or val <= 0:
                raise ConfigError(f"defaults.{key} must be positive")


def config_hash_from_yaml_obj(obj: Any) -> str:
    """Deterministic sha256 of the parsed YAML object."""
    canonical = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def config_hash_from_path(path: Path) -> str:
    """Deterministic sha256 of the YAML config at ``path``."""
    path = Path(path)
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    return config_hash_from_yaml_obj(raw)


def _short_run_id(payload: str) -> str:
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:12]


def _parse_cell_dir(obj: Any, *, where: str) -> str:
    """Parse ``grid.cell_dir``; default ``hash`` when absent."""
    if obj is None:
        return "hash"
    mode = _require_str(obj, where=where)
    if mode not in _CELL_DIR_MODES:
        allowed = ", ".join(sorted(_CELL_DIR_MODES))
        raise ConfigError(f"{where} must be one of: {allowed}")
    return mode


def _cell_dir_name(
    mode: str,
    *,
    dgp: str,
    target: str,
    seed: int | None,
    run_id: str,
) -> str:
    """Return the filesystem directory name for a grid cell."""
    if mode == "hash":
        return run_id
    if mode == "dgp":
        return dgp
    if mode == "slug":
        if seed is None:
            return f"{dgp}__target-{target}"
        return f"{dgp}__target-{target}__seed-{seed}"
    raise ConfigError(f"unsupported grid.cell_dir mode: {mode!r}")


def _assert_unique_cell_dir_names(cells: list[CellSpec], *, mode: str) -> None:
    """Raise when ``grid.cell_dir`` would map two cells to the same directory."""
    seen: dict[str, CellSpec] = {}
    for cell in cells:
        prev = seen.get(cell.cell_dir_name)
        if prev is not None:
            raise ConfigError(
                f"grid.cell_dir={mode!r} produced duplicate directory name "
                f"{cell.cell_dir_name!r} for cells "
                f"({prev.dgp}, target={prev.target}, seed={prev.seed}, n={prev.n}) and "
                f"({cell.dgp}, target={cell.target}, seed={cell.seed}, n={cell.n}); "
                f"use cell_dir: slug or hash"
            )
        seen[cell.cell_dir_name] = cell


def _resolve_handcrafted_dgp(dgp: Mapping[str, Any], *, where: str) -> DGPSpec:
    """Build a ``DGPSpec`` for a ``handcrafted_table`` DGP entry.

    The entry names a fixture via ``source``; node count, sample count, edges,
    and targets default to the fixture's own values when not given in the YAML.
    """
    from causal.experiments.handcrafted import load_handcrafted, normalize_source

    dgp_id = _require_str(dgp.get("id"), where=f"{where}.id")
    source_raw = _require_str(dgp.get("source"), where=f"{where}.source")
    normalize_source(source_raw)
    fx = load_handcrafted(source_raw)

    nodes = dgp.get("nodes")
    if nodes is None:
        nodes_int = fx.nodes
    else:
        nodes_int = _require_int(nodes, where=f"{where}.nodes")

    n_val = dgp.get("n")
    if n_val is None:
        sample_n = len(fx.df)
    else:
        sample_n = _require_int(n_val, where=f"{where}.n")

    edges = _parse_edges(
        dgp.get("edges"),
        nodes=nodes_int,
        where=f"{where}.edges",
        required=False,
    )
    if not edges:
        edges = fx.edges

    targets_obj = dgp.get("targets")
    targets: tuple[str, ...] | None
    if targets_obj is None:
        targets = fx.resolved_learning_targets()
    else:
        t_list = _require_list(targets_obj, where=f"{where}.targets")
        targets = tuple(_require_str(t, where=f"{where}.targets[{i}]") for i, t in enumerate(t_list))

    return DGPSpec(
        id=dgp_id,
        nodes=nodes_int,
        edges=edges,
        n=sample_n,
        graph_type=str(dgp.get("graph_type", "handcrafted_table")),
        example_split=dgp.get("example_split"),
        source=source_raw,
        targets=targets,
    )


def load_config(path: Path) -> ExperimentConfig:
    """Load and validate an experiment YAML config (INFRA.md §3.1–3.3)."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)

    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:  # pragma: no cover
        raise ConfigError(f"YAML parse error: {e}") from e

    cfg = _require_dict(raw, where="config")

    experiment_id = _require_str(cfg.get("experiment_id"), where="experiment_id")
    if path.stem != experiment_id:
        raise ConfigError(
            f"experiment_id must match filename stem: {experiment_id!r} != {path.stem!r}"
        )

    description = cfg.get("description")
    if description is not None and not isinstance(description, str):
        raise ConfigError("description must be a string if present")

    defaults_obj = cfg.get("defaults")
    defaults = _require_dict(defaults_obj, where="defaults")
    _validate_defaults(defaults)

    dgps_obj = cfg.get("dgps")
    dgps_list = _require_list(dgps_obj, where="dgps")
    dgps: list[DGPSpec] = []
    seen_ids: set[str] = set()
    for i, dgp_obj in enumerate(dgps_list):
        dgp = _require_dict(dgp_obj, where=f"dgps[{i}]")
        graph_type = dgp.get("graph_type")
        if graph_type == "handcrafted_table":
            spec = _resolve_handcrafted_dgp(dgp, where=f"dgps[{i}]")
        else:
            dgp_id = _require_str(dgp.get("id"), where=f"dgps[{i}].id")
            nodes = _require_int(dgp.get("nodes"), where=f"dgps[{i}].nodes")
            if nodes < 2:
                raise ConfigError(f"dgps[{i}].nodes must be >= 2")
            edges = _parse_edges(
                dgp.get("edges"), nodes=nodes, where=f"dgps[{i}].edges"
            )
            n_override = dgp.get("n")
            n_val = _require_int(n_override, where=f"dgps[{i}].n") if n_override is not None else None
            targets_obj = dgp.get("targets")
            targets: tuple[str, ...] | None = None
            if targets_obj is not None:
                t_list = _require_list(targets_obj, where=f"dgps[{i}].targets")
                targets = tuple(
                    _require_str(t, where=f"dgps[{i}].targets[{j}]")
                    for j, t in enumerate(t_list)
                )
            example_split = dgp.get("example_split")
            if example_split is not None:
                example_split = _require_str(example_split, where=f"dgps[{i}].example_split")
            spec = DGPSpec(
                id=dgp_id,
                nodes=nodes,
                edges=edges,
                n=n_val,
                graph_type=str(graph_type) if graph_type is not None else None,
                example_split=example_split,
                source=None,
                targets=targets,
            )
        if spec.id in seen_ids:
            raise ConfigError(f"duplicate dgp id: {spec.id}")
        seen_ids.add(spec.id)
        dgps.append(spec)

    grid_obj = _require_dict(cfg.get("grid"), where="grid")
    seed_obj = grid_obj.get("seed")
    if seed_obj is None:
        seeds: tuple[int, ...] = ()
    else:
        seeds = _parse_seeds(seed_obj, where="grid.seed")

    n_vals: tuple[int, ...] | None
    n_obj = grid_obj.get("n")
    if n_obj is None:
        n_vals = None
    else:
        n_list = _require_list(n_obj, where="grid.n")
        parsed_n: list[int] = []
        for j, n in enumerate(n_list):
            n_int = _require_int(n, where=f"grid.n[{j}]")
            if n_int <= 0:
                raise ConfigError("grid.n values must be positive")
            parsed_n.append(n_int)
        if not parsed_n:
            raise ConfigError("grid.n must be non-empty")
        n_vals = tuple(parsed_n)

    if n_vals is None and any(d.n is None for d in dgps):
        raise ConfigError("grid.n is required when a DGP omits per-dgp n")

    target_obj = grid_obj.get("target")
    if target_obj == "all":
        target: str | tuple[str, ...] = "all"
    else:
        t_list = _require_list(target_obj, where="grid.target")
        t_vals = [
            _require_str(t, where=f"grid.target[{k}]") for k, t in enumerate(t_list)
        ]
        if not t_vals:
            raise ConfigError("grid.target must be 'all' or a non-empty list")
        target = tuple(t_vals)

    cell_dir = _parse_cell_dir(grid_obj.get("cell_dir"), where="grid.cell_dir")

    provenance = cfg.get("provenance")
    if provenance is not None:
        provenance = _require_dict(provenance, where="provenance")

    return ExperimentConfig(
        experiment_id=experiment_id,
        description=description,
        defaults=defaults,
        dgps=tuple(dgps),
        grid=GridSpec(seeds=seeds, target=target, n=n_vals, cell_dir=cell_dir),
        provenance=provenance,
    )


def _dgp_graph_type(dgp: DGPSpec, defaults: Mapping[str, Any]) -> str:
    if dgp.graph_type is not None:
        return str(dgp.graph_type)
    return str(defaults.get("graph_type", "continuous"))


def _dgp_example_split(dgp: DGPSpec, defaults: Mapping[str, Any], graph_type: str) -> str:
    if dgp.example_split is not None:
        return str(dgp.example_split)
    if graph_type == "discrete":
        return str(defaults.get("example_split", "pick_target_variable"))
    if graph_type == "handcrafted_table":
        return "handcrafted"
    return str(defaults.get("example_split", "median"))


def expand_cells(cfg: ExperimentConfig, *, config_path: Path) -> list[CellSpec]:
    """Expand config into a deterministic cell list (INFRA.md §3.2)."""
    config_path = Path(config_path)
    config_hash = config_hash_from_path(config_path)
    grid_n = cfg.grid.n if cfg.grid.n is not None else ()
    cell_dir_mode = cfg.grid.cell_dir

    cells: list[CellSpec] = []
    for dgp in cfg.dgps:
        graph_type = _dgp_graph_type(dgp, cfg.defaults)
        example_split = _dgp_example_split(dgp, cfg.defaults, graph_type)

        if dgp.targets is not None:
            targets = list(dgp.targets)
        elif cfg.grid.target == "all":
            targets = [f"x{i}" for i in range(dgp.nodes)]
        else:
            targets = list(cfg.grid.target)

        for t in targets:
            if not t.startswith("x"):
                raise ConfigError(f"invalid target name: {t}")
            try:
                idx = int(t[1:])
            except ValueError as e:
                raise ConfigError(f"invalid target name: {t}") from e
            if idx < 0 or idx >= dgp.nodes:
                raise ConfigError(f"target {t} out of range for dgp {dgp.id}")

        n_values: tuple[int, ...]
        if dgp.n is not None:
            n_values = (dgp.n,)
        elif grid_n:
            n_values = grid_n
        else:
            raise ConfigError(f"DGP {dgp.id} has no n and grid.n is absent")

        # Empty seeds ⇒ one cell with seed=None (no seed dimension).
        seed_values: tuple[int | None, ...] = (
            tuple(cfg.grid.seeds) if cfg.grid.seeds else (None,)
        )

        for n in n_values:
            for seed in seed_values:
                for target in targets:
                    seed_token = "none" if seed is None else str(seed)
                    payload = (
                        f"{cfg.experiment_id}|{dgp.id}|{dgp.nodes}|{dgp.edges}|"
                        f"{n}|{seed_token}|{target}|{graph_type}|{config_hash}"
                    )
                    run_id = _short_run_id(payload)
                    dir_name = _cell_dir_name(
                        cell_dir_mode,
                        dgp=dgp.id,
                        target=target,
                        seed=seed,
                        run_id=run_id,
                    )
                    cells.append(
                        CellSpec(
                            experiment_id=cfg.experiment_id,
                            dgp=dgp.id,
                            nodes=dgp.nodes,
                            edges=dgp.edges,
                            n=n,
                            seed=seed,
                            target=target,
                            config_hash=config_hash,
                            run_id=run_id,
                            cell_dir_name=dir_name,
                            graph_type=graph_type,
                            example_split=example_split,
                            handcrafted_source=dgp.source,
                        )
                    )
    _assert_unique_cell_dir_names(cells, mode=cell_dir_mode)
    return cells
