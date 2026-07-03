# Phygn v0.3 — Full Frontend Dashboard Specification

## Objetivo

Construir el frontend completo de Phygn como un **scientific cockpit** para Frontera C.

No debe ser una landing decorativa.  
Debe ser un laboratorio visual donde el usuario pueda:

```txt
calcular firmas Q/B
revisar escala operacional L
visualizar huellas epistemológicas
ejecutar casos de estudio
evaluar claims
ver cotas negativas
leer tarjetas conceptuales de grandes físicos
exportar resultados
```

## Nombre público

```txt
Phygn — Physical Signatures Lab
```

## Tagline

```txt
Physical signatures. Epistemic traces. Boundary claims.
```

## Stack obligatorio

```txt
Next.js App Router
TypeScript
Tailwind CSS
shadcn/ui
lucide-react
TanStack Query
Recharts
KaTeX / react-katex
Zod
React Hook Form
```

Opcional:

```txt
Framer Motion
Zustand
next-themes
```

## Estructura frontend recomendada

```txt
frontend/
  package.json
  next.config.ts
  tsconfig.json
  postcss.config.mjs
  tailwind.config.ts
  app/
    layout.tsx
    page.tsx
    globals.css
    dashboard/
      page.tsx
    signature/
      page.tsx
    scale/
      page.tsx
    trace/
      page.tsx
    gain/
      page.tsx
    claims/
      page.tsx
    case-studies/
      page.tsx
      mesoscopic/
        page.tsx
      quantum-channel/
        page.tsx
    physicists/
      page.tsx
    docs/
      page.tsx
  components/
    layout/
      AppShell.tsx
      Sidebar.tsx
      Topbar.tsx
      MobileNav.tsx
    phygn/
      PhygnLogo.tsx
      MetricCard.tsx
      FormulaBlock.tsx
      TraceBadge.tsx
      ClaimDecisionBadge.tsx
      ScaleReviewCard.tsx
      BoundarySignaturePanel.tsx
      EpistemicTracePanel.tsx
      PredictiveGainPanel.tsx
      ClaimGatekeeperPanel.tsx
      PhysicistCard.tsx
      CaseStudyCard.tsx
      JsonOutput.tsx
    charts/
      QBLogChart.tsx
      DistributionBarChart.tsx
      GainGauge.tsx
    ui/
      shadcn components
  lib/
    api.ts
    types.ts
    constants.ts
    physicists.ts
    formulas.ts
    cn.ts
```

## Diseño visual

### Estética

```txt
scientific
premium
minimal
dark-capable
off-white + charcoal
taupe/sand como color base
iridescent spectrum como acento controlado
```

No usar arcoíris infantil.  
Usar **espectro físico / iridiscencia observacional**.

### Paleta sugerida

```txt
--background: 42 30% 97%;
--foreground: 220 18% 12%;

--card: 42 35% 99%;
--card-foreground: 220 18% 12%;

--primary: 42 18% 57%;
--primary-foreground: 42 40% 98%;

--secondary: 220 16% 18%;
--secondary-foreground: 42 40% 98%;

--muted: 42 18% 90%;
--muted-foreground: 220 10% 40%;

--accent: 190 80% 45%;
--accent-foreground: 220 18% 12%;

--destructive: 0 72% 50%;
--border: 42 16% 82%;
--input: 42 16% 84%;
--ring: 190 80% 45%;
```

### Gradiente espectral

Usar solo como acento:

```css
background: linear-gradient(
  90deg,
  #ef4444,
  #f97316,
  #eab308,
  #22c55e,
  #06b6d4,
  #3b82f6,
  #7c3aed
);
```

Uso permitido:

```txt
borde superior de cards
estado de traza detectable
visual de logo
hero sutil
```

Uso prohibido:

```txt
fondos enteros chillones
botones primarios saturados
dashboard arcoíris permanente
```

## shadcn/ui

Inicializar shadcn/ui.

Componentes mínimos:

```txt
button
card
badge
input
label
select
textarea
tabs
separator
sheet
dialog
tooltip
table
scroll-area
sonner
alert
form
```

## Preset Tailwind / shadcn

Configurar `globals.css` con tokens HSL compatibles con shadcn.

Añadir utilidades:

```css
.phygn-spectrum {
  background: linear-gradient(90deg,#ef4444,#f97316,#eab308,#22c55e,#06b6d4,#3b82f6,#7c3aed);
}

.phygn-glass {
  background: hsl(var(--card) / 0.72);
  backdrop-filter: blur(18px);
  border: 1px solid hsl(var(--border));
}

.phygn-formula {
  font-family: var(--font-mono);
  letter-spacing: -0.02em;
}

.phygn-muted-grid {
  background-image:
    linear-gradient(to right, hsl(var(--border) / 0.28) 1px, transparent 1px),
    linear-gradient(to bottom, hsl(var(--border) / 0.28) 1px, transparent 1px);
  background-size: 32px 32px;
}
```

## Layout

### AppShell

Debe tener:

```txt
sidebar izquierda
topbar
zona principal
estado API
selector dark/light
```

### Sidebar

Secciones:

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

## Pantalla 1 — Dashboard

Ruta:

```txt
/dashboard
```

Debe mostrar:

```txt
estado API
número de módulos activos
casos de estudio
últimas decisiones de claims
resumen de filosofía Phygn
```

Cards superiores:

```txt
Boundary Signatures
Epistemic Traces
Negative Bounds
Claim Gatekeeper
```

Hero:

```txt
Phygn
Physical Signatures Lab
```

Subtexto:

```txt
A local-first scientific cockpit for computing physical signatures, epistemic traces, negative bounds and claim validity.
```

## Pantalla 2 — Frontier Signature Lab

Ruta:

```txt
/signature
```

Formulario:

```txt
m_kg
L_value_m
L_type
physical_role
observer_channel
justification
allowed_range_min
allowed_range_max
arbitrariness_risk
```

Conecta a:

```txt
POST /frontier/signature
```

Outputs:

```txt
λC
rg
RS
Q
B
QB
(ℓP/L)^2
delta_QB
trace_type
claim_status
interpretation
```

Componentes:

```txt
FormulaBlock
MetricCard
QBLogChart
TraceBadge
ScaleReviewCard
JsonOutput
```

Fórmulas visibles:

\[
\lambda_C=\frac{\hbar}{mc}
\]

\[
r_g=\frac{Gm}{c^2}
\]

\[
Q=\frac{\lambda_C}{L}
\]

\[
B=\frac{r_g}{L}
\]

\[
QB=\left(\frac{\ell_P}{L}\right)^2
\]

## Pantalla 3 — Operational Scale Review

Ruta:

```txt
/scale
```

Explicar que \(L\) no puede ser arbitraria.

Mostrar tipos:

```txt
L_SYS
L_DET
L_INT
L_COH
L_WAVELENGTH
L_CURV
L_HORIZON
L_BOX
L_CHANNEL
```

Crear cards explicativas para cada una.

## Pantalla 4 — Epistemic Trace Lab

Ruta:

```txt
/trace
```

Caso inicial:

```txt
Depolarizing quantum channel
```

Formulario:

```txt
p
epsilon_exp
```

Conecta a:

```txt
POST /trace/depolarizing
```

Outputs:

```txt
P(Y|H)
P(Y|¬H)
τ
trace_type
claim_status
interpretation
```

Chart:

```txt
DistributionBarChart
```

Fórmula:

\[
\tau_O(H)=D[P(Y_O|H),P(Y_O|\neg H)]
\]

## Pantalla 5 — Predictive Gain

Ruta:

```txt
/gain
```

Formulario:

```txt
error_base
error_model
```

Conecta a:

```txt
POST /gain
```

Output:

```txt
Gain_C
status
interpretation
```

Fórmula:

\[
Gain_C=\frac{Error(M_{base})-Error(M_C)}{Error(M_{base})}
\]

## Pantalla 6 — Claim Gatekeeper

Ruta:

```txt
/claims
```

Formulario:

```txt
text
claim_type
layer
trace_type
predictive_gain
requires_L
L_status
```

Conecta a:

```txt
POST /claims/evaluate
```

Output:

```txt
decision
reason
safe_rewrite
```

Estados visuales:

```txt
ALLOWED
ALLOWED_LIMITED
REQUIRES_TRACE
REQUIRES_MODEL
BLOCKED
```

Claims de prueba predefinidos:

```txt
El invariante demuestra nueva física.
Minkowski demuestra Frontera C completa.
La conciencia valida Frontera C.
La cancelación de masa prueba una nueva ley.
El invariante es un lema estructural de consistencia.
```

## Pantalla 7 — Case Studies

Ruta:

```txt
/case-studies
```

Cards:

```txt
Quantum Depolarizing Channel
Mesoscopic Interferometer Negative Bound
```

### Mesoscopic

Ruta:

```txt
/case-studies/mesoscopic
```

Conecta a:

```txt
GET /case-studies/mesoscopic
```

Debe mostrar:

```txt
m = 1e-17 kg
L = 1e-7 m
Q
B
QB
trace_type = NEGATIVE_BOUND_TRACE
claim permitido
claim prohibido
```

### Quantum Channel

Ruta:

```txt
/case-studies/quantum-channel
```

Debe usar el mismo motor de `/trace`.

## Pantalla 8 — Physicists Cards

Ruta:

```txt
/physicists
```

Objetivo:

Crear tarjetas conceptuales de grandes físicos vinculando cada figura con una capa de Phygn/Frontera C.

Importante:

```txt
No afirmar que estos físicos validan Phygn.
No usar autoridad como prueba.
Usar las tarjetas como mapa histórico/conceptual.
```

Cards mínimas:

### Albert Einstein

Tema:

```txt
c, relatividad, causalidad, masa-energía
```

Conexión permitida:

```txt
Einstein proporciona parte del trasfondo relativista donde c actúa como límite causal.
```

Claim prohibido:

```txt
Einstein demuestra Frontera C.
```

### Hermann Minkowski

Tema:

```txt
espacio-tiempo, cono de luz, estructura causal
```

Conexión:

```txt
Minkowski proporciona la geometría causal mínima sobre la que Phygn define accesibilidad.
```

### Max Planck

Tema:

```txt
h, escala de Planck, cuantización
```

Conexión:

```txt
Planck aporta la constante h/ħ y el marco dimensional donde aparecen escalas frontera.
```

### Werner Heisenberg

Tema:

```txt
incertidumbre, límites de medición
```

Conexión:

```txt
Heisenberg representa la imposibilidad de separar medición, escala y observabilidad.
```

### Niels Bohr

Tema:

```txt
complementariedad, fenómeno observado
```

Conexión:

```txt
Bohr conecta con la idea de que el fenómeno físico depende del contexto experimental.
```

### John Archibald Wheeler

Tema:

```txt
it from bit, observador, información
```

Conexión:

```txt
Wheeler inspira la lectura informacional, sin servir como validación empírica.
```

### John Bell

Tema:

```txt
desigualdades, no localidad, test experimental
```

Conexión:

```txt
Bell muestra cómo convertir disputas conceptuales en desigualdades testeables.
```

### Wojciech Zurek

Tema:

```txt
decoherencia, quantum Darwinism, información robusta
```

Conexión:

```txt
Zurek es referencia natural para estudiar qué información deja huella en entornos.
```

### Leonard Susskind

Tema:

```txt
horizontes, complementaridad, información de agujeros negros
```

Conexión:

```txt
Susskind conecta frontera causal e información en contextos gravitacionales.
```

### Judea Pearl

Tema:

```txt
causalidad, modelos causales, intervención
```

Conexión:

```txt
Pearl inspira la necesidad de distinguir correlación, intervención y estructura causal.
```

## Modelo `physicists.ts`

Crear array:

```ts
export const physicists = [
  {
    name: "Albert Einstein",
    years: "1879–1955",
    domain: "Relativity",
    coreIdea: "c as invariant causal structure",
    phygnConnection: "...",
    allowedClaim: "...",
    forbiddenClaim: "...",
    layer: "PHYSICAL_CORE"
  }
]
```

No usar retratos si no hay derechos claros. Usar iniciales, geometrías, fórmulas o abstracciones.

## Pantalla 9 — Docs

Ruta:

```txt
/docs
```

Mostrar documentos `.md` de `/docs` o enlaces a:

```txt
Master Context
Backend Architecture
Frontend Architecture
API Spec
Benchmarks
Roadmap
```

## Componentes visuales clave

### `MetricCard`

Para valores numéricos.

### `FormulaBlock`

Debe renderizar LaTeX con KaTeX.

### `TraceBadge`

Colores:

```txt
NULL_TRACE → muted
STRUCTURAL_TRACE → sand/taupe
DETECTABLE_TRACE → cyan/blue
PREDICTIVE_TRACE → green
NEGATIVE_BOUND_TRACE → amber
BLOCKED → red
```

### `ClaimDecisionBadge`

Colores:

```txt
ALLOWED → green
ALLOWED_LIMITED → blue/taupe
REQUIRES_TRACE → amber
REQUIRES_MODEL → orange
BLOCKED → red
```

### `PhysicistCard`

Debe mostrar:

```txt
nombre
dominio
idea central
conexión permitida
claim prohibido
layer badge
```

## API client

Crear `lib/api.ts`.

Debe usar `fetch`.

Config:

```ts
const API_BASE_URL = process.env.NEXT_PUBLIC_PHYGN_API_URL ?? "http://127.0.0.1:8000"
```

Funciones:

```ts
getHealth()
validateInvariant(input)
calculateSignature(input)
calculateDepolarizingTrace(input)
calculateGain(input)
evaluateClaim(input)
getMesoscopicCase()
```

## Robustez UX

Si backend no está disponible:

```txt
mostrar estado API offline
mostrar instrucciones para uvicorn
no romper UI
```

## Criterios de aceptación frontend

```txt
npm run dev arranca
todas las rutas cargan
dashboard muestra estado API
signature llama a backend
trace llama a backend
claims llama a backend
case studies llama a backend
physicists muestra cards
diseño coherente con Phygn
no hay claims inflados
```
