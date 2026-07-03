import type { AnswerControllerDecision } from "src/lib/xendris/controller/types"
import { repairWithMockRules } from "src/lib/xendris/repair/mock-repairer"
import type { RepairResult } from "src/lib/xendris/repair/types"
import type { EpistemicEvaluation } from "src/lib/xendris/epistemic/types"

export function repairResponse(
  userMessage: string,
  content: string,
  controllerDecision: AnswerControllerDecision,
  epistemicEvaluation?: EpistemicEvaluation
): RepairResult {
  return repairWithMockRules(userMessage, content, controllerDecision, epistemicEvaluation)
}
