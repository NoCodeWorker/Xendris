# Phygn v4.9 — Reporting & Next Gate

## 0. Purpose

This document defines reporting and next-gate decisions for the source identity preflight.

---

## 1. Required reports

Generate:

```txt
reports/preflight/source_identity/candidate_family_source_inventory_v4_9.md
reports/preflight/source_identity/source_identity_resolution_matrix_v4_9.md
reports/preflight/source_identity/source_availability_matrix_v4_9.md
reports/preflight/source_identity/observable_identity_matrix_v4_9.md
reports/preflight/source_identity/ytrue_path_plausibility_matrix_v4_9.md
reports/preflight/source_identity/candidate_preflight_decision_matrix_v4_9.md
reports/preflight/source_identity/source_identity_preflight_gate_v4_9.md
reports/campaigns/PHYGN-SOURCE-IDENTITY-PREFLIGHT-GATE-v4_9.md
```

---

## 2. Gate output

Create:

```txt
data/preflight/source_identity/source_identity_preflight_gate_v4_9.json
```

Schema:

```python
class SourceIdentityPreflightGate(BaseModel):
    gate_id: str
    final_status: str
    candidate_count: int
    passed_candidate_count: int
    partial_candidate_count: int
    failed_candidate_count: int
    selected_candidate_family: str | None
    allowed_next_phase: str | None
    blocked_next_phases: list[str]
    required_before_next_pipeline: list[str]
    blocked_claims: list[str]
    allowed_claims: list[str]
    notes: list[str]
```

---

## 3. Next phase mapping

If a candidate passes:

```txt
v5.0 — Selected Candidate Minimal Source/y_true Campaign
```

If candidates are partial only:

```txt
v5.0 — Targeted Source Acquisition and Human Lookup Sprint
```

If none pass:

```txt
v5.0 — Candidate Family Reprioritization / External Source Strategy
```

If source identity is globally weak:

```txt
v5.0 — Literature Identity Acquisition Campaign
```

---

## 4. Canonical statuses

Add:

```txt
PHYGN_SOURCE_IDENTITY_PREFLIGHT_COMPLETED
PHYGN_SOURCE_IDENTITY_PREFLIGHT_BLOCKED_MISSING_PRIOR_RESULTS
PHYGN_SOURCE_IDENTITY_PREFLIGHT_NO_CANDIDATE_PASSED
PHYGN_SOURCE_IDENTITY_PREFLIGHT_CANDIDATE_PASSED
PHYGN_SOURCE_IDENTITY_PREFLIGHT_REQUIRES_SOURCE_ACQUISITION
PHYGN_SOURCE_IDENTITY_PREFLIGHT_REQUIRES_HUMAN_LOOKUP
```

Suggested mapping if candidate passed:

```txt
Canonical Permission: REVIEW_REQUIRED
Evidence Level: SOURCE_IDENTITY_PREFLIGHT_ONLY
Support Level: NOT_YET_SUPPORTED
Risk Level: SCIENTIFIC_RISK
```

Suggested mapping if none passed:

```txt
Canonical Permission: CLAIM_BLOCKED
Evidence Level: NO_RESOLVABLE_SOURCE_IDENTITY
Support Level: UNSUPPORTED
Risk Level: SCIENTIFIC_RISK
```

---

## 5. Allowed claims

Allowed:

```txt
Candidate families were screened for resolvable source identity.
A candidate passed/failed/was partial according to source identity preflight.
A next source acquisition or minimal campaign was permitted by gate.
```

Blocked:

```txt
Any candidate is validated.
Any candidate has PredictiveGain.
Any candidate is empirically supported.
Source identity preflight creates y_true.
Source identity preflight creates physical validation.
```

---

## 6. Final principle

```txt
Do not build a cathedral on a rumor of a source.
```
