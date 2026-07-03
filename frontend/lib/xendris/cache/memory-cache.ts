import type { XendrisCacheEntry } from "src/lib/xendris/cache/types"
import type { XendrisChatSuccessResponse } from "src/lib/xendris/api-contracts"

const DEFAULT_TTL_MS = 10 * 60 * 1000
const DEFAULT_MAX_ENTRIES = 100

const cacheStore = new Map<string, XendrisCacheEntry<XendrisChatSuccessResponse>>()

function removeExpired(nowMs: number) {
  for (const [key, entry] of cacheStore.entries()) {
    if (entry.expiresAtMs <= nowMs) {
      cacheStore.delete(key)
    }
  }
}

function removeOldestEntry() {
  const oldestKey = cacheStore.keys().next().value as string | undefined
  if (oldestKey) {
    cacheStore.delete(oldestKey)
  }
}

export function getMemoryCacheEntry(key: string, nowMs = Date.now()) {
  const entry = cacheStore.get(key)

  if (!entry) return null

  if (entry.expiresAtMs <= nowMs) {
    cacheStore.delete(key)
    return null
  }

  cacheStore.delete(key)
  cacheStore.set(key, entry)

  return entry.value
}

export function setMemoryCacheEntry(
  key: string,
  value: XendrisChatSuccessResponse,
  ttlMs = DEFAULT_TTL_MS,
  maxEntries = DEFAULT_MAX_ENTRIES,
  nowMs = Date.now()
) {
  removeExpired(nowMs)

  cacheStore.set(key, {
    value,
    createdAtMs: nowMs,
    expiresAtMs: nowMs + ttlMs,
  })

  while (cacheStore.size > maxEntries) {
    removeOldestEntry()
  }
}

export function getMemoryCacheTtlMs() {
  return DEFAULT_TTL_MS
}
