"""
Tests v1.7 — UX: Math Translator
"""

import pytest
from phyng.ux.idea_intake import IdeaIntake
from phyng.ux.math_translator import translate_intuition_to_testable_structure, translate_from_intake


def test_math_translator_suggests_observable_and_proxy():
    # Test for financial domain
    out_fin = translate_intuition_to_testable_structure(
        intuition="Volume and price movements are correlated.",
        domain="finance",
        intended_use="explore",
    )
    assert out_fin.label == "SUGGESTED_NOT_VALIDATED"
    assert "price" in out_fin.possible_x_variables or "volume" in out_fin.possible_x_variables
    assert any("volume" in p or "deviation" in p or "count" in p for p in out_fin.proxy_candidates)

    # Test for quantum domain
    out_q = translate_intuition_to_testable_structure(
        intuition="Boundary gravity kills coherence.",
        domain="quantum_decoherence",
        intended_use="explore",
    )
    assert any("visibility" in o or "decay" in o for o in out_q.possible_y_observables)
    assert any("contrast" in p or "decay" in p for p in out_q.proxy_candidates)


def test_translate_from_intake():
    intake = IdeaIntake(
        raw_intuition="Decoherence is fast.",
        domain="quantum_decoherence",
    )
    out = translate_from_intake(intake)
    assert out.idea_id == intake.idea_id
    assert len(out.test_plan_candidates) > 0
