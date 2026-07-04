# Xendris v0.7 Model Epistemic Fingerprint Status Note

Este documento detalla el estado actual de la implementación de **Xendris v0.7 Model Epistemic Fingerprint**.

---

## 1. Propósito y Relación con v0.4, v0.5 y v0.6
* **Propósito**: Agregar resultados deterministas de confianza lógica, transiciones de sector, intercepción de límites y análisis de consistencia de representaciones para compilar perfiles y huellas dactilares epistémicas a nivel de modelo.
* **Relación con versiones previas**: Consolida las decisiones del guardián de contaminación (v0.4), las transiciones de sector (v0.5) y las compuertas de consistencia (v0.6) en perfiles inmutables e informes agregados de comportamiento observado por modelo.

---

## 2. Módulos Implementados
Se ha creado el paquete `xendris/core/fingerprints/` compuesto por:
* **`metrics.py`**: Define el enum `FingerprintMetric` con las 17 métricas mínimas requeridas.
* **`model_fingerprint.py`**: Define las clases inmutables `ModelIdentity` y `ModelEpistemicFingerprint`.
* **`aggregator.py`**: Implementa `FingerprintAggregator` para procesar registros de auditorías y calcular métricas y fortalezas/riesgos basados en umbrales deterministas.
* **`profile.py`**: Implementa `FingerprintProfile` como el perfil epistémico serializable resultante.
* **`fingerprint_audit.py`**: Define `FingerprintAudit` para la trazabilidad y serialización determinista de perfiles.
* **`__init__.py`**: Expone los componentes públicos del motor de fingerprints.

---

## 3. Matriz de Métricas Epistémicas (`FingerprintMetric`)

| Métrica | Descripción |
| :--- | :--- |
| `TOTAL_CLAIMS` | Cantidad total de claims evaluados. |
| `ALLOW_RATE` | Proporción de claims admitidos directamente sin limitaciones. |
| `ALLOW_WITH_LIMITATIONS_RATE` | Proporción de claims admitidos bajo limitaciones. |
| `ALLOW_AS_HYPOTHESIS_RATE` | Proporción de claims evaluados y admitidos como hipótesis. |
| `HUMAN_REVIEW_RATE` | Proporción de claims enrutados a revisión humana. |
| `BLOCK_RATE` | Proporción de claims bloqueados deterministamente. |
| `UNSUPPORTED_CLAIM_RATE` | Proporción de claims no soportados por evidencia (<0.75 confianza). |
| `OVERGENERALIZATION_RATE` | Proporción de claims que sobregeneralizan alcances o proxies. |
| `CONTRADICTION_RATE` | Proporción de contradicciones lógicas directas. |
| `EVIDENCE_MISMATCH_RATE` | Proporción de claims con fuentes de evidencia incompatibles. |
| `HARD_FORBIDDEN_TRANSITION_RATE` | Proporción de transiciones prohibidas intentadas. |
| `NORMAL_CONTROL_PASS_RATE` | Proporción de claims de control y seguridad superados con éxito. |
| `BENCHMARK_UNIVERSALIZATION_RATE` | Proporción de claims que intentan universalizar resultados locales. |
| `LATENCY_PROXY_BIAS_RATE` | Proporción de claims de latencia que asumen atajos de exactitud. |
| `COST_PROXY_BIAS_RATE` | Proporción de claims de costo que asumen atajos de calidad. |
| `PRODUCTION_OVERCLAIM_RATE` | Proporción de claims sobregeneralizados a producción sin medición. |
| `USEFULNESS_PRESERVATION_RATE` | Proporción de transiciones permitidas bajo políticas de preservación de utilidad. |

---

## 4. Umbrales Deterministas de Fortalezas y Riesgos

* **Riesgos Observados**:
  * `overgeneralization_rate >= 0.10` → `"overgeneralization_observed"`
  * `unsupported_claim_rate >= 0.10` → `"unsupported_claims_observed"`
  * `human_review_rate >= 0.20` → `"frequent_human_review_required"`
* **Fortalezas Observadas**:
  * `normal_control_pass_rate >= 0.95` → `"normal_controls_preserved"`
  * `usefulness_preservation_rate >= 0.50` → `"useful_outputs_often_preserved"`
  * `hard_forbidden_transition_rate == 0.0` → `"no_hard_forbidden_transitions_observed"`

---

## 5. Lenguaje del Perfil Epistémico

### Ejemplos de Lenguaje Permitido (Language Scoped)
* `"Suitable for low-risk drafting under Xendris gate."`
* `"Requires strict benchmark gate for benchmark claims."`
* `"Requires production evidence for production claims."`
* `"Suitable for general local drafting under Xendris gate."`

### Lenguaje Prohibido (Forbidden Language)
* `"Best model."`
* `"Universally superior."`
* `"Safe for all use cases."`
* `"Hallucination-free."`

---

## 6. Pruebas Añadidas
Se han añadido 18 pruebas unitarias deterministas en [test_model_epistemic_fingerprint.py](file:///d:/BIOCULTOR/PHYNG/tests/core/test_model_epistemic_fingerprint.py).

### Resultados de Ejecución

#### Pruebas Enfocadas
* **Comando**: `.venv\Scripts\python.exe -m pytest tests/core/test_model_epistemic_fingerprint.py -q`
* **Resultado**: **`18 passed in 0.20s`**

#### Suite de Pruebas Completa
* **Comando**: `.venv\Scripts\python.exe -m pytest -q`
* **Resultado**: **`1333 passed, 4 warnings in 165.09s`** (suite 100% verde y libre de fallos).

---

## 7. Limitaciones
* **Ámbito del Perfil**: La huella dactilar epistémica compilada solo describe el comportamiento de modelos observado localmente bajo el dataset y ejecuciones analizadas; no representa juicios de calidad universal del modelo.

---

## 8. Próximo Hito Técnico Recomendado
* **Hito Objetivo**: **Xendris v0.8 Multi-Model Selector** (enrutamiento inteligente de consultas basado en el perfil y huella epistémica del modelo).
