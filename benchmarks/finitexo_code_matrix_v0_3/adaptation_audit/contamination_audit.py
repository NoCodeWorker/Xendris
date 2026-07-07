"""Contamination audit for adapted source material."""

from __future__ import annotations

from benchmarks.finitexo_code_matrix_v0_3.source_acquisition import ContaminationRisk, OriginCandidate

from .adaptation_record import AdaptationRecord
from .adaptation_types import AdaptationType, LeakageRisk

INTERNAL_FIXTURE_HINTS = ("fixtures/", "local_fixture", "candidate_task_", "external_task_")
SELF_FAVORING_TERMS = ("designed for xendris", "must use xendris", "score by xendris")


def audit_contamination(record: AdaptationRecord) -> dict[str, object]:
    flags: list[str] = []
    rejection_reasons: list[str] = list(record.rejection_reasons)
    warnings: list[str] = list(record.warnings)

    candidate_text = " ".join(
        str(value)
        for value in [
            record.adaptation_summary,
            record.adapted_candidate_path,
            record.normalized_source_path,
            record.task_metadata,
        ]
    ).lower()

    if any(hint in candidate_text for hint in INTERNAL_FIXTURE_HINTS):
        flags.append("resembles_internal_fixture_naming")
    if any(term in candidate_text for term in SELF_FAVORING_TERMS):
        rejection_reasons.append("suspicious_self_favoring_language")
    if record.source_origin_candidate in {OriginCandidate.MUTATED_FIXTURE, OriginCandidate.SEMI_EXTERNAL_SYNTHETIC}:
        flags.append("source_origin_not_external")
    if record.adaptation_type in {AdaptationType.SYNTHETIC_EXPANSION, AdaptationType.MUTATED_INTERNAL_FIXTURE}:
        rejection_reasons.append("adaptation_type_not_external_safe")
    if record.structural_change_score > 0.65:
        warnings.append("high_structural_divergence")
    if not record.raw_source_hash:
        rejection_reasons.append("missing_raw_source_hash")
    if not record.adapted_candidate_hash:
        rejection_reasons.append("missing_adapted_candidate_hash")
    if not record.adaptation_summary:
        rejection_reasons.append("missing_adaptation_summary")
    if not record.acquisition_record_path:
        rejection_reasons.append("missing_source_acquisition_record")

    risk = record.contamination_risk
    if rejection_reasons and risk == ContaminationRisk.LOW:
        risk = ContaminationRisk.MEDIUM
    if record.leakage_risk == LeakageRisk.BLOCKED:
        risk = ContaminationRisk.BLOCKED

    return {
        "contamination_risk": risk,
        "leakage_risk": record.leakage_risk,
        "flags": flags,
        "rejection_reasons": rejection_reasons,
        "warnings": warnings,
    }

