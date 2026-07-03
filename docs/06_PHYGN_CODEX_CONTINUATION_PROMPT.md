# Prompt para Codex — Continuar desarrollo de Phygn

Estás trabajando en el proyecto local:

```txt
d:\BIOCULTOR\PHYNG\
```

El proyecto se llama:

```txt
Phygn — Physical Signatures Lab
```

Antes de modificar código, lee todos los documentos `.md` de la carpeta `docs/`.

## Contexto actual

La estructura del proyecto ya existe:

```txt
phyng/
  constants.py
  enums.py
  errors.py
  frontier_lengths.py
  operational_scale.py
  signature.py
  epistemic_trace.py
  predictive_gain.py
  claim_gatekeeper.py
  api.py
  case_studies/
    quantum_channel.py
    mesoscopic_interferometer.py
tests/
```

Hay aproximadamente 63 tests distribuidos entre:

```txt
test_frontier_lengths.py
test_operational_scale.py
test_signature.py
test_epistemic_trace.py
test_predictive_gain.py
test_claim_gatekeeper.py
test_case_quantum_channel.py
test_case_mesoscopic.py
```

## Tu tarea

Continúa el desarrollo sin reescribir todo desde cero.

Primero inspecciona:

```bash
dir
pytest -v
```

Después:

1. Detecta tests fallidos.
2. Corrige implementación sin cambiar la intención científica.
3. No rebajes tests para hacerlos pasar.
4. No cambies nombres públicos salvo necesidad justificada.
5. Mantén compatibilidad con la API.
6. Actualiza README si cambias comportamiento.
7. Añade tests si detectas bugs conceptuales.

## Prioridades

### Prioridad 1 — Backend correcto

Asegura que:

```txt
pytest -v
```

pasa completo.

### Prioridad 2 — API funcional

Asegura:

```bash
uvicorn phyng.api:app --reload
```

Endpoints:

```txt
GET /health
POST /frontier/invariant
POST /frontier/signature
POST /trace/depolarizing
POST /gain
POST /claims/evaluate
GET /case-studies/mesoscopic
```

### Prioridad 3 — README

README debe explicar:

```txt
qué es Phygn
qué no es
instalación
tests
API
ejemplos
claims permitidos/prohibidos
```

### Prioridad 4 — Reporte automático

Si backend y API funcionan, añade:

```txt
phyng/reporting.py
```

para generar reportes Markdown de casos de estudio.

Función sugerida:

```python
def generate_mesoscopic_report(output_path: str = "reports/mesoscopic_negative_bound_report.md") -> str:
    ...
```

El reporte debe incluir:

```txt
inputs
fórmulas
resultados
trace_type
claim_status
interpretación permitida
interpretación prohibida
limitaciones
```

Añade tests.

### Prioridad 5 — No frontend todavía

No implementes frontend hasta que backend, tests, API, README y reporting estén estables.

## Reglas científicas innegociables

### Regla 1

El lema:

\[
\lambda_C r_g=\ell_P^2
\]

es:

```txt
STRUCTURAL_LEMMA
STRUCTURAL_TRACE
```

No es prueba de nueva física.

### Regla 2

La firma:

\[
Q=\lambda_C/L,\quad B=r_g/L
\]

solo puede soportar claims si \(L\) está justificada.

### Regla 3

Una hipótesis sin traza:

\[
\tau_O(H)=0
\]

no tiene validez operacional para el canal dado.

### Regla 4

Las extensiones cognitivas no validan el núcleo físico.

### Regla 5

Un claim de nueva física exige:

```txt
DETECTABLE_TRACE
PREDICTIVE_TRACE
NEGATIVE_BOUND_TRACE explícita
```

o debe ser bloqueado.

## Comandos esperados

```bash
pip install -e .
pytest -v
uvicorn phyng.api:app --reload
```

## Criterios de aceptación

Termina cuando:

```txt
todos los tests pasan
API responde
README actualizado
Claim Gatekeeper bloquea claims indebidos
mesoscopic case produce NEGATIVE_BOUND_TRACE
depolarizing channel produce tau=0 si p=0 y tau>0 si p>0
```

## Principio final

Phygn no existe para confirmar Frontera C.

Phygn existe para intentar romperla con cálculo.

```txt
La generalidad puede esperar.
La predicción no.
```
