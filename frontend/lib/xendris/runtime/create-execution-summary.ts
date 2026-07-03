import type { AnswerControllerDecision } from "src/lib/xendris/controller/types"
import type { XendrisEvaluationResult } from "src/lib/xendris/evaluation/types"
import type { XendrisRepairMetadata } from "src/lib/xendris/repair/types"
import type { ExecutionSummary } from "src/lib/xendris/runtime/types"
import type { XendrisIntent } from "src/lib/xendris/types"

type CreateExecutionSummaryInput = {
  endpoint: "/api/chat"
  intent: XendrisIntent
  cognitiveMode: string
  provider: string
  model: string
  startedAt: Date
  completedAt: Date
  evaluation?: XendrisEvaluationResult
  controllerDecision?: AnswerControllerDecision
  repair?: XendrisRepairMetadata
  timings?: ExecutionSummary["timings"]
}

export function createExecutionSummary(input: CreateExecutionSummaryInput): ExecutionSummary {
  return {
    id: crypto.randomUUID(),
    endpoint: input.endpoint,
    intent: input.intent,
    cognitiveMode: input.cognitiveMode,
    provider: input.provider,
    model: input.model,
    startedAt: input.startedAt.toISOString(),
    completedAt: input.completedAt.toISOString(),
    latencyMs: Math.max(0, input.completedAt.getTime() - input.startedAt.getTime()),
    evaluation: input.evaluation
      ? {
          qualityScore: input.evaluation.qualityScore,
          confidenceScore: input.evaluation.confidenceScore,
          riskLevel: input.evaluation.riskLevel,
        }
      : undefined,
    controller: input.controllerDecision
      ? {
          action: input.controllerDecision.action,
          severity: input.controllerDecision.severity,
        }
      : undefined,
    repair: input.repair
      ? {
          repaired: input.repair.repaired,
          repairStrategy: input.repair.repairStrategy,
        }
      : undefined,
    timings: input.timings,
  }
}
