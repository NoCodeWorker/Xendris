"""Create and register the SLOT_4 scientific debt object."""

from __future__ import annotations

from phyng.scientific_debt.schemas import ScientificDebtObject


def create_slot4_debt_object() -> ScientificDebtObject:
    """Build the official scientific debt object for the missing SLOT_4 gradient component."""
    return ScientificDebtObject(
        debt_id="DEBT-SLOT4-GRADIENT-COMPONENT-GAP",
        title="SLOT_4 Gradient Component Evidence Gap",
        status="OPEN_BLOCKING_FOR_GRADIENT_CLAIMS",
        severity="HIGH",
        opened_by="v3.9 source pressure decision",
        source_pressure_ref="data/real_sources/source_pressure/phi_gradient_source_pressure_decision_v3_9.json",
        blocks=[
            "PHI_GRADIENT as physical gradient mechanism",
            "Frontera C empirical validation",
            "invariant empirical confirmation",
            "gradient-component source-backed claim",
        ],
        does_not_block=[
            "benchmark dataset construction",
            "observable alignment",
            "baseline decoherence modeling",
            "negative-control comparisons",
            "targeted SLOT_4 source acquisition",
            "Pedernales manual review",
        ],
        evidence_gap="Zero validation-ready extracts for SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS.",
        current_findings=[
            "v3.9 source pressure gate resolved with zero SLOT_4 extracts.",
            "The candidate cannot claim physical gradient-based decoherence mitigation without primary literature validation.",
        ],
        resolution_conditions=[
            "New validation-ready SLOT_4 extracts are found and v3.9-style gate grants pressure.",
            "Existing Pedernales manual review yields clean SLOT_4 extract and source-pressure gate upgrades status.",
            "Source pressure contradicts SLOT_4 and PHI_GRADIENT pivots away from gradient mechanism.",
            "PHI_GRADIENT is redefined explicitly as benchmark/observable model without gradient-mechanism claim.",
        ],
        prohibited_claims=[
            "PHI_GRADIENT is source-backed as a gradient mechanism.",
            "Pedernales supports the gradient component.",
            "Gradient-transition-effective dynamics are literature-backed.",
            "Frontera C is empirically validated.",
            "The invariant has empirical confirmation.",
        ],
        allowed_work=[
            "benchmark construction",
            "observable alignment",
            "baseline model comparison",
            "negative-control design",
            "SLOT_4 source acquisition",
            "Pedernales manual review",
            "candidate revision",
            "kill/pivot analysis",
        ],
        review_frequency="Every campaign gate evaluation",
        notes=[
            "Scientific debt is not shameful. Untracked scientific debt is fatal.",
            "This debt explicitly blocks mechanism claims while permitting benchmark comparisons.",
        ],
    )
