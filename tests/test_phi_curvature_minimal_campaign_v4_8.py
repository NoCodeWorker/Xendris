import json
from pathlib import Path

from phyng.phi_curvature_minimal_campaign.campaign import run_phi_curvature_minimal_source_ytrue_campaign
from phyng.phi_curvature_minimal_campaign.dataset import build_minimal_dataset
from phyng.phi_curvature_minimal_campaign.next_gate import BLOCKED_CLAIMS, final_status_for_dataset
from phyng.phi_curvature_minimal_campaign.observable_extraction import extract_candidate_observables
from phyng.phi_curvature_minimal_campaign.schemas import (
    PhiCurvatureAcceptedYTrue,
    PhiCurvatureYTrueCandidate,
    SourceResolutionRecord,
)
from phyng.phi_curvature_minimal_campaign.source_availability import availability_for_source
from phyng.phi_curvature_minimal_campaign.source_resolution import resolve_reference
from phyng.phi_curvature_minimal_campaign.ytrue_qc import ytrue_candidate_passes_qc


RAW_REF = "Phys. Rev. A 99, 012345"


def test_missing_v47_screen_blocks_campaign(tmp_path: Path):
    result = run_phi_curvature_minimal_source_ytrue_campaign(tmp_path)

    assert result.status == "PHI_CURVATURE_MINIMAL_CAMPAIGN_BLOCKED_MISSING_SCREEN"
    assert result.inputs_loaded is False
    assert result.accepted_ytrue == []


def test_raw_citation_is_not_source(tmp_path: Path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "note.md").write_text(f"{RAW_REF}\nsource_hash: fake", encoding="utf-8")

    record = resolve_reference(tmp_path, RAW_REF)

    assert record.resolution_status == "REQUIRES_EXTERNAL_LOOKUP"
    assert "NO_LOCAL_TITLE_AUTHORS_DOI_OR_HASHED_SOURCE_OBJECT" in record.blockers


def test_unresolved_source_cannot_enter_extraction(tmp_path: Path):
    record = resolve_reference(tmp_path, RAW_REF)
    observables = extract_candidate_observables(
        [record],
        [],
        {"observable_classes": ["VISIBILITY"], "proposed_observables": ["fringe_visibility"]},
    )

    assert observables[0].extraction_status == "SOURCE_NOT_EXTRACTION_READY"
    assert "SOURCE_UNRESOLVED" in observables[0].blockers


def test_missing_local_pdf_requires_download(tmp_path: Path):
    record = SourceResolutionRecord(
        source_ref_raw=RAW_REF,
        source_id="SRC-PHI-CURVATURE-TEST",
        publication="Phys. Rev. A",
        page_or_article="012345",
        resolution_status="RESOLVED_EXACT",
        confidence="HIGH",
    )

    availability = availability_for_source(tmp_path, record)

    assert availability.availability_status == "SOURCE_REQUIRES_DOWNLOAD"
    assert availability.local_pdf_available is False
    assert availability.local_pdf_hash is None


def test_ytrue_requires_numeric_value():
    candidate = _candidate(value=None, unit="dimensionless", location=True, source_hash="abc")

    assert ytrue_candidate_passes_qc(candidate) is False


def test_ytrue_requires_unit_when_dimensional():
    candidate = _candidate(value=1.0, unit=None, location=True, source_hash="abc", observable_class="DECOHERENCE_RATE")

    assert ytrue_candidate_passes_qc(candidate) is False


def test_ytrue_requires_location():
    candidate = _candidate(value=1.0, unit="dimensionless", location=False, source_hash="abc")

    assert ytrue_candidate_passes_qc(candidate) is False


def test_ytrue_requires_hash():
    candidate = _candidate(value=1.0, unit="dimensionless", location=True, source_hash=None)

    assert ytrue_candidate_passes_qc(candidate) is False


def test_accepted_ytrue_does_not_create_predictive_gain():
    dataset = build_minimal_dataset([_accepted("1")])

    assert dataset.accepted_ytrue_count == 1
    assert dataset.predictive_gain_status == "UNDEFINED_NOT_COMPUTED_IN_MINIMAL_CAMPAIGN"
    assert dataset.physical_claim_permission == "BLOCKED"


def test_threshold_reached_requires_three_ytrue():
    below = build_minimal_dataset([_accepted("1"), _accepted("2")])
    reached = build_minimal_dataset([_accepted("1"), _accepted("2"), _accepted("3")])

    assert below.threshold_reached is False
    assert final_status_for_dataset(below) == "PHI_CURVATURE_MINIMAL_YTRUE_FOUND"
    assert reached.threshold_reached is True
    assert final_status_for_dataset(reached) == "PHI_CURVATURE_MINIMAL_YTRUE_THRESHOLD_REACHED"


def test_no_physical_claim_created(tmp_path: Path):
    _write_passed_inputs(tmp_path)

    result = run_phi_curvature_minimal_source_ytrue_campaign(tmp_path)

    assert result.dataset.physical_claim_permission == "BLOCKED"
    assert "PHI_CURVATURE is validated." in result.next_gate.blocked_claims
    assert "PHI_CURVATURE validates Frontera C." in result.next_gate.blocked_claims


def test_phi_gradient_remains_method_only(tmp_path: Path):
    _write_passed_inputs(tmp_path)

    run_phi_curvature_minimal_source_ytrue_campaign(tmp_path)
    result_doc = (tmp_path / "docs/315_PHYGN_V4_8_PHI_CURVATURE_MINIMAL_CAMPAIGN_RESULTS.md").read_text(encoding="utf-8")

    assert "PHI_GRADIENT remains method-only" in result_doc


def test_slot4_remains_open_and_scoped(tmp_path: Path):
    _write_passed_inputs(tmp_path)

    run_phi_curvature_minimal_source_ytrue_campaign(tmp_path)
    result_doc = (tmp_path / "docs/315_PHYGN_V4_8_PHI_CURVATURE_MINIMAL_CAMPAIGN_RESULTS.md").read_text(encoding="utf-8")

    assert "SLOT_4 remains open" in result_doc


def test_reports_include_canonical_status(tmp_path: Path):
    _write_passed_inputs(tmp_path)

    result = run_phi_curvature_minimal_source_ytrue_campaign(tmp_path)
    campaign_report = Path(result.report_paths["campaign"])
    text = campaign_report.read_text(encoding="utf-8")

    assert "Canonical Status" in text
    assert result.status == "PHI_CURVATURE_REJECTED_NO_RESOLVABLE_SOURCES"


def _candidate(
    *,
    value: float | None,
    unit: str | None,
    location: bool,
    source_hash: str | None,
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


def _write_passed_inputs(root: Path) -> None:
    payloads = {
        "data/candidate_screening/phi_curvature_screening_decision_v4_7.json": {
            "final_status": "PHI_CURVATURE_ACCESSIBILITY_SCREEN_PASSED",
        },
        "data/candidate_screening/phi_curvature_source_accessibility_screen_v4_7.json": {
            "known_source_refs": [RAW_REF],
        },
        "data/candidate_screening/phi_curvature_observable_accessibility_screen_v4_7.json": {
            "observable_classes": ["VISIBILITY"],
            "proposed_observables": ["fringe_visibility"],
        },
        "data/candidate_screening/phi_curvature_ytrue_accessibility_screen_v4_7.json": {},
        "data/candidate_screening/phi_curvature_public_dataset_screen_v4_7.json": {},
        "data/candidate_screening/phi_curvature_experimental_feasibility_screen_v4_7.json": {},
        "data/candidate_screening/phi_curvature_claim_risk_screen_v4_7.json": {},
        "data/candidate_decisions/phi_gradient_method_only_redefinition_v4_6.json": {
            "redefinition_status": "PHI_GRADIENT_REDEFINED_AS_METHOD_ONLY",
        },
        "data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json": {
            "debt_status": "OPEN_BLOCKING_FOR_GRADIENT_CLAIMS",
        },
    }
    for rel_path, payload in payloads.items():
        path = root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload), encoding="utf-8")
