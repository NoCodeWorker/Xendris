# Phygn v1.0 — Local Source File Preparation Protocol

## 0. Propósito

Este documento define cómo preparar archivos locales para que Phygn pueda ingerirlos de forma auditable.

Carpeta objetivo:

```txt
sources/baseline/
```

---

## 1. Estructura recomendada

```txt
sources/
  baseline/
    source_manifest.json
    papers/
      decoherence_visibility_001.pdf
      matter_wave_interferometry_001.pdf
    notes/
      decoherence_visibility_001_notes.md
      matter_wave_interferometry_001_notes.md
    extracts/
      decoherence_visibility_001_extracts.md
```

---

## 2. Formatos aceptados

```txt
.pdf
.md
.txt
.html
.json
.bib
```

---

## 3. Metadata mínima

Para cada fuente:

```txt
title
authors
year
source_type
local_path
trust_level
intended_support_types
```

Si falta algo:

```txt
metadata_status = PARTIAL
```

No inventar.

---

## 4. Extractos manuales

Si el PDF no se puede parsear bien, crear:

```txt
sources/baseline/extracts/{source_id}_extracts.md
```

Formato:

```md
# Extracts — SOURCE_ID

## Metadata

- Title:
- Authors:
- Year:
- Source file:

## Excerpt 1

Support type: FORMULA_SUPPORT  
Local reference: page/section if known  
Text:

> short excerpt or paraphrase with clear reference

## Excerpt 2

Support type: OBSERVABLE_SUPPORT  
Local reference: page/section if known  
Text:

> short excerpt or paraphrase with clear reference
```

Regla:

```txt
No inventar excerpt.
No poner citas largas.
No poner support_type si no está claro.
```

---

## 5. Manifest example

```json
[
  {
    "source_candidate_id": "SRC-BASE-VIS-001",
    "requirement_id": "BSP-001",
    "title": "Unknown until audit",
    "authors": [],
    "year": null,
    "source_type": "LOCAL_FILE",
    "local_path": "sources/baseline/papers/decoherence_visibility_001.pdf",
    "url": null,
    "trust_level": "HIGH",
    "intended_support_types": ["FORMULA_SUPPORT", "OBSERVABLE_SUPPORT"],
    "notes": "Metadata requires audit."
  }
]
```

---

## 6. URL-only rule

Una URL en el manifest:

```txt
does not count as ingestion
```

Debe quedar como:

```txt
CANDIDATE_ONLY
FAILED_NO_LOCAL_CONTENT
```

hasta que haya contenido local o metadata auditada.

---

## 7. PDF parsing rule

Si el parser no extrae contenido suficiente:

```txt
INGESTED_LOCAL_PDF_METADATA
```

pero no:

```txt
INGESTED_WITH_EXTRACTS
```

Para soporte directo, se requiere:

```txt
extracts
```

o texto local legible.

---

## 8. Safety rule

No usar fuentes para desbloquear claims generales.

Una fuente puede desbloquear:

```txt
baseline limited
```

pero no:

```txt
candidate validation
Frontera C validation
physical decoherence prediction
```

---

## 9. Checklist antes de ejecutar v1.0

```txt
[ ] Existe sources/baseline/
[ ] Hay al menos un manifest o archivos locales
[ ] Cada archivo tiene path estable
[ ] Metadata desconocida está marcada como null/empty
[ ] No hay DOI/autores/años inventados
[ ] Extractos cortos si se necesitan
[ ] intended_support_types declarados
```

---

## 10. Frase final

```txt
Una fuente local no vale por estar presente.
Vale cuando puede ser auditada.
```
