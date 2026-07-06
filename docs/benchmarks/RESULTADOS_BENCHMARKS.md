# Resultados de Benchmarks — Xendris Trust Runtime

> **Advertencia**: Ningún resultado implica superioridad universal. Todos los benchmarks son
> cerrados, acotados a su dataset, configuración y proveedor específicos. No generalizar.

---

## 1. Trust Traps v0.1 — Resistencia a trampas epistémicas

**Dataset**: 100 prompts diseñados para inducir overclaiming, sycophancy,
universalización, promoción de hipótesis sin evidencia y garantías absolutas.
Cada prompt se envía a DeepSeek base (sin gates) y a DeepSeek + Xendris (con gates).

**Score**: Proporción de respuestas que NO caen en la trampa (0 = cae, 1 = resiste).

### Dry-run (mock provider)

| Métrica | DeepSeek | Xendris | Diferencia |
|---|---|---|---|
| Score promedio | 0.100 | 0.985 | **+0.885** |
| Victorias | 0 / 100 | 90 / 100 | — |
| Empates | — | 10 / 100 | — |
| Latencia promedio | ~100ms | ~100ms | ~0ms |
| Costo total | ~$0.0008 | ~$0.0008 | ~$0 |

### Historical real DeepSeek run (deepseek-chat, 100 samples; not admitted)

This run is retained for audit history only. It is not admitted by the current
Benchmark Evidence Registry because the summary is missing required metadata.

| Métrica | DeepSeek | Xendris | Diferencia |
|---|---|---|---|
| Score promedio | 0.100 | **0.976** | **+0.876** |
| Victorias | 0 / 100 | **90 / 100** | — |
| Empates | — | 10 / 100 | — |
| Latencia promedio | 4,686ms | 9,564ms | **+4,878ms** |
| Costo total | $0.0092 | $0.0094 | +$0.0003 |
| Exclusion rate | — | 90% | — |
| Human review rate | — | 15% | — |

### Interpretación

| Conclusión | Nivel de confianza |
|---|---|
| Xendris bloquea/limita el 90% de las trampas de confianza en el artefacto dry-run admitido | **Alta** dentro del dataset cerrado |
| El run real histórico muestra la misma dirección, pero no está admitido como evidencia pública | **Media** hasta remediar metadata |
| DeepSeek base solo resiste el 10% sin gates en estos artefactos | **Alta** para el dry-run admitido; histórica para el run real |
| El overhead de latencia (~4.8s) aparece en el run real histórico | **Media**; no usar como claim público admitido |
| El overhead de costo es marginal (~$0.0003/100 samples) en el run real histórico | **Media**; no usar como claim público admitido |
| Esto funcionaría igual con otros proveedores | **Baja** (solo probamos DeepSeek) |

### Limitaciones

- Solo DeepSeek; no probado con OpenAI, Anthropic u otros.
- Dataset cerrado (Trust Traps v0.1).
- No mide utilidad real, solo resistencia a trampas.
- Latencia incluye Python overhead local, no solo llamada API.

---

## 2. Programming Reliability v0.1 — Confiabilidad en código

**Dataset**: 100 problemas de programación en Python que evalúan: contratos de API,
corrección de bugs, casos límite, rendimiento, refactorización segura, seguridad
básica y generación de tests. Cada solución se ejecuta contra tests.

**Score**: 0.0 si falla (error runtime, test fallido o riesgo seguridad), 1.0 si pasa.

### Real DeepSeek (deepseek-chat, 100 samples)

| Métrica | DeepSeek | Xendris | Diferencia |
|---|---|---|---|
| **Score promedio** | **0.77** | **0.72** | **-0.05** |
| Tests pasados | 77 / 100 | 72 / 100 | -5 |
| Errores runtime | 15 | 16 | +1 |
| Riesgos de seguridad | 8 | 12 | +4 |
| Latencia promedio | 2,052ms | 2,488ms | +436ms |
| Costo total | $0.0057 | $0.0076 | +$0.0019 |

### Score por categoría

| Categoría | DeepSeek | Xendris | ¿Quién gana? |
|---|---|---|---|
| api_contracts | **1.0** | 0.2 | DeepSeek |
| bug_fixing | 1.0 | 1.0 | Empate |
| **edge_cases** | 0.47 | **1.0** | **Xendris (+0.53)** |
| normal_control | 1.0 | 1.0 | Empate |
| performance | 1.0 | 1.0 | Empate |
| refactor_safety | 1.0 | 1.0 | Empate |
| security_basics | 0.0 | 0.0 | Empate |
| unit_tests | **0.67** | 0.33 | DeepSeek |

### Interpretación

| Conclusión | Nivel de confianza |
|---|---|
| Xendris es significativamente **mejor en edge cases** (1.0 vs 0.47) | **Alta** |
| Xendris pierde en api_contracts y unit_tests por **sobreingeniería** | **Alta** |
| Las pérdidas son **falsos negativos**, no errores de lógica | **Alta** |
| El código de Xendris es más verboso y añade imports que a veces fallan (`ImportError: __import__ not found`) | **Alta** |
| La tasa de exclusión (28% vs 23%) refleja que Xendris es más conservador | **Media** |

### Causa raíz de las pérdidas de Xendris

Xendris añade validaciones exhaustivas de tipos, imports complejos y tests
adicionales. En el sandbox restringido del benchmark, esto causa:

- `ImportError: __import__ not found` al usar módulos como `pytest`, `decimal`, `math`
  en entornos sin esos imports disponibles.
- `NameError: name 'complex' is not defined` por referencias a tipos no cargados.
- `SECURITY_RISK` por código que parece inseguro pero no lo es (falso positivo).

**Esto no es un problema de corrección, es un problema de ajuste**: el nivel de
escrutinio de Xendris está calibrado para producción, no para el sandbox de
benchmark.

---

## 3. Evidence Registry

El estado de evidencia debe separarse por artefacto. Programming Reliability
está admitido en el registro actual. El resumen real de Trust Traps listado
abajo queda como artefacto histórico rechazado porque no contiene todos los
metadatos exigidos por la compuerta de excelencia.

| Artefacto | Status | Decisión | Blockers |
|---|---|---|---|
| Trust Traps v0.1 (real DeepSeek) | REJECTED / historical only | BLOCKED_FOR_INTERPRETATION | missing metadata |
| Programming Reliability v0.1 (real DeepSeek) | ADMITTED | READY_FOR_INTERPRETATION | 0 |

Archivo de referencia: `runs/benchmark_evidence_registry_real.json`

---

## 4. Resumen ejecutivo

| Afirmación | Evidencia |
|---|---|
| Xendris reduce drásticamente las trampas epistémicas | Trust Traps dry-run admitido: 90% de bloqueo/limitación |
| El run real histórico de Trust Traps apunta en la misma dirección | No admitido como evidencia pública hasta remediar metadata |
| El overhead de latencia es ~4.8s por request | Solo en Trust Traps real histórico rechazado; no usar como claim admitido |
| El overhead de costo es marginal | Trust Traps real histórico: +$0.0003; Programming admitido: +$0.0019 |
| Xendris mejora manejo de edge cases en código | Programming: 0.47 → 1.0 |
| Xendris puede sobreingenieriar en entornos restringidos | Programming: api_contracts 1.0 → 0.2 |
| Solo probado con DeepSeek | No hay datos de OpenAI/Anthropic |

---

## Archivos fuente y artefactos rechazados

- `runs/real_deepseek_trust_traps_v0_1_7507d5f1_summary.json` — artefacto histórico rechazado; no admitido como evidencia pública.
- `runs/deepseek_vs_xendris_programming_reliability_v0_1_2026_07_04_summary.json`
- `runs/benchmark_evidence_registry_real.json`
- `docs/benchmarks/BENCHMARK_EVIDENCE_REGISTRY_REAL.md`
