"""PHI_GRADIENT source-pressure audit and deterministic fixtures."""

from __future__ import annotations

from phyng.core.compatibility import normalize_status
from phyng.source_pressure.schemas import (
    BenchmarkPressureRecord,
    PhiGradientSourcePressureResult,
    SourceCandidate,
)
from phyng.source_pressure.slots import build_phi_gradient_source_slots
from phyng.source_pressure.source_gate import assess_source_support


def run_phi_gradient_source_pressure_audit(sources: list[SourceCandidate]) -> PhiGradientSourcePressureResult:
    slots = build_phi_gradient_source_slots()
    assessments = [assess_source_support(source) for source in sources]
    negative = [assessment for assessment in assessments if assessment.status == "SOURCE_CONTRADICTS_CANDIDATE"]
    supported_statuses = {assessment.status for assessment in assessments if assessment.counts_as_support}
    has_observable_or_baseline = bool({"SOURCE_SUPPORTS_OBSERVABLE", "SOURCE_SUPPORTS_BASELINE"} & supported_statuses)
    has_component = "SOURCE_SUPPORTS_COMPONENT" in supported_statuses
    has_alpha_constraint = "SOURCE_CONSTRAINS_PARAMETER" in supported_statuses

    missing: list[str] = []
    if not has_observable_or_baseline:
        missing.append("observable_or_baseline_support")
    if not has_component:
        missing.append("gradient_transition_component_support")
    if not has_alpha_constraint:
        missing.append("alpha_like_parameter_constraint")

    if negative:
        status = "PHI_GRADIENT_CONTRADICTED_BY_SOURCE"
    elif has_observable_or_baseline and has_component:
        status = "PHI_GRADIENT_SOURCE_BACKED_LIMITED"
    elif any(assessment.status == "SOURCE_ANALOGY_ONLY" for assessment in assessments):
        status = "PHI_GRADIENT_SOURCE_ANALOGY_ONLY"
    elif not sources:
        status = "PHI_GRADIENT_SOURCE_AUDIT_BLOCKED"
    else:
        status = "PHI_GRADIENT_SOURCE_UNSUPPORTED"

    if status == "PHI_GRADIENT_SOURCE_BACKED_LIMITED" and missing == ["alpha_like_parameter_constraint"]:
        next_actions = ["search alpha-like parameter constraints", "search benchmark data", "keep physical claims blocked"]
    elif status == "PHI_GRADIENT_SOURCE_BACKED_LIMITED":
        next_actions = ["replace fixtures with real literature extracts", "search benchmark data", "keep physical claims blocked"]
    elif status == "PHI_GRADIENT_CONTRADICTED_BY_SOURCE":
        next_actions = ["address negative source before upgrade", "retain contradiction in report"]
    else:
        next_actions = ["collect concrete sources for missing slots", "reject analogy-only upgrade"]

    return PhiGradientSourcePressureResult(
        status=status,
        canonical_status=normalize_status(status, domain="source_pressure"),
        slots=slots,
        sources=sources,
        assessments=assessments,
        negative_sources=negative,
        missing_requirements=missing,
        allowed_claims=_allowed_claims(status),
        blocked_claims=_blocked_claims(),
        next_actions=next_actions,
        fixture_based=True,
    )


def source_analogy_only_fixture() -> SourceCandidate:
    return SourceCandidate(
        source_id="SRC-FIX-ANALOGY-001",
        title="Boundary and gradient language analogy fixture",
        source_type="fixture",
        slot_ids=["SLOT_4_GRADIENT_TRANSITION_OPERATORS"],
        extracted_claims=["Uses gradient and boundary words without observable or equations."],
        citation_quality="fixture_analogy_only",
    )


def source_observable_support_fixture() -> SourceCandidate:
    return SourceCandidate(
        source_id="SRC-FIX-OBS-001",
        title="Visibility decay observable fixture",
        source_type="fixture",
        slot_ids=["SLOT_1_DECOHERENCE_BASELINE_MODELS", "SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT"],
        extracted_claims=["Defines visibility decay as an observable linked to Gamma_env."],
        supported_components=["visibility decay", "baseline"],
        equations_found=["V(t)=exp(-Gamma_env*t)"],
        observables_found=["fringe visibility"],
    )


def source_gradient_component_support_fixture() -> SourceCandidate:
    return SourceCandidate(
        source_id="SRC-FIX-GRAD-001",
        title="Gradient transition component fixture",
        source_type="fixture",
        slot_ids=["SLOT_4_GRADIENT_TRANSITION_OPERATORS"],
        extracted_claims=["Transition gradient contributes to an effective rate term."],
        supported_components=["gradient transition component"],
        equations_found=["rate += |d phi / du|"],
    )


def source_parameter_constraint_fixture() -> SourceCandidate:
    return SourceCandidate(
        source_id="SRC-FIX-ALPHA-001",
        title="Alpha-like parameter constraint fixture",
        source_type="fixture",
        slot_ids=["SLOT_6_ALPHA_LIKE_PARAMETER_CONSTRAINTS"],
        extracted_claims=["Provides an upper bound on an alpha-like dimensionless rate ratio."],
        supported_components=["alpha constraint"],
        parameter_constraints_found=["0 <= alpha <= 1"],
    )


def source_negative_conflict_fixture() -> SourceCandidate:
    return SourceCandidate(
        source_id="SRC-FIX-NEG-001",
        title="Negative conflict fixture",
        source_type="fixture",
        slot_ids=["SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES"],
        extracted_claims=["Existing environmental decoherence bound overwhelms the candidate contribution."],
        contradicted_components=["candidate effective rate"],
        citation_quality="fixture_negative",
    )


def benchmark_baseline_only_fixture() -> BenchmarkPressureRecord:
    return BenchmarkPressureRecord(
        benchmark_id="BM-FIX-BASELINE-001",
        source_id="SRC-FIX-OBS-001",
        observable="visibility_decay",
        parameter_ranges={"m_kg": (1e-20, 1e-14), "L_m": (1e-9, 1e-5), "t_s": (0.0, 10.0)},
        data_type="fixture_range",
        supports_baseline=True,
        comparable_to_phi_gradient=True,
        has_visibility_or_decoherence_measure=True,
        has_environmental_baseline=True,
        citation_or_path="fixture://baseline",
        limitations=["baseline only"],
    )


def benchmark_candidate_limited_fixture() -> BenchmarkPressureRecord:
    return BenchmarkPressureRecord(
        benchmark_id="BM-FIX-CANDIDATE-001",
        source_id="SRC-FIX-GRAD-001",
        observable="visibility_decay",
        parameter_ranges={"m_kg": (1e-20, 1e-14), "L_m": (1e-9, 1e-5), "t_s": (0.0, 10.0)},
        data_type="fixture_comparable_range",
        supports_baseline=True,
        supports_candidate_component=True,
        constrains_alpha=True,
        comparable_to_phi_gradient=True,
        has_visibility_or_decoherence_measure=True,
        has_environmental_baseline=True,
        citation_or_path="fixture://candidate_limited",
        limitations=["fixture-based; real literature acquisition still required"],
    )


def benchmark_not_comparable_fixture() -> BenchmarkPressureRecord:
    return BenchmarkPressureRecord(
        benchmark_id="BM-FIX-NOT-COMPARABLE-001",
        source_id=None,
        observable="unrelated_observable",
        parameter_ranges={"temperature_K": (1.0, 10.0)},
        data_type="fixture_unrelated",
        comparable_to_phi_gradient=False,
        citation_or_path="fixture://not_comparable",
        limitations=["observable and ranges not comparable"],
    )


def default_source_fixtures(include_negative: bool = False) -> list[SourceCandidate]:
    sources = [
        source_analogy_only_fixture(),
        source_observable_support_fixture(),
        source_gradient_component_support_fixture(),
        source_parameter_constraint_fixture(),
    ]
    if include_negative:
        sources.append(source_negative_conflict_fixture())
    return sources


def default_benchmark_fixtures() -> list[BenchmarkPressureRecord]:
    return [
        benchmark_baseline_only_fixture(),
        benchmark_candidate_limited_fixture(),
        benchmark_not_comparable_fixture(),
    ]


def _allowed_claims(status: str) -> list[str]:
    if status == "PHI_GRADIENT_SOURCE_BACKED_LIMITED":
        return ["PHI_GRADIENT has fixture-backed limited source support for required components."]
    return ["PHI_GRADIENT source pressure was assessed."]


def _blocked_claims() -> list[str]:
    return [
        "PHI_GRADIENT is physically validated.",
        "PHI_GRADIENT proves Frontera C.",
        "A source analogy validates the candidate.",
        "Benchmark pressure confirms the real effect.",
    ]
