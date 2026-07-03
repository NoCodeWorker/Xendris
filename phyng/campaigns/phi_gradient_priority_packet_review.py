"""Campaign wrapper for PHI_GRADIENT priority packet review v3.8.3."""

from __future__ import annotations

from pathlib import Path

from phyng.priority_packet_review.campaign import run_phi_gradient_priority_packet_review_campaign


def run(root: str | Path = "."):
    return run_phi_gradient_priority_packet_review_campaign(root)


if __name__ == "__main__":
    result = run_phi_gradient_priority_packet_review_campaign(root=".")
    gate = result.gate_result
    print(
        {
            "status": result.status,
            "input_priority_packet_count": gate.input_priority_packet_count,
            "expanded_pedernales_slot4_count": gate.expanded_pedernales_slot4_count,
            "review_target_count": gate.review_target_count,
            "validation_ready_count": gate.validation_ready_count,
            "manual_review_count": gate.manual_review_count,
            "rejected_count": gate.rejected_count,
            "analogy_only_count": gate.analogy_only_count,
            "ready_for_v3_9": gate.ready_for_v3_9,
        }
    )
