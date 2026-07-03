"""Next-gate decision for v5.7.3."""

from __future__ import annotations

from phyng.targeted_ytrue.schemas import DatasetQuality


def build_next_gate(quality: DatasetQuality, rejected_count: int) -> dict:
    if quality.total_accepted_ytrue_count >= 10 and quality.independent_source_count >= 2:
        status = "TARGETED_YTRUE_EXTRACTION_THRESHOLD_REACHED"
        allowed = "v5.8 - Multi-Source Benchmark & Out-of-Source Control Gate"
        rationale = "Accepted y_true threshold and independent-source threshold were reached."
    elif quality.new_accepted_ytrue_count > 0:
        status = "TARGETED_YTRUE_EXTRACTION_PARTIAL"
        allowed = "v5.7.4 - Targeted Human Figure/Table Review or Additional Source Download & y_true Expansion"
        rationale = "New y_true was accepted, but the v5.8 threshold was not reached."
    elif rejected_count > 0:
        status = "TARGETED_YTRUE_EXTRACTION_REQUIRES_HUMAN_FIGURE_REVIEW"
        allowed = "v5.7.4 - Human Figure Review or Supplementary Data Acquisition"
        rationale = "No new y_true passed QC; candidate values require human figure/condition review."
    else:
        status = "TARGETED_YTRUE_EXTRACTION_BLOCKED_NO_ACCEPTED_YTRUE"
        allowed = None
        rationale = "No accepted y_true was produced."
    return {
        "final_status": status,
        "new_accepted_ytrue_count": quality.new_accepted_ytrue_count,
        "total_accepted_ytrue_count": quality.total_accepted_ytrue_count,
        "independent_source_count": quality.independent_source_count,
        "benchmark_readiness": quality.benchmark_readiness,
        "allowed_next_phase": allowed,
        "blocked_next_phases": ["PredictiveGain computation", "Frontera C validation", "physical claim"],
        "rationale": rationale,
        "no_predictive_gain_computed": True,
        "benchmark_built": False,
        "physical_claim_created": False,
        "frontera_c_validated": False,
    }
