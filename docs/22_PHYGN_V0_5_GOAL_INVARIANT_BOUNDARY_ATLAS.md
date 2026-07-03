# Phygn v0.5 — Goal: Invariant Boundary Atlas

## 0. Propósito

Phygn v0.5 debe dejar de ser solo un laboratorio de validación interna y convertirse en una **máquina de producción de resultados científicos auditables**.

El goal v0.5 es:

```txt
Construir el primer Invariant Boundary Atlas:
un atlas computacional de regiones permitidas, regiones despreciables y regiones prohibidas del espacio de fronteras físicas, anclado en el invariante QB = (ℓP/L)^2, alimentado por RAG, validado por tests y protegido por agentes de auditoría.
```

## 1. Ambición

La ambición es producir algo que pueda ser genuinamente diferencial:

```txt
no una nueva "teoría total",
no una metáfora,
no una visualización,
no una colección de fórmulas conocidas,
sino un atlas computacional que convierta el invariante Compton-gravitacional en una máquina de cotas, exclusiones y preguntas experimentales.
```

## 2. Regla de honestidad

No se permite decir:

```txt
Phygn ha descubierto una nueva ley física.
Phygn demuestra nueva física.
Phygn demuestra Frontera C.
Phygn ha producido algo que nadie ha visto jamás.
```

Sí se permite decir, si el sistema lo sostiene:

```txt
Phygn formaliza una estructura computacional auditable basada en el invariante QB = (ℓP/L)^2.
Phygn genera un atlas de cotas y regiones de frontera para sistemas físicos parametrizados.
Phygn identifica claims permitidos, limitados y bloqueados para cada región.
Phygn produce una campaña reproducible que busca una predicción o una cota negativa no trivial.
```

## 3. Pilar lógico invariable

El pilar es:

\[
\lambda_C r_g = \ell_P^2
\]

con:

\[
\lambda_C = \frac{\hbar}{mc}
\]

\[
r_g = \frac{Gm}{c^2}
\]

\[
\ell_P = \sqrt{\frac{\hbar G}{c^3}}
\]

A escala operacional \(L\):

\[
Q = \frac{\lambda_C}{L}
\]

\[
B = \frac{r_g}{L}
\]

por tanto:

\[
\boxed{QB = \left(\frac{\ell_P}{L}\right)^2}
\]

## 4. Interpretación correcta

Este resultado implica:

```txt
Q y B no son independientes a L fijo.
La masa mueve el sistema sobre una hipérbola en el plano Q/B.
L fija la hoja de la foliación.
El producto QB está determinado solo por L y constantes fundamentales.
```

Esto no prueba nueva física.  
Pero sí impone una restricción geométrica dura sobre la firma \(Q/B\).

## 5. Hipótesis de trabajo v0.5

```txt
HYP-v0.5:
Si una clase de sistemas físicos puede expresarse mediante una firma operacional B_C(S;L), entonces el invariante QB = (ℓP/L)^2 induce un atlas de regiones donde ciertos claims son permitidos, limitados o bloqueados de forma computable.
```

Estado:

```txt
HYPOTHESIS
PHYSICAL_CORE
REQUIRES_BENCHMARK
REQUIRES_RAG_SUPPORT
REQUIRES_CASE_STUDY
```

## 6. Resultado objetivo

Crear:

```txt
reports/campaigns/CAMPAIGN-001_invariant_boundary_atlas.md
```

Debe contener:

```txt
1. definición del atlas
2. invariante usado
3. sistemas físicos explorados
4. rangos de masa
5. rangos de escala L
6. mapas Q/B
7. regiones de cota negativa
8. regiones de frontera cuántica
9. regiones de frontera gravitacional
10. claims permitidos
11. claims bloqueados
12. fuentes RAG
13. tests
14. benchmarks
15. próximos experimentos candidatos
```

## 7. Qué sería "nuevo" de forma defendible

La novedad no debe formularse como "descubrimiento de una ley".

Debe formularse así:

```txt
Una arquitectura computacional reproducible que usa el invariante QB para construir un atlas de restricciones, claims y cotas por escala operacional L.
```

Esto puede ser nuevo como:

```txt
sistema de auditoría
geometría operacional
atlas computacional
metodología de exclusión
herramienta de investigación
```

pero no se debe vender como:

```txt
nueva física demostrada
```

## 8. Objetivo de no-trivialidad

Phygn v0.5 debe intentar superar el test de no-trivialidad.

Una contribución es no trivial si produce al menos uno:

```txt
A. cota negativa que descarte una familia de claims;
B. región prohibida en el espacio Q/B/L;
C. benchmark que distinga dos modelos;
D. número reproducible para un experimento candidato;
E. claim-source-test matrix que degrade una afirmación fuerte;
F. nueva pregunta experimental cuantitativa.
```

## 9. Sistemas iniciales del atlas

Iniciales:

```txt
1. Electron scale
2. Proton scale
3. Mesoscopic nanoparticle
4. MAQRO-like particle
5. Atomic interferometer scale
6. Planck mass/Planck length limit
7. Black hole horizon toy scale
```

Cada sistema debe incluir:

```txt
mass_kg
L_value_m
L_type
physical_role
observer_channel
justification
sources_required
```

## 10. Salidas computacionales

Para cada sistema:

```txt
lambda_C
r_g
R_S
Q
B
QB
logQ
logB
u = (logQ + logB)/2
w = (logB - logQ)/2
trace_type
claim_status
negative_bound_status
scale_review_status
```

## 11. Atlas como objeto formal

```python
class BoundaryAtlasPoint(BaseModel):
    system_id: str
    label: str
    m_kg: float
    L_value_m: float
    L_type: str
    lambda_c_m: float
    r_g_m: float
    schwarzschild_radius_m: float
    Q: float
    B: float
    QB: float
    planck_ratio_squared: float
    logQ: float
    logB: float
    u: float
    w: float
    scale_status: str
    trace_type: str
    claim_status: str
    allowed_claims: list[str]
    blocked_claims: list[str]
    source_ids: list[str]
    test_ids: list[str]
```

## 12. Regiones del atlas

```txt
QUANTUM_BOUNDARY_REGION:
Q ~ 1

GRAVITATIONAL_BOUNDARY_REGION:
B ~ 1

CLASSICAL_ACCESSIBLE_REGION:
Q << 1 and B << 1

PLANCK_CROSSING_REGION:
Q ~ B ~ 1

NEGATIVE_GRAVITY_BOUND_REGION:
B < threshold_B

AD_HOC_SCALE_REGION:
L not justified

CLAIM_BLOCKED_REGION:
claim exceeds trace/source/test
```

## 13. Tests mínimos

```txt
test_atlas_point_validates_QB_constraint
test_atlas_rejects_invalid_mass
test_atlas_rejects_invalid_L
test_atlas_requires_scale_justification
test_atlas_classifies_negative_gravity_bound
test_atlas_generates_allowed_and_blocked_claims
test_atlas_report_contains_claim_matrix
```

## 14. RAG mínimo para v0.5

Antes de declarar cualquier interpretación, el atlas debe crear ResearchTasks para fuentes sobre:

```txt
Compton wavelength
Schwarzschild radius
Planck scale
Compton-Schwarzschild diagram
MAQRO/mesoscopic interferometry
decoherence models
Diósi-Penrose if used
Caldeira-Leggett if used
```

Si no hay fuentes ingeridas:

```txt
claims fuertes → REQUIRES_SOURCE
```

## 15. Frase guía

```txt
El invariante no demuestra nueva física.
El atlas demuestra qué claims sobreviven cuando el invariante se aplica sin permiso para alucinar.
```
