import type { IntentRoute, XendrisIntent } from "src/lib/xendris/types"

const INTENT_TERMS: Record<XendrisIntent, string[]> = {
  general: [],
  coding: [
    "api",
    "bug",
    "build",
    "code",
    "component",
    "debug",
    "deploy",
    "error",
    "frontend",
    "function",
    "implement",
    "typescript",
  ],
  business: [
    "business",
    "customer",
    "market",
    "pricing",
    "revenue",
    "sales",
    "startup",
    "subscription",
  ],
  research: [
    "citation",
    "evidence",
    "literature",
    "paper",
    "research",
    "source",
    "study",
    "verify",
  ],
  strategy: [
    "decision",
    "focus",
    "goal",
    "plan",
    "priority",
    "roadmap",
    "risk",
    "strategy",
  ],
  creative: [
    "brand",
    "copy",
    "creative",
    "design",
    "idea",
    "name",
    "story",
    "visual",
  ],
  security: [
    "auth",
    "attack",
    "permission",
    "privacy",
    "risk",
    "secure",
    "security",
    "threat",
    "vulnerability",
  ],
}

export function routeIntent(message: string): IntentRoute {
  const normalized = message.toLowerCase()
  const scores = Object.entries(INTENT_TERMS).map(([intent, terms]) => {
    const matchedTerms = terms.filter((term) => normalized.includes(term))
    return {
      intent: intent as XendrisIntent,
      matchedTerms,
      score: matchedTerms.length,
    }
  })

  const winner = scores
    .filter((result) => result.intent !== "general")
    .sort((a, b) => b.score - a.score || a.intent.localeCompare(b.intent))[0]

  if (!winner || winner.score === 0) {
    return {
      intent: "general",
      confidence: message.trim() ? 0.35 : 0,
      matchedTerms: [],
    }
  }

  return {
    intent: winner.intent,
    confidence: Math.min(0.95, 0.45 + winner.score * 0.15),
    matchedTerms: winner.matchedTerms,
  }
}
