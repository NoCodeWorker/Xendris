from phyng.synthetic_benchmark_design.detectability_protocol import build_detectability_protocol
from phyng.synthetic_benchmark_design.log_boundary import create_log_boundary_candidate_spec


def test_detectability_protocol_defines_max_abs_delta():
    protocol = build_detectability_protocol(create_log_boundary_candidate_spec())

    assert "max_abs_delta" in protocol.detectability_metric
    assert "delta(t)" in protocol.delta_equation
    assert "DETECTABLE_SYNTHETIC_DELTA" in protocol.detectability_classification_rule
    assert "FAIL_UNDETECTABLE_DELTA" in protocol.failure_classification_rules
