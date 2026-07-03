import { evaluateWithMockHeuristics } from "src/lib/xendris/evaluation/mock-evaluator"
import type { XendrisEvaluationResult } from "src/lib/xendris/evaluation/types"

export function evaluateResponse(responseText: string): XendrisEvaluationResult {
  return evaluateWithMockHeuristics(responseText)
}
