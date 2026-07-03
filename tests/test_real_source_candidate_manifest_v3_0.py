from phyng.real_source_acquisition.campaign_gate import run_phi_gradient_real_source_acquisition
from phyng.real_source_acquisition.candidate_manifest import ManifestOnlySourceAcquisitionBackend
from phyng.real_source_acquisition.schemas import RealSourceCandidate
from phyng.real_source_ingestion.extract_validation import real_source_negative_double


def test_negative_sources_can_block_upgrade():
    candidate = RealSourceCandidate(
        source_id="SRC-NEG-REAL-001",
        title="Real negative source",
        source_type="paper",
        targeted_slots=["SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES"],
        expected_components=["contradiction"],
        acquisition_status="REAL_SOURCE_AVAILABLE_LOCAL",
        local_path="local/negative-source.md",
        reason_for_inclusion="Contradicts the candidate mechanism.",
        is_support=False,
    )
    extract = real_source_negative_double().model_copy(
        update={
            "source_id": candidate.source_id,
            "is_test_double": False,
            "is_fixture": False,
        }
    )

    result = run_phi_gradient_real_source_acquisition(
        backend=ManifestOnlySourceAcquisitionBackend([candidate]),
        extracts_by_source_id={candidate.source_id: extract},
    )

    assert result.status == "PHI_GRADIENT_REAL_SOURCE_CONTRADICTED"
    assert result.negative_sources[0].blocks_upgrade is True
    assert "PHI_GRADIENT is physically validated." in result.blocked_claims
