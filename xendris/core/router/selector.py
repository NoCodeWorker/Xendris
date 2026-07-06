"""MultiModelSelector implementation for routing requests based on risk, capability, and fingerprints."""

from __future__ import annotations

from typing import Any, Mapping
from xendris.core.router.model_registry import ModelRegistry, ModelCapabilityProfile
from xendris.core.router.route_request import RouteRequest, RouteDecision
from xendris.core.router.cost_policy import CostPolicy
from xendris.core.router.risk_policy import RiskPolicy
from xendris.core.fingerprints.model_fingerprint import ModelEpistemicFingerprint
from xendris.core.fingerprints.metrics import FingerprintMetric
from xendris.core.sectors.sector import EpistemicSector
from xendris.core.trust.types import ClaimType, RiskLevel


class MultiModelSelector:
    """Orchestrates model selection by checking eligibility, fingerprint metrics, and cost/latency bands."""

    def __init__(
        self,
        cost_policy: CostPolicy | None = None,
        risk_policy: RiskPolicy | None = None,
    ) -> None:
        self.cost_policy = cost_policy or CostPolicy()
        self.risk_policy = risk_policy or RiskPolicy()

    def select_model(
        self,
        request: RouteRequest,
        registry: ModelRegistry,
        fingerprints: Mapping[str, ModelEpistemicFingerprint] | None = None,
    ) -> RouteDecision:
        """Route a request to the best eligible model under constraints."""
        all_models = registry.list_models()
        rejected_models: list[str] = []
        eligible_candidates: list[tuple[ModelCapabilityProfile, tuple[str, ...]]] = []

        # 1. Filter by basic risk eligibility and capabilities
        for model in all_models:
            eligible, reason, gates = self.risk_policy.is_eligible(request, model)
            if not eligible:
                rejected_models.append(model.model_id)
            else:
                eligible_candidates.append((model, gates))

        # 2. Handle empty candidates early
        if not eligible_candidates:
            if request.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL):
                return RouteDecision(
                    decision="REQUIRE_HUMAN_REVIEW",
                    selected_model_id=None,
                    selected_provider=None,
                    reason="NO_ELIGIBLE_MODELS_FOR_HIGH_RISK_REQUEST",
                    required_gates=("Manual Review Routing Gate",),
                    rejected_models=tuple(rejected_models),
                    estimated_cost=0.0,
                    estimated_latency_ms=0,
                    limitations=("All models exceed risk limit or lack required capabilities",),
                    human_review_required=True,
                )
            else:
                return RouteDecision(
                    decision="NO_SAFE_MODEL_AVAILABLE",
                    selected_model_id=None,
                    selected_provider=None,
                    reason="NO_ELIGIBLE_MODELS_IN_REGISTRY",
                    required_gates=(),
                    rejected_models=tuple(rejected_models),
                    estimated_cost=0.0,
                    estimated_latency_ms=0,
                    limitations=("No model registered supports requested capabilities/risk",),
                )

        # 3. Fingerprint filtering (if provided)
        has_fingerprints = fingerprints is not None and len(fingerprints) > 0
        limitations: list[str] = []
        if not has_fingerprints:
            limitations.append("Routed without epistemic fingerprint audits.")

        safe_candidates: list[tuple[ModelCapabilityProfile, tuple[str, ...], float, float, float]] = []

        for model, gates in eligible_candidates:
            # Default rate metrics
            univ_rate = 0.0
            over_rate = 0.0
            unsp_rate = 0.0
            rev_rate = 0.0
            overclaim_rate = 0.0
            contradict_rate = 0.0

            if has_fingerprints and fingerprints is not None and model.model_id in fingerprints:
                fp = fingerprints[model.model_id]
                # Extract rates safely
                univ_rate = fp.metrics.get(FingerprintMetric.BENCHMARK_UNIVERSALIZATION_RATE, 0.0)
                over_rate = fp.metrics.get(FingerprintMetric.OVERGENERALIZATION_RATE, 0.0)
                unsp_rate = fp.metrics.get(FingerprintMetric.UNSUPPORTED_CLAIM_RATE, 0.0)
                rev_rate = fp.metrics.get(FingerprintMetric.HUMAN_REVIEW_RATE, 0.0)
                overclaim_rate = fp.metrics.get(FingerprintMetric.PRODUCTION_OVERCLAIM_RATE, 0.0)
                contradict_rate = fp.metrics.get(FingerprintMetric.CONTRADICTION_RATE, 0.0)

            # Apply hard filters based on request context/sector/risk
            # A. Benchmark claim: avoid high universalization/overgeneralization models
            ctx_str = request.local_context.name if hasattr(request.local_context, "name") else str(request.local_context).upper()
            if ctx_str in ("BENCHMARK", "SCIENCE") or request.epistemic_sector == EpistemicSector.BENCHMARK:
                if has_fingerprints and (univ_rate >= 0.10 or over_rate >= 0.10):
                    rejected_models.append(model.model_id)
                    continue
                if "Benchmark Gate" not in gates:
                    gates = tuple(list(gates) + ["Benchmark Gate"])

            # B. Production/Code claim: require code support, low production_overclaim_rate
            if ctx_str in ("PRODUCTION", "LAW", "FINANCE", "MEDICINE") or request.requires_code:
                if request.requires_code and not model.supports_code:
                    rejected_models.append(model.model_id)
                    continue
                if has_fingerprints and overclaim_rate >= 0.10:
                    rejected_models.append(model.model_id)
                    continue
                if "Production Evidence Gate" not in gates:
                    gates = tuple(list(gates) + ["Production Evidence Gate"])

            # C. High-risk factual claim: require low unsupported_claim_rate, low contradiction_rate
            if request.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL) and request.claim_type == ClaimType.FACTUAL:
                if has_fingerprints and (unsp_rate >= 0.10 or contradict_rate >= 0.10):
                    rejected_models.append(model.model_id)
                    continue
                if "Strict Evidence Gate" not in gates:
                    gates = tuple(list(gates) + ["Strict Evidence Gate"])

            # D. Strict Gate requirements for specific sectors
            sec_str2 = request.epistemic_sector.name if hasattr(request.epistemic_sector, "name") else str(request.epistemic_sector).upper()
            if sec_str2 in ("BENCHMARK", "POLICY") or request.epistemic_sector == EpistemicSector.FACTUAL:
                if "Strict Safety Fence" not in gates:
                    gates = tuple(list(gates) + ["Strict Safety Fence"])

            safe_candidates.append((model, gates, over_rate + unsp_rate, rev_rate, overclaim_rate))

        # Check if all candidates were rejected by fingerprint filters
        if not safe_candidates:
            if request.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL):
                return RouteDecision(
                    decision="REQUIRE_HUMAN_REVIEW",
                    selected_model_id=None,
                    selected_provider=None,
                    reason="NO_SAFE_MODELS_EXCEED_FINGERPRINT_RISK_THRESHOLDS",
                    required_gates=("Manual Review Routing Gate",),
                    rejected_models=tuple(rejected_models),
                    estimated_cost=0.0,
                    estimated_latency_ms=0,
                    limitations=("All eligible models have unsafe fingerprint metrics",),
                    human_review_required=True,
                )
            else:
                return RouteDecision(
                    decision="NO_SAFE_MODEL_AVAILABLE",
                    selected_model_id=None,
                    selected_provider=None,
                    reason="NO_SAFE_MODELS_AVAILABLE_UNDER_FINGERPRINT_THRESHOLDS",
                    required_gates=(),
                    rejected_models=tuple(rejected_models),
                    estimated_cost=0.0,
                    estimated_latency_ms=0,
                    limitations=("No eligible models meet strict epistemic safety metrics",),
                )

        # 4. Sorting & Ranking candidates
        # Tie breaker sort order:
        # A. Cost preference or Latency preference
        # B. Tie-breaker sorting:
        #    1. safer fingerprint (lower combined over_rate + unsp_rate)
        #    2. lower human review rate
        #    3. lower cost
        #    4. lower expected latency
        #    5. lexicographic model_id
        
        def candidate_key(item: tuple[ModelCapabilityProfile, tuple[str, ...], float, float, float]) -> tuple[Any, ...]:
            model_prof, _, combined_safety, human_rev, _ = item
            cost = self.cost_policy.estimate_cost(
                request.estimated_input_tokens,
                request.estimated_output_tokens,
                model_prof,
            )
            latency = model_prof.expected_latency_ms

            # Primary key modifier based on preferences (LOW COST or LOW LATENCY)
            # If prefer_low_cost is True, we sort by cost first *after* safety filters are satisfied.
            # If prefer_low_latency is True, we sort by latency first *after* safety.
            # Safety constraints have already filtered out unsafe models, so we can now sort.
            pref_key = 0.0
            if request.prefer_low_cost:
                pref_key = cost
            elif request.prefer_low_latency:
                pref_key = float(latency)

            # Combined key: pref_key, safety, human_rev, cost, latency, model_id
            if request.prefer_low_cost or request.prefer_low_latency:
                return (pref_key, combined_safety, human_rev, cost, latency, model_prof.model_id)
            else:
                return (combined_safety, human_rev, cost, latency, model_prof.model_id)

        sorted_candidates = sorted(safe_candidates, key=candidate_key)
        selected_model, final_gates, _, _, _ = sorted_candidates[0]

        # Calculate final estimates
        est_cost = self.cost_policy.estimate_cost(
            request.estimated_input_tokens,
            request.estimated_output_tokens,
            selected_model,
        )
        est_latency = selected_model.expected_latency_ms

        # Fallback model ID (second best option if available)
        fallback_id: str | None = None
        if len(sorted_candidates) > 1:
            fallback_id = sorted_candidates[1][0].model_id

        # Determine decision tag
        decision_val = "SELECT"
        if len(final_gates) > len(selected_model.required_gates):
            decision_val = "SELECT_WITH_LIMITATIONS"

        # Limitations aggregation
        all_limitations = list(limitations)
        all_limitations.extend([
            "Evaluation scoped strictly to registered model profile capabilities.",
            f"Estimated latency is expected at {est_latency}ms.",
        ])

        return RouteDecision(
            decision=decision_val,
            selected_model_id=selected_model.model_id,
            selected_provider=selected_model.provider,
            reason=f"MODEL_{selected_model.model_id.upper()}_SELECTED",
            required_gates=final_gates,
            rejected_models=tuple(r for r in rejected_models if r != selected_model.model_id),
            estimated_cost=est_cost,
            estimated_latency_ms=est_latency,
            limitations=tuple(all_limitations),
            fallback_model_id=fallback_id,
            human_review_required=False,
            audit_tags=("SELECT", selected_model.provider.upper()),
        )
