"""
FastAPI Server for the Antigravity Biomedical Constellation Platform.
Serves GraphRAG query resolution, full graph topologies, node deep-dives, and SaaS mode configurations.
"""

from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import json
from typing import Optional, List, Dict, Any

from backend.db.embedded_graph import EmbeddedGraphDB
from backend.rag.pipeline import GraphRAGPipeline
from agents.config import AGENT_ROLES

app = FastAPI(
    title="Antigravity Biomedical Constellation API",
    description="GraphRAG & 3D WebGL Starfield Platform for Biomedical Knowledge Discovery",
    version="1.0.0"
)

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = EmbeddedGraphDB("biomed_graph.db")
pipeline = GraphRAGPipeline("biomed_graph.db")

class QueryRequest(BaseModel):
    query: str
    mode: Optional[str] = "triage"

@app.get("/api/health")
async def health_check():
    counts = db.count_entities()
    return {
        "status": "ONLINE",
        "database": "Embedded SQLite Graph + Vector Index",
        "nodes_indexed": counts["node_count"],
        "edges_indexed": counts["edge_count"],
        "active_workforce": {
            "orchestrator": AGENT_ROLES["orchestrator"]["model"],
            "coder": AGENT_ROLES["coder"]["model"],
            "reviewer": AGENT_ROLES["reviewer"]["model"],
            "backend": AGENT_ROLES["backend_specialist"]["model"],
            "frontend": AGENT_ROLES["frontend_specialist"]["model"]
        }
    }

@app.get("/api/modes")
async def get_modes():
    return [
        {"id": "triage", "name": "Symptom Navigator & Triage", "icon": "🩺", "badge": "Consumer/Clinical", "description": "Describe how you feel to illuminate connected symptom clusters and red flags."},
        {"id": "drug_moa", "name": "Drug Repurposing & MoA", "icon": "🧪", "badge": "Pharma R&D", "description": "Explore molecular targets, kinase cascades, and off-target therapeutic bridges."},
        {"id": "polypharmacy", "name": "Polypharmacy & Interactions", "icon": "💊", "badge": "Clinician/Rx", "description": "Detect dangerous drug-drug interactions, CYP450 competition, and toxicity paths."},
        {"id": "multi_omics", "name": "Multi-Omic Pathway Tracer", "icon": "🧬", "badge": "Biotech", "description": "Trace genomic variants to downstream phenotypic hallmarks and cellular targets."},
        {"id": "rare_disease", "name": "Rare Disease Odyssey", "icon": "🔬", "badge": "Specialist", "description": "Match disparate cross-system phenotypes to syndromic loci and collagen gene defects."}
    ]

@app.get("/api/graph/full")
async def get_full_graph():
    """Returns the full 3D constellation topology for WebGL rendering."""
    if os.path.exists("network_data.json"):
        with open("network_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return db.export_full_graph_json("network_data.json")

@app.post("/api/query")
async def process_user_query(req: QueryRequest):
    """Executes the GraphRAG pipeline and returns activated nodes, edges, and grounded synthesis."""
    if not req.query or len(req.query.strip()) < 2:
        raise HTTPException(status_code=400, detail="Query string is too short")
    result = pipeline.process_query(req.query, mode=req.mode or "triage")
    return result

@app.get("/api/nodes/{node_id}")
async def get_node_detail(node_id: str):
    """Returns deep-dive inspector data for a specific node."""
    node = db.get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    subgraph = db.get_subgraph(node_id, max_1hop=10, max_2hop=10)
    return {
        "node": node.model_dump(),
        "subgraph": subgraph
    }

# Mount static frontend files
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
