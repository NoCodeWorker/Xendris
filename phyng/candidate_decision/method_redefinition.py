"""Method redefinition module for v4.6 candidate freeze review."""

from __future__ import annotations

from typing import Any
from phyng.candidate_decision.schemas import MethodOnlyRedefinition

def redefine_as_method_only(inputs: dict[str, Any]) -> MethodOnlyRedefinition:
    allowed_method_roles = [
        "negative-control generator",
        "benchmark-shaping heuristic",
        "candidate-stress-test fixture",
        "source-pressure pipeline test case",
        "claim-gating regression fixture"
    ]

    prohibited_scientific_roles = [
        "physical model",
        "validated mechanism",
        "predictive model",
        "Frontera C evidence",
        "invariant confirmation"
    ]

    allowed_future_use = [
        "benchmark comparisons",
        "negative control validations",
        "pipeline integration testing"
    ]

    notes = [
        "Redefinition protects the codebase from false physical claims.",
        "The candidate remains valuable for testing and heuristic guidance."
    ]

    return MethodOnlyRedefinition(
        candidate_id="PHI_GRADIENT",
        redefinition_status="PHI_GRADIENT_REDEFINED_AS_METHOD_ONLY",
        allowed_method_roles=allowed_method_roles,
        prohibited_scientific_roles=prohibited_scientific_roles,
        allowed_future_use=allowed_future_use,
        required_label="METHOD_ONLY_EMPIRICALLY_UNGROUNDED",
        notes=notes,
    )
