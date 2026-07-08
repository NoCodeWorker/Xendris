"""Real-provider smoke layer for Finitexo Code Matrix v0.5.1.

This package only performs bounded smoke execution on the frozen v0.4.3 n=10
dataset. It does not authorize statistical, provider-superiority, Xendris
superiority, external benchmark validation, or production-readiness claims.
"""

from .real_provider_gate import RealProviderGateResult, evaluate_real_provider_gate
from .real_smoke_config import RealProviderSpec, RealSmokeConfig
from .real_smoke_runner import RealProviderCallResult, run_real_provider_smoke
from .real_smoke_report_builder import build_real_provider_smoke_report

__all__ = [
    "RealProviderCallResult",
    "RealProviderGateResult",
    "RealProviderSpec",
    "RealSmokeConfig",
    "build_real_provider_smoke_report",
    "evaluate_real_provider_gate",
    "run_real_provider_smoke",
]
