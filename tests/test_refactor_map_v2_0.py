from pathlib import Path

from phyng.repository_audit.refactor_map import generate_refactor_map
from phyng.repository_audit.structure import audit_repository_structure


def test_refactor_recommendations_have_risk_levels():
    audit = audit_repository_structure(Path("."))
    recommendations = generate_refactor_map(audit)

    assert recommendations
    assert all(recommendation.risk_level for recommendation in recommendations)


def test_high_risk_refactors_require_human_review():
    audit = audit_repository_structure(Path("."))
    recommendations = generate_refactor_map(audit)
    high_risk = [
        recommendation for recommendation in recommendations
        if recommendation.risk_level.startswith("HIGH_RISK")
    ]

    assert high_risk
    assert all(recommendation.requires_human_review for recommendation in high_risk)
    assert min(r.suggested_order for r in high_risk) > 3
