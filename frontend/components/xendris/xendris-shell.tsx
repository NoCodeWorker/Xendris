"use client"

import * as React from "react"
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
    <main className="flex min-h-screen bg-background text-foreground">
      <aside className="hidden w-72 shrink-0 border-r bg-muted/35 p-3 lg:flex lg:flex-col">
        <a
          href="/"
          className="flex h-11 items-center rounded-xl px-3 text-sm font-semibold tracking-tight hover:bg-background"
        >
          Xendris AI
        </a>

        <button
          type="button"
          onClick={handleNewConversation}
          disabled={isGenerating}
          className="mt-3 flex h-10 w-full items-center justify-between rounded-xl border bg-background px-3 text-left text-sm font-medium shadow-sm transition-colors hover:bg-muted"
        >
          <span>Nueva conversación</span>
          <span className="text-lg leading-none text-muted-foreground">+</span>
        </button>

        <nav className="mt-6 min-h-0 flex-1 space-y-1 overflow-y-auto">
          {conversations.map((conversation) => (
            <div
              key={conversation.id}
              className={cn(
                "group flex min-h-10 w-full items-center gap-1 rounded-lg px-2 py-1 transition-colors",
                conversation.id === activeConversation?.id
                  ? "bg-background text-foreground shadow-sm"
                  : "text-muted-foreground hover:bg-background hover:text-foreground"
              )}
            >
              <button
                type="button"
                onClick={() => setActiveConversationId(conversation.id)}
                className="min-w-0 flex-1 truncate px-1 text-left text-sm"
              >
                {conversation.title}
              </button>
              <button
                type="button"
                disabled={isGenerating}
                onClick={() => handleRenameConversation(conversation)}
                className="rounded-md px-1.5 py-1 text-xs text-muted-foreground opacity-0 transition-opacity hover:bg-muted hover:text-foreground disabled:pointer-events-none disabled:opacity-30 group-hover:opacity-100"
              >
                Renombrar
              </button>
              <button
                type="button"
                disabled={isGenerating}
                onClick={() => handleDeleteConversation(conversation)}
                className="rounded-md px-1.5 py-1 text-xs text-muted-foreground opacity-0 transition-opacity hover:bg-destructive/10 hover:text-destructive disabled:pointer-events-none disabled:opacity-30 group-hover:opacity-100"
              >
                Eliminar
              </button>
            </div>
          ))}
        </nav>

        <div className="mt-3 rounded-xl border bg-background/70 p-3">
          <p className="text-xs font-medium text-foreground">Modo adaptativo</p>
          <p className="mt-1 text-xs leading-5 text-muted-foreground">
            Xendris decide el modo cognitivo internamente en cada mensaje.
          </p>
        </div>
      </aside>

      <section className="flex min-h-screen min-w-0 flex-1 flex-col">
        <header className="flex h-14 shrink-0 items-center justify-between border-b px-4 lg:px-6">
          <div className="min-w-0">
            <p className="truncate text-sm font-medium">
              {activeConversation?.title ?? EMPTY_TITLE}
            </p>
            <p className="hidden text-xs text-muted-foreground sm:block">
              Interfaz experimental de Xendris AI
            </p>
          </div>
          <div className="flex items-center gap-2">
            <ThemeToggle className="hidden sm:inline-flex" />
            <button
              type="button"
              onClick={handleClearActiveConversation}
              disabled={isGenerating || !activeConversation || activeConversation.messages.length === 0}
              className="rounded-lg px-3 py-1.5 text-sm text-muted-foreground transition-colors hover:bg-muted hover:text-foreground disabled:pointer-events-none disabled:opacity-40"
            >
              Vaciar
            </button>
            <button
              type="button"
              onClick={handleNewConversation}
              disabled={isGenerating}
              className="rounded-lg px-3 py-1.5 text-sm text-muted-foreground transition-colors hover:bg-muted hover:text-foreground disabled:pointer-events-none disabled:opacity-40 lg:hidden"
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
