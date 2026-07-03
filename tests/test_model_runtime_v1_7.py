"""
Tests v1.7 — Model-Agnostic Runtime & Routing
"""

import pytest
from phyng.model_runtime.schemas import BackendRegistration
from phyng.model_runtime.backends import (
    register_model_backend,
    evaluate_backend_permission,
    route_model_task,
    clear_registry,
)


@pytest.fixture(autouse=True)
def setup_test_backends():
    clear_registry()
    # Register 3 standard test backends
    register_model_backend(
        BackendRegistration(
            backend_id="gpt-test-frontier",
            model_name="Frontier GPT",
            model_type="FRONTIER_API",
            quality_tier=1,
        )
    )
    register_model_backend(
        BackendRegistration(
            backend_id="llama-test-open",
            model_name="Llama 3 Open",
            model_type="OPEN_SOURCE_API",
            quality_tier=2,
        )
    )
    register_model_backend(
        BackendRegistration(
            backend_id="local-phi",
            model_name="Phi 3 Local",
            model_type="LOCAL_LLM",
            quality_tier=3,
        )
    )
    register_model_backend(
        BackendRegistration(
            backend_id="rule-test",
            model_name="Deterministic gate",
            model_type="RULE_BASED",
            quality_tier=3,
        )
    )


def test_open_source_model_allowed_for_low_risk():
    # Low-risk task: idea_intake
    perm = evaluate_backend_permission("llama-test-open", "idea_intake")
    assert perm.is_blocked is False
    assert perm.permission_status == "MODEL_FULLY_ALLOWED_FOR_LOW_RISK"


def test_open_source_model_blocked_for_financial_execution():
    # High-risk task: financial_action or automated_execution
    perm_local = evaluate_backend_permission("local-phi", "automated_execution")
    assert perm_local.is_blocked is True
    assert perm_local.permission_status == "MODEL_BLOCKED_FOR_HIGH_RISK"

    perm_open = evaluate_backend_permission("llama-test-open", "automated_execution")
    # Open-source models can be blocked OR require human review
    assert perm_open.is_blocked is True or perm_open.requires_human_review is True


def test_rule_based_backend_allowed_for_gatekeeping():
    # Medium-risk task: gatekeeping
    perm = evaluate_backend_permission("rule-test", "gatekeeping")
    assert perm.is_blocked is False
    assert perm.permission_status == "MODEL_ALLOWED_WITH_VALIDATION"
    assert perm.requires_validation is True


def test_capability_routing():
    # High risk task: automated_execution -> should prefer HUMAN_REVIEW or FRONTIER_API
    rec = route_model_task("automated_execution")
    assert rec == "gpt-test-frontier"

    # Low risk task: proxy_suggestion -> prefers LOCAL_LLM / OPEN_SOURCE_API
    rec_low = route_model_task("proxy_suggestion")
    assert rec_low in ("local-phi", "llama-test-open")
