"""Campaign wrapper for PHI_GRADIENT semantic triage v3.8.2."""

from __future__ import annotations

from pathlib import Path

from phyng.semantic_triage.campaign import run_phi_gradient_semantic_triage_campaign


def run(root: str | Path = "."):
    return run_phi_gradient_semantic_triage_campaign(root)


if __name__ == "__main__":
    result = run_phi_gradient_semantic_triage_campaign(root=".")
    gate = result.gate_result
    print(
        {
            "status": result.status,
            "input_candidate_count": gate.input_candidate_count,
            "triaged_candidate_count": gate.triaged_candidate_count,
            "priority_packet_count": gate.priority_packet_count,
            "critical_count": gate.critical_count,
            "high_count": gate.high_count,
            "ready_for_v3_9": gate.next_gate_readiness.ready_for_v3_9,
        }
    )
