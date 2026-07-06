"use client"

import { ShieldCheck, ShieldAlert, ShieldX } from "lucide-react"
import type { XendrisGuardResult } from "src/lib/xendris/types"

type TrustPanelProps = {
  verdict: string
  guardResults: XendrisGuardResult[]
  requiresCouncil: boolean
}

const RESULT_ICON: Record<string, typeof ShieldCheck> = {
  PASS: ShieldCheck,
  FLAG: ShieldAlert,
  BLOCK: ShieldX,
}

const RESULT_COLOR: Record<string, string> = {
  PASS: "text-emerald-600 dark:text-emerald-400",
  FLAG: "text-amber-600 dark:text-amber-400",
  BLOCK: "text-red-600 dark:text-red-400",
}

const RESULT_BG: Record<string, string> = {
  PASS: "bg-emerald-50 dark:bg-emerald-950/30 border-emerald-200 dark:border-emerald-800/40",
  FLAG: "bg-amber-50 dark:bg-amber-950/30 border-amber-200 dark:border-amber-800/40",
  BLOCK: "bg-red-50 dark:bg-red-950/30 border-red-200 dark:border-red-800/40",
}

export function TrustPanel({ verdict, guardResults, requiresCouncil }: TrustPanelProps) {
  if (!verdict && guardResults.length === 0) return null

  return (
    <div className="mt-3 rounded-2xl border bg-card/50 p-4 shadow-xs">
      <div className="mb-3 flex items-center justify-between">
        <p className="text-xs font-semibold tracking-wide text-muted-foreground uppercase">
          Trust Council
        </p>
        <span
          className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-[11px] font-semibold tracking-wide uppercase ${
            verdict === "ESCALATED_TO_COUNCIL"
              ? "bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300"
              : verdict === "SINGLE_MODEL_OK"
                ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300"
                : "bg-muted text-muted-foreground"
          }`}
        >
          {verdict || "N/A"}
        </span>
      </div>

      {guardResults.length > 0 && (
        <div className="space-y-1.5">
          {guardResults.map((g, i) => {
            const Icon = RESULT_ICON[g.result] || ShieldCheck
            const color = RESULT_COLOR[g.result] || "text-muted-foreground"
            const bg = RESULT_BG[g.result] || "bg-muted/30 border-border"
            return (
              <div
                key={i}
                className={`flex items-start gap-2.5 rounded-xl border px-3 py-2.5 ${bg}`}
              >
                <Icon className={`mt-0.5 size-4 shrink-0 ${color}`} />
                <div className="min-w-0">
                  <p className="text-xs font-semibold text-foreground">{g.guard}</p>
                  {g.reason && (
                    <p className="mt-0.5 text-[11px] leading-snug text-muted-foreground">
                      {g.reason}
                    </p>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      )}

      {requiresCouncil && (
        <p className="mt-3 text-[11px] font-medium text-amber-600 dark:text-amber-400">
          Multiple models recommended for this response
        </p>
      )}
    </div>
  )
}