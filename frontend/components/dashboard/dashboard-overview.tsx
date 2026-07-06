"use client"
/* eslint-disable react-hooks/set-state-in-effect */

import * as React from "react"
import { Wallet, TrendingDown, Activity, DollarSign } from "lucide-react"

type OverviewData = {
  balance: string
  currency: string
  hardCap: string
  dailyLimit: string
  monthlyLimit: string
  usageRecords: number
  todayCost: string
}

export function DashboardOverview({ tenantId }: { tenantId: string }) {
  const [data, setData] = React.useState<OverviewData | null>(null)
  const [loading, setLoading] = React.useState(true)
  const [error, setError] = React.useState<string | null>(null)

  React.useEffect(() => {
    setLoading(true)
    setError(null)
    Promise.all([
      fetch(`/api/xendris/wallet?tenant_id=${encodeURIComponent(tenantId)}`).then((r) => r.json()),
      fetch(`/api/xendris/usage?tenant_id=${encodeURIComponent(tenantId)}`).then((r) => r.json()),
    ])
      .then(([wallet, usage]) => {
        const records = Array.isArray(usage) ? usage : []
        const todayStr = new Date().toISOString().slice(0, 10)
        const todayCost = records
          .filter((r: { timestamp?: string; xendris_cost?: string }) => r.timestamp?.startsWith(todayStr))
          .reduce((sum: number, r: { xendris_cost?: string }) => sum + parseFloat(r.xendris_cost || "0"), 0)

        setData({
          balance: wallet.balance || "0.00",
          currency: wallet.currency || "USD",
          hardCap: wallet.hard_cap || "1000.00",
          dailyLimit: wallet.daily_limit || "100.00",
          monthlyLimit: wallet.monthly_limit || "500.00",
          usageRecords: records.length,
          todayCost: todayCost.toFixed(6),
        })
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [tenantId])

  if (loading) {
    return (
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="h-28 animate-pulse rounded-2xl border bg-muted/30" />
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <div className="rounded-2xl border border-red-200 bg-red-50 dark:bg-red-950/20 dark:border-red-800/40 p-6 text-center">
        <p className="text-sm font-medium text-red-600 dark:text-red-400">Error loading dashboard: {error}</p>
        <p className="mt-1 text-xs text-muted-foreground">Make sure the Runtime API is running on port 8001.</p>
      </div>
    )
  }

  if (!data) return null

  const balanceNum = parseFloat(data.balance)
  const hardCapNum = parseFloat(data.hardCap)
  const usagePct = hardCapNum > 0 ? ((balanceNum / hardCapNum) * 100).toFixed(1) : "0"

  const cards = [
    {
      label: "Balance",
      value: `${parseFloat(data.balance).toFixed(2)} ${data.currency}`,
      sub: `${usagePct}% of ${data.hardCap} ${data.currency} cap`,
      icon: Wallet,
      color: "text-emerald-600 dark:text-emerald-400",
      bg: "bg-emerald-50 dark:bg-emerald-950/30",
    },
    {
      label: "Today's Cost",
      value: `${parseFloat(data.todayCost).toFixed(6)} ${data.currency}`,
      sub: `${data.usageRecords} total requests`,
      icon: TrendingDown,
      color: "text-blue-600 dark:text-blue-400",
      bg: "bg-blue-50 dark:bg-blue-950/30",
    },
    {
      label: "Daily Limit",
      value: `${data.dailyLimit} ${data.currency}`,
      sub: `${data.monthlyLimit} monthly limit`,
      icon: Activity,
      color: "text-amber-600 dark:text-amber-400",
      bg: "bg-amber-50 dark:bg-amber-950/30",
    },
    {
      label: "Avg Cost / Request",
      value: data.usageRecords > 0 ? `${(parseFloat(data.todayCost) / data.usageRecords).toFixed(6)} ${data.currency}` : "—",
      sub: `${data.usageRecords} recorded`,
      icon: DollarSign,
      color: "text-purple-600 dark:text-purple-400",
      bg: "bg-purple-50 dark:bg-purple-950/30",
    },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold tracking-tight">Overview</h2>
        <p className="text-sm text-muted-foreground">Resumen de wallet, consumo y métricas para <span className="font-mono font-semibold">{tenantId}</span></p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {cards.map((card) => {
          const Icon = card.icon
          return (
            <div
              key={card.label}
              className="rounded-2xl border bg-card p-5 shadow-xs transition-all hover:shadow-sm"
            >
              <div className="flex items-center justify-between">
                <p className="text-sm font-medium text-muted-foreground">{card.label}</p>
                <div className={`rounded-xl ${card.bg} p-2`}>
                  <Icon className={`size-4 ${card.color}`} />
                </div>
              </div>
              <p className="mt-3 text-2xl font-semibold tracking-tight text-foreground">{card.value}</p>
              <p className="mt-1 text-xs text-muted-foreground">{card.sub}</p>
            </div>
          )
        })}
      </div>

      <div className="rounded-2xl border bg-card p-5 shadow-xs">
        <h3 className="mb-4 text-sm font-semibold text-foreground">Wallet Status</h3>
        <div className="space-y-3">
          <div>
            <div className="flex items-center justify-between text-xs text-muted-foreground mb-1.5">
              <span>Balance usage</span>
              <span>{usagePct}%</span>
            </div>
            <div className="h-2.5 rounded-full bg-muted overflow-hidden">
              <div
                className="h-full rounded-full bg-primary transition-all duration-500"
                style={{ width: `${Math.min(parseFloat(usagePct), 100)}%` }}
              />
            </div>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
            <div className="rounded-xl bg-muted/30 p-3">
              <p className="text-muted-foreground">Daily limit</p>
              <p className="mt-0.5 font-semibold text-foreground">{data.dailyLimit} {data.currency}</p>
            </div>
            <div className="rounded-xl bg-muted/30 p-3">
              <p className="text-muted-foreground">Monthly limit</p>
              <p className="mt-0.5 font-semibold text-foreground">{data.monthlyLimit} {data.currency}</p>
            </div>
            <div className="rounded-xl bg-muted/30 p-3">
              <p className="text-muted-foreground">Hard cap</p>
              <p className="mt-0.5 font-semibold text-foreground">{data.hardCap} {data.currency}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}