"""v4.1 and legacy Model Comparison for PHI_GRADIENT."""

from phyng.model_comparison.comparison import run_model_comparison
from phyng.model_comparison.models import default_boundary_coupling_spec
from phyng.model_comparison.report import generate_model_comparison_report
from phyng.model_comparison.schemas import (
    ModelComparisonResult,
    ModelComparisonSpec,
    BoundaryCouplingSpec,
)
from phyng.model_comparison.source_backed import (
    SourceBackedModelSpec,
    evaluate_source_backed_comparison_readiness,
    generate_source_backed_readiness_report,
)
from phyng.model_comparison.campaign import (
    run_phi_gradient_debt_bounded_model_comparison_campaign,
)

__all__ = [
    "run_model_comparison",
    "default_boundary_coupling_spec",
    "generate_model_comparison_report",
    "ModelComparisonResult",
    "ModelComparisonSpec",
    "BoundaryCouplingSpec",
    "SourceBackedModelSpec",
    "evaluate_source_backed_comparison_readiness",
    "generate_source_backed_readiness_report",
    "run_phi_gradient_debt_bounded_model_comparison_campaign",
]
