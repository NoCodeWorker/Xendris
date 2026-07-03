"use client"

import * as React from "react"
import { Button } from "src/components/ui/button"
import { Textarea } from "src/components/ui/textarea"
import { AgentStatus } from "src/components/xendris/agent-status"
import { DevRuntimeStatus } from "src/components/xendris/dev-runtime-status"
import { MarkdownMessage } from "src/components/xendris/markdown-message"
import { cn } from "src/lib/utils"
import type {
  XendrisChatResponse,
  XendrisStreamDeltaEvent,
  XendrisStreamEvent,
  XendrisStreamMetaEvent,
} from "src/lib/xendris/api-contracts"
import type {
  IntentRoute,
  XendrisConversation,
  XendrisMessage,
  XendrisProviderName,
} from "src/lib/xendris/types"

const INITIAL_ROUTE: IntentRoute = {
  intent: "general",
  confidence: 0,
  matchedTerms: [],
}
const DEV_TOOLS_ENABLED = process.env.NEXT_PUBLIC_XENDRIS_DEV_TOOLS === "true"
const STREAMING_ENABLED = process.env.NEXT_PUBLIC_XENDRIS_STREAMING === "true"
const DEV_PROVIDER_STORAGE_KEY = "xendris.dev.provider.v1"
const PROVIDERS: XendrisProviderName[] = ["mock", "deepseek"]

type ChatPanelProps = {
  conversation: XendrisConversation
  onConversationChange: (conversation: XendrisConversation) => void
  onGeneratingChange?: (isGenerating: boolean) => void
}

function createConversationTitle(message: string) {
  const normalized = message.replace(/\s+/g, " ").trim()
  if (normalized.length <= 42) return normalized || "Nueva conversación"

  return `${normalized.slice(0, 39).trimEnd()}...`
}

function nowIso() {
  return new Date().toISOString()
}

function createMessage(
  role: XendrisMessage["role"],
  content: string,
  metadata?: XendrisMessage["metadata"]
): XendrisMessage {
  return {
    id: crypto.randomUUID(),
    role,
    content,
    createdAt: nowIso(),
    metadata,
  }
}

function readStoredProvider(): XendrisProviderName {
  try {
    const value = window.localStorage.getItem(DEV_PROVIDER_STORAGE_KEY)
    return value === "deepseek" || value === "mock" ? value : "mock"
  } catch {
    return "mock"
  }
}

function parseSseMessage(rawMessage: string) {
  const eventLine = rawMessage
    .split("\n")
    .find((line) => line.startsWith("event: "))
    ?.slice("event: ".length)
  const dataLine = rawMessage
    .split("\n")
    .find((line) => line.startsWith("data: "))
    ?.slice("data: ".length)

  if (!eventLine || !dataLine) return null

  try {
    return {
      event: eventLine,
      data: JSON.parse(dataLine) as XendrisStreamEvent,
    }
  } catch {
    return null
  }
}

export function ChatPanel({
  conversation,
  onConversationChange,
  onGeneratingChange,
}: ChatPanelProps) {
  const [input, setInput] = React.useState("")
  const [route, setRoute] = React.useState<IntentRoute>(INITIAL_ROUTE)
  const [isSending, setIsSending] = React.useState(false)
  const [copiedMessageId, setCopiedMessageId] = React.useState<string | null>(null)
  const [selectedProvider, setSelectedProvider] = React.useState<XendrisProviderName>("mock")
  const messagesEndRef = React.useRef<HTMLDivElement | null>(null)
  const inFlightRef = React.useRef(false)

  const messages = conversation.messages
  const lastAssistantMetadata = [...messages]
    .reverse()
    .find(
      (message) =>
        message.role === "assistant" &&
        message.metadata?.provider &&
        message.metadata?.model &&
        !message.metadata.pending
    )?.metadata
  const providerLabel =
    lastAssistantMetadata?.provider && lastAssistantMetadata.model
      ? `${lastAssistantMetadata.provider} / ${lastAssistantMetadata.model}`
      : "mock / xendris-mock-v0"

  React.useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth", block: "end" })
  }, [messages, isSending])

  React.useEffect(() => {
    setInput("")
    setRoute(INITIAL_ROUTE)
  }, [conversation.id])

  React.useEffect(() => {
    onGeneratingChange?.(isSending)
  }, [isSending, onGeneratingChange])

  React.useEffect(() => {
    if (!DEV_TOOLS_ENABLED) return
    setSelectedProvider(readStoredProvider())
  }, [])

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    await sendMessage()
  }

  function commitConversation(nextMessages: XendrisMessage[]) {
    const updatedAt = nowIso()
    const firstUserMessage = nextMessages.find((message) => message.role === "user")
    const title =
      conversation.title === "Nueva conversación" && firstUserMessage
        ? createConversationTitle(firstUserMessage.content)
        : conversation.title

    const nextConversation: XendrisConversation = {
      ...conversation,
      title,
      messages: nextMessages,
      updatedAt,
    }

    onConversationChange(nextConversation)
    return nextConversation
  }

  async function sendMessage() {
    const content = input.trim()
    if (!content || inFlightRef.current) return

    const userMessage = createMessage("user", content)
    const pendingMessage = createMessage("assistant", "Xendris está pensando…", {
      pending: true,
    })
    const conversationWithPending = commitConversation([...messages, userMessage, pendingMessage])

    setInput("")
    inFlightRef.current = true
    setIsSending(true)

    if (STREAMING_ENABLED) {
      await sendStreamingMessage(content, conversationWithPending, pendingMessage)
      return
    }

    try {
      const apiResponse = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: content,
          ...(DEV_TOOLS_ENABLED ? { provider: selectedProvider } : {}),
        }),
      })

      const data = (await apiResponse.json()) as XendrisChatResponse

      if (!data.ok) {
        const messagesAfterError = conversationWithPending.messages.map((message) =>
          message.id === pendingMessage.id
            ? {
                ...message,
                content: `No he podido completar la respuesta: ${data.error.message}`,
                metadata: undefined,
              }
            : message
        )
        commitConversation(messagesAfterError)
        return
      }

      const messagesAfterSuccess = conversationWithPending.messages.map((message) =>
        message.id === pendingMessage.id
          ? {
              ...message,
              content: data.response,
              metadata: {
                detectedIntent: data.detectedIntent,
                cognitiveMode: data.cognitiveMode,
                provider: data.provider,
                model: data.model,
                cache: data.cache,
                evaluation: data.evaluation,
                controllerDecision: data.controllerDecision,
                repair: data.repair,
                executionSummary: data.executionSummary,
              },
            }
          : message
      )

      setRoute(data.route)
      commitConversation(messagesAfterSuccess)
    } catch {
      const messagesAfterFailure = conversationWithPending.messages.map((message) =>
        message.id === pendingMessage.id
          ? {
              ...message,
              content:
                "No he podido conectar con el contrato de chat local. Revisa que el servidor siga activo.",
              metadata: undefined,
            }
          : message
      )
      commitConversation(messagesAfterFailure)
    } finally {
      inFlightRef.current = false
      setIsSending(false)
    }
  }

  async function sendStreamingMessage(
    content: string,
    conversationWithPending: XendrisConversation,
    pendingMessage: XendrisMessage
  ) {
    let latestMessages = conversationWithPending.messages
    let streamedContent = ""
    let streamMetadata: XendrisMessage["metadata"] | undefined

    function replacePendingMessage(nextMessage: XendrisMessage) {
      latestMessages = latestMessages.map((message) =>
        message.id === pendingMessage.id ? nextMessage : message
      )
      commitConversation(latestMessages)
    }

    try {
      const response = await fetch("/api/chat/stream", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: content,
          ...(DEV_TOOLS_ENABLED ? { provider: selectedProvider } : {}),
        }),
      })

      if (!response.ok || !response.body) {
        let errorMessage = "No he podido iniciar la respuesta en streaming."

        try {
          const data = (await response.json()) as XendrisChatResponse
          if (!data.ok) errorMessage = data.error.message
        } catch {
          // Keep the safe generic message.
        }

        replacePendingMessage({
          ...pendingMessage,
          content: `No he podido completar la respuesta: ${errorMessage}`,
          metadata: undefined,
        })
        return
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ""

      while (true) {
        const { value, done } = await reader.read()
        buffer += decoder.decode(value, { stream: !done })

        const messages = buffer.split("\n\n")
        buffer = messages.pop() ?? ""

        for (const rawMessage of messages) {
          const parsed = parseSseMessage(rawMessage)
          if (!parsed) continue

          if (parsed.data.type === "meta") {
            const data = parsed.data as XendrisStreamMetaEvent
            streamMetadata = {
              detectedIntent: data.detectedIntent,
              cognitiveMode: data.cognitiveMode,
              provider: data.provider,
              model: data.model,
              pending: true,
            }
            setRoute(data.route)
            replacePendingMessage({
              ...pendingMessage,
              content: "",
              metadata: streamMetadata,
            })
          }

          if (parsed.data.type === "delta") {
            const data = parsed.data as XendrisStreamDeltaEvent
            streamedContent += data.content
            replacePendingMessage({
              ...pendingMessage,
              content: streamedContent,
              metadata: {
                ...streamMetadata,
                pending: true,
              },
            })
          }

          if (parsed.data.type === "error") {
            const data = parsed.data
            replacePendingMessage({
              ...pendingMessage,
              content: `No he podido completar la respuesta: ${data.error.message}`,
              metadata: undefined,
            })
            return
          }

          if (parsed.data.type === "done") {
            replacePendingMessage({
              ...pendingMessage,
              content: streamedContent || "Respuesta completada sin contenido.",
              metadata: streamMetadata
                ? {
                    ...streamMetadata,
                    pending: false,
                  }
                : undefined,
            })
          }
        }

        if (done) break
      }
    } catch {
      replacePendingMessage({
        ...pendingMessage,
        content:
          "No he podido conectar con el contrato de streaming local. Revisa que el servidor siga activo.",
        metadata: undefined,
      })
    } finally {
      inFlightRef.current = false
      setIsSending(false)
    }
  }

  function handleKeyDown(event: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key !== "Enter" || event.shiftKey) return
    event.preventDefault()
    void sendMessage()
  }

  async function handleCopyMessage(message: XendrisMessage) {
    if (!navigator.clipboard) return

    try {
      await navigator.clipboard.writeText(message.content)
      setCopiedMessageId(message.id)
      window.setTimeout(() => setCopiedMessageId(null), 1400)
    } catch {
      setCopiedMessageId(null)
    }
  }

  function handleProviderChange(event: React.ChangeEvent<HTMLSelectElement>) {
    const value = event.target.value
    if (value !== "mock" && value !== "deepseek") return

    setSelectedProvider(value)

    try {
      window.localStorage.setItem(DEV_PROVIDER_STORAGE_KEY, value)
    } catch {
      // Dev tooling preference is best-effort only.
    }
  }

  return (
    <section className="flex min-h-0 flex-1 flex-col bg-background">
      <div className="flex-1 overflow-y-auto px-4 py-8">
        {messages.length === 0 ? (
          <div className="mx-auto flex min-h-[58vh] max-w-2xl flex-col items-center justify-center text-center">
            <div className="mb-6 flex size-12 items-center justify-center rounded-2xl border bg-muted text-lg font-semibold">
              X
            </div>
            <h1 className="text-3xl font-semibold tracking-tight text-balance sm:text-4xl">
              ¿En qué trabajamos hoy?
            </h1>
            <p className="mt-4 max-w-xl text-base leading-7 text-muted-foreground">
              Escribe una petición y Xendris elegirá internamente el modo cognitivo adecuado.
            </p>
          </div>
        ) : (
          <div className="mx-auto flex max-w-3xl flex-col gap-7">
            {messages.map((message) => (
              <article
                key={message.id}
                className={cn(
                  "flex w-full gap-3",
                  message.role === "user" ? "justify-end" : "justify-start"
                )}
              >
                {message.role === "assistant" ? (
                  <div className="mt-1 flex size-8 shrink-0 items-center justify-center rounded-full border bg-muted text-xs font-semibold">
                    X
                  </div>
                ) : null}
                <div
                  className={cn(
                    "max-w-[82%] px-4 py-3 text-sm leading-6",
                    message.role === "user"
                      ? "whitespace-pre-line rounded-3xl bg-primary text-primary-foreground"
                      : "rounded-2xl text-foreground"
                  )}
                >
                  {message.role === "assistant" && message.metadata?.pending ? (
                    <div className="flex items-center gap-3 text-muted-foreground">
                      <span>{message.content}</span>
                      <span className="flex items-center gap-1" aria-hidden="true">
                        <span className="size-1.5 animate-pulse rounded-full bg-muted-foreground/70" />
                        <span className="size-1.5 animate-pulse rounded-full bg-muted-foreground/70 [animation-delay:120ms]" />
                        <span className="size-1.5 animate-pulse rounded-full bg-muted-foreground/70 [animation-delay:240ms]" />
                      </span>
                    </div>
                  ) : message.role === "assistant" ? (
                    <MarkdownMessage content={message.content} />
                  ) : (
                    <p>{message.content}</p>
                  )}
                  {message.role === "assistant" && message.metadata?.detectedIntent ? (
                    <p className="mt-3 border-t pt-2 text-xs text-muted-foreground">
                      Intent: {message.metadata.detectedIntent}
                    </p>
                  ) : null}
                  {message.role === "assistant" && !message.metadata?.pending ? (
                    <div className="mt-3 flex items-center gap-2 border-t pt-2">
                      <button
                        type="button"
                        onClick={() => void handleCopyMessage(message)}
                        className="rounded-md px-1.5 py-1 text-xs text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
                      >
                        {copiedMessageId === message.id ? "Copiado" : "Copiar"}
                      </button>
                    </div>
                  ) : null}
                </div>
                {message.role === "user" ? (
                  <div className="mt-1 flex size-8 shrink-0 items-center justify-center rounded-full bg-primary text-xs font-semibold text-primary-foreground">
                    Tú
                  </div>
                ) : null}
              </article>
            ))}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <div className="sticky bottom-0 bg-background/95 px-4 pb-5 pt-3 backdrop-blur">
        <div className="mx-auto max-w-3xl space-y-3">
          <AgentStatus route={route} providerLabel={providerLabel} />
          {DEV_TOOLS_ENABLED ? (
            <>
              <DevRuntimeStatus
                selectedProvider={selectedProvider}
                streamingEnabled={STREAMING_ENABLED}
                lastMetadata={lastAssistantMetadata}
                route={route}
              />
              <div className="flex items-center justify-between rounded-2xl border bg-muted/30 px-3 py-2 text-xs text-muted-foreground">
                <span>Dev provider override</span>
                <label className="flex items-center gap-2">
                  <span className="sr-only">Model provider</span>
                  <select
                    value={selectedProvider}
                    onChange={handleProviderChange}
                    disabled={isSending}
                    className="h-8 rounded-lg border bg-background px-2 text-xs text-foreground outline-none transition-colors focus-visible:ring-3 focus-visible:ring-ring/30 disabled:opacity-50"
                  >
                    {PROVIDERS.map((provider) => (
                      <option key={provider} value={provider}>
                        {provider}
                      </option>
                    ))}
                  </select>
                </label>
              </div>
            </>
          ) : null}
          <form
            className="rounded-3xl border bg-card p-2 shadow-lg shadow-black/5 focus-within:ring-3 focus-within:ring-ring/20"
            onSubmit={handleSubmit}
          >
            <Textarea
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Pregunta, pega código o describe el siguiente paso..."
              rows={1}
              className="max-h-44 min-h-12 resize-none border-0 bg-transparent px-4 py-3 text-[15px] shadow-none focus-visible:ring-0"
            />
            <div className="flex items-center justify-between gap-3 px-2 pb-1">
              <p className="pl-2 text-xs text-muted-foreground">
                Enter para enviar. Shift+Enter para nueva línea.
              </p>
              <Button className="h-9 rounded-full px-4" type="submit" disabled={isSending || !input.trim()}>
                {isSending ? "Enviando..." : "Enviar"}
              </Button>
            </div>
          </form>
        </div>
      </div>
    </section>
  )
}
