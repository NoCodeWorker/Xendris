"""Diagnostic-only expansion scoring."""

from __future__ import annotations

from .expansion_candidate import ExpansionCandidate
from .expansion_types import ExpansionSourceClass


def score_expansion_candidate(candidate: ExpansionCandidate) -> float:
    """Return a diagnostic score that never authorizes dataset promotion."""
    provenance = sum(
        1
        for value in (
            candidate.source_url,
            candidate.source_license,
            candidate.acquisition_record_ref,
            candidate.adaptation_record_ref,
            candidate.proposed_task_hash,
            candidate.provenance_ref,
        )
        if value
    ) / 6
    externality = {
        ExpansionSourceClass.EXTERNAL_VERIFIED: 1.0,
        ExpansionSourceClass.EXTERNAL_ADAPTED: 0.85,
        ExpansionSourceClass.SEMI_EXTERNAL_ADAPTED: 0.55,
        ExpansionSourceClass.MUTATED_FIXTURE: 0.2,
        ExpansionSourceClass.SYNTHETIC_LOCAL: 0.1,
        ExpansionSourceClass.UNKNOWN: 0.0,
    }[candidate.source_origin]
    preservation = max(0.0, min(1.0, candidate.semantic_preservation_score))
    contamination = 1.0 if candidate.contamination_risk == "LOW" else 0.4 if candidate.contamination_risk == "MEDIUM" else 0.0
    leakage = 1.0 if candidate.leakage_risk == "LOW" else 0.7 if candidate.leakage_risk == "MEDIUM" else 0.0
    task_validity = 1.0 if candidate.task_validity_status == "VALID" else 0.75 if candidate.task_validity_status == "VALID_WITH_WARNINGS" else 0.0
    benchmark_fit = 1.0 if candidate.benchmark_fit_status == "FIT_FOR_AGENTIC_PROGRAMMING" else 0.75 if candidate.benchmark_fit_status == "FIT_WITH_LIMITATIONS" else 0.0
    reproducibility = 0.0 if (candidate.provider_execution_required or candidate.network_required or candidate.secrets_required) else 1.0
    difficulty = 1.0 if candidate.difficulty_estimate in {"small", "medium", "large"} else 0.5
    return round(
        (
            provenance
            + externality
            + preservation
            + contamination
            + leakage
            + task_validity
            + benchmark_fit
            + reproducibility
            + difficulty
        )
        / 9,
        4,
    )
