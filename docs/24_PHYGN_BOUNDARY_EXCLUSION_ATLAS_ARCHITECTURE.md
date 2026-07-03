# Phygn v0.5 — Boundary Exclusion Atlas Architecture

## 0. Propósito

Este documento define la arquitectura del **Boundary Exclusion Atlas**.

El atlas no es una visualización.  
Es una estructura computacional que clasifica sistemas físicos en regiones de frontera y produce decisiones de claim.

## 1. Objeto central

```txt
BoundaryExclusionAtlas
```

Responsabilidad:

```txt
recibir sistemas físicos
validar escala L
calcular firma Q/B
validar invariante
clasificar región
generar claims permitidos/bloqueados
vincular fuentes RAG
generar benchmarks
exportar reportes
```

## 2. Arquitectura modular

```txt
phyng/atlas/
  __init__.py
  schemas.py
  atlas_point.py
  region_classifier.py
  exclusion_rules.py
  atlas_builder.py
  atlas_report.py
```

## 3. Data flow

```txt
PhysicalSystemSpec
→ OperationalScale review
→ frontier_signature
→ invariant validation
→ BoundaryAtlasPoint
→ RegionClassifier
→ ExclusionRules
→ ClaimGatekeeper
→ RAG citation audit
→ AtlasReport
```

## 4. PhysicalSystemSpec

```python
class PhysicalSystemSpec(BaseModel):
    system_id: str
    label: str
    description: str
    m_kg: float
    L_value_m: float
    L_type: str
    physical_role: str
    observer_channel: str
    justification: str
    allowed_range_m: tuple[float, float]
    arbitrariness_risk: str
    source_ids: list[str] = []
```

## 5. BoundaryAtlasPoint

```python
class BoundaryAtlasPoint(BaseModel):
    system_id: str
    label: str
    m_kg: float
    L_value_m: float
    lambda_c_m: float
    r_g_m: float
    schwarzschild_radius_m: float
    Q: float
    B: float
    QB: float
    planck_ratio_squared: float
    delta_QB: float
    logQ: float
    logB: float
    u: float
    w: float
    scale_status: str
    region: str
    trace_type: str
    claim_status: str
```

## 6. Coordenadas logarítmicas

\[
q=\log Q
\]

\[
b=\log B
\]

\[
u=\frac{q+b}{2}=\log(\ell_P/L)
\]

\[
w=\frac{b-q}{2}=\log(m/m_P)
\]

Interpretación:

```txt
u fija la escala operacional L.
w fija la posición de masa relativa a mP.
```

La foliación:

```txt
q + b = 2 log(ℓP/L)
```

## 7. Regiones

```python
class AtlasRegion(str, Enum):
    CLASSICAL_ACCESSIBLE = "CLASSICAL_ACCESSIBLE"
    QUANTUM_BOUNDARY = "QUANTUM_BOUNDARY"
    GRAVITATIONAL_BOUNDARY = "GRAVITATIONAL_BOUNDARY"
    PLANCK_CROSSING = "PLANCK_CROSSING"
    NEGATIVE_GRAVITY_BOUND = "NEGATIVE_GRAVITY_BOUND"
    NEGATIVE_QUANTUM_BOUND = "NEGATIVE_QUANTUM_BOUND"
    AD_HOC_SCALE_BLOCKED = "AD_HOC_SCALE_BLOCKED"
    UNCLASSIFIED = "UNCLASSIFIED"
```

## 8. Region rules

Suggested default thresholds:

```txt
near_boundary_threshold = 1e-1 to 10
small_threshold = 1e-20
```

Rules:

```txt
if scale rejected:
    AD_HOC_SCALE_BLOCKED

elif abs(log10(Q)) < boundary_window and abs(log10(B)) < boundary_window:
    PLANCK_CROSSING

elif Q near 1:
    QUANTUM_BOUNDARY

elif B near 1:
    GRAVITATIONAL_BOUNDARY

elif B < small_threshold:
    NEGATIVE_GRAVITY_BOUND

elif Q < small_threshold:
    NEGATIVE_QUANTUM_BOUND

else:
    CLASSICAL_ACCESSIBLE or UNCLASSIFIED
```

## 9. Exclusion rules

The atlas must generate blocked claims.

Examples:

```txt
If region = NEGATIVE_GRAVITY_BOUND:
block "direct gravitational boundary effect is observable" unless external model provides trace.

If scale_status != ACCEPTED:
block all predictive claims.

If QB invalid:
block atlas point.

If no source_ids for hard interpretation:
mark REQUIRES_SOURCE.
```

## 10. Allowed claims by region

### NEGATIVE_GRAVITY_BOUND

Allowed:

```txt
B is negligible under the selected operational scale.
Direct gravitational boundary claims are not supported by this signature.
```

Blocked:

```txt
Phygn predicts gravitational decoherence.
The system is near a gravitational horizon.
```

### QUANTUM_BOUNDARY

Allowed:

```txt
Q is order unity, indicating quantum-localization boundary relevance.
```

Blocked:

```txt
Quantum boundary proves consciousness/measurement collapse.
```

### PLANCK_CROSSING

Allowed:

```txt
Q and B are simultaneously order unity.
The point is structurally near Planck crossing.
```

Blocked:

```txt
This proves quantum gravity.
```

## 11. AtlasBuilder

```python
def build_atlas(
    systems: list[PhysicalSystemSpec],
    thresholds: AtlasThresholds
) -> BoundaryAtlas:
    ...
```

## 12. BoundaryAtlas

```python
class BoundaryAtlas(BaseModel):
    atlas_id: str
    version: str
    points: list[BoundaryAtlasPoint]
    summary: dict
    allowed_claims: list[str]
    blocked_claims: list[str]
    required_sources: list[str]
    generated_at: str
```

## 13. Reports

Generate:

```txt
reports/atlas/invariant_boundary_atlas.md
reports/atlas/atlas_points.json
reports/atlas/claim_exclusion_matrix.md
```

## 14. Tests

```txt
test_atlas_point_qb_identity
test_log_coordinates_valid
test_planck_crossing_region
test_negative_gravity_bound_region
test_ad_hoc_scale_blocks_predictive_claims
test_exclusion_matrix_blocks_overclaims
test_atlas_report_generated
```

## 15. No-claim rule

The atlas does not prove.

The atlas classifies.

```txt
Atlas output is not "truth".
Atlas output is "allowed status under explicit assumptions".
```
