"use client"
/* eslint-disable react-hooks/set-state-in-effect */


import * as React from "react"
import { ArrowUp, Copy, Check } from "lucide-react"
import { Button } from "src/components/ui/button"
import { DevRuntimeStatus } from "src/components/xendris/dev-runtime-status"
import { TrustPanel } from "src/components/xendris/trust-panel"
import { CostPanel } from "src/components/xendris/cost-panel"


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
  XendrisMode,
} from "src/lib/xendris/types"

const INITIAL_ROUTE: IntentRoute = {
  intent: "general",
  confidence: 0,
  matchedTerms: [],
}
const DEV_TOOLS_ENABLED = process.env.NEXT_PUBLIC_XENDRIS_DEV_TOOLS === "true"
const STREAMING_ENABLED = process.env.NEXT_PUBLIC_XENDRIS_STREAMING === "true"
const DEV_PROVIDER_STORAGE_KEY = "xendris.dev.provider.v1"
const PROVIDERS: XendrisProviderName[] = ["mock", "deepseek", "runtime"]

type ChatPanelProps = {
  conversation: XendrisConversation
  onConversationChange: (conversation: XendrisConversation) => void
  onGeneratingChange?: (isGenerating: boolean) => void
  mode?: XendrisMode
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
    return value === "deepseek" || value === "mock" || value === "runtime" ? value : "mock"
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
  mode = "normal",
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

    if (STREAMING_ENABLED && selectedProvider !== "runtime") {
      await sendStreamingMessage(content, conversationWithPending, pendingMessage)
      return
    }

    try {
      if (selectedProvider === "runtime") {
        const apiResponse = await fetch("/api/xendris/runtime", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            message: content,
            mode: mode,
          }),
        })

        const data = await apiResponse.json()

        if (!data.ok) {
          const messagesAfterError = conversationWithPending.messages.map((message) =>
            message.id === pendingMessage.id
              ? { ...message, content: `Runtime error: ${data.error.message}`, metadata: undefined }
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
                  provider: data.provider,
                  model: data.model,
                  council: data.council,
                  wallet: data.wallet,
                },
              }
            : message
        )

        commitConversation(messagesAfterSuccess)
      } else {
        const apiResponse = await fetch("/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            message: content,
            ...(DEV_TOOLS_ENABLED ? { provider: selectedProvider } : {}),
          }),
        })

        const data = (await apiResponse.json()) as XendrisChatResponse

        if (!data.ok) {
          const messagesAfterError = conversationWithPending.messages.map((message) =>
            message.id === pendingMessage.id
              ? { ...message, content: `No he podido completar la respuesta: ${data.error.message}`, metadata: undefined }
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
      }
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : "Error desconocido"
      const messagesAfterFailure = conversationWithPending.messages.map((message) =>
        message.id === pendingMessage.id
          ? { ...message, content: `Error: ${errorMsg}`, metadata: undefined }
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
    if (value !== "mock" && value !== "deepseek" && value !== "runtime") return

    setSelectedProvider(value)

    try {
      window.localStorage.setItem(DEV_PROVIDER_STORAGE_KEY, value)
    } catch {
      // Dev tooling preference is best-effort only.
    }
  }

  return (
    <section className="flex min-h-0 flex-1 flex-col bg-background">
      <div className="flex-1 overflow-y-auto pt-6 pb-4 md:pt-8 md:pb-6">
        {messages.length === 0 ? (
          <div className="mx-auto flex min-h-[58vh] max-w-3xl flex-col items-center justify-center text-center px-8">
            <div className="mb-7 flex size-12 items-center justify-center rounded-2xl bg-[oklch(0.26_0.018_107.4)] text-lg font-black text-white shadow-md border border-[oklch(0.35_0.025_107.4)]">
              X
            </div>
            <h1 className="text-balance text-3xl font-semibold tracking-tight sm:text-4xl">
              ¿En qué trabajamos hoy?
            </h1>
            <p className="mt-4 max-w-xl text-base leading-7 text-muted-foreground">
              Escribe una petición y Xendris elegirá internamente el modo cognitivo adecuado.
            </p>
            <div className="mt-10 grid gap-3 sm:grid-cols-3 max-w-2xl w-full">
              {[
                {
                  label: "Analizar candidato v4.7",
                  description: "Revisar accesibilidad de PHI",
                  prompt: "Analiza la accesibilidad y y_true para el candidato v4.7 PHI",
                },
                {
                  label: "Verificar matriz cognitiva",
                  description: "Revisar reglas de decisión",
                  prompt: "Verifica la matriz de decisión cognitiva y mapeo de estados",
                },
                {
                  label: "Ejecutar screening PHI",
                  description: "Ejecutar campaña en phyng",
                  prompt: "Ejecuta la campaña de screening de accesibilidad PHI",
                },
              ].map((chip, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => setInput(chip.prompt)}
                  className="flex flex-col items-start gap-1 rounded-2xl border bg-muted/10 p-4 text-left transition-all hover:bg-muted/20 hover:border-primary/25 hover:shadow-xs group focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/30"
                >
                  <span className="text-xs font-semibold text-foreground group-hover:text-primary transition-colors">
                    {chip.label}
                  </span>
                  <span className="text-[11px] text-muted-foreground leading-normal">
                    {chip.description}
                  </span>
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="mx-auto flex w-full max-w-[1180px] flex-col gap-6 px-8">
            {messages.map((message) => (
              <article
                key={message.id}
                className={cn(
                  "flex w-full gap-3",
                  message.role === "user" ? "justify-end" : "justify-start"
                )}
              >
                {message.role === "assistant" ? (
                  <div className="mt-1 flex size-8 shrink-0 items-center justify-center rounded-full bg-[oklch(0.92_0.005_107.4)] border border-[oklch(0.85_0.01_107.4)] text-[oklch(0.20_0.012_107.4)] dark:bg-[oklch(0.20_0.012_107.4)] dark:border-[oklch(0.25_0.015_107.4)] dark:text-white text-[11px] font-black shadow-sm select-none">
                    X
                  </div>
                ) : null}
                <div
                  className={cn(
                    "px-5 py-4 text-sm leading-6 transition-all duration-200",
                    message.role === "user"
                      ? "chat-bubble-user whitespace-pre-line max-w-[74%]"
                      : "chat-bubble-assistant max-w-[82%]"
                  )}
                >
                  <p className="mb-2 text-xs font-semibold opacity-70">
                    {message.role === "user" ? "Tú" : "Xendris"}
                  </p>
                  {message.role === "assistant" && message.metadata?.pending ? (
                    <div className="flex items-center gap-3 opacity-90">
                      <span>{message.content}</span>
                      <span className="flex items-center gap-1" aria-hidden="true">
                        <span className="size-1.5 animate-pulse rounded-full bg-current opacity-70" />
                        <span className="size-1.5 animate-pulse rounded-full bg-current opacity-70 [animation-delay:120ms]" />
                        <span className="size-1.5 animate-pulse rounded-full bg-current opacity-70 [animation-delay:240ms]" />
                      </span>
                    </div>
                  ) : message.role === "assistant" ? (
                    <MarkdownMessage content={message.content} />
                  ) : (
                    <p>{message.content}</p>
                  )}
                  {message.role === "assistant" && message.metadata?.council && !message.metadata?.pending ? (
                    <TrustPanel
                      verdict={message.metadata.council.verdict}
                      guardResults={message.metadata.council.guard_results}
                      requiresCouncil={message.metadata.council.requires_council}
                    />
                  ) : null}
                  {message.role === "assistant" && message.metadata?.wallet && !message.metadata?.pending ? (
                    <CostPanel
                      charge={message.metadata.wallet.charge}
                      usageId={message.metadata.wallet.usage_id}
                      provider={message.metadata.provider || ""}
                      model={message.metadata.model || ""}
                    />
                  ) : null}
                  {message.role === "assistant" && !message.metadata?.pending ? (
                    <div className="mt-3 flex items-center gap-2 border-t border-current/15 pt-2">
                      <button
                        type="button"
                        aria-label="Copiar respuesta de Xendris"
                        onClick={() => void handleCopyMessage(message)}
                        className="flex items-center gap-1.5 rounded-md px-2 py-1 text-xs opacity-75 transition-all hover:bg-current/10 hover:opacity-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-current/25"
                      >
                        {copiedMessageId === message.id ? (
                          <>
                            <Check className="size-3.5" />
                            <span>Copiado</span>
                          </>
                        ) : (
                          <>
                            <Copy className="size-3.5" />
                            <span>Copiar</span>
                          </>
                        )}
                      </button>
                    </div>
                  ) : null}
                </div>
                {message.role === "user" ? (
                  <div className="mt-1 flex size-8 shrink-0 items-center justify-center rounded-full bg-[oklch(0.90_0.015_107.4)] border border-[oklch(0.80_0.02_107.4)] text-[oklch(0.25_0.018_107.4)] dark:bg-[oklch(0.26_0.018_107.4)] dark:border-[oklch(0.35_0.025_107.4)] dark:text-white text-[10px] font-bold shadow-sm select-none">
                    Tú
                  </div>
                ) : null}
              </article>
            ))}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <div className="sticky bottom-0 border-t bg-background/90 px-4 pb-5 pt-4 backdrop-blur-xl">
        <div className="mx-auto w-full max-w-[1180px] px-8">
          {DEV_TOOLS_ENABLED ? (
            <div className="mb-3 flex flex-col gap-3">
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
            </div>
          ) : null}
          <form
            className="rounded-[1.75rem] border border-border bg-card p-3 shadow-md transition-all duration-200 focus-within:border-primary/45 focus-within:ring-4 focus-within:ring-primary/10"
            onSubmit={handleSubmit}
          >
            <label className="sr-only" htmlFor="xendris-composer">
              Mensaje para Xendris
            </label>
            <textarea
              id="xendris-composer"
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Pregunta, pega código o describe el siguiente paso..."
              rows={1}
              className="w-full field-sizing-content max-h-44 min-h-[64px] resize-none border-0 bg-transparent px-4 py-3 text-[15px] leading-7 shadow-none placeholder:text-muted-foreground/75 outline-none focus:outline-none focus:ring-0 focus:border-0 focus-visible:ring-0"
            />
            <div className="flex flex-col gap-3 px-2 pb-1 sm:flex-row sm:items-center sm:justify-between">
              <p className="text-sm text-muted-foreground">
                Enter para enviar. Shift+Enter para nueva línea.
              </p>
              <Button
                className="h-10 rounded-full pl-5 pr-4 sm:min-w-24 flex items-center justify-center gap-1.5 shadow-sm active:scale-95 transition-all"
                type="submit"
                disabled={isSending || !input.trim()}
                aria-label="Enviar mensaje"
              >
                <span>{isSending ? "Enviando" : "Enviar"}</span>
                <ArrowUp className="size-4 shrink-0" />
              </Button>
            </div>
          </form>
        </div>
      </div>
    </section>
  )
}
