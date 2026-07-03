"""Load source-pack seeds for exact extract review."""

from __future__ import annotations

from pathlib import Path

from phyng.source_pack_validation.loader import load_seed_pack
from phyng.source_pack_population.schemas import SeedSourceExtractPack, SeedSourceManifest


def load_exact_review_inputs(root: str | Path = ".") -> tuple[SeedSourceManifest | None, SeedSourceExtractPack | None, str | None]:
    return load_seed_pack(root)
