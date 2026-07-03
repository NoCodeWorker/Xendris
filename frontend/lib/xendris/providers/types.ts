import type { XendrisIntent, XendrisProviderName } from "src/lib/xendris/types"
export type { XendrisProviderName }

export interface XendrisModelRequest {
  message: string
  detectedIntent: XendrisIntent
  cognitiveMode: string
  systemPromptId: string
  systemPrompt: string
}

export interface XendrisModelResponse {
  content: string
  provider: string
  model: string
  latencyMs?: number
  cached?: boolean
}

export class XendrisProviderError extends Error {
  status: number
  provider: string

  constructor(message: string, provider: string, status = 502) {
    super(message)
    this.name = "XendrisProviderError"
    this.provider = provider
    this.status = status
  }
}

export interface XendrisModelProvider {
  name: string
  model: string
  generate(request: XendrisModelRequest): Promise<XendrisModelResponse>
}

export type XendrisStreamingModelRequest = XendrisModelRequest

export type XendrisStreamingChunk =
  | {
      type: "delta"
      content: string
    }
  | {
      type: "done"
    }

export interface XendrisStreamingModelProvider {
  name: string
  model: string
  stream(request: XendrisStreamingModelRequest): AsyncGenerator<XendrisStreamingChunk>
}
