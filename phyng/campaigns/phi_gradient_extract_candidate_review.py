"""Campaign wrapper for PHI_GRADIENT extract candidate review v3.8."""

from phyng.extract_candidate_review.campaign import run_phi_gradient_extract_candidate_review_campaign

__all__ = ["run_phi_gradient_extract_candidate_review_campaign"]


if __name__ == "__main__":
    result = run_phi_gradient_extract_candidate_review_campaign()
    gate = result.gate_result
    print(
        {
            "status": result.status,
            "input_candidate_count": gate.input_candidate_count,
            "validation_ready_count": gate.validation_ready_count,
            "rejected_count": gate.rejected_count,
            "manual_review_count": gate.manual_review_count,
        }
    )
