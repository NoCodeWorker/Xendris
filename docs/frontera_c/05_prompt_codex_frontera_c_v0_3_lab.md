# Prompt maestro para Codex — Frontera C Lab v0.3

Vas a construir un proyecto local llamado `c-boundary-lab-v0-3`.

Lee todos los documentos `.md` de esta carpeta antes de escribir código.

## Objetivo

Implementar un Lab computacional minimalista para Frontera C v0.3 centrado en:

1. selección justificada de escala operacional L;
2. cálculo de firma Q,B;
3. verificación del lema estructural QB=(lP/L)^2;
4. motor de huella epistemológica para un canal cuántico simple;
5. cota negativa para un interferómetro mesoscópico;
6. Claim Gatekeeper.

## Stack sugerido

Backend:

```txt
Python 3.11+
FastAPI
Pydantic v2
NumPy
SciPy
pytest
```

Frontend opcional:

```txt
Next.js
TypeScript
Tailwind
shadcn/ui
Recharts
KaTeX
```

Si el tiempo es limitado, prioriza backend + tests.

## Módulos obligatorios

```txt
c_boundary/constants.py
c_boundary/frontier_lengths.py
c_boundary/operational_scale.py
c_boundary/signature.py
c_boundary/epistemic_trace.py
c_boundary/predictive_gain.py
c_boundary/claim_gatekeeper.py
c_boundary/case_studies/quantum_channel.py
c_boundary/case_studies/mesoscopic_interferometer.py
tests/
```

## Constantes

```python
C = 299_792_458.0
HBAR = 1.054571817e-34
G = 6.67430e-11
KB = 1.380649e-23
```

## Funciones físicas

Implementa:

```python
compton_reduced(m_kg: float) -> float
gravitational_radius(m_kg: float) -> float
schwarzschild_radius(m_kg: float) -> float
planck_length() -> float
planck_mass() -> float
```

## Firma Q/B

Implementa:

```python
frontier_signature(m_kg: float, L_m: float, L_metadata: OperationalScale) -> FrontierSignature
```

Debe devolver lambda_c_m, r_g_m, Q, B, QB, planck_ratio_squared, delta_QB, trace_type y scale_review_status.

## Huella epistemológica

Implementa Jensen-Shannon divergence entre distribuciones discretas:

```python
jensen_shannon(p: np.ndarray, q: np.ndarray) -> float
```

Caso canal despolarizante:

```python
depolarizing_distribution(p: float) -> np.ndarray
```

Debe producir:

```txt
p=0 => tau=0
p>0 => tau>0
```

## Tests obligatorios

1. test_compton_gravity_invariant
2. test_QB_constraint
3. test_operational_scale_blocks_ad_hoc_L
4. test_depolarizing_tau_zero_when_p_zero
5. test_depolarizing_tau_positive_when_p_positive
6. test_mesoscopic_negative_bound
7. test_gatekeeper_blocks_new_physics_claim
8. test_gatekeeper_allows_structural_lemma_claim

## Endpoints mínimos

```txt
GET /health
POST /signature
POST /trace/depolarizing
POST /claims/evaluate
GET /case-studies/mesoscopic
```

## Principio rector

```txt
La generalidad puede esperar. La predicción no.
```
