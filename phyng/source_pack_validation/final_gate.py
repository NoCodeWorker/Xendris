"""Final gate for PHI_GRADIENT source-pack validation."""

from __future__ import annotations

from phyng.core.compatibility import normalize_status
from phyng.source_pack_validation.analogy_rejection import analogy_rejections
from phyng.source_pack_validation.benchmark_scoring import score_benchmark_comparability
from phyng.source_pack_validation.negative_pressure import score_negative_pressure
from phyng.source_pack_validation.schemas import (
    PhiGradientSourcePackValidationGateResult,
    SourcePackBenchmarkScoringResult,
    SourcePackNegativePressureResult,
    SourcePackSlotCoverageMatrix,
)


def build_blocked_gate(reason: str) -> PhiGradientSourcePackValidationGateResult:
    status = "PHI_GRADIENT_SOURCE_PACK_VALIDATION_BLOCKED"
    return PhiGradientSourcePackValidationGateResult(
        status=status,
        canonical_status=normalize_status(status, domain="source_pack_validation"),
        slot_coverage=SourcePackSlotCoverageMatrix(),
        benchmark_scoring=SourcePackBenchmarkScoringResult(status="BENCHMARK_SCORING_BLOCKED"),
        negative_pressure=SourcePackNegativePressureResult(status="NEGATIVE_PRESSURE_SCORING_BLOCKED"),
        blocked_reason=reason,
        allowed_claims=["Validation was blocked before source pressure could be assessed."],
        blocked_claims=_blocked_claims(status),
        next_actions=["Restore the v3.2 seed manifest and extract pack before rerunning validation."],
    )


def build_final_gate(manifest, extract_pack, validations, validated_extracts, slot_coverage) -> PhiGradientSourcePackValidationGateResult:
    benchmark = score_benchmark_comparability(validations)
    negative = score_negative_pressure(validations)
    status = _final_status(validations, slot_coverage, benchmark, negative)
    return PhiGradientSourcePackValidationGateResult(
        status=status,
        canonical_status=normalize_status(status, domain="source_pack_validation"),
        manifest=manifest,
        extract_pack=extract_pack,
        extract_validations=validations,
        validated_extracts=validated_extracts,
        slot_coverage=slot_coverage,
        benchmark_scoring=benchmark,
        negative_pressure=negative,
        validated_support_count=sum(1 for validation in validations if validation.counts_as_real_support),
        manual_review_count=sum(1 for validation in validations if validation.status == "EXTRACT_REQUIRES_MANUAL_REVIEW"),
        rejected_analogy_count=len(analogy_rejections(validations)),
        allowed_claims=_allowed_claims(status),
        blocked_claims=_blocked_claims(status),
        next_actions=_next_actions(status),
    )


def _final_status(validations, slot_coverage, benchmark, negative) -> str:
    if negative.negative_pressure_count:
        return "PHI_GRADIENT_REAL_SOURCE_CONTRADICTED"
    if benchmark.benchmark_comparable_count:
        return "PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND"
    if _source_backed_limited(slot_coverage):
        return "PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED"
    if validations and all(validation.status == "EXTRACT_REJECTED_ANALOGY_ONLY" for validation in validations):
        return "PHI_GRADIENT_REAL_SOURCE_ANALOGY_ONLY"
    if validations:
        return "PHI_GRADIENT_EXTRACT_VALIDATION_COMPLETED"
    return "PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE"


def _source_backed_limited(slot_coverage) -> bool:
    by_slot = {record.slot_id: record for record in slot_coverage.records}
    observable = (
        by_slot.get("SLOT_1_DECOHERENCE_BASELINE_MODELS")
        and by_slot["SLOT_1_DECOHERENCE_BASELINE_MODELS"].validated_support_count > 0
    ) or (
        by_slot.get("SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT")
        and by_slot["SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT"].validated_support_count > 0
    )
    component = (
        by_slot.get("SLOT_4_GRADIENT_TRANSITION_OPERATORS")
        and by_slot["SLOT_4_GRADIENT_TRANSITION_OPERATORS"].validated_support_count > 0
    )
    return bool(observable and component)


def _allowed_claims(status: str) -> list[str]:
    if status == "PHI_GRADIENT_EXTRACT_VALIDATION_COMPLETED":
        return ["Extract validation was completed; manual review debt remains."]
    if status == "PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED":
        return ["PHI_GRADIENT has limited real source pressure for specific validated components."]
    if status == "PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND":
        return ["PHI_GRADIENT has a comparable benchmark pressure candidate."]
    if status == "PHI_GRADIENT_REAL_SOURCE_CONTRADICTED":
        return ["PHI_GRADIENT is contradicted or constrained by validated source pressure."]
    return ["Source pack validation executed under conservative claim controls."]


def _blocked_claims(status: str) -> list[str]:
    claims = [
        "Seed extract validation proves PHI_GRADIENT.",
        "Manual-review extract counts as support.",
        "Benchmark candidate counts as benchmark data.",
        "PHI_GRADIENT is physically validated.",
        "PHI_GRADIENT validates Frontera C.",
        "Experimental confirmation.",
    ]
    if status != "PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND":
        claims.append("Benchmark-supported claim.")
    if status != "PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED":
        claims.append("Source-backed claim.")
    return claims


def _next_actions(status: str) -> list[str]:
    if status == "PHI_GRADIENT_EXTRACT_VALIDATION_COMPLETED":
        return ["Create exact-extract acquisition task.", "Prioritize high-value sources.", "Reject analogy-only paths."]
    if status == "PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED":
        return ["Schedule benchmark comparison.", "Target missing alpha constraints.", "Search negative sources."]
    if status == "PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND":
        return ["Schedule parameter alignment and numerical benchmark comparison."]
    if status == "PHI_GRADIENT_REAL_SOURCE_CONTRADICTED":
        return ["Trigger PHI_GRADIENT post-mortem.", "Down-rank candidate or narrow claim."]
    return ["Improve exact extract quality and rerun validation."]
