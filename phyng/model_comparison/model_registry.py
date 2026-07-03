"""Model registry for v4.1 model comparison."""

from __future__ import annotations

from phyng.model_comparison.schemas import ModelRegistryRecord


def get_registered_models() -> list[ModelRegistryRecord]:
    """Return the list of formal model registry records for v4.1 comparison."""
    return [
        ModelRegistryRecord(
            model_id="M_base",
            model_name="Decoherence Baseline Model",
            model_family="BASELINE",
            allowed_claim_scope="Standard thermal/collisional decoherence limits, baseline comparison, observable alignment",
            uses_slot4_gradient_mechanism=False,  # Enforce False
            slot4_debt_compliant=True,
            input_features=["mass", "temperature", "pressure", "time"],
            output_observables=["thermal decoherence rate", "gas scattering rate"],
            parameter_constraints_used=[],
            limitations=["Cannot model any gradient-based coherence mitigation."],
            blocked_claims=["gradient mechanism claim"],
        ),
        ModelRegistryRecord(
            model_id="M_candidate_debt_bounded",
            model_name="PHI_GRADIENT Bounded Candidate Model",
            model_family="PHI_GRADIENT_CANDIDATE",
            allowed_claim_scope="Compare benchmark behavior, use source-pressure-limited observables, parameter constraints",
            uses_slot4_gradient_mechanism=False,  # Enforce False
            slot4_debt_compliant=True,
            input_features=["mass", "temperature", "pressure", "time", "observable mapping"],
            output_observables=["thermal decoherence rate", "interference visibility"],
            parameter_constraints_used=["SLOT_5 parameter constraints"],
            limitations=["Does not simulate active SLOT_4 gradient coupling."],
            blocked_claims=["physical gradient mechanism", "SLOT_4 support", "Frontera C validation", "gradient mechanism claim"],
        ),

        ModelRegistryRecord(
            model_id="M_negative_control_no_slot4",
            model_name="PHI_GRADIENT Negative Control (No SLOT_4)",
            model_family="NEGATIVE_CONTROL",
            allowed_claim_scope="Test whether benchmark behavior depends on unsupported SLOT_4 mechanism",
            uses_slot4_gradient_mechanism=False,  # Enforce False
            slot4_debt_compliant=True,
            input_features=["mass", "temperature", "pressure", "time"],
            output_observables=["thermal decoherence rate", "interference visibility"],
            parameter_constraints_used=["SLOT_5 parameter constraints"],
            limitations=["Active gradient coupling zeroed out."],
            blocked_claims=["All gradient claims", "Physical validation"],
        ),
        ModelRegistryRecord(
            model_id="M_parameter_constrained_variant",
            model_name="PHI_GRADIENT Parameter Constrained Variant",
            model_family="PHI_GRADIENT_CANDIDATE_VARIANT",
            allowed_claim_scope="Candidate constrained by SLOT_5 parameter extracts",
            uses_slot4_gradient_mechanism=False,  # Enforce False
            slot4_debt_compliant=True,
            input_features=["mass", "temperature", "pressure", "time"],
            output_observables=["thermal decoherence rate", "interference visibility"],
            parameter_constraints_used=["SLOT_5 parameter constraints (strict bounds)"],
            limitations=["Constrained parameter space."],
            blocked_claims=["All gradient claims", "Physical validation"],
        ),
        ModelRegistryRecord(
            model_id="M_observable_only_variant",
            model_name="PHI_GRADIENT Observable-Only Variant",
            model_family="PHI_GRADIENT_CANDIDATE_VARIANT",
            allowed_claim_scope="Model using only source-backed observable alignment",
            uses_slot4_gradient_mechanism=False,  # Enforce False
            slot4_debt_compliant=True,
            input_features=["mass", "temperature", "pressure", "time"],
            output_observables=["interference visibility"],
            parameter_constraints_used=[],
            limitations=["Ignores parameter constraints, focuses on visibility observable."],
            blocked_claims=["All gradient claims", "Physical validation"],
        ),
    ]
