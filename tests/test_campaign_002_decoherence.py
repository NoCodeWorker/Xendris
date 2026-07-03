from pathlib import Path

from phyng.campaigns.campaign_002_decoherence import (
    Campaign002Input,
    run_campaign_002_decoherence_model_comparison,
)


def test_campaign_002_generates_toy_delta(tmp_path):
    result = run_campaign_002_decoherence_model_comparison(tmp_path)

    assert result.campaign_id == "CAMPAIGN-002"
    assert result.mode == "TOY_MODEL_COMPARISON"
    assert len(result.comparison.y_base) == len(result.comparison.y_candidate)
    assert len(result.comparison.delta_series) == len(result.comparison.y_base)
    assert result.comparison.gain_c is None
    assert result.comparison.predictive_status == "MODEL_DELTA_ONLY"


def test_campaign_002_blocks_decoherence_prediction(tmp_path):
    result = run_campaign_002_decoherence_model_comparison(tmp_path)

    assert "Phygn predicts gravitational decoherence." in result.comparison.blocked_claims
    assert result.comparison.maximum_allowed_claim_level == 3


def test_campaign_002_report_generated(tmp_path):
    result = run_campaign_002_decoherence_model_comparison(
        tmp_path,
        Campaign002Input(alpha=1e36, B=1e-38),
    )

    assert Path(result.report_path).exists()
    assert Path(result.model_report_path).exists()
    assert result.comparison.detectability_status in {
        "UNDETECTABLE_DIFFERENCE",
        "DETECTABLE_TOY_DIFFERENCE",
    }
