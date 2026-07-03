# Phygn v1.0 — Baseline Source Selection Guide

## 0. Propósito

Este documento define qué fuentes debe buscar el usuario o el IDE para alimentar `sources/baseline/`.

La misión no es encontrar fuentes que “den la razón” a Frontera C.  
La misión es encontrar fuentes que hagan sólido el baseline.

---

## 1. Baseline objetivo

\[
V_{base}(t)=e^{-\Gamma t}
\]

Uso permitido:

```txt
phenomenological baseline for visibility/coherence decay
limited comparison reference
```

Uso prohibido:

```txt
universal decoherence model
proof of boundary-aware candidate
validation of Frontera C
```

---

## 2. Categorías de fuente necesarias

### SRC-VIS-001 — Visibility / coherence decay

Debe respaldar:

```txt
visibility loss
coherence decay
decay curve
interferometric visibility
```

Support types posibles:

```txt
FORMULA_SUPPORT
OBSERVABLE_SUPPORT
CONTEXT_SUPPORT
```

---

### SRC-DECOH-001 — Environmental decoherence

Debe respaldar:

```txt
environment-induced decoherence
effective decoherence rate
loss of interference
```

Support types posibles:

```txt
FORMULA_SUPPORT
PARAMETER_SUPPORT
OBSERVABLE_SUPPORT
```

---

### SRC-MWI-001 — Matter-wave / nanoparticle interferometry

Debe respaldar:

```txt
matter-wave interferometry context
mesoscopic systems
nanoparticles
visibility as observable
```

Support types posibles:

```txt
OBSERVABLE_SUPPORT
CONTEXT_SUPPORT
EXPERIMENTAL_CONTEXT
```

---

### SRC-THRESH-001 — Visibility thresholds / uncertainty

Debe respaldar:

```txt
experimental visibility uncertainty
detectability threshold
epsilon_exp candidate
```

Support types posibles:

```txt
PARAMETER_SUPPORT
OBSERVABLE_SUPPORT
BENCHMARK_SUPPORT
```

---

## 3. Prioridad de fuentes

Orden preferido:

```txt
1. Review académica de decoherencia en interferometría.
2. Paper experimental sobre interferometría de materia o nanopartículas.
3. Paper/modelo sobre decoherencia ambiental.
4. Libro o capítulo técnico estándar.
5. Notas universitarias de alta calidad.
```

Evitar para hard claims:

```txt
blogs
foros
resúmenes sin referencias
textos generados por IA
Wikipedia como soporte directo
```

---

## 4. Source manifest recomendado

Archivo:

```txt
sources/baseline/source_manifest.json
```

Formato:

```json
[
  {
    "source_candidate_id": "SRC-VIS-001",
    "requirement_id": "BSP-001",
    "title": null,
    "authors": [],
    "year": null,
    "source_type": "LOCAL_FILE",
    "local_path": "sources/baseline/example.pdf",
    "url": null,
    "trust_level": "HIGH",
    "intended_support_types": ["FORMULA_SUPPORT", "OBSERVABLE_SUPPORT"],
    "notes": "Replace with real metadata after audit."
  }
]
```

Regla:

```txt
No rellenar metadata si no se conoce.
No inventar DOI, autores, año, páginas ni citas.
```

---

## 5. Qué fragmentos son útiles

Phygn debe buscar en las fuentes fragmentos que digan explícitamente:

```txt
visibility decays with time
loss of coherence/interference
environmental decoherence rate
interferometric visibility as observable
experimental visibility uncertainty
```

Pero debe evitar inferir demasiado.

---

## 6. Qué NO basta

No basta:

```txt
un paper que mencione decoherence sin fórmula
un paper que hable de quantum gravity sin visibility
una URL sin contenido local
metadata sin texto
contexto histórico sin soporte directo
```

---

## 7. Source acceptance decision

```txt
FORMULA_SUPPORT + OBSERVABLE_SUPPORT + PASSED_LIMITED
→ candidate for BASELINE_SOURCE_BACKED_LIMITED
```

```txt
CONTEXT_SUPPORT only
→ no upgrade
```

```txt
CONTRADICTION
→ block upgrade
```

---

## 8. Resultado esperado

El source pack debe responder:

```txt
¿Tenemos soporte directo para usar V_base(t)=exp(-Γt) como baseline limitado?
```

No debe responder:

```txt
¿Frontera C es real?
```

---

## 9. Frase final

```txt
Busca fuentes para fortalecer al adversario, no al candidato.
```
