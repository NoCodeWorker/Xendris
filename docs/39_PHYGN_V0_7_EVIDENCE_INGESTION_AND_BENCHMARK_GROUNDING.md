# Phygn v0.7 — Evidence Ingestion & Benchmark Grounding

## 0. Propósito

Phygn v0.6 construyó el juicio:

```txt
model comparison engine
CAMPAIGN-002 toy model comparison
MODEL_DELTA_ONLY
Gain_C undefined without y_true
decoherence overclaims blocked
```

v0.7 debe traer pruebas admisibles al juicio.

Objetivo:

```txt
pasar de MODEL_DELTA_ONLY
a SOURCE_BACKED_MODEL_COMPARISON
```

sin afirmar todavía predicción física fuerte.

## 1. Estado heredado

De v0.5:

```txt
CAMPAIGN-001:
m = 1e-17 kg
L = 1e-7 m
B = 7.43e-38
region = NEGATIVE_GRAVITY_BOUND
non_triviality = NEGATIVE_NONTRIVIAL
```

De v0.6:

```txt
CAMPAIGN-002:
toy baseline = exp(-gamma_base t)
toy candidate = exp(-(gamma_base + alpha B)t)
max_abs_delta ≈ 0
detectability = UNDETECTABLE_DIFFERENCE
Gain_C = None without y_true
evidence_level = 3
claim_level_max = 3
```

## 2. Goal v0.7

Construir la capa que permite responder:

```txt
¿Qué fuentes soportan el modelo base?
¿Qué fuentes soportan los parámetros?
¿Qué datos o benchmark permiten calcular error?
¿Qué y_true es real, sintético o placeholder?
¿Qué claims suben de nivel y cuáles siguen bloqueados?
```

## 3. Ambición histórica controlada

v0.7 puede ser histórica si logra algo que casi ningún sistema especulativo hace:

```txt
separar de forma computacional:
- cálculo estructural
- toy model
- fuente científica
- benchmark
- dato real
- dato sintético
- predicción permitida
- predicción bloqueada
```

No es histórico por afirmar más.

Es histórico por **no permitir saltos de evidencia**.

## 4. Pilar invariable

Todo sigue anclado en:

\[
QB=\left(\frac{\ell_P}{L}\right)^2
\]

y en la regla:

```txt
El invariante no demuestra nueva física.
El invariante fija una restricción estructural de coordenadas frontera.
```

v0.7 no puede reetiquetar el invariante como:

```txt
physical decoherence cause
empirical evidence
prediction
```

## 5. Transición buscada

Entrada:

```txt
MODEL_DELTA_ONLY
```

Salida posible:

```txt
SOURCE_BACKED_TOY_MODEL
SOURCE_BACKED_BASELINE
SYNTHETIC_BENCHMARK_READY
EXPERIMENTAL_BENCHMARK_READY
POSITIVE_SYNTHETIC_GAIN
ZERO_SYNTHETIC_GAIN
NEGATIVE_SYNTHETIC_GAIN
REQUIRES_EXPERIMENTAL_DATA
```

No saltar a:

```txt
PREDICTIVE_NONTRIVIAL
EMPIRICALLY_ACTIONABLE
```

salvo que haya:

```txt
fuentes
modelo físico defendible
observable
benchmark
y_true
epsilon_exp realista
Gain_C
revisión gatekeeper
```

## 6. Nuevos objetos v0.7

```txt
EvidenceRecord
BenchmarkDataset
BenchmarkProvenance
SourceBackedModelSpec
EvidenceAuditResult
BenchmarkReadinessResult
```

## 7. Criterio de éxito mínimo

v0.7 se considera completada si:

```txt
1. existe un protocolo de ingesta de fuentes;
2. existe un registro de evidencia;
3. existe un protocolo de benchmark;
4. existe distinción entre y_true real, sintético y placeholder;
5. CAMPAIGN-002 puede ejecutarse con benchmark sintético etiquetado;
6. Gain_C solo se calcula si y_true está presente;
7. los claims físicos siguen bloqueados si las fuentes o benchmarks no bastan;
8. reports son generados;
9. tests pasan.
```

## 8. No source ingestion fake rule

Si la IA no puede navegar o no tiene PDFs:

```txt
crear ResearchTask
crear SourceRequirement
no crear SourceRecord falso
no marcar SOURCE_INGESTED
no desbloquear claims
```

Si sí tiene fuentes concretas:

```txt
crear SourceRecord
guardar notas/chunks
crear ClaimSourceLink
auditar trust/support
actualizar claim status
```

## 9. Benchmark honesty rule

Un benchmark debe etiquetarse como:

```txt
SYNTHETIC
SIMULATED
LITERATURE_EXTRACTED
EXPERIMENTAL
PLACEHOLDER
```

Regla:

```txt
PLACEHOLDER no puede calcular Gain_C.
SYNTHETIC puede calcular Synthetic Gain, no physical Predictive Gain.
EXPERIMENTAL puede calcular Predictive Gain si la procedencia es válida.
```

## 10. Frase guía

```txt
Ya tenemos el juicio.
Ahora necesitamos pruebas admisibles.
```

## 11. Mantra v0.7

```txt
No fuente, no interpretación.
No procedencia, no benchmark.
No y_true, no Gain.
No experimental threshold, no detectabilidad física.
No evidencia suficiente, no subida de claim.
```
