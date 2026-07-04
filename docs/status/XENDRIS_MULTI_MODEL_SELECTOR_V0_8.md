# Xendris v0.8 Multi-Model Selector Status Note

Este documento detalla el estado actual de la implementación de **Xendris v0.8 Multi-Model Selector**.

---

## 1. Propósito y Relación con v0.4, v0.5, v0.6 y v0.7
* **Propósito**: Enrutar solicitudes lógicas a los modelos disponibles en base a restricciones de contexto local, sector epistémico, capacidades requeridas (tools, code, json, etc.), nivel de riesgo y perfiles epistémicos compilados (fingerprints).
* **Relación con versiones previas**: Aprovecha las alertas de límites (v0.4), las transiciones seguras de sector (v0.5), el consenso de múltiples representaciones (v0.6) y los perfiles e históricos de comportamiento compilados en huellas dactilares epistémicas (v0.7) para guiar la asignación de modelos sin incurrir en atajos no seguros.

---

## 2. Módulos Implementados
Se ha creado el paquete `xendris/core/router/` compuesto por:
* **`model_registry.py`**: Define `ModelCapabilityProfile` y la clase `ModelRegistry` para el registro determinista de capacidades.
* **`route_request.py`**: Define `RouteRequest` y `RouteDecision` para modelar entradas y decisiones de enrutamiento.
* **`cost_policy.py`**: Implementa la estimación de costos por token y bandas de costos (`LOW`, `MEDIUM`, `HIGH`).
* **`risk_policy.py`**: Implementa la evaluación de compatibilidad de riesgo, exclusión de contextos y adición dinámica de compuertas requeridas.
* **`routing_policy.py`**: Paquete integrador de las políticas anteriores.
* **`selector.py`**: Implementa `MultiModelSelector` con lógica de enrutamiento por tipo de claim, filtros de seguridad e históricos de fingerprints, y desempates ordenados.
* **`router_audit.py`**: Define `RouterAudit` para registrar y serializar decisiones deterministas de enrutamiento.
* **`__init__.py`**: Expone las interfaces públicas del selector.

---

## 3. Matriz de Decisiones de Enrutamiento (`RouteDecision`)

| Decisión | Criterio de Selección | Acción Requerida / Compuertas |
| :--- | :--- | :--- |
| `SELECT` | Modelo apto, dentro del límite de riesgo y capacidades, sin compuertas adicionales. | Gates por defecto del modelo. |
| `SELECT_WITH_LIMITATIONS` | Modelo apto, pero requiere compuertas de seguridad adicionales (e.g. `Strict Safety Fence` o `Benchmark Gate`). | Compuertas agregadas dinámicamente. |
| `REQUIRE_STRONGER_MODEL` | Ningún modelo del nivel de riesgo solicitado es apto, requiriendo un modelo más capaz. | Escalar a modelo con mayor límite de riesgo. |
| `REQUIRE_HUMAN_REVIEW` | Solicitud de alto riesgo/crítica donde ningún modelo cumple con las huellas epistémicas seguras. | Enrutar a revisión manual. |
| `NO_SAFE_MODEL_AVAILABLE` | No existen modelos registrados que soporten la combinación de capacidades y riesgo. | Bloqueo preventivo de la solicitud. |
| `BLOCK` | Violación explícita de políticas operativas de enrutamiento. | Bloqueo determinista de la ejecución. |

---

## 4. Políticas Fundamentales y Reglas de Descarte

### Cost Policy (Política de Costos)
* Estima el costo combinando entrada y salida (`cost_per_1k_tokens`).
* **Regra de Oro**: El costo nunca se utiliza como proxy de calidad o exactitud. Solo influye en la selección entre modelos que ya han sido clasificados como seguros. Si se prefiere bajo costo, se selecciona el modelo seguro de menor costo, no el de menor costo absoluto.

### Risk Policy (Política de Riesgo)
* Filtra modelos cuyo `max_risk_level` sea inferior al riesgo de la solicitud.
* Asigna compuertas obligatorias: `Benchmark Gate` para claims de benchmark y `Production Evidence Gate` para claims de producción.

### Fingerprint-Aware Routing (Enrutamiento por Huella Epistémica)
* **Benchmark Claims**: Descarta modelos con tasa de universalización/sobregeneralización `>= 0.10`.
* **Production/Code Claims**: Descarta modelos con tasa de sobregeneralización a producción `>= 0.10`.
* **High-Risk Factual Claims**: Descarta modelos con tasa de claims no soportados o contradicciones `>= 0.10`.

### Atajos Prohibidos (Forbidden Shortcuts)
* Seleccionar un modelo únicamente por costo (ignorar el riesgo).
* Seleccionar un modelo únicamente por latencia (ignorar la seguridad).
* Utilizar latencia como proxy de exactitud semántica.

---

## 5. Pruebas Añadidas
Se han añadido 20 pruebas unitarias deterministas en [test_multi_model_selector.py](file:///d:/BIOCULTOR/PHYNG/tests/core/test_multi_model_selector.py).

### Resultados de Ejecución

#### Pruebas Enfocadas
* **Comando**: `.venv\Scripts\python.exe -m pytest tests/core/test_multi_model_selector.py -q`
* **Resultado**: **`20 passed in 0.21s`**

#### Suite de Pruebas Completa
* **Comando**: `.venv\Scripts\python.exe -m pytest -q`
* **Resultado**: **`1353 passed, 4 warnings in 177.68s`** (suite 100% verde y libre de fallos).

---

## 6. Limitaciones
* **Asignación de Capacidades**: Las capacidades y límites de riesgo son mapeados estáticamente en perfiles y huellas observadas; cambios dinámicos en los proveedores de base no se actualizan automáticamente en el registro sin una re-evaluación del fingerprint.

---

## 7. Próximo Hito Técnico Recomendado
* **Hito Objetivo**: **Xendris v0.9 Trust Ledger** (registro y trazabilidad distribuida e inmutable de auditorías y decisiones de enrutamiento y consenso).
