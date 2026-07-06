"use client"
/* eslint-disable react-hooks/set-state-in-effect */

import * as React from "react"

type Transaction = {
  transaction_id: string
  type: string
  amount: string
  description: string
  timestamp: string
}

type WalletData = {
  balance: string
  currency: string
  hard_cap: string
  daily_limit: string
  monthly_limit: string
  transactions: Transaction[]
}

export function WalletView({ tenantId }: { tenantId: string }) {
  const [data, setData] = React.useState<WalletData | null>(null)
  const [loading, setLoading] = React.useState(true)
  const [error, setError] = React.useState<string | null>(null)

  React.useEffect(() => {
    setLoading(true)
    setError(null)
    Promise.all([
      fetch(`/api/xendris/wallet?tenant_id=${encodeURIComponent(tenantId)}`).then((r) => r.json()),
      fetch(`/api/xendris/wallet?tenant_id=${encodeURIComponent(tenantId)}&path=history&limit=50`).then((r) => r.json()),
    ])
      .then(([balance, history]) => {
        setData({
          balance: balance.balance || "0.00",
          currency: balance.currency || "USD",
          hard_cap: balance.hard_cap || "1000.00",
          daily_limit: balance.daily_limit || "100.00",
          monthly_limit: balance.monthly_limit || "500.00",
          transactions: Array.isArray(history.transactions) ? history.transactions : [],
        })
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [tenantId])

  if (loading) {
    return (
      <div className="space-y-4">
        <div className="h-32 animate-pulse rounded-2xl border bg-muted/30" />
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

  if (!data) return null

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold tracking-tight">Wallet & Billing</h2>
        <p className="text-sm text-muted-foreground">Saldo, límites y transacciones para <span className="font-mono font-semibold">{tenantId}</span></p>
      </div>

      <div className="grid gap-4 sm:grid-cols-4">
        <div className="rounded-2xl border bg-card p-5 shadow-xs col-span-1">
          <p className="text-sm font-medium text-muted-foreground">Balance</p>
          <p className="mt-2 text-3xl font-bold tracking-tight text-foreground">
            {parseFloat(data.balance).toFixed(2)}
          </p>
          <p className="text-xs text-muted-foreground">{data.currency}</p>
        </div>
        <div className="rounded-2xl border bg-card p-5 shadow-xs">
          <p className="text-sm font-medium text-muted-foreground">Daily Limit</p>
          <p className="mt-2 text-xl font-semibold text-foreground">{data.daily_limit}</p>
          <p className="text-xs text-muted-foreground">{data.currency}</p>
        </div>
        <div className="rounded-2xl border bg-card p-5 shadow-xs">
          <p className="text-sm font-medium text-muted-foreground">Monthly Limit</p>
          <p className="mt-2 text-xl font-semibold text-foreground">{data.monthly_limit}</p>
          <p className="text-xs text-muted-foreground">{data.currency}</p>
        </div>
        <div className="rounded-2xl border bg-card p-5 shadow-xs">
          <p className="text-sm font-medium text-muted-foreground">Hard Cap</p>
          <p className="mt-2 text-xl font-semibold text-foreground">{data.hard_cap}</p>
          <p className="text-xs text-muted-foreground">{data.currency}</p>
        </div>
      </div>

      <div className="rounded-2xl border bg-card p-5 shadow-xs">
        <h3 className="mb-4 text-sm font-semibold text-foreground">Transaction History</h3>
        {data.transactions.length === 0 ? (
          <p className="text-sm text-muted-foreground py-8 text-center">No transactions yet.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="border-b text-xs text-muted-foreground">
                  <th className="pb-2 pr-4 font-semibold">ID</th>
                  <th className="pb-2 pr-4 font-semibold">Type</th>
                  <th className="pb-2 pr-4 font-semibold">Amount</th>
                  <th className="pb-2 pr-4 font-semibold">Description</th>
                  <th className="pb-2 font-semibold">Date</th>
                </tr>
              </thead>
              <tbody>
                {data.transactions.map((tx) => (
                  <tr key={tx.transaction_id} className="border-b last:border-0">
                    <td className="py-2.5 pr-4 font-mono text-xs text-muted-foreground">{tx.transaction_id.slice(0, 16)}...</td>
                    <td className="py-2.5 pr-4">
                      <span className={`inline-flex rounded-full px-2 py-0.5 text-[11px] font-semibold ${
                        tx.type === "CREDIT" || tx.type === "TOPUP"
                          ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300"
                          : "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300"
                      }`}>
                        {tx.type}
                      </span>
                    </td>
                    <td className="py-2.5 pr-4 font-mono font-medium">{tx.amount}</td>
                    <td className="py-2.5 pr-4 text-muted-foreground">{tx.description || "—"}</td>
                    <td className="py-2.5 text-xs text-muted-foreground whitespace-nowrap">
                      {new Date(tx.timestamp).toLocaleDateString()}
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