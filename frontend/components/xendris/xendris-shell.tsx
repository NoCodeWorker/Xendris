"use client"
/* eslint-disable react-hooks/set-state-in-effect */


import * as React from "react"
import Link from "next/link"
import { Pencil, Trash2 } from "lucide-react"
import { ThemeToggle } from "src/components/theme-toggle"


import { ChatPanel } from "src/components/xendris/chat-panel"
import { cn } from "src/lib/utils"
import type { XendrisConversation } from "src/lib/xendris/types"

const STORAGE_KEY = "xendris.conversations.v1"
const EMPTY_TITLE = "Nueva conversación"

function createConversation(): XendrisConversation {
  const now = new Date().toISOString()

  return {
    id: crypto.randomUUID(),
    title: EMPTY_TITLE,
    messages: [],
    createdAt: now,
    updatedAt: now,
  }
}

function isConversation(value: unknown): value is XendrisConversation {
  if (!value || typeof value !== "object") return false

  const conversation = value as Partial<XendrisConversation>

  return (
    typeof conversation.id === "string" &&
    typeof conversation.title === "string" &&
    Array.isArray(conversation.messages) &&
    typeof conversation.createdAt === "string" &&
    typeof conversation.updatedAt === "string"
  )
}

function loadStoredConversations(): XendrisConversation[] {
  try {
    const stored = window.localStorage.getItem(STORAGE_KEY)
    if (!stored) return []

    const parsed = JSON.parse(stored) as unknown
    if (!Array.isArray(parsed)) return []

    return parsed.filter(isConversation).sort((a, b) => b.updatedAt.localeCompare(a.updatedAt))
  } catch {
    return []
  }
}

function saveStoredConversations(conversations: XendrisConversation[]) {
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(conversations))
  } catch {
    // Local conversation persistence is best-effort until a backend exists.
  }
}

export function XendrisShell() {
  const [conversations, setConversations] = React.useState<XendrisConversation[]>([])
  const [activeConversationId, setActiveConversationId] = React.useState<string | null>(null)
  const [isHydrated, setIsHydrated] = React.useState(false)
  const [isGenerating, setIsGenerating] = React.useState(false)

  React.useEffect(() => {
    const storedConversations = loadStoredConversations()
    const nextConversations =
      storedConversations.length > 0 ? storedConversations : [createConversation()]

    setConversations(nextConversations)
    setActiveConversationId(nextConversations[0]?.id ?? null)
    setIsHydrated(true)
  }, [])

  React.useEffect(() => {
    if (!isHydrated) return
    saveStoredConversations(conversations)
  }, [conversations, isHydrated])

  const activeConversation =
    conversations.find((conversation) => conversation.id === activeConversationId) ?? conversations[0]

  function handleNewConversation() {
    if (isGenerating) return

    const conversation = createConversation()
    setConversations((current) => [conversation, ...current])
    setActiveConversationId(conversation.id)
  }

  function updateActiveConversation(nextConversation: XendrisConversation) {
    setConversations((current) => {
      const updated = current.map((conversation) =>
        conversation.id === nextConversation.id ? nextConversation : conversation
      )

      return updated.sort((a, b) => b.updatedAt.localeCompare(a.updatedAt))
    })
  }

  function handleRenameConversation(conversation: XendrisConversation) {
    if (isGenerating) return

    const nextTitle = window.prompt("Renombrar conversación", conversation.title)?.trim()
    if (!nextTitle) return

    const updatedAt = new Date().toISOString()

    setConversations((current) =>
      current
        .map((item) =>
          item.id === conversation.id ? { ...item, title: nextTitle, updatedAt } : item
        )
        .sort((a, b) => b.updatedAt.localeCompare(a.updatedAt))
    )
  }

  function handleDeleteConversation(conversation: XendrisConversation) {
    if (isGenerating) return

    const shouldDelete = window.confirm(`Eliminar "${conversation.title}"?`)
    if (!shouldDelete) return

    const remaining = conversations.filter((item) => item.id !== conversation.id)
    const nextConversations = remaining.length > 0 ? remaining : [createConversation()]
    const nextActiveId =
      conversation.id === activeConversationId
        ? nextConversations[0]?.id ?? null
        : activeConversationId

    setConversations(nextConversations.sort((a, b) => b.updatedAt.localeCompare(a.updatedAt)))
    setActiveConversationId(nextActiveId)
  }

  function handleClearActiveConversation() {
    if (isGenerating || !activeConversation) return

    const shouldClear = window.confirm(`Vaciar "${activeConversation.title}"?`)
    if (!shouldClear) return

    const updatedAt = new Date().toISOString()

    updateActiveConversation({
      ...activeConversation,
      title: EMPTY_TITLE,
      messages: [],
      updatedAt,
    })
  }

  return (
    <main className="flex h-screen w-screen overflow-hidden bg-background text-foreground">
      <aside className="hidden w-80 shrink-0 border-r bg-muted/25 p-4 lg:flex lg:flex-col">
        <Link
          href="/"
          className="flex h-12 items-center gap-2 rounded-xl px-3 text-base font-bold tracking-tight transition-colors hover:bg-muted"
        >
          <div className="flex size-7 items-center justify-center rounded-lg bg-primary text-xs font-black text-primary-foreground shadow-sm">
            X
          </div>
          <span>Xendris AI</span>
        </Link>

        <button
          type="button"
          onClick={handleNewConversation}
          disabled={isGenerating}
          className="mt-4 flex h-11 w-full items-center justify-between rounded-xl border bg-background px-4 text-left text-sm font-semibold shadow-sm transition-all hover:bg-muted hover:border-primary/20 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/30 disabled:opacity-50"
        >
          <span>Nueva conversación</span>
          <span className="text-xl leading-none text-muted-foreground font-light">+</span>
        </button>

        <nav className="mt-6 min-h-0 flex-1 space-y-1.5 overflow-y-auto">
          {conversations.map((conversation) => (
            <div
              key={conversation.id}
              className={cn(
                "group relative flex h-11 w-full items-center gap-1.5 rounded-xl pl-4 pr-3 py-1 transition-all duration-150 border",
                conversation.id === activeConversation?.id
                  ? "bg-background text-foreground shadow-xs border-border/80 font-semibold"
                  : "text-muted-foreground hover:bg-background/50 hover:text-foreground border-transparent"
              )}
            >
              {conversation.id === activeConversation?.id && (
                <span className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-5 rounded-r bg-primary" />
              )}
              <button
                type="button"
                onClick={() => setActiveConversationId(conversation.id)}
                className="min-w-0 flex-1 truncate px-1 text-left text-sm font-medium"
              >
                {conversation.title}
              </button>
              <button
                type="button"
                disabled={isGenerating}
                onClick={() => handleRenameConversation(conversation)}
                className="rounded-lg p-1.5 text-muted-foreground opacity-0 hover:bg-muted hover:text-foreground transition-all duration-150 disabled:pointer-events-none disabled:opacity-30 group-hover:opacity-100"
                aria-label="Renombrar conversación"
              >
                <Pencil className="size-3.5" />
              </button>
              <button
                type="button"
                disabled={isGenerating}
                onClick={() => handleDeleteConversation(conversation)}
                className="rounded-lg p-1.5 text-muted-foreground opacity-0 hover:bg-destructive/15 hover:text-destructive transition-all duration-150 disabled:pointer-events-none disabled:opacity-30 group-hover:opacity-100"
                aria-label="Eliminar conversación"
              >
                <Trash2 className="size-3.5" />
              </button>
            </div>
          ))}
        </nav>

        <div className="mt-3 rounded-xl border bg-background/70 p-3 shadow-xs">
          <p className="text-xs font-semibold text-foreground">Modo adaptativo</p>
          <p className="mt-1 text-[11px] leading-relaxed text-muted-foreground">
            Xendris decide el modo cognitivo internamente en cada mensaje.
          </p>
        </div>
      </aside>

      <section className="flex h-full min-w-0 flex-1 flex-col overflow-hidden">
        <header className="flex h-14 shrink-0 items-center justify-between border-b bg-background/55 backdrop-blur-md px-6">
          <div className="min-w-0 flex items-center gap-2.5">
            <span className="inline-block size-2 rounded-full bg-emerald-500 animate-pulse shrink-0" />
            <div>
              <p className="truncate text-sm font-semibold tracking-tight text-foreground">
                {activeConversation?.title ?? EMPTY_TITLE}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <ThemeToggle className="scale-90" />
            {activeConversation && activeConversation.messages.length > 0 ? (
              <button
                type="button"
                onClick={handleClearActiveConversation}
                disabled={isGenerating}
                className="flex items-center gap-1.5 h-9 rounded-xl px-3 text-xs font-medium text-muted-foreground/80 hover:bg-muted hover:text-foreground transition-all disabled:opacity-40 disabled:pointer-events-none"
                aria-label="Vaciar conversación"
              >
                <Trash2 className="size-3.5 shrink-0" />
                <span>Vaciar</span>
              </button>
            ) : null}
            <button
              type="button"
              onClick={handleNewConversation}
              disabled={isGenerating}
              className="flex items-center gap-1.5 h-9 rounded-xl border px-3 text-xs font-semibold text-muted-foreground hover:bg-muted hover:text-foreground transition-all shadow-xs disabled:opacity-40 lg:hidden"
            >
              Nueva
            </button>
          </div>
        </header>
        {activeConversation ? (
          <ChatPanel
            conversation={activeConversation}
            onConversationChange={updateActiveConversation}
            onGeneratingChange={setIsGenerating}
          />
        ) : null}
      </section>
    </main>
  )
}
