# Phygn v3.0 — Real Source Campaign Report & Loop Feedback

## 0. Purpose

This document defines the required reports and closed-loop feedback for v3.0.

---

## 1. Required reports

Generate:

```txt
reports/real_source_acquisition/phi_gradient_query_plan_v3_0.md
reports/real_source_acquisition/phi_gradient_source_candidate_manifest_v3_0.md
reports/real_source_acquisition/phi_gradient_extract_validation_v3_0.md
reports/real_source_acquisition/phi_gradient_slot_coverage_v3_0.md
reports/real_source_acquisition/phi_gradient_negative_sources_v3_0.md
reports/real_source_acquisition/phi_gradient_benchmark_comparability_v3_0.md
reports/real_source_acquisition/phi_gradient_real_source_gate_v3_0.md
reports/real_source_acquisition/phi_gradient_loop_feedback_v3_0.md
reports/campaigns/PHI-GRADIENT-REAL-SOURCE-ACQUISITION-v3_0.md
```

---

## 2. Final status report must include

```txt
campaign status
actual_real_sources_acquired
actual_real_extracts_validated
slot coverage matrix
accepted sources
rejected analogy-only sources
negative/conflicting sources
benchmark comparable records
alpha/Gamma_env/m/L/t constraints
canonical status
allowed claims
blocked claims
next actions
discipline note
```

---

## 3. Allowed outcomes

If source-backed limited:

```txt
Allowed:
- PHI_GRADIENT has limited real source pressure for specific components.
- Candidate may proceed to benchmark comparison campaign.

Blocked:
- physical prediction
- Frontera C validation
- experimental confirmation
```

If benchmark data found:

```txt
Allowed:
- PHI_GRADIENT has comparable real benchmark pressure.
- Candidate may proceed to parameter-alignment and benchmark comparison.

Blocked:
- experimental validation
- physical prediction
```

If inconclusive:

```txt
Allowed:
- acquisition campaign completed or attempted.
- missing slots identified.

Blocked:
- source-backed claim
- benchmark-supported claim
```

If contradicted:

```txt
Allowed:
- contradiction report
- post-mortem
- candidate down-ranking proposal

Blocked:
- claim promotion
```

---

## 4. Loop feedback

Possible updates:

```txt
increase source-search priority for missing slots
schedule benchmark comparison if benchmark found
schedule parameter-alignment if alpha/Gamma_env constraints found
down-rank candidate if contradicted
select next candidate family if acquisition fails
```

Always blocked:

```txt
physical claim authorization
Frontera C validation
experimental confirmation
source requirement reduction
benchmark requirement reduction
canonical permission semantic change
```

---

## 5. Final principle

```txt
The campaign does not need to confirm PHI_GRADIENT.
It needs to make the next ignorance precise.
```
