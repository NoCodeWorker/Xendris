import type { Metadata } from "next"
import { DashboardShell } from "src/components/dashboard/dashboard-shell"

export const metadata: Metadata = {
  title: "Xendris AI — Dashboard",
  description: "Trust Dashboard: wallet, usage, cost, and trust metrics.",
}

export default function DashboardPage() {
  return <DashboardShell />
}