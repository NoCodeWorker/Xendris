"""Source support versus analogy gate."""

from __future__ import annotations

from phyng.core.compatibility import normalize_status
from phyng.source_pressure.schemas import SourceCandidate, SourceSupportAssessment


def assess_source_support(source: SourceCandidate) -> SourceSupportAssessment:
    if source.contradicted_components:
        status = "SOURCE_CONTRADICTS_CANDIDATE"
        counts = False
        reasons = ["Source contradicts or constrains a candidate component."]
    elif source.benchmark_data_found:
        status = "SOURCE_PROVIDES_BENCHMARK_DATA"
        counts = True
        reasons = ["Source provides benchmark data."]
    elif source.parameter_constraints_found:
        status = "SOURCE_CONSTRAINS_PARAMETER"
        counts = True
        reasons = ["Source constrains an alpha-like or rate parameter."]
    elif _supports_baseline(source):
        status = "SOURCE_SUPPORTS_BASELINE"
        counts = True
        reasons = ["Source supports baseline visibility/decoherence model."]
    elif source.observables_found:
        status = "SOURCE_SUPPORTS_OBSERVABLE"
        counts = True
        reasons = ["Source supports an observable required by the candidate."]
    elif _supports_component(source):
        status = "SOURCE_SUPPORTS_COMPONENT"
        counts = True
        reasons = ["Source supports a concrete gradient/transition component with extractable structure."]
    elif source.extracted_claims:
        status = "SOURCE_ANALOGY_ONLY"
        counts = False
        reasons = ["Source has related language but no equation, observable, component or parameter constraint."]
    else:
        status = "SOURCE_REJECTED_DECORATIVE_ANALOGY"
        counts = False
        reasons = ["Source does not constrain the candidate."]

    return SourceSupportAssessment(
        source_id=source.source_id,
        status=status,
        counts_as_support=counts,
        supported_slots=source.slot_ids if counts else [],
        supported_components=list(source.supported_components),
        contradicted_components=list(source.contradicted_components),
        reasons=reasons,
        canonical_status=normalize_status(_domain_status(status), domain="source_pressure"),
    )


def _supports_component(source: SourceCandidate) -> bool:
    components = {component.lower() for component in source.supported_components}
    baseline_components = {"baseline", "decoherence baseline", "visibility decay"}
    return bool(source.supported_components and source.equations_found and not components <= baseline_components)


def _supports_baseline(source: SourceCandidate) -> bool:
    components = {component.lower() for component in source.supported_components}
    return bool(source.equations_found and {"baseline", "decoherence baseline", "visibility decay"} & components)


def _domain_status(source_status: str) -> str:
    if source_status == "SOURCE_CONTRADICTS_CANDIDATE":
        return "PHI_GRADIENT_CONTRADICTED_BY_SOURCE"
    if source_status == "SOURCE_ANALOGY_ONLY":
        return "PHI_GRADIENT_SOURCE_ANALOGY_ONLY"
    if source_status == "SOURCE_REJECTED_DECORATIVE_ANALOGY":
        return "PHI_GRADIENT_SOURCE_UNSUPPORTED"
    return "PHI_GRADIENT_SOURCE_PRESSURE_INCONCLUSIVE"
