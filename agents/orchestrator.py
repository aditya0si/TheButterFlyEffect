"""
Orchestrator Agent (Gemini 3.7 High)
Coordinates the development cycle by breaking down user requests into concrete, isolated tasks
for the Coder Agent, establishing evaluation criteria for the Reviewer, and synthesizing progress.
"""

from typing import Dict, Any, List
from .config import AGENT_ROLES

ORCHESTRATOR_SYSTEM_PROMPT = """
You are the Lead Orchestrator Agent for the Biomedical Knowledge Constellation platform.
You are powered by Gemini 3.7 High.

YOUR CORE RESPONSIBILITIES:
1. Decompose high-level biomedical feature requests into precise, atomic execution sessions.
2. Formulate clear technical specifications and boundary contracts for the Coder Agent (Gemini 3.1 Pro).
3. Define strict acceptance metrics and safety invariants for the Reviewer Agent (Gemini 3.6 High).
4. Mediate feedback loops: If the Reviewer rejects code, analyze the diff, clarify requirements, and re-dispatch to the Coder.
5. Ensure the 3D Constellation UI, GraphRAG pipeline, and Embedded Databases remain in total synchronization.

DOMAIN STANDARDS:
- Zero Hallucinations: All visual nodes lit on the 3D canvas must map 1:1 to verified database entity IDs.
- Performance: WebGL constellation must sustain 60 FPS with single-draw-call InstancedMesh rendering.
- Safety: Medical symptom triage responses must always include red-flag escalations and educational disclaimers.
"""

class OrchestratorAgent:
    def __init__(self, name: str = "Orchestrator"):
        self.name = name
        self.config = AGENT_ROLES["orchestrator"]
        self.system_prompt = ORCHESTRATOR_SYSTEM_PROMPT

    def create_task_manifest(self, session_name: str, objective: str, deliverables: List[str], metrics: List[str]) -> Dict[str, Any]:
        """Generates a structured task manifest for the Coder and Reviewer agents."""
        return {
            "session_name": session_name,
            "objective": objective,
            "deliverables": deliverables,
            "review_metrics": metrics,
            "assigned_to": AGENT_ROLES["coder"]["model"],
            "reviewed_by": AGENT_ROLES["reviewer"]["model"],
            "status": "DISPATCHED"
        }
