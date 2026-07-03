from phyng.source_pack_population.schemas import SeedSourceExtract, SeedSourceExtractPack, SeedSourceManifest, SeedSourceManifestEntry
from phyng.source_pack_validation.extract_validator import validate_source_pack_extracts, validated_extracts
from phyng.source_pack_validation.final_gate import build_final_gate
from phyng.source_pack_validation.slot_scoring import score_slot_coverage


def test_negative_contradiction_overrides_promotion():
    manifest = SeedSourceManifest(entries=[
        SeedSourceManifestEntry(source_id="SRC-OBS", title="Obs", doi="10.1/obs", target_slots=["SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT"]),
        SeedSourceManifestEntry(source_id="SRC-COMP", title="Comp", doi="10.1/comp", target_slots=["SLOT_4_GRADIENT_TRANSITION_OPERATORS"]),
        SeedSourceManifestEntry(source_id="SRC-NEG", title="Neg", doi="10.1/neg", target_slots=["SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES"]),
    ])
    pack = SeedSourceExtractPack(extracts=[
        SeedSourceExtract(extract_id="EXT-OBS", source_id="SRC-OBS", slot_id="SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT", extract_text_or_paraphrase="Obs", exact_quote_available=True, observable_text="V(t)", supported_components=["visibility_decay_observable"], manual_review_required=False),
        SeedSourceExtract(extract_id="EXT-COMP", source_id="SRC-COMP", slot_id="SLOT_4_GRADIENT_TRANSITION_OPERATORS", extract_text_or_paraphrase="Comp", exact_quote_available=True, equation_text="rate += |d phi / du|", supported_components=["gradient_transition_operator"], manual_review_required=False),
        SeedSourceExtract(extract_id="EXT-NEG", source_id="SRC-NEG", slot_id="SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES", extract_text_or_paraphrase="Negative exact source.", exact_quote_available=True, contradicted_components=["gradient_transition_operator"], manual_review_required=False),
    ])

    validations = validate_source_pack_extracts(manifest, pack)
    coverage = score_slot_coverage(manifest, pack, validations)
    gate = build_final_gate(manifest, pack, validations, validated_extracts(validations), coverage)

    assert gate.status == "PHI_GRADIENT_REAL_SOURCE_CONTRADICTED"
    assert gate.negative_pressure.negative_pressure_count == 1
