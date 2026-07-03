from pathlib import Path

from phyng.campaigns.frontera_c_reality_contact_candidate_family import run


def test_no_physical_claim_created():
    result = run(".")
    import json

    next_gate = json.loads(open("data/frontera_c/candidates/v5_9_next_gate_decision.json", encoding="utf-8").read())

    assert result["status"] in {
        "CANDIDATE_FAMILY_SELECTED_FOR_PREDICTIVE_GATE",
        "NO_CANDIDATE_WITH_REALITY_CONTACT",
        "CANDIDATE_SELECTION_REQUIRES_THEORY_REFORMULATION",
        "CANDIDATE_SELECTION_REQUIRES_NEW_OBSERVABLES",
        "CANDIDATE_SELECTION_REQUIRES_NEW_EXPERIMENT",
        "CANDIDATE_SELECTION_BLOCKED_BY_LEAKAGE",
        "CANDIDATE_SELECTION_BLOCKED_BY_MISSING_FEATURES",
        "CANDIDATE_SELECTION_BLOCKED_BY_SCIENTIFIC_DEBT",
    }
    assert next_gate["physical_claim_created"] is False
    assert next_gate["frontera_c_validated"] is False


def test_v59_reports_generated():
    run(".")
    expected = [
        "data/frontera_c/candidates/candidate_family_registry_v5_9.json",
        "data/frontera_c/candidates/candidate_feature_schema_v5_9.json",
        "data/frontera_c/candidates/candidate_prediction_rules_v5_9.json",
        "data/frontera_c/candidates/candidate_reality_contact_screen_v5_9.json",
        "data/frontera_c/candidates/candidate_leakage_screen_v5_9.json",
        "data/frontera_c/candidates/candidate_selection_decision_v5_9.json",
        "data/frontera_c/candidates/v5_9_next_gate_decision.json",
        "reports/frontera_c/candidates/candidate_family_registry_v5_9.md",
        "reports/frontera_c/candidates/candidate_feature_schema_v5_9.md",
        "reports/frontera_c/candidates/candidate_prediction_rules_v5_9.md",
        "reports/frontera_c/candidates/candidate_reality_contact_screen_v5_9.md",
        "reports/frontera_c/candidates/candidate_leakage_screen_v5_9.md",
        "reports/frontera_c/candidates/candidate_selection_decision_v5_9.md",
        "reports/campaigns/FRONTERA-C-REALITY-CONTACT-CANDIDATE-FAMILY-CONSTRUCTION-v5_9.md",
        "docs/374_PHYGN_V5_9_REALITY_CONTACT_CANDIDATE_FAMILY_RESULTS.md",
    ]

    assert all(Path(path).exists() for path in expected)
