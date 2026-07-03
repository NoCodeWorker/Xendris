from phyng.phi_curvature_minimal_campaign.dataset import build_minimal_dataset
from phyng.phi_curvature_minimal_campaign.next_gate import BLOCKED_CLAIMS, final_status_for_dataset


def test_no_physical_claim_created():
    assert "PHI_CURVATURE is validated." in BLOCKED_CLAIMS
    assert "PHI_CURVATURE validates Frontera C." in BLOCKED_CLAIMS


def test_no_accepted_ytrue_status_stays_pre_predictive_gain():
    dataset = build_minimal_dataset([])

    assert final_status_for_dataset(dataset) == "PHI_CURVATURE_NO_ACCEPTED_YTRUE_IN_MINIMAL_CAMPAIGN"
