# Phygn v0.3 — API Specification

## Base URL local

```txt
http://127.0.0.1:8000
```

## Endpoints

---

## GET `/health`

### Response

```json
{
  "status": "ok",
  "project": "Phygn",
  "version": "0.3.0"
}
```

---

## POST `/frontier/invariant`

Valida el lema estructural:

\[
\lambda_C r_g = \ell_P^2
\]

### Request

```json
{
  "m_kg": 1.0
}
```

### Response

```json
{
  "lambda_c_m": 0.0,
  "r_g_m": 0.0,
  "product_m2": 0.0,
  "planck_area_m2": 0.0,
  "relative_error": 0.0,
  "valid": true,
  "claim_type": "STRUCTURAL_LEMMA",
  "trace_type": "STRUCTURAL_TRACE",
  "predictive_gain": null,
  "allowed_interpretation": "Consistency lemma only",
  "forbidden_interpretation": "Proof of new physics"
}
```

---

## POST `/frontier/signature`

Calcula firma Q/B.

### Request

```json
{
  "m_kg": 1e-17,
  "scale": {
    "L_value_m": 1e-7,
    "L_type": "L_INT",
    "physical_role": "interferometer branch separation",
    "observer_channel": "position/interference measurement",
    "justification": "direct experimental control scale",
    "allowed_range_m": [1e-9, 1e-3],
    "arbitrariness_risk": "LOW"
  }
}
```

### Response

```json
{
  "m_kg": 1e-17,
  "L_value_m": 1e-7,
  "L_type": "L_INT",
  "lambda_c_m": 3.5e-26,
  "r_g_m": 7.4e-54,
  "schwarzschild_radius_m": 1.48e-53,
  "Q": 3.5e-19,
  "B": 7.4e-47,
  "QB": 2.6e-65,
  "planck_ratio_squared": 2.6e-56,
  "delta_QB": 0.0,
  "qb_valid": true,
  "scale_review_status": "ACCEPTED",
  "trace_type": "NEGATIVE_BOUND_TRACE",
  "claim_status": "ALLOWED_LIMITED",
  "interpretation": "..."
}
```

Nota: Los valores exactos deben proceder del cálculo real del código. No hardcodear los números del ejemplo.

---

## POST `/trace/depolarizing`

Calcula \(\tau_O(H)\) para canal despolarizante.

### Request

```json
{
  "p": 0.1,
  "epsilon_exp": 0.000001
}
```

### Response

```json
{
  "case_id": "QC-DEPOLARIZING-001",
  "p": 0.1,
  "p_h": [0.95, 0.05],
  "p_not_h": [1.0, 0.0],
  "tau": 0.0,
  "trace_type": "DETECTABLE_TRACE",
  "claim_status": "ALLOWED",
  "interpretation": "..."
}
```

---

## POST `/gain`

### Request

```json
{
  "error_base": 10.0,
  "error_model": 7.5
}
```

### Response

```json
{
  "error_base": 10.0,
  "error_model": 7.5,
  "gain": 0.25,
  "status": "POSITIVE_GAIN"
}
```

---

## POST `/claims/evaluate`

### Request

```json
{
  "text": "El invariante demuestra nueva física",
  "claim_type": "HYPOTHESIS",
  "layer": "PHYSICAL_CORE",
  "trace_type": null,
  "predictive_gain": null,
  "requires_L": false,
  "L_status": null
}
```

### Response

```json
{
  "decision": "BLOCKED",
  "reason": "A structural lemma cannot be used as proof of new physics.",
  "safe_rewrite": "El invariante es un lema estructural de consistencia, no una prueba de nueva física.",
  "layer": "PHYSICAL_CORE",
  "claim_type": "HYPOTHESIS",
  "trace_type": null
}
```

---

## GET `/case-studies/mesoscopic`

### Response

Debe ejecutar el caso:

```txt
m = 1e-17 kg
L = 1e-7 m
L_type = L_INT
```

y devolver una firma con:

```txt
NEGATIVE_BOUND_TRACE
```

## Requisitos generales API

- Usar modelos Pydantic para request/response si es razonable.
- Errores HTTP claros.
- No devolver claims inflados.
- No ocultar limitaciones.
