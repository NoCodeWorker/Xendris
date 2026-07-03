# Phygn v1.5 — Informe Consolidado de Benchmark Sintético
### Candidate vs Baseline · CAND-FC-B-NEGCTRL-001 · 2026-06-30

> Este documento unifica los 5 reportes generados por la campaña v1.5 en un único
> documento narrado y completamente explicado. Ningún resultado aquí constituye
> una predicción física validada. Todos los claims físicos permanecen **BLOQUEADOS**.

---

## Índice

1. [Contexto del experimento](#1-contexto-del-experimento)
2. [Las dos ecuaciones que se comparan](#2-las-dos-ecuaciones-que-se-comparan)
3. [Parámetros del sistema](#3-parámetros-del-sistema)
4. [Resultado principal: Delta y Detectabilidad](#4-resultado-principal-delta-y-detectabilidad)
5. [Alpha Sweep: ¿cuánto alpha haría falta?](#5-alpha-sweep-cuánto-alpha-haría-falta)
6. [Condiciones de fallo disparadas](#6-condiciones-de-fallo-disparadas)
7. [Supervivencia del candidato](#7-supervivencia-del-candidato)
8. [Claims permitidos y bloqueados](#8-claims-permitidos-y-bloqueados)
9. [Próximas acciones requeridas](#9-próximas-acciones-requeridas)
10. [Fuentes de los reportes](#10-fuentes-de-los-reportes)

---

## 1. Contexto del experimento

### ¿Qué es Phygn?

Phygn es un laboratorio de **Physical Signatures** (firmas físicas). Su misión es
desarrollar y someter a prueba modelos candidatos que pretendan añadir un término
nuevo a la física de la decoherencia cuántica. El sistema está diseñado para ser
**epistemológicamente honesto**: ningún claim físico puede proclamarse sin pasar por
una cadena estricta de validaciones cuantitativas.

### ¿Qué es el candidato `CAND-FC-B-NEGCTRL-001`?

El candidato pertenece a la familia **B_SUPPRESSED** de la teoría Frontera C.
Propone que la tasa de decoherencia del entorno se ve modificada por un término
adicional proporcional al factor gravitacional B:

```
DeltaGamma_C = alpha × B
```

donde:
- **B** = r_g / L (razón de Schwarzschild al tamaño del sistema) — un número
  extremadamente pequeño para sistemas mesoscópicos ordinarios.
- **alpha** = escala de acoplamiento pre-registrada (libre por ahora, sin
  justificación de fuentes).

Este candidato es un **control negativo** por diseño: se espera que B sea tan
pequeño que el efecto sea indetectable bajo parámetros físicamente razonables.
Eso es información valiosa, no un fracaso.

### ¿Qué hace este benchmark?

Por primera vez en Phygn (v1.5), se confronta cuantitativamente la curva del
modelo base con la del candidato:

```
¿Produce el candidato una diferencia numérica detectable frente al baseline?
```

Este benchmark es **sintético** (toy): usa parámetros declarados, no datos
experimentales reales. No puede desbloquear predicciones físicas.

---

## 2. Las dos ecuaciones que se comparan

### Baseline — modelo de decoherencia de entorno puro

```
V_base(t) = exp(−Γ_env · t)
```

Describe la **visibilidad de interferencia** de un sistema cuántico que decae
exponencialmente a una tasa Γ_env dictada por el entorno. Es el modelo de
referencia: sin ningún efecto Frontera C.

### Candidato — modelo con término Frontera C

```
V_candidate(t) = exp(−(Γ_env + ΔΓ_C) · t)
     donde  ΔΓ_C = alpha × B
```

El candidato añade una **tasa de decoherencia extra** ΔΓ_C al baseline. Si este
término fuera detectable, el sistema decaería más rápido de lo predicho por el
baseline solo.

### La diferencia (delta)

```
delta(t) = V_candidate(t) − V_base(t)
```

Como ΔΓ_C > 0 siempre, el candidato **decae más rápido** que el baseline:
delta(t) ≤ 0 para todo t > 0. El tamaño de esta diferencia es lo que se evalúa.

---

## 3. Parámetros del sistema

Estos parámetros corresponden al sistema mesoscópico de la Campaña 002 de Phygn:

| Parámetro | Valor | Descripción |
|---|---|---|
| `m_kg` | 1.000×10⁻¹⁷ kg | Masa del sistema (mesoscópico) |
| `L_value_m` | 1.000×10⁻⁷ m | Escala de longitud del sistema (100 nm) |
| **`B`** | **7.426×10⁻³⁸** | Factor gravitacional B = r_g/L (extremadamente pequeño) |
| `QB` | 2.612×10⁻⁵⁶ | Factor cuántico-gravitacional QB (más pequeño aún) |
| `gamma_env` (Γ_env) | 0.05 s⁻¹ | Tasa de decoherencia del entorno (baseline) |
| `alpha` (default) | 1.0 | Factor de acoplamiento candidato (default, sin constricción) |
| `epsilon_exp` | 1×10⁻⁶ | Umbral experimental declarado de detectabilidad |
| `t_grid` | [0, 10] s (101 puntos) | Rejilla temporal del benchmark |

> **Por qué B es tan pequeño:** Para un sistema de 10⁻¹⁷ kg y tamaño 100 nm,
> el radio de Schwarzschild r_g ≈ 7.4×10⁻⁴⁵ m. La razón r_g/L ≈ 7.4×10⁻³⁸.
> Este número refleja que la gravedad es negligible a escalas mesoscópicas,
> lo cual es física conocida.

---

## 4. Resultado principal: Delta y Detectabilidad

### ¿Cuánto difieren baseline y candidato?

Con los parámetros por defecto (alpha = 1.0):

```
ΔΓ_C = alpha × B = 1.0 × 7.426×10⁻³⁸ ≈ 7.43×10⁻³⁸  [s⁻¹]
```

Esta es una tasa de decoherencia adicional **38 órdenes de magnitud más pequeña**
que la tasa de entorno (Γ_env = 0.05 s⁻¹).

La diferencia máxima entre las curvas:

| Métrica | Valor | Interpretación |
|---|---|---|
| `max_abs_delta` | **≈ 0.000** (< 10⁻⁵⁰) | La diferencia es numéricamente cero |
| `epsilon_exp` | 1×10⁻⁶ | Umbral de detectabilidad declarado |
| `detectability_status` | **`UNDETECTABLE_SYNTHETIC_DELTA`** | El candidato NO es detectable |

### ¿Qué significa "undetectable"?

Que incluso si existiera un detector con sensibilidad 10⁻⁶ (muy por encima de
cualquier capacidad experimental actual), el candidato bajo alpha=1 produciría
una diferencia 44 órdenes de magnitud por debajo de ese umbral.

> **Importante:** Esto no significa que la teoría sea falsa. Significa que bajo
> parámetros razonables el efecto es **invisible numéricamente**. El benchmark
> lo ha confirmado cuantitativamente.

### Estimación de alpha_min

¿Qué valor de alpha sería necesario para cruzar el umbral ε = 10⁻⁶?

Usando la estimación de primer orden:

```
alpha_min ≈ epsilon_exp / (B × max_t(t × exp(−Γ_env × t)))
          ≈ 1×10⁻⁶ / (7.426×10⁻³⁸ × max_t(...))
          ≈ 2.22×10³⁰
```

Un alpha de ~10³⁰ sería necesario para que el candidato cruce el umbral.
Esto clasifica como **`ALPHA_EXTREME`** en la clasificación heurística del sistema.

---

## 5. Alpha Sweep: ¿cuánto alpha haría falta?

El sweep explora 7 órdenes de magnitud para trazar la transición desde
"indetectable" hasta "detectable":

| alpha | ΔΓ_C | max_abs_delta | Detectabilidad | Razonabilidad |
|---|---|---|---|---|
| **1×10⁰** | 7.43×10⁻³⁸ | ~0 | `UNDETECTABLE` | `ALPHA_REASONABLE_TOY` |
| **1×10¹⁰** | 7.43×10⁻²⁸ | ~0 | `UNDETECTABLE` | `ALPHA_LARGE` |
| **1×10²⁰** | 7.43×10⁻¹⁸ | 1.11×10⁻¹⁶ | `UNDETECTABLE` | `ALPHA_LARGE` |
| **1×10³⁰** | 7.43×10⁻⁸ | 4.50×10⁻⁷ | `UNDETECTABLE` | `ALPHA_EXTREME` |
| **1×10³⁵** | 7.43×10⁻³ | **4.34×10⁻²** | ✅ `DETECTABLE` | `ALPHA_EXTREME` |
| **1×10³⁸** | 7.43×10⁰ | 9.60×10⁻¹ | ✅ `DETECTABLE` | ⚠️ `UNPHYSICAL` |
| **1×10⁴⁰** | 7.43×10⁺² | 9.95×10⁻¹ | ✅ `DETECTABLE` | ⚠️ `UNPHYSICAL` |

### Lectura del sweep

- **Para alpha ≤ 10³⁰**: el delta crece pero permanece por debajo de ε = 10⁻⁶.
  Son 30 órdenes de magnitud de margen antes de rozar la detectabilidad.

- **alpha = 10³⁵**: primer cruce del umbral en el sweep. El delta alcanza ~0.043,
  que es 43 000 veces el umbral declarado. Sin embargo, alpha = 10³⁵ es
  clasificado como `ALPHA_EXTREME`: un valor heurístico muy grande pero aún dentro
  del espacio "toy extremo".

- **alpha ≥ 10³⁸**: el delta se acerca a 1.0, lo que significa que el candidato
  predice una decoherencia casi total durante el experimento. Pero alpha en este
  rango es `ALPHA_UNPHYSICAL_OR_UNCONSTRAINED`, lo que activa la condición de fallo
  `REQUIRES_UNPHYSICAL_ALPHA`.

> **Conclusión del sweep:** Para este candidato B-suprimido con los parámetros
> mesoscópicos de la Campaña 002, no existe ningún valor de alpha razonable
> (≤ 10³⁵ en clasificación EXTREME) que produzca una detectabilidad creíble
> sin apelar a un acoplamiento no físico.

---

## 6. Condiciones de fallo disparadas

El sistema evalúa 4 condiciones de fallo v1.5. Las 3 siguientes se dispararon:

### `FAIL_UNDETECTABLE_DELTA` ✅ Disparado

**¿Por qué?** `max_abs_delta ≤ epsilon_exp` bajo alpha = 1.0.

**Significado:** El candidato no produce ninguna señal distinguible del baseline
bajo el umbral experimental declarado. Es el fallo más básico de un candidato:
produce el mismo resultado que el modelo sin él.

**Lenguaje permitido:**
> "El candidato es sintéticamente indetectable bajo el umbral declarado."

---

### `FAIL_NO_BENCHMARK` ✅ Disparado

**¿Por qué?** No hay `y_true` (datos experimentales reales). El benchmark es
sintético por definición.

**Significado:** Sin datos experimentales, es imposible calcular el `PredictiveGain`
real del candidato. El benchmark solo puede comparar ecuaciones contra sí mismas,
no contra la naturaleza.

**Lenguaje permitido:**
> "PredictiveGain no puede computarse. No existen datos experimentales."

---

### `FAIL_NO_SOURCE_SUPPORT` ✅ Disparado

**¿Por qué?** El candidato no tiene `source_ids`: ningún paper, ninguna referencia
experimental, ningún resultado previo respalda el término `ΔΓ_C = alpha × B`.

**Significado:** Sin soporte de fuentes, el candidato es toy-level: puede ser
computado, pero no puede ser interpretado físicamente. Alpha es un parámetro libre
sin constricción externa.

**Lenguaje permitido:**
> "El candidato no puede reclamar interpretación física en ausencia de soporte bibliográfico."

---

### `REQUIRES_UNPHYSICAL_ALPHA` — No disparado bajo alpha_min estimado

El alpha mínimo estimado es ~2.22×10³⁰, que clasificaría como `ALPHA_EXTREME`
(umbral de "unphysical" es > 10³⁵). Sin embargo, **en el sweep**, los primeros
valores detectables que aparecen como `UNPHYSICAL` son alpha ≥ 10³⁸, donde sí
se dispara `REQUIRES_UNPHYSICAL_ALPHA`.

---

## 7. Supervivencia del candidato

Tras evaluar todas las condiciones de fallo, el sistema clasifica al candidato:

```
candidate_survival = SURVIVES_AS_TOY_NEGATIVE_CONTROL
```

### ¿Qué significa esto?

| Estado | Significado |
|---|---|
| `SURVIVES_AS_TOY_NEGATIVE_CONTROL` | El candidato sobrevive como **control negativo** del sistema |

Un **control negativo** en Phygn es un candidato que:
- Está bien definido matemáticamente ✅
- Tiene sus condiciones de fallo claras ✅
- Produce una señal indetectable bajo parámetros razonables ✅ (esperado)
- No tiene soporte de fuentes ni datos reales ✅ (conocido)

Esto es valioso porque:
1. **Calibra el sistema**: confirma que el framework no infla resultados vacuos.
2. **Establece el baseline de comparación**: futuros candidatos más fuertes se
   medirán contra este zero-point.
3. **Es honesto**: un sistema que no reporta nada cuando no hay nada que reportar
   es un sistema en el que se puede confiar.

> El candidato CAND-FC-B-NEGCTRL-001 no es un fracaso de Frontera C.
> Es el primer paso cuantitativo de Frontera C.

---

## 8. Claims permitidos y bloqueados

### ✅ Lo que SÍ se puede afirmar

| Claim | Base |
|---|---|
| El candidato fue sometido a benchmark sintético. | Resultado computado y verificado. |
| El candidato es indetectable bajo los parámetros toy declarados. | max_abs_delta ≈ 0, epsilon = 1e-6. |
| El candidato requiere alpha ≈ 2.22×10³⁰ para detectabilidad sintética. | Estimación de primer orden confirmada. |
| Los claims físicos permanecen bloqueados. | Protocolo epistémico activo. |

### ❌ Lo que NO se puede afirmar

| Claim bloqueado | Razón |
|---|---|
| "Phygn predicts decoherence." | No hay datos experimentales, ni source-backing. |
| "Frontera C is validated." | Ningún benchmark sintético puede validar una teoría física. |
| "Candidate has physical PredictiveGain." | Sin y_true, PredictiveGain no puede computarse. |
| "Synthetic delta proves physical effect." | Toy benchmark ≠ evidencia experimental. |

---

## 9. Próximas acciones requeridas

Para avanzar al siguiente nivel (v1.6 o posterior), se requiere:

### Acción 1 — Obtener alpha justificado desde literatura

Alpha es actualmente un parámetro **libre y sin constricción**. Para que el
candidato sea físicamente interpretable, se necesita un valor de alpha derivado de:
- Un paper de física cuántica/gravitacional que prediga el acoplamiento.
- Un resultado experimental que constriña la escala.
- Un argumento dimensional o de simetría fundamentado.

### Acción 2 — Transicionar a benchmark `LITERATURE_EXTRACTED`

El benchmark actual es `SYNTHETIC`: generado internamente con parámetros declarados.
El próximo paso es usar datos de visibilidad de interferencia extraídos de un
experimento real publicado (e.g., Arndt, Hornberger, Zeh, etc.).

### Acción 3 — Evaluar detectabilidad source-backed

Una vez que exista un alpha justificado y datos reales:
- Computar delta contra y_true experimental.
- Calcular PredictiveGain real.
- Evaluar si el candidato mejora o empeora el baseline frente a datos.

Solo entonces podrán desbloquearse claims físicos.

---

## 10. Fuentes de los reportes

Este documento consolidó los siguientes 5 reportes generados automáticamente por la campaña v1.5:

| Reporte | Archivo |
|---|---|
| Benchmark principal | [BENCH-CAND-FC-B-NEGCTRL-001-SYNTH-001.md](file:///D:/BIOCULTOR/PHYNG/reports/benchmarks/BENCH-CAND-FC-B-NEGCTRL-001-SYNTH-001.md) |
| Benchmark del candidato | [CAND-FC-B-NEGCTRL-001_synthetic_benchmark_v1_5.md](file:///D:/BIOCULTOR/PHYNG/reports/candidates/CAND-FC-B-NEGCTRL-001_synthetic_benchmark_v1_5.md) |
| Alpha Sweep | [CAND-FC-B-NEGCTRL-001_alpha_sweep_v1_5.md](file:///D:/BIOCULTOR/PHYNG/reports/candidates/CAND-FC-B-NEGCTRL-001_alpha_sweep_v1_5.md) |
| Failure Report | [CAND-FC-B-NEGCTRL-001_failure_report_v1_5.md](file:///D:/BIOCULTOR/PHYNG/reports/prediction_pressure/CAND-FC-B-NEGCTRL-001_failure_report_v1_5.md) |
| Campaign Report | [CANDIDATE-BASELINE-SYNTHETIC-BENCHMARK-v1_5.md](file:///D:/BIOCULTOR/PHYNG/reports/campaigns/CANDIDATE-BASELINE-SYNTHETIC-BENCHMARK-v1_5.md) |

---

## Resumen ejecutivo

```
Candidato    : CAND-FC-B-NEGCTRL-001  (familia B_SUPPRESSED)
Benchmark    : BENCH-CAND-FC-B-NEGCTRL-001-SYNTH-001  (SYNTHETIC)
Campaña      : CANDIDATE-vs-BASELINE-SYNTH-v1_5

Resultado central
─────────────────
max_abs_delta          ≈ 0.000  (38 órdenes bajo el umbral)
detectability_status   UNDETECTABLE_SYNTHETIC_DELTA
alpha_min estimado     2.22×10³⁰  (ALPHA_EXTREME)
Primer alpha detectable en sweep: 10³⁵  (ALPHA_EXTREME → ALPHA_UNPHYSICAL)

Fallos disparados
─────────────────
FAIL_UNDETECTABLE_DELTA      ← delta < epsilon bajo alpha razonable
FAIL_NO_BENCHMARK            ← sin datos experimentales (y_true = None)
FAIL_NO_SOURCE_SUPPORT       ← sin referencias bibliográficas para alpha

Supervivencia del candidato
───────────────────────────
SURVIVES_AS_TOY_NEGATIVE_CONTROL

Claims físicos
──────────────
BLOQUEADOS  ← sin excepción

Próximo paso obligatorio
─────────────────────────
Obtener alpha con soporte de fuentes
Obtener datos experimentales (y_true)
Transicionar a benchmark LITERATURE_EXTRACTED
```

---

*El candidato entró al ring. No ganó por fe. Sangró números.*

*Eso es exactamente lo que debe hacer un candidato honesto.*
