import type { XendrisEvaluationResult } from "src/lib/xendris/evaluation/types"
import type { AnswerControllerDecision } from "src/lib/xendris/controller/types"
import type { XendrisCacheMetadata } from "src/lib/xendris/cache/types"
import type { XendrisRepairMetadata } from "src/lib/xendris/repair/types"
import type { ExecutionSummary } from "src/lib/xendris/runtime/types"
import type { EpistemicEvaluation } from "src/lib/xendris/epistemic/types"

export type XendrisIntent =
  | "general"
  | "coding"
  | "business"
  | "research"
  | "strategy"
  | "creative"
  | "security"

export type XendrisProviderName = "mock" | "deepseek"

export type XendrisMessageRole = "user" | "assistant"

export type XendrisMessage = {
  id: string
  role: XendrisMessageRole
  content: string
  createdAt: string
  metadata?: {
    detectedIntent?: XendrisIntent
    cognitiveMode?: string
    provider?: string
    model?: string
    pending?: boolean
    cache?: XendrisCacheMetadata
    evaluation?: XendrisEvaluationResult
    epistemicEvaluation?: EpistemicEvaluation
    controllerDecision?: AnswerControllerDecision
    repair?: XendrisRepairMetadata
    executionSummary?: ExecutionSummary
    detectedLanguage?: "es" | "en"
  }
}

export type XendrisConversation = {
  id: string
  title: string
  messages: XendrisMessage[]
  createdAt: string
  updatedAt: string
}

export type IntentRoute = {
  intent: XendrisIntent
  confidence: number
  matchedTerms: string[]
  cognitiveMode?: string
  systemPromptId?: string
}

export type XendrisSystemPrompt = {
  id: string
  intent: XendrisIntent
  cognitiveMode: string
  prompt: string
}
