# Phygn v4.8 — Reporting & Next Gate

## 0. Purpose

This document defines reporting and next-gate logic after the PHI_CURVATURE minimal campaign.

---

## 1. Required reports

Generate:

```txt
reports/phi_curvature/sources/phi_curvature_source_resolution_v4_8.md
reports/phi_curvature/sources/phi_curvature_source_availability_v4_8.md
reports/phi_curvature/evidence/phi_curvature_candidate_observables_v4_8.md
reports/phi_curvature/evidence/phi_curvature_ytrue_candidates_v4_8.md
reports/phi_curvature/evidence/phi_curvature_accepted_ytrue_v4_8.md
reports/phi_curvature/evidence/phi_curvature_rejected_ytrue_v4_8.md
reports/phi_curvature/evidence/phi_curvature_evidence_audit_trail_v4_8.md
reports/phi_curvature/datasets/phi_curvature_minimal_ytrue_dataset_v4_8.md
reports/phi_curvature/next/phi_curvature_v4_8_next_gate_decision.md
reports/campaigns/PHI-CURVATURE-MINIMAL-SOURCE-YTRUE-CAMPAIGN-v4_8.md
```

---

## 2. Next gate decision

Create:

```txt
data/phi_curvature/next/phi_curvature_v4_8_next_gate_decision.json
```

Schema:

```python
class PhiCurvatureNextGateDecision(BaseModel):
    candidate_family: str
    final_status: str
    accepted_ytrue_count: int
    threshold_reached: bool
    source_resolution_summary: dict
    source_availability_summary: dict
    blocked_claims: list[str]
    allowed_claims: list[str]
    allowed_next_phase: str | None
    blocked_next_phases: list[str]
    required_before_predictive_gain: list[str]
    notes: list[str]
```

---

## 3. Next phase mapping

If threshold reached:

```txt
v4.9 — PHI_CURVATURE Minimal Benchmark Construction & Prediction Alignment
```

If some y_true found but threshold not reached:

```txt
v4.9 — PHI_CURVATURE Targeted y_true Expansion
```

If no y_true accepted but sources resolvable:

```txt
v4.9 — PHI_CURVATURE Human Table/Supplement Review
```

If sources unresolved/unavailable:

```txt
v4.9 — PHI_CURVATURE Source Acquisition Sprint
```

If no reality contact:

```txt
v4.9 — Candidate Reprioritization
```

---

## 4. Canonical statuses

Add:

```txt
PHI_CURVATURE_MINIMAL_CAMPAIGN_COMPLETED
PHI_CURVATURE_MINIMAL_CAMPAIGN_BLOCKED_MISSING_SCREEN
PHI_CURVATURE_MINIMAL_YTRUE_FOUND
PHI_CURVATURE_MINIMAL_YTRUE_THRESHOLD_REACHED
PHI_CURVATURE_NO_ACCEPTED_YTRUE_IN_MINIMAL_CAMPAIGN
PHI_CURVATURE_REQUIRES_TARGETED_SOURCE_DOWNLOAD
PHI_CURVATURE_REQUIRES_HUMAN_TABLE_REVIEW
PHI_CURVATURE_REJECTED_NO_RESOLVABLE_SOURCES
```

Suggested mapping if y_true found:

```txt
Canonical Permission: REVIEW_REQUIRED
Evidence Level: REAL_OBSERVED_YTRUE_PARTIAL
Support Level: LIMITED
Risk Level: SCIENTIFIC_RISK
```

Suggested mapping if no y_true:

```txt
Canonical Permission: REVIEW_REQUIRED
Evidence Level: SOURCE_ACCESSIBILITY_ONLY
Support Level: NOT_YET_SUPPORTED
Risk Level: SCIENTIFIC_RISK
```

Suggested mapping if sources unresolved:

```txt
Canonical Permission: CLAIM_BLOCKED
Evidence Level: NO_RESOLVABLE_SOURCE
Support Level: UNSUPPORTED
Risk Level: SCIENTIFIC_RISK
```

---

## 5. Allowed claims

Allowed:

```txt
PHI_CURVATURE minimal source/y_true campaign was performed.
Accepted y_true records were added only if QC passed.
PHI_CURVATURE may proceed only according to next gate.
```

Blocked:

```txt
PHI_CURVATURE is validated.
PHI_CURVATURE has PredictiveGain.
PHI_CURVATURE is empirically supported beyond accepted y_true records.
PHI_CURVATURE validates Frontera C.
PHI_CURVATURE confirms the invariant.
```

---

## 6. Final principle

```txt
Do not call the door a destination.
```
