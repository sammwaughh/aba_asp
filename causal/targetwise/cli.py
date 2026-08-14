"""CLI for validating, preparing, and running target-complete collections."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from causal.targetwise.collection import (
    prepare_collection,
    run_collection,
    validate_collection_config,
)
from causal.targetwise.config import load_targetwise_config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m causal.targetwise.cli",
        description=(
            "Run ABA Learning once per variable over one frozen causal-fixture sample."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    parsers: dict[str, argparse.ArgumentParser] = {}
    for name, help_text in (
        ("validate", "validate the fixture, sample, encoding, and learner config"),
        ("prepare", "write every target's immutable task inputs and provenance"),
        ("run", "prepare and serially run selected targets"),
    ):
        subparser = subparsers.add_parser(name, help=help_text)
        parsers[name] = subparser
        subparser.add_argument("--config", type=Path, required=True)
        if name != "validate":
            subparser.add_argument(
                "--output-root",
                type=Path,
                help=(
                    "override causal/outputs/aba_learning/targetwise "
                    "(primarily for tests)"
                ),
            )
    parsers["run"].add_argument(
        "--targets",
        help=(
            "comma-separated subset of fixture variables to execute "
            "(default: every variable)"
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = load_targetwise_config(args.config)
    if args.command == "validate":
        bundle = validate_collection_config(config)
        result = {
            "validated": True,
            "fixture_id": bundle.fixture_id,
            "configuration_id": config.configuration_id,
            "configuration_hash": config.configuration_hash,
            "sample": bundle.sample_name,
            "n": bundle.n,
            "seed": bundle.seed,
            "sample_sha256": bundle.sample_hash,
            "targets": list(bundle.variables),
            "learning_mode": config.learning_mode,
            "joint_check_timeout_s": config.joint_check_timeout_s,
        }
    elif args.command == "prepare":
        prepared = prepare_collection(
            config,
            output_root=args.output_root,
        )
        result = {
            "prepared": True,
            "fixture_id": prepared.bundle.fixture_id,
            "configuration_id": config.configuration_id,
            "sample": prepared.bundle.sample_name,
            "targets": list(prepared.tasks),
            "output_directory": str(prepared.paths.root),
            "manifest": str(prepared.paths.manifest_path),
        }
    elif args.command == "run":
        selected = None
        if args.targets:
            selected = [item.strip() for item in args.targets.split(",") if item.strip()]
        prepared = run_collection(
            config,
            output_root=args.output_root,
            targets=selected,
        )
        manifest = json.loads(prepared.paths.manifest_path.read_text(encoding="utf-8"))
        result = {
            "completed": manifest.get("status") == "completed",
            "status": manifest.get("status"),
            "fixture_id": prepared.bundle.fixture_id,
            "configuration_id": config.configuration_id,
            "sample": prepared.bundle.sample_name,
            "targets": list(prepared.tasks),
            "executed_targets": [
                entry["target"]
                for entry in manifest.get("targets", [])
                if entry.get("outcome") is not None
            ],
            "outcome_counts": manifest.get("outcome_counts", {}),
            "output_directory": str(prepared.paths.root),
            "summary": str(prepared.paths.summary_markdown_path),
        }
    else:  # pragma: no cover - argparse enforces known commands
        raise AssertionError(args.command)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
