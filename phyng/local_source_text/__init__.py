"""Local source text registry for PHI_GRADIENT v3.6."""

from phyng.local_source_text.campaign import run_phi_gradient_local_source_text_registry_campaign
from phyng.local_source_text.source_registry import build_local_source_text_registry

__all__ = [
    "build_local_source_text_registry",
    "run_phi_gradient_local_source_text_registry_campaign",
]
