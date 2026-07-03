import { NextResponse } from "next/server"
import { createCacheKey } from "src/lib/xendris/cache/cache-key"
import {
  getMemoryCacheEntry,
  getMemoryCacheTtlMs,
  setMemoryCacheEntry,
} from "src/lib/xendris/cache/memory-cache"
import { decideAnswerAction } from "src/lib/xendris/controller/answer-controller"
import { evaluateResponse } from "src/lib/xendris/evaluation/evaluate-response"
import { evaluateEpistemicSafety } from "src/lib/xendris/epistemic/epistemic-evaluator"
import { detectLanguage } from "src/lib/xendris/language/detect-language"
import { routeIntent } from "src/lib/xendris/intent-router"
import { selectModelProvider } from "src/lib/xendris/model-provider"
import { XendrisProviderError } from "src/lib/xendris/providers/types"
import { repairResponse } from "src/lib/xendris/repair/repair-response"
import { createExecutionSummary } from "src/lib/xendris/runtime/create-execution-summary"
import { getSystemPrompt } from "src/lib/xendris/system-prompts"
import type {
  XendrisChatErrorResponse,
  XendrisChatSuccessResponse,
} from "src/lib/xendris/api-contracts"
import type { XendrisProviderName } from "src/lib/xendris/types"

function errorResponse(code: string, message: string, status = 400) {
  return NextResponse.json<XendrisChatErrorResponse>(
    {
      ok: false,
      error: {
        code,
        message,
      },
    },
    { status }
  )
}

function isProviderName(value: unknown): value is XendrisProviderName {
  return value === "mock" || value === "deepseek"
}

export async function POST(request: Request) {
  const startedAt = new Date()
  let body: unknown

  // 1. Validation
  const valStart = performance.now()
  try {
    body = await request.json()
  } catch {
    return errorResponse("INVALID_JSON", "Request body must be valid JSON.")
  }

  if (!body || typeof body !== "object" || !("message" in body)) {
    return errorResponse("MISSING_MESSAGE", 'Request body must include "message".')
  }

  const { message, provider } = body as { message: unknown; provider?: unknown }

  if (typeof message !== "string" || message.trim().length === 0) {
    return errorResponse("INVALID_MESSAGE", '"message" must be a non-empty string.')
  }

  if (provider !== undefined && !isProviderName(provider)) {
    return errorResponse("INVALID_PROVIDER", '"provider" must be "mock" or "deepseek".')
  }
  const validationMs = Math.round(performance.now() - valStart)

  const detectedLanguage = detectLanguage(message)

  // 2. Intent Routing
  const intentStart = performance.now()
  const route = routeIntent(message)
  const intentMs = Math.round(performance.now() - intentStart)

  // 3. Prompt Configuration
  const promptStart = performance.now()
  const systemPrompt = getSystemPrompt(route.intent, detectedLanguage)
  const selectedProvider = selectModelProvider(provider ?? process.env.XENDRIS_MODEL_PROVIDER)
  const promptMs = Math.round(performance.now() - promptStart)

  // 4. Cache Check
  const cacheStart = performance.now()
  const cacheTtlMs = getMemoryCacheTtlMs()
  const cacheKey = createCacheKey({
    message,
    provider: selectedProvider.name,
    model: selectedProvider.model,
    intent: route.intent,
    systemPromptId: systemPrompt.id,
  })
  const cachedResponse = getMemoryCacheEntry(cacheKey)
  const cacheMs = Math.round(performance.now() - cacheStart)

  if (cachedResponse) {
    const completedAt = new Date()
    const totalMs = Math.round(completedAt.getTime() - startedAt.getTime())
    const executionSummary = createExecutionSummary({
      endpoint: "/api/chat",
      intent: cachedResponse.detectedIntent,
      cognitiveMode: cachedResponse.cognitiveMode,
      provider: cachedResponse.provider,
      model: cachedResponse.model,
      startedAt,
      completedAt,
      evaluation: cachedResponse.evaluation,
      controllerDecision: cachedResponse.controllerDecision,
      repair: cachedResponse.repair,
      timings: {
        validationMs,
        intentMs,
        promptMs,
        cacheMs,
        totalMs,
      },
    })

    return NextResponse.json<XendrisChatSuccessResponse>({
      ...cachedResponse,
      cached: true,
      cache: {
        hit: true,
        key: cacheKey,
        ttlMs: cacheTtlMs,
      },
      executionSummary,
      detectedLanguage: cachedResponse.detectedLanguage ?? detectedLanguage,
    })
  }

  // 5. Provider Execution
  const providerStart = performance.now()
  let modelResponse

  try {
    modelResponse = await selectedProvider.generate({
      message,
      detectedIntent: route.intent,
      cognitiveMode: systemPrompt.cognitiveMode,
      systemPromptId: systemPrompt.id,
      systemPrompt: systemPrompt.prompt,
    })
  } catch (error) {
    if (error instanceof XendrisProviderError) {
      return errorResponse("PROVIDER_ERROR", error.message, error.status)
    }

    return errorResponse("PROVIDER_REQUEST_FAILED", "Model provider request failed.", 502)
  }
  const providerMs = Math.round(performance.now() - providerStart)

  const responseRoute = {
    ...route,
    cognitiveMode: systemPrompt.cognitiveMode,
    systemPromptId: systemPrompt.id,
  }

  // 6. Evaluation
  const evalStart = performance.now()
  const evaluation = evaluateResponse(modelResponse.content)
  const evaluationMs = Math.round(performance.now() - evalStart)

  // 7. Epistemic Safety
  const epistemicStart = performance.now()
  const epistemicEvaluation = evaluateEpistemicSafety(message, modelResponse.content)
  const epistemicMs = Math.round(performance.now() - epistemicStart)

  // 8. Controller Decision
  const controllerStart = performance.now()
  const controllerDecision = decideAnswerAction(evaluation, epistemicEvaluation)
  const controllerMs = Math.round(performance.now() - controllerStart)

  // 9. Repair Loop
  const repairStart = performance.now()
  const repair = repairResponse(message, modelResponse.content, controllerDecision, epistemicEvaluation)
  const repairMetadata = {
    repaired: repair.repaired,
    repairReason: repair.repairReason,
    repairStrategy: repair.repairStrategy,
  }
  const repairMs = Math.round(performance.now() - repairStart)

  const completedAt = new Date()
  const totalMs = Math.round(completedAt.getTime() - startedAt.getTime())

  const timings = {
    validationMs,
    intentMs,
    promptMs,
    cacheMs,
    providerMs,
    evaluationMs,
    epistemicMs,
    controllerMs,
    repairMs,
    totalMs,
  }

  const executionSummary = createExecutionSummary({
    endpoint: "/api/chat",
    intent: route.intent,
    cognitiveMode: systemPrompt.cognitiveMode,
    provider: modelResponse.provider,
    model: modelResponse.model,
    startedAt,
    completedAt,
    evaluation,
    controllerDecision,
    repair: repairMetadata,
    timings,
  })

  const cacheMetadata = {
    hit: false,
    key: cacheKey,
    ttlMs: cacheTtlMs,
  }

  const successResponse: XendrisChatSuccessResponse = {
    ok: true,
    detectedIntent: route.intent,
    cognitiveMode: systemPrompt.cognitiveMode,
    systemPromptId: systemPrompt.id,
    response: repair.finalContent,
    provider: modelResponse.provider,
    model: modelResponse.model,
    latencyMs: modelResponse.latencyMs,
    cached: modelResponse.cached,
    cache: cacheMetadata,
    evaluation,
    epistemicEvaluation,
    controllerDecision,
    repair: repairMetadata,
    executionSummary,
    route: responseRoute,
    detectedLanguage,
  }

  setMemoryCacheEntry(cacheKey, successResponse, cacheTtlMs)

  return NextResponse.json<XendrisChatSuccessResponse>(successResponse)
}
