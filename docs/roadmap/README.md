# Xendris Roadmap

**Arquitectura algebraica de confianza para gobernar modelos generativos**

Este directorio contiene el roadmap técnico de Xendris a partir del estado actual del proyecto y de una lectura arquitectónica inspirada en *Algebraic Quantum Field Theory* de Hans Halvorson, con apéndice de Michael Müger.

## Advertencia metodológica

AQFT no se usa aquí como validación física de Xendris. Se usa como inspiración formal para diseñar una arquitectura computacional con:

- claims observables;
- contextos locales;
- reglas de no contaminación;
- sectores epistémicos;
- representaciones de modelos;
- reconstrucción auditable desde outputs.

La tesis defendible es:

> Xendris gobierna modelos generativos mediante algebras locales de claims, reglas de no contaminación epistémica, sectores de admisión y reconstrucción auditable del comportamiento de cada modelo.

## Archivos

1. `00_vision.md` — visión estratégica y tesis fundacional.
2. `01_aqft_mapping.md` — traducción prudente AQFT → Xendris.
3. `02_architecture.md` — arquitectura objetivo.
4. `03_roadmap_versions.md` — roadmap por versiones.
5. `04_v0_4_local_claim_algebras.md` — especificación ejecutable del siguiente bloque.
6. `05_tests_acceptance.md` — criterios de aceptación y tests.
7. `06_prompt_inicio.md` — prompt de inicio para el IDE/agente.
8. `07_goal_roadmap.md` — goal de roadmap para guiar implementación.
9. `08_glossary.md` — glosario del sistema.
10. `AlgebraicQuantumFieldTheory.pdf` — documento de consulta.

## Orden recomendado

Empezar por `06_prompt_inicio.md` y usar `07_goal_roadmap.md` como objetivo de alto nivel. Después implementar `04_v0_4_local_claim_algebras.md` y validar con `05_tests_acceptance.md`.
