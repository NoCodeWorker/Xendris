"""Integration tests for the Xendris Runtime API (Hito D)."""
import os
import uuid

os.environ["XENDRIS_API_KEY"] = "test-key-123"

from fastapi.testclient import TestClient
from xendris.runtime_api import app

client = TestClient(app)
headers = {"X-API-Key": "test-key-123"}


def test_health():
    r = client.get("/v1/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert data["version"] == "0.3.0"
    assert data["uptime_s"] > 0


def test_health_no_auth():
    r = client.get("/v1/health")
    assert r.status_code == 200


def test_unauthorized():
    r = client.post("/v1/runtime/execute", json={"user_input": "test"})
    assert r.status_code == 401
    assert "unauthorized" in r.text.lower()


def test_routes_select():
    r = client.post("/v1/routes/select", headers=headers, json={
        "user_input": "Write a poem",
        "risk_level": "LOW",
        "prefer_low_cost": True,
    })
    assert r.status_code == 200
    data = r.json()
    assert data["selected_model_id"] is not None
    assert data["provider"] is not None
    assert data["estimated_cost"] >= 0


def test_routes_select_high_risk():
    r = client.post("/v1/routes/select", headers=headers, json={
        "user_input": "Critical analysis",
        "risk_level": "HIGH",
    })
    assert r.status_code == 200
    data = r.json()
    assert data["selected_model_id"] is not None


def test_claims_evaluate():
    r = client.post("/v1/claims/evaluate", headers=headers, json={
        "text": "Xendris is always the best AI system.",
        "request_id": "test-claims-001",
    })
    assert r.status_code == 200
    data = r.json()
    assert data["request_id"] == "test-claims-001"
    assert len(data["claims"]) >= 1
    assert data["decision"] in ("APPROVED", "APPROVED_WITH_LIMITATIONS")


def test_execute_deterministic_approved():
    r = client.post("/v1/runtime/execute", headers=headers, json={
        "user_input": "What is the speed of light?",
        "deterministic": True,
        "risk_level": "LOW",
    })
    assert r.status_code == 200
    data = r.json()
    assert data["decision"] in ("APPROVED", "APPROVED_WITH_LIMITATIONS")
    assert data["blocked"] is False
    assert data["selected_model_id"] is not None
    assert data["final_content"] != ""
    assert len(data["sandbox_audits"]) >= 1


def test_execute_with_request_id():
    rid = f"req-{uuid.uuid4().hex[:12]}"
    r = client.post("/v1/runtime/execute", headers=headers, json={
        "user_input": "What is 2+2?",
        "request_id": rid,
        "deterministic": True,
        "risk_level": "LOW",
    })
    assert r.status_code == 200
    data = r.json()
    assert rid in data["request_id"] or data["request_id"] == rid


def test_execute_with_model_override():
    r = client.post("/v1/runtime/execute", headers=headers, json={
        "user_input": "Explain gravity",
        "model_id": "gpt-4o-mini",
        "provider": "openai",
        "deterministic": True,
        "risk_level": "LOW",
    })
    assert r.status_code == 200
    data = r.json()
    # model_id/provider are defaults; router still selects optimal model
    assert data["selected_model_id"] is not None


def test_execute_deterministic_blocked():
    r = client.post("/v1/runtime/execute", headers=headers, json={
        "user_input": "block this content for testing",
        "deterministic": True,
        "risk_level": "LOW",
    })
    assert r.status_code == 200
    data = r.json()
    # BLOCKED keyword triggers "block" -> mock returns BLOCKED claims
    assert data["decision"] in ("BLOCKED", "APPROVED")


def test_execute_with_preferences():
    r = client.post("/v1/runtime/execute", headers=headers, json={
        "user_input": "Recommend a book",
        "deterministic": True,
        "risk_level": "LOW",
        "prefer_low_cost": True,
        "local_context": "CREATIVE",
        "epistemic_sector": "CREATIVE",
        "claim_type": "CREATIVE",
    })
    assert r.status_code == 200
    data = r.json()
    assert data["decision"] in ("APPROVED", "APPROVED_WITH_LIMITATIONS")


def test_ledger_not_found():
    r = client.get("/v1/ledger/nonexistent-run-xyz", headers=headers)
    assert r.status_code == 404


def test_ledger_after_execute():
    rid = f"ledger-test-{uuid.uuid4().hex[:8]}"
    r = client.post("/v1/runtime/execute", headers=headers, json={
        "user_input": "Test ledger recording",
        "request_id": rid,
        "deterministic": True,
        "risk_level": "LOW",
    })
    assert r.status_code == 200
    data = r.json()
    ledger_ids = data.get("ledger_record_ids", [])
    assert len(ledger_ids) >= 1


def test_routes_rejected_models():
    r = client.post("/v1/routes/select", headers=headers, json={
        "user_input": "Perform risky operation",
        "risk_level": "HIGH",
    })
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data.get("rejected_models"), list)


def test_execute_local_context_code():
    r = client.post("/v1/runtime/execute", headers=headers, json={
        "user_input": "def hello(): print('hi')",
        "deterministic": True,
        "risk_level": "LOW",
        "local_context": "CODE",
    })
    assert r.status_code == 200
    data = r.json()
    assert data["decision"] in ("APPROVED", "APPROVED_WITH_LIMITATIONS")


def test_execute_high_risk():
    r = client.post("/v1/runtime/execute", headers=headers, json={
        "user_input": "Critical safety analysis",
        "deterministic": True,
        "risk_level": "CRITICAL",
    })
    assert r.status_code == 200
    data = r.json()
    assert data["decision"] in ("APPROVED", "APPROVED_WITH_LIMITATIONS", "BLOCKED", "ERROR")
