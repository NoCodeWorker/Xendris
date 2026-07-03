import pytest

from phyng.model_comparison import ModelComparisonSpec, run_model_comparison
from phyng.model_comparison.models import boundary_aware_visibility


def _spec(y_true=None):
    return ModelComparisonSpec(
        comparison_id="TEST-CMP",
        campaign_id="CAMPAIGN-002",
        system_id="SYS-TEST",
        observable="visibility_loss",
        t=[0.0, 1.0, 2.0],
        parameters={"gamma_base": 0.1, "alpha": 0.2, "B": 0.5, "QB": 0.01},
        model_base_name="TOY_BASE",
        model_candidate_name="TOY_CANDIDATE",
        model_base_description="Toy base.",
        model_candidate_description="Toy candidate.",
        epsilon_exp=1e-6,
        error_metric="MAE",
        status="ACTIVE",
        y_true=y_true,
    )


def test_gain_none_without_y_true():
    result = run_model_comparison(_spec())

    assert result.gain_c is None
    assert result.error_base is None
    assert result.error_candidate is None
    assert result.predictive_status == "MODEL_DELTA_ONLY"
    assert result.evidence_level == 3


def test_gain_positive_when_candidate_better():
    y_true = boundary_aware_visibility([0.0, 1.0, 2.0], 0.1, 0.1)
    result = run_model_comparison(_spec(y_true=y_true))

    assert result.error_candidate == pytest.approx(0.0)
    assert result.gain_c is not None
    assert result.gain_c > 0
    assert result.predictive_status == "POSITIVE_TOY_GAIN"
    assert result.evidence_level == 4
