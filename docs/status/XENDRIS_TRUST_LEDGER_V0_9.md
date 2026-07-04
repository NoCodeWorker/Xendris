# Xendris v0.9 Trust Ledger Status Note

Este documento detalla el estado actual de la implementación de **Xendris v0.9 Trust Ledger**.

---

## 1. Propósito y Relación con v0.4, v0.5, v0.6, v0.7 y v0.8
* **Propósito**: Proporcionar registros de confianza deterministas, de solo anexión (append-only) y serializables para todas las decisiones principales de Xendris.
* **Relación con versiones previas**: Registra y audita las decisiones de límites de claim (v0.4), transiciones de sector (v0.5), consenso de representaciones (v0.6), huellas dactilares epistémicas (v0.7) y decisiones de enrutamiento multi-modelo (v0.8).

---

## 2. Módulos Implementados
Se ha creado el paquete `xendris/core/ledger/` compuesto por:
* **`event_type.py`**: Define el enum `TrustEventType` con los 14 tipos de eventos principales.
* **`record.py`**: Estructura inmutable `TrustLedgerRecord` con serialización JSON canónica y hashing determinista.
* **`writer.py`**: Implementa `TrustLedgerWriter` para anexar eventos y persistirlos en formato JSONL.
* **`reader.py`**: Implementa `TrustLedgerReader` para realizar consultas y filtros sobre los registros.
* **`export.py`**: Implementa `TrustLedgerExporter` para exportar a formatos JSON, JSONL y Markdown Summary.
* **`hashchain.py`**: Implementa `TrustHashChain` para enlazar hashes y verificar la integridad de la cadena.
* **`ledger_audit.py`**: Consolida auditorías de corrida agregadas a través de `LedgerAudit`.
* **`__init__.py`**: Expone las interfaces públicas y proporciona funciones adaptadoras ligeras.

---

## 3. Matriz de Eventos de Confianza (`TrustEventType`)

| Evento | Descripción |
| :--- | :--- |
| `CLAIM_BOUNDARY_DECISION` | Decisión de intercepción de contaminación en contexto local. |
| `SECTOR_TRANSITION_DECISION` | Decisión de transición entre sectores epistémicos. |
| `REPRESENTATION_CONSISTENCY_DECISION` | Consenso y validación de consistencia entre representaciones. |
| `MODEL_FINGERPRINT_SUMMARY` | Registro del fingerprint epistémico observado en un modelo. |
| `ROUTING_DECISION` | Decisión de enrutamiento multi-modelo para una solicitud. |
| `EVIDENCE_BRIDGE_USED` | Uso de un puente de evidencia para elevar la confianza. |
| `HUMAN_REVIEW_ROUTED` | Enrutamiento a revisión manual de un claim crítico o no seguro. |
| `CLAIM_BLOCKED` | Bloqueo explícito de un claim no seguro. |
| `CLAIM_ALLOWED_WITH_LIMITATIONS` | Claim permitido con restricciones operacionales o compuertas. |
| `CLAIM_ALLOWED_AS_HYPOTHESIS` | Claim permitido únicamente dentro del sector de hipótesis. |
| `MODEL_SELECTED` | Selección exitosa de un modelo compatible. |
| `MODEL_REJECTED` | Descarte de un modelo por no ser apto o superar límites. |
| `COST_ESTIMATE_RECORDED` | Registro de estimación de costos asociados a la solicitud. |
| `LATENCY_ESTIMATE_RECORDED` | Registro de estimación de latencia esperada en milisegundos. |

---

## 4. Estructura del Registro (`TrustLedgerRecord`)
* `record_id`: Identificador único del registro.
* `run_id`: Identificador de la corrida/ejecución.
* `event_type`: El enum `TrustEventType`.
* `sequence_index`: Índice incremental determinista.
* `source_component`: Componente que originó la decisión.
* `claim_id` / `model_id` / `provider`: Identificadores opcionales asociados.
* `decision` / `reason` / `risk_level`: Información lógica de la auditoría.
* `limitations` / `evidence_refs`: Restricciones y referencias.
* `input_hash` / `output_hash`: Hashes de entrada/salida para estabilidad de contenido.
* `previous_record_hash`: Enlace al hash del registro anterior en la cadena.
* `record_hash`: SHA-256 hex del contenido del registro.

---

## 5. Local Deterministic Hash Chain
* **Funcionamiento**: Cada registro calcula su `record_hash` basándose en todos sus campos de contenido y en el `previous_record_hash`.
* **Verificación**: `TrustHashChain.verify_chain(records)` valida secuencialmente que no existan alteraciones en los hashes ni rupturas en los enlaces de la cadena.
* **Declaración de Inmutabilidad Limitada**: El ledger no reclama inmutabilidad de cadena de bloques (blockchain) distribuida o criptográfica global. Se trata de un mecanismo local determinista de detección de alteraciones (hash chain) que opera estrictamente en memoria y almacenamiento local de anexión.

---

## 6. Pruebas Añadidas
Se agregaron 20 pruebas unitarias deterministas en `tests/core/test_trust_ledger.py`.

### Resultados de Ejecución

#### Pruebas Enfocadas
* **Comando**: `.venv\Scripts\python.exe -m pytest tests/core/test_trust_ledger.py -q`
* **Resultado**: **`20 passed in 0.18s`**

#### Suite de Pruebas Completa
* **Comando**: `.venv\Scripts\python.exe -m pytest -q`
* **Resultado**: **`1373 passed, 4 warnings in 181.25s`**

---

## 7. Limitaciones
* **Integridad Física**: Al ser un archivo local (`.jsonl`), no previene la manipulación directa por parte de un usuario con permisos de escritura en el sistema de archivos, sino que detecta discrepancias en los hashes durante la lectura o auditoría.

---

## 8. Próximo Hito Técnico Recomendado
* **Hito Objetivo**: **Xendris v1.0 Agentic Trust Runtime** (orquestación completa en tiempo de ejecución del agente con todas las compuertas lógicas y auditoría integrada).
