import type { IntentRoute, XendrisIntent, XendrisProviderName } from "src/lib/xendris/types"
import type { AnswerControllerDecision } from "src/lib/xendris/controller/types"
import type { XendrisCacheMetadata } from "src/lib/xendris/cache/types"
import type { XendrisEvaluationResult } from "src/lib/xendris/evaluation/types"
import type { XendrisRepairMetadata } from "src/lib/xendris/repair/types"
import type { ExecutionSummary } from "src/lib/xendris/runtime/types"

export type XendrisApiError = {
  code: string
  message: string
}

export type XendrisChatRequest = {
  message: string
  provider?: XendrisProviderName
}

export type XendrisChatSuccessResponse = {
  ok: true
  detectedIntent: XendrisIntent
  cognitiveMode: string
  systemPromptId: string
  response: string
  provider: string
  model: string
  latencyMs?: number
  cached?: boolean
  cache?: XendrisCacheMetadata
  evaluation?: XendrisEvaluationResult
  controllerDecision?: AnswerControllerDecision
  repair?: XendrisRepairMetadata
  executionSummary?: ExecutionSummary
  route: IntentRoute
}

export type XendrisChatErrorResponse = {
  ok: false
  error: XendrisApiError
}

export type XendrisChatResponse = XendrisChatSuccessResponse | XendrisChatErrorResponse

export type XendrisStreamMetaEvent = {
  type: "meta"
  detectedIntent: XendrisIntent
  cognitiveMode: string
  systemPromptId: string
  provider: string
  model: string
  route: IntentRoute
}

export type XendrisStreamDeltaEvent = {
  type: "delta"
  content: string
}

export type XendrisStreamDoneEvent = {
  type: "done"
}

export type XendrisStreamErrorEvent = {
  type: "error"
  error: XendrisApiError
}

export type XendrisStreamEvent =
  | XendrisStreamMetaEvent
  | XendrisStreamDeltaEvent
  | XendrisStreamDoneEvent
  | XendrisStreamErrorEvent
