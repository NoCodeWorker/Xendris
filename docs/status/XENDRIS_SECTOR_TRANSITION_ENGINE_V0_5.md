# Xendris v0.5 Sector Transition Engine Status Note

Este documento detalla el estado actual de la implementación de **Xendris v0.5 Sector Transition Engine**.

---

## 1. Propósito y Relación con la v0.4
* **Propósito**: Formalizar y regular de manera robusta y determinista cómo los claims se promueven, degradan o limitan a través de diferentes sectores epistémicos (`EpistemicSector`).
* **Relación con la v0.4**: Mientras que la v0.4 previene la contaminación de contextos locales (`LocalContext`), la v0.5 añade gobernanza epistémica de alto nivel (por ejemplo, impidiendo que una hipótesis se publique en producción o que un resultado de benchmark se declare como superioridad universal).

---

## 2. Módulos Implementados
Se ha creado el paquete `xendris/core/sectors/` conteniendo:
* **`sector.py`**: Define el enum `EpistemicSector` con los 16 sectores requeridos.
* **`transition.py`**: Define la clase inmutable de transporte `SectorTransition`.
* **`transition_policy.py`**: Define `SectorTransitionDecision` y la lógica de reglas y políticas de `SectorTransitionPolicy`.
* **`transition_engine.py`**: Implementa `SectorTransitionEngine`, el cual integra las políticas del sector y compone limpiamente con `ContaminationGuard` de v0.4.
* **`sector_audit.py`**: Implementa `SectorAudit` para la generación determinista y serializable de registros de auditoría.
* **`__init__.py`**: Expone las abstracciones públicas para todo el kernel.

---

## 3. Matriz de Transiciones y Reglas Rígidas (Hard Forbidden)

| Sector Origen | Sector Destino | Evidencia Requerida / Regla | Decisión Inicial |
| :--- | :--- | :--- | :--- |
| `USER_PROVIDED` | `FACTUAL` / `POLICY` | Requiere `SOURCE_CITATION`, `TEST_RESULT` o `HUMAN_REVIEW` | `BLOCK` (si no hay) |
| `HYPOTHESIS` | `FACTUAL` | Requiere puente de evidencia factual | `BLOCK` (si no hay) |
| `HYPOTHESIS` | `PRODUCTION` | Requiere `DEPLOYMENT_LOG` o `RUNTIME_TRACE` | `BLOCK` (si no hay) |
| `BENCHMARK` | (Universal Superiority) | Bloqueo absoluto si declara superioridad general | `BLOCK` |
| `BENCHMARK` | `POLICY` | Requiere validación externa | `BLOCK` (si no hay) |
| `LATENCY` | `FACTUAL` / `POLICY` | Prohibido alegar exactitud (`LATENCY -> ACCURACY`) | `BLOCK` |
| `COST` | `FACTUAL` / `POLICY` | Prohibido alegar calidad (`COST -> QUALITY`) | `BLOCK` |
| `CODE_STATE` | `PRODUCTION` | Requiere `TEST_RESULT`, `BUILD_RESULT` o `DEPLOYMENT_LOG` | `BLOCK` (si no hay) |
| `RUNTIME` | `PRODUCTION` | Requiere prueba real de despliegue | `BLOCK` (si no hay) |
| `NORMAL_CONTROL`| `POLICY` | Prohibido alegar seguridad general (`NORMAL_CONTROL -> UNIVERSAL_SAFETY`)| `BLOCK` |
| `CREATIVE` | `FACTUAL` | Requiere evidencia factual | `BLOCK` (si no hay) |
| `EXPLANATORY` | `POLICY` | Requiere evidencia factual | `BLOCK` (si no hay) |

---

## 4. Transiciones Permitidas y Acotadas (Allowed / Limited)
* **`USER_PROVIDED -> HYPOTHESIS`**: Permitido como `ALLOW_AS_HYPOTHESIS` si es especulación explícita.
* **`HYPOTHESIS -> HYPOTHESIS`**: Permitido como `ALLOW_AS_HYPOTHESIS` sin aserción factual.
* **`INFERRED -> HYPOTHESIS`**: Permitido como `ALLOW_AS_HYPOTHESIS` si la evidencia es insuficiente.
* **`CALCULATED -> FACTUAL`**: Permitido con puente determinista (`TEST_RESULT`, `BENCHMARK_ARTIFACT`).
* **`CODE_STATE -> CODE_STATE`**: Permitido con tests o build éxitoso (`ALLOW`).
* **`BENCHMARK -> BENCHMARK`**: Admitido con limitaciones específicas del dataset (`ALLOW_WITH_LIMITATIONS`).
* **`LATENCY -> LATENCY`**: Admitido con limitaciones de entorno simulado/dry-run (`ALLOW_WITH_LIMITATIONS`).
* **`HUMAN_REVIEW -> FACTUAL`**: Admitido si cuenta con aprobación humana explícita.
* **`HUMAN_REVIEW -> POLICY`**: Admitido con limitaciones si existen incertidumbres no resueltas.

---

## 5. Pruebas Añadidas
Se ha creado el archivo de pruebas en [test_sector_transition_engine.py](file:///d:/BIOCULTOR/PHYNG/tests/core/test_sector_transition_engine.py) validando de forma determinista los 16 casos de comportamiento requeridos.

### Resultados de Ejecución

#### Pruebas Enfocadas
* **Comando**: `.venv\Scripts\python.exe -m pytest tests/core/test_sector_transition_engine.py -q`
* **Resultado**: **`16 passed in 0.18s`**

#### Suite de Pruebas Completa
* **Comando**: `.venv\Scripts\python.exe -m pytest -q`
* **Resultado**: **`1299 passed, 4 warnings in 167.07s`** (todas las pruebas del kernel pasan al 100% de forma exitosa).

---

## 6. Limitaciones
* **Integración RAG/Phyng**: Las transiciones del sector no están vinculadas directamente al pipeline activo del RAG para filtrar queries en tiempo real.
* **Persistencia**: La serialización de `SectorAudit` se realiza en memoria; la persistencia física en un backend o ledger no está contemplada en este hito.

---

## 7. Próximo Hito Técnico Recomendado
* **Hito Objetivo**: **Xendris v0.6 Representation Consistency Gate** (formalización y validación de la consistencia lógica de las representaciones y claims antes de su almacenamiento epistémico).
