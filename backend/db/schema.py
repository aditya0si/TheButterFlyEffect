"""
Pydantic Schemas for the Biomedical Knowledge Graph & Vector Store.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class BiomedicalNode(BaseModel):
    id: str = Field(..., description="Unique deterministic identifier (e.g., sym_nausea, dis_migraine, drg_sumatriptan)")
    name: str = Field(..., description="Canonical clinical / biomedical name")
    type: str = Field(..., description="Entity type: Symptom | Condition | Drug | MolecularTarget | Pathway | BodySystem")
    domain: str = Field(..., description="Medical domain: Neurological, Gastrointestinal, Cardiovascular, Oncology, etc.")
    aliases: List[str] = Field(default_factory=list, description="Layman aliases, colloquial phrases, or alternative chemical names")
    summary: str = Field(..., description="Brief clinical / pharmacological overview")
    coordinates_3d: List[float] = Field(default_factory=lambda: [0.0, 0.0, 0.0], description="Pre-computed 3D coordinates [x, y, z] for WebGL rendering")
    base_color: str = Field(default="#00f0ff", description="Hex color for domain constellation clustering")
    severity_level: Optional[str] = Field("Normal", description="Normal, Moderate, High, Emergency")
    red_flag_triggers: List[str] = Field(default_factory=list, description="Red-flag symptoms requiring emergency escalation")
    literature_citations: List[str] = Field(default_factory=list, description="Textbook and journal references")
    embedding: Optional[List[float]] = Field(default=None, description="Dense vector embedding")

class BiomedicalEdge(BaseModel):
    id: str = Field(..., description="Unique edge ID (e.g., edge_nausea_migraine)")
    source: str = Field(..., description="Source Node ID")
    target: str = Field(..., description="Target Node ID")
    predicate: str = Field(..., description="Relationship: SYMPTOM_OF | INHIBITS | ACTIVATES | CO_OCCURS_WITH | RED_FLAG_FOR | CONTRAINDICATED_WITH")
    weight: float = Field(default=1.0, description="Connection strength / correlation confidence [0.0 to 1.0]")
    evidence_count: int = Field(default=1, description="Number of supporting literature citations")
    mechanism: Optional[str] = Field(None, description="Biological or pharmacokinetic mechanism of connection")
    literature_citations: List[str] = Field(default_factory=list)

class SubgraphResult(BaseModel):
    center_node: BiomedicalNode
    one_hop_nodes: List[BiomedicalNode]
    two_hop_nodes: List[BiomedicalNode]
    active_edges: List[BiomedicalEdge]
    grounded_synthesis: str
    red_flag_warning: Optional[str] = None
    citations: List[str]
