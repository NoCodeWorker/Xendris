"use client"

import type { IntentRoute, XendrisMessage, XendrisProviderName } from "src/lib/xendris/types"

type DevRuntimeStatusProps = {
  selectedProvider: XendrisProviderName
  streamingEnabled: boolean
  lastMetadata?: XendrisMessage["metadata"]
  route: IntentRoute
}

function RuntimeRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex min-w-0 items-center justify-between gap-3">
      <span className="text-muted-foreground">{label}</span>
      <span className="truncate font-medium text-foreground">{value}</span>
    </div>
  )
}

export function DevRuntimeStatus({
  selectedProvider,
  streamingEnabled,
  lastMetadata,
  route,
}: DevRuntimeStatusProps) {
  return (
    <section className="rounded-2xl border bg-muted/25 p-3 text-xs">
      <div className="mb-2 flex items-center justify-between gap-3">
        <p className="font-medium text-foreground">Dev runtime</p>
        <span className="rounded-full border bg-background px-2 py-0.5 text-muted-foreground">
          local only
        </span>
      </div>
      <div className="grid gap-1.5 sm:grid-cols-2">
        <RuntimeRow label="Selected provider" value={selectedProvider} />
        <RuntimeRow label="Streaming" value={streamingEnabled ? "enabled" : "disabled"} />
        <RuntimeRow
          label="Endpoint"
          value={streamingEnabled ? "/api/chat/stream" : "/api/chat"}
        />
        <RuntimeRow label="Last provider" value={lastMetadata?.provider ?? "none"} />
        <RuntimeRow label="Last model" value={lastMetadata?.model ?? "none"} />
        <RuntimeRow
          label="Last intent"
          value={lastMetadata?.detectedIntent ?? route.intent ?? "none"}
        />
        <RuntimeRow
          label="Quality"
          value={
            lastMetadata?.evaluation
              ? lastMetadata.evaluation.qualityScore.toFixed(2)
              : "none"
          }
        />
        <RuntimeRow
          label="Confidence"
          value={
            lastMetadata?.evaluation
              ? lastMetadata.evaluation.confidenceScore.toFixed(2)
              : "none"
          }
        />
        <RuntimeRow
          label="Risk"
          value={lastMetadata?.evaluation?.riskLevel ?? "none"}
        />
        <RuntimeRow
          label="Controller"
          value={lastMetadata?.controllerDecision?.action ?? "none"}
        />
        <RuntimeRow
          label="Severity"
          value={lastMetadata?.controllerDecision?.severity ?? "none"}
        />
        <RuntimeRow
          label="Repaired"
          value={
            lastMetadata?.repair ? (lastMetadata.repair.repaired ? "yes" : "no") : "none"
          }
        />
        <RuntimeRow
          label="Repair strategy"
          value={lastMetadata?.repair?.repairStrategy ?? "none"}
        />
        <RuntimeRow
          label="Execution id"
          value={lastMetadata?.executionSummary?.id ?? "none"}
        />
        <RuntimeRow
          label="Provider latency"
          value={
            lastMetadata?.executionSummary?.timings?.providerMs !== undefined
              ? `${lastMetadata.executionSummary.timings.providerMs} ms`
              : "none"
          }
        />
        <RuntimeRow
          label="Total latency"
          value={
            lastMetadata?.executionSummary?.timings?.totalMs !== undefined
              ? `${lastMetadata.executionSummary.timings.totalMs} ms`
              : lastMetadata?.executionSummary
                ? `${lastMetadata.executionSummary.latencyMs} ms`
                : "none"
          }
        />
        <RuntimeRow
          label="Summary endpoint"
          value={lastMetadata?.executionSummary?.endpoint ?? "none"}
        />
        <RuntimeRow
          label="Cache hit"
          value={lastMetadata?.cache ? (lastMetadata.cache.hit ? "yes" : "no") : "none"}
        />
        <RuntimeRow
          label="Cache key"
          value={lastMetadata?.cache ? `${lastMetadata.cache.key.slice(0, 10)}...` : "none"}
        />
        <RuntimeRow
          label="Epistemic risk"
          value={lastMetadata?.epistemicEvaluation?.riskLevel ?? "none"}
        />
        <RuntimeRow
          label="Overconfidence"
          value={
            lastMetadata?.epistemicEvaluation
              ? lastMetadata.epistemicEvaluation.overconfidenceScore.toFixed(2)
              : "none"
          }
        />
        <RuntimeRow
          label="Unsupported certainty"
          value={
            lastMetadata?.epistemicEvaluation
              ? (lastMetadata.epistemicEvaluation.unsupportedCertainty ? "yes" : "no")
              : "none"
          }
        />
        <RuntimeRow
          label="False premise risk"
          value={
            lastMetadata?.epistemicEvaluation
              ? (lastMetadata.epistemicEvaluation.falsePremiseRisk ? "yes" : "no")
              : "none"
          }
        />
        <RuntimeRow
          label="Detected language"
          value={lastMetadata?.detectedLanguage ?? "none"}
        />
      </div>
    </section>
  )
}
