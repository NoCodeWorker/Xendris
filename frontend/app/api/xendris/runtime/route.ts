import { NextResponse } from "next/server"
import type {
  XendrisMode,
  XendrisRuntimeErrorResponse,
  XendrisRuntimeSuccessResponse,
} from "src/lib/xendris/api-contracts"

const RUNTIME_API_URL = process.env.XENDRIS_RUNTIME_API_URL || "http://localhost:8001"

function errorResponse(code: string, message: string, status = 502) {
  return NextResponse.json<XendrisRuntimeErrorResponse>({ ok: false, error: { code, message } }, { status })
}

const MODE_RISK_MAP: Record<XendrisMode, { risk_level: string; claim_type: string }> = {
  eco: { risk_level: "LOW", claim_type: "INFERRED" },
  normal: { risk_level: "MEDIUM", claim_type: "FACTUAL" },
  precision: { risk_level: "HIGH", claim_type: "FACTUAL" },
  custom: { risk_level: "MEDIUM", claim_type: "FACTUAL" },
}

export async function POST(request: Request) {
  let body: unknown
  try {
    body = await request.json()
  } catch {
    return errorResponse("INVALID_JSON", "Request body must be valid JSON.")
  }

  if (!body || typeof body !== "object" || !("message" in body)) {
    return errorResponse("MISSING_MESSAGE", 'Request body must include "message".')
  }

  const { message, mode, model_id, provider, tenant_id } = body as {
    message: unknown
    mode?: unknown
    model_id?: unknown
    provider?: unknown
    tenant_id?: unknown
  }

  if (typeof message !== "string" || message.trim().length === 0) {
    return errorResponse("INVALID_MESSAGE", '"message" must be a non-empty string.')
  }

  const resolvedMode: XendrisMode =
    mode === "eco" || mode === "normal" || mode === "precision" || mode === "custom" ? mode : "normal"

  const riskConfig = MODE_RISK_MAP[resolvedMode]

  try {
    const runtimeResponse = await fetch(`${RUNTIME_API_URL}/v1/runtime/execute`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_input: message,
        risk_level: riskConfig.risk_level,
        claim_type: riskConfig.claim_type,
        model_id: typeof model_id === "string" ? model_id : "",
        provider: typeof provider === "string" ? provider : "",
        tenant_id: typeof tenant_id === "string" ? tenant_id : "",
        enable_council: true,
        deterministic: true,
      }),
    })

    if (!runtimeResponse.ok) {
      const errBody = await runtimeResponse.text()
      return errorResponse("RUNTIME_ERROR", `Runtime API error (${runtimeResponse.status}): ${errBody}`, runtimeResponse.status)
    }

    const data = await runtimeResponse.json()

    return NextResponse.json<XendrisRuntimeSuccessResponse>({
      ok: true,
      response: data.final_content || "",
      provider: data.provider || "unknown",
      model: data.selected_model_id || "unknown",
      decision: data.decision || "APPROVED",
      reason: data.reason || "OK",
      council: {
        verdict: data.council_verdict || "",
        guard_results: data.council_guard_results || [],
        requires_council: data.human_review_required || false,
      },
      wallet: {
        charge: data.wallet_charge || "",
        usage_id: data.usage_id || "",
      },
      route: {
        intent: "general",
        confidence: 1,
        matchedTerms: [],
      },
    })
  } catch (error) {
    const msg = error instanceof Error ? error.message : "Unknown error"
    return errorResponse("RUNTIME_UNREACHABLE", `Cannot reach Xendris Runtime API at ${RUNTIME_API_URL}: ${msg}`)
  }
}