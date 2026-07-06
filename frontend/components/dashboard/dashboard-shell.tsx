"use client"

import * as React from "react"
import Link from "next/link"
import { Wallet, BarChart3, BookOpen, Home, ArrowLeft, Key, Activity } from "lucide-react"
import { ThemeToggle } from "src/components/theme-toggle"
import { cn } from "src/lib/utils"
import { DashboardOverview } from "src/components/dashboard/dashboard-overview"
import { WalletView } from "src/components/dashboard/wallet-view"
import { UsageAnalyticsView } from "src/components/dashboard/usage-analytics"
import { TrustDecisionsView } from "src/components/dashboard/trust-decisions-view"
import { LedgerViewer } from "src/components/dashboard/ledger-viewer"

type DashboardTab = "overview" | "wallet" | "usage" | "trust" | "ledger"

const NAV_ITEMS: { id: DashboardTab; label: string; icon: typeof Home }[] = [
  { id: "overview", label: "Overview", icon: Home },
  { id: "wallet", label: "Wallet", icon: Wallet },
  { id: "usage", label: "Usage", icon: BarChart3 },
  { id: "trust", label: "Trust", icon: Activity },
  { id: "ledger", label: "Ledger", icon: BookOpen },
]

export function DashboardShell() {
  const [activeTab, setActiveTab] = React.useState<DashboardTab>("overview")
  const [tenantId, setTenantId] = React.useState("demo-tenant")
  const [editingTenant, setEditingTenant] = React.useState(false)
  const [tenantInput, setTenantInput] = React.useState("demo-tenant")

  function handleTenantSubmit() {
    setTenantId(tenantInput.trim() || "demo-tenant")
    setEditingTenant(false)
  }

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-background text-foreground">
      <aside className="hidden w-64 shrink-0 border-r bg-card lg:flex lg:flex-col">
        <div className="flex h-14 items-center gap-2.5 border-b px-5">
          <Link href="/x" className="flex items-center gap-2 text-sm font-semibold text-muted-foreground hover:text-foreground transition-colors">
            <ArrowLeft className="size-4" />
            Back to chat
          </Link>
        </div>

        <div className="border-b px-4 py-3">
          {editingTenant ? (
            <form
              onSubmit={(e) => { e.preventDefault(); handleTenantSubmit(); }}
              className="flex gap-2"
            >
              <input
                value={tenantInput}
                onChange={(e) => setTenantInput(e.target.value)}
                className="h-8 flex-1 rounded-lg border bg-background px-2.5 text-xs outline-none focus:border-ring"
                placeholder="Tenant ID"
              />
              <button type="submit" className="h-8 rounded-lg bg-primary px-2.5 text-[11px] font-semibold text-primary-foreground">
                Set
              </button>
            </form>
          ) : (
            <button
              type="button"
              onClick={() => { setTenantInput(tenantId); setEditingTenant(true); }}
              className="flex w-full items-center gap-2 rounded-lg border bg-muted/30 px-3 py-2 text-left transition-colors hover:bg-muted/50"
            >
              <Key className="size-3.5 text-muted-foreground shrink-0" />
              <div className="min-w-0">
                <p className="text-[11px] font-semibold text-foreground">{tenantId}</p>
                <p className="text-[10px] text-muted-foreground">Tenant ID</p>
              </div>
            </button>
          )}
        </div>

        <nav className="flex-1 space-y-1 px-3 py-4">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon
            return (
              <button
                key={item.id}
                type="button"
                onClick={() => setActiveTab(item.id)}
                className={cn(
                  "flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left text-sm transition-all",
                  activeTab === item.id
                    ? "bg-primary/10 text-foreground font-semibold"
                    : "text-muted-foreground hover:bg-muted/40 hover:text-foreground",
                )}
              >
                <Icon className="size-4 shrink-0" />
                {item.label}
              </button>
            )
          })}
        </nav>

        <div className="border-t px-4 py-3">
          <ThemeToggle className="w-full justify-start" />
        </div>
      </aside>

      <main className="flex min-w-0 flex-1 flex-col overflow-hidden">
        <header className="flex h-14 shrink-0 items-center border-b bg-background/55 backdrop-blur-md px-6">
          <div className="flex items-center gap-2.5">
            <span className="inline-block size-2 rounded-full bg-emerald-500" />
            <h1 className="text-sm font-semibold tracking-tight">
              {NAV_ITEMS.find((n) => n.id === activeTab)?.label || "Dashboard"}
            </h1>
          </div>
        </header>

        <div className="flex-1 overflow-y-auto p-6">
          {activeTab === "overview" && <DashboardOverview tenantId={tenantId} />}
          {activeTab === "wallet" && <WalletView tenantId={tenantId} />}
          {activeTab === "usage" && <UsageAnalyticsView tenantId={tenantId} />}
          {activeTab === "trust" && <TrustDecisionsView tenantId={tenantId} />}
          {activeTab === "ledger" && <LedgerViewer />}
        </div>
      </main>
    </div>
  )
}