# Claim Gatekeeper v0.3

## Objetivo

Convertir el autocontrol epistémico de Frontera C en una máquina de clasificación de claims.

## Tipos

```txt
DEFINITION
AXIOM
STRUCTURAL_LEMMA
HYPOTHESIS
MODEL
BENCHMARK
NEGATIVE_BOUND
SPECULATIVE_EXTENSION
```

## Trazas

```txt
NULL_TRACE
STRUCTURAL_TRACE
THEORETICAL_TRACE
DETECTABLE_TRACE
PREDICTIVE_TRACE
NEGATIVE_BOUND_TRACE
BLOCKED
```

## Reglas principales

### Regla 1 — Hipótesis sin modelo alternativo

Si una hipótesis requiere:

\[
\tau_O(H)=D[P(Y|H),P(Y|\neg H)]
\]

pero no define \(P(Y|\neg H)\):

```txt
status = REQUIRES_MODEL
```

### Regla 2 — Hipótesis con tau=0

Si:

\[
\tau_O(H)=0
\]

```txt
status = BLOCKED_AS_OPERATIONALLY_EMPTY
```

### Regla 3 — Lema estructural

Si una expresión deriva de definiciones:

```txt
type = STRUCTURAL_LEMMA
trace = STRUCTURAL_TRACE
predictive_gain = NONE_YET
```

### Regla 4 — Claim de nueva física

Todo claim de nueva física exige al menos:

```txt
DETECTABLE_TRACE o PREDICTIVE_TRACE o NEGATIVE_BOUND_TRACE explícita contra modelo base
```

### Regla 5 — Escala L injustificada

Si L no tiene metadatos físicos suficientes:

```txt
status = BLOCKED_AS_AD_HOC_SCALE
```

## Claims bloqueados por defecto

```txt
El invariante demuestra nueva física.
Minkowski demuestra Frontera C completa.
La conciencia valida Frontera C.
Cancelación de masa prueba nueva ley.
Una firma Q/B con L arbitraria tiene valor predictivo.
```
