"""Command-line interface for validating and deriving causal fixture artefacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from causal.fixtures.artifacts import (
    ArtifactConflictError,
    FIXTURE_TOOLKIT_VERSION,
    file_sha256,
    write_text_once,
)
from causal.fixtures.analysis import (
    build_certificate,
    write_certificate_json,
    write_population_csv,
)
from causal.fixtures.interop import export_bif
from causal.fixtures.io import LoadedFixture, load_fixture
from causal.fixtures.sampling import write_sample_artifacts


def _file_hash(path: Path) -> str:
    return file_sha256(path)


def _path_for_manifest(path: Path, *, base: Path) -> str:
    try:
        return str(path.resolve().relative_to(base.resolve()))
    except ValueError:
        return str(path.resolve())


def _write_fixture_manifest(
    loaded: LoadedFixture,
    *,
    output_dir: Path,
    artifacts: Mapping[str, Path],
    certificate: Mapping[str, Any],
    bif_report: Mapping[str, Any] | None = None,
    sample_summary: Mapping[str, Any] | None = None,
) -> Path:
    fixture = loaded.fixture
    document: dict[str, Any] = {
        "fixture_manifest_schema_version": 1,
        "fixture_toolkit_version": FIXTURE_TOOLKIT_VERSION,
        "fixture": {
            "id": fixture.fixture_id,
            "title": fixture.title,
            "model_class": "positive_finite_discrete_causal_bayesian_network",
            "source_path": str(loaded.source_path),
            "source_hash": loaded.source_hash,
            "source_hash_basis": "exact UTF-8 source-file bytes",
            "document_hash": loaded.document_hash,
            "document_hash_basis": "canonical parsed YAML document",
            "semantic_hash": loaded.semantic_hash,
            "variables": list(fixture.variable_names),
            "edges": [list(edge) for edge in fixture.edges],
        },
        "derived_artifacts": {
            name: {
                "path": _path_for_manifest(path, base=output_dir),
                "sha256": _file_hash(path),
            }
            for name, path in sorted(artifacts.items())
        },
        "certificate_summary": {
            "causal_sufficiency": certificate["assumptions_and_results"][
                "causal_sufficiency"
            ]["status"],
            "causal_markov_condition": certificate["assumptions_and_results"][
                "causal_markov_condition"
            ]["status"],
            "ordinary_faithfulness": certificate["assumptions_and_results"][
                "ordinary_faithfulness"
            ]["status"],
            "ci_query_count": certificate["conditional_independence_audit"][
                "query_count"
            ],
            "mec_size": certificate["graph"]["markov_equivalence_class"]["size"],
        },
        "bif_round_trip": bif_report,
        "sample": sample_summary,
        "boundaries": [
            "the fixture graph and certificate are evaluator-only",
            "no target is selected during fixture definition or sampling",
            "no ABA Learning run is performed by this package",
            "no learned-rule-to-CPDAG decoder is asserted",
            "generated fixture artefacts are not experiment claims",
        ],
    }
    destination = output_dir / "fixture_manifest.json"
    write_text_once(
        destination, json.dumps(document, indent=2, sort_keys=True) + "\n"
    )
    return destination


def _preflight_bundle_directory(output_dir: Path, *, n: int, seed: int) -> None:
    """Reject stale or differently parameterised files before any bundle write."""
    if not output_dir.exists():
        return
    sample_stem = f"n{n}_seed{seed}"
    allowed = {
        Path("population.csv"),
        Path("certificate.json"),
        Path("model.bif"),
        Path("fixture_manifest.json"),
        Path("samples") / f"{sample_stem}.csv",
        Path("samples") / f"{sample_stem}.manifest.json",
    }
    existing = {
        path.relative_to(output_dir)
        for path in output_dir.rglob("*")
        if path.is_file()
    }
    unexpected = existing - allowed
    if unexpected:
        raise ArtifactConflictError(
            "output directory contains files from a different bundle: "
            + ", ".join(str(path) for path in sorted(unexpected))
        )
    manifest_path = output_dir / "fixture_manifest.json"
    if manifest_path.is_file():
        try:
            existing_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            raise ArtifactConflictError(
                f"cannot validate existing bundle manifest: {manifest_path}"
            ) from exc
        sample = existing_manifest.get("sample")
        if not isinstance(sample, dict) or sample.get("n") != n or sample.get("seed") != seed:
            raise ArtifactConflictError(
                f"output directory already contains a different frozen bundle: {output_dir}"
            )


def certify_to_directory(
    loaded: LoadedFixture, output_dir: Path
) -> tuple[dict[str, Any], dict[str, Path]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    population, certificate = build_certificate(loaded)
    population_path = write_population_csv(population, output_dir / "population.csv")
    certificate_path = write_certificate_json(
        certificate, output_dir / "certificate.json"
    )
    return certificate, {
        "population": population_path,
        "certificate": certificate_path,
    }


def build_artifact_bundle(
    loaded: LoadedFixture,
    *,
    output_dir: Path,
    n: int,
    seed: int,
) -> dict[str, Any]:
    """Build the population/certificate, BIF, and one frozen sample."""
    _preflight_bundle_directory(output_dir, n=n, seed=seed)
    certificate, artifacts = certify_to_directory(loaded, output_dir)

    bif_path = output_dir / "model.bif"
    bif_report = export_bif(loaded.fixture, bif_path)
    artifacts["bif"] = bif_path

    samples_dir = output_dir / "samples"
    sample_stem = f"n{n}_seed{seed}"
    sample_artifacts = write_sample_artifacts(
        loaded,
        n=n,
        seed=seed,
        csv_path=samples_dir / f"{sample_stem}.csv",
        manifest_path=samples_dir / f"{sample_stem}.manifest.json",
    )
    artifacts["sample_csv"] = sample_artifacts.csv_path
    artifacts["sample_manifest"] = sample_artifacts.manifest_path

    manifest_path = _write_fixture_manifest(
        loaded,
        output_dir=output_dir,
        artifacts=artifacts,
        certificate=certificate,
        bif_report=bif_report.as_dict(),
        sample_summary={
            "n": n,
            "seed": seed,
            "target": None,
            "csv_sha256": sample_artifacts.csv_hash,
            "unique_joint_states_observed": sample_artifacts.manifest[
                "empirical_table_summary"
            ]["unique_joint_states_observed"],
        },
    )
    return {
        "fixture_id": loaded.fixture.fixture_id,
        "output_dir": str(output_dir),
        "manifest": str(manifest_path),
        "faithfulness": certificate["assumptions_and_results"][
            "ordinary_faithfulness"
        ]["status"],
        "bif_round_trip_ok": bif_report.ok,
        "sample_n": n,
        "sample_seed": seed,
    }


def _add_fixture_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--fixture", type=Path, required=True, help="exact fixture YAML")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m causal.fixtures.cli",
        description="Validate and derive exact finite-discrete causal fixture artefacts.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser(
        "validate", help="validate schema, DAG, CPT coverage, and exact probabilities"
    )
    _add_fixture_argument(validate_parser)

    certify_parser = subparsers.add_parser(
        "certify", help="write exact population and graph/population certificate"
    )
    _add_fixture_argument(certify_parser)
    certify_parser.add_argument("--output-dir", type=Path, required=True)

    bif_parser = subparsers.add_parser(
        "export-bif", help="export a derived BIF and verify a pgmpy round trip"
    )
    _add_fixture_argument(bif_parser)
    bif_parser.add_argument("--output", type=Path, required=True)

    sample_parser = subparsers.add_parser(
        "sample", help="write one target-free IID table and sample manifest"
    )
    _add_fixture_argument(sample_parser)
    sample_parser.add_argument("--n", type=int, required=True)
    sample_parser.add_argument("--seed", type=int, default=42)
    sample_parser.add_argument("--output", type=Path, required=True)
    sample_parser.add_argument("--manifest", type=Path)

    build_parser_ = subparsers.add_parser(
        "build", help="derive certificate, BIF, and a frozen target-free sample"
    )
    _add_fixture_argument(build_parser_)
    build_parser_.add_argument("--output-dir", type=Path, required=True)
    build_parser_.add_argument("--n", type=int, default=50)
    build_parser_.add_argument("--seed", type=int, default=42)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    loaded = load_fixture(args.fixture)

    if args.command == "validate":
        result = {
            "validated": True,
            "fixture_id": loaded.fixture.fixture_id,
            "source_hash": loaded.source_hash,
            "document_hash": loaded.document_hash,
            "semantic_hash": loaded.semantic_hash,
            "variables": list(loaded.fixture.variable_names),
            "edges": [list(edge) for edge in loaded.fixture.edges],
            "topological_order": list(loaded.fixture.topological_order),
        }
    elif args.command == "certify":
        certificate, artifacts = certify_to_directory(loaded, args.output_dir)
        manifest_path = _write_fixture_manifest(
            loaded,
            output_dir=args.output_dir,
            artifacts=artifacts,
            certificate=certificate,
        )
        result = {
            "fixture_id": loaded.fixture.fixture_id,
            "output_dir": str(args.output_dir),
            "manifest": str(manifest_path),
            "faithfulness": certificate["assumptions_and_results"][
                "ordinary_faithfulness"
            ]["status"],
        }
    elif args.command == "export-bif":
        report = export_bif(loaded.fixture, args.output)
        result = {
            "fixture_id": loaded.fixture.fixture_id,
            "output": str(args.output),
            "round_trip": report.as_dict(),
        }
    elif args.command == "sample":
        artifacts = write_sample_artifacts(
            loaded,
            n=args.n,
            seed=args.seed,
            csv_path=args.output,
            manifest_path=args.manifest,
        )
        result = {
            "fixture_id": loaded.fixture.fixture_id,
            "output": str(artifacts.csv_path),
            "manifest": str(artifacts.manifest_path),
            "n": args.n,
            "seed": args.seed,
            "target": None,
        }
    elif args.command == "build":
        result = build_artifact_bundle(
            loaded,
            output_dir=args.output_dir,
            n=args.n,
            seed=args.seed,
        )
    else:  # pragma: no cover - argparse enforces known subcommands
        raise AssertionError(args.command)

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
