# Codex Prompt — Phygn v0.6 Model Comparison Campaign

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
v0.5 complete.
Boundary Atlas exists.
CAMPAIGN-001 runs.
B = 7.43e-38 for m=1e-17 kg and L=1e-7 m.
Region = NEGATIVE_GRAVITY_BOUND.
Decoherence overclaim is blocked.
108 tests passed.
RAG tasks are awaiting source ingestion.
```

Your task is to implement **v0.6: From Negative Bound to Model Comparison**.

This is a core scientific task.

Do not work on styling.  
Do not claim new physics.  
Do not fake source ingestion.  
Do not pretend toy models are physical predictions.

---

# 1. Read first

Read:

```txt
docs/31_PHYGN_V0_6_HISTORIC_GOAL_MODEL_COMPARISON.md
docs/32_PHYGN_CAMPAIGN_002_DECOHERENCE_MODEL_COMPARISON.md
docs/33_PHYGN_RAG_SOURCE_INGESTION_CAMPAIGN_V0_6.md
docs/34_PHYGN_MODEL_COMPARISON_ENGINE_ARCHITECTURE.md
docs/35_PHYGN_NON_INFLATION_CLAIM_PROTOCOL_V0_6.md
```

Also read:

```txt
docs/27_PHYGN_CODEX_V0_5_CAMPAIGN_PROMPT.md
docs/25_PHYGN_NON_TRIVIALITY_AND_FALSIFIABILITY_PROTOCOL.md
docs/20_PHYGN_RAG_RESEARCH_FEEDBACK_LOOP_v0_4.md
```

---

# 2. First action

Run:

```bash
pytest -v
```

If tests fail, fix core first.

---

# 3. Mission

Implement:

```txt
model comparison engine
CAMPAIGN-002 Decoherence Model Comparison
toy visibility decay model
boundary-aware toy candidate
detectability classifier
Predictive Gain handling
non-inflation claim protocol
RAG source ingestion campaign scaffolding
reports
tests
```

---

# 4. New modules

Create:

```txt
phyng/model_comparison/
  __init__.py
  schemas.py
  models.py
  metrics.py
  detectability.py
  comparison.py
  report.py
```

Extend/create:

```txt
phyng/campaigns/campaign_002_decoherence.py
phyng/campaigns/non_inflation.py
```

---

# 5. Model comparison engine

Implement:

```txt
exponential_visibility
boundary_aware_visibility
mse
mae
rmse
compute_predictive_gain
classify_detectability
run_model_comparison
generate_model_comparison_report
```

Rules:

```txt
if y_true is None:
    gain_c = None
    predictive_status = MODEL_DELTA_ONLY

if epsilon_exp is None:
    detectability_status = DETECTABILITY_REQUIRES_EPSILON

if delta <= epsilon_exp:
    detectability_status = UNDETECTABLE_DIFFERENCE

if delta > epsilon_exp:
    detectability_status = DETECTABLE_TOY_DIFFERENCE
```

---

# 6. CAMPAIGN-002

Implement:

```python
run_campaign_002_decoherence_model_comparison(...)
```

Default safe mode:

```txt
TOY_MODEL_COMPARISON
```

Default observable:

```txt
visibility_loss
```

Default base model:

```txt
V_base(t)=exp(-gamma_base*t)
```

Default candidate:

```txt
V_C(t)=exp(-(gamma_base + delta_gamma_c)*t)
```

Where:

```txt
delta_gamma_c = alpha * B
```

Use CAMPAIGN-001 B if available.

Do not interpret physically.

---

# 7. Claims

Allowed:

```txt
The candidate produces a computed toy delta under explicit assumptions.
```

Allowed if delta below epsilon:

```txt
The candidate toy delta is below the selected detectability threshold.
```

Blocked:

```txt
Phygn predicts gravitational decoherence.
Boundary C causes decoherence.
The invariant explains decoherence.
This validates Frontera C.
```

Safe rewrite:

```txt
Phygn computes a toy model delta under explicit assumptions. No physical decoherence prediction is claimed.
```

---

# 8. RAG source ingestion campaign

Implement or extend research tasks for:

```txt
standard decoherence visibility decay
environmental decoherence matter-wave interferometry
Caldeira-Leggett model if referenced
Diósi-Penrose if referenced
MAQRO-like mesoscopic interferometry
experimental visibility thresholds
```

If no browsing/source file exists:

```txt
create ResearchTasks
do not mark SOURCE_INGESTED
```

---

# 9. Non-inflation protocol

Implement claim ladder:

```txt
LEVEL-0 calculation exists
LEVEL-1 structural identity validated
LEVEL-2 negative bound produced
LEVEL-3 toy model delta produced
LEVEL-4 toy benchmark gain produced
LEVEL-5 source-backed physical model comparison
LEVEL-6 detectable candidate prediction
LEVEL-7 empirically actionable proposal
```

Function:

```python
def evaluate_claim_level(evidence_level: int, requested_claim_level: int) -> ClaimLevelDecision:
    ...
```

If requested > evidence:

```txt
BLOCKED_OVERCLAIM
```

---

# 10. Reports

Generate:

```txt
reports/campaigns/CAMPAIGN-002_decoherence_model_comparison.md
reports/model_comparison/CAMPAIGN-002_default_toy_comparison.md
reports/rag/foundational_source_ingestion.md
reports/rag/source_claim_matrix.md
```

---

# 11. Tests

Add:

```txt
tests/test_model_comparison_metrics.py
tests/test_model_comparison_engine.py
tests/test_model_comparison_detectability.py
tests/test_model_comparison_report.py
tests/test_campaign_002_decoherence.py
tests/test_non_inflation_claim_protocol.py
tests/test_rag_source_ingestion_campaign.py
```

Minimum tests:

```txt
test_mse
test_mae
test_rmse
test_gain_none_without_y_true
test_gain_positive_when_candidate_better
test_detectability_requires_epsilon
test_delta_below_epsilon_is_undetectable
test_campaign_002_generates_toy_delta
test_campaign_002_blocks_decoherence_prediction
test_missing_sources_create_research_tasks
test_claim_level_overreach_blocked
test_report_generated
```

---

# 12. Optional API

Only if safe:

```txt
GET /model-comparison
POST /model-comparison/run
GET /campaigns/decoherence-model-comparison
POST /campaigns/decoherence-model-comparison/run
```

Do not break existing API.

---

# 13. Acceptance criteria

Complete when:

```txt
pytest -v passes
model comparison engine works
CAMPAIGN-002 runs in toy mode
Gain_C is None without y_true
detectability is classified
decoherence prediction overclaim is blocked
research tasks created for missing sources
reports generated
non-inflation protocol blocks claim level jumps
no physical prediction is claimed
```

---

# 14. Final discipline

This phase can become historic only if it refuses to cheat.

```txt
The invariant is the pillar.
The model comparison is the trial.
The benchmark is the judge.
The RAG is the evidence room.
The Gatekeeper is the law.
```

Build the trial.
