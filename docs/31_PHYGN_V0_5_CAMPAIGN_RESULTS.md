# Phygn v0.5 Campaign Results

Date: 2026-06-29

Source prompt:

```txt
docs/27_PHYGN_CODEX_V0_5_CAMPAIGN_PROMPT.md
```

## 1. Completion Status

Status: **COMPLETE UNDER THE PROMPT ACCEPTANCE CRITERIA**

The v0.5 campaign work is implemented and verified:

- Boundary Exclusion Atlas exists.
- CAMPAIGN-001 Mesoscopic Boundary Number runs.
- Required Q/B signature calculations are produced.
- QB identity is validated.
- Default campaign region is classified as `NEGATIVE_GRAVITY_BOUND`.
- Decoherence overclaim is blocked.
- Non-triviality is classified without inflating the result.
- RAG source tasks are created for missing evidence.
- Atlas and campaign reports are generated.
- Test suite passes.

Important limitation:

```txt
No new physics is claimed.
No source ingestion is claimed.
Source-dependent interpretations remain blocked or awaiting source ingestion.
```

## 2. Implemented Core Modules

### Atlas

```txt
phyng/atlas/__init__.py
phyng/atlas/schemas.py
phyng/atlas/atlas_point.py
phyng/atlas/region_classifier.py
phyng/atlas/exclusion_rules.py
phyng/atlas/atlas_builder.py
phyng/atlas/atlas_report.py
```

Implemented capabilities:

- `BoundaryAtlasPoint`
- `PhysicalSystemSpec`
- `BoundaryAtlas`
- `AtlasThresholds`
- `build_atlas(...)`
- `classify_region(...)`
- `generate_exclusion_claims(...)`
- `generate_atlas_report(...)`

### Campaigns

```txt
phyng/campaigns/__init__.py
phyng/campaigns/schemas.py
phyng/campaigns/mesoscopic_boundary_number.py
phyng/campaigns/campaign_runner.py
phyng/campaigns/campaign_report.py
phyng/campaigns/non_triviality.py
```

Implemented capabilities:

- `CampaignInput`
- `CampaignResult`
- `run_mesoscopic_boundary_campaign(...)`
- `run_campaign(...)`
- `generate_campaign_reports(...)`
- `classify_non_triviality(...)`

## 3. CAMPAIGN-001 Input

```txt
campaign_id = CAMPAIGN-001
system_id = SYS-MESO-NANOPARTICLE
m_kg = 1e-17
L_value_m = 1e-7
L_type = L_INT
physical_role = interferometric path separation or characteristic localization scale
observer_channel = matter-wave interference readout
```

Operational scale review:

```txt
ACCEPTED
Scale is justified and within bounds.
```

## 4. Numerical Result

CAMPAIGN-001 produced the following boundary signature:

| Quantity | Value |
|---|---:|
| Reduced Compton wavelength, `lambda_C` | `3.52e-26 m` |
| Gravitational radius, `r_g` | `7.43e-45 m` |
| Schwarzschild radius, `R_S` | `1.49e-44 m` |
| Quantum localization ratio, `Q` | `3.52e-19` |
| Gravity boundary ratio, `B` | `7.43e-38` |
| Product, `QB` | `2.61e-56` |
| Planck ratio squared, `(l_P/L)^2` | `2.61e-56` |
| Delta, `delta_QB` | `9.06e-72` |
| `logQ` | `-18.45` |
| `logB` | `-37.13` |
| `u` | `-27.79` |
| `w` | `-9.34` |

Invariant validation:

```txt
QB = (l_P/L)^2
validated within numerical precision
```

## 5. Region Classification

Default CAMPAIGN-001 classification:

```txt
NEGATIVE_GRAVITY_BOUND
```

Interpretation:

```txt
For the selected m and L, the direct gravitational boundary ratio B = r_g/L is negligible.
```

This is a negative bound, not a positive prediction.

## 6. Non-Triviality Result

Non-triviality status:

```txt
NEGATIVE_NONTRIVIAL
```

Reason:

```txt
The campaign generates a reproducible negative bound and blocks a specific overclaim.
```

The result is not classified as `PREDICTIVE_NONTRIVIAL` or `EMPIRICALLY_ACTIONABLE` because:

- no dynamic decoherence model comparison exists yet;
- no baseline/candidate model benchmark exists yet;
- `Gain_C` is not computed;
- primary sources are still awaiting ingestion.

## 7. Allowed And Blocked Claims

Allowed limited claim:

```txt
For the selected m and L, Phygn computes a negative bound showing that the direct gravitational boundary ratio B = r_g/L is negligible.
```

Blocked claims:

```txt
Phygn predicts gravitational decoherence.
The system is near a gravitational horizon.
Phygn predicts new gravitational decoherence.
```

Required before any decoherence prediction can be considered:

```txt
dynamic decoherence model comparison
source support
benchmark
Predictive Gain
```

## 8. Boundary Atlas Result

Generated atlas:

```txt
ATLAS-v0.5
version = 0.5.0
systems mapped = 5
```

Mapped systems:

| System ID | Region | Claim Status |
|---|---|---|
| `SYS-ELECTRON` | `QUANTUM_BOUNDARY` | `ALLOWED` |
| `SYS-PROTON` | `QUANTUM_BOUNDARY` | `ALLOWED` |
| `SYS-MESO-NANOPARTICLE` | `NEGATIVE_GRAVITY_BOUND` | `ALLOWED_LIMITED` |
| `SYS-PLANCK-LIMIT` | `PLANCK_CROSSING` | `ALLOWED` |
| `SYS-BLACK-HOLE-TOY` | `GRAVITATIONAL_BOUNDARY` | `ALLOWED` |

The atlas is a classification and exclusion machine. It does not validate Frontera C and does not prove new physics.

## 9. RAG Status

RAG source status:

```txt
AWAITING_SOURCE_INGESTION
```

Created research tasks:

| Task ID | Purpose | Status |
|---|---|---|
| `RT-CAMPAIGN-001-SRC-CAT-001` | Compton wavelength grounding | `AWAITING_SOURCE_INGESTION` |
| `RT-CAMPAIGN-001-SRC-CAT-002` | Schwarzschild/gravitational radius grounding | `AWAITING_SOURCE_INGESTION` |
| `RT-CAMPAIGN-001-SRC-CAT-003` | Planck scale grounding | `AWAITING_SOURCE_INGESTION` |
| `RT-CAMPAIGN-001-SRC-CAT-004` | Compton-Schwarzschild diagram grounding | `AWAITING_SOURCE_INGESTION` |
| `RT-CAMPAIGN-001-SRC-CAT-005` | Mesoscopic interferometry grounding | `AWAITING_SOURCE_INGESTION` |

No source ingestion is asserted by this result document.

## 10. Generated Reports

Generated campaign and atlas artifacts:

```txt
reports/atlas/invariant_boundary_atlas.md
reports/atlas/atlas_points.json
reports/atlas/claim_exclusion_matrix.md
reports/campaigns/CAMPAIGN-001_mesoscopic_boundary_number.md
reports/campaigns/CAMPAIGN-001_citation_audit.md
```

## 11. Tests

Latest verification:

```txt
pytest -v
108 passed
```

Relevant v0.5 tests:

```txt
tests/test_atlas_point.py
tests/test_atlas_region_classifier.py
tests/test_atlas_builder.py
tests/test_atlas_report.py
tests/test_campaign_mesoscopic_boundary_number.py
tests/test_campaign_non_triviality.py
```

Covered behaviors:

- QB identity validation.
- Log coordinate validation.
- Region classifier behavior.
- Atlas report artifact generation.
- CAMPAIGN-001 signature calculation.
- CAMPAIGN-001 region classification.
- Decoherence overclaim blocking.
- Missing-source research task creation.
- Campaign report generation.
- Non-triviality classification.

## 12. Final Answer

Yes: `docs/27_PHYGN_CODEX_V0_5_CAMPAIGN_PROMPT.md` is complete under its acceptance criteria.

The result is not a new physics claim. The result is:

```txt
Phygn v0.5 now has a reproducible Boundary Atlas and a CAMPAIGN-001 negative-bound calculation.
For m = 1e-17 kg and L = 1e-7 m, the direct gravitational boundary ratio is B = 7.43e-38.
The invariant QB = (l_P/L)^2 is validated.
The default region is NEGATIVE_GRAVITY_BOUND.
The decoherence prediction overclaim is blocked.
The result is NEGATIVE_NONTRIVIAL because it changes a claim decision.
Hard interpretation remains blocked until sources, dynamic models, benchmarks and Predictive Gain exist.
```
