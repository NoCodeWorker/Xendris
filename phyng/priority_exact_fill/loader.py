"""Load v3.5 priority exact fill inputs."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.exact_extract_review.schemas import ExactReviewedExtractPack
from phyng.source_pack_population.schemas import SeedSourceExtractPack, SeedSourceManifest

MANIFEST_V3_2_PATH = Path("data/real_sources/phi_gradient_reviewed_manifest_v3_2.seed.json")
SEED_EXTRACT_V3_2_PATH = Path("data/real_sources/extracts/phi_gradient_extract_pack_v3_2.seed.json")
REVIEWED_EXTRACT_V3_4_PATH = Path("data/real_sources/extracts/phi_gradient_extract_pack_v3_4.reviewed.json")


def load_priority_exact_fill_inputs(
    root: str | Path = ".",
) -> tuple[SeedSourceManifest | None, SeedSourceExtractPack | None, ExactReviewedExtractPack | None, str | None]:
    repo_root = Path(root)
    required = [MANIFEST_V3_2_PATH, SEED_EXTRACT_V3_2_PATH, REVIEWED_EXTRACT_V3_4_PATH]
    for relative_path in required:
        if not (repo_root / relative_path).exists():
            return None, None, None, f"Missing input file: {relative_path}"
    manifest = SeedSourceManifest.model_validate(json.loads((repo_root / MANIFEST_V3_2_PATH).read_text(encoding="utf-8")))
    seed_extract_pack = SeedSourceExtractPack.model_validate(
        json.loads((repo_root / SEED_EXTRACT_V3_2_PATH).read_text(encoding="utf-8"))
    )
    reviewed_pack = ExactReviewedExtractPack.model_validate(
        json.loads((repo_root / REVIEWED_EXTRACT_V3_4_PATH).read_text(encoding="utf-8"))
    )
    return manifest, seed_extract_pack, reviewed_pack, None
