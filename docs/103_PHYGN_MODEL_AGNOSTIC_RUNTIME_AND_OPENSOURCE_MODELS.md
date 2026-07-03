# Phygn v1.7 — Model-Agnostic Runtime & Open-Source Models

## 0. Purpose

Phygn must not depend on frontier LLMs.

It should work with:

```txt
frontier APIs
open-source LLMs
local models
small specialized classifiers
embedding models
rule-based validators
deterministic scientific gates
human review
```

The core architecture must be:

```txt
model-agnostic
auditable
replaceable
degradable
```

---

## 1. Core rule

```txt
LLM proposes.
Phygn verifies.
```

The model is not the authority.

Authority comes from:

```txt
sources
benchmarks
metrics
gates
risk rules
post-mortems
audit trails
```

---

## 2. ModelBackend interface

```python
class ModelBackend(Protocol):
    backend_id: str
    model_name: str
    model_type: str
    supports_json_mode: bool
    supports_tool_use: bool
    context_window_tokens: int | None

    def generate(self, prompt: str, schema: dict | None = None) -> ModelResponse:
        ...
```

---

## 3. Backend types

```txt
FRONTIER_API
OPEN_SOURCE_API
LOCAL_LLM
SMALL_CLASSIFIER
EMBEDDING_MODEL
RULE_BASED
HUMAN_REVIEW
```

---

## 4. Capability-aware routing

Phygn should route tasks based on difficulty and risk.

Examples:

```txt
idea brainstorming -> any competent local/open model
claim extraction -> medium LLM + deterministic validation
source audit -> stronger model or human review
financial action -> deterministic gates + human approval
automated execution -> never model-only
```

---

## 5. Open-source compatibility

Phygn can work with open-source models if:

```txt
outputs are treated as proposals
schemas validate output
unsupported claims are blocked
source citations are verified externally
high-risk decisions require deterministic gates
```

Open-source models may be enough for:

```txt
idea intake
hypothesis seed generation
proxy suggestion
extract summarization draft
report drafting
initial claim extraction
```

They should not alone authorize:

```txt
physical prediction
financial recommendation
automated execution
medical/legal claims
```

---

## 6. Degradation modes

If model quality is low:

```txt
increase friction
require more user confirmation
require source-backed extraction
route to human review
limit to DREAM/HYPOTHESIS modes
disable execution/action modes
```

Statuses:

```txt
MODEL_FULLY_ALLOWED_FOR_LOW_RISK
MODEL_ALLOWED_WITH_VALIDATION
MODEL_REQUIRES_HUMAN_REVIEW
MODEL_BLOCKED_FOR_HIGH_RISK
```

---

## 7. Anti-hallucination stance

Do not claim:

```txt
Phygn eliminates hallucinations completely.
```

Correct:

```txt
Phygn prevents unsupported model outputs from becoming authorized claims/actions.
```

---

## 8. Reports

Generate:

```txt
reports/model_runtime/model_backend_registry_v1_7.md
reports/model_runtime/opensource_model_mode_v1_7.md
reports/model_runtime/capability_routing_v1_7.md
```

---

## 9. Final principle

```txt
The weaker the model, the stronger the gate must be.
```
