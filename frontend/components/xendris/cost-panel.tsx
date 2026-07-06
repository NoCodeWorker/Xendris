"use client"

import { DollarSign, CreditCard } from "lucide-react"

type CostPanelProps = {
  charge: string
  usageId: string
  provider: string
  model: string
}

export function CostPanel({ charge, usageId, provider, model }: CostPanelProps) {
  if (!charge && !usageId) return null

  return (
    <div className="mt-2 flex flex-wrap items-center gap-3">
      {charge && (
        <span className="inline-flex items-center gap-1 rounded-lg border bg-muted/30 px-2 py-1 text-[11px] font-medium text-muted-foreground">
          <DollarSign className="size-3" />
          {charge} USD
        </span>
      )}
      {usageId && (
        <span className="inline-flex items-center gap-1 rounded-lg border bg-muted/30 px-2 py-1 text-[11px] font-mono text-muted-foreground">
          <CreditCard className="size-3" />
          {usageId.slice(0, 18)}...
        </span>
      )}
      <span className="inline-flex items-center gap-1 rounded-lg border bg-muted/30 px-2 py-1 text-[11px] text-muted-foreground">
        {provider} / {model}
      </span>
    </div>
  )
}