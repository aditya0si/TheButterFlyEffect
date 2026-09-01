"""
Configuration module for the Antigravity Biomedical Multi-Agent Workforce.
Defines models, temperature settings, role instructions, and SDK runtime configs.
"""

from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class ModelTier:
    ORCHESTRATOR = "gemini-3.7-high"
    CODER = "gemini-3.1-pro-high"
    REVIEWER = "gemini-3.6-high"
    BACKEND_SPECIALIST = "gemini-3.6-high"
    FRONTEND_SPECIALIST = "gemini-3.7-high"
    E2E_SPECIALIST = "gemini-3.7-high"
    SWARM_WORKER = "gemini-3.5-high"

AGENT_ROLES: Dict[str, Dict[str, Any]] = {
    "orchestrator": {
        "model": ModelTier.ORCHESTRATOR,
        "temperature": 0.2,
        "description": "Master coordinator that parses user objectives, assigns scoped coding tasks, and evaluates reviewer feedback."
    },
    "coder": {
        "model": ModelTier.CODER,
        "temperature": 0.1,
        "description": "Implementation specialist responsible for writing clean, robust, and performant frontend/backend code."
    },
    "reviewer": {
        "model": ModelTier.REVIEWER,
        "temperature": 0.0,
        "description": "Strict quality gate evaluating code for medical accuracy, performance, security, and edge-case handling."
    },
    "backend_specialist": {
        "model": ModelTier.BACKEND_SPECIALIST,
        "temperature": 0.1,
        "description": "Expert in embedded graph databases, vector indexing, GraphRAG retrieval pipelines, and FastAPI services."
    },
    "frontend_specialist": {
        "model": ModelTier.FRONTEND_SPECIALIST,
        "temperature": 0.3,
        "description": "Expert in Three.js WebGL rendering, 3D starfield constellation shaders, GSAP animations, and SaaS aesthetics."
    },
    "e2e_specialist": {
        "model": ModelTier.E2E_SPECIALIST,
        "temperature": 0.0,
        "description": "Integration and test engineer verifying seamless frontend-to-backend communication, WebSocket streaming, and 60 FPS performance."
    },
    "swarm_worker": {
        "model": ModelTier.SWARM_WORKER,
        "temperature": 0.1,
        "description": "High-throughput parallel extractor for mining biomedical entities, triples, and citations across medical books."
    }
}
