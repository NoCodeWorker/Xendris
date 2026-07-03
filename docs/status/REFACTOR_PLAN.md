# Plan de Refactorización — Xendris / Frontera C

Este documento establece un plan detallado en fases para ordenar el repositorio, reducir la deuda técnica acumulada por experimentos y scripts solapados, y migrar hacia una estructura limpia y sostenible.

---

## 1. Propuesta de Estructura Limpia Objetivo

La arquitectura propuesta agrupa los componentes cognitivos y lógicos de Xendris, las validaciones de límites físicos de Frontera C, y las herramientas de validación de manera coherente:

```
xendris/
├── core/                  # Motores principales de orquestación y flujos lógicos
├── models/                # Definiciones de datos tipadas y contratos comunes
├── frontera_c/            # Reglas y validaciones físicas (Compton, interferómetros, etc.)
├── benchmarks/            # Suites de evaluación por familia de fallo
│   └── false_formality/   # Evaluador de Falsa Formalidad Matemática
├── prompts/               # System prompts e instrucciones textuales aisladas
├── outputs/               # Resultados e informes generados por ejecuciones
├── tests/                 # Suites de pruebas unitarias y de integración
└── scripts/               # Utilidades, cargadores y scripts de ejecución únicos
```

---

## 2. Plan de Refactorización por Fases

### Baseline actual verificada

* **Estado**: `BASELINE_STABLE_MINIMAL`.
* **Python**: `1070 passed, 4 warnings`.
* **Frontend**: `npm run build` correcto.
* **Lean**: bloqueado por entorno local (`lake` no está disponible en PATH).
* **Regla de seguridad**: no mover módulos históricos de `phyng/` hasta tener compatibilidad de imports, tests focalizados y rollback documentado.

### Fase 1: Aislamiento y Contratos de Seguridad
* **Objetivo**: Asegurar que ningún cambio afecte los contratos clave de Xendris.
* **Acciones**:
  * [x] Creación e integración de tests mínimos de seguridad/contratos (`test_pipeline_contract.py`, `test_scorer_contract.py`, `test_benchmark_contract.py`).
  * Verificar que todos los tests existentes pasen antes de iniciar reubicaciones.

### Fase 2: Reubicación de Componentes de Frontera C
* **Objetivo**: Consolidar las reglas y cálculos físicos dispersos en `phyng/`.
* **Acciones**:
  * Mover el núcleo físico (`claim_gatekeeper.py`, `constants.py`, `enums.py`, `errors.py`, `frontier_lengths.py`, `operational_scale.py`, `predictive_gain.py`, `signature.py`, `epistemic_trace.py`) a `xendris/frontera_c/`.
  * Adaptar los imports de manera controlada y ejecutar la suite de pruebas unitarias para validar.

### Fase 3: Consolidación de Campañas y RAG
* **Objetivo**: Limpiar los múltiples directorios correspondientes a las iteraciones v1 a v5 en `phyng/`.
* **Acciones**:
  * **Fusión (MERGE)** de módulos de extracción y procesamiento (e.g. `manual_data_extraction`, `exact_extract_review`, `pdf_text_extraction`) bajo un submódulo RAG simplificado `xendris/core/rag/`.
  * Reubicar campañas de validación históricas útiles a `xendris/core/campaigns/` o `xendris/scripts/`.

### Fase 4: Desconexión y Depreciación
* **Objetivo**: Desactivar código obsoleto.
* **Acciones**:
  * Marcar los archivos candidatos a borrar como deprecados mediante advertencias en runtime (`warnings.warn`).
  * Mantener los archivos en el repositorio durante una iteración intermedia de seguridad antes de eliminarlos físicamente.

---

## 3. Fusión de Módulos Duplicados (MERGE)

| Funcionalidad | Archivos Implicados | Propuesta |
|---|---|---|
| **Extracción y Validación de y_true** | `phyng/ytrue_extraction/`, `phyng/targeted_ytrue/`, `phyng/ytrue_acquisition_plan/` | Fusionar en `xendris/core/rag/ytrue_extractor.py`. El módulo `ytrue_extraction` es el más completo. |
| **Procesamiento de Fuentes y Descargas** | `phyng/source_download/`, `phyng/source_acquisition/`, `phyng/real_source_acquisition/` | Fusionar en `xendris/core/rag/source_manager.py`. `real_source_acquisition` posee la lógica de colas más robusta. |
| **Evaluación de Presión de Predicción** | `phyng/prediction_pressure/`, `phyng/source_pressure/`, `phyng/source_pressure_decision/` | Fusionar en `xendris/core/campaigns/pressure_evaluator.py`. |

---

## 4. Archivos Candidatos a Borrar (DELETE_CANDIDATE)

*Nota: Estos archivos no se eliminarán en esta fase de auditoría. Se conservan intactos y solo se propone su eliminación para la Fase 4.*

1. **`phyng/baselines/`** (Experimentos iniciales redundantes tras la consolidación de modelos en `xendris/benchmarks/`).
2. **`phyng/closed_loop/`** (Código de sandbox inicial solapado con el runner actual del benchmark de Xendris).
3. **`phyng/closed_loop_meta_improvement_campaign_v2_4.py`** (Script de iteración único obsoleto).
4. **`phyng/synthetic_benchmark_design/`** (Diseños de pruebas simuladas reemplazados por `false_formality/cases.json`).
5. **`phyng/copilot/`** (Prototipos de chat intermedio de consola redundantes tras la unificación con la UI de Xendris).
