"""Real source ingestion pipeline for PHI_GRADIENT."""

from phyng.real_source_ingestion.extract_validation import validate_real_source_extract
from phyng.real_source_ingestion.manifest import build_real_source_manifest
from phyng.real_source_ingestion.phi_gradient_real_source_gate import run_phi_gradient_real_source_gate

__all__ = [
    "build_real_source_manifest",
    "validate_real_source_extract",
    "run_phi_gradient_real_source_gate",
]
