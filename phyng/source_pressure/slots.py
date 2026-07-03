"""Evidence slot registry for PHI_GRADIENT."""

from __future__ import annotations

from phyng.source_pressure.schemas import SourceEvidenceSlot


def build_phi_gradient_source_slots() -> list[SourceEvidenceSlot]:
    return [
        _slot(
            "SLOT_1_DECOHERENCE_BASELINE_MODELS",
            "Decoherence baseline models",
            "visibility/decoherence baseline",
            ["explicit visibility decay model", "decoherence rate equation", "environmental decoherence baseline"],
            ["generic mention of decoherence", "qualitative analogy only"],
        ),
        _slot(
            "SLOT_2_GRAVITATIONAL_DECOHERENCE_MODELS",
            "Gravitational decoherence models",
            "mass/scale decoherence comparison",
            ["explicit gravitational decoherence model", "mass-dependent decoherence rate", "experimental constraint"],
            ["mere mention of gravity and quantum mechanics"],
        ),
        _slot(
            "SLOT_3_LOG_OR_SCALE_SPACE_FORMULATIONS",
            "Log or scale-space formulations",
            "dimensionless log/scale transform",
            ["explicit dimensionless log variables", "scale transformation used in model derivation"],
            ["generic statement that logarithms are useful", "log plot only"],
        ),
        _slot(
            "SLOT_4_GRADIENT_TRANSITION_OPERATORS",
            "Gradient transition operators",
            "gradient/transition component",
            ["explicit gradient term", "transition-region operator", "rate contribution from gradient structure"],
            ["metaphorical gradient", "optimization gradient unrelated to observable"],
        ),
        _slot(
            "SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS",
            "Mesoscopic interferometry benchmarks",
            "comparable benchmark data",
            ["experimental interferometry data", "visibility decay dataset", "published benchmark parameter ranges"],
            ["proposal without observable", "unrelated experiment"],
        ),
        _slot(
            "SLOT_6_ALPHA_LIKE_PARAMETER_CONSTRAINTS",
            "Alpha-like parameter constraints",
            "alpha-like coupling constraint",
            ["parameter bound", "fitted coupling", "dimensionless rate ratio constraint"],
            ["arbitrary alpha choice", "toy parameter with no external bound"],
        ),
        _slot(
            "SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES",
            "Negative or conflicting sources",
            "negative/conflicting evidence",
            ["experimental exclusion", "model incompatibility", "parameter bound that kills effect"],
            [],
        ),
        _slot(
            "SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT",
            "Observable visibility decay support",
            "visibility observable",
            ["visibility contrast definition", "fringe visibility equation", "measured contrast decay"],
            ["vague observable language"],
        ),
    ]


def _slot(
    slot_id: str,
    slot_name: str,
    required_component: str,
    acceptable: list[str],
    unacceptable: list[str],
) -> SourceEvidenceSlot:
    return SourceEvidenceSlot(
        slot_id=slot_id,
        slot_name=slot_name,
        required_component=required_component,
        acceptable_support_types=acceptable,
        unacceptable_support_types=unacceptable,
        minimum_extract_fields=["source_id", "slot_id", "supported_component", "extract_or_paraphrase", "limitations"],
    )
