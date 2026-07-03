# Phygn v0.3 — Backend Architecture

## Objetivo del backend

El backend de Phygn debe ser un motor científico local, reproducible y testeado.

Prioridad absoluta:

```txt
cálculo correcto
tipado
tests
decisiones auditables
sin claims inflados
```

## Stack

```txt
Python 3.11+
FastAPI
Pydantic v2
NumPy
SciPy
pytest
uvicorn
```

Opcional:

```txt
SQLAlchemy
SQLite
pandas
sympy
```

Solo añadir opcionales si aportan valor real.

## Estructura actual esperada

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

## Módulos

### `constants.py`

Debe contener:

```python
C = 299_792_458.0
HBAR = 1.054571817e-34
G = 6.67430e-11
KB = 1.380649e-23
```

Funciones:

```python
planck_length() -> float
planck_mass() -> float
planck_area() -> float
```

### `errors.py`

Errores claros:

```python
InvalidMassError
InvalidProbabilityError
InvalidScaleError
InvalidDistributionError
InvalidClaimError
```

### `frontier_lengths.py`

Funciones:

```python
compton_reduced(m_kg: float) -> float
gravitational_radius(m_kg: float) -> float
schwarzschild_radius(m_kg: float) -> float
validate_compton_gravity_invariant(m_kg: float, relative_tolerance: float = 1e-12) -> dict
```

Regla:

```txt
m_kg debe ser > 0
```

El invariante siempre debe clasificarse como:

```txt
STRUCTURAL_LEMMA
STRUCTURAL_TRACE
```

Nunca como hipótesis física.

### `operational_scale.py`

Debe definir `OperationalScale`.

Campos obligatorios:

```txt
L_value_m
L_type
physical_role
observer_channel
justification
allowed_range_m
arbitrariness_risk
```

Función:

```python
review_operational_scale(scale: OperationalScale) -> dict
```

Estados:

```txt
ACCEPTED
REQUIRES_JUSTIFICATION
REJECTED
```

Si \(L\) no está aceptada, Phygn puede calcular una firma, pero no puede usarla para claims predictivos.

### `signature.py`

Función principal:

```python
frontier_signature(m_kg: float, scale: OperationalScale, qb_tolerance: float = 1e-12, gravity_threshold: float = 1e-20) -> dict
```

Debe calcular:

```txt
lambda_c_m
r_g_m
schwarzschild_radius_m
Q
B
QB
planck_ratio_squared
delta_QB
qb_valid
scale_review_status
trace_type
claim_status
interpretation
```

Reglas:

```txt
Si L no aceptada → BLOCKED_AS_AD_HOC_SCALE.
Si B < gravity_threshold y L aceptada → NEGATIVE_BOUND_TRACE.
Si solo valida QB → STRUCTURAL_TRACE.
```

### `epistemic_trace.py`

Debe implementar:

```python
normalize_distribution(p)
kl_divergence(p, q)
jensen_shannon_divergence(p, q)
epistemic_trace(p_h, p_not_h, epsilon_exp=1e-6)
```

Reglas:

```txt
τ = 0 → NULL_TRACE
0 < τ <= εexp → NOT_DETECTABLE
τ > εexp → DETECTABLE_TRACE
```

### `predictive_gain.py`

Función:

```python
predictive_gain(error_base: float, error_model: float) -> dict
```

Reglas:

```txt
error_base > 0
error_model >= 0
```

Estados:

```txt
POSITIVE_GAIN
ZERO_GAIN
NEGATIVE_GAIN
```

### `claim_gatekeeper.py`

Debe implementar las reglas anti-autoengaño.

Claims bloqueados por defecto:

```txt
El invariante demuestra nueva física.
Minkowski demuestra Frontera C completa.
La conciencia valida Frontera C.
La cancelación de masa prueba una nueva ley.
Una firma Q/B con L arbitraria tiene valor predictivo.
El área de Planck aparece, por tanto la teoría está validada.
```

### `api.py`

Endpoints mínimos:

```txt
GET /health
POST /frontier/invariant
POST /frontier/signature
POST /trace/depolarizing
POST /gain
POST /claims/evaluate
GET /case-studies/mesoscopic
```

## Calidad

Todo debe tener:

```txt
type hints
docstrings científicos
errores explícitos
tests
sin sobreingeniería
```

## Regla final

El backend no debe confirmar Frontera C.  
Debe intentar romperla.
