"""Non-saturating phi candidate family definitions."""

from __future__ import annotations

from phyng.synthetic_benchmark_design.schemas import PhiCandidateSpec


def generate_phi_candidate_families() -> list[PhiCandidateSpec]:
    return [
        PhiCandidateSpec(
            candidate_id="PHI-001",
            family="PHI_CENTERED",
            formula="abs(phi_raw - mean(phi_raw over declared sweep))",
            parameters={"k": 1.0, "k2": 1.0},
            boundedness_claim="Bounded in [0, 1] because phi_raw is bounded in [0, 1].",
            dimensionless_inputs=["u", "w", "u0", "w0"],
            known_risks=["threshold tuning", "residual saturation inheritance"],
            control_expectations=["should not match constant phi=1", "must retain coordinate contribution"],
        ),
        PhiCandidateSpec(
            candidate_id="PHI-002",
            family="PHI_GRADIENT",
            formula="abs(d phi_raw / du) + abs(d phi_raw / dw), normalized",
            parameters={"k": 1.0, "k2": 1.0},
            boundedness_claim="Normalized and bounded over declared sweep to [0, 1].",
            dimensionless_inputs=["u", "w", "u0", "w0"],
            known_risks=["transition-region threshold dependence"],
            control_expectations=["should reject saturated plateau behavior"],
        ),
        PhiCandidateSpec(
            candidate_id="PHI-003",
            family="PHI_BANDPASS",
            formula="exp(-((u-u0)^2/sigma_u^2 + (w-w0)^2/sigma_w^2))",
            parameters={"sigma_u": 20.0, "sigma_w": 20.0},
            boundedness_claim="Exponential bandpass is bounded in (0, 1].",
            dimensionless_inputs=["u", "w", "u0", "w0"],
            known_risks=["center tuning", "width tuning"],
            control_expectations=["must survive threshold perturbation"],
        ),
        PhiCandidateSpec(
            candidate_id="PHI-004",
            family="PHI_CURVATURE",
            formula="abs(d2 phi_raw / du2) + abs(d2 phi_raw / dw2), normalized",
            parameters={"k": 1.0, "k2": 1.0},
            boundedness_claim="Normalized and bounded over declared sweep to [0, 1].",
            dimensionless_inputs=["u", "w", "u0", "w0"],
            known_risks=["numerical sensitivity"],
            control_expectations=["should emphasize transition curvature over amplitude"],
        ),
        PhiCandidateSpec(
            candidate_id="PHI-005",
            family="PHI_RELATIVE_BOUNDARY",
            formula="abs(u-w)/(1+abs(u)+abs(w))",
            boundedness_claim="Ratio is bounded in [0, 1].",
            dimensionless_inputs=["u", "w"],
            known_risks=["may be effectively constant for fixed m/L sweep"],
            control_expectations=["must show coordinate contribution beyond fixed modulation"],
        ),
        PhiCandidateSpec(
            candidate_id="PHI-006",
            family="PHI_NON_SATURATING_RATIO",
            formula="log(1+abs(u-u0))/(1+log(1+abs(u-u0))+log(1+abs(w-w0)))",
            boundedness_claim="Positive ratio with denominator larger than numerator, bounded in [0, 1].",
            dimensionless_inputs=["u", "w", "u0", "w0"],
            known_risks=["center dependence"],
            control_expectations=["should avoid hard sigmoid saturation"],
        ),
        PhiCandidateSpec(
            candidate_id="PHI-007",
            family="PHI_COORDINATE_CONTRAST",
            formula="abs(zscore(u)-zscore(w))/(1+abs(zscore(u))+abs(zscore(w)))",
            boundedness_claim="Contrast ratio is bounded in [0, 1].",
            dimensionless_inputs=["u", "w"],
            known_risks=["degenerate if coordinate variance is absent"],
            control_expectations=["must fail clearly when coordinates do not vary"],
        ),
        PhiCandidateSpec(
            candidate_id="PHI-008",
            family="PHI_LOCALIZED_WINDOW",
            formula="sech((u-u0)/sigma_u)^2 * sech((w-w0)/sigma_w)^2",
            parameters={"sigma_u": 10.0, "sigma_w": 10.0},
            boundedness_claim="sech squared product is bounded in (0, 1].",
            dimensionless_inputs=["u", "w", "u0", "w0"],
            known_risks=["center and width tuning"],
            control_expectations=["must not survive only at a narrow tuned window"],
        ),
    ]
