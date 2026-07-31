"""Immutable, atomic writes and hashes for derived fixture artefacts."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import tempfile


FIXTURE_TOOLKIT_VERSION = 2


class ArtifactConflictError(FileExistsError):
    """Raised when a generated artefact would overwrite different bytes."""


def sha256_bytes(data: bytes) -> str:
    return f"sha256:{hashlib.sha256(data).hexdigest()}"


def file_sha256(path: Path | str) -> str:
    return sha256_bytes(Path(path).read_bytes())


def write_bytes_once(path: Path | str, data: bytes) -> Path:
    """Atomically create ``path`` or accept an already byte-identical file.

    A different existing file is never overwritten. The temporary file is
    hard-linked into place, so another writer cannot be replaced between the
    existence check and promotion.
    """
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if destination.is_file() and destination.read_bytes() == data:
            return destination
        raise ArtifactConflictError(
            f"refusing to overwrite non-identical frozen artefact: {destination}"
        )

    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=destination.parent,
            prefix=f".{destination.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
            temporary = Path(handle.name)
        temporary.chmod(0o644)
        try:
            os.link(temporary, destination)
        except FileExistsError:
            if destination.is_file() and destination.read_bytes() == data:
                return destination
            raise ArtifactConflictError(
                f"refusing to overwrite non-identical frozen artefact: {destination}"
            )
        return destination
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def write_text_once(path: Path | str, text: str) -> Path:
    return write_bytes_once(path, text.encode("utf-8"))
