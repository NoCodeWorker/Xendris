"""Hashing and local PDF verification helpers for v5.7.2."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path


def is_pdf_object(path: Path) -> bool:
    if not path.exists() or not path.is_file() or path.stat().st_size <= 0:
        return False
    with path.open("rb") as handle:
        return handle.read(5) == b"%PDF-"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def modified_time_utc(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()
