"""
Phygn v1.7 — Model-Agnostic Runtime: Backend Registry & Routing

register_model_backend, route_model_task, evaluate_backend_permission.

Rule: The weaker the model, the stronger the gate must be.
"""

from __future__ import annotations

from phyng.model_runtime.schemas import (
    BackendRegistration,
    BackendPermission,
    ModelPermissionStatus,
    ModelType,
    TaskCategory,
)

# ---------------------------------------------------------------------------
# Task risk classification
# ---------------------------------------------------------------------------

# Tasks allowed for any model type (low-risk, proposals only)
_LOW_RISK_TASKS: set[TaskCategory] = {
    "idea_intake",
    "hypothesis_seed_generation",
    "proxy_suggestion",
    "report_drafting",
}

# Tasks requiring at least validation (medium-risk)
_MEDIUM_RISK_TASKS: set[TaskCategory] = {
    "claim_extraction",
    "source_audit",
    "gatekeeping",
}

# Tasks blocked for open-source/local models — require strong gate or human
_HIGH_RISK_TASKS: set[TaskCategory] = {
    "financial_action",
    "automated_execution",
    "physical_validation",
    "medical_legal_claim",
}

# Model types that are considered "lower quality" for routing purposes
_LOWER_QUALITY_TYPES: set[ModelType] = {
    "LOCAL_LLM",
    "SMALL_CLASSIFIER",
    "EMBEDDING_MODEL",
    "RULE_BASED",
}

_HIGH_QUALITY_TYPES: set[ModelType] = {
    "FRONTIER_API",
    "HUMAN_REVIEW",
}

# ---------------------------------------------------------------------------
# Registry (in-memory)
# ---------------------------------------------------------------------------

_REGISTRY: dict[str, BackendRegistration] = {}


def register_model_backend(backend: BackendRegistration) -> None:
    """Register a model backend. Overwrites if backend_id already exists."""
    _REGISTRY[backend.backend_id] = backend


def get_backend(backend_id: str) -> BackendRegistration | None:
    """Retrieve a registered backend by ID."""
    return _REGISTRY.get(backend_id)


def list_backends() -> list[BackendRegistration]:
    """List all registered backends."""
    return list(_REGISTRY.values())


def clear_registry() -> None:
    """Clear the registry (used in tests)."""
    _REGISTRY.clear()


# ---------------------------------------------------------------------------
# Permission evaluation
# ---------------------------------------------------------------------------

def evaluate_backend_permission(
    backend_id: str,
    task: TaskCategory,
) -> BackendPermission:
    """
    Evaluate whether a registered backend is permitted for a given task.

    Rules:
    - LOW_RISK tasks: all model types allowed (proposals labeled NOT_VALIDATED)
    - MEDIUM_RISK tasks: open-source/local require validation flag
    - HIGH_RISK tasks: open-source/local blocked; FRONTIER + HUMAN_REVIEW get human-review flag
    """
    backend = _REGISTRY.get(backend_id)
    if backend is None:
        return BackendPermission(
            backend_id=backend_id,
            model_type="RULE_BASED",
            task=task,
            permission_status="MODEL_BLOCKED_FOR_HIGH_RISK",
            requires_validation=True,
            requires_human_review=True,
            is_blocked=True,
            routing_notes=["Backend not found in registry."],
        )

    mtype = backend.model_type
    notes: list[str] = []
    status: ModelPermissionStatus
    requires_validation = False
    requires_human = False
    is_blocked = False

    if task in _LOW_RISK_TASKS:
        status = "MODEL_FULLY_ALLOWED_FOR_LOW_RISK"
        notes.append("Low-risk task: all backends allowed. Output labeled PROPOSED_NOT_VALIDATED.")

    elif task in _MEDIUM_RISK_TASKS:
        if mtype in _LOWER_QUALITY_TYPES:
            status = "MODEL_ALLOWED_WITH_VALIDATION"
            requires_validation = True
            notes.append("Medium-risk task: lower-quality model requires output validation.")
        else:
            status = "MODEL_ALLOWED_WITH_VALIDATION"
            requires_validation = True
            notes.append("Medium-risk task: validation required regardless of model quality.")

    elif task in _HIGH_RISK_TASKS:
        if mtype in _LOWER_QUALITY_TYPES:
            status = "MODEL_BLOCKED_FOR_HIGH_RISK"
            is_blocked = True
            notes.append(
                f"HIGH-RISK task '{task}': model type '{mtype}' is not permitted. "
                "Route to HUMAN_REVIEW or deterministic gate."
            )
        elif mtype == "OPEN_SOURCE_API":
            status = "MODEL_REQUIRES_HUMAN_REVIEW"
            requires_validation = True
            requires_human = True
            notes.append(f"HIGH-RISK task '{task}': open-source API requires human review.")
        else:
            # FRONTIER_API, HUMAN_REVIEW
            status = "MODEL_REQUIRES_HUMAN_REVIEW"
            requires_validation = True
            requires_human = True
            notes.append(f"HIGH-RISK task '{task}': human review required regardless of model.")
    else:
        status = "MODEL_REQUIRES_HUMAN_REVIEW"
        requires_validation = True
        requires_human = True
        notes.append("Unknown task category: defaulting to maximum friction.")

    return BackendPermission(
        backend_id=backend_id,
        model_type=mtype,
        task=task,
        permission_status=status,
        requires_validation=requires_validation,
        requires_human_review=requires_human,
        is_blocked=is_blocked,
        routing_notes=notes,
    )


def route_model_task(task: TaskCategory) -> str:
    """
    Suggest the most appropriate backend_id for a task.

    Routing logic:
    - HIGH_RISK → prefer HUMAN_REVIEW, then FRONTIER_API
    - MEDIUM_RISK → prefer FRONTIER_API, then OPEN_SOURCE_API
    - LOW_RISK → any backend (prefer local/open-source)
    Returns backend_id or "NO_BACKEND_AVAILABLE".
    """
    if not _REGISTRY:
        return "NO_BACKEND_AVAILABLE"

    if task in _HIGH_RISK_TASKS:
        preferred = ["HUMAN_REVIEW", "FRONTIER_API"]
    elif task in _MEDIUM_RISK_TASKS:
        preferred = ["FRONTIER_API", "OPEN_SOURCE_API", "HUMAN_REVIEW"]
    else:
        preferred = ["LOCAL_LLM", "OPEN_SOURCE_API", "RULE_BASED", "SMALL_CLASSIFIER", "FRONTIER_API"]

    for preferred_type in preferred:
        for backend in _REGISTRY.values():
            if backend.model_type == preferred_type:
                if task not in (backend.blocked_tasks or []):
                    return backend.backend_id

    # Fallback: first non-blocked backend
    for backend in _REGISTRY.values():
        if task not in (backend.blocked_tasks or []):
            return backend.backend_id

    return "NO_BACKEND_AVAILABLE"
