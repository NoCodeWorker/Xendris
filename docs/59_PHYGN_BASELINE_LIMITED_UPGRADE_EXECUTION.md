# Phygn v1.0 — Baseline Limited Upgrade Execution

## 0. Propósito

Este documento define la ejecución formal para intentar:

```txt
BASELINE_REQUIRES_SOURCE
→ BASELINE_SOURCE_BACKED_LIMITED
```

---

## 1. Campaign ID

```txt
BASELINE-SRC-PACK-001
```

Linked campaign:

```txt
CAMPAIGN-002
```

---

## 2. Pipeline

```txt
scan sources/baseline/
→ load source_manifest.json
→ register SourceCandidates
→ check local files
→ parse or read local content
→ run CitationAudit
→ create SourceRecords
→ create ClaimSourceLinks
→ build BaselineSourcePack
→ build support matrix
→ run BaselineUpgradeAttempt
→ update CAMPAIGN-002 readiness
→ generate reports
```

---

## 3. Minimum support

To upgrade to:

```txt
BASELINE_SOURCE_BACKED_LIMITED
```

Need:

```txt
FORMULA_SUPPORT
OBSERVABLE_SUPPORT
PASSED_LIMITED audit
HIGH or PRIMARY trust
no active contradiction
```

---

## 4. Optional support

To upgrade to:

```txt
BASELINE_SOURCE_BACKED_READY
```

Need additionally:

```txt
PARAMETER_SUPPORT
assumption support
unit support
parameter status not arbitrary
```

v1.0 does not require READY.

---

## 5. Claim result if LIMITED

Allowed:

```txt
CAMPAIGN-002 has a source-backed limited visibility/coherence decay baseline.
```

Blocked:

```txt
Phygn predicts gravitational decoherence.
Frontera C is validated.
The boundary-aware candidate is validated.
SyntheticGain is physical PredictiveGain.
```

---

## 6. Claim result if still blocked

Allowed:

```txt
The baseline upgrade attempt failed because evidence was insufficient.
```

Blocked:

```txt
Any source-backed baseline claim.
```

---

## 7. BaselineUpgradeExecutionResult

```python
class BaselineUpgradeExecutionResult(BaseModel):
    execution_id: str
    campaign_id: str
    linked_campaign_id: str
    source_pack_status: str
    audited_sources_count: int
    formula_support_count: int
    observable_support_count: int
    parameter_support_count: int
    contradiction_count: int
    baseline_before: str
    baseline_after: str
    upgrade_success: bool
    max_claim_level: int
    allowed_claims: list[str]
    blocked_claims: list[str]
    report_paths: list[str]
```

---

## 8. Tests

```txt
tests/test_baseline_limited_upgrade_execution.py
```

Cases:

```txt
test_execution_empty_sources_fails_honestly
test_execution_url_only_sources_do_not_upgrade
test_execution_formula_observable_sources_upgrade_limited
test_execution_contradiction_blocks_upgrade
test_execution_limited_baseline_does_not_validate_candidate
test_execution_reports_generated
```

---

## 9. Reports

Generate:

```txt
reports/campaigns/BASELINE-SRC-PACK-001_ingestion_result.md
reports/campaigns/CAMPAIGN-002_baseline_upgrade_attempt_v1_0.md
reports/model_comparison/CAMPAIGN-002_source_backed_baseline_status_v1_0.md
reports/rag/baseline_source_pack_v1_0.md
reports/rag/baseline_support_matrix_v1_0.md
reports/rag/citation_audit_v1_0.md
```

---

## 10. Dashboard reflection

Dashboard should display:

```txt
Baseline Source Pack Status
Audited Sources Count
Formula Support
Observable Support
Baseline After
Upgrade Success
Still Blocked Claims
Next Evidence Needed
```

---

## 11. Final principle

```txt
El primer upgrade permitido debe ser pequeño, limitado y reversible.
```
