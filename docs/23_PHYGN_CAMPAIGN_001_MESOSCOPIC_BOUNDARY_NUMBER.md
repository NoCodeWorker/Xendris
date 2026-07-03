# Phygn v0.5 — CAMPAIGN-001: Mesoscopic Boundary Number

## 0. Propósito

Esta campaña busca el primer número serio de Phygn.

No se trata de probar Frontera C.  
Se trata de producir un cálculo reproducible para un sistema mesoscópico y forzar al framework a decidir:

```txt
qué puede afirmar
qué debe bloquear
qué fuente necesita
qué benchmark falta
qué modelo base se requiere
```

## 1. Pregunta científica

```txt
Para un sistema mesoscópico tipo nanopartícula en interferometría de materia, ¿qué restricción impone QB = (ℓP/L)^2 sobre la relevancia simultánea de las fronteras cuántica y gravitacional, y qué claims quedan permitidos o bloqueados?
```

## 2. Sistema inicial

Parámetros iniciales:

```txt
m = 1e-17 kg
L = 1e-7 m
L_type = L_INT
physical_role = interferometric path separation or characteristic localization scale
observer_channel = matter-wave interference readout
```

Estos valores pueden representar una escala tipo MAQRO-like, pero no se debe afirmar MAQRO exacto sin fuente RAG.

## 3. Cálculos obligatorios

\[
\lambda_C = \frac{\hbar}{mc}
\]

\[
r_g = \frac{Gm}{c^2}
\]

\[
R_S = \frac{2Gm}{c^2}
\]

\[
Q = \frac{\lambda_C}{L}
\]

\[
B = \frac{r_g}{L}
\]

\[
QB = \left(\frac{\ell_P}{L}\right)^2
\]

## 4. Interpretación inicial esperada

Para masas mesoscópicas y escalas \(L \sim 10^{-7}m\), se espera:

```txt
Q very small
B extremely small
QB fixed by L
direct gravitational boundary effect negligible
```

Pero esto debe calcularse, no asumirse.

## 5. Claim permitido

```txt
For the selected m and L, Phygn computes a negative bound showing that the direct gravitational boundary ratio B = r_g/L is negligible.
```

En español:

```txt
Para los valores seleccionados de m y L, Phygn calcula una cota negativa que muestra que la razón gravitacional directa B = r_g/L es despreciable.
```

## 6. Claim bloqueado

```txt
Phygn predicts new gravitational decoherence.
```

Debe bloquearse salvo que exista:

```txt
modelo dinámico de decoherencia
modelo base
modelo candidato
métrica de error
Predictive Gain
fuentes
benchmark
```

## 7. Distinción crítica

Una cota negativa no es una predicción positiva.

```txt
NEGATIVE_BOUND_TRACE:
descarta o limita claims.

PREDICTIVE_TRACE:
predice una señal observable.
```

CAMPAIGN-001 empieza como:

```txt
NEGATIVE_BOUND_TRACE
```

y solo puede evolucionar a:

```txt
PREDICTIVE_TRACE
```

si se añade modelo dinámico y benchmark.

## 8. Pipeline de campaña

```txt
1. cargar sistema físico
2. revisar escala L
3. calcular firma Q/B
4. validar QB
5. clasificar región
6. generar claims permitidos
7. bloquear claims excesivos
8. crear ResearchTasks faltantes
9. generar reporte
10. crear siguiente tarea
```

## 9. Objeto `CampaignInput`

```python
class CampaignInput(BaseModel):
    campaign_id: str
    system_id: str
    m_kg: float
    L_value_m: float
    L_type: str
    physical_role: str
    observer_channel: str
    justification: str
    allowed_range_m: tuple[float, float]
    arbitrariness_risk: str
```

## 10. Objeto `CampaignResult`

```python
class CampaignResult(BaseModel):
    campaign_id: str
    system_id: str
    signature: dict
    atlas_region: str
    trace_type: str
    allowed_claims: list[str]
    blocked_claims: list[str]
    required_sources: list[str]
    required_models: list[str]
    required_tests: list[str]
    benchmark_status: str
    next_tasks: list[str]
```

## 11. Módulos sugeridos

```txt
phyng/campaigns/
  __init__.py
  schemas.py
  mesoscopic_boundary_number.py
  campaign_runner.py
  campaign_report.py
```

## 12. Tests sugeridos

```txt
tests/test_campaign_mesoscopic_boundary_number.py
tests/test_campaign_runner.py
tests/test_campaign_report.py
```

Casos:

```txt
test_mesoscopic_campaign_computes_signature
test_mesoscopic_campaign_validates_QB
test_mesoscopic_campaign_classifies_negative_bound
test_mesoscopic_campaign_blocks_positive_decoherence_claim
test_mesoscopic_campaign_creates_research_tasks_if_sources_missing
test_mesoscopic_campaign_report_generated
```

## 13. Reporte

Generar:

```txt
reports/campaigns/CAMPAIGN-001_mesoscopic_boundary_number.md
```

Debe contener:

```txt
Scientific Question
Input System
Operational Scale Review
Boundary Signature
Invariant Check
Region Classification
Allowed Claims
Blocked Claims
RAG Status
Benchmark Status
Tests
Next Tasks
```

## 14. Siguiente escalón

Si CAMPAIGN-001 funciona, CAMPAIGN-002 puede intentar:

```txt
dynamic decoherence comparison
```

con:

```txt
M_base = standard decoherence model
M_C = boundary-aware modification
Error metric
Gain_C
```

Pero CAMPAIGN-001 no debe fingir esto.

## 15. Criterio de victoria

La campaña es exitosa si produce:

```txt
un número reproducible
una cota negativa
un reporte
tests
claims bloqueados correctamente
research tasks para lo que falte
```

No necesita producir nueva física positiva.

## 16. Frase guía

```txt
Primero una cota que nadie pueda inflar.
Después, si sobrevive, una predicción.
```
