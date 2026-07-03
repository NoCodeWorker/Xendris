export type XendrisEvaluationRiskLevel = "low" | "medium" | "high"

export type XendrisEvaluationResult = {
  qualityScore: number
  confidenceScore: number
  riskLevel: XendrisEvaluationRiskLevel
  flags: string[]
  improvementHints: string[]
}
