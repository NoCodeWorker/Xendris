"""Load or create reviewed manifest and extract-pack inputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from phyng.reviewed_manifest.schemas import ReviewedSourceExtractPack, ReviewedSourceManifest


MANIFEST_JSON = Path("data/real_sources/phi_gradient_reviewed_manifest_v3_1.json")
MANIFEST_YAML = Path("data/real_sources/phi_gradient_reviewed_manifest_v3_1.yaml")
EXTRACT_PACK_JSON = Path("data/real_sources/extracts/phi_gradient_extract_pack_v3_1.json")
EXTRACT_PACK_YAML = Path("data/real_sources/extracts/phi_gradient_extract_pack_v3_1.yaml")


def load_or_create_reviewed_manifest_inputs(root: str | Path = ".") -> tuple[
    ReviewedSourceManifest,
    ReviewedSourceExtractPack,
    bool,
    bool,
]:
    repo_root = Path(root)
    manifest_path = _first_existing(repo_root, [MANIFEST_JSON, MANIFEST_YAML])
    extract_path = _first_existing(repo_root, [EXTRACT_PACK_JSON, EXTRACT_PACK_YAML])
    manifest_created = False
    extract_created = False

    if manifest_path is None:
        manifest_path = repo_root / MANIFEST_JSON
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest = ReviewedSourceManifest(notes=["Template created by v3.1; no real sources have been reviewed yet."])
        manifest_path.write_text(_json(manifest.model_dump()), encoding="utf-8")
        manifest_created = True
    else:
        manifest = ReviewedSourceManifest.model_validate(_load_mapping(manifest_path))

    if extract_path is None:
        extract_path = repo_root / EXTRACT_PACK_JSON
        extract_path.parent.mkdir(parents=True, exist_ok=True)
        extract_pack = ReviewedSourceExtractPack(
            manifest_id=manifest.manifest_id,
            notes=["Template created by v3.1; no extracts have been reviewed yet."],
        )
        extract_path.write_text(_json(extract_pack.model_dump()), encoding="utf-8")
        extract_created = True
    else:
        extract_pack = ReviewedSourceExtractPack.model_validate(_load_mapping(extract_path))

    return manifest, extract_pack, manifest_created, extract_created


def _first_existing(root: Path, candidates: list[Path]) -> Path | None:
    for candidate in candidates:
        path = root / candidate
        if path.exists():
            return path
    return None


def _load_mapping(path: Path) -> dict[str, Any]:
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise ValueError(f"YAML manifest requires PyYAML: {path}") from exc
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    return loaded or {}


def _json(payload: dict) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"
