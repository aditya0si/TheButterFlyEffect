"""
Coder Agent (Gemini 3.1 Pro High)
Responsible for executing scoped implementation tasks given by the Orchestrator.
Writes clean, production-grade code adhering to exact architectural requirements.
"""

from typing import Dict, Any, List
from .config import AGENT_ROLES

CODER_SYSTEM_PROMPT = """
You are the Lead Coder Agent for the Biomedical Knowledge Constellation platform.
You are powered by Gemini 3.1 Pro High.

YOUR CORE RESPONSIBILITIES:
1. Implement clean, modular, and performant code based on the Orchestrator's task manifest.
2. Ensure full type annotations, defensive error handling, and robust docstrings.
3. Strictly follow project architectures:
   - Embedded Graph Store: KùzuDB / SQLite with indexed node/edge traversals.
   - 3D WebGL Frontend: Three.js InstancedMesh, bloom shaders, GSAP camera animations.
   - Backend GraphRAG: FastAPI asynchronous pipelines, deterministic entity linking.
4. Prepare code diffs and explanation summaries for the Reviewer Agent.
"""

class CoderAgent:
    def __init__(self, name: str = "Coder"):
        self.name = name
        self.config = AGENT_ROLES["coder"]
        self.system_prompt = CODER_SYSTEM_PROMPT

    def generate_code_submission(self, task_manifest: Dict[str, Any], files_changed: List[str], implementation_notes: str) -> Dict[str, Any]:
        """Packages implemented code for submission to the Reviewer agent."""
        return {
            "session_name": task_manifest.get("session_name"),
            "files_changed": files_changed,
            "implementation_notes": implementation_notes,
            "status": "AWAITING_REVIEW"
        }
