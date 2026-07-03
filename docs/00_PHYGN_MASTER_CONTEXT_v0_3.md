# Phygn v0.3 — Master Context

## Nombre del proyecto

```txt
Phygn
```

## Significado de marca

```txt
PHY = Physical / Physics
GN  = Sign / Signature / Trace / Geometry / Network
```

Interpretación oficial:

> **Phygn — Physical Signatures Lab**

Definición:

> Phygn es un laboratorio científico-computacional local para calcular firmas físicas, huellas epistemológicas, cotas negativas y validez de hipótesis dentro del marco Frontera C.

## Propósito

Phygn no es una teoría física nueva por sí mismo.  
Phygn es el laboratorio operacional de Frontera C.

Su función es convertir:

```txt
conceptos → cálculos → benchmarks → trazas → decisiones de claim
```

## Principio rector

```txt
La generalidad puede esperar.
La predicción no.
```

## Núcleo de Frontera C implementado en Phygn

Phygn implementa:

1. longitudes frontera;
2. firma mínima Q/B;
3. validación del lema estructural \(\lambda_C r_g = \ell_P^2\);
4. selección justificada de escala operacional \(L\);
5. huella epistemológica \(\tau_O(H)\);
6. Predictive Gain;
7. Claim Gatekeeper;
8. casos de estudio computables;
9. API local;
10. tests.

## Claim central permitido

> Phygn implementa un protocolo computable para clasificar fronteras físicas, calcular huellas epistemológicas, producir cotas negativas y bloquear claims no justificados.

## Claim prohibido

```txt
Phygn demuestra nueva física.
```

## Capas conceptuales

```txt
PHYSICAL_CORE
ONTO_EPISTEMIC_CORE
QUANTUM_CHANNEL_CORE
APPLICATION_TRACK
COGNITIVE_EXTENSION
SPECULATIVE_ONLY
```

Regla dura:

```txt
COGNITIVE_EXTENSION no puede validar PHYSICAL_CORE.
```

## Tipos formales

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

## Tipos de traza

```txt
NULL_TRACE
STRUCTURAL_TRACE
THEORETICAL_TRACE
DETECTABLE_TRACE
PREDICTIVE_TRACE
NEGATIVE_BOUND_TRACE
BLOCKED
```

## Primer lema estructural

\[
\lambda_C r_g = \ell_P^2
\]

donde:

\[
\lambda_C=\frac{\hbar}{mc}
\]

\[
r_g=\frac{Gm}{c^2}
\]

\[
\ell_P=\sqrt{\frac{\hbar G}{c^3}}
\]

Clasificación:

```txt
LEM-001
Tipo: STRUCTURAL_LEMMA
Traza: STRUCTURAL_TRACE
Predictive Gain: NONE_YET
Uso permitido: consistencia, firma Q/B, benchmark
Uso prohibido: prueba de nueva física
```

## Firma mínima Q/B

\[
Q=\frac{\lambda_C}{L}
\]

\[
B=\frac{r_g}{L}
\]

\[
QB=\left(\frac{\ell_P}{L}\right)^2
\]

La firma solo tiene validez operacional si \(L\) está físicamente justificada.

## Huella epistemológica

\[
\tau_O(H)=D[P(Y_O|H),P(Y_O|\neg H)]
\]

Interpretación:

```txt
Si τ = 0 → hipótesis operativamente vacía para el observador/canal dado.
Si τ > εexp → huella detectable.
```

## Predictive Gain

\[
Gain_C=\frac{Error(M_{base})-Error(M_C)}{Error(M_{base})}
\]

Phygn debe calcularlo sin maquillaje:

```txt
POSITIVE_GAIN
ZERO_GAIN
NEGATIVE_GAIN
```

## Estado del proyecto

El usuario ya tiene una primera estructura de código en:

```txt
d:\BIOCULTOR\PHYNG\
```

con módulos backend, API y tests.

La siguiente fase es continuar el desarrollo sin romper esa estructura, añadir documentación, endurecer tests, mejorar README, preparar API y opcionalmente construir frontend.
