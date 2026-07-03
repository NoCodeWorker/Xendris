import { Badge } from "src/components/ui/badge"
import type { IntentRoute } from "src/lib/xendris/types"

type AgentStatusProps = {
  route: IntentRoute
  providerLabel: string
}

export function AgentStatus({ route, providerLabel }: AgentStatusProps) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-2 text-xs text-muted-foreground">
      <div className="flex flex-wrap items-center gap-2">
        <Badge variant="secondary">{route.intent}</Badge>
        {route.cognitiveMode ? <span>{route.cognitiveMode}</span> : <span>Ready</span>}
        <span>{(route.confidence * 100).toFixed(0)}%</span>
      </div>
      <span>{providerLabel}</span>
    </div>
  )
}
