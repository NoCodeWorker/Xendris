"""Load v3.2 seed packs for v3.3 validation."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.source_pack_population.seed_pack import EXTRACT_SEED_PATH, MANIFEST_SEED_PATH
from phyng.source_pack_population.schemas import SeedSourceExtractPack, SeedSourceManifest


def load_seed_pack(root: str | Path = ".") -> tuple[SeedSourceManifest | None, SeedSourceExtractPack | None, str | None]:
    repo_root = Path(root)
    manifest_path = repo_root / MANIFEST_SEED_PATH
    extract_path = repo_root / EXTRACT_SEED_PATH
    if not manifest_path.exists():
        return None, None, f"Missing seed manifest: {MANIFEST_SEED_PATH}"
    if not extract_path.exists():
        return None, None, f"Missing seed extract pack: {EXTRACT_SEED_PATH}"
    manifest = SeedSourceManifest.model_validate(json.loads(manifest_path.read_text(encoding="utf-8")))
    extract_pack = SeedSourceExtractPack.model_validate(json.loads(extract_path.read_text(encoding="utf-8")))
    return manifest, extract_pack, None
