# Phygn v0.3 — Frontend Architecture

## Estado

El frontend es opcional en esta fase.

Solo debe construirse cuando:

```txt
backend funciona
tests pasan
API responde
casos de estudio devuelven resultados correctos
```

## Objetivo del frontend

Crear un cockpit científico para visualizar:

```txt
firmas Q/B
huellas epistemológicas
cotas negativas
claims bloqueados
estado de escala L
resultados de benchmarks
```

No debe ser una landing bonita.  
Debe ser un panel de laboratorio.

## Stack recomendado

```txt
Next.js App Router
TypeScript
Tailwind CSS
shadcn/ui
TanStack Query
Recharts o Plotly
KaTeX
Zustand opcional
```

## Diseño conceptual

Nombre:

```txt
Phygn — Physical Signatures Lab
```

Tagline:

```txt
Physical signatures. Epistemic traces. Boundary claims.
```

## Pantallas principales

### 1. Dashboard

Debe mostrar:

```txt
estado API
número de tests/benchmarks
últimas firmas calculadas
claims bloqueados
casos de estudio disponibles
```

### 2. Frontier Signature Lab

Inputs:

```txt
m_kg
L_value_m
L_type
physical_role
observer_channel
justification
arbitrariness_risk
allowed_range_m
```

Output:

```txt
lambda_C
r_g
R_S
Q
B
QB
delta_QB
trace_type
claim_status
interpretation
```

Visualizaciones:

```txt
Q/B card
log plot q,b
validación QB
semáforo de L
```

### 3. Operational Scale Review

Pantalla dedicada a \(L\).

Debe responder:

```txt
¿qué es L?
¿por qué se eligió?
¿qué canal representa?
¿puede soportar claims predictivos?
```

### 4. Epistemic Trace Lab

Caso inicial:

```txt
Depolarizing quantum channel
```

Inputs:

```txt
p
epsilon_exp
```

Output:

```txt
P(Y|H)
P(Y|¬H)
tau
trace_type
operational_status
```

Visualizaciones:

```txt
barras de distribución
valor de tau
umbral epsilon_exp
```

### 5. Predictive Gain Lab

Inputs:

```txt
error_base
error_model
```

Output:

```txt
Gain_C
status
interpretation
```

### 6. Claim Gatekeeper

Input:

```txt
claim text
claim_type
layer
trace_type
predictive_gain
requires_L
L_status
```

Output:

```txt
decision
reason
safe_rewrite
```

Debe mostrar visualmente:

```txt
ALLOWED
ALLOWED_LIMITED
REQUIRES_TRACE
REQUIRES_MODEL
BLOCKED
```

### 7. Case Studies

Iniciales:

```txt
Quantum depolarizing channel
Mesoscopic interferometer negative bound
```

Cada caso debe tener:

```txt
inputs
fórmulas
resultados
interpretación permitida
interpretación prohibida
```

## Identidad visual

Símbolo sugerido:

```txt
huella física / fingerprint / physical sign
contenida por una frontera circular
```

Paleta recomendada:

```txt
background: off-white
text: charcoal
primary: taupe/sand
accent: iridescent spectrum, usado con moderación
```

El arcoíris literal debe evitarse como identidad base. Mejor usar:

```txt
espectro físico
iridiscencia observacional
gradiente científico refinado
```

## Principio UX

Cada pantalla debe responder:

```txt
¿Qué se está calculando?
¿Qué claim permite?
¿Qué claim bloquea?
Qué traza produce?
Cuál es la limitación?
```

## No hacer

```txt
No ocultar incertidumbre.
No presentar STRUCTURAL_TRACE como PREDICTIVE_TRACE.
No usar colores para exagerar resultados.
No convertir Phygn en una web de marketing.
```
