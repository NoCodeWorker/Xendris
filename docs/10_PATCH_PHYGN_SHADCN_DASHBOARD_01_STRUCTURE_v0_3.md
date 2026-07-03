# PATCH — Phygn dashboard structure with shadcn dashboard-01

## Corrección de estructura

El dashboard/lab visual de Phygn debe basarse en el bloque oficial de shadcn:

```bash
npx shadcn@latest add dashboard-01
```

Esto debe usarse como estructura base del cockpit.

## Prioridad de inicialización

La secuencia correcta para el frontend es:

```bash
npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir false
cd frontend
npx shadcn@latest init --preset b4gMUX5Dk --template next
npx shadcn@latest add dashboard-01
```

Después instalar dependencias científicas adicionales si no están ya presentes:

```bash
npm install @tanstack/react-query recharts lucide-react katex react-katex zod react-hook-form @hookform/resolvers next-themes
```

## Regla de prioridad

```txt
1. Mantener backend Phygn y tests existentes.
2. Inicializar frontend con preset b4gMUX5Dk.
3. Añadir dashboard-01 como layout/base estructural.
4. Adaptar dashboard-01 a Phygn.
5. Añadir componentes científicos Phygn.
6. Conectar con FastAPI.
```

## Qué conservar de dashboard-01

Codex debe conservar y adaptar:

```txt
sidebar
app shell
header/topbar
cards
layout responsive
navigation structure
main content area
```

## Qué reemplazar

Reemplazar contenido genérico de dashboard-01 por contenido Phygn:

```txt
Dashboard genérico → Phygn Scientific Cockpit
Analytics genéricos → Boundary Signatures
Sales/revenue cards → Q/B metrics, traces, claims, negative bounds
Users/customers → case studies, claims evaluated, traces detected
Generic tables → claims table, physicists cards, benchmark results
```

## Rutas Phygn obligatorias

El dashboard debe exponer:

```txt
/
dashboard
signature
scale
trace
gain
claims
case-studies
case-studies/mesoscopic
case-studies/quantum-channel
physicists
docs
```

## Navegación adaptada

Sidebar basada en dashboard-01, pero con navegación:

```txt
Dashboard
Frontier Signature
Operational Scale
Epistemic Trace
Predictive Gain
Claim Gatekeeper
Case Studies
Physicists
Docs
```

Iconos sugeridos:

```txt
Dashboard → Gauge
Frontier Signature → Fingerprint
Operational Scale → Ruler
Epistemic Trace → Activity
Predictive Gain → TrendingUp
Claim Gatekeeper → ShieldCheck
Case Studies → FlaskConical
Physicists → Atom
Docs → BookOpen
```

## Pantalla Dashboard

Debe usar la estética y layout de dashboard-01, pero con cards Phygn:

```txt
Boundary Signatures
Epistemic Traces
Negative Bounds
Claim Gatekeeper
```

Cada card debe mostrar estado real o placeholder conectado a API.

## Componentes Phygn encima de dashboard-01

Crear o adaptar:

```txt
components/phygn/PhygnLogo.tsx
components/phygn/MetricCard.tsx
components/phygn/FormulaBlock.tsx
components/phygn/TraceBadge.tsx
components/phygn/ClaimDecisionBadge.tsx
components/phygn/ScaleReviewCard.tsx
components/phygn/BoundarySignaturePanel.tsx
components/phygn/EpistemicTracePanel.tsx
components/phygn/PredictiveGainPanel.tsx
components/phygn/ClaimGatekeeperPanel.tsx
components/phygn/PhysicistCard.tsx
components/phygn/CaseStudyCard.tsx
components/phygn/JsonOutput.tsx
```

## No hacer

```txt
No dejar contenido de ejemplo de dashboard-01 sin adaptar.
No mostrar revenue, sales o customers si no tienen sentido.
No romper el preset b4gMUX5Dk.
No eliminar estructura responsive de dashboard-01.
No hacer una landing en vez de un cockpit.
```

## Criterio de aceptación

El dashboard se considera correcto si:

```txt
usa dashboard-01 como base
mantiene preset b4gMUX5Dk
muestra sidebar Phygn
tiene rutas del Lab
llama a la API FastAPI
muestra estados de claim/traza
incluye physicists cards
incluye case studies
no conserva datos genéricos irrelevantes
```
