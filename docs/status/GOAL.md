# Xendris / Frontera C — Definición de Goal Estable del Proyecto

“El objetivo de Xendris/Frontera C es construir una capa de control sobre un modelo base capaz de generar una respuesta inicial, evaluar su validez, detectar errores, reparar errores detectables, verificar la respuesta reparada, registrar trazas y convertir patrones repetibles en reglas reutilizables.”

## Restricciones Críticas y Contexto Operacional

1. **Sin Afirmación de Superioridad Universal**: Toda validación de mejoras debe formularse para familias concretas de fallo (e.g., Falsa Formalidad Matemática) mediante métricas cuantitativas y benchmarks representativos, nunca con afirmaciones generales de superioridad absoluta sobre el modelo base.
2. **Framework de Control Cognitivo**: Frontera C es el framework interno (escrito en Python) encargado de las reglas de validación física, epistémica, álgebra y límites computacionales, mientras que Xendris actúa como el producto e interfaz de chat final del usuario.
3. **Bucle de Reparación**: Cualquier fallo calificado como de alto riesgo en la etapa de evaluación no debe ser meramente anotado o complementado al final, sino reparado (reemplazado) en su totalidad antes de ser presentado como respuesta al usuario final.
