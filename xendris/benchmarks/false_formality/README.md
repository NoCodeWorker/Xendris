# False Formality Benchmark Suite (v0.2)

Este módulo implementa la iteración v0.2 del pipeline de evaluación epistémica de Xendris, enfocado en identificar y corregir errores de **Falsa Formalidad Matemática** (argumentos deductivos que aparentan validez usando símbolos y estructura formal pero contienen saltos lógicos no demostrados).

## Requisitos

1. Asegúrate de tener el entorno virtual activo:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```

2. El servidor Next.js debe estar corriendo localmente para atender las peticiones HTTP del benchmark:
   ```bash
   cd frontend
   npm run dev
   ```

## Ejecución del Benchmark

El script ejecuta cada uno de los 20 casos trampa contra el modelo base directo y contra la capa de análisis y control cognitivo de Xendris.

### Modo Mock (Determinista y Rápido)

Para validar el flujo completo y el comportamiento del evaluador de manera rápida y sin llamadas externas a APIs:
```bash
python -m xendris.benchmarks.false_formality.runner --provider mock
```

### Modo DeepSeek (Evaluación Real con LLM)

Para ejecutar una campaña real de validación utilizando la API de DeepSeek configurada en el backend de Next.js:
```bash
python -m xendris.benchmarks.false_formality.runner --provider deepseek
```

## Salidas de la Ejecución

Las salidas se depositan automáticamente en el directorio `outputs/`:
* `false_formality_results.json`: Archivo con el desglose detallado de puntuaciones y metadatos de auditoría para cada caso.
* `false_formality_report.md`: Informe resumido en Markdown que detalla las estadísticas globales, ganador de cada caso, regresiones graves y estado final del benchmark (`PASSED_PATTERN_REUSABLE` o `FAILED_PATTERN_REUSABLE`).
