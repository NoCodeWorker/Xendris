# Codex Prompt — Phygn v0.5 Invariant Boundary Atlas Campaign

You are working in:

```txt
d:\BIOCULTOR\PHYNG\
```

Project:

```txt
Phygn — Physical Signatures Lab
```

Current state:

```txt
v0.4 loop is implemented.
RAG MVP exists.
Claim linker exists.
Gap detection exists.
Reports exist.
99/99 tests have passed.
```

Your task is to implement **v0.5: Invariant Boundary Atlas + CAMPAIGN-001 Mesoscopic Boundary Number**.

This is a core scientific development task.

Do not work on styling.  
Do not work on frontend unless a minimal docs link is needed.  
Do not invent sources.  
Do not claim new physics.

---

# 1. Read first

Read:

```txt
docs/22_PHYGN_V0_5_GOAL_INVARIANT_BOUNDARY_ATLAS.md
docs/23_PHYGN_CAMPAIGN_001_MESOSCOPIC_BOUNDARY_NUMBER.md
docs/24_PHYGN_BOUNDARY_EXCLUSION_ATLAS_ARCHITECTURE.md
docs/25_PHYGN_NON_TRIVIALITY_AND_FALSIFIABILITY_PROTOCOL.md
docs/26_PHYGN_CAMPAIGN_RAG_SOURCE_PLAN_v0_5.md
```

Also read:

```txt
docs/18_PHYGN_CONTINUOUS_CORE_DEVELOPMENT_LOOP_v0_4.md
docs/20_PHYGN_RAG_RESEARCH_FEEDBACK_LOOP_v0_4.md
```

---

# 2. First action

Run:

```bash
pytest -v
```

If tests fail, fix tests/core first.

---

# 3. Mission

Implement:

```txt
Boundary Exclusion Atlas
CAMPAIGN-001 Mesoscopic Boundary Number
Non-triviality classifier
Campaign reports
RAG research tasks for missing sources
Tests
```

---

# 4. New modules

Create:

```txt
phyng/atlas/
  __init__.py
  schemas.py
  atlas_point.py
  region_classifier.py
  exclusion_rules.py
  atlas_builder.py
  atlas_report.py

phyng/campaigns/
  __init__.py
  schemas.py
  mesoscopic_boundary_number.py
  campaign_runner.py
  campaign_report.py
  non_triviality.py
```

---

# 5. Reports directories

Ensure:

```txt
reports/atlas/
reports/campaigns/
```

---

# 6. Atlas implementation

Implement:

```python
build_atlas(...)
classify_region(...)
generate_exclusion_claims(...)
generate_atlas_report(...)
```

Use existing:

```txt
frontier_lengths.py
operational_scale.py
signature.py
claim_gatekeeper.py
rag modules
loop modules
```

Do not duplicate physics calculations.

---

# 7. Campaign implementation

Implement:

```python
run_mesoscopic_boundary_campaign(...)
```

Input defaults:

```txt
m_kg = 1e-17
L_value_m = 1e-7
L_type = L_INT
physical_role = interferometric path separation or characteristic localization scale
observer_channel = matter-wave interference readout
arbitrariness_risk = LOW or MEDIUM if justification is not source-backed
```

If sources are missing:

```txt
create ResearchTasks
mark source-dependent claims REQUIRES_SOURCE
do not block the numerical calculation
block hard interpretation
```

---

# 8. Required calculations

Campaign must calculate:

```txt
lambda_C
r_g
R_S
Q
B
QB
planck_ratio_squared
delta_QB
logQ
logB
u
w
```

Validate:

```txt
QB = (ℓP/L)^2
```

---

# 9. Region classification

At minimum:

```txt
NEGATIVE_GRAVITY_BOUND
QUANTUM_BOUNDARY
GRAVITATIONAL_BOUNDARY
PLANCK_CROSSING
CLASSICAL_ACCESSIBLE
AD_HOC_SCALE_BLOCKED
```

For default campaign, expect:

```txt
NEGATIVE_GRAVITY_BOUND
```

unless current thresholds disagree. If thresholds disagree, report clearly.

---

# 10. Non-triviality classifier

Implement:

```python
classify_non_triviality(...)
```

Outputs:

```txt
TRIVIAL_STRUCTURAL
STRUCTURAL_USEFUL
NEGATIVE_NONTRIVIAL
PREDICTIVE_NONTRIVIAL
EMPIRICALLY_ACTIONABLE
```

Default campaign should likely classify as:

```txt
NEGATIVE_NONTRIVIAL
```

only if it blocks a specific overclaim and generates reproducible bound.

Otherwise:

```txt
STRUCTURAL_USEFUL
```

Do not inflate.

---

# 11. Claims

Allowed claim:

```txt
For the selected m and L, Phygn computes a negative bound showing that B = rg/L is negligible.
```

Blocked claim:

```txt
Phygn predicts new gravitational decoherence.
```

Required action for blocked claim:

```txt
Requires dynamic decoherence model comparison, source support, benchmark and Predictive Gain.
```

---

# 12. RAG tasks

Ensure ResearchTasks are created for missing sources:

```txt
Compton wavelength
Schwarzschild/gravitational radius
Planck scale
Compton-Schwarzschild diagram
MAQRO-like mesoscopic interferometry
decoherence models if decoherence claims are evaluated
```

Do not pretend to ingest sources unless actual source data exists.

---

# 13. Tests

Add:

```txt
tests/test_atlas_point.py
tests/test_atlas_region_classifier.py
tests/test_atlas_builder.py
tests/test_atlas_report.py
tests/test_campaign_mesoscopic_boundary_number.py
tests/test_campaign_non_triviality.py
```

Minimum tests:

```txt
test_atlas_point_qb_identity
test_log_coordinates_valid
test_negative_gravity_bound_region
test_ad_hoc_scale_blocks_claims
test_mesoscopic_campaign_computes_signature
test_mesoscopic_campaign_blocks_decoherence_overclaim
test_mesoscopic_campaign_creates_research_tasks
test_campaign_report_generated
test_non_triviality_not_inflated
```

---

# 14. Reports

Generate:

```txt
reports/atlas/invariant_boundary_atlas.md
reports/atlas/atlas_points.json
reports/atlas/claim_exclusion_matrix.md
reports/campaigns/CAMPAIGN-001_mesoscopic_boundary_number.md
reports/campaigns/CAMPAIGN-001_citation_audit.md
```

Reports must include:

```txt
inputs
formulas
results
region
non-triviality status
allowed claims
blocked claims
RAG status
tests
next tasks
```

---

# 15. Optional API

Only if safe:

```txt
GET /atlas
POST /atlas/build
GET /campaigns/mesoscopic-boundary-number
POST /campaigns/mesoscopic-boundary-number/run
```

Do not break existing API.

---

# 16. Acceptance criteria

Complete when:

```txt
pytest -v passes
Boundary Atlas builds
CAMPAIGN-001 runs
QB identity validated
default campaign classifies region
overclaim about decoherence blocked
RAG tasks created for missing sources
reports generated
non-triviality classifier does not inflate result
```

---

# 17. Final discipline

Do not seek glory in the wording.

Seek irreversibility in the logic.

```txt
The invariant is the pillar.
The atlas is the machine.
The campaign is the first number.
The gatekeeper is the immune system.
The RAG is the memory of evidence.
The tests are the judge.
```
