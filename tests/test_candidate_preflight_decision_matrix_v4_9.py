from pathlib import Path

from phyng.source_identity_preflight.availability import build_source_availability_matrix
from phyng.source_identity_preflight.decision import build_candidate_preflight_decision_matrix
from phyng.source_identity_preflight.identity_resolution import build_source_identity_resolution_matrix
from phyng.source_identity_preflight.inventory import build_candidate_family_source_inventory
from phyng.source_identity_preflight.loader import load_source_identity_preflight_inputs
from phyng.source_identity_preflight.observable_identity import build_observable_identity_matrix
from phyng.source_identity_preflight.ytrue_path import build_ytrue_path_plausibility_matrix

from tests.test_phygn_source_identity_preflight_campaign_v4_9 import write_prior_inputs


def test_candidate_partial_requires_human_lookup(tmp_path: Path):
    write_prior_inputs(tmp_path)
    inputs = load_source_identity_preflight_inputs(tmp_path)
    inventory = build_candidate_family_source_inventory(tmp_path, inputs)
    identities = build_source_identity_resolution_matrix(inventory)
    availability = build_source_availability_matrix(identities)
    observables = build_observable_identity_matrix(identities)
    paths = build_ytrue_path_plausibility_matrix(observables, availability)

    decisions = build_candidate_preflight_decision_matrix(inventory, identities, availability, observables, paths)

    assert any(record.preflight_status == "PREFLIGHT_REQUIRES_HUMAN_LOOKUP" for record in decisions)
    assert all(record.preflight_status != "PREFLIGHT_PASSED" for record in decisions)
