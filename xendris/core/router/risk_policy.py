"""RiskPolicy checking safety constraints, risk limits, and gating requirements."""

from __future__ import annotations

from xendris.core.router.model_registry import ModelCapabilityProfile
from xendris.core.router.route_request import RouteRequest
from xendris.core.local.context import LocalContext
from xendris.core.sectors.sector import EpistemicSector
from xendris.core.trust.types import RiskLevel


class RiskPolicy:
    """Evaluates risk and safety constraints for a given request and candidate model."""

    def is_eligible(
        self,
        request: RouteRequest,
        model: ModelCapabilityProfile,
    ) -> tuple[bool, str, tuple[str, ...]]:
        """Assess compatibility. Returns (eligible, reason, required_gates)."""
        # 1. Compare risk levels
        risk_values = {
            RiskLevel.LOW: 1,
            RiskLevel.MEDIUM: 2,
            RiskLevel.HIGH: 3,
            RiskLevel.CRITICAL: 4,
        }
        req_val = risk_values.get(request.risk_level, 1)
        model_val = risk_values.get(model.max_risk_level, 1)
        if model_val < req_val:
            return False, "MODEL_RISK_LIMIT_EXCEEDED", ()

        # 2. Context/Sector support check
        context_str = request.local_context.name if hasattr(request.local_context, "name") else str(request.local_context)
        sector_str = request.epistemic_sector.name if hasattr(request.epistemic_sector, "name") else str(request.epistemic_sector)

        if not any(ctx.upper() == context_str.upper() for ctx in model.supported_contexts):
            return False, "UNSUPPORTED_LOCAL_CONTEXT", ()

        if not any(sec.upper() == sector_str.upper() for sec in model.supported_sectors):
            return False, "UNSUPPORTED_EPISTEMIC_SECTOR", ()

        # 3. Capabilities check
        if request.requires_tools and not model.supports_tools:
            return False, "TOOLS_CAPABILITY_MISSING", ()
        if request.requires_code and not model.supports_code:
            return False, "CODE_CAPABILITY_MISSING", ()
        if request.requires_json and not model.supports_json:
            return False, "JSON_CAPABILITY_MISSING", ()
        if request.requires_long_context and not model.supports_long_context:
            return False, "LONG_CONTEXT_CAPABILITY_MISSING", ()

        # 4. Gating determinations
        gates = list(model.required_gates)

        if request.local_context == LocalContext.PRODUCTION:
            if "Production Evidence Gate" not in gates:
                gates.append("Production Evidence Gate")
        elif request.local_context == LocalContext.BENCHMARK:
            if "Benchmark Gate" not in gates:
                gates.append("Benchmark Gate")

        # Stricter sectors
        strict_sectors = (EpistemicSector.POLICY, EpistemicSector.FACTUAL)
        if request.epistemic_sector in strict_sectors:
            if "Strict Evidence Gate" not in gates:
                gates.append("Strict Evidence Gate")

        if request.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL) or request.require_strict_gate:
            if "Strict Safety Fence" not in gates:
                gates.append("Strict Safety Fence")

        return True, "ELIGIBLE", tuple(gates)
