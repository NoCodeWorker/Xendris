"""Global source-pressure decision engine for v3.9."""

from __future__ import annotations

from phyng.source_pressure_decision.schemas import (
    ExtractPressureRecord,
    SlotPressureSummary,
    BenchmarkAlignmentRecord,
    ContradictionLimitationMap,
    SourcePressureDecision,
)


def compute_decision(
    records: list[ExtractPressureRecord],
    slot_summaries: list[SlotPressureSummary],
    benchmark: BenchmarkAlignmentRecord,
    contradiction_map: ContradictionLimitationMap,
) -> SourcePressureDecision:
    """Compute the global source-pressure decision from classified extracts."""
    gradient_support = _has_gradient_component_support(records, slot_summaries)
    global_decisions = _compute_global_decisions(records, slot_summaries, benchmark, contradiction_map, gradient_support)
    primary = _primary_decision(global_decisions, contradiction_map)
    confidence = _global_confidence(records, global_decisions, contradiction_map)
    allowed = _allowed_claims(global_decisions, gradient_support)
    blocked = _blocked_claims()
    recommendations = _recommendations(global_decisions, gradient_support, contradiction_map)

    return SourcePressureDecision(
        validation_ready_count=len(records),
        global_decisions=global_decisions,
        primary_decision=primary,
        confidence=confidence,
        gradient_component_support=gradient_support,
        physical_claim_permission="BLOCKED",
        allowed_claims=allowed,
        blocked_claims=blocked,
        next_recommendations=recommendations,
        notes=[
            "Source pressure decision was performed.",
            "Physical claims remain blocked unless explicitly permitted by later experimental gates.",
        ],
    )


def _has_gradient_component_support(
    records: list[ExtractPressureRecord],
    slot_summaries: list[SlotPressureSummary],
) -> bool:
    """Critical rule: No SLOT_4 validation-ready extract → gradient_component_support = false."""
    slot4_records = [r for r in records if r.assigned_slot == "SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS"]
    if not slot4_records:
        return False
    slot4_support = [r for r in slot4_records if r.pressure_class == "SUPPORTS_GRADIENT_COMPONENT"]
    return len(slot4_support) > 0


def _compute_global_decisions(
    records: list[ExtractPressureRecord],
    slot_summaries: list[SlotPressureSummary],
    benchmark: BenchmarkAlignmentRecord,
    contradiction_map: ContradictionLimitationMap,
    gradient_support: bool,
) -> list[str]:
    """Compute all applicable global decisions."""
    decisions: list[str] = []

    # Contradiction dominates (rule 6: negative evidence priority)
    if contradiction_map.contradictions:
        decisions.append("PHI_GRADIENT_REAL_SOURCE_CONTRADICTED")

    # Benchmark data found
    if benchmark.benchmark_decision != "NO_BENCHMARK_EXTRACTS":
        decisions.append("PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND")

    # Limited source backing (requires baseline/observable clean + no dominating contradiction)
    has_baseline = any(r.pressure_class == "SUPPORTS_BASELINE_ONLY" for r in records)
    has_observable = any(r.pressure_class == "SUPPORTS_OBSERVABLE_ONLY" for r in records)
    contradiction_dominates = _contradiction_dominates(records)

    if (has_baseline or has_observable) and not contradiction_dominates:
        decisions.append("PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED")

    # Check for analogy-only
    support_like = [r for r in records if r.pressure_class.startswith("SUPPORTS_")]
    analogy = [r for r in records if r.pressure_class == "ANALOGY_ONLY"]
    if analogy and not support_like:
        decisions.append("PHI_GRADIENT_REAL_SOURCE_ANALOGY_ONLY")

    # Inconclusive fallback
    if not decisions:
        decisions.append("PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE")

    return decisions


def _contradiction_dominates(records: list[ExtractPressureRecord]) -> bool:
    """A weak positive must lose to a clean contradiction (rule 9)."""
    total_support = sum(r.pressure_score for r in records if r.pressure_score > 0)
    total_negative = abs(sum(r.pressure_score for r in records if r.pressure_score < 0))
    return total_negative > total_support


def _primary_decision(global_decisions: list[str], contradiction_map: ContradictionLimitationMap) -> str:
    """Select the primary (most significant) decision. Contradiction takes precedence."""
    priority = [
        "PHI_GRADIENT_REAL_SOURCE_CONTRADICTED",
        "PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED",
        "PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND",
        "PHI_GRADIENT_REAL_SOURCE_ANALOGY_ONLY",
        "PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE",
    ]
    for decision in priority:
        if decision in global_decisions:
            return decision
    return "PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE"


def _global_confidence(
    records: list[ExtractPressureRecord],
    decisions: list[str],
    contradiction_map: ContradictionLimitationMap,
) -> str:
    """Default LOW unless alignment is direct and slot coverage is strong."""
    if not records:
        return "LOW"
    slots_covered = len({r.assigned_slot for r in records})
    has_high = any(r.confidence == "HIGH" for r in records)
    medium_count = sum(1 for r in records if r.confidence == "MEDIUM")

    if has_high and slots_covered >= 4:
        return "HIGH"
    if medium_count >= 5 and slots_covered >= 3:
        return "MEDIUM"
    return "LOW"


def _allowed_claims(decisions: list[str], gradient_support: bool) -> list[str]:
    claims: list[str] = []
    if "PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED" in decisions:
        claims.append("The literature supports baseline decoherence framing.")
        claims.append("The literature supports visibility/coherence as a relevant observable.")
    if "PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND" in decisions:
        claims.append("The literature contains benchmark ranges relevant for model comparison.")
    if not gradient_support:
        claims.append("The current extract pack does not support the gradient-component mechanism.")
    if "PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE" in decisions:
        claims.append("The current source pressure is inconclusive.")
    if "PHI_GRADIENT_REAL_SOURCE_ANALOGY_ONLY" in decisions:
        claims.append("The current source pressure is analogy-only.")
    if "PHI_GRADIENT_REAL_SOURCE_CONTRADICTED" in decisions:
        claims.append("The candidate requires revision before model comparison.")
    claims.append("Physical claims remain blocked unless explicitly permitted by later experimental gates.")
    return claims


def _blocked_claims() -> list[str]:
    return [
        "PHI_GRADIENT is physically validated.",
        "Frontera C is validated.",
        "The invariant has empirical confirmation.",
        "Source pressure is experimental proof.",
        "Source pressure validates PHI_GRADIENT.",
        "Benchmark relevance validates physics.",
        "Baseline support validates gradient mechanism.",
        "Parameter constraints prove the model.",
    ]


def _recommendations(
    decisions: list[str],
    gradient_support: bool,
    contradiction_map: ContradictionLimitationMap,
) -> list[str]:
    recs: list[str] = []
    if "PHI_GRADIENT_REAL_SOURCE_CONTRADICTED" in decisions:
        recs.append("v4.0 — Candidate Revision or Kill/Pivot Gate")
        recs.append("Review contradicted components before any model update.")
    if "PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND" in decisions and "PHI_GRADIENT_REAL_SOURCE_CONTRADICTED" not in decisions:
        recs.append("v4.0 — Benchmark Dataset Construction & Observable Alignment")
    if "PHI_GRADIENT_REAL_SOURCE_ANALOGY_ONLY" in decisions:
        recs.append("v4.0 — Literature Gap Expansion for SLOT_4")
        recs.append("Seek new SLOT_4 literature.")
    if "PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE" in decisions:
        recs.append("v4.0 — Targeted Source Acquisition & Manual Review")
    if not gradient_support:
        recs.append("Seek exact Pedernales manual review for SLOT_4 content.")
        recs.append("Design benchmark-only model comparison without gradient-component claim.")
    if contradiction_map.limitations:
        recs.append("Run negative-control source pressure.")
    return recs
