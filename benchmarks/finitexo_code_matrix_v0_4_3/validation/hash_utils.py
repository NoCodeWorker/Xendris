"""Stable hashing utilities for v0.4.3 frozen artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping


def canonical_json_bytes(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def stable_json_hash(obj: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_json_bytes(obj)).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def hash_task(task: Mapping[str, Any]) -> str:
    return stable_json_hash({key: value for key, value in task.items() if key != "content_hash"})


def hash_manifest(manifest: Mapping[str, Any]) -> str:
    return stable_json_hash(manifest)


def hash_provenance(provenance: Mapping[str, Any]) -> str:
    return stable_json_hash(provenance)


def hash_human_review(record: Mapping[str, Any]) -> str:
    return stable_json_hash(record)
