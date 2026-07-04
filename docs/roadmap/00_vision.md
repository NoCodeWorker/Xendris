# 00 — Visión de Xendris

## Nombre

**Xendris Algebraic Trust Architecture**

## Subtítulo

**A local claim algebra and sector-gated trust runtime for generative models.**

En español:

> Una arquitectura de algebras locales de claims y compuertas sectoriales para gobernar modelos generativos.

## Tesis fundacional

Xendris no intenta sustituir a los modelos generativos. Los gobierna.

Un modelo generativo produce texto plausible. Xendris decide si ese texto puede convertirse en conocimiento operativo, si debe limitarse, si debe bloquearse o si debe escalarse a revisión humana.

```text
Modelo generativo → output plausible → claims → sectores → contexto local → evidencia → decisión auditada
```

## Frase central

> El modelo genera posibilidades; Xendris decide qué posibilidades pueden atravesar la frontera hacia conocimiento operativo.

## Qué problema resuelve

Los LLMs tienden a:

- aceptar premisas falsas;
- responder con seguridad a claims no soportados;
- convertir evidencia local en conclusiones globales;
- confundir longitud, tono o latencia con calidad;
- presentar resultados de benchmark como superioridad universal;
- afirmar estados de producción sin trazas verificables.

Xendris introduce una capa anterior al scoring, al despliegue y a la confianza del usuario:

> admisión epistémica antes de aceptación operativa.

## Qué no afirma

Xendris no afirma:

- superioridad universal sobre otros modelos;
- que una arquitectura IA sea una teoría física;
- que AQFT valide físicamente el sistema;
- que los resultados en Trust Traps prueben inteligencia general.

## Qué sí afirma

Xendris sí puede afirmar, si los tests lo sostienen:

- reducción de contaminación epistémica en datasets definidos;
- bloqueo de transiciones inválidas entre tipos de claim;
- separación de contextos para evitar generalizaciones indebidas;
- trazabilidad de decisiones;
- capacidad de convertir modelos baratos en componentes más gobernables.

## Posicionamiento comercial

**Trust Firewall for Generative Models**

O en español:

**Cortafuegos de confianza para modelos generativos.**

## Producto inicial

**Xendris Trust Router v1**

Capacidades mínimas:

- recibe prompt y output de modelo;
- extrae claims;
- clasifica claims por sector;
- aplica reglas de transición;
- bloquea contaminación;
- decide `INCLUDE`, `INCLUDE_WITH_LIMITATIONS`, `EXCLUDE` o `HUMAN_REVIEW`;
- registra todo en ledger;
- genera informe reproducible.

## Safe Admissibility Over Maximum Blocking

Xendris must not maximize blocking. Xendris must maximize safe admissibility.

Xendris is not a censor, nor is it designed to discard everything that is uncertain. Instead, it aims to assign the correct epistemic status to generated outputs. Useful but unsupported low-risk outputs should be limited or downgraded rather than blocked. Blocking is reserved for unsafe epistemic contamination, contradiction, forbidden transitions, unsupported high-risk claims, or claims that cannot be safely constrained.

The target behavior of Xendris is not simply to "say no"; the target behavior is to "say yes, but only within the correct epistemic boundary." Xendris should convert overstrong claims into admissible, limited, and auditable claims whenever safe.

* “Xendris does not prevent a generative model from hallucinating. It prevents unsupported hallucinated claims from being admitted as verified operational knowledge.”
* “Useful but unsupported low-risk outputs should be scoped, downgraded, or admitted with limitations rather than discarded.”

