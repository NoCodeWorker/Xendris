"""Tests for v4.6 candidate method-only redefinition."""

from __future__ import annotations

from phyng.candidate_decision.method_redefinition import redefine_as_method_only


def test_phi_gradient_redefined_method_only() -> None:
    inputs = {}
    redef = redefine_as_method_only(inputs)
    assert redef.redefinition_status == "PHI_GRADIENT_REDEFINED_AS_METHOD_ONLY"
    assert redef.required_label == "METHOD_ONLY_EMPIRICALLY_UNGROUNDED"


def test_method_only_prohibits_physical_model_role() -> None:
    inputs = {}
    redef = redefine_as_method_only(inputs)
    assert "physical model" in redef.prohibited_scientific_roles
    assert "negative-control generator" in redef.allowed_method_roles
