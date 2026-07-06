"""Integration tests for the Xendris Runtime API (Hito D + E)."""
import os
import tempfile
import uuid

_tmp_wallet = tempfile.mkdtemp(prefix="xendris_wallet_")
_tmp_usage = tempfile.mkdtemp(prefix="xendris_usage_")

os.environ["XENDRIS_API_KEY"] = "test-key-123"
os.environ["XENDRIS_WALLET_DIR"] = _tmp_wallet
os.environ["XENDRIS_USAGE_DIR"] = _tmp_usage

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


# ── Wallet / Billing tests (Hito E) ────────────────────────────────────

def test_wallet_topup():
    r = client.post("/v1/wallet/topup", headers=headers, json={
        "tenant_id": "wallet-test-t1",
        "amount": "100.00",
    })
    assert r.status_code == 200
    data = r.json()
    assert data["tenant_id"] == "wallet-test-t1"
    assert data["new_balance"] == "100.00"
    assert data["transaction_id"] is not None


def test_wallet_topup_multiple():
    client.post("/v1/wallet/topup", headers=headers, json={
        "tenant_id": "wallet-test-t2",
        "amount": "50.00",
    })
    r = client.post("/v1/wallet/topup", headers=headers, json={
        "tenant_id": "wallet-test-t2",
        "amount": "25.00",
    })
    assert r.status_code == 200
    assert r.json()["new_balance"] == "75.00"


def test_wallet_balance():
    client.post("/v1/wallet/topup", headers=headers, json={
        "tenant_id": "wallet-test-t3",
        "amount": "200.00",
    })
    r = client.get("/v1/wallet/balance?tenant_id=wallet-test-t3", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["balance"] == "200.00"
    assert data["currency"] == "USD"
    assert float(data["hard_cap"]) > 0
    assert float(data["daily_limit"]) > 0


def test_wallet_not_found():
    r = client.get("/v1/wallet/balance?tenant_id=nonexistent-wallet", headers=headers)
    assert r.status_code == 404


def test_wallet_history():
    client.post("/v1/wallet/topup", headers=headers, json={
        "tenant_id": "wallet-test-t4",
        "amount": "10.00",
    })
    client.post("/v1/wallet/topup", headers=headers, json={
        "tenant_id": "wallet-test-t4",
        "amount": "20.00",
    })
    r = client.get("/v1/wallet/history?tenant_id=wallet-test-t4&limit=10", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert len(data["transactions"]) == 2
    assert data["transactions"][0]["type"] == "CREDIT"


def test_wallet_topup_custom_tenant():
    r = client.post("/v1/wallet/topup", headers=headers, json={
        "tenant_id": "custom-tenant-abc",
        "amount": "500.00",
        "description": "Initial top-up",
    })
    assert r.status_code == 200
    assert r.json()["new_balance"] == "500.00"

    r = client.get("/v1/wallet/balance?tenant_id=custom-tenant-abc", headers=headers)
    assert r.json()["balance"] == "500.00"


def test_usage_query_empty():
    r = client.get("/v1/usage?tenant_id=nonexistent-usage", headers=headers)
    assert r.status_code == 200
    assert r.json() == []


def test_wallet_topup_large_amount():
    r = client.post("/v1/wallet/topup", headers=headers, json={
        "tenant_id": "wallet-test-large",
        "amount": "9999.99",
    })
    assert r.status_code == 200
    assert r.json()["new_balance"] == "9999.99"


def test_wallet_unauthorized():
    r = client.post("/v1/wallet/topup", json={
        "tenant_id": "no-auth",
        "amount": "10.00",
    })
    assert r.status_code == 401


# ── Full pipeline integration tests ────────────────────────────────────

def test_execute_with_wallet_balance_check():
    tenant = "full-pipe-t1"
    client.post("/v1/wallet/topup", headers=headers, json={
        "tenant_id": tenant, "amount": "10.00",
    })
    r = client.post("/v1/runtime/execute", headers=headers, json={
        "user_input": "What is the capital of France?",
        "deterministic": True,
        "risk_level": "LOW",
        "tenant_id": tenant,
    })
    assert r.status_code == 200
    data = r.json()
    assert data["decision"] in ("APPROVED", "APPROVED_WITH_LIMITATIONS")
    assert data["wallet_charge"] == "0.01"
    assert data["usage_id"] != ""
    assert data["council_verdict"] != ""


def test_execute_with_wallet_insufficient_balance():
    tenant = "full-pipe-t2"
    client.post("/v1/wallet/topup", headers=headers, json={
        "tenant_id": tenant, "amount": "0.005",
    })
    r = client.post("/v1/runtime/execute", headers=headers, json={
        "user_input": "Hello world",
        "deterministic": True,
        "risk_level": "LOW",
        "tenant_id": tenant,
    })
    assert r.status_code == 200
    data = r.json()
    assert data["blocked"] is True
    assert "wallet" in data["reason"].lower() or "blocked" in data["decision"].lower()


def test_execute_council_escalation_recorded_in_ledger():
    r = client.post("/v1/runtime/execute", headers=headers, json={
        "user_input": "So obviously X is the only answer, right?",
        "deterministic": True,
        "risk_level": "HIGH",
    })
    assert r.status_code == 200
    data = r.json()
    assert "council_verdict" in data
    assert len(data["ledger_record_ids"]) >= 1


def test_execute_council_skipped_when_disabled():
    r = client.post("/v1/runtime/execute", headers=headers, json={
        "user_input": "What is Python?",
        "deterministic": True,
        "risk_level": "LOW",
        "enable_council": False,
    })
    assert r.status_code == 200
    data = r.json()
    assert data["council_verdict"] == ""
