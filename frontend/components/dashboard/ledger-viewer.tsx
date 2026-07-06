"use client"

import * as React from "react"
import { Search, BookOpen } from "lucide-react"

type LedgerRecord = {
  record_id: string
  event_type: string
  decision: string
  reason: string
  model_id?: string
  provider?: string
  sequence_index?: number
  timestamp?: string
  metadata?: Record<string, unknown>
}

export function LedgerViewer() {
  const [runId, setRunId] = React.useState("")
  const [input, setInput] = React.useState("")
  const [records, setRecords] = React.useState<LedgerRecord[]>([])
  const [loading, setLoading] = React.useState(false)
  const [error, setError] = React.useState<string | null>(null)
  const [searched, setSearched] = React.useState(false)

  async function handleSearch(e: React.FormEvent) {
    e.preventDefault()
    const id = input.trim()
    if (!id) return

    setRunId(id)
    setLoading(true)
    setError(null)
    setSearched(true)

    try {
      const res = await fetch(`/api/xendris/ledger?run_id=${encodeURIComponent(id)}`)
      if (!res.ok) {
        if (res.status === 404) {
          setError(`Ledger not found for run_id: ${id}`)
          setRecords([])
          return
        }
        setError(`Error ${res.status}`)
        setRecords([])
        return
      }
      const data = await res.json()
      setRecords(Array.isArray(data.records) ? data.records : [])
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error")
      setRecords([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold tracking-tight">Ledger Viewer</h2>
        <p className="text-sm text-muted-foreground">Busca eventos de confianza por run_id</p>
      </div>

      <form onSubmit={handleSearch} className="flex gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 size-4 text-muted-foreground" />
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="run_id (e.g. run-req-abc123)..."
            className="h-11 w-full rounded-2xl border bg-card pl-10 pr-4 text-sm outline-none transition-colors focus:border-ring focus:ring-2 focus:ring-ring/20"
          />
        </div>
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="h-11 rounded-2xl bg-primary px-6 text-sm font-semibold text-primary-foreground shadow-sm transition-all hover:bg-primary/85 disabled:opacity-50"
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </form>

      {error && (
        <div className="rounded-2xl border border-red-200 bg-red-50 dark:bg-red-950/20 dark:border-red-800/40 p-6 text-center">
          <p className="text-sm font-medium text-red-600 dark:text-red-400">{error}</p>
        </div>
      )}

      {searched && !loading && !error && records.length === 0 && (
        <div className="rounded-2xl border bg-card p-12 text-center">
          <BookOpen className="mx-auto size-8 text-muted-foreground/50" />
          <p className="mt-3 text-sm text-muted-foreground">No ledger records found.</p>
        </div>
      )}

      {records.length > 0 && (
        <div className="space-y-3">
          <p className="text-xs text-muted-foreground">
            {records.length} record{records.length !== 1 ? "s" : ""} for <span className="font-mono font-semibold">{runId}</span>
          </p>
          {records.map((rec, i) => (
            <div key={rec.record_id || i} className="rounded-2xl border bg-card p-4 shadow-xs">
              <div className="flex items-start justify-between gap-4">
                <div className="min-w-0">
                  <div className="flex items-center gap-2">
                    <span className={`inline-flex rounded-full px-2 py-0.5 text-[11px] font-semibold ${
                      rec.event_type?.includes("BLOCKED") || rec.event_type?.includes("ESCALATION")
                        ? "bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300"
                        : rec.event_type?.includes("ROUTING")
                          ? "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300"
                          : "bg-muted text-muted-foreground"
                    }`}>
                      {rec.event_type || "UNKNOWN"}
                    </span>
                    <span className={`text-xs font-semibold ${
                      rec.decision === "APPROVED" || rec.decision === "ALLOW"
                        ? "text-emerald-600 dark:text-emerald-400"
                        : rec.decision === "BLOCKED" || rec.decision === "BLOCK"
                          ? "text-red-600 dark:text-red-400"
                          : "text-muted-foreground"
                    }`}>
                      {rec.decision}
                    </span>
                  </div>
                  <p className="mt-1.5 text-xs text-muted-foreground">{rec.reason}</p>
                  {rec.model_id && (
                    <p className="mt-1 text-[11px] font-mono text-muted-foreground">
                      {rec.provider && `${rec.provider}/`}{rec.model_id}
                    </p>
                  )}
                </div>
                <span className="shrink-0 text-[11px] font-mono text-muted-foreground">
                  #{rec.sequence_index ?? i}
                </span>
              </div>
              {rec.metadata && Object.keys(rec.metadata).length > 0 && (
                <details className="mt-2">
                  <summary className="cursor-pointer text-[11px] text-muted-foreground hover:text-foreground transition-colors">
                    Metadata
                  </summary>
                  <pre className="mt-2 overflow-x-auto rounded-xl bg-muted/30 p-3 text-[11px] font-mono text-muted-foreground">
                    {JSON.stringify(rec.metadata, null, 2)}
                  </pre>
                </details>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}