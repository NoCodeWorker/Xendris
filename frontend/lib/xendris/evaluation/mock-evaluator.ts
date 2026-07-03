import type { XendrisEvaluationResult, XendrisEvaluationRiskLevel } from "src/lib/xendris/evaluation/types"

function clampScore(value: number) {
  return Math.max(0, Math.min(1, Number(value.toFixed(2))))
}

function riskFromScore(score: number, hasErrorWording: boolean): XendrisEvaluationRiskLevel {
  if (hasErrorWording) return score < 0.45 ? "high" : "medium"
  if (score < 0.4) return "medium"
  return "low"
}

export function evaluateWithMockHeuristics(responseText: string): XendrisEvaluationResult {
  const normalized = responseText.trim()
  const flags: string[] = []

  const improvementHints: string[] = []

  const hasCodeBlock = /```[\s\S]*?```/.test(normalized)
  const hasHeading = /^#{1,6}\s+/m.test(normalized)
  const hasList = /(^|\n)([-*+]|\d+\.)\s+/m.test(normalized)
  const hasErrorWording = /\b(error|failed|timeout|timed out|no he podido|fall[oó]|failed)\b/i.test(
    normalized
  )
  const wordCount = normalized.split(/\s+/).filter(Boolean).length

  let qualityScore = 0.72
  let confidenceScore = 0.72

  if (wordCount < 18) {
    qualityScore -= 0.25
    confidenceScore -= 0.15
    improvementHints.push("Response is short; consider adding concrete next steps.")
  }

  if (hasCodeBlock) {
    flags.push("code_response")
    qualityScore += 0.06
  }

  if (hasHeading || hasList) {
    flags.push("structured_response")
    qualityScore += 0.08
    confidenceScore += 0.04
  }

  if (hasErrorWording) {
    flags.push("error_wording")
    qualityScore -= 0.25
    confidenceScore -= 0.2
    improvementHints.push("Response appears to include an error or failure path.")
  }

  if (flags.length === 0) {
    flags.push("plain_response")
  }

  const finalQualityScore = clampScore(qualityScore)
  const finalConfidenceScore = clampScore(confidenceScore)

  return {
    qualityScore: finalQualityScore,
    confidenceScore: finalConfidenceScore,
    riskLevel: riskFromScore(finalQualityScore, hasErrorWording),
    flags,
    improvementHints,
  }
}
