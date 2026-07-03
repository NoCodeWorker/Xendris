"""Tests for v4.1 model registry."""

from __future__ import annotations

from phyng.model_comparison.model_registry import get_registered_models


def test_model_registry_contains_required_models() -> None:
    models = get_registered_models()
    model_ids = {m.model_id for m in models}
    expected = {
        "M_base",
        "M_candidate_debt_bounded",
        "M_negative_control_no_slot4",
        "M_parameter_constrained_variant",
        "M_observable_only_variant",
    }
    assert expected.issubset(model_ids)


def test_models_do_not_use_slot4_claim() -> None:
    models = get_registered_models()
    for m in models:
        # Enforce hardcoded False for gradient mechanism support
        assert m.uses_slot4_gradient_mechanism is False
        assert "gradient mechanism claim" in m.blocked_claims or "All gradient claims" in m.blocked_claims
