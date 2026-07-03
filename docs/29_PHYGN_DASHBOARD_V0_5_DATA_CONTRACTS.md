# Phygn v0.5 — Dashboard Data Contracts

## 0. Propósito

Este documento define los contratos de datos que el dashboard debe esperar para reflejar el core v0.5.

El dashboard debe ser robusto aunque el backend no exponga todavía todos los endpoints.

## 1. Principio

```txt
Frontend shows state.
Frontend does not invent state.
```

Si faltan datos:

```txt
AWAITING_BACKEND_ENDPOINT
AWAITING_GENERATED_REPORT
AWAITING_RAG_SOURCE
```

## 2. AtlasSummary

```ts
export type AtlasSummary = {
  atlas_id: string
  version: string
  status: "BUILT" | "PENDING" | "AWAITING_SOURCES" | "ERROR"
  point_count: number
  region_counts: Record<string, number>
  blocked_claim_count: number
  allowed_claim_count: number
  requires_source_count: number
  qb_valid_count: number
  qb_invalid_count: number
  generated_at?: string
  report_path?: string
}
```

## 3. AtlasPoint

```ts
export type AtlasPoint = {
  system_id: string
  label: string
  m_kg: number
  L_value_m: number
  L_type: string
  lambda_c_m: number
  r_g_m: number
  schwarzschild_radius_m: number
  Q: number
  B: number
  QB: number
  planck_ratio_squared: number
  delta_QB: number
  logQ: number
  logB: number
  u: number
  w: number
  scale_status: string
  region: string
  trace_type: string
  claim_status: string
  source_ids: string[]
  test_ids: string[]
}
```

## 4. ClaimExclusionRow

```ts
export type ClaimExclusionRow = {
  claim_id: string
  claim_text: string
  decision:
    | "ALLOWED"
    | "ALLOWED_LIMITED"
    | "REQUIRES_SOURCE"
    | "REQUIRES_MODEL"
    | "REQUIRES_TRACE"
    | "REQUIRES_TEST"
    | "BLOCKED"

  reason: string
  safe_rewrite?: string
  region?: string
  source_status?: string
  test_status?: string
  benchmark_status?: string
}
```

## 5. CampaignSummary

```ts
export type CampaignSummary = {
  campaign_id: string
  title: string
  status:
    | "PLANNED"
    | "RUNNING"
    | "COMPLETED_WITH_NEGATIVE_BOUND"
    | "BLOCKED_BY_SOURCE"
    | "BLOCKED_BY_MODEL"
    | "READY_FOR_NEXT_CAMPAIGN"

  non_triviality_status:
    | "TRIVIAL_STRUCTURAL"
    | "STRUCTURAL_USEFUL"
    | "NEGATIVE_NONTRIVIAL"
    | "PREDICTIVE_NONTRIVIAL"
    | "EMPIRICALLY_ACTIONABLE"

  region?: string
  report_path?: string
  test_count?: number
  rag_task_count?: number
  blocked_claim_count?: number
}
```

## 6. MesoscopicCampaignResult

```ts
export type MesoscopicCampaignResult = {
  campaign_id: "CAMPAIGN-001"
  system_id: string
  input: {
    m_kg: number
    L_value_m: number
    L_type: string
    physical_role: string
    observer_channel: string
    justification: string
    arbitrariness_risk: string
  }
  signature: AtlasPoint
  invariant_check: {
    qb_valid: boolean
    delta_QB: number
  }
  region: string
  non_triviality_status: string
  allowed_claims: string[]
  blocked_claims: string[]
  required_sources: string[]
  required_models: string[]
  required_tests: string[]
  benchmark_status: string
  rag_status: string
  next_tasks: string[]
}
```

## 7. RagCoverageSummary

```ts
export type RagCoverageSummary = {
  source_count: number
  claim_count: number
  claim_source_link_count: number
  research_task_count: number
  requires_source_count: number
  requires_higher_trust_count: number
  contradicted_claim_count: number
  blocked_claim_count: number
}
```

## 8. RagSource

```ts
export type RagSource = {
  source_id: string
  title: string
  authors: string[]
  year?: string | null
  url?: string | null
  local_path?: string | null
  source_type: string
  trust_level: "PRIMARY" | "HIGH" | "MEDIUM" | "LOW"
  relevance: "HIGH" | "MEDIUM" | "LOW"
  topics: string[]
  used_for: string[]
  notes?: string | null
}
```

## 9. RagClaim

```ts
export type RagClaim = {
  claim_id: string
  text: string
  claim_type: string
  layer: string
  trace_type?: string | null
  status: string
  source_ids: string[]
  test_ids: string[]
  benchmark_ids: string[]
  safe_rewrite?: string | null
  forbidden_interpretations: string[]
}
```

## 10. ResearchTask

```ts
export type ResearchTask = {
  task_id: string
  question: string
  reason: string
  linked_claim_id?: string | null
  priority: "P0" | "P1" | "P2" | "P3"
  required_source_types: string[]
  suggested_queries: string[]
  status:
    | "TODO"
    | "IN_PROGRESS"
    | "AWAITING_SOURCE_INGESTION"
    | "SOURCE_INGESTED"
    | "DONE"
    | "BLOCKED"
}
```

## 11. Fallback strategy

Every page should have this logic:

```ts
try API
if API missing:
  try static generated JSON/report
if report missing:
  show honest empty state
```

Honest empty states:

```txt
Atlas not generated yet.
Campaign report not generated yet.
Backend endpoint pending.
RAG source registry empty.
No claim-source links available.
```

## 12. Mock data rule

Mock data is allowed only if clearly marked:

```txt
DEVELOPMENT_PLACEHOLDER
```

Mock data must not be mixed with real campaign status.

## 13. Reports mapping

```txt
reports/atlas/invariant_boundary_atlas.md → /atlas
reports/atlas/atlas_points.json → /atlas/points
reports/atlas/claim_exclusion_matrix.md → /atlas/exclusions
reports/campaigns/CAMPAIGN-001_mesoscopic_boundary_number.md → /campaigns/mesoscopic-boundary-number
reports/campaigns/CAMPAIGN-001_citation_audit.md → /rag or /campaigns/mesoscopic-boundary-number
reports/rag_status.md → /rag
reports/claim_source_matrix.md → /rag/claims
```

## 14. Final rule

```txt
If the core has not produced it, the dashboard must say so.
```
