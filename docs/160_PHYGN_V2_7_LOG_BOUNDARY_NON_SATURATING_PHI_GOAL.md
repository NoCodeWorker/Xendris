# Phygn v2.7 — LOG_BOUNDARY Non-Saturating Phi Search & Control-Resistant Candidate Design Goal

## 0. Context

The latest confirmed document is:

```txt
159_PHYGN_V2_6_LOG_BOUNDARY_SENSITIVITY_ABLATION_RESULTS.md
```

Therefore, v2.7 starts at:

```txt
160
```

v2.6 classified the current LOG_BOUNDARY phi formulation as:

```txt
LOG_BOUNDARY_SIGNAL_IS_SATURATION_ARTIFACT
```

Key diagnostic facts:

```txt
candidate_delta == constant_phi_delta
control_gain == 0.0
saturation_ratio == 1.0
```

Meaning:

```txt
The current phi formulation does not earn source-pressure priority.
The large synthetic delta was explained by phi saturation and the constant phi=1 control.
```

---

## 1. Core thesis

```txt
A candidate that only wins by becoming a constant has not won.
It has disappeared.
```

v2.7 searches for alternative LOG_BOUNDARY phi functions that:

```txt
do not saturate trivially
do not match constant controls
depend meaningfully on log-boundary coordinates
survive coordinate removal controls
survive threshold robustness checks
remain bounded and dimensionless
```

---

## 2. Hard rule

```txt
No phi saturation.
No constant-control match.
No threshold-tuning dependency.
No coordinate-removal survival.
No source-pressure upgrade without ablation survival.
```

---

## 3. Candidate families

v2.7 must generate and evaluate alternative phi families:

```txt
PHI_CENTERED
PHI_GRADIENT
PHI_BANDPASS
PHI_CURVATURE
PHI_RELATIVE_BOUNDARY
PHI_NON_SATURATING_RATIO
PHI_COORDINATE_CONTRAST
PHI_LOCALIZED_WINDOW
```

These are synthetic candidate functions, not physical laws.

---

## 4. Required checks

Every candidate phi must pass:

```txt
dimensionless input check
bounded output check
non-saturation check
constant-control comparison
coordinate contribution check
threshold robustness check
alpha sensitivity check
finite numerical execution
canonical status mapping
blocked physical claims
```

---

## 5. Possible outcomes

```txt
PHI_CANDIDATE_SURVIVES_CONTROLS
PHI_CANDIDATE_FAILS_CONSTANT_CONTROL
PHI_CANDIDATE_SATURATES
PHI_CANDIDATE_FAILS_COORDINATE_CONTRIBUTION
PHI_CANDIDATE_REQUIRES_THRESHOLD_TUNING
PHI_CANDIDATE_NUMERICALLY_UNSTABLE
PHI_SEARCH_NO_SURVIVOR
```

---

## 6. Canonical interpretation

If a candidate survives controls:

```txt
CanonicalPermission: CLAIM_LIMITED_ALLOWED
Evidence: SYNTHETIC_ONLY
Support: SYNTHETIC
Blocked: MISSING_SOURCE_SUPPORT, MISSING_BENCHMARK, MISSING_EXPERIMENTAL_DATA
```

If all candidates fail:

```txt
CanonicalPermission: CLAIM_BLOCKED
Evidence: SYNTHETIC_ONLY
Support: SYNTHETIC
Blocked: UNPHYSICAL_PARAMETER or HUMAN_REVIEW_REQUIRED
```

No physical validation may be authorized.

---

## 7. Acceptance criteria

v2.7 is complete when:

```txt
non-saturating phi candidate schemas exist
candidate generator exists
candidate evaluation suite exists
constant control comparison exists
coordinate ablation comparison exists
threshold robustness check exists
ranking exists
reports generated
loop feedback generated
tests pass
physical claims remain blocked
```

---

## 8. Final principle

```txt
A useful phi must create structure, not hide as amplitude.
```
