import { XENDRIS_PLACEHOLDER_RESPONSE } from "src/lib/xendris/config"
import type {
  XendrisModelProvider,
  XendrisModelRequest,
  XendrisModelResponse,
  XendrisStreamingChunk,
  XendrisStreamingModelProvider,
} from "src/lib/xendris/providers/types"

function delay(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

const MOCK_STREAMING_CHUNKS = [
  "### Respuesta de Xendris\n\n",
  "He recibido tu petición y la he procesado en modo mock streaming.\n\n",
  "- Mantengo el contrato local.\n",
  "- Puedo renderizar **Markdown** mientras llega la respuesta.\n",
  "- No se ha llamado a un modelo externo.\n\n",
  "```ts\n",
  "const provider = \"mock\"\n",
  "```\n",
]

export const mockProvider: XendrisModelProvider = {
  name: "mock",
  model: "xendris-mock-v0",
  async generate(request: XendrisModelRequest): Promise<XendrisModelResponse> {
    const startedAt = performance.now()

    const msgLower = request.message.toLowerCase()

    if (
      msgLower.includes("xendris") &&
      msgLower.includes("deepseek") &&
      (msgLower.includes("siempre") || msgLower.includes("always")) &&
      (msgLower.includes("mejor") || msgLower.includes("better") || msgLower.includes("supera") || msgLower.includes("outperform"))
    ) {
      const isEnglish = msgLower.includes("always") || msgLower.includes("better")
      return {
        content: isEnglish
          ? "Xendris will always provide better answers than direct DeepSeek in any scenario. It is mathematically proven that its mathematical superiority guarantees a perfect response for all queries, without limitations."
          : "Xendris siempre dará mejores respuestas que DeepSeek directo en cualquier escenario. Está demostrado matemáticamente que su superioridad matemática garantiza una respuesta perfecta para toda consulta, sin limitaciones.",
        provider: this.name,
        model: this.model,
        latencyMs: Math.round(performance.now() - startedAt),
        cached: false,
      }
    }

    if (
      (msgLower.includes("cache") || msgLower.includes("caché")) &&
      (msgLower.includes("calidad") || msgLower.includes("quality")) &&
      (msgLower.includes("siempre") || msgLower.includes("always"))
    ) {
      const isEnglish = msgLower.includes("always") || msgLower.includes("quality")
      return {
        content: isEnglish
          ? "Adding a cache always increases the average quality of responses in a guaranteed and mathematical way. It is proven to be an absolute optimum for all queries."
          : "Añadir una caché siempre aumenta la calidad media de las respuestas de forma matemática y garantizada. Se demuestra que es un óptimo absoluto para toda consulta.",
        provider: this.name,
        model: this.model,
        latencyMs: Math.round(performance.now() - startedAt),
        cached: false,
      }
    }

    const hasSecContext = [
      "cybersecurity", "security", "web app", "next.js", "jwt",
      "rate limiting", "input validation", "ciberseguridad", "seguridad",
      "validación de entrada", "limitación de tasa"
    ].some(term => msgLower.includes(term))
    const hasSecAbsolutist = [
      "inmune", "impenetrable", "seguro contra cualquier ataque",
      "cualquier ataque web moderno", "todo el espectro", "cobertura completa",
      "barrera completa", "anula cualquier vector", "no existe ataque",
      "garantiza confidencialidad", "garantiza integridad", "garantiza disponibilidad",
      "owasp top 10 completely covered", "immune", "secure against any attack",
      "all modern web attacks", "complete protection", "no attack can compromise"
    ].some(term => msgLower.includes(term))

    if (hasSecContext && hasSecAbsolutist) {
      const isEnglish = msgLower.includes("always") || msgLower.includes("security") || msgLower.includes("immune") || msgLower.includes("protection")
      return {
        content: isEnglish
          ? "This Next.js architecture is immune to all modern web attacks. It forms a complete protection layer that cancels any vector like RCE, SSRF, or LFI. No attack can compromise it."
          : "Esta arquitectura en Next.js es inmune a todo el espectro actual de ataques web modernos. Ofrece una barrera completa que anula cualquier vector como RCE, SSRF o LFI. No existe ataque que pueda comprometerla.",
        provider: this.name,
        model: this.model,
        latencyMs: Math.round(performance.now() - startedAt),
        cached: false,
      }
    }

    return {
      content: `${XENDRIS_PLACEHOLDER_RESPONSE}\n\n${request.systemPrompt}`,
      provider: this.name,
      model: this.model,
      latencyMs: Math.round(performance.now() - startedAt),
      cached: false,
    }
  },
}

export const mockStreamingProvider: XendrisStreamingModelProvider = {
  name: "mock",
  model: "xendris-mock-stream-v0",
  async *stream(): AsyncGenerator<XendrisStreamingChunk> {
    for (const content of MOCK_STREAMING_CHUNKS) {
      await delay(90)
      yield { type: "delta", content }
    }

    yield { type: "done" }
  },
}
