from pathlib import Path

from phyng.source_identity_preflight.inventory import REQUIRED_FAMILIES, build_candidate_family_source_inventory
from phyng.source_identity_preflight.loader import load_source_identity_preflight_inputs

from tests.test_phygn_source_identity_preflight_campaign_v4_9 import write_prior_inputs


def test_phi_curvature_reflects_v48_rejection(tmp_path: Path):
    write_prior_inputs(tmp_path)
    inputs = load_source_identity_preflight_inputs(tmp_path)

    inventory = build_candidate_family_source_inventory(tmp_path, inputs)
    by_family = {record.family_id: record for record in inventory}

    assert set(REQUIRED_FAMILIES).issubset(by_family)
    assert by_family["PHI_CURVATURE"].previous_status == "PHI_CURVATURE_REJECTED_NO_RESOLVABLE_SOURCES"
    assert by_family["PHI_CURVATURE"].inventory_status == "HAS_RAW_REFS_ONLY"


def test_phi_gradient_remains_method_only(tmp_path: Path):
    write_prior_inputs(tmp_path)
    inputs = load_source_identity_preflight_inputs(tmp_path)

    inventory = build_candidate_family_source_inventory(tmp_path, inputs)
    gradient = [record for record in inventory if record.family_id == "PHI_GRADIENT"][0]

    assert gradient.previous_status == "METHOD_ONLY_EMPIRICALLY_UNGROUNDED"
