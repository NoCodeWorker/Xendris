import type {
  XendrisModelProvider,
  XendrisModelRequest,
  XendrisModelResponse,
} from "src/lib/xendris/providers/types"
import { XendrisProviderError } from "src/lib/xendris/providers/types"

const DEEPSEEK_BASE_URL = "https://api.deepseek.com"
const DEEPSEEK_TIMEOUT_MS = 30_000
const DEFAULT_DEEPSEEK_MODEL = "deepseek-v4-flash"

type DeepSeekChatCompletionResponse = {
  choices?: Array<{
    message?: {
      content?: string | null
    }
  }>
}

export const deepseekProvider: XendrisModelProvider = {
  name: "deepseek",
  model: process.env.DEEPSEEK_MODEL || DEFAULT_DEEPSEEK_MODEL,
  async generate(request: XendrisModelRequest): Promise<XendrisModelResponse> {
    const apiKey = process.env.DEEPSEEK_API_KEY
    const model = process.env.DEEPSEEK_MODEL || DEFAULT_DEEPSEEK_MODEL

    if (!apiKey) {
      throw new XendrisProviderError(
        "DeepSeek provider selected, but DEEPSEEK_API_KEY is not configured.",
        this.name,
        503
      )
    }

    const startedAt = performance.now()
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), DEEPSEEK_TIMEOUT_MS)

    try {
      const response = await fetch(`${DEEPSEEK_BASE_URL}/chat/completions`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${apiKey}`,
        },
        body: JSON.stringify({
          model,
          messages: [
            {
              role: "system",
              content: request.systemPrompt,
            },
            {
              role: "user",
              content: request.message,
            },
          ],
          stream: false,
        }),
        signal: controller.signal,
      })

      if (!response.ok) {
        throw new XendrisProviderError(
          `DeepSeek request failed with status ${response.status}.`,
          this.name,
          502
        )
      }

      const data = (await response.json()) as DeepSeekChatCompletionResponse
      const content = data.choices?.[0]?.message?.content?.trim()

      if (!content) {
        throw new XendrisProviderError("DeepSeek returned an empty response.", this.name, 502)
      }

      return {
        content,
        provider: this.name,
        model,
        latencyMs: Math.round(performance.now() - startedAt),
        cached: false,
      }
    } catch (error) {
      if (error instanceof XendrisProviderError) {
        throw error
      }

      if (error instanceof DOMException && error.name === "AbortError") {
        throw new XendrisProviderError("DeepSeek request timed out.", this.name, 504)
      }

      throw new XendrisProviderError("DeepSeek request failed.", this.name, 502)
    } finally {
      clearTimeout(timeout)
    }
  },
}
