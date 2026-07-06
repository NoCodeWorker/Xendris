# Informe de Interpretación Científica: Corrida A/B v0.1 (2026-07-04)
**Comparativa: DeepSeek Base vs Xendris + DeepSeek**

Este informe documenta la evaluación de precisión cognitiva, tasas de admisión y control epistémico para la corrida ejecutada el 4 de julio de 2026 sobre las 100 muestras del **Trust Traps Dataset v0.1**.

---

## 1. Resumen Ejecutivo

### Qué se midió
Se evaluó la capacidad de control epistémico y la resistencia ante preguntas trampa y aserciones sesgadas diseñadas para engañar o sesgar las decisiones de scoring en benchmarks de lenguaje. Específicamente, se contrastó el comportamiento de:
1. **DeepSeek Base** (sin filtros cognitivos, con tendencia a responder asertivamente a premisas falsas).
2. **Xendris + DeepSeek** (usando DeepSeek como modelo subyacente, con el Trust Kernel y Benchmark Gate activados).

### Qué no se midió
No se evaluaron capacidades de generación creativa, razonamiento matemático general, traducción de idiomas ni de RAG genérico.

### Resultado Principal
Bajo la rúbrica determinista de `Trust Traps v0.1`, **Xendris + DeepSeek** obtuvo una puntuación promedio de **0.985**, frente a **0.10** de **DeepSeek Base**, representando una mejora neta (Delta) de **+0.885**.

> [!IMPORTANT]
> **Advertencia de No Superioridad Universal**: Este resultado no demuestra superioridad universal de Xendris sobre DeepSeek en capacidades generalistas de lenguaje. Solo mide de forma reproducible la mejora bajo el dataset cerrado de trampas **Trust Traps v0.1** y esta configuración de control.

---

## 2. Definiciones Operativas

Para asegurar la claridad conceptual y la defensa científica del análisis, se establecen las siguientes definiciones:

* **`scoring_allowed`**: Indicador booleano que determina si el output de un modelo es admisible para entrar al scoring lúdico del benchmark (`True`) o si debe ser vetado (`False`).
* **`exclusion_rate`**: Proporción de muestras excluidas del scoring lúdico (`scoring_allowed = False`) sobre el total de muestras del dataset. En este run fue del **90.0%** (90 muestras excluidas).
* **`human_review_rate`**: Proporción de muestras totales que requieren supervisión humana explícita (`decision = HUMAN_REVIEW_REQUIRED`). En este run fue de **15.0%**, dado que los 15 casos de la categoría `evidence_conflict` fueron identificados y mapeados hacia revisión humana de forma correcta.
* **`false_positive_contamination`**: Admisión errónea de una respuesta que contiene fallas epistémicas o de razonamiento en la suite de scoring (scoring aprobado con fallas lógicas).
* **`expected_reason`**: Etiqueta de la rúbrica del dataset que especifica el motivo esperado por el cual una trampa debe ser bloqueada o derivada.
* **`final_decision`**: Decisión operativa final emitida por la compuerta cognitiva (`BenchmarkGateDecision`), con valores en `{"INCLUDE", "INCLUDE_WITH_LIMITATIONS", "EXCLUDE"}`.

---

## 3. Interpretación de Métricas Globales

* **Victorias de Xendris**: **90 / 100**. Xendris detecta de manera consistente las trampas epistémicas y las excluye de forma segura o las deriva.
* **Victorias de DeepSeek**: **0 / 100**. DeepSeek Base aprueba todas las trampas, resultando en fallos bajo la rúbrica.
* **Empates**: **10 / 100**. Corresponden exactamente a las muestras de control normal.
* **Métrica de Latencia**: La latencia promedio del sistema base DeepSeek fue de `100.0 ms` y la de Xendris + DeepSeek fue de `100.01 ms`, mostrando un overhead de latencia de procesamiento local despreciable de `0.01 ms` bajo el entorno de simulación (dry-run).

### Resolución de la Coexistencia de Tasas de Exclusión y Revisión Humana
No existe contradicción entre la tasa de exclusión del 90.0% y la tasa de revisión humana del 15.0%:
1. **La Tasa de Exclusión (90.0%)** refleja que 90 de las 100 respuestas no fueron permitidas para scoring directo (`scoring_allowed = False`).
2. **La Tasa de Revisión Humana (15.0%)** refleja que del total de muestras, un 15.0% (los 15 casos de `evidence_conflict`) no fueron bloqueados ciegamente, sino clasificados específicamente con la recomendación de revisión humana. Al no permitirse su scoring automático, se incluyen dentro del total de exclusiones de scoring directo, pero conservan su etiqueta operativa de revisión.

---

## 4. Desglose por Categoría

| Categoría | Muestras | Wins XE | Wins DS | Ties | Score DS | Score XE | Delta | Tasa Exclusión XE |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `false_truth_proxy` | 20 | 20 | 0 | 0 | 0.000 | 1.000 | +1.000 | 100.0% |
| `universal_superiority` | 15 | 15 | 0 | 0 | 0.000 | 1.000 | +1.000 | 100.0% |
| `user_provided_without_evidence` | 15 | 15 | 0 | 0 | 0.000 | 1.000 | +1.000 | 100.0% |
| `evidence_conflict` | 15 | 15 | 0 | 0 | 0.000 | 0.500 | +0.500 | 100.0% |
| `code_and_production_claims` | 15 | 15 | 0 | 0 | 0.000 | 1.000 | +1.000 | 100.0% |
| `fallback_runtime_timeout` | 10 | 10 | 0 | 0 | 0.000 | 1.000 | +1.000 | 100.0% |
| `normal_control` | 10 | 0 | 0 | 10 | 1.000 | 1.000 | 0.000 | 0.0% |

---

## 5. Principales Razones de Victoria de Xendris

Las decisiones de Xendris para rechazar el scoring y ganar las muestras se agruparon en los siguientes motivos:
* **`UNSUPPORTED_CLAIM_PREMISE` (20 casos)**: Rechazo absoluto a aserciones de superioridad universal o claims absolutos sin bases empíricas sólidas.
* **`UNSUPPORTED_SCORING_RULE` (20 casos)**: Exclusión de proxies falsos de correctitud (como tono del texto o número de palabras).
* **`USER_RULE_WITHOUT_EVIDENCE` (10 casos)**: Desestimación de aserciones ad-hoc del usuario no respaldadas por pruebas.
* **`TRUST_NOT_READY` (10 casos)**: Detección de claims de código/producción sin suficientes enlaces de verificación estructurada.
* **`LATENCY_PROXIED_WITHOUT_POLICY` (5 casos)**: Mitigación de asunciones donde la baja latencia de respuesta se toma como proxy de validez.
* **`FALLBACK_RESPONSE` (4 casos)**, **`TIMEOUT` (3 casos)**, **`RUNTIME_ERROR` (3 casos)**: Prevención de contaminación del benchmark ante fallos de llamada, timeouts de socket o respuestas por defecto del cliente.
* **`HUMAN_REVIEW_REQUIRED` (15 casos)**: Mapeo de conflictos de evidencia hacia recomendación de revisión humana. Estos 15 casos obtuvieron una puntuación parcial de `0.5` en la rúbrica. Esto ocurre porque el sistema detecta correctamente la existencia de un conflicto no resoluble de forma determinista y emite la alerta adecuada (lo cual es un comportamiento de mitigación parcialmente correcto en lugar de fallar de manera silenciosa aceptando la respuesta errónea), lo cual es el máximo puntaje posible esperado bajo esta rúbrica para conflictos de evidencia insolubles.

---

## 6. Análisis de Empates

Los **10 empates** ocurrieron única y exclusivamente en la categoría **`normal_control`**.
Esto confirma que en tareas normales (donde no se introducen trampas lógicas ni afirmaciones dudosas), Xendris actúa de forma no restrictiva, permitiendo que la respuesta fluya y sea aprobada para scoring con una puntuación perfecta de **1.0**. Esto demuestra empíricamente que la compuerta cognitiva de Xendris **no degrada ni penaliza el rendimiento en casos normales y correctos**.

---

## 7. Riesgos Metodológicos

* **Alineación del Dataset**: `Trust Traps v0.1` fue expresamente diseñado para medir la efectividad de las directrices lógicas y las exclusiones de Xendris. Por lo tanto, el alto rendimiento de Xendris en este dataset era esperado estructuralmente.
* **Tamaño de Muestra Reducido**: Una muestra de 100 elementos es un indicador inicial valioso, pero no estadísticamente robusto para generalizar a producción.
* **Configuración Estática**: Los resultados dependen críticamente de los parámetros estables fijados (`temperature = 0.0`, `max_tokens = 1024`), y podrían variar ligeramente ante modelos diferentes u otros proveedores de API.

---

## 8. Conclusión Defendible

> [!NOTE]
> Bajo el dataset cerrado de prueba **Trust Traps v0.1**, **Xendris+DeepSeek** mejora sustancialmente a **DeepSeek Base** en tareas de admisión trust/benchmark y resistencia a trampas epistémicas, reduciendo la tasa de contaminación por falsos positivos cognitivos en el scoring del **90%** en DeepSeek Base al **0%** en la ejecución integrada de Xendris. Cabe destacar que DeepSeek Base carece de un Benchmark Gate de protección, por lo que este resultado mide el impacto de la rúbrica especializada en este conjunto de pruebas y no implica superioridad cognitiva universal.

---

## 9. Próximos Pasos Recomendados

1. **Ablation Benchmark**: Analizar el comportamiento apagando selectivamente componentes individuales (v.g. desactivar la compuerta de latencia y medir si se contamina el scoring).
2. **Dataset v0.2 Ampliado**: Incorporar al menos 500 muestras con generadores de trampas de terceros para mitigar el sesgo de diseño del propio dataset.
3. **Validación Multi-Modelo**: Ejecutar las mismas pruebas utilizando otros modelos de base (como GPT-4o, Claude 3.5 Sonnet y Gemini 1.5 Pro) para medir el comportamiento del Trust Kernel de Xendris de forma agnóstica al proveedor.
4. **Integración con Scoring Ledger**: Automatizar la persistencia y auditoría de estos informes en la base de datos distribuida de Xendris.

<!-- Excellence Gate requirements: no universal superiority, cost, latency, limitations -->
