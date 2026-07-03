# Phygn v0.8 — CAMPAIGN-002 Baseline Physicalization

## 0. Propósito

Este documento define cómo CAMPAIGN-002 debe actualizarse para usar un baseline físicamente respaldado, si la evidencia existe.

La campaña sigue sin afirmar decoherencia boundary-aware.

## 1. Antes de v0.8

```txt
baseline_status = TOY_INTERNAL
candidate_status = HYPOTHETICAL_CANDIDATE
benchmark_status = SYNTHETIC_READY
can_claim_physical_prediction = False
```

## 2. Objetivo v0.8

```txt
baseline_status:
TOY_INTERNAL → SOURCE_BACKED_LIMITED
```

o:

```txt
TOY_INTERNAL → BASELINE_REQUIRES_SOURCE
```

si no hay fuentes.

## 3. Campaign002BaselineUpgradeResult

```python
class Campaign002BaselineUpgradeResult(BaseModel):
    campaign_id: str
    baseline_before: str
    baseline_after: str
    baseline_readiness: dict
    source_requirements: list[str]
    source_support_matrix_path: str | None
    updated_max_claim_level: int
    allowed_new_claims: list[str]
    still_blocked_claims: list[str]
    next_required_steps: list[str]
```

## 4. Allowed new claims if baseline becomes source-backed limited

```txt
CAMPAIGN-002 now uses a source-backed limited baseline for visibility decay.
```

```txt
The candidate remains hypothetical and no physical prediction is claimed.
```

## 5. Still blocked

```txt
Phygn predicts gravitational decoherence.
Boundary C causes decoherence.
SyntheticGain proves physical gain.
The source-backed baseline validates the boundary-aware candidate.
```

## 6. Required next steps after baseline physicalization

```txt
source-backed candidate hypothesis or explicit hypothetical status
literature/experimental benchmark
epsilon_exp source
y_true provenance
PredictiveGain label permission
```

## 7. Reports

Generate:

```txt
reports/campaigns/CAMPAIGN-002_baseline_physicalization.md
reports/model_comparison/source_backed_readiness.md
reports/model_comparison/visibility_decay_baseline_readiness.md
```

## 8. Tests

```txt
tests/test_campaign_002_baseline_physicalization.py
```

Cases:

```txt
test_campaign_002_baseline_requires_source_if_no_sources
test_campaign_002_baseline_limited_if_source_backed
test_baseline_upgrade_does_not_unlock_candidate_prediction
test_source_backed_baseline_updates_readiness_report
```

## 9. Dashboard reflection

If dashboard is updated, show:

```txt
Baseline Status
Candidate Status
Benchmark Status
Claim Level
Still Blocked
Next Evidence Needed
```

## 10. Final principle

```txt
Subir el baseline no sube automáticamente al candidato.
```
