# PATCH para Codex — usar shadcn dashboard-01 como estructura del Lab

Estás trabajando en:

```txt
d:\BIOCULTOR\PHYNG\
```

El frontend de Phygn debe construirse usando:

```bash
npx shadcn@latest add dashboard-01
```

como estructura base del dashboard/lab.

## Secuencia obligatoria

Desde la raíz del proyecto:

```bash
npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir false
cd frontend
npx shadcn@latest init --preset b4gMUX5Dk --template next
npx shadcn@latest add dashboard-01
npm install @tanstack/react-query recharts lucide-react katex react-katex zod react-hook-form @hookform/resolvers next-themes
```

Si el frontend ya existe, no lo recrees sin preguntar. Inspecciona primero:

```bash
cd frontend
dir
```

y adapta lo existente.

## Objetivo

Convertir `dashboard-01` en el cockpit científico de Phygn.

No construir una landing.

## Adaptación de dashboard-01

### Sidebar

Reemplazar navegación por:

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

### Cards principales

Reemplazar cards genéricas por:

```txt
Boundary Signatures
Epistemic Traces
Negative Bounds
Claim Gatekeeper
```

### Tablas/listas

Reemplazar tablas genéricas por:

```txt
recent claim evaluations
case studies
benchmark statuses
physicists conceptual map
```

### Gráficas

Sustituir gráficas genéricas por:

```txt
Q/B log chart
distribution bar chart
Predictive Gain gauge
```

## Rutas obligatorias

Crear/adaptar:

```txt
app/page.tsx
app/dashboard/page.tsx
app/signature/page.tsx
app/scale/page.tsx
app/trace/page.tsx
app/gain/page.tsx
app/claims/page.tsx
app/case-studies/page.tsx
app/case-studies/mesoscopic/page.tsx
app/case-studies/quantum-channel/page.tsx
app/physicists/page.tsx
app/docs/page.tsx
```

## API

Crear `lib/api.ts` con:

```ts
const API_BASE_URL =
  process.env.NEXT_PUBLIC_PHYGN_API_URL ?? "http://127.0.0.1:8000";
```

Funciones:

```txt
getHealth
validateInvariant
calculateSignature
calculateDepolarizingTrace
calculateGain
evaluateClaim
getMesoscopicCase
```

## Regla de backend

No rompas el backend. Antes de trabajar frontend:

```bash
pytest -v
```

Si falla, reporta y corrige solo lo necesario.

## Resultado esperado

Al terminar:

```bash
cd frontend
npm run dev
```

Debe cargar un dashboard basado en dashboard-01, pero convertido en:

```txt
Phygn — Physical Signatures Lab
```

con:

```txt
sidebar científica
cards científicas
formularios conectados a API
físicos conceptuales
casos de estudio
Claim Gatekeeper
estética del preset b4gMUX5Dk
```

## Prohibiciones

```txt
No conservar textos genéricos de dashboard-01.
No mostrar métricas tipo revenue/sales/customers salvo que estén reinterpretadas científicamente.
No usar el lema como prueba de nueva física.
No permitir claims sin traza.
No mezclar cognitive extension como validación física.
```

## Criterio final

Phygn debe sentirse como:

```txt
un laboratorio científico operativo
```

no como:

```txt
un dashboard SaaS genérico
```
