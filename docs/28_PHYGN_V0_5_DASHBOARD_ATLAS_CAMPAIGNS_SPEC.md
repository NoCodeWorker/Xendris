# Phygn v0.5 — Dashboard Reflection: Atlas, Campaigns & Non-Triviality

## 0. Propósito

Este documento define cómo el dashboard/cockpit de Phygn debe reflejar la fase v0.5:

```txt
Invariant Boundary Atlas
CAMPAIGN-001 — Mesoscopic Boundary Number
Claim Exclusion Matrix
Non-Triviality Protocol
RAG Source Coverage
Campaign Reports
```

El objetivo no es estética.  
El objetivo es que el cockpit muestre con claridad las decisiones del core.

Phygn debe ser visible como:

```txt
core científico → cálculo → región → claim permitido/bloqueado → fuente/test/benchmark → reporte
```

## 1. Principio

```txt
El dashboard no valida Phygn.
El dashboard muestra qué ha sobrevivido al core.
```

No debe parecer una landing ni un SaaS genérico.

Debe parecer:

```txt
laboratorio de frontera
sistema de exclusión
cockpit de campañas
matriz de evidencia
panel de claims bloqueados
```

## 2. Rutas nuevas

Añadir:

```txt
/app/atlas/page.tsx
/app/atlas/points/page.tsx
/app/atlas/exclusions/page.tsx
/app/campaigns/page.tsx
/app/campaigns/mesoscopic-boundary-number/page.tsx
/app/non-triviality/page.tsx
/app/rag/page.tsx
/app/rag/sources/page.tsx
/app/rag/claims/page.tsx
```

Si `/rag` ya existe, adaptar sin duplicar.

## 3. Sidebar actualizada

Sidebar final sugerida:

```txt
Dashboard
Frontier Signature
Operational Scale
Epistemic Trace
Predictive Gain
Claim Gatekeeper
Boundary Atlas
Campaigns
Non-Triviality
RAG / Sources
Agents & Skills
Case Studies
Physicists
Docs
```

Iconos sugeridos:

```txt
Boundary Atlas      → Map
Campaigns           → FlaskConical
Non-Triviality      → ShieldQuestion
RAG / Sources       → Database
Atlas Points        → ScatterChart
Exclusions          → ShieldX
```

## 4. Nuevos componentes

Crear:

```txt
components/phygn/AtlasStatusCard.tsx
components/phygn/AtlasPointTable.tsx
components/phygn/AtlasRegionBadge.tsx
components/phygn/ClaimExclusionMatrix.tsx
components/phygn/CampaignCard.tsx
components/phygn/CampaignResultPanel.tsx
components/phygn/NonTrivialityBadge.tsx
components/phygn/NonTrivialityPanel.tsx
components/phygn/RagCoverageCard.tsx
components/phygn/RagSourceTable.tsx
components/phygn/ResearchTaskTable.tsx
components/phygn/ReportLinkCard.tsx
components/phygn/CoreTruthBanner.tsx
```

## 5. Nuevos tipos frontend

Crear o ampliar:

```txt
frontend/lib/atlas.ts
frontend/lib/campaigns.ts
frontend/lib/non-triviality.ts
frontend/lib/rag.ts
```

Tipos esperados:

```ts
export type AtlasRegion =
  | "CLASSICAL_ACCESSIBLE"
  | "QUANTUM_BOUNDARY"
  | "GRAVITATIONAL_BOUNDARY"
  | "PLANCK_CROSSING"
  | "NEGATIVE_GRAVITY_BOUND"
  | "NEGATIVE_QUANTUM_BOUND"
  | "AD_HOC_SCALE_BLOCKED"
  | "UNCLASSIFIED"

export type NonTrivialityStatus =
  | "TRIVIAL_STRUCTURAL"
  | "STRUCTURAL_USEFUL"
  | "NEGATIVE_NONTRIVIAL"
  | "PREDICTIVE_NONTRIVIAL"
  | "EMPIRICALLY_ACTIONABLE"
```

## 6. Dashboard principal

En `/dashboard`, añadir una sección:

```txt
v0.5 Research Campaign Layer
```

Cards:

```txt
Invariant Boundary Atlas
CAMPAIGN-001
Claim Exclusion Matrix
Non-Triviality Status
RAG Source Coverage
```

Cada card debe mostrar:

```txt
status
count
last generated
blocking issue
CTA
```

Ejemplo:

```txt
Invariant Boundary Atlas
Status: BUILT / PENDING / AWAITING_SOURCES
Points: 7
Regions: 6
Blocked Claims: 3
CTA: Open Atlas
```

## 7. Página `/atlas`

Título:

```txt
Invariant Boundary Atlas
```

Subtítulo:

```txt
A computable atlas of boundary regions, negative bounds and claim exclusions anchored in QB = (ℓP/L)^2.
```

Debe mostrar:

```txt
AtlasStatusCard
region summary
QB validation summary
RAG source coverage
blocked claim count
report links
```

Debe incluir fórmula:

\[
QB=\left(\frac{\ell_P}{L}\right)^2
\]

Mensaje obligatorio:

```txt
The atlas does not prove new physics. It classifies allowed, limited and blocked claims under explicit assumptions.
```

## 8. Página `/atlas/points`

Debe mostrar tabla de puntos:

```txt
system_id
label
m_kg
L_value_m
L_type
Q
B
QB
logQ
logB
u
w
region
trace_type
claim_status
scale_status
```

Funciones UX:

```txt
filter by region
filter by claim_status
filter by scale_status
sort by B
sort by Q
```

No es necesario gráfico avanzado en esta fase.

## 9. Página `/atlas/exclusions`

Debe mostrar la matriz de exclusión:

```txt
claim_id
claim_text
decision
reason
region
source_status
test_status
safe_rewrite
```

Debe destacar claims bloqueados:

```txt
Phygn predicts new gravitational decoherence.
This proves quantum gravity.
The invariant proves new physics.
```

## 10. Página `/campaigns`

Hub de campañas:

```txt
CAMPAIGN-001 — Mesoscopic Boundary Number
```

Cada `CampaignCard` muestra:

```txt
campaign_id
title
status
non_triviality_status
region
reports
tests
RAG tasks
CTA
```

Estados:

```txt
PLANNED
RUNNING
COMPLETED_WITH_NEGATIVE_BOUND
BLOCKED_BY_SOURCE
BLOCKED_BY_MODEL
READY_FOR_NEXT_CAMPAIGN
```

## 11. Página `/campaigns/mesoscopic-boundary-number`

Debe mostrar:

```txt
Scientific Question
Input System
Operational Scale Review
Boundary Signature
Invariant Check
Region Classification
Non-Triviality Status
Allowed Claims
Blocked Claims
RAG Status
Benchmark Status
Tests
Next Tasks
```

Valores esperados:

```txt
m = 1e-17 kg
L = 1e-7 m
L_type = L_INT
region = NEGATIVE_GRAVITY_BOUND
blocked claim = Phygn predicts new gravitational decoherence
```

Debe mostrar los cálculos:

```txt
λC
rg
RS
Q
B
QB
(ℓP/L)^2
delta_QB
logQ
logB
u
w
```

## 12. Página `/non-triviality`

Debe explicar los estados:

```txt
TRIVIAL_STRUCTURAL
STRUCTURAL_USEFUL
NEGATIVE_NONTRIVIAL
PREDICTIVE_NONTRIVIAL
EMPIRICALLY_ACTIONABLE
```

Debe mostrar para CAMPAIGN-001:

```txt
current status
why
what would upgrade it
what would falsify/defeat it
what is still missing
```

Frase obligatoria:

```txt
Lo no trivial no es lo que suena profundo. Lo no trivial es lo que cambia una decisión.
```

## 13. Página `/rag`

Debe mostrar cobertura RAG:

```txt
sources count
claims count
claim-source links
research tasks
claims requiring source
claims blocked by contradiction
low-trust hard claims
```

## 14. Página `/rag/sources`

Tabla:

```txt
source_id
title
authors
year
source_type
trust_level
relevance
topics
used_for
```

## 15. Página `/rag/claims`

Tabla:

```txt
claim_id
text
status
layer
trace_type
source_ids
test_ids
benchmark_ids
safe_rewrite
```

## 16. Lectura de datos

Prioridad:

```txt
1. API endpoints si existen
2. reportes JSON generados
3. Markdown reports resumidos
4. static fallback claramente etiquetado como placeholder
```

No fingir datos.

Si falta endpoint:

```txt
status: Awaiting backend endpoint
```

Si falta reporte:

```txt
status: Awaiting generated report
```

## 17. API client sugerido

Extender `frontend/lib/api.ts`:

```ts
getAtlas()
getAtlasPoints()
getAtlasExclusions()
getCampaigns()
getMesoscopicBoundaryCampaign()
getNonTrivialityStatus()
getRagSources()
getRagClaims()
getRagResearchTasks()
```

Si endpoints no existen, usar fallback.

## 18. Estados visuales

### AtlasRegionBadge

```txt
NEGATIVE_GRAVITY_BOUND → amber
QUANTUM_BOUNDARY → blue/cyan
GRAVITATIONAL_BOUNDARY → violet/red
PLANCK_CROSSING → spectrum/accent
CLASSICAL_ACCESSIBLE → muted/green
AD_HOC_SCALE_BLOCKED → destructive
```

### NonTrivialityBadge

```txt
TRIVIAL_STRUCTURAL → muted
STRUCTURAL_USEFUL → blue/taupe
NEGATIVE_NONTRIVIAL → amber
PREDICTIVE_NONTRIVIAL → green
EMPIRICALLY_ACTIONABLE → emerald/highlight
```

### ClaimExclusion

```txt
BLOCKED → red
REQUIRES_SOURCE → amber
REQUIRES_MODEL → orange
ALLOWED_LIMITED → blue
ALLOWED → green
```

## 19. Prohibiciones

No escribir:

```txt
Phygn proves new physics.
The atlas validates Frontera C.
CAMPAIGN-001 predicts decoherence.
The invariant is a discovered law.
```

Sí escribir:

```txt
Phygn computes a negative bound.
The atlas classifies claim status under explicit assumptions.
CAMPAIGN-001 blocks the decoherence overclaim unless model comparison exists.
```

## 20. Criterio de aceptación

```txt
/sidebar includes Boundary Atlas, Campaigns, Non-Triviality, RAG/Sources
/atlas loads
/atlas/points loads
/atlas/exclusions loads
/campaigns loads
/campaigns/mesoscopic-boundary-number loads
/non-triviality loads
/rag loads
dashboard contains v0.5 research cards
blocked decoherence overclaim visible
no new-physics proof language appears
fallback states are honest
```
