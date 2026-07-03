"""Exact reviewed extract pack construction."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.exact_extract_review.schemas import ExactReviewedExtract, ExactReviewedExtractPack
from phyng.source_pack_population.schemas import SeedSourceExtractPack, SeedSourceManifest


REVIEWED_EXTRACT_PACK_PATH = Path("data/real_sources/extracts/phi_gradient_extract_pack_v3_4.reviewed.json")
LOCATION_OUTPUT_PATH = Path("data/real_sources/extracts/phi_gradient_exact_extract_locations_v3_4.json")
EQUATION_OBSERVABLE_MAP_PATH = Path("data/real_sources/extracts/phi_gradient_equation_observable_map_v3_4.json")
PARAMETER_RANGE_MAP_PATH = Path("data/real_sources/extracts/phi_gradient_parameter_range_map_v3_4.json")


def build_unresolved_exact_extract_pack(
    manifest: SeedSourceManifest,
    seed_extract_pack: SeedSourceExtractPack,
) -> ExactReviewedExtractPack:
    titles = {entry.source_id: entry.title for entry in manifest.entries}
    extracts = [
        ExactReviewedExtract(
            exact_extract_id=f"EXACT-{seed.extract_id}",
            source_id=seed.source_id,
            slot_id=seed.slot_id,
            source_title=titles.get(seed.source_id),
            location_type="UNKNOWN_LOCATION_REQUIRES_REVIEW",
            location_value="",
            exact_quote=None,
            paraphrase_context=seed.extract_text_or_paraphrase,
            supported_components=list(seed.supported_components),
            contradicted_components=list(seed.contradicted_components),
            limitations=[*seed.limitations, "No exact quote, equation, observable, or range has been reviewed yet."],
            review_status="EXACT_EXTRACT_REQUIRES_LOCATION",
            reviewer_notes=["Generated from v3.2 seed paraphrase; not validation-ready."],
            validation_ready=False,
            manual_review_required=True,
        )
        for seed in seed_extract_pack.extracts
    ]
    return ExactReviewedExtractPack(
        source_manifest_id=manifest.manifest_id,
        extracts=extracts,
        notes=["v3.4 unresolved exact extract pack; no quotes or ranges were fabricated."],
    )


def write_exact_review_outputs(
    root: str | Path,
    exact_pack: ExactReviewedExtractPack,
    location_results,
    equation_map,
    parameter_map,
) -> dict[str, str]:
    repo_root = Path(root)
    paths = {
        "reviewed_extract_pack": REVIEWED_EXTRACT_PACK_PATH,
        "locations": LOCATION_OUTPUT_PATH,
        "equation_observable_map": EQUATION_OBSERVABLE_MAP_PATH,
        "parameter_range_map": PARAMETER_RANGE_MAP_PATH,
    }
    for path in paths.values():
        (repo_root / path).parent.mkdir(parents=True, exist_ok=True)
    (repo_root / REVIEWED_EXTRACT_PACK_PATH).write_text(_json(exact_pack.model_dump()), encoding="utf-8")
    (repo_root / LOCATION_OUTPUT_PATH).write_text(_json({"results": [item.model_dump() for item in location_results]}), encoding="utf-8")
    (repo_root / EQUATION_OBSERVABLE_MAP_PATH).write_text(_json(equation_map.model_dump()), encoding="utf-8")
    (repo_root / PARAMETER_RANGE_MAP_PATH).write_text(_json(parameter_map.model_dump()), encoding="utf-8")
    return {key: str(path) for key, path in paths.items()}


def _json(payload: dict) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"
