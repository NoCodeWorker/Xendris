"""v0.5.2 real-provider execution layer.

The layer is diagnostic-only. It does not read .env files, does not print
secrets, does not fall back to mocks, and does not authorize statistical,
provider superiority, Xendris superiority, external validation, or production
readiness claims.
"""

from .artifact_writer import write_real_provider_execution_artifacts
from .execution_config import ProviderExecutionSpec, RealProviderExecutionConfig
from .execution_gate import RealProviderExecutionGateResult, evaluate_real_provider_execution_gate
from .execution_runner import ProviderExecutionResult, run_real_provider_execution

__all__ = [
    "ProviderExecutionResult",
    "ProviderExecutionSpec",
    "RealProviderExecutionConfig",
    "RealProviderExecutionGateResult",
    "evaluate_real_provider_execution_gate",
    "run_real_provider_execution",
    "write_real_provider_execution_artifacts",
]
