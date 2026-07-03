import type { AnswerControllerDecision } from "src/lib/xendris/controller/types"
import type { XendrisEvaluationResult } from "src/lib/xendris/evaluation/types"
import type { EpistemicEvaluation } from "src/lib/xendris/epistemic/types"

export function decideAnswerAction(
  evaluation: XendrisEvaluationResult,
  epistemicEvaluation?: EpistemicEvaluation
): AnswerControllerDecision {
  if (epistemicEvaluation?.riskLevel === "high") {
    return {
      action: "needs_review",
      reason: "Epistemic evaluation reported high risk due to unsupported absolute declarations.",
      severity: "high",
      suggestedNextStep: "Review absolute assertions or false-premise compliance.",
    }
  }

  if (evaluation.riskLevel === "high") {
    return {
      action: "needs_review",
      reason: "Evaluation reported high response risk.",
      severity: "high",
      suggestedNextStep: "Review the response before relying on it.",
    }
  }

  if (epistemicEvaluation?.riskLevel === "medium" && evaluation.qualityScore < 0.75) {
    return {
      action: "needs_improvement",
      reason: "Epistemic evaluation reported medium risk and quality score is below the threshold.",
      severity: "medium",
      suggestedNextStep: "Moderate absolute declarations and state limitations.",
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
