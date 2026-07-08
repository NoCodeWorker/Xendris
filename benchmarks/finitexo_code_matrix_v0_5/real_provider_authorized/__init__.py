"""v0.5.4 authorized real-provider diagnostic execution."""

from .authorized_artifacts import write_authorized_diagnostic_artifacts
from .authorized_config import AuthorizedDiagnosticConfig, AuthorizedProviderSpec
from .authorized_gate import evaluate_authorized_preflight
from .authorized_runner import AuthorizedProviderResult, run_authorized_diagnostic
from .direct_transport import direct_provider_adapter

__all__ = [
    "AuthorizedDiagnosticConfig",
    "AuthorizedProviderResult",
    "AuthorizedProviderSpec",
    "direct_provider_adapter",
    "evaluate_authorized_preflight",
    "run_authorized_diagnostic",
    "write_authorized_diagnostic_artifacts",
]
