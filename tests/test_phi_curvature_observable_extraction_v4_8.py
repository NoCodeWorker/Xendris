from pathlib import Path

from phyng.phi_curvature_minimal_campaign.observable_extraction import extract_candidate_observables
from phyng.phi_curvature_minimal_campaign.source_resolution import resolve_reference


def test_unresolved_source_cannot_enter_extraction(tmp_path: Path):
    record = resolve_reference(tmp_path, "Phys. Rev. A 102, 022101")

    observables = extract_candidate_observables(
        [record],
        [],
        {"observable_classes": ["VISIBILITY"], "proposed_observables": ["visibility"]},
    )

    assert observables[0].extraction_status == "SOURCE_NOT_EXTRACTION_READY"
    assert observables[0].numeric_candidate_present is False
