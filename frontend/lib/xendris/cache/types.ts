import type { XendrisIntent } from "src/lib/xendris/types"

export type XendrisCacheMetadata = {
  hit: boolean
  key: string
  ttlMs: number
}

export type XendrisCacheKeyInput = {
  message: string
  provider: string
  model: string
  intent: XendrisIntent
  systemPromptId: string
}

export type XendrisCacheEntry<TValue> = {
  value: TValue
  createdAtMs: number
  expiresAtMs: number
}
