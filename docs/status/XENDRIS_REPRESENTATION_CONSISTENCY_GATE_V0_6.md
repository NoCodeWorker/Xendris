# Xendris v0.6 Representation Consistency Gate Status Note

Este documento detalla el estado actual de la implementación de **Xendris v0.6 Representation Consistency Gate**.

---

## 1. Propósito y Relación con v0.4 y v0.5
* **Propósito**: Validar y asegurar la consistencia lógica entre múltiples representaciones de un mismo claim de conocimiento (provenientes de diferentes modelos, prompts, contextos o ejecuciones).
* **Relación con v0.4 y v0.5**: Se apoya en el control de contaminación local de v0.4 y las transiciones del sector epistémico de v0.5, aplicando una capa adicional de consistencia de consenso antes de admitir cualquier claim como conocimiento operativo.

---

## 2. Módulos Implementados
Se ha creado el paquete `xendris/core/representations/` compuesto por:
* **`representation.py`**: Define la clase inmutable `ClaimRepresentation`.
* **`equivalence.py`**: Define el enum `RepresentationRelation` y la clase `RepresentationComparison`.
* **`contradiction.py`**: Implementa las heurísticas lógicas para la detección de contradicciones, proxy-overgeneralizations y falta de especificación.
* **`consistency_gate.py`**: Implementa `RepresentationConsistencyDecision` y la compuerta `RepresentationConsistencyGate`, la cual compone limpiamente con `SectorTransitionEngine` y `ContaminationGuard`.
* **`representation_audit.py`**: Implementa `RepresentationAudit` para serializar y registrar deterministamente las decisiones de consenso.
* **`__init__.py`**: Exposición pública de la compuerta lógica.

---

## 3. Matriz de Relaciones de Representación

| Relación | Descripción / Regla Heurística | Decisión de la Compuerta |
| :--- | :--- | :--- |
| `EQUIVALENT` | Mismo ID, sector compatible, limitaciones compatibles, sin conflictos. | `ALLOW` |
| `PARTIALLY_EQUIVALENT` | Mismo ID, limitaciones o alcances de contexto diferentes sin contradicciones directas. | `ALLOW_WITH_LIMITATIONS` |
| `CONTRADICTORY` | Asertos opuestos (pass vs. fail, ready vs. unverified, universal vs. limited). | `BLOCK` (o `HUMAN_REVIEW` si es crítico) |
| `DISJOINT` | Claims diferentes sin solapamiento operacional ni de ID. | `ALLOW_WITH_LIMITATIONS` (sin consenso forzado) |
| `OVERGENERALIZED` | Saltos de alcance indebidos (dry-run a prod, cost a quality, controls a safety). | `BLOCK` o degradación segura |
| `UNDERSPECIFIED` | Faltan campos clave (model, provider, etc.). | `ALLOW_WITH_LIMITATIONS` |
| `EVIDENCE_MISMATCH` | Tipos de evidencias incompatibles (e.g. json vs. log). | `BLOCK` |

---

## 4. Casos Rígidos de Sobregeneralización (Overgeneralization)
Se detectan y mitigan deterministamente a través del análisis de palabras clave y campos de contexto:
1. **Proxy Costo-Calidad**: Un claim de costo no puede implicar calidad del modelo.
2. **Proxy Latencia-Exactitud**: Un claim de rapidez no puede implicar exactitud/calidad de la respuesta.
3. **Dry-Run a Producción**: Métricas simuladas no pueden promoverse a métricas de producción sin medición real.
4. **Benchmark a Superioridad Universal**: Un resultado de benchmark no puede promoverse a superioridad universal o general del modelo.
5. **Control a Seguridad Universal**: El éxito sobre controles normales de seguridad no implica seguridad universal.

---

## 5. Pruebas Añadidas
Se han añadido 16 pruebas unitarias deterministas en [test_representation_consistency_gate.py](file:///d:/BIOCULTOR/PHYNG/tests/core/test_representation_consistency_gate.py).

### Resultados de Ejecución

#### Pruebas Enfocadas
* **Comando**: `.venv\Scripts\python.exe -m pytest tests/core/test_representation_consistency_gate.py -q`
* **Resultado**: **`16 passed in 0.20s`**

#### Suite de Pruebas Completa
* **Comando**: `.venv\Scripts\python.exe -m pytest -q`
* **Resultado**: **`1315 passed, 4 warnings in 169.48s`** (suite 100% verde y libre de errores activos o esperados).

---

## 6. Limitaciones
* **Procesamiento Semántico**: Las heurísticas lógicas están basadas en concordancia de campos estructurados y palabras clave; no se utiliza procesamiento de lenguaje natural (NLP) ni LLMs para evitar varianza en las aserciones.

---

## 7. Próximo Hito Técnico Recomendado
* **Hito Objetivo**: **Xendris v0.7 Model Epistemic Fingerprint** (construcción de huellas dactilares epistémicas de modelos a partir de sus aserciones consistentes admitidas).
