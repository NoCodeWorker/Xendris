import { NextResponse } from "next/server"
import { routeIntent } from "src/lib/xendris/intent-router"
import { selectStreamingModelProvider } from "src/lib/xendris/model-provider"
import { XendrisProviderError } from "src/lib/xendris/providers/types"
import { getSystemPrompt } from "src/lib/xendris/system-prompts"
import type {
  XendrisChatErrorResponse,
  XendrisStreamDeltaEvent,
  XendrisStreamDoneEvent,
  XendrisStreamErrorEvent,
  XendrisStreamMetaEvent,
} from "src/lib/xendris/api-contracts"
import type { XendrisProviderName } from "src/lib/xendris/types"

function errorResponse(code: string, message: string, status = 400) {
  return NextResponse.json<XendrisChatErrorResponse>(
    {
      ok: false,
      error: {
        code,
        message,
      },
    },
    { status }
  )
}

function isProviderName(value: unknown): value is XendrisProviderName {
  return value === "mock" || value === "deepseek"
}

function encodeSse(event: string, data: unknown) {
  return `event: ${event}\ndata: ${JSON.stringify(data)}\n\n`
}

export async function POST(request: Request) {
  let body: unknown

  try {
    body = await request.json()
  } catch {
    return errorResponse("INVALID_JSON", "Request body must be valid JSON.")
  }

  if (!body || typeof body !== "object" || !("message" in body)) {
    return errorResponse("MISSING_MESSAGE", 'Request body must include "message".')
  }

  const { message, provider } = body as { message: unknown; provider?: unknown }

  if (typeof message !== "string" || message.trim().length === 0) {
    return errorResponse("INVALID_MESSAGE", '"message" must be a non-empty string.')
  }

  if (provider !== undefined && !isProviderName(provider)) {
    return errorResponse("INVALID_PROVIDER", '"provider" must be "mock" or "deepseek".')
  }

  const route = routeIntent(message)
  const systemPrompt = getSystemPrompt(route.intent)
  let streamingProvider

  try {
    streamingProvider = selectStreamingModelProvider(provider ?? process.env.XENDRIS_MODEL_PROVIDER)
  } catch (error) {
    if (error instanceof XendrisProviderError) {
      return errorResponse("PROVIDER_ERROR", error.message, error.status)
    }

    return errorResponse(
      "STREAMING_PROVIDER_SELECTION_FAILED",
      "Streaming model provider selection failed.",
      502
    )
  }

  const responseRoute = {
    ...route,
    cognitiveMode: systemPrompt.cognitiveMode,
    systemPromptId: systemPrompt.id,
  }

  const encoder = new TextEncoder()
  const stream = new ReadableStream<Uint8Array>({
    async start(controller) {
      try {
        controller.enqueue(
          encoder.encode(
            encodeSse("meta", {
              type: "meta",
              detectedIntent: route.intent,
              cognitiveMode: systemPrompt.cognitiveMode,
              systemPromptId: systemPrompt.id,
              provider: streamingProvider.name,
              model: streamingProvider.model,
              route: responseRoute,
            } satisfies XendrisStreamMetaEvent)
          )
        )

        for await (const chunk of streamingProvider.stream({
          message,
          detectedIntent: route.intent,
          cognitiveMode: systemPrompt.cognitiveMode,
          systemPromptId: systemPrompt.id,
          systemPrompt: systemPrompt.prompt,
        })) {
          const event =
            chunk.type === "delta"
              ? ({
                  type: "delta",
                  content: chunk.content,
                } satisfies XendrisStreamDeltaEvent)
              : ({
                  type: "done",
                } satisfies XendrisStreamDoneEvent)

          controller.enqueue(encoder.encode(encodeSse(event.type, event)))
        }
      } catch (error) {
        const message =
          error instanceof XendrisProviderError
            ? error.message
            : "Streaming model provider request failed."

        controller.enqueue(
          encoder.encode(
            encodeSse("error", {
              type: "error",
              error: {
                code:
                  error instanceof XendrisProviderError
                    ? "PROVIDER_ERROR"
                    : "STREAMING_PROVIDER_REQUEST_FAILED",
                message,
              },
            } satisfies XendrisStreamErrorEvent)
          )
        )
      } finally {
        controller.close()
      }
    },
  })

  return new Response(stream, {
    headers: {
      "Cache-Control": "no-cache, no-transform",
      Connection: "keep-alive",
      "Content-Type": "text/event-stream; charset=utf-8",
    },
  })
}
