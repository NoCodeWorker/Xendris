import type { XendrisIntent } from "src/lib/xendris/types"

export const XENDRIS_PRODUCT_NAME = "Xendris AI"

export const XENDRIS_INTENTS: XendrisIntent[] = [
  "general",
  "coding",
  "business",
  "research",
  "strategy",
  "creative",
  "security",
]

export const XENDRIS_PLACEHOLDER_RESPONSE =
  "Placeholder response: Xendris has classified the request locally. Model orchestration is not connected yet."
