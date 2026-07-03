"""Tests for v4.5 external evidence loader."""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from phyng.external_evidence.loader import load_evidence_sprint_inputs


def test_missing_prior_artifacts_blocks_external_evidence(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_evidence_sprint_inputs(tmp_path)


def write_mock_v4_5_inputs(tmp_path: Path) -> None:
    # Create necessary subdirectories
    (tmp_path / "data/y_true/manual_extraction").mkdir(parents=True, exist_ok=True)
    (tmp_path / "data/observables").mkdir(parents=True, exist_ok=True)
    (tmp_path / "data/model_comparison").mkdir(parents=True, exist_ok=True)
    (tmp_path / "data/real_sources/pdfs").mkdir(parents=True, exist_ok=True)
    (tmp_path / "data/debts").mkdir(parents=True, exist_ok=True)
    (tmp_path / "data/audits/remediation").mkdir(parents=True, exist_ok=True)

    # Write files
    with open(tmp_path / "data/y_true/phi_gradient_v4_4_next_predictive_gain_inputs.json", "w") as f:
        json.dump({"ready_for_predictive_gain": False}, f)

    with open(tmp_path / "data/y_true/phi_gradient_assembled_y_true_dataset_v4_4.json", "w") as f:
        json.dump({"records": []}, f)

    with open(tmp_path / "data/y_true/phi_gradient_dataset_quality_report_v4_4.json", "w") as f:
        json.dump({}, f)

    with open(tmp_path / "data/y_true/manual_extraction/phi_gradient_manual_extraction_rejected_v4_4.json", "w") as f:
        json.dump({"rejected_records": []}, f)

    with open(tmp_path / "data/y_true/manual_extraction/phi_gradient_manual_extraction_review_records_v4_4.json", "w") as f:
        json.dump({"review_records": []}, f)

    with open(tmp_path / "data/y_true/phi_gradient_public_dataset_lookup_queue_v4_3.json", "w") as f:
        json.dump({"public_dataset_lookup_queue": []}, f)

    with open(tmp_path / "data/y_true/phi_gradient_supplementary_lookup_queue_v4_3.json", "w") as f:
        json.dump({"supplementary_lookup_queue": []}, f)

    with open(tmp_path / "data/observables/phi_gradient_normalized_observable_targets_v4_2.json", "w") as f:
        json.dump({"normalized_targets": []}, f)

    with open(tmp_path / "data/model_comparison/phi_gradient_model_predictions_v4_1.json", "w") as f:
        json.dump({"predictions": []}, f)

    with open(tmp_path / "data/real_sources/source_hashes_v3_6.json", "w") as f:
        json.dump({"hashes": []}, f)

    with open(tmp_path / "data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json", "w") as f:
        json.dump({"status": "OPEN_BLOCKING_FOR_GRADIENT_CLAIMS"}, f)

    with open(tmp_path / "data/audits/remediation/phygn_v4_4_2_continuation_gate.json", "w") as f:
        json.dump({"gate_status": "RESUME_ALLOWED_WITH_RESIDUAL_DEBT"}, f)

    with open(tmp_path / "data/audits/remediation/phygn_accepted_residual_audit_debt_v4_4_2.json", "w") as f:
        json.dump({}, f)


def test_loader_loads_successfully_when_present(tmp_path: Path) -> None:
    write_mock_v4_5_inputs(tmp_path)
    inputs = load_evidence_sprint_inputs(tmp_path)
    assert "assembled_dataset_v4_4" in inputs
    assert inputs["pdfs_dir_exists"] is True
    assert inputs["supplementary_dir_exists"] is False
