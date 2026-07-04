# Xendris v0.4 Local Claim Algebras Status Note

Este documento detalla el estado actual de la implementación de **Xendris v0.4 Local Claim Algebras**.

---

## 1. Módulos Implementados
Se han creado e integrado de manera limpia y determinista los siguientes tres paquetes de gobernanza:
* **`xendris/core/algebra/`**:
  * `claim_object.py` (define la clase inmutable `ClaimObject` como unidad formal y auditable de aserción).
* **`xendris/core/local/`**:
  * `context.py` (define el enum `LocalContext` con los 10 dominios operativos locales).
  * `local_algebra.py` (define `TransitionRule` y `LocalClaimAlgebra`).
* **`xendris/core/boundary/`**:
  * `evidence_bridge.py` (define `EvidenceBridge` y `EvidenceBridgeType`).
  * `contamination_guard.py` (implementa `ContaminationGuard` y `UsefulnessPreservationPolicy` con el flujo de evaluación completo).

---

## 2. Decisiones Soportadas
La compuerta lógica y la política de preservación admiten las siguientes decisiones operativas de frontera:
* `ALLOW`
* `ALLOW_WITH_LIMITATIONS`
* `ALLOW_AS_HYPOTHESIS`
* `HUMAN_REVIEW`
* `BLOCK`

---

## 3. Transiciones Prohibidas Rígidas (Hard Forbidden)
Se garantiza el bloqueo determinista del paso de claims en los siguientes casos:
1. `BENCHMARK -> UNIVERSAL_SUPERIORITY`
2. `BENCHMARK -> GENERAL_MODEL_QUALITY` (sin validación externa)
3. `LATENCY -> ACCURACY`
4. `USER_PROVIDED -> VERIFIED` (sin puente de evidencia)
5. `CODE_STATE -> PRODUCTION_READY` (sin compilación/pruebas de despliegue)
6. `DRY_RUN_LATENCY -> PRODUCTION_LATENCY`
7. `NORMAL_CONTROL -> UNIVERSAL_SAFETY`

---

## 4. Política de Preservación de Utilidad (Usefulness Preservation Policy)
El motor de preservación implementa las siguientes transformaciones anti-sobrebloqueo:
* **Claims Exploratorios**: Se degradan a `ALLOW_AS_HYPOTHESIS` con acotaciones específicas de exploración.
* **Contenido Creativo o de Brainstorming**: Se admite (`ALLOW`) sin obstrucciones lógicas, excepto en presencia de aserciones de alto riesgo sin soporte.
* **Aserciones sobremedidas (v.g. Hallucinación/Superioridad)**: Se reescriben/acotan automáticamente a `ALLOW_WITH_LIMITATIONS` con los límites definidos en la especificación en lugar de ser bloqueadas ciegamente.

---

## 5. Remoción de Decoradores xfail
Las especificaciones futuras marcadas previamente como esperadas a fallar en la versión v0.4.6 han sido completadas:
* Se removió el decorador `xfail` de `test_10_normal_control_success_cannot_become_universal_safety` (resuelto reordenando la prioridad de la regla de control).
* Se removió el decorador `xfail` de `test_12_human_review_bridges_handling` (resuelto aislando el puente de auditoría humana de la regla de validez general de puentes).

---

## 6. Resultados de Pruebas Observados

### Pruebas Enfocadas
* **Comando**: `.venv\Scripts\python.exe -m pytest tests/core/test_local_claim_algebras.py -q`
* **Resultado**: `24 passed in 0.18s` (las 12 especificaciones originales más los 12 tests agregados para validación de la preservación de utilidad y anti-sobrebloqueo).

### Pruebas de la Suite Completa
* **Comando**: `.venv\Scripts\python.exe -m pytest -q`
* **Resultado**: `1283 passed, 4 warnings in 166.48s` (cero errores activos, cero fallos esperados).

---

## 7. Limitaciones
* **Validación Multi-Modelo**: El comportamiento del guard de contaminación no ha sido evaluado en entornos de concurrencia y producción real con múltiples proveedores activos simultáneamente.
* **Trazabilidad de Ledger**: El registro detallado de las decisiones del guard en la base de datos distribuida o ledger persistente está pendiente de automatización.

---

## 8. Próximo Hito Técnico
* **Hito Objetivo**: **Xendris v0.5 Sector Transition Engine** (formalización del motor de transición de sectores lógicos complejos).
