"""Parameter and benchmark range mapping for exact extracts."""

from __future__ import annotations

from phyng.exact_extract_review.location_validation import is_validation_ready
from phyng.exact_extract_review.schemas import ExactReviewedExtractPack, ParameterRangeMap, ParameterRangeMapEntry


def build_parameter_range_map(pack: ExactReviewedExtractPack, manifest_source_ids: set[str]) -> ParameterRangeMap:
    entries: list[ParameterRangeMapEntry] = []
    for extract in pack.extracts:
        if not is_validation_ready(extract, manifest_source_ids):
            continue
        if not (extract.parameter_range_text or extract.benchmark_range_text):
            continue
        entries.append(
            ParameterRangeMapEntry(
                source_id=extract.source_id,
                exact_extract_id=extract.exact_extract_id,
                mass_range=_extract_field(extract.benchmark_range_text, "mass"),
                length_or_separation_range=_extract_field(extract.benchmark_range_text, "length"),
                time_range=_extract_field(extract.benchmark_range_text, "time"),
                visibility_or_decoherence_measure=_extract_field(extract.benchmark_range_text, "visibility"),
                environmental_conditions=_extract_field(extract.benchmark_range_text, "environment"),
                alpha_like_constraint=extract.parameter_range_text if extract.slot_id == "SLOT_6_ALPHA_LIKE_PARAMETER_CONSTRAINTS" else None,
                gamma_env_constraint=extract.parameter_range_text if extract.slot_id == "SLOT_1_DECOHERENCE_BASELINE_MODELS" else None,
                comparability_status=_comparability_status(extract),
                missing_requirements=_missing_requirements(extract),
            )
        )
    return ParameterRangeMap(entries=entries)


def _extract_field(text: str | None, marker: str) -> str | None:
    if text and marker.lower() in text.lower():
        return text
    return None


def _comparability_status(extract) -> str:
    missing = _missing_requirements(extract)
    if extract.benchmark_range_text and not missing:
        return "COMPARABLE_RANGE_READY"
    if extract.benchmark_range_text:
        return "PARTIAL_RANGE_REQUIRES_REVIEW"
    if extract.parameter_range_text:
        return "PARTIAL_RANGE_REQUIRES_REVIEW"
    return "REQUIRES_EXACT_VALUES"


def _missing_requirements(extract) -> list[str]:
    if not extract.benchmark_range_text:
        return ["benchmark_range_text"]
    required = {
        "mass range": "mass",
        "length/separation range": "length",
        "time range": "time",
        "visibility/decoherence measure": "visibility",
        "environmental limitations": "environment",
    }
    return [name for name, marker in required.items() if marker not in extract.benchmark_range_text.lower()]
