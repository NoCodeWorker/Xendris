"""Reviewed extract pack helpers."""

from __future__ import annotations

from phyng.reviewed_manifest.schemas import ReviewedSourceExtractPack, ReviewedSourceManifest


def extract_source_ids(pack: ReviewedSourceExtractPack) -> set[str]:
    return {extract.source_id for extract in pack.extracts}


def manifest_entry_ids(manifest: ReviewedSourceManifest) -> set[str]:
    return {entry.source_id for entry in manifest.entries}
