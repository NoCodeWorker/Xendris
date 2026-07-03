"""Observable location scan for resolved local sources."""

from __future__ import annotations

from phyng.dataset_expansion.schemas import ObservableLocationCandidate, SourcePoolRecord


def scan_observable_locations(source_pool: list[SourcePoolRecord]) -> list[ObservableLocationCandidate]:
    by_source = {record.source_id: record for record in source_pool}

    def src(source_id: str) -> SourcePoolRecord:
        return by_source[source_id]

    candidates = [
        ObservableLocationCandidate(
            location_id="V57-LOC-HACKERMUELLER-FIG2-VISIBILITY",
            source_id="SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE",
            local_pdf_path=src("SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE").local_pdf_path,
            local_pdf_hash=src("SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE").local_pdf_hash,
            page_number=2,
            figure_id="FIG. 2",
            observable_class="VISIBILITY",
            variable_name="visibility_fraction",
            numeric_value_text="V=47%; V=29%; V=7%; V=0%",
            unit_text="dimensionless_fraction",
            condition_text="P=0 W; P=3 W; P=6 W; P=10.5 W",
            snippet="The fringe visibility V decreases with increasing heating power P: P=0 W (V=47%), P=3 W (V=29%), P=6 W (V=7%), P=10.5 W (V=0%).",
            classification="OBSERVED_MEASUREMENT_CANDIDATE",
            recommended_next_action="Carry forward already accepted strict y_true records.",
        ),
        ObservableLocationCandidate(
            location_id="V57-LOC-HACKERMUELLER-FIG4-DECOHERENCE-CURVE",
            source_id="SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE",
            local_pdf_path=src("SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE").local_pdf_path,
            local_pdf_hash=src("SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE").local_pdf_hash,
            page_number=4,
            figure_id="FIG. 4",
            observable_class="THERMAL_DECOHERENCE_VISIBILITY",
            variable_name="visibility_fraction",
            numeric_value_text=None,
            unit_text="dimensionless_fraction",
            condition_text="laser heating power",
            snippet="Visibility/decoherence curve as function of laser heating power.",
            classification="REGIME_VALUE",
            extraction_blockers=["REQUIRES_VISUAL_REVIEW", "NO_EXACT_NUMERIC_VALUE_IN_TEXT"],
            recommended_next_action="Manual figure/table digitization before y_true acceptance.",
        ),
        ObservableLocationCandidate(
            location_id="V57-LOC-HORNBERGER-FIG2-COLLISIONAL-VISIBILITY",
            source_id="SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE",
            local_pdf_path=src("SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE").local_pdf_path,
            local_pdf_hash=src("SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE").local_pdf_hash,
            page_number=3,
            figure_id="FIG. 2",
            observable_class="COLLISIONAL_DECOHERENCE_RATE",
            variable_name="fringe_visibility",
            numeric_value_text="p=0.05e-6 mbar; p=0.6e-6 mbar",
            unit_text="mbar condition only",
            condition_text="methane pressure",
            snippet="Fullerene fringe visibility as a function of methane gas pressure; caption has pressure values but no exact visibility values.",
            classification="REGIME_VALUE",
            extraction_blockers=["NO_NUMERIC_VISIBILITY_VALUE_IN_TEXT", "REQUIRES_VISUAL_FIGURE_REVIEW"],
            recommended_next_action="Manual figure review or digitization required.",
        ),
        ObservableLocationCandidate(
            location_id="V57-LOC-NIMMRICHTER-FIG1-CSL-BOUND",
            source_id="SRC-NIMMRICHTER-2011-CSL-MATTER-WAVE-TEST",
            local_pdf_path=src("SRC-NIMMRICHTER-2011-CSL-MATTER-WAVE-TEST").local_pdf_path,
            local_pdf_hash=src("SRC-NIMMRICHTER-2011-CSL-MATTER-WAVE-TEST").local_pdf_hash,
            page_number=2,
            figure_id="FIG. 1",
            observable_class="DECOHERENCE_RATE",
            variable_name="csl_bound",
            snippet="Critical mass / CSL rate figure; source is a constraint plot rather than observed visibility measurement.",
            classification="BOUND_OR_CONSTRAINT",
            extraction_blockers=["BOUND_ONLY", "NOT_OBSERVED_MEASUREMENT"],
            recommended_next_action="Do not accept as visibility/decoherence y_true.",
        ),
        ObservableLocationCandidate(
            location_id="V57-LOC-SCHRINSKI-EQ-CONTRAST",
            source_id="SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS",
            local_pdf_path=src("SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS").local_pdf_path,
            local_pdf_hash=src("SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS").local_pdf_hash,
            page_number=3,
            equation_id="contrast/visibility equation",
            observable_class="INTERFERENCE_CONTRAST",
            variable_name="contrast",
            snippet="Theoretical contrast/visibility expression, not an observed measurement.",
            classification="THEORETICAL_EQUATION",
            extraction_blockers=["MODEL_ONLY", "NOT_OBSERVED_MEASUREMENT"],
            recommended_next_action="Keep as model context only.",
        ),
        ObservableLocationCandidate(
            location_id="V57-LOC-PEDERNALES-DECOHERENCE-PROSE",
            source_id="SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING",
            local_pdf_path=src("SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING").local_pdf_path,
            local_pdf_hash=src("SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING").local_pdf_hash,
            page_number=5,
            section_id="II SOURCES OF DECOHERENCE",
            observable_class="COHERENCE_LOSS",
            variable_name="qualitative_decoherence",
            snippet="Qualitative discussion of sources of decoherence; no accepted numeric observed measurement.",
            classification="QUALITATIVE_PROSE",
            extraction_blockers=["NO_NUMERIC_VALUE", "QUALITATIVE_ONLY"],
            recommended_next_action="Do not accept without numeric observed value.",
        ),
    ]
    return candidates
