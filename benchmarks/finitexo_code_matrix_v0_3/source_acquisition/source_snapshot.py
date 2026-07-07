"""Local source snapshot utilities.

This module intentionally does not fetch network resources. It only hashes
local snapshot material that already exists in the repository.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


def hash_local_snapshot(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot_exists(path: str | None) -> bool:
    return bool(path)

