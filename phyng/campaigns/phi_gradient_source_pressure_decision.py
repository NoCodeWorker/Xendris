"""Campaign wrapper for PHI_GRADIENT source pressure decision v3.9."""

from __future__ import annotations

from pathlib import Path

from phyng.source_pressure_decision.campaign import run_phi_gradient_source_pressure_decision_campaign


def run(root: str | Path = "."):
    return run_phi_gradient_source_pressure_decision_campaign(root)


if __name__ == "__main__":
    result = run_phi_gradient_source_pressure_decision_campaign(root=".")
    gate = result.gate_result
    dec = gate.decision
    print(
        {
            "status": result.status,
            "primary_decision": dec.primary_decision,
            "confidence": dec.confidence,
            "gradient_component_support": dec.gradient_component_support,
            "validation_ready_count": dec.validation_ready_count,
            "physical_claim_permission": dec.physical_claim_permission,
            "global_decisions": dec.global_decisions,
        }
    )
