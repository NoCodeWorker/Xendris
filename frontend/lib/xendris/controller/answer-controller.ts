import type { AnswerControllerDecision } from "src/lib/xendris/controller/types"
import type { XendrisEvaluationResult } from "src/lib/xendris/evaluation/types"

export function decideAnswerAction(evaluation: XendrisEvaluationResult): AnswerControllerDecision {
  if (evaluation.riskLevel === "high") {
    return {
      action: "needs_review",
      reason: "Evaluation reported high response risk.",
      severity: "high",
      suggestedNextStep: "Review the response before relying on it.",
    }
  }

  if (evaluation.qualityScore < 0.55) {
    return {
      action: "needs_improvement",
      reason: "Evaluation quality score is below the acceptable threshold.",
      severity: "medium",
      suggestedNextStep: "Improve specificity, structure, or completeness.",
    }
  }

  if (evaluation.confidenceScore < 0.5) {
    return {
      action: "needs_improvement",
      reason: "Evaluation confidence score is below the acceptable threshold.",
      severity: "medium",
      suggestedNextStep: "Clarify assumptions or reduce ambiguous wording.",
    }
  }

  return {
    action: "accept",
    reason: "Evaluation passed deterministic quality and risk thresholds.",
    severity: "low",
  }
}
