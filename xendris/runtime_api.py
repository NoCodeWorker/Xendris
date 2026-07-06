"""
Xendris Runtime API — Trust-routed AI inference gateway.

Endpoints:
    GET  /v1/health             — Health check
    POST /v1/runtime/execute    — Full runtime: select → call → gate → respond
    POST /v1/claims/evaluate    — Evaluate existing output claims (no model call)
    POST /v1/routes/select      — Model selection only (no execution)
    GET  /v1/ledger/{run_id}    — Retrieve trust ledger for a run
"""

from __future__ import annotations

import json
import os
import secrets
import time
import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from xendris.core.runtime import (
    ProviderAdapter,
    ProviderAdapterSandbox,
    RuntimeRequest,
)
from xendris.core.runtime.claim_extractor import ClaimExtractor
from xendris.core.ledger import (
    TrustLedgerWriter, TrustEventType, TrustLedgerRecord,
)
from xendris.core.router.model_registry import ModelRegistry, ModelCapabilityProfile
from xendris.core.router.selector import MultiModelSelector
from xendris.core.router.route_request import RouteRequest
from xendris.core.router.cost_policy import CostPolicy
from xendris.core.router.risk_policy import RiskPolicy
from xendris.core.local.context import LocalContext
from xendris.core.sectors.sector import EpistemicSector
from xendris.core.trust.types import ClaimType, RiskLevel

# ── App setup ──────────────────────────────────────────────────────────

LEDGER_DIR = Path(os.getenv("XENDRIS_LEDGER_DIR", "runs/ledger"))
LEDGER_DIR.mkdir(parents=True, exist_ok=True)

# In-memory ledger storage (per run_id)
_ledgers: dict[str, "TrustLedgerWriter"] = {}

app = FastAPI(
    title="Xendris Runtime API",
    version="0.3.0",
    description="Epistemic trust runtime for AI agents and model outputs.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "type": type(exc).__name__},
    )

# ── Auth ───────────────────────────────────────────────────────────────

API_KEYS: set[str] = set()
_key_from_env = os.getenv("XENDRIS_API_KEY")
if _key_from_env:
    API_KEYS.add(_key_from_env)


def _check_api_key(request: Request) -> str | None:
    key = request.headers.get("X-API-Key", "")
    if not API_KEYS:
        return None  # no keys configured → open access
    if key in API_KEYS:
        return key
    return None


@app.middleware("http")
async def auth_middleware(request: Request, call_next: Any) -> JSONResponse:
    if request.url.path == "/v1/health":
        return await call_next(request)
    api_key = _check_api_key(request)
    if api_key is None and API_KEYS:
        return JSONResponse(status_code=401, content={"error": "unauthorized", "message": "Valid X-API-Key header required"})
    return await call_next(request)


# ── Request / Response models ──────────────────────────────────────────

class ExecuteRequest(BaseModel):
    user_input: str
    request_id: str = ""
    local_context: str = "GENERAL"
    epistemic_sector: str = "FACTUAL"
    claim_type: str = "FACTUAL"
    risk_level: str = "LOW"
    model_id: str = ""
    provider: str = ""
    prefer_low_cost: bool = False
    prefer_low_latency: bool = False
    deterministic: bool = False


class ExecuteResponse(BaseModel):
    response_id: str
    request_id: str
    decision: str
    final_content: str
    selected_model_id: str
    provider: str
    limitations: list[str]
    ledger_record_ids: list[str]
    human_review_required: bool
    blocked: bool
    reason: str
    sandbox_audits: list[dict]


class EvaluateClaimsRequest(BaseModel):
    text: str
    request_id: str = ""


class EvaluateClaimsResponse(BaseModel):
    request_id: str
    claims: list[dict]
    decision: str
    reason: str


class RouteSelectRequest(BaseModel):
    user_input: str
    request_id: str = ""
    local_context: str = "GENERAL"
    epistemic_sector: str = "FACTUAL"
    claim_type: str = "FACTUAL"
    risk_level: str = "LOW"
    prefer_low_cost: bool = False
    prefer_low_latency: bool = False


class RouteSelectResponse(BaseModel):
    request_id: str
    selected_model_id: str
    provider: str
    estimated_cost: float
    estimated_latency_ms: int
    reason: str
    rejected_models: list[dict]
    required_gates: list[str]


class HealthResponse(BaseModel):
    status: str
    version: str
    uptime_s: float


# ── Helpers ────────────────────────────────────────────────────────────

def _resolve_enum(enum_cls: type, value: str, default: Any = None) -> Any:
    upper = value.upper()
    if upper in enum_cls.__members__:
        return enum_cls[upper]
    return default or list(enum_cls.__members__.values())[0]


def _build_default_registry() -> ModelRegistry:
    registry = ModelRegistry()
    registry.register_model(ModelCapabilityProfile(
        model_id="gpt-4", provider="openai",
        supported_contexts=("GENERAL", "CODE", "SCIENCE"),
        supported_sectors=("FACTUAL", "INFERRED", "CREATIVE"),
        max_risk_level=RiskLevel.CRITICAL,
        cost_per_1k_input_tokens=0.03, cost_per_1k_output_tokens=0.06,
        expected_latency_ms=1000, supports_tools=True, supports_code=True,
        supports_json=True, supports_long_context=True,
        required_gates=(),
    ))
    registry.register_model(ModelCapabilityProfile(
        model_id="gpt-4o-mini", provider="openai",
        supported_contexts=("GENERAL", "CODE", "CREATIVE", "CUSTOMER"),
        supported_sectors=("FACTUAL", "INFERRED", "CREATIVE"),
        max_risk_level=RiskLevel.HIGH,
        cost_per_1k_input_tokens=0.00015, cost_per_1k_output_tokens=0.0006,
        expected_latency_ms=500, supports_tools=True, supports_code=True,
        supports_json=True, supports_long_context=False,
        required_gates=(),
    ))
    registry.register_model(ModelCapabilityProfile(
        model_id="deepseek-chat", provider="deepseek",
        supported_contexts=("GENERAL", "CODE", "SCIENCE"),
        supported_sectors=("FACTUAL", "INFERRED", "CALCULATED"),
        max_risk_level=RiskLevel.HIGH,
        cost_per_1k_input_tokens=0.00014, cost_per_1k_output_tokens=0.00028,
        expected_latency_ms=800, supports_tools=False, supports_code=True,
        supports_json=True, supports_long_context=True,
        required_gates=(),
    ))
    registry.register_model(ModelCapabilityProfile(
        model_id="claude-3-haiku", provider="anthropic",
        supported_contexts=("GENERAL", "CODE", "CREATIVE"),
        supported_sectors=("FACTUAL", "INFERRED", "CREATIVE"),
        max_risk_level=RiskLevel.HIGH,
        cost_per_1k_input_tokens=0.00025, cost_per_1k_output_tokens=0.00125,
        expected_latency_ms=600, supports_tools=False, supports_code=True,
        supports_json=True, supports_long_context=False,
        required_gates=(),
    ))
    return registry


def _make_sandbox(provider: str, model_id: str) -> ProviderAdapterSandbox:
    adapter = ProviderAdapter(model_id, provider)
    return ProviderAdapterSandbox(adapter)


def _register_mock(sandbox: ProviderAdapterSandbox, user_input: str, model_id: str, provider: str) -> None:
    lower = user_input.lower()
    if "block" in lower:
        content = f"CLAIM: {user_input}\nCLAIM_TYPE: FACTUAL\nSECTOR: FACTUAL"
    elif "limit" in lower:
        content = f"CLAIM: {user_input}\nLIMITATION: scoped to available data\nCLAIM_TYPE: FACTUAL"
    else:
        content = f"CLAIM: {user_input}\nEVIDENCE: standard response\nCLAIM_TYPE: FACTUAL"

    if provider == "anthropic":
        url = "https://api.anthropic.com/v1/messages"
        sandbox.register_mock(url, user_input, 200, {"content": [{"type": "text", "text": content}]})
    elif provider == "deepseek":
        url = "https://api.deepseek.com/v1/completions"
        sandbox.register_mock(url, user_input, 200, {"text": content})
    else:
        url = f"https://api.{provider}.com/v1/chat/completions"
        sandbox.register_mock(url, user_input, 200, {"choices": [{"message": {"role": "assistant", "content": content}}]})


# ── Endpoints ──────────────────────────────────────────────────────────

_start_time = time.time()


@app.get("/v1/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        version="0.3.0",
        uptime_s=round(time.time() - _start_time, 2),
    )


@app.post("/v1/runtime/execute", response_model=ExecuteResponse)
def runtime_execute(req: ExecuteRequest) -> ExecuteResponse:
    ctx = _resolve_enum(LocalContext, req.local_context, LocalContext.GENERAL)
    sector = _resolve_enum(EpistemicSector, req.epistemic_sector, EpistemicSector.FACTUAL)
    ctype = _resolve_enum(ClaimType, req.claim_type, ClaimType.FACTUAL)
    risk = _resolve_enum(RiskLevel, req.risk_level, RiskLevel.LOW)

    rid = req.request_id or f"req-{uuid.uuid4().hex[:12]}"
    run_id = f"run-{rid}"

    registry = _build_default_registry()
    model_id = req.model_id or "gpt-4o-mini"
    provider = req.provider or "openai"

    # 1. Route: select model
    selector = MultiModelSelector(cost_policy=CostPolicy(), risk_policy=RiskPolicy())
    route_req = RouteRequest(
        request_id=rid, user_intent="GENERAL_CHAT",
        local_context=ctx, epistemic_sector=sector,
        claim_type=ctype, risk_level=risk,
        estimated_input_tokens=512, estimated_output_tokens=1024,
        prefer_low_cost=req.prefer_low_cost,
        prefer_low_latency=req.prefer_low_latency,
    )
    route_decision = selector.select_model(route_req, registry)
    selected_model = getattr(route_decision, "selected_model_id", model_id)
    selected_provider = getattr(route_decision, "selected_provider", provider)

    # 2. Sandboxed provider call
    adapter = ProviderAdapter(selected_model, selected_provider)
    sandbox = ProviderAdapterSandbox(adapter)
    if req.deterministic:
        _register_mock(sandbox, req.user_input, selected_model, selected_provider)

    runtime_req = RuntimeRequest(
        request_id=rid,
        user_input=req.user_input,
        user_intent="GENERAL_CHAT",
        local_context=ctx,
        epistemic_sector=sector,
        claim_type=ctype,
        risk_level=risk,
    )
    try:
        candidate = adapter.generate(runtime_req)
        content = candidate.content
    except Exception as e:
        return ExecuteResponse(
            response_id=f"resp-{uuid.uuid4().hex[:8]}",
            request_id=rid,
            decision="ERROR",
            final_content=f"Provider error: {e}",
            selected_model_id=selected_model,
            provider=selected_provider,
            limitations=[],
            ledger_record_ids=[],
            human_review_required=False,
            blocked=True,
            reason=f"Provider error: {e}",
            sandbox_audits=[a.to_dict() for a in sandbox.audits],
        )

    # 3. Basic claim extraction
    extractor = ClaimExtractor()
    claims = extractor.extract_claims(content)

    # 4. Evaluate claims
    blocked = False
    limitations = []
    decision = "APPROVED"
    reason = "OK"
    for claim in claims:
        ctype_val = claim.get("claim_type", "INFERRED")
        if ctype_val == "BLOCKED":
            blocked = True
            decision = "BLOCKED"
            reason = f"Claim blocked: {claim.get('content', '')[:80]}"
            break
        limitations_list = claim.get("limitations", ())
        if limitations_list and decision == "APPROVED":
            decision = "APPROVED_WITH_LIMITATIONS"
            reason = "Some claims limited"
            limitations.append(claim.get("content", "")[:80])

    # 5. Record in ledger
    writer = TrustLedgerWriter()
    record_id = f"rec-{uuid.uuid4().hex[:8]}"
    writer.append_event(
        record_id=record_id, run_id=run_id,
        event_type=TrustEventType.ROUTING_DECISION,
        source_component="RuntimeAPI",
        decision=decision, reason=reason,
        risk_level=risk.name if hasattr(risk, "name") else str(risk),
        model_id=selected_model, provider=selected_provider,
    )
    _ledgers[run_id] = writer

    return ExecuteResponse(
        response_id=f"resp-{uuid.uuid4().hex[:8]}",
        request_id=rid,
        decision=decision,
        final_content=content,
        selected_model_id=selected_model,
        provider=selected_provider,
        limitations=limitations,
        ledger_record_ids=[record_id],
        human_review_required=False,
        blocked=blocked,
        reason=reason,
        sandbox_audits=[a.to_dict() for a in sandbox.audits],
    )


@app.post("/v1/claims/evaluate", response_model=EvaluateClaimsResponse)
def claims_evaluate(req: EvaluateClaimsRequest) -> EvaluateClaimsResponse:
    rid = req.request_id or f"req-{uuid.uuid4().hex[:12]}"

    extractor = ClaimExtractor()
    claims_raw = extractor.extract_claims(req.text)

    claims_out = []
    for c in claims_raw:
        claims_out.append({
            "text": c.get("content", ""),
            "claim_type": c.get("claim_type", "INFERRED"),
            "risk": c.get("risk_level", "LOW"),
            "support_status": "UNSUPPORTED",
            "evidence_issue": "",
            "code_production_issue": "",
        })

    decision = "APPROVED"
    reason = "All claims passed evaluation"
    for c in claims_out:
        limitations = c.get("limitations", ())
        if limitations:
            decision = "APPROVED_WITH_LIMITATIONS"

    return EvaluateClaimsResponse(
        request_id=rid,
        claims=claims_out,
        decision=decision,
        reason=reason,
    )


@app.post("/v1/routes/select", response_model=RouteSelectResponse)
def routes_select(req: RouteSelectRequest) -> RouteSelectResponse:
    ctx = _resolve_enum(LocalContext, req.local_context, LocalContext.GENERAL)
    sector = _resolve_enum(EpistemicSector, req.epistemic_sector, EpistemicSector.FACTUAL)
    ctype = _resolve_enum(ClaimType, req.claim_type, ClaimType.FACTUAL)
    risk = _resolve_enum(RiskLevel, req.risk_level, RiskLevel.LOW)

    rid = req.request_id or f"req-{uuid.uuid4().hex[:12]}"

    registry = _build_default_registry()
    selector = MultiModelSelector(cost_policy=CostPolicy(), risk_policy=RiskPolicy())
    route_req = RouteRequest(
        request_id=rid,
        user_intent="GENERAL_CHAT",
        local_context=ctx,
        epistemic_sector=sector,
        claim_type=ctype,
        risk_level=risk,
        estimated_input_tokens=512, estimated_output_tokens=1024,
        prefer_low_cost=req.prefer_low_cost,
        prefer_low_latency=req.prefer_low_latency,
    )
    decision = selector.select_model(route_req, registry)

    rejected = []
    for rm in getattr(decision, "rejected_models", ()):
        rejected.append({"model_id": rm.model_id if hasattr(rm, "model_id") else str(rm), "reason": "cost"})

    return RouteSelectResponse(
        request_id=rid,
        selected_model_id=getattr(decision, "selected_model_id", "none"),
        provider=getattr(decision, "selected_provider", "none"),
        estimated_cost=getattr(decision, "estimated_cost", 0.0),
        estimated_latency_ms=getattr(decision, "estimated_latency_ms", 0),
        reason=getattr(decision, "reason", "Unknown"),
        rejected_models=rejected,
        required_gates=list(getattr(decision, "required_gates", ())),
    )


@app.get("/v1/ledger/{run_id}")
def ledger_get(run_id: str) -> dict:
    writer = _ledgers.get(run_id)
    if writer is None:
        raise HTTPException(status_code=404, detail=f"Ledger run {run_id} not found")
    return {
        "run_id": run_id,
        "record_count": len(writer._records),
        "records": [r.to_dict() if hasattr(r, "to_dict") else r for r in writer._records],
    }
