# Phygn v0.6 Model Comparison Results

Date: 2026-06-29

Source prompts:

```txt
docs/32_PHYGN_V0_6_HISTORIC_GOAL_MODEL_COMPARISON.md
docs/33_PHYGN_CAMPAIGN_002_DECOHERENCE_MODEL_COMPARISON.md
docs/34_PHYGN_RAG_SOURCE_INGESTION_CAMPAIGN_V0_6.md
docs/35_PHYGN_MODEL_COMPARISON_ENGINE_ARCHITECTURE.md
docs/36_PHYGN_NON_INFLATION_CLAIM_PROTOCOL_V0_6.md
docs/37_PHYGN_CODEX_V0_6_MODEL_COMPARISON_PROMPT.md
```

## 1. Completion Status

Status: **COMPLETE UNDER THE v0.6 PROMPT ACCEPTANCE CRITERIA**

The v0.6 work is implemented and verified:

- Model comparison engine exists.
- CAMPAIGN-002 Decoherence Model Comparison runs in toy mode.
- Default toy comparison inherits CAMPAIGN-001 negative bound.
- `Gain_C` remains undefined when `y_true` is absent.
- Detectability is classified.
- Decoherence prediction overclaim is blocked.
- Non-inflation claim protocol blocks level jumps.
- RAG source ingestion tasks are created without invented citations.
- Campaign, model-comparison and RAG reports are generated.
- Test suite passes.

Important limitation:

```txt
No physical decoherence prediction is claimed.
No Frontera C validation is claimed.
No source ingestion is claimed.
No empirical actionability is claimed.
```

## 2. Implemented Core Modules

### Model Comparison

```txt
phyng/model_comparison/__init__.py
phyng/model_comparison/schemas.py
phyng/model_comparison/models.py
phyng/model_comparison/metrics.py
phyng/model_comparison/detectability.py
phyng/model_comparison/comparison.py
phyng/model_comparison/report.py
```

Implemented capabilities:

- `ModelComparisonSpec`
- `ModelComparisonResult`
- `BoundaryCouplingSpec`
- `run_model_comparison(...)`
- `generate_model_comparison_report(...)`
- `mse(...)`, `mae(...)`, `rmse(...)`
- `compute_predictive_gain(...)`
- `classify_detectability(...)`

### Campaign 002

```txt
phyng/campaigns/campaign_002_decoherence.py
```

Implemented capabilities:

- `Campaign002Input`
- `Campaign002Result`
- `build_campaign_002_spec(...)`
- `create_campaign_002_research_tasks(...)`
- `run_campaign_002_decoherence_model_comparison(...)`
- `generate_campaign_002_report(...)`
- `generate_foundational_source_ingestion_reports(...)`

### Claim Non-Inflation

```txt
phyng/campaigns/non_inflation.py
```

Implemented capabilities:

- `CLAIM_LEVELS`
- `evaluate_claim_level(...)`

### API Extensions

```txt
phyng/api.py
```

Added endpoints:

```txt
POST /model-comparison/run
GET  /campaigns/decoherence-model-comparison
POST /campaigns/decoherence-model-comparison/run
```

## 3. CAMPAIGN-002 Default Input

```txt
campaign_id = CAMPAIGN-002
comparison_id = CAMPAIGN-002_default_toy_comparison
system_id = SYS-MESO-NANOPARTICLE
observable = visibility_loss
gamma_base = 0.05
alpha = 1.0
B = 7.426160269118667e-38
QB = 2.612280302374279e-56
epsilon_exp = 1e-6
y_true = None
error_metric = MSE
```

Inherited CAMPAIGN-001 status:

```txt
region = NEGATIVE_GRAVITY_BOUND
direct gravitational decoherence overclaims remain blocked
```

## 4. Model Comparison Result

Default toy equations:

```txt
V_base(t) = exp(-gamma_base * t)
V_C(t) = exp(-(gamma_base + alpha * B) * t)
```

Default result:

| Quantity | Value |
|---|---:|
| Series points | `11` |
| `max_abs_delta` | `0.000000e+00` |
| `epsilon_exp` | `1e-6` |
| Detectability | `UNDETECTABLE_DIFFERENCE` |
| `error_base` | `undefined without y_true` |
| `error_candidate` | `undefined without y_true` |
| `Gain_C` | `undefined without y_true` |
| Predictive status | `MODEL_DELTA_ONLY` |
| Evidence level | `3` |
| Maximum allowed claim level | `3` |

Interpretation:

```txt
The default CAMPAIGN-002 run produces a toy-model comparison surface only.
Because y_true is absent, Predictive Gain is not computed.
Because the default delta is below epsilon_exp, the toy difference is classified as undetectable.
```

## 5. Allowed And Blocked Claims

Allowed limited claims:

```txt
The candidate produces a computed toy delta under explicit assumptions.
The candidate toy delta is below the selected detectability threshold.
```

Blocked claims:

```txt
Phygn predicts gravitational decoherence.
Boundary C causes decoherence.
The invariant explains decoherence.
This validates Frontera C.
```

Safe rewrite:

```txt
Phygn computes a toy model delta under explicit assumptions.
No physical decoherence prediction is claimed.
```

## 6. RAG Status

RAG source status:

```txt
AWAITING_SOURCE_INGESTION
```

Created research tasks:

| Task ID | Purpose | Status |
|---|---|---|
| `RT-CAMPAIGN-002-SRC-DECOH-001` | Standard decoherence visibility decay grounding | `AWAITING_SOURCE_INGESTION` |
| `RT-CAMPAIGN-002-SRC-DECOH-002` | Environmental decoherence in matter-wave interferometry grounding | `AWAITING_SOURCE_INGESTION` |
| `RT-CAMPAIGN-002-SRC-DECOH-003` | Experimental visibility threshold grounding | `AWAITING_SOURCE_INGESTION` |
| `RT-CAMPAIGN-002-SRC-DECOH-004` | Benchmark or `y_true` data grounding | `AWAITING_SOURCE_INGESTION` |

No source ingestion is asserted by this result document.

## 7. Claim Non-Inflation Result

The evidence ladder is enforced:

```txt
evidence_level = 3
requested_claim_level = 6
decision = BLOCKED_OVERCLAIM
```

This prevents a toy delta from being promoted into a detectable physical candidate prediction.

## 8. Generated Reports

Generated artifacts:

```txt
reports/campaigns/CAMPAIGN-002_decoherence_model_comparison.md
reports/model_comparison/CAMPAIGN-002_default_toy_comparison.md
reports/rag/foundational_source_ingestion.md
reports/rag/source_claim_matrix.md
reports/rag/claims_awaiting_sources.md
```

Generated RAG task records:

```txt
rag/research_tasks/RT-CAMPAIGN-002-SRC-DECOH-001.json
rag/research_tasks/RT-CAMPAIGN-002-SRC-DECOH-002.json
rag/research_tasks/RT-CAMPAIGN-002-SRC-DECOH-003.json
rag/research_tasks/RT-CAMPAIGN-002-SRC-DECOH-004.json
```

## 9. Tests

Latest verification:

```txt
pytest -q
125 passed
```

Relevant v0.6 tests:

```txt
tests/test_model_comparison_metrics.py
tests/test_model_comparison_engine.py
tests/test_model_comparison_detectability.py
tests/test_model_comparison_report.py
tests/test_campaign_002_decoherence.py
tests/test_non_inflation_claim_protocol.py
tests/test_rag_source_ingestion_campaign.py
```

Covered behaviors:

- MSE, MAE and RMSE metrics.
- Predictive Gain formula.
- `Gain_C` remains `None` without `y_true`.
- Positive toy gain is computed only when benchmark data is provided.
- Detectability requires or applies `epsilon_exp`.
- CAMPAIGN-002 runs in toy mode.
- Decoherence prediction overclaim is blocked.
- Campaign reports are generated.
- Missing sources create research tasks.
- Non-inflation protocol blocks unsupported claim-level jumps.

API import check:

```txt
phyng.api imported successfully
/campaigns/decoherence-model-comparison route registered = True
```

## 10. Final Answer

Yes: `docs/32_PHYGN_V0_6_HISTORIC_GOAL_MODEL_COMPARISON.md` is complete under the v0.6 acceptance criteria.

The result is:

```txt
Phygn v0.6 now has a toy model-comparison engine and CAMPAIGN-002.
The default run compares an exponential visibility baseline against a boundary-aware toy candidate.
For the inherited CAMPAIGN-001 negative bound, the default toy delta is below detectability.
Gain_C is undefined because y_true is absent.
The result is MODEL_DELTA_ONLY at evidence level 3.
All physical decoherence, causation and validation claims remain blocked.
RAG tasks were created for the missing sources and benchmark evidence.
```
