"""Equation and observable mapping for exact extracts."""

from __future__ import annotations

from phyng.exact_extract_review.location_validation import is_validation_ready
from phyng.exact_extract_review.schemas import EquationObservableMap, EquationObservableMapEntry, ExactReviewedExtractPack


def build_equation_observable_map(pack: ExactReviewedExtractPack, manifest_source_ids: set[str]) -> EquationObservableMap:
    entries: list[EquationObservableMapEntry] = []
    for extract in pack.extracts:
        if not is_validation_ready(extract, manifest_source_ids):
            continue
        if not (extract.equation_text or extract.observable_text):
            continue
        entries.append(
            EquationObservableMapEntry(
                source_id=extract.source_id,
                exact_extract_id=extract.exact_extract_id,
                equation_text=extract.equation_text,
                observable_text=extract.observable_text,
                model_role=_model_role(extract),
                slot_id=extract.slot_id,
                candidate_relevance="EXACT_EXTRACT_REQUIRES_NEXT_GATE_VALIDATION",
                limitations=list(extract.limitations),
            )
        )
    return EquationObservableMap(entries=entries)


def _model_role(extract) -> str:
    if extract.negative_constraint_text:
        return "NEGATIVE_CONSTRAINT"
    if extract.slot_id == "SLOT_1_DECOHERENCE_BASELINE_MODELS":
        return "DECOHERENCE_BASELINE"
    if extract.slot_id == "SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT":
        return "VISIBILITY_DECAY_OBSERVABLE"
    if extract.slot_id == "SLOT_4_GRADIENT_TRANSITION_OPERATORS":
        return "GRADIENT_COMPONENT"
    if extract.slot_id == "SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS":
        return "BENCHMARK_MODEL"
    if extract.slot_id == "SLOT_6_ALPHA_LIKE_PARAMETER_CONSTRAINTS":
        return "PARAMETER_CONSTRAINT"
    return "REQUIRES_REVIEW"
