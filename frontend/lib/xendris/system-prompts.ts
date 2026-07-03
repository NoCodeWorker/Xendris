import type { XendrisIntent, XendrisSystemPrompt } from "src/lib/xendris/types"

export const XENDRIS_MODE_DESCRIPTIONS: Record<XendrisIntent, string> = {
  general: "General coordination mode for open-ended requests.",
  coding: "Coding mode for implementation, debugging, architecture, and technical delivery.",
  business: "Business mode for positioning, operations, customers, and commercial decisions.",
  research: "Research mode for evidence gathering, synthesis, and source-aware analysis.",
  strategy: "Strategy mode for priorities, sequencing, risk, and decision framing.",
  creative: "Creative mode for naming, narrative, ideation, and content direction.",
  security: "Security mode for risk review, threat modeling, and safety-sensitive implementation.",
}

const MODE_LABELS: Record<XendrisIntent, string> = {
  general: "General Coordinator",
  coding: "Engineering Operator",
  business: "Business Analyst",
  research: "Research Synthesizer",
  strategy: "Strategy Planner",
  creative: "Creative Partner",
  security: "Security Reviewer",
}

export const XENDRIS_SYSTEM_PROMPTS: Record<XendrisIntent, XendrisSystemPrompt> = {
  general: createSystemPrompt("general"),
  coding: createSystemPrompt("coding"),
  business: createSystemPrompt("business"),
  research: createSystemPrompt("research"),
  strategy: createSystemPrompt("strategy"),
  creative: createSystemPrompt("creative"),
  security: createSystemPrompt("security"),
}

function createSystemPrompt(intent: XendrisIntent): XendrisSystemPrompt {
  return {
    id: `xendris-mode-${intent}`,
    intent,
    cognitiveMode: MODE_LABELS[intent],
    prompt: `Xendris internal mode: ${intent}. ${XENDRIS_MODE_DESCRIPTIONS[intent]}`,
  }
}

export function getSystemPrompt(intent: XendrisIntent) {
  return XENDRIS_SYSTEM_PROMPTS[intent]
}
