"""Stable hashing utilities for frozen benchmark artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping


HASH_ALGORITHM = "sha256"


def canonical_json_bytes(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def stable_json_hash(obj: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_json_bytes(obj)).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def task_hash_material(task: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in task.items() if key != "content_hash"}


def manifest_hash_material(manifest: Mapping[str, Any]) -> dict[str, Any]:
    return dict(manifest)


def hash_task(task: Mapping[str, Any]) -> str:
    return stable_json_hash(task_hash_material(task))


def hash_manifest(manifest: Mapping[str, Any]) -> str:
    return stable_json_hash(manifest_hash_material(manifest))


def hash_provenance(provenance: Mapping[str, Any]) -> str:
    return stable_json_hash(provenance)


def hash_file_json(path: Path) -> str:
    return stable_json_hash(load_json(path))
