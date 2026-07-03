import type { AnswerControllerAction, AnswerControllerSeverity } from "src/lib/xendris/controller/types"
import type { XendrisEvaluationRiskLevel } from "src/lib/xendris/evaluation/types"
import type { XendrisIntent } from "src/lib/xendris/types"

export type ExecutionSummary = {
  id: string
  endpoint: "/api/chat"
  intent: XendrisIntent
  cognitiveMode: string
  provider: string
  model: string
  startedAt: string
  completedAt: string
  latencyMs: number
  evaluation?: {
    qualityScore: number
    confidenceScore: number
    riskLevel: XendrisEvaluationRiskLevel
  }
  controller?: {
    action: AnswerControllerAction
    severity: AnswerControllerSeverity
  }
  repair?: {
    repaired: boolean
    repairStrategy?: string
  }
}
