from phyng.frontera_c_disposition.allowed_future_roles import build_allowed_future_roles
from phyng.frontera_c_disposition.candidate_disposition import build_candidate_disposition
from phyng.frontera_c_disposition.control_failure_review import build_control_failure_review
from phyng.frontera_c_disposition.loader import load_control_failure_inputs


def test_log_boundary_retained_only_as_fixture():
    disposition = build_candidate_disposition(build_control_failure_review(load_control_failure_inputs(".")))
    roles = build_allowed_future_roles(disposition)

    assert "benchmark fixture" in roles.allowed_roles
    assert "negative-control fixture" in roles.allowed_roles
    assert "active Frontera C validation candidate" in roles.blocked_roles
    assert "physical mechanism" in roles.blocked_roles
