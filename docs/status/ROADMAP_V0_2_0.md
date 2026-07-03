# Xendris Roadmap v0.2.0

## Baseline reference

- Current stable tag: `v0.1.0-baseline`
- Baseline commit: `9ba100c chore: finalize repository baseline cleanup`

## Objective

Definir `v0.2.0` como la primera versión funcional orientada a framework público, manteniendo `phyng` como motor científico interno/legacy.

## Non-goals

- No renombrar todavía `phyng/`
- No eliminar módulos legacy
- No introducir claims científicas nuevas
- No añadir outputs generados al repositorio
- No romper compatibilidad hacia atrás

## Proposed scope

1. Public API stabilization
   - Revisar exports de `xendris/`
   - Definir qué módulos forman parte de la API pública
   - Mantener compatibilidad con `phyng`

2. CLI mínima
   - Evaluar si conviene añadir comando `xendris`
   - Comandos candidatos:
     - `xendris status`
     - `xendris validate`
     - `xendris benchmark`

3. Documentation polish
   - Mejorar README
   - Añadir quickstart
   - Añadir ejemplo mínimo reproducible

4. Benchmark hygiene
   - Separar fixtures de outputs
   - Documentar benchmarks reproducibles
   - Mantener outputs fuera de Git

5. Lean environment
   - Documentar instalación de Lean/Lake
   - Convertir el bloqueo actual en una verificación reproducible

## Validation requirements

- Python suite passes
- Focused Xendris contracts pass
- Frontend build passes, if frontend remains in repo
- Lean build verified or explicitly marked as environment-blocked

## Release criteria

`v0.2.0` solo podrá etiquetarse si:

- working tree limpio
- tests Python pasan
- README refleja estado real
- no hay outputs generados versionados
- API pública mínima está documentada
- fallos Lean, si existen, están documentados como ambientales o técnicos

## Candidate tag

`v0.2.0-framework-api`

## Recommended first task

Auditar `xendris/__init__.py` y los módulos reexportados para decidir la API pública mínima.
