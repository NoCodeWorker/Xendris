"""Input loading for v5.6 LOG_BOUNDARY control failure review."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.frontera_c_disposition.schemas import ControlFailureInputs


REQUIRED_INPUTS = {
    "v5_5_result": Path("docs/326_PHYGN_V5_5_LOG_BOUNDARY_NEGATIVE_CONTROLS_RESULTS.md"),
    "control_models": Path("data/frontera_c/controls/log_boundary_negative_control_models_v5_5.json"),
    "control_predictions": Path("data/frontera_c/controls/log_boundary_negative_control_predictions_v5_5.json"),
    "error_metrics": Path("data/frontera_c/controls/log_boundary_negative_control_error_metrics_v5_5.json"),
    "leakage_tests": Path("data/frontera_c/controls/log_boundary_leakage_tests_v5_5.json"),
    "loo_results": Path("data/frontera_c/controls/log_boundary_leave_one_out_results_v5_5.json"),
    "control_decision": Path("data/frontera_c/controls/log_boundary_control_decision_v5_5.json"),
    "next_gate_decision": Path("data/frontera_c/controls/log_boundary_v5_5_next_gate_decision.json"),
    "predictive_gain_smoke_test": Path("data/frontera_c/benchmark/log_boundary_predictive_gain_smoke_test_v5_4.json"),
    "ytrue_dataset": Path("data/frontera_c/ytrue/log_boundary_ytrue_dataset_v5_3.json"),
    "accepted_ytrue": Path("data/frontera_c/ytrue/log_boundary_accepted_ytrue_v5_3.json"),
}


def load_control_failure_inputs(root: str | Path = ".") -> ControlFailureInputs:
    repo_root = Path(root)
    missing = [str(path) for path in REQUIRED_INPUTS.values() if not (repo_root / path).exists()]
    data: dict[str, dict] = {}
    for key, rel_path in REQUIRED_INPUTS.items():
        path = repo_root / rel_path
        if path.exists() and path.suffix == ".json":
            data[key] = json.loads(path.read_text(encoding="utf-8"))
    return ControlFailureInputs(
        root=str(repo_root),
        missing_files=missing,
        control_decision=data.get("control_decision", {}),
        next_gate_decision=data.get("next_gate_decision", {}),
        predictive_gain_smoke_test=data.get("predictive_gain_smoke_test", {}),
        ytrue_dataset=data.get("ytrue_dataset", {}),
        accepted_ytrue=data.get("accepted_ytrue", {}),
        error_metrics=data.get("error_metrics", {}),
        leakage_tests=data.get("leakage_tests", {}),
        loo_results=data.get("loo_results", {}),
    )
