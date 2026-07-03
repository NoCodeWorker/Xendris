import pytest

from phyng.model_comparison.source_backed import SourceBackedModelSpec


def test_source_backed_model_spec_accepts_hypothetical_candidate():
    spec = SourceBackedModelSpec(
        model_id="MODEL-C",
        name="Candidate",
        model_role="CANDIDATE",
        formula="V_C(t)",
        support_status="HYPOTHETICAL_CANDIDATE",
        allowed_claims=["testable hypothesis"],
        forbidden_claims=["physically validated"],
    )

    assert spec.model_role == "CANDIDATE"
    assert spec.support_status == "HYPOTHETICAL_CANDIDATE"


def test_source_backed_model_spec_rejects_unknown_role():
    with pytest.raises(ValueError):
        SourceBackedModelSpec(
            model_id="MODEL-BAD",
            name="Bad",
            model_role="OTHER",
            formula="x",
            support_status="TOY_INTERNAL",
        )
