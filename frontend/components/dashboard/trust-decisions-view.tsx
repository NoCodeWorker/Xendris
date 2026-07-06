"use client"
/* eslint-disable react-hooks/set-state-in-effect */

import * as React from "react"
import { ShieldCheck, ShieldAlert, ShieldX, Scale } from "lucide-react"

export function TrustDecisionsView({ tenantId }: { tenantId: string }) {
  const [councilRecords, setCouncilRecords] = React.useState<number>(0)
  const [loading, setLoading] = React.useState(true)

  React.useEffect(() => {
    setLoading(true)
    fetch(`/api/xendris/usage?tenant_id=${encodeURIComponent(tenantId)}`)
      .then((r) => r.json())
      .then(() => {
        // Currently the ledger is per run_id — we use this for placeholder data
        setCouncilRecords(0)
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [tenantId])

  if (loading) {
    return (
      <div className="space-y-4">
        <div className="h-32 animate-pulse rounded-2xl border bg-muted/30" />
        <div className="h-48 animate-pulse rounded-2xl border bg-muted/30" />
      </div>
    )
  }

  const metrics = [
    {
      label: "Local Guard Resolution Rate",
      value: "—",
      sub: "Requires council escalation data",
      icon: ShieldCheck,
      color: "text-emerald-600 dark:text-emerald-400",
      bg: "bg-emerald-50 dark:bg-emerald-950/30",
    },
    {
      label: "Council Escalations",
      value: String(councilRecords),
      sub: "Total escalated to multi-model council",
      icon: ShieldAlert,
      color: "text-amber-600 dark:text-amber-400",
      bg: "bg-amber-50 dark:bg-amber-950/30",
    },
    {
      label: "Blocked Overclaim Rate",
      value: "—",
      sub: "Requires claim-level data",
      icon: ShieldX,
      color: "text-red-600 dark:text-red-400",
      bg: "bg-red-50 dark:bg-red-950/30",
    },
    {
      label: "Hypothesis Preservation Rate",
      value: "—",
      sub: "Requires hypothesis-tagged output data",
      icon: Scale,
      color: "text-blue-600 dark:text-blue-400",
      bg: "bg-blue-50 dark:bg-blue-950/30",
    },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold tracking-tight">Trust Metrics</h2>
        <p className="text-sm text-muted-foreground">Decisiones de confianza, tasas de resolución y métricas del council</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {metrics.map((m) => {
          const Icon = m.icon
          return (
            <div key={m.label} className="rounded-2xl border bg-card p-5 shadow-xs">
              <div className="flex items-center justify-between">
                <p className="text-sm font-medium text-muted-foreground">{m.label}</p>
                <div className={`rounded-xl ${m.bg} p-2`}>
                  <Icon className={`size-4 ${m.color}`} />
                </div>
              </div>
              <p className="mt-3 text-2xl font-bold tracking-tight text-foreground">{m.value}</p>
              <p className="mt-1 text-xs text-muted-foreground">{m.sub}</p>
            </div>
          )
        })}
      </div>

      <div className="rounded-2xl border bg-card p-5 shadow-xs">
        <h3 className="mb-4 text-sm font-semibold text-foreground">Trust Metrics Definitions</h3>
        <div className="space-y-3 text-sm">
          <div className="rounded-xl bg-muted/30 p-3">
            <p className="font-semibold text-foreground">cost_per_admissible_answer</p>
            <p className="mt-0.5 text-xs text-muted-foreground">
              Costo total dividido por respuestas que pasaron todos los guards sin escalar a council. 
              Métrica central de eficiencia de Xendris.
            </p>
          </div>
          <div className="rounded-xl bg-muted/30 p-3">
            <p className="font-semibold text-foreground">local_guard_resolution_rate</p>
            <p className="mt-0.5 text-xs text-muted-foreground">
              Proporción de outputs que los guards locales resolvieron sin necesidad de escalar a multi-model council.
            </p>
          </div>
          <div className="rounded-xl bg-muted/30 p-3">
            <p className="font-semibold text-foreground">premium_model_avoidance_rate</p>
            <p className="mt-0.5 text-xs text-muted-foreground">
              Proporción de requests donde se evitó usar un modelo frontier (gpt-4, claude-3-opus) 
              porque los guards locales fueron suficientes.
            </p>
          </div>
          <div className="rounded-xl bg-muted/30 p-3">
            <p className="font-semibold text-foreground">human_review_avoidance_rate</p>
            <p className="mt-0.5 text-xs text-muted-foreground">
              Proporción de outputs que habrían requerido revisión humana sin Xendris, pero que los guards resolvieron automáticamente.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}