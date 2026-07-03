import json
from pathlib import Path

from phyng.source_identity_preflight.campaign import run_phygn_source_identity_preflight_campaign


def test_no_ytrue_created(tmp_path: Path):
    write_prior_inputs(tmp_path)

    result = run_phygn_source_identity_preflight_campaign(tmp_path)

    assert result.status in {
        "PHYGN_SOURCE_IDENTITY_PREFLIGHT_REQUIRES_HUMAN_LOOKUP",
        "PHYGN_SOURCE_IDENTITY_PREFLIGHT_NO_CANDIDATE_PASSED",
    }
    assert not (tmp_path / "data/preflight/source_identity/accepted_ytrue_v4_9.json").exists()


def test_no_predictive_gain_created(tmp_path: Path):
    write_prior_inputs(tmp_path)

    result = run_phygn_source_identity_preflight_campaign(tmp_path)

    assert all("PredictiveGain" in claim for claim in result.gate.blocked_claims if "PredictiveGain" in claim)
    assert not (tmp_path / "data/preflight/source_identity/predictive_gain_v4_9.json").exists()


def test_reports_include_canonical_status(tmp_path: Path):
    write_prior_inputs(tmp_path)

    result = run_phygn_source_identity_preflight_campaign(tmp_path)
    campaign_report = Path(result.report_paths["campaign"])
    text = campaign_report.read_text(encoding="utf-8")

    assert "Canonical Status" in text
    assert result.gate.candidate_count == 8


def write_prior_inputs(root: Path) -> None:
    payloads = {
        "data/phi_curvature/next/phi_curvature_v4_8_next_gate_decision.json": {
            "final_status": "PHI_CURVATURE_REJECTED_NO_RESOLVABLE_SOURCES",
        },
        "data/phi_curvature/sources/phi_curvature_source_resolution_v4_8.json": [
            {
                "source_ref_raw": "Phys. Rev. A 102, 022101",
                "source_id": "SRC-PHI-CURVATURE-PHYS-REV-A-102-022101",
                "resolution_status": "REQUIRES_EXTERNAL_LOOKUP",
            },
            {
                "source_ref_raw": "Nature Physics 15, 890",
                "source_id": "SRC-PHI-CURVATURE-NATURE-PHYSICS-15-890",
                "resolution_status": "REQUIRES_EXTERNAL_LOOKUP",
            },
        ],
        "data/phi_curvature/sources/phi_curvature_source_availability_v4_8.json": [],
        "data/candidate_decisions/next_candidate_family_selection_matrix_v4_6.json": [
            {"family_id": "PHI_CURVATURE", "previous_status": "PHI_CANDIDATE_SURVIVES_CONTROLS", "notes": []},
            {"family_id": "PHI_LOCALIZED_WINDOW", "previous_status": "PHI_CANDIDATE_SURVIVES_CONTROLS", "notes": []},
            {"family_id": "PHI_BANDPASS", "previous_status": "PHI_CANDIDATE_SURVIVES_CONTROLS", "notes": []},
            {"family_id": "PHI_GRADIENT", "previous_status": "PHI_GRADIENT_EMPIRICALLY_UNGROUNDED_FREEZE", "notes": []},
            {"family_id": "B_SUPPRESSED", "previous_status": "UNSUPPORTED", "notes": []},
            {"family_id": "QB_STRUCTURAL", "previous_status": "UNSUPPORTED", "notes": []},
            {"family_id": "LOG_BOUNDARY", "previous_status": "UNSUPPORTED", "notes": []},
            {"family_id": "THRESHOLD_SATURATION", "previous_status": "UNSUPPORTED", "notes": []},
        ],
        "data/candidate_decisions/phygn_v4_6_pivot_decision_v4_6.json": {
            "next_candidate_family": "PHI_CURVATURE",
        },
        "data/candidate_decisions/phi_gradient_method_only_redefinition_v4_6.json": {
            "required_label": "METHOD_ONLY_EMPIRICALLY_UNGROUNDED",
        },
        "data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json": {
            "status": "OPEN_BLOCKING_FOR_GRADIENT_CLAIMS",
        },
    }
    for rel_path, payload in payloads.items():
        path = root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload), encoding="utf-8")
