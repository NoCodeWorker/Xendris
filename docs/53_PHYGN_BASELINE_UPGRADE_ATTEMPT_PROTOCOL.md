# Phygn v0.9 — Baseline Upgrade Attempt Protocol

## 0. Propósito

Este documento define el intento formal de subir el baseline de CAMPAIGN-002.

El intento puede fallar.  
Si falla honestamente, v0.9 sigue siendo válida.

## 1. Input

```txt
VisibilityDecayBaselineSpec
BaselineSourcePack
CitationAuditResults
BaselineSourceSupportMatrix
```

## 2. Output

```python
class BaselineUpgradeAttemptResult(BaseModel):
    attempt_id: str
    campaign_id: str
    baseline_before: str
    baseline_after: str
    success: bool
    reason: str
    source_pack_status: str
    direct_support_types: list[str]
    missing_support_types: list[str]
    contradiction_ids: list[str]
    max_claim_level: int
    allowed_claims: list[str]
    blocked_claims: list[str]
    next_research_tasks: list[str]
```

## 3. Upgrade rules

### Rule A — no source

```txt
if no audited sources:
    baseline_after = BASELINE_REQUIRES_SOURCE
    success = False
```

### Rule B — metadata only

```txt
if sources are metadata only:
    baseline_after = BASELINE_REQUIRES_DIRECT_SUPPORT
    success = False
```

### Rule C — formula only

```txt
if FORMULA_SUPPORT but no OBSERVABLE_SUPPORT:
    baseline_after = BASELINE_BACKGROUND_SUPPORTED
    success = False
```

### Rule D — formula + observable support

```txt
if FORMULA_SUPPORT and OBSERVABLE_SUPPORT and audit passed:
    baseline_after = BASELINE_SOURCE_BACKED_LIMITED
    success = True
```

### Rule E — ready baseline

```txt
if formula + observable + parameter + assumptions:
    baseline_after = BASELINE_SOURCE_BACKED_READY
    success = True
```

### Rule F — contradiction

```txt
if contradiction:
    baseline_after = BASELINE_CONTRADICTED
    success = False
```

## 4. Claim effects

If LIMITED:

Allowed:

```txt
CAMPAIGN-002 now has a source-backed limited baseline.
```

Still blocked:

```txt
Phygn predicts gravitational decoherence.
The candidate is validated.
SyntheticGain is physical PredictiveGain.
Frontera C is proven.
```

If READY:

Allowed:

```txt
The baseline is ready for limited source-backed comparison.
```

Still blocked:

```txt
Candidate physical prediction, unless candidate and benchmark are also source-backed.
```

## 5. Reports

Generate:

```txt
reports/campaigns/CAMPAIGN-002_baseline_upgrade_attempt_v0_9.md
reports/model_comparison/baseline_upgrade_attempt_v0_9.md
```

## 6. Tests

```txt
tests/test_baseline_upgrade_attempt_v0_9.py
```

Cases:

```txt
test_no_sources_keeps_baseline_requires_source
test_metadata_only_does_not_upgrade
test_formula_only_does_not_make_limited_baseline
test_formula_and_observable_support_upgrades_to_limited
test_parameter_and_assumptions_upgrade_to_ready
test_contradiction_blocks_upgrade
test_limited_baseline_does_not_unlock_candidate_prediction
```

## 7. Final principle

```txt
Un intento fallido con razones claras vale más que un éxito inflado.
```
