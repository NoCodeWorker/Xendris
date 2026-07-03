"""Final gate for PHI_GRADIENT priority exact fill v3.5."""

from __future__ import annotations

from phyng.core.compatibility import normalize_status
from phyng.priority_exact_fill.equation_observable_map import (
    build_priority_equation_observable_map,
    write_priority_equation_observable_map,
)
from phyng.priority_exact_fill.loader import load_priority_exact_fill_inputs
from phyng.priority_exact_fill.parameter_range_map import (
    build_priority_parameter_range_map,
    write_priority_parameter_range_map,
)
from phyng.priority_exact_fill.priority_fill import (
    build_priority_fill_records,
    validate_priority_fill_locations,
    write_priority_fill_outputs,
)
from phyng.priority_exact_fill.schemas import (
    PhiGradientPriorityExactFillGateResult,
    PriorityEquationObservableMap,
    PriorityExactFillRecord,
    PriorityParameterRangeMap,
)
from phyng.priority_exact_fill.source_availability import classify_priority_source_availability


def run_phi_gradient_priority_exact_fill_gate(
    root: str = ".",
    priority_records: list[PriorityExactFillRecord] | None = None,
) -> PhiGradientPriorityExactFillGateResult:
    manifest, seed_pack, reviewed_pack, blocked_reason = load_priority_exact_fill_inputs(root)
    if blocked_reason or manifest is None or seed_pack is None or reviewed_pack is None:
        return _blocked_gate(blocked_reason or "Priority exact fill inputs could not be loaded.")
    availability = classify_priority_source_availability(manifest, root)
    records = priority_records or build_priority_fill_records(manifest, seed_pack, reviewed_pack, availability)
    location_records = validate_priority_fill_locations(records)
    equation_map = build_priority_equation_observable_map(records)
    parameter_map = build_priority_parameter_range_map(records)
    output_paths = write_priority_fill_outputs(root, records, location_records)
    output_paths["priority_equation_observable_map"] = write_priority_equation_observable_map(root, equation_map)
    output_paths["priority_parameter_range_map"] = write_priority_parameter_range_map(root, parameter_map)
    status = _status_for(records)
    return PhiGradientPriorityExactFillGateResult(
        status=status,
        canonical_status=normalize_status(status, domain="priority_exact_fill"),
        manifest=manifest,
        seed_extract_pack=seed_pack,
        source_availability=availability,
        priority_records=records,
        location_records=location_records,
        equation_observable_map=equation_map,
        parameter_range_map=parameter_map,
        priority_source_count=len(records),
        validation_ready_count=sum(1 for record in records if record.validation_ready),
        unresolved_count=sum(1 for record in records if not record.validation_ready),
        source_text_required_count=sum(1 for record in records if record.source_text_status != "SOURCE_TEXT_AVAILABLE_LOCAL"),
        negative_candidate_count=sum(1 for record in records if record.negative_constraint_text or record.contradicted_components),
        output_paths=output_paths,
        allowed_claims=_allowed_claims(status),
        blocked_claims=_blocked_claims(),
        next_actions=_next_actions(status),
    )


def _blocked_gate(reason: str) -> PhiGradientPriorityExactFillGateResult:
    status = "PHI_GRADIENT_PRIORITY_EXTRACT_FILL_BLOCKED"
    return PhiGradientPriorityExactFillGateResult(
        status=status,
        canonical_status=normalize_status(status, domain="priority_exact_fill"),
        equation_observable_map=PriorityEquationObservableMap(),
        parameter_range_map=PriorityParameterRangeMap(),
        blocked_reason=reason,
        allowed_claims=["Priority exact fill was blocked before output generation."],
        blocked_claims=_blocked_claims(),
        next_actions=["Restore v3.2 seed files and v3.4 reviewed exact extract pack, then rerun v3.5."],
    )


def _status_for(records: list[PriorityExactFillRecord]) -> str:
    if not records:
        return "PHI_GRADIENT_PRIORITY_EXTRACT_FILL_BLOCKED"
    ready_count = sum(1 for record in records if record.validation_ready)
    unavailable_count = sum(1 for record in records if record.source_text_status != "SOURCE_TEXT_AVAILABLE_LOCAL")
    no_content_count = sum(1 for record in records if record.source_text_status == "SOURCE_TEXT_AVAILABLE_LOCAL" and not _has_exact_content(record))
    if unavailable_count == len(records):
        return "PHI_GRADIENT_PRIORITY_EXTRACTS_REQUIRE_SOURCE_TEXT"
    if ready_count == len(records):
        return "PHI_GRADIENT_PRIORITY_EXTRACTS_ACQUIRED"
    if ready_count:
        return "PHI_GRADIENT_PRIORITY_EXTRACTS_PARTIAL"
    if no_content_count:
        return "PHI_GRADIENT_PRIORITY_EXTRACTS_NO_VALIDATABLE_CONTENT"
    return "PHI_GRADIENT_PRIORITY_EXTRACTS_REQUIRE_SOURCE_TEXT"


def _has_exact_content(record: PriorityExactFillRecord) -> bool:
    return bool(
        record.exact_quote
        or record.equation_text
        or record.observable_text
        or record.parameter_range_text
        or record.benchmark_range_text
        or record.negative_constraint_text
    )


def _allowed_claims(status: str) -> list[str]:
    if status == "PHI_GRADIENT_PRIORITY_EXTRACTS_PARTIAL":
        return ["Some priority exact fills may be ready for a downstream review gate."]
    if status == "PHI_GRADIENT_PRIORITY_EXTRACTS_ACQUIRED":
        return ["Priority exact fills are locally reviewable for the next validation gate."]
    return ["Priority exact fill was attempted under source-text controls."]


def _blocked_claims() -> list[str]:
    return [
        "Priority exact fill validates PHI_GRADIENT.",
        "Unresolved priority records count as source support.",
        "Availability of a source URL counts as exact source text.",
        "PHI_GRADIENT is physically validated.",
        "PHI_GRADIENT validates Frontera C.",
    ]


def _next_actions(status: str) -> list[str]:
    if status == "PHI_GRADIENT_PRIORITY_EXTRACTS_REQUIRE_SOURCE_TEXT":
        return ["Manually acquire local source text for the five priority sources, then rerun exact fill."]
    if status == "PHI_GRADIENT_PRIORITY_EXTRACTS_PARTIAL":
        return ["Separate validation-ready priority fills from unresolved source-text debt."]
    if status == "PHI_GRADIENT_PRIORITY_EXTRACTS_ACQUIRED":
        return ["Run a source-pressure validation gate using only validation-ready exact content."]
    if status == "PHI_GRADIENT_PRIORITY_EXTRACTS_NO_VALIDATABLE_CONTENT":
        return ["Review local source text and add exact quote, equation, observable, range, or negative constraint fields."]
    return ["Restore missing inputs and rerun v3.5."]
