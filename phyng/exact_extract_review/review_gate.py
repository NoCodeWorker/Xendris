"""Final gate for exact extract review v3.4."""

from __future__ import annotations

from phyng.core.compatibility import normalize_status
from phyng.exact_extract_review.equation_observable_map import build_equation_observable_map
from phyng.exact_extract_review.exact_extracts import build_unresolved_exact_extract_pack, write_exact_review_outputs
from phyng.exact_extract_review.loader import load_exact_review_inputs
from phyng.exact_extract_review.location_validation import validate_exact_extract_locations
from phyng.exact_extract_review.parameter_range_map import build_parameter_range_map
from phyng.exact_extract_review.schemas import (
    EquationObservableMap,
    ExactReviewedExtractPack,
    ParameterRangeMap,
    PhiGradientExactExtractReviewGateResult,
)


def run_phi_gradient_exact_extract_review_gate(
    root: str = ".",
    exact_pack: ExactReviewedExtractPack | None = None,
) -> PhiGradientExactExtractReviewGateResult:
    manifest, seed_extract_pack, blocked_reason = load_exact_review_inputs(root)
    if blocked_reason or manifest is None or seed_extract_pack is None:
        return _blocked_gate(blocked_reason or "Seed files could not be loaded.")

    reviewed_pack = exact_pack or build_unresolved_exact_extract_pack(manifest, seed_extract_pack)
    manifest_source_ids = {entry.source_id for entry in manifest.entries}
    location_results = validate_exact_extract_locations(reviewed_pack, manifest_source_ids)
    equation_map = build_equation_observable_map(reviewed_pack, manifest_source_ids)
    parameter_map = build_parameter_range_map(reviewed_pack, manifest_source_ids)
    output_paths = write_exact_review_outputs(root, reviewed_pack, location_results, equation_map, parameter_map)
    ready_count = sum(1 for result in location_results if result.validation_ready)
    exact_content_count = sum(1 for extract in reviewed_pack.extracts if _has_exact_content(extract))
    manual_before = sum(1 for extract in seed_extract_pack.extracts if extract.manual_review_required)
    manual_after = sum(1 for result in location_results if not result.validation_ready)
    status = _status_for(reviewed_pack, ready_count, exact_content_count, manual_after)
    return PhiGradientExactExtractReviewGateResult(
        status=status,
        canonical_status=normalize_status(status, domain="exact_extract_review"),
        manifest=manifest,
        seed_extract_pack=seed_extract_pack,
        exact_extract_pack=reviewed_pack,
        location_results=location_results,
        equation_observable_map=equation_map,
        parameter_range_map=parameter_map,
        manual_review_debt_before=manual_before,
        manual_review_debt_after=manual_after,
        exact_extract_count=len(reviewed_pack.extracts),
        validation_ready_count=ready_count,
        unresolved_extract_count=manual_after,
        equation_map_count=sum(1 for entry in equation_map.entries if entry.equation_text),
        observable_map_count=sum(1 for entry in equation_map.entries if entry.observable_text),
        parameter_range_count=sum(1 for entry in parameter_map.entries if entry.alpha_like_constraint or entry.gamma_env_constraint),
        benchmark_range_count=sum(1 for entry in parameter_map.entries if entry.comparability_status == "COMPARABLE_RANGE_READY"),
        negative_constraint_count=sum(1 for extract in reviewed_pack.extracts if extract.negative_constraint_text),
        output_paths=output_paths,
        allowed_claims=_allowed_claims(status),
        blocked_claims=_blocked_claims(),
        next_actions=_next_actions(status),
    )


def _blocked_gate(reason: str) -> PhiGradientExactExtractReviewGateResult:
    status = "PHI_GRADIENT_EXACT_EXTRACT_REVIEW_BLOCKED"
    return PhiGradientExactExtractReviewGateResult(
        status=status,
        canonical_status=normalize_status(status, domain="exact_extract_review"),
        exact_extract_pack=ExactReviewedExtractPack(),
        equation_observable_map=EquationObservableMap(),
        parameter_range_map=ParameterRangeMap(),
        blocked_reason=reason,
        allowed_claims=["Exact extract review was blocked before review outputs could be generated."],
        blocked_claims=_blocked_claims(),
        next_actions=["Restore v3.2 seed manifest and extract pack, then rerun exact extract review."],
    )


def _status_for(pack: ExactReviewedExtractPack, ready_count: int, exact_content_count: int, unresolved_count: int) -> str:
    if not pack.extracts:
        return "PHI_GRADIENT_EXACT_EXTRACTS_REQUIRE_MORE_REVIEW"
    if exact_content_count == 0:
        return "PHI_GRADIENT_EXACT_EXTRACTS_REQUIRE_MORE_REVIEW"
    if ready_count == 0:
        return "PHI_GRADIENT_EXACT_EXTRACTS_NO_VALIDATABLE_CONTENT"
    if unresolved_count:
        return "PHI_GRADIENT_EXACT_EXTRACTS_PARTIAL"
    return "PHI_GRADIENT_EXACT_EXTRACTS_ACQUIRED"


def _has_exact_content(extract) -> bool:
    return bool(
        extract.exact_quote
        or extract.equation_text
        or extract.observable_text
        or extract.parameter_range_text
        or extract.benchmark_range_text
        or extract.negative_constraint_text
    )


def _allowed_claims(status: str) -> list[str]:
    if status == "PHI_GRADIENT_EXACT_EXTRACTS_REQUIRE_MORE_REVIEW":
        return ["Exact extract review templates were generated and unresolved review debt was measured."]
    if status in {"PHI_GRADIENT_EXACT_EXTRACTS_PARTIAL", "PHI_GRADIENT_EXACT_EXTRACTS_ACQUIRED"}:
        return ["Some extracts may be validation-ready for the next gate."]
    return ["Exact source review was performed under conservative claim controls."]


def _blocked_claims() -> list[str]:
    return [
        "Exact extract review validates PHI_GRADIENT.",
        "A located quote is source support by itself.",
        "A located benchmark mention is benchmark data.",
        "PHI_GRADIENT has real source support.",
        "PHI_GRADIENT has benchmark support.",
        "PHI_GRADIENT is physically validated.",
        "PHI_GRADIENT validates Frontera C.",
    ]


def _next_actions(status: str) -> list[str]:
    if status == "PHI_GRADIENT_EXACT_EXTRACTS_REQUIRE_MORE_REVIEW":
        return ["Acquire exact quotes, equations, observables and ranges for the unresolved extracts.", "Do not rerun source-pressure validation until exact content exists."]
    if status == "PHI_GRADIENT_EXACT_EXTRACTS_PARTIAL":
        return ["Run v3.5 on validation-ready extracts and keep unresolved debt separate."]
    if status == "PHI_GRADIENT_EXACT_EXTRACTS_ACQUIRED":
        return ["Run v3.5 exact extract validation and limited source-pressure gate."]
    return ["Review exact extract quality before downstream validation."]
