from phyng.frontera_c_disposition.loader import load_control_failure_inputs


def test_missing_control_results_blocks_disposition(tmp_path):
    inputs = load_control_failure_inputs(tmp_path)

    assert inputs.missing_files
    assert "data\\frontera_c\\controls\\log_boundary_v5_5_next_gate_decision.json" in inputs.missing_files
