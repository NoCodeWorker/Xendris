export type AnswerControllerAction = "accept" | "needs_improvement" | "needs_review"

export type AnswerControllerSeverity = "low" | "medium" | "high"

export type AnswerControllerDecision = {
  action: AnswerControllerAction
  reason: string
  severity: AnswerControllerSeverity
  suggestedNextStep?: string
}
