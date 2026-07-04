"""Unit tests for Xendris v1.1 Provider Adapter Sandbox."""

from __future__ import annotations

import json
import pytest
from xendris.core.local.context import LocalContext
from xendris.core.sectors.sector import EpistemicSector
from xendris.core.trust.types import ClaimType, RiskLevel
from xendris.core.router.model_registry import ModelRegistry, ModelCapabilityProfile
from xendris.core.ledger import TrustLedgerWriter
from xendris.core.runtime import (
    RuntimeRequest,
    RuntimeResponse,
    AgenticTrustRuntime,
    ProviderAdapter,
    ProviderAdapterSandbox,
    SandboxAudit,
)


@pytest.fixture
def registry() -> ModelRegistry:
    reg = ModelRegistry()
    reg.register_model(ModelCapabilityProfile(
        model_id="gpt-4",
        provider="openai",
        supported_contexts=("PRODUCTION", "BENCHMARK"),
        supported_sectors=("FACTUAL", "PRODUCTION"),
        max_risk_level=RiskLevel.CRITICAL,
        cost_per_1k_input_tokens=0.03,
        cost_per_1k_output_tokens=0.06,
        expected_latency_ms=1000,
        supports_tools=True,
        supports_code=True,
        supports_json=True,
        supports_long_context=True,
        required_gates=(),
    ))
    return reg


def test_1_provider_adapter_default_http_post_raises_error():
    adapter = ProviderAdapter("gpt-4", "openai")
    req = RuntimeRequest(
        request_id="REQ-1",
        user_input="Hello",
        user_intent="test",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    with pytest.raises(RuntimeError, match="Direct network access blocked by default"):
        adapter.generate(req)


def test_2_sandbox_intercepts_openai_mock_completions():
    adapter = ProviderAdapter("gpt-4", "openai")
    sandbox = ProviderAdapterSandbox(adapter)
    
    url = "https://api.openai.com/v1/chat/completions"
    user_input = "Give me a mock response"
    mock_response = {
        "choices": [{
            "message": {
                "role": "assistant",
                "content": "CLAIM: OpenAI is integrated\nCLAIM_TYPE: FACTUAL\nSECTOR: FACTUAL\nCONTEXT: PRODUCTION\nEVIDENCE: deploy",
            }
        }]
    }
    sandbox.register_mock(url, user_input, 200, mock_response)
    
    req = RuntimeRequest(
        request_id="REQ-2",
        user_input=user_input,
        user_intent="test",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    resp = adapter.generate(req)
    assert "OpenAI is integrated" in resp.content
    assert len(sandbox.audits) == 1
    assert sandbox.audits[0].reason == "MOCK_RESPONSE_DISPATCHED"


def test_3_sandbox_intercepts_anthropic_mock_messages():
    adapter = ProviderAdapter("claude-3-opus", "anthropic")
    sandbox = ProviderAdapterSandbox(adapter)
    
    url = "https://api.anthropic.com/v1/messages"
    user_input = "Anthropic check"
    mock_response = {
        "content": [{
            "type": "text",
            "text": "CLAIM: Anthropic works\nCLAIM_TYPE: FACTUAL\nSECTOR: FACTUAL\nCONTEXT: PRODUCTION\nEVIDENCE: deploy",
        }]
    }
    sandbox.register_mock(url, user_input, 200, mock_response)
    
    req = RuntimeRequest(
        request_id="REQ-3",
        user_input=user_input,
        user_intent="test",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    resp = adapter.generate(req)
    assert "Anthropic works" in resp.content


def test_4_sandbox_intercepts_generic_mock():
    adapter = ProviderAdapter("custom-model", "generic-provider")
    sandbox = ProviderAdapterSandbox(adapter)
    
    url = "https://api.generic-provider.com/v1/completions"
    user_input = "Generic query"
    mock_response = {
        "text": "CLAIM: Generic text\nCLAIM_TYPE: FACTUAL\nSECTOR: FACTUAL\nCONTEXT: PRODUCTION\nEVIDENCE: deploy",
    }
    sandbox.register_mock(url, user_input, 200, mock_response)
    
    req = RuntimeRequest(
        request_id="REQ-4",
        user_input=user_input,
        user_intent="test",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    resp = adapter.generate(req)
    assert "Generic text" in resp.content


def test_5_sandbox_enforces_input_token_limit():
    adapter = ProviderAdapter("gpt-4", "openai")
    sandbox = ProviderAdapterSandbox(adapter, max_input_tokens=5)
    
    # 24 chars / 4 = 6 estimated tokens > 5
    req = RuntimeRequest(
        request_id="REQ-5",
        user_input="Very long input statement",
        user_intent="test",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    with pytest.raises(ValueError, match="INPUT_TOKEN_LIMIT_EXCEEDED"):
        adapter.generate(req)


def test_6_sandbox_enforces_output_token_limit():
    adapter = ProviderAdapter("gpt-4", "openai")
    sandbox = ProviderAdapterSandbox(adapter, max_output_tokens=5)
    
    url = "https://api.openai.com/v1/chat/completions"
    mock_response = {
        "choices": [{
            "message": {
                "role": "assistant",
                "content": "This response contains a significantly long message output.",
            }
        }]
    }
    sandbox.register_mock(url, "Test", 200, mock_response)
    
    req = RuntimeRequest(
        request_id="REQ-6",
        user_input="Test",
        user_intent="test",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    with pytest.raises(ValueError, match="OUTPUT_TOKEN_LIMIT_EXCEEDED"):
        adapter.generate(req)


def test_7_sandbox_enforces_cost_limit():
    adapter = ProviderAdapter("gpt-4", "openai")
    # Set limit to $0.0001
    sandbox = ProviderAdapterSandbox(adapter, max_cost=0.0001)
    
    url = "https://api.openai.com/v1/chat/completions"
    mock_response = {
        "choices": [{
            "message": {
                "role": "assistant",
                "content": "Some output content text",
            }
        }]
    }
    sandbox.register_mock(url, "Prompt", 200, mock_response)
    
    req = RuntimeRequest(
        request_id="REQ-7",
        user_input="Prompt",
        user_intent="test",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    with pytest.raises(ValueError, match="COST_LIMIT_EXCEEDED"):
        adapter.generate(req)


def test_8_sandbox_unauthorized_network_access_raises_error():
    adapter = ProviderAdapter("gpt-4", "openai")
    sandbox = ProviderAdapterSandbox(adapter, network_allowed=False)
    
    req = RuntimeRequest(
        request_id="REQ-8",
        user_input="Unregistered Prompt",
        user_intent="test",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    with pytest.raises(RuntimeError, match="NETWORK_ACCESS_BLOCKED"):
        adapter.generate(req)


def test_9_sandbox_estimates_tokens_correctly():
    adapter = ProviderAdapter("gpt-4", "openai")
    sandbox = ProviderAdapterSandbox(adapter)
    
    text = "Hello world! Test estimation"
    tokens = sandbox.estimate_tokens(text)
    # length 28 / 4 = 7
    assert tokens == 7


def test_10_sandbox_fuzzy_mock_matching():
    adapter = ProviderAdapter("gpt-4", "openai")
    sandbox = ProviderAdapterSandbox(adapter)
    
    url = "https://api.openai.com/v1/chat/completions"
    mock_response = {
        "choices": [{
            "message": {
                "role": "assistant",
                "content": "Fuzzy matched answer",
            }
        }]
    }
    sandbox.register_mock(url, "TriggerKey", 200, mock_response)
    
    req = RuntimeRequest(
        request_id="REQ-10",
        user_input="This input contains TriggerKey inside it.",
        user_intent="test",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    resp = adapter.generate(req)
    assert resp.content == "Fuzzy matched answer"


def test_11_sandbox_audit_contains_correct_fields():
    audit = SandboxAudit(
        endpoint="https://test.api",
        status_code=200,
        input_tokens=10,
        output_tokens=20,
        estimated_cost=0.015,
        network_allowed=False,
        blocked_by_sandbox=False,
        reason="MOCK",
    )
    d = audit.to_dict()
    assert d["endpoint"] == "https://test.api"
    assert d["status_code"] == 200
    assert d["input_tokens"] == 10
    assert d["output_tokens"] == 20
    assert d["estimated_cost"] == 0.015
    assert d["network_allowed"] is False
    assert d["blocked_by_sandbox"] is False
    assert d["reason"] == "MOCK"


def test_12_sandbox_audit_records_cost_rates():
    adapter = ProviderAdapter("gpt-4", "openai")
    sandbox = ProviderAdapterSandbox(adapter)
    
    url = "https://api.openai.com/v1/chat/completions"
    mock_response = {
        "choices": [{
            "message": {
                "role": "assistant",
                "content": "Short text",
            }
        }]
    }
    sandbox.register_mock(url, "Test cost rates", 200, mock_response)
    
    req = RuntimeRequest(
        request_id="REQ-12",
        user_input="Test cost rates",
        user_intent="test",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    adapter.generate(req)
    assert sandbox.audits[0].estimated_cost > 0.0


def test_13_sandbox_audit_records_mock_dispatch():
    adapter = ProviderAdapter("gpt-4", "openai")
    sandbox = ProviderAdapterSandbox(adapter)
    
    url = "https://api.openai.com/v1/chat/completions"
    mock_response = {
        "choices": [{
            "message": {
                "role": "assistant",
                "content": "Response content",
            }
        }]
    }
    sandbox.register_mock(url, "Test mock dispatch", 200, mock_response)
    
    req = RuntimeRequest(
        request_id="REQ-13",
        user_input="Test mock dispatch",
        user_intent="test",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    adapter.generate(req)
    assert len(sandbox.audits) == 1
    assert sandbox.audits[0].reason == "MOCK_RESPONSE_DISPATCHED"


def test_14_sandbox_cost_rate_customization():
    adapter = ProviderAdapter("gpt-4", "openai")
    sandbox = ProviderAdapterSandbox(adapter)
    # Set custom cost rates: ($0.10 input, $0.20 output per 1K tokens)
    sandbox.cost_rates["gpt-4"] = (0.10, 0.20)
    
    url = "https://api.openai.com/v1/chat/completions"
    mock_response = {
        "choices": [{
            "message": {
                "role": "assistant",
                "content": "Output",
            }
        }]
    }
    sandbox.register_mock(url, "Test customization", 200, mock_response)
    
    req = RuntimeRequest(
        request_id="REQ-14",
        user_input="Test customization",
        user_intent="test",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    adapter.generate(req)
    # input tokens: ~4 (chars 18 / 4 = 4), output: 1 (chars 6 / 4 = 1)
    # cost = (4 / 1000) * 0.10 + (1 / 1000) * 0.20 = 0.0004 + 0.0002 = 0.0006
    assert abs(sandbox.audits[0].estimated_cost - 0.0006) < 0.0001


def test_15_provider_adapter_parses_openai_error_status():
    adapter = ProviderAdapter("gpt-4", "openai")
    sandbox = ProviderAdapterSandbox(adapter)
    
    url = "https://api.openai.com/v1/chat/completions"
    error_response = {
        "error": {
            "message": "Billing limit reached",
            "type": "billing_error",
        }
    }
    sandbox.register_mock(url, "Fail trigger", 402, error_response)
    
    req = RuntimeRequest(
        request_id="REQ-15",
        user_input="Fail trigger",
        user_intent="test",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    with pytest.raises(RuntimeError, match="Billing limit reached"):
        adapter.generate(req)


def test_16_sandbox_integration_with_agentic_trust_runtime(registry: ModelRegistry):
    adapter = ProviderAdapter("gpt-4", "openai")
    sandbox = ProviderAdapterSandbox(adapter)
    
    url = "https://api.openai.com/v1/chat/completions"
    mock_response = {
        "choices": [{
            "message": {
                "role": "assistant",
                "content": "CLAIM: OpenAI pipeline works\nCLAIM_TYPE: FACTUAL\nSECTOR: FACTUAL\nCONTEXT: PRODUCTION\nEVIDENCE: deploy log is green",
            }
        }]
    }
    sandbox.register_mock(url, "Test integration", 200, mock_response)
    
    req = RuntimeRequest(
        request_id="REQ-16",
        user_input="Test integration",
        user_intent="test",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    runtime = AgenticTrustRuntime(registry, {"gpt-4": adapter})
    resp = runtime.execute(req, "RUN-16")
    assert resp.decision == "ANSWER"


def test_17_sandbox_integration_runs_pipeline_successfully(registry: ModelRegistry):
    adapter = ProviderAdapter("gpt-4", "openai")
    sandbox = ProviderAdapterSandbox(adapter)
    
    url = "https://api.openai.com/v1/chat/completions"
    mock_response = {
        "choices": [{
            "message": {
                "role": "assistant",
                "content": "CLAIM: Integration test passes\nLIMITATION: local sandbox limitation\nCLAIM_TYPE: FACTUAL\nSECTOR: FACTUAL\nCONTEXT: PRODUCTION\nEVIDENCE: deploy log is green",
            }
        }]
    }
    sandbox.register_mock(url, "Verify full run", 200, mock_response)
    
    req = RuntimeRequest(
        request_id="REQ-17",
        user_input="Verify full run",
        user_intent="test",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    runtime = AgenticTrustRuntime(registry, {"gpt-4": adapter})
    resp = runtime.execute(req, "RUN-17")
    assert resp.decision == "ANSWER_WITH_LIMITATIONS"
    assert "local sandbox limitation" in resp.limitations


def test_18_sandbox_integration_ledger_recording(registry: ModelRegistry):
    adapter = ProviderAdapter("gpt-4", "openai")
    sandbox = ProviderAdapterSandbox(adapter)
    writer = TrustLedgerWriter()
    
    url = "https://api.openai.com/v1/chat/completions"
    mock_response = {
        "choices": [{
            "message": {
                "role": "assistant",
                "content": "CLAIM: Ledger check\nCLAIM_TYPE: FACTUAL\nSECTOR: FACTUAL\nCONTEXT: PRODUCTION\nEVIDENCE: deploy log is green",
            }
        }]
    }
    sandbox.register_mock(url, "Ledger run", 200, mock_response)
    
    req = RuntimeRequest(
        request_id="REQ-18",
        user_input="Ledger run",
        user_intent="test",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    runtime = AgenticTrustRuntime(registry, {"gpt-4": adapter}, ledger_writer=writer)
    runtime.execute(req, "RUN-18")
    
    records = writer.export_records()
    final_records = [r for r in records if r.record_id == "REC-FINAL-REQ-18"]
    assert len(final_records) == 1
    assert final_records[0].decision == "ANSWER"


def test_19_sandbox_estimations_are_deterministic():
    adapter = ProviderAdapter("gpt-4", "openai")
    sandbox = ProviderAdapterSandbox(adapter)
    
    t1 = sandbox.estimate_tokens("Deterministic check")
    t2 = sandbox.estimate_tokens("Deterministic check")
    assert t1 == t2


def test_20_sandbox_real_network_validation_simulated_http_error():
    # If network is allowed but server is down / returns HTTP error:
    adapter = ProviderAdapter("gpt-4", "openai")
    sandbox = ProviderAdapterSandbox(adapter, network_allowed=True)
    
    # We register a mock response indicating HTTP 500 error
    url = "https://api.openai.com/v1/chat/completions"
    sandbox.register_mock(url, "Trigger server down", 500, {"error": "Server overloaded"})
    
    req = RuntimeRequest(
        request_id="REQ-20",
        user_input="Trigger server down",
        user_intent="test",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    with pytest.raises(RuntimeError, match="status 500"):
        adapter.generate(req)
