from pathlib import Path

from phyng.campaigns.frontera_c_targeted_ytrue_extraction import run


def test_reports_generated():
    result = run(".")
    expected = [
        "data/frontera_c/targeted_ytrue/targeted_ytrue_candidates_v5_7_3.json",
        "data/frontera_c/targeted_ytrue/targeted_accepted_ytrue_v5_7_3.json",
        "data/frontera_c/targeted_ytrue/targeted_rejected_ytrue_v5_7_3.json",
        "data/frontera_c/targeted_ytrue/targeted_ytrue_extraction_audit_trail_v5_7_3.json",
        "data/frontera_c/targeted_ytrue/visibility_decoherence_expanded_ytrue_dataset_v5_7_3.json",
        "data/frontera_c/targeted_ytrue/visibility_decoherence_dataset_quality_v5_7_3.json",
        "data/frontera_c/targeted_ytrue/v5_7_3_next_gate_decision.json",
        "reports/frontera_c/targeted_ytrue/targeted_ytrue_candidates_v5_7_3.md",
        "reports/frontera_c/targeted_ytrue/targeted_accepted_ytrue_v5_7_3.md",
        "reports/frontera_c/targeted_ytrue/targeted_rejected_ytrue_v5_7_3.md",
        "reports/frontera_c/targeted_ytrue/targeted_ytrue_extraction_audit_trail_v5_7_3.md",
        "reports/frontera_c/targeted_ytrue/visibility_decoherence_expanded_ytrue_dataset_v5_7_3.md",
        "reports/frontera_c/targeted_ytrue/visibility_decoherence_dataset_quality_v5_7_3.md",
        "reports/frontera_c/targeted_ytrue/v5_7_3_next_gate_decision.md",
        "reports/campaigns/FRONTERA-C-TARGETED-YTRUE-EXTRACTION-v5_7_3.md",
        "docs/356_PHYGN_V5_7_3_TARGETED_YTRUE_EXTRACTION_RESULTS.md",
    ]

    assert result.status in {
        "TARGETED_YTRUE_EXTRACTION_COMPLETED",
        "TARGETED_YTRUE_EXTRACTION_THRESHOLD_REACHED",
        "TARGETED_YTRUE_EXTRACTION_PARTIAL",
        "TARGETED_YTRUE_EXTRACTION_BLOCKED_NO_ACCEPTED_YTRUE",
        "TARGETED_YTRUE_EXTRACTION_REQUIRES_HUMAN_FIGURE_REVIEW",
        "TARGETED_YTRUE_EXTRACTION_REQUIRES_SUPPLEMENTARY_DATA",
        "TARGETED_YTRUE_EXTRACTION_BLOCKED_PROVENANCE_FAILURE",
        "FRONTERA_C_REQUIRES_DATASET_EXPANSION",
    }
    assert all(Path(path).exists() for path in expected)
