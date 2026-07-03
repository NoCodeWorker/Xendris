from phyng.phi_curvature_minimal_campaign.schemas import PhiCurvatureYTrueCandidate
from phyng.phi_curvature_minimal_campaign.ytrue_qc import ytrue_candidate_passes_qc


def test_ytrue_requires_numeric_value():
    assert ytrue_candidate_passes_qc(_candidate(value=None, unit="dimensionless", source_hash="hash", location=True)) is False


def test_ytrue_requires_unit_when_dimensional():
    candidate = _candidate(value=1.0, unit=None, source_hash="hash", location=True, observable_class="DECOHERENCE_RATE")
    assert ytrue_candidate_passes_qc(candidate) is False


def test_ytrue_requires_location():
    assert ytrue_candidate_passes_qc(_candidate(value=1.0, unit="dimensionless", source_hash="hash", location=False)) is False


def test_ytrue_requires_hash():
    assert ytrue_candidate_passes_qc(_candidate(value=1.0, unit="dimensionless", source_hash=None, location=True)) is False


def _candidate(
    *,
    value: float | None,
    unit: str | None,
    source_hash: str | None,
    location: bool,
    observable_class: str = "VISIBILITY",
) -> PhiCurvatureYTrueCandidate:
    return PhiCurvatureYTrueCandidate(
        candidate_id="CAND",
        observable_id="OBS",
        source_id="SRC",
        source_hash=source_hash,
        observable_class=observable_class,
        variable_name="observable",
        value=value,
        unit=unit,
        source_location_type="page" if location else None,
        source_location_value="1" if location else None,
        extraction_method="TEST",
        provenance_status="PROVENANCE_COMPLETE",
        qc_status="PASS",
        can_enter_dataset=True,
    )
