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
