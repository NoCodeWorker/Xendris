"use client"
/* eslint-disable react-hooks/set-state-in-effect */

import * as React from "react"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from "recharts"

type UsageRecord = {
  usage_id: string
  model_id: string
  provider: string
  input_tokens: number
  output_tokens: number
  provider_cost: string
  xendris_cost: string
  timestamp: string
}

const COLORS = ["#22c55e", "#3b82f6", "#a855f7", "#f59e0b", "#ef4444"]

export function UsageAnalyticsView({ tenantId }: { tenantId: string }) {
  const [records, setRecords] = React.useState<UsageRecord[]>([])
  const [loading, setLoading] = React.useState(true)
  const [error, setError] = React.useState<string | null>(null)

  React.useEffect(() => {
    setLoading(true)
    fetch(`/api/xendris/usage?tenant_id=${encodeURIComponent(tenantId)}`)
      .then((r) => r.json())
      .then((data) => {
        setRecords(Array.isArray(data) ? data : [])
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [tenantId])

  if (loading) {
    return (
      <div className="space-y-4">
        <div className="h-48 animate-pulse rounded-2xl border bg-muted/30" />
        <div className="h-64 animate-pulse rounded-2xl border bg-muted/30" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="rounded-2xl border border-red-200 bg-red-50 dark:bg-red-950/20 dark:border-red-800/40 p-6 text-center">
        <p className="text-sm font-medium text-red-600 dark:text-red-400">Error: {error}</p>
      </div>
    )
  }

  const totalCost = records.reduce((sum, r) => sum + parseFloat(r.xendris_cost || "0"), 0)
  const totalTokens = records.reduce((sum, r) => sum + r.input_tokens + r.output_tokens, 0)
  const avgCostPerRequest = records.length > 0 ? totalCost / records.length : 0
  const costPerToken = totalTokens > 0 ? totalCost / totalTokens : 0

  const modelBreakdown: Record<string, { cost: number; count: number }> = {}
  for (const r of records) {
    const key = r.model_id || r.provider || "unknown"
    if (!modelBreakdown[key]) modelBreakdown[key] = { cost: 0, count: 0 }
    modelBreakdown[key].cost += parseFloat(r.xendris_cost || "0")
    modelBreakdown[key].count += 1
  }

  const pieData = Object.entries(modelBreakdown).map(([name, { cost, count }]) => ({
    name,
    value: Math.round(cost * 1000000) / 1000000,
    requests: count,
  }))

  const dailyCosts: Record<string, number> = {}
  for (const r of records) {
    const day = r.timestamp?.slice(0, 10) || "unknown"
    dailyCosts[day] = (dailyCosts[day] || 0) + parseFloat(r.xendris_cost || "0")
  }

  const barData = Object.entries(dailyCosts)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([date, cost]) => ({ date: date.slice(5), cost: Math.round(cost * 1000000) / 1000000 }))

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold tracking-tight">Usage Analytics</h2>
        <p className="text-sm text-muted-foreground">Coste por respuesta, desglose por modelo y consumo diario</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-4">
        <div className="rounded-2xl border bg-card p-5 shadow-xs">
          <p className="text-sm font-medium text-muted-foreground">Total Cost</p>
          <p className="mt-2 text-2xl font-bold tracking-tight text-foreground">{totalCost.toFixed(6)}</p>
          <p className="text-xs text-muted-foreground">USD</p>
        </div>
        <div className="rounded-2xl border bg-card p-5 shadow-xs">
          <p className="text-sm font-medium text-muted-foreground">Total Tokens</p>
          <p className="mt-2 text-2xl font-bold tracking-tight text-foreground">{totalTokens.toLocaleString()}</p>
        </div>
        <div className="rounded-2xl border bg-card p-5 shadow-xs">
          <p className="text-sm font-medium text-muted-foreground">Avg Cost / Request</p>
          <p className="mt-2 text-2xl font-bold tracking-tight text-foreground">{avgCostPerRequest.toFixed(6)}</p>
          <p className="text-xs text-muted-foreground">USD</p>
        </div>
        <div className="rounded-2xl border bg-card p-5 shadow-xs">
          <p className="text-sm font-medium text-muted-foreground">Cost / Token</p>
          <p className="mt-2 text-2xl font-bold tracking-tight text-foreground">{costPerToken.toFixed(8)}</p>
          <p className="text-xs text-muted-foreground">USD</p>
        </div>
      </div>

      <div className="grid gap-6 sm:grid-cols-2">
        <div className="rounded-2xl border bg-card p-5 shadow-xs">
          <h3 className="mb-4 text-sm font-semibold text-foreground">Model Spend Breakdown</h3>
          {pieData.length === 0 ? (
            <p className="text-sm text-muted-foreground py-8 text-center">No usage data.</p>
          ) : (
            <ResponsiveContainer width="100%" height={260}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={2}
                  dataKey="value"
                >
                  {pieData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} stroke="transparent" />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ borderRadius: 12, border: "1px solid var(--border)" }}
                  formatter={(value) => [`${Number(value).toFixed(6)} USD`]}
                />
                <Legend
                  formatter={(value) => (
                    <span className="text-xs text-muted-foreground">{String(value)}</span>
                  )}
                />
              </PieChart>
            </ResponsiveContainer>
          )}
        </div>

        <div className="rounded-2xl border bg-card p-5 shadow-xs">
          <h3 className="mb-4 text-sm font-semibold text-foreground">Daily Cost (USD)</h3>
          {barData.length === 0 ? (
            <p className="text-sm text-muted-foreground py-8 text-center">No usage data.</p>
          ) : (
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" strokeOpacity={0.4} />
                <XAxis dataKey="date" tick={{ fontSize: 11 }} stroke="var(--muted-foreground)" />
                <YAxis tick={{ fontSize: 11 }} stroke="var(--muted-foreground)" />
                <Tooltip
                  contentStyle={{ borderRadius: 12, border: "1px solid var(--border)" }}
                  formatter={(value) => [`${Number(value).toFixed(6)} USD`]}
                />
                <Bar dataKey="cost" fill="var(--primary)" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      <div className="rounded-2xl border bg-card p-5 shadow-xs">
        <h3 className="mb-4 text-sm font-semibold text-foreground">Request Log</h3>
        {records.length === 0 ? (
          <p className="text-sm text-muted-foreground py-8 text-center">No requests yet.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="border-b text-xs text-muted-foreground">
                  <th className="pb-2 pr-3 font-semibold">Model</th>
                  <th className="pb-2 pr-3 font-semibold">Provider</th>
                  <th className="pb-2 pr-3 font-semibold">Tokens</th>
                  <th className="pb-2 pr-3 font-semibold">Cost</th>
                  <th className="pb-2 font-semibold">Date</th>
                </tr>
              </thead>
              <tbody>
                {records.map((r) => (
                  <tr key={r.usage_id} className="border-b last:border-0">
                    <td className="py-2 pr-3 font-mono text-xs">{r.model_id}</td>
                    <td className="py-2 pr-3 text-xs text-muted-foreground">{r.provider}</td>
                    <td className="py-2 pr-3 font-mono text-xs">{(r.input_tokens + r.output_tokens).toLocaleString()}</td>
                    <td className="py-2 pr-3 font-mono text-xs">{parseFloat(r.xendris_cost).toFixed(6)}</td>
                    <td className="py-2 text-xs text-muted-foreground whitespace-nowrap">
                      {r.timestamp ? new Date(r.timestamp).toLocaleString() : "—"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}