# 01 — Mapeo AQFT → Xendris

## Advertencia

Este documento no intenta probar Xendris mediante física. Usa *Algebraic Quantum Field Theory* como fuente de patrones formales.

AQFT sirve aquí como inspiración porque trabaja con:

- algebras de observables;
- estados;
- representaciones;
- nets locales;
- microcausalidad;
- sectores de superselección;
- reconstrucción desde estructuras observables.

## Tabla de correspondencias

| AQFT | Xendris |
|---|---|
| Observable algebra | Álgebra de claims auditables |
| Observable | Claim extraído de un output |
| State | Estado epistémico de una respuesta |
| Representation | Output concreto de un modelo/proveedor |
| Local algebra | Contexto local: benchmark, código, runtime, usuario, RAG |
| Quasilocal algebra | Registro global de claims y decisiones |
| Microcausality | No contaminación entre dominios sin puente válido |
| Superselection sector | Tipo de claim que no puede mutar libremente |
| Intertwiner / morphism | Evidencia o transformación válida entre sectores/contextos |
| Reconstruction | Inferir perfil epistémico del modelo desde outputs observables |
| Gauge / field hidden layer | Modelo/proveedor subyacente, no plenamente transparente |

## Idea 1 — Algebras locales

AQFT no parte de un único objeto global. Asocia algebras de observables a regiones.

Xendris debe asociar algebras de claims a contextos operativos:

```text
A_user
A_benchmark
A_code
A_runtime
A_rag
A_policy
A_cost
A_latency
A_production
A_documentation
```

Cada álgebra local tiene reglas propias sobre qué claims admite y qué transiciones permite.

## Idea 2 — Microcausalidad epistémica

En Xendris:

> Ningún claim puede contaminar otro dominio sin un puente de evidencia válido.

Ejemplos bloqueados:

```text
benchmark_score → universal_superiority
dry_run_latency → production_latency_claim
tests_passed → production_ready_claim
user_says_true → factual_verified_claim
```

Ejemplo permitido:

```text
benchmark_score + benchmark_artifact → limited_benchmark_claim
```

## Idea 3 — Sectores de superselección epistémica

Un claim no puede saltar de sector por tono, longitud o autoridad aparente.

Ejemplo:

```text
USER_PROVIDED → FACTUAL
```

requiere evidencia externa, cálculo, test o revisión humana.

## Idea 4 — Representaciones inequivalentes

El mismo claim puede ser representado por varios modelos.

Xendris debe distinguir:

- representaciones equivalentes;
- representaciones parcialmente equivalentes;
- representaciones contradictorias;
- representaciones disjuntas.

## Idea 5 — Reconstrucción desde observables

Xendris no debe confiar en el marketing del proveedor. Debe reconstruir la huella epistémica del modelo desde su comportamiento observable:

- tasa de claims no soportados;
- tasa de universalización;
- tasa de contaminación por proxy;
- coste por claim admisible;
- tasa de revisión humana;
- robustez por categoría.

## Principio final

> AQFT no prueba Xendris; le da esqueleto formal.
