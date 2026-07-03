"""
Phygn v1.7 — Model Runtime Reports Writer
"""

from __future__ import annotations

from pathlib import Path
from phyng.model_runtime.schemas import (
    BackendRegistration,
    BackendPermission,
)
from phyng.model_runtime.backends import list_backends, evaluate_backend_permission


def write_model_runtime_reports(
    reports_dir: str | Path,
    permissions_evaluated: list[BackendPermission],
) -> dict[str, str]:
    """
    Write the 3 model runtime reports:
    - reports/model_runtime/model_backend_registry_v1_7.md
    - reports/model_runtime/opensource_model_mode_v1_7.md
    - reports/model_runtime/capability_routing_v1_7.md
    """
    base_path = Path(reports_dir) / "model_runtime"
    base_path.mkdir(parents=True, exist_ok=True)

    registry_path = base_path / "model_backend_registry_v1_7.md"
    opensource_path = base_path / "opensource_model_mode_v1_7.md"
    routing_path = base_path / "capability_routing_v1_7.md"

    backends = list_backends()

    # 1. Backend Registry Report
    reg_rows = []
    for b in backends:
        local_str = "🖥️ Local" if b.is_local else "🌐 API/Cloud"
        json_str = "✅" if b.supports_json_mode else "❌"
        tool_str = "✅" if b.supports_tool_use else "❌"
        reg_rows.append(
            f"| `{b.backend_id}` | `{b.model_name}` | `{b.model_type}` | {local_str} | {json_str} | {tool_str} | Tier {b.quality_tier} |"
        )

    registry_content = f"""# Model Backend Registry — Phygn v1.7

## Registered Backends ({len(backends)} total)

| Backend ID | Model Name | Model Type | Hosting | JSON Mode | Tool Use | Quality Tier |
|---|---|---|---|---|---|---|
{chr(10).join(reg_rows) if reg_rows else "| No backends registered | - | - | - | - | - | - |"}

## Backend Philosophy
- **Auditable & Replaceable**: Any backend conforming to the `ModelBackend` protocol can be registered.
- **Degradability**: When high-tier models are unavailable or local models are used, gates dynamically adjust their strictness.
"""

    # 2. Open-Source Model Mode Report
    os_backends = [b for b in backends if b.model_type in ("OPEN_SOURCE_API", "LOCAL_LLM")]
    os_rows = []
    for ob in os_backends:
        # Evaluate a few test tasks to show permissions
        p_low = evaluate_backend_permission(ob.backend_id, "idea_intake")
        p_high = evaluate_backend_permission(ob.backend_id, "automated_execution")
        os_rows.append(
            f"| `{ob.backend_id}` | `{ob.model_type}` | `{p_low.permission_status}` | `{p_high.permission_status}` |"
        )

    opensource_content = f"""# Open-Source & Local Model Mode — Phygn v1.7

## Compatibility Statement
Phygn explicitly supports open-source and local model backends to reduce dependency on proprietary APIs.
However, because these models may have lower reasoning capabilities, the following rule is enforced:
> **LLM proposes. Phygn verifies.**

## Open-Source Backend Permissions Matrix
| Backend ID | Model Type | Low-Risk Task (Idea Intake) | High-Risk Task (Automated Exec) |
|---|---|---|---|
{chr(10).join(os_rows) if os_rows else "| No open-source/local backends found | - | - | - |"}

## Degradation Rules
1. **Low-Risk Tasks**: Permitted without extra validation. Proposals labeled `PROPOSED_NOT_VALIDATED`.
2. **Medium-Risk Tasks**: Output must pass deterministic Pydantic schema validation.
3. **High-Risk Tasks**: Open-source and local models are **blocked** or require **human review** before action.
"""

    # 3. Capability Routing Report
    routing_rows = []
    for p in permissions_evaluated:
        blocked_str = "⛔ BLOCKED" if p.is_blocked else "✅ Allowed"
        val_str = "✅ Yes" if p.requires_validation else "—"
        human_str = "✅ Yes" if p.requires_human_review else "—"
        routing_rows.append(
            f"| `{p.backend_id}` | `{p.model_type}` | `{p.task}` | {blocked_str} | {val_str} | {human_str} | `{p.permission_status}` |"
        )

    routing_content = f"""# Capability-Aware Routing Report — Phygn v1.7

## Evaluated Tasks Routing Decisions

| Backend ID | Model Type | Task | Action | Requires Validation | Requires Human | Permission Status |
|---|---|---|---|---|---|---|
{chr(10).join(routing_rows) if routing_rows else "| No routing actions evaluated | - | - | - | - | - | - |"}

## Routing Principles
- **Task Risk Matching**: Tasks are routed to backends matching the task's risk category.
- **Deterministic Verification**: No model output is trusted as ground truth. All outputs are validated against Pydantic definitions.
"""

    registry_path.write_text(registry_content, encoding="utf-8")
    opensource_path.write_text(opensource_content, encoding="utf-8")
    routing_path.write_text(routing_content, encoding="utf-8")

    return {
        "registry": str(registry_path),
        "opensource": str(opensource_path),
        "routing": str(routing_path),
    }
