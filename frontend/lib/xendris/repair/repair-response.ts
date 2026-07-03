import type { AnswerControllerDecision } from "src/lib/xendris/controller/types"
import { repairWithMockRules } from "src/lib/xendris/repair/mock-repairer"
import type { RepairResult } from "src/lib/xendris/repair/types"

export function repairResponse(
  content: string,
  controllerDecision: AnswerControllerDecision
): RepairResult {
  return repairWithMockRules(content, controllerDecision)
}
