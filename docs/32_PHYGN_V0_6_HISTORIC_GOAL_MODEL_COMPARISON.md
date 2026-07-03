# Phygn v0.6 — Historic Goal: From Negative Bound to Model Comparison

## 0. Propósito

Phygn v0.5 produjo su primer resultado negativo no trivial:

```txt
CAMPAIGN-001:
m = 1e-17 kg
L = 1e-7 m
B = rg/L = 7.43e-38
region = NEGATIVE_GRAVITY_BOUND
decoherence overclaim = BLOCKED
non-triviality = NEGATIVE_NONTRIVIAL
```

Ese resultado no demuestra nueva física.  
Pero sí demuestra algo esencial:

```txt
Phygn puede calcular, clasificar, bloquear y exigir condiciones antes de permitir un claim.
```

v0.6 debe intentar el siguiente salto:

```txt
pasar de cota negativa
a comparación de modelos
```

## 1. Ambición histórica

El goal v0.6 es construir una arquitectura donde Phygn pueda preguntar:

```txt
¿Un modelo boundary-aware mejora, distingue o modifica alguna predicción frente a un modelo base físico conocido?
```

Esto es lo que puede volver histórico al Lab:

```txt
no porque proclame una nueva teoría,
sino porque obliga a cualquier hipótesis de Frontera C a competir contra modelos estándar bajo fuentes, tests, benchmarks y métricas.
```

La ambición no es gritar:

```txt
hemos descubierto nueva física
```

La ambición es construir una máquina que diga:

```txt
esta modificación no aporta nada;
esta modificación empeora;
esta modificación produce una diferencia no detectable;
esta modificación produce una diferencia detectable;
esta modificación mejora el modelo base bajo una métrica explícita.
```

Si algún día aparece un `Gain_C > 0` defendible, Phygn habrá ganado el derecho a hablar más fuerte.

## 2. Pilar invariable

Todo v0.6 sigue anclado en:

\[
\lambda_C r_g = \ell_P^2
\]

\[
Q = \frac{\lambda_C}{L}
\]

\[
B = \frac{r_g}{L}
\]

\[
QB = \left(\frac{\ell_P}{L}\right)^2
\]

Este invariante no se infla.

Estado correcto:

```txt
STRUCTURAL_LEMMA
STRUCTURAL_TRACE
BOUNDARY_COORDINATE_CONSTRAINT
```

Estado prohibido:

```txt
NEW_PHYSICS_PROOF
EXPERIMENTAL_EVIDENCE
PREDICTIVE_TRACE
```

## 3. Qué significa "hacer algo histórico" sin autoengaño

Histórico no significa "afirmar algo más grande".

Histórico significa:

```txt
construir una máquina que no deja pasar claims falsos,
pero sí puede detectar cuándo una hipótesis empieza a ganar derecho predictivo.
```

Phygn v0.6 debe aspirar a ser:

```txt
el primer cockpit computacional donde una hipótesis frontera se somete automáticamente a:
- invariante Q/B
- escala L
- RAG
- fuentes
- test
- benchmark
- modelo base
- modelo candidato
- Predictive Gain
- Gatekeeper
- Red Team
```

## 4. Goal v0.6

Crear:

```txt
CAMPAIGN-002 — Decoherence Model Comparison
```

Objetivo:

```txt
comparar un modelo base de decoherencia mesoscópica contra un modelo candidato boundary-aware, sin afirmar éxito salvo que exista diferencia cuantificada y fuente suficiente.
```

## 5. Pregunta científica

```txt
Para un sistema mesoscópico con masa m y escala operacional L, ¿puede una modificación boundary-aware producir una diferencia cuantificable frente a un modelo base de decoherencia, y esa diferencia supera un umbral experimental?
```

## 6. Resultado permitido

v0.6 puede producir uno de estos estados:

```txt
MODEL_NOT_READY:
faltan fuentes o modelo base.

ZERO_GAIN:
el candidato no mejora.

NEGATIVE_GAIN:
el candidato empeora.

UNDETECTABLE_DIFFERENCE:
hay diferencia matemática pero queda por debajo de epsilon_exp.

POSITIVE_TOY_GAIN:
hay mejora en toy benchmark, pero no claim físico fuerte.

PREDICTIVE_CANDIDATE:
hay diferencia cuantificable, fuente suficiente y benchmark, pero aún falta experimento.

EMPIRICALLY_ACTIONABLE:
hay observable, rango, umbral, sistema, protocolo y fuente.
```

## 7. Regla de oro

```txt
No source → no hard claim.
No model base → no gain.
No candidate model → no comparison.
No error metric → no benchmark.
No epsilon_exp → no detectability.
No test → no feature.
No report → no result.
```

## 8. Qué debe bloquear v0.6

Debe seguir bloqueando:

```txt
Phygn predicts gravitational decoherence.
Phygn proves quantum gravity.
The invariant explains decoherence.
Boundary C causes collapse.
The atlas validates Frontera C.
```

Hasta que exista todo:

```txt
dynamic model
sources
observable
baseline
candidate
metric
benchmark
Predictive Gain
detectability threshold
```

## 9. Novedad defendible

La novedad v0.6, si se completa, no será una predicción física fuerte.

Será:

```txt
un pipeline reproducible para degradar, bloquear o comparar hipótesis boundary-aware frente a modelos de decoherencia.
```

Eso ya es serio.

## 10. Métrica central

\[
Gain_C = \frac{Error(M_{base}) - Error(M_C)}{Error(M_{base})}
\]

Clasificación:

```txt
Gain_C > 0 → candidate improves under selected metric.
Gain_C = 0 → candidate redundant.
Gain_C < 0 → candidate worse.
```

Pero:

```txt
toy data → limited claim
simulated data → limited claim
experimental data → stronger claim
```

## 11. Frase guía

```txt
Ya no buscamos una frase más grande.
Buscamos una comparación que sobreviva.
```

## 12. Manifiesto operativo

```txt
El invariante es el pilar.
La escala L es la puerta.
El RAG es la memoria.
El benchmark es el juicio.
El Predictive Gain es el permiso.
El Gatekeeper es la frontera.
```
