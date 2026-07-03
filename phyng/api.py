"""
Phyng API — Local FastAPI server.

Endpoints:
    GET  /health                → status check
    POST /frontier/invariant    → validate λ_C·r_g = ℓ_P²
    POST /frontier/signature    → compute Q/B signature
    POST /trace/depolarizing    → quantum channel epistemic trace
    POST /gain                  → predictive gain
    POST /claims/evaluate       → claim gatekeeper
    GET  /case-studies/mesoscopic → mesoscopic interferometer case
"""

from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from phyng.claim_gatekeeper import Claim, evaluate_claim
from phyng.case_studies.mesoscopic_interferometer import mesoscopic_interferometer_case
from phyng.case_studies.quantum_channel import quantum_channel_trace_case
from phyng.enums import ClaimType, Layer, TraceType
from phyng.frontier_lengths import validate_compton_gravity_invariant
from phyng.operational_scale import OperationalScale
from phyng.predictive_gain import predictive_gain
from phyng.signature import frontier_signature

app = FastAPI(
    title="Phygn — Physical Signatures Lab",
    version="0.3.0",
    description=(
        "Computational laboratory for Frontera C v0.3. "
        "Phygn does NOT demonstrate new physics."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request models ─────────────────────────────────────────────────────

class InvariantRequest(BaseModel):
    m_kg: float = Field(gt=0)


class SignatureRequest(BaseModel):
    m_kg: float = Field(gt=0)
    scale: OperationalScale


class DepolarizingRequest(BaseModel):
    p: float = Field(ge=0, le=1)
    epsilon_exp: float = Field(default=1e-6, gt=0)


class GainRequest(BaseModel):
    error_base: float = Field(gt=0)
    error_model: float = Field(ge=0)


class ClaimRequest(BaseModel):
    text: str
    claim_type: ClaimType
    layer: Layer
    trace_type: TraceType | None = None
    predictive_gain: float | None = None
    requires_L: bool = False
    L_status: str | None = None


# ── Endpoints ──────────────────────────────────────────────────────────

@app.get("/health")
def health():
    """Health check."""
    return {
        "status": "ok",
        "project": "Phygn",
        "version": "0.3.0",
    }


@app.post("/frontier/invariant")
def compute_invariant(req: InvariantRequest):
    """Validate the structural lemma λ_C · r_g = ℓ_P²."""
    return validate_compton_gravity_invariant(req.m_kg)


@app.post("/frontier/signature")
def compute_signature(req: SignatureRequest):
    """Compute the Q/B frontier signature."""
    return frontier_signature(req.m_kg, req.scale)


@app.post("/trace/depolarizing")
def compute_depolarizing_trace(req: DepolarizingRequest):
    """Run the depolarizing channel case study."""
    return quantum_channel_trace_case(req.p, req.epsilon_exp)


@app.post("/gain")
def compute_gain(req: GainRequest):
    """Compute predictive gain."""
    return predictive_gain(req.error_base, req.error_model)


@app.post("/claims/evaluate")
def evaluate(req: ClaimRequest):
    """Evaluate a claim through the gatekeeper."""
    claim = Claim(
        text=req.text,
        claim_type=req.claim_type,
        layer=req.layer,
        trace_type=req.trace_type,
        predictive_gain=req.predictive_gain,
        requires_L=req.requires_L,
        L_status=req.L_status,
    )
    return evaluate_claim(claim)


@app.get("/case-studies/mesoscopic")
def case_mesoscopic():
    """Run the mesoscopic interferometer case study."""
    return mesoscopic_interferometer_case()


# ── Loop & RAG extensions ────────────────────────────────────────────────
from pathlib import Path
from phyng.loop import run_iteration_once, scan_project_state
from phyng.loop.backlog import load_backlog, save_backlog
from phyng.loop.schemas import BacklogTask as LoopBacklogTask
from phyng.rag import (
    SourceRecord, ClaimRecord, ClaimSourceLink,
    add_source, list_sources, add_claim, list_claims,
    link_claim_to_source, audit_claim_support
)


@app.get("/loop/status")
def get_loop_status():
    """Get the project state scan summary."""
    return scan_project_state(Path("."))


@app.post("/loop/iterate-once")
def iterate_once():
    """Execute a single core development loop iteration."""
    return run_iteration_once(Path("."))


@app.get("/rag/sources")
def get_sources():
    """List all registered RAG sources."""
    return list_sources(Path("."))


@app.post("/rag/sources")
def register_source(source: SourceRecord):
    """Register a new physical source in RAG."""
    add_source(source, Path("."))
    return {"status": "success", "source_id": source.source_id}


@app.get("/rag/claims")
def get_claims():
    """List all registered claims."""
    return list_claims(Path("."))


@app.post("/rag/claims")
def register_claim(claim: ClaimRecord):
    """Register a new claim in RAG."""
    add_claim(claim, Path("."))
    return {"status": "success", "claim_id": claim.claim_id}


@app.post("/rag/claims/link")
def link_claim(link: ClaimSourceLink):
    """Link a claim to a source with specific support level."""
    link_claim_to_source(link, Path("."))
    return {"status": "success"}


@app.post("/rag/audit-claim")
def audit_claim(claim_id: str):
    """Audit a claim's support level against linked sources and trust rules."""
    updated = audit_claim_support(claim_id, Path("."))
    return updated


@app.get("/rag/report")
def get_rag_report():
    """Get the RAG status report details."""
    report_path = Path(".") / "reports" / "rag_status.md"
    if not report_path.exists():
        return {"report": "Report not generated yet."}
    with open(report_path, "r", encoding="utf-8") as f:
        return {"report": f.read()}


@app.get("/backlog")
def get_backlog():
    """Get all backlog tasks."""
    return load_backlog(Path("."))


@app.post("/backlog")
def add_backlog_task(task: LoopBacklogTask):
    """Add a new task manually to the backlog."""
    tasks = load_backlog(Path("."))
    # Prevent duplicate ids
    if any(t.task_id == task.task_id for t in tasks):
        return {"status": "error", "message": "Duplicate task id"}
    tasks.append(task)
    save_backlog(tasks, Path("."))
    return {"status": "success", "task_id": task.task_id}


# ── Atlas & Campaign extensions ──────────────────────────────────────────
import json
from phyng.atlas import PhysicalSystemSpec, AtlasThresholds, build_atlas
from phyng.campaigns import (
    Campaign002Input,
    CampaignInput,
    run_campaign_002_decoherence_model_comparison,
    run_mesoscopic_boundary_campaign,
)
from phyng.model_comparison import ModelComparisonSpec, run_model_comparison


@app.get("/atlas")
def get_atlas():
    """Get the current Invariant Boundary Atlas points from file."""
    atlas_points_file = Path(".") / "reports" / "atlas" / "atlas_points.json"
    if not atlas_points_file.exists():
        return {"points": []}
    try:
        with open(atlas_points_file, "r", encoding="utf-8") as f:
            return {"points": json.load(f)}
    except Exception:
        return {"points": []}


@app.post("/atlas/build")
def build_custom_atlas(systems: list[PhysicalSystemSpec]):
    """Build a custom Boundary Atlas for specified physical systems."""
    thresholds = AtlasThresholds()
    atlas = build_atlas(systems, thresholds)
    return atlas


@app.get("/campaigns/mesoscopic-boundary-number")
def get_default_campaign():
    """Run and return the default Mesoscopic Boundary Number Campaign result."""
    default_input = CampaignInput(
        campaign_id="CAMPAIGN-001",
        system_id="SYS-MESO-NANOPARTICLE",
        m_kg=1e-17,
        L_value_m=1e-7,
        L_type="L_INT",
        physical_role="interferometric path separation or characteristic localization scale",
        observer_channel="matter-wave interference readout",
        justification="Standard nanoparticle space interferometry.",
        allowed_range_m=(1e-8, 1e-6),
        arbitrariness_risk="LOW"
    )
    result = run_mesoscopic_boundary_campaign(default_input, Path("."))
    return result


@app.post("/campaigns/mesoscopic-boundary-number/run")
def run_custom_campaign(campaign_input: CampaignInput):
    """Run the Mesoscopic Campaign with custom parameters."""
    result = run_mesoscopic_boundary_campaign(campaign_input, Path("."))
    return result


@app.post("/model-comparison/run")
def run_custom_model_comparison(spec: ModelComparisonSpec):
    """Run a toy model comparison without claiming physical prediction."""
    return run_model_comparison(spec)


@app.get("/campaigns/decoherence-model-comparison")
def get_default_decoherence_model_comparison():
    """Run CAMPAIGN-002 with the conservative default toy inputs."""
    return run_campaign_002_decoherence_model_comparison(Path("."))


@app.post("/campaigns/decoherence-model-comparison/run")
def run_custom_decoherence_model_comparison(campaign_input: Campaign002Input):
    """Run CAMPAIGN-002 with explicit toy comparison parameters."""
    return run_campaign_002_decoherence_model_comparison(Path("."), campaign_input)
