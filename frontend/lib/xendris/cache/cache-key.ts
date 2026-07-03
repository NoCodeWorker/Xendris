import { createHash } from "node:crypto"
import type { XendrisCacheKeyInput } from "src/lib/xendris/cache/types"

function normalizeMessage(message: string) {
  return message.trim().replace(/\s+/g, " ").toLowerCase()
}

export function createCacheKey(input: XendrisCacheKeyInput) {
  const rawKey = JSON.stringify({
    message: normalizeMessage(input.message),
    provider: input.provider,
    model: input.model,
    intent: input.intent,
    systemPromptId: input.systemPromptId,
  })

  return createHash("sha256").update(rawKey).digest("hex")
}
