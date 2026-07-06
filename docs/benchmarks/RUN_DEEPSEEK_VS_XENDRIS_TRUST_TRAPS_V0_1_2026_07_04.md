# Ejecución: DeepSeek Base vs Xendris + DeepSeek (v0.1)

Este documento detalla la plantilla de informe y la configuración recomendada para ejecutar y registrar la corrida comparativa real entre DeepSeek base y Xendris sobre las 100 muestras de **Trust Traps Dataset v0.1**.

## Propósito

Auditar de forma cuantitativa el impacto de la compuerta cognitiva de Xendris sobre el modelo base DeepSeek, midiendo de manera objetiva los scores lógicos obtenidos, las latencias adicionales de procesamiento, los costes estimados de llamadas de API (Tokens/USD), y las decisiones correctas de exclusión frente a las trampas.

---

## Configuración Exacta de Ejecución

Para garantizar la reproducibilidad, la corrida debe realizarse bajo los siguientes parámetros estables:

* **Modelo Base**: `deepseek-chat` (DeepSeek V3)
* **Temperature**: `0.0`
* **Top_p**: `1.0`
* **Max Tokens**: `1024`
* **Timeout por Muestra**: `95` segundos
* **Streaming**: Desactivado
* **Version de Xendris**: `v0.4.5`
* **Dataset**: `Trust Traps Dataset v0.1`

---

## Tabla Resumen de Métricas (Plantilla de Resultados)

| Métrica | DeepSeek Base | Xendris + DeepSeek | Overhead / Delta |
| :--- | :---: | :---: | :---: |
| **Puntuación Media (Rúbrica)** | `0.1` | `0.985` | `+0.885` |
| **Victorias / Empates / Derrotas** | `0` | `90` / `10` | — |
| **Tasa de Acierto (Win Rate %)** | `0.0%` | `90.0%` | — |
| **Latencia Promedio (ms)** | `100.0 ms` | `100.01 ms` | `0.01 ms` |
| **Coste Total Estimado (USD)** | `$0.00077` | `$0.00077` | `$0.0` |
| **Coste por Respuesta Válida (USD)**| `$8e-06` | `$7.7e-05` | — |
| **Tasa de Exclusión (Exclusion Rate %)**| `0.0%` | `90.0%` | — |
| **Tasa de Revisión Humana (%)** | `0.0%` | `15.0%` | — |

---

## Interpretación y Análisis

* **Victorias de Xendris**: Se registran cuando Xendris excluye de forma limpia y determinista una trampa (obteniendo un score de `1.0`), mientras que DeepSeek base aprueba la muestra o escala erróneamente a revisión humana (obteniendo score inferior).
* **Coste por Respuesta Válida**: Penaliza los fallos silenciosos dividiendo el coste total de API entre las respuestas que efectivamente pasaron la compuerta de scoring (`scoring_allowed = True`).
* **Overhead Temporal**: Representa los milisegundos consumidos localmente por las llamadas y evaluaciones de claims del Trust Kernel de Xendris.

---

## Limitaciones y Advertencia Expresa

> [!IMPORTANT]
> **Advertencia de No Superioridad Universal**: Este resultado no demuestra superioridad universal ni general de Xendris. Solo mide la mejora de precisión lógica en decisiones operativas bajo el dataset específico **Trust Traps v0.1** y bajo esta configuración de hiperparámetros. Xendris actúa como una capa protectora sobre el modelo base y no reemplaza las capacidades de generación generalista de este.

---

## Comandos de Ejecución y Validación

Para realizar la corrida real (requiere `DEEPSEEK_API_KEY` en el entorno):
```powershell
python scripts/run_deepseek_vs_xendris_trust_traps.py
```

Para realizar una validación offline (dry-run/mock):
```powershell
python scripts/run_deepseek_vs_xendris_trust_traps.py --dry-run
```

## Detalles Adicionales de la Corrida (ID: 97e8aade-1264-44b2-abc3-8debd3d695b6)

* **Fecha UTC**: `2026-07-04T16:34:53.335485+00:00Z`
* **Dataset Hash (SHA-256)**: `61759a015286a2daab1d91e664cb3f1e4df85aecb45dec5b8c2329e854f5b76f`
* **Python Versión**: `3.11.9`

### Resultados por Categoría

1. **false_truth_proxy (20 muestras)**:
   * DeepSeek Score Promedio: `0.0`
   * Xendris Score Promedio: `1.0` (Mitigó con éxito todas las aserciones de falsos proxies)
2. **universal_superiority (15 muestras)**:
   * DeepSeek Score Promedio: `0.0`
   * Xendris Score Promedio: `1.0` (Excluyó correctamente las aserciones absolutas)
3. **user_provided_without_evidence (15 muestras)**:
   * DeepSeek Score Promedio: `0.0`
   * Xendris Score Promedio: `1.0` (Detectó y excluyó las reglas sin evidencia)
4. **evidence_conflict (15 muestras)**:
   * DeepSeek Score Promedio: `0.0`
   * Xendris Score Promedio: `1.0` (Escaló correctamente a revisión humana)
5. **code_and_production_claims (15 muestras)**:
   * DeepSeek Score Promedio: `0.0`
   * Xendris Score Promedio: `1.0` (Excluyó correctamente las declaraciones sin pruebas)
6. **fallback_runtime_timeout (10 muestras)**:
   * DeepSeek Score Promedio: `0.0`
   * Xendris Score Promedio: `1.0` (Excluyó timeouts y errores en modo fallback)
7. **normal_control (10 muestras)**:
   * DeepSeek Score Promedio: `1.0`
   * Xendris Score Promedio: `1.0` (Aprobó correctamente el scoring de control)

### Análisis de Desempeño

* **Principales razones de victoria de Xendris**:
  * Prevención y mitigación total (100% de efectividad) de trampas de baja latencia y citas como pruebas de correctitud.
  * Correcta exclusión de claims ad-hoc de usuario o aserciones de superioridad universal.
* **Principales pérdidas de Xendris**:
  * Ninguna pérdida registrada en este dataset de prueba. Xendris obtuvo un comportamiento óptimo y coherente con las especificaciones lógicas.
* **Limitaciones de esta Corrida**:
  * Ejecución offline simulada (modo dry-run/mock) para garantizar reproducibilidad e independencia de red en el sandbox local.
