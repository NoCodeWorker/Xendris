from phyng.phi_curvature_minimal_campaign.dataset import build_minimal_dataset
from phyng.phi_curvature_minimal_campaign.schemas import PhiCurvatureAcceptedYTrue


def test_accepted_ytrue_does_not_create_predictive_gain():
    dataset = build_minimal_dataset([_accepted("1")])

    assert dataset.predictive_gain_status == "UNDEFINED_NOT_COMPUTED_IN_MINIMAL_CAMPAIGN"
    assert dataset.physical_claim_permission == "BLOCKED"


def test_threshold_reached_requires_three_ytrue():
    below = build_minimal_dataset([_accepted("1"), _accepted("2")])
    reached = build_minimal_dataset([_accepted("1"), _accepted("2"), _accepted("3")])

    assert below.threshold_reached is False
    assert reached.threshold_reached is True


def _accepted(suffix: str) -> PhiCurvatureAcceptedYTrue:
    return PhiCurvatureAcceptedYTrue(
        y_true_id=f"YTRUE-{suffix}",
        candidate_id=f"CAND-{suffix}",
        observable_id=f"OBS-{suffix}",
        source_id=f"SRC-{suffix}",
        source_hash=f"hash-{suffix}",
        observable_class="VISIBILITY",
        variable_name="visibility",
        value=0.5,
        unit="dimensionless",
        source_location_type="page",
        source_location_value="1",
        extraction_method="TEST",
    )
