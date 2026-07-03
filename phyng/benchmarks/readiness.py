from phyng.benchmarks.schemas import BenchmarkDataset, BenchmarkReadinessResult


def classify_benchmark_readiness(dataset: BenchmarkDataset) -> BenchmarkReadinessResult:
    provenance = dataset.provenance_type

    if provenance == "PLACEHOLDER":
        return BenchmarkReadinessResult(
            dataset_id=dataset.dataset_id,
            readiness_status="NOT_A_BENCHMARK",
            can_compute_gain=False,
            gain_label=None,
            allowed_claim_level=0,
            blocked_reason="PLACEHOLDER data cannot compute Gain_C.",
            required_actions=["Replace placeholder data with sourced, synthetic or simulated y_true."],
        )

    if provenance == "SYNTHETIC":
        if not dataset.generation_method:
            return BenchmarkReadinessResult(
                dataset_id=dataset.dataset_id,
                readiness_status="REJECTED",
                can_compute_gain=False,
                gain_label=None,
                allowed_claim_level=0,
                blocked_reason="SYNTHETIC benchmark requires an explicit generation_method.",
                required_actions=["Add formula, parameters, seed if random and purpose."],
            )
        return BenchmarkReadinessResult(
            dataset_id=dataset.dataset_id,
            readiness_status="SYNTHETIC_READY",
            can_compute_gain=True,
            gain_label="SyntheticGain",
            allowed_claim_level=4,
            blocked_reason=None,
            required_actions=["Do not label SyntheticGain as physical PredictiveGain."],
        )

    if provenance == "SIMULATED":
        if not dataset.generation_method:
            return BenchmarkReadinessResult(
                dataset_id=dataset.dataset_id,
                readiness_status="REJECTED",
                can_compute_gain=False,
                gain_label=None,
                allowed_claim_level=0,
                blocked_reason="SIMULATED benchmark requires documented simulation method.",
                required_actions=["Document simulation method and parameters."],
            )
        return BenchmarkReadinessResult(
            dataset_id=dataset.dataset_id,
            readiness_status="SIMULATED_READY",
            can_compute_gain=True,
            gain_label="SimulatedGain",
            allowed_claim_level=4,
            required_actions=["Keep physical claims limited until source-backed and experimental."],
        )

    if provenance == "LITERATURE_EXTRACTED":
        actions: list[str] = []
        if not dataset.source_ids:
            actions.append("Add source_ids for literature extraction.")
        if not dataset.extraction_notes:
            actions.append("Add extraction_notes with figure/table and method.")
        if actions:
            return BenchmarkReadinessResult(
                dataset_id=dataset.dataset_id,
                readiness_status="LITERATURE_REQUIRES_EXTRACTION_NOTES",
                can_compute_gain=False,
                gain_label=None,
                allowed_claim_level=3,
                blocked_reason="LITERATURE_EXTRACTED benchmark requires source_ids and extraction_notes.",
                required_actions=actions,
            )
        return BenchmarkReadinessResult(
            dataset_id=dataset.dataset_id,
            readiness_status="LITERATURE_READY_WITH_LIMITATIONS",
            can_compute_gain=True,
            gain_label="PredictiveGainCandidate",
            allowed_claim_level=5,
            required_actions=["Audit extraction uncertainty before strong claims."],
        )

    if provenance == "EXPERIMENTAL":
        actions = []
        if not dataset.source_ids:
            actions.append("Add source_ids for experimental dataset.")
        if dataset.uncertainty is None:
            actions.append("Add uncertainty for experimental y_true.")
        if actions:
            reason = (
                "EXPERIMENTAL benchmark requires source_ids and uncertainty."
                if len(actions) == 2
                else actions[0]
            )
            return BenchmarkReadinessResult(
                dataset_id=dataset.dataset_id,
                readiness_status="EXPERIMENTAL_REQUIRES_UNCERTAINTY"
                if dataset.uncertainty is None
                else "EXPERIMENTAL_REQUIRES_SOURCE",
                can_compute_gain=False,
                gain_label=None,
                allowed_claim_level=3,
                blocked_reason=reason,
                required_actions=actions,
            )
        return BenchmarkReadinessResult(
            dataset_id=dataset.dataset_id,
            readiness_status="EXPERIMENTAL_READY",
            can_compute_gain=True,
            gain_label="PredictiveGain",
            allowed_claim_level=6,
            required_actions=["Run source-backed model and claim gatekeeper before prediction."],
        )

    return BenchmarkReadinessResult(
        dataset_id=dataset.dataset_id,
        readiness_status="REJECTED",
        can_compute_gain=False,
        allowed_claim_level=0,
        blocked_reason="Unsupported benchmark provenance.",
        required_actions=["Use a supported provenance_type."],
    )
