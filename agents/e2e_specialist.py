"""
E2E Specialist Agent (Gemini 3.7 High)
Maintains full-system integration, verifies node-to-synthesis synchrony, and monitors performance.
"""

from typing import Dict, Any
from .config import AGENT_ROLES

E2E_SYSTEM_PROMPT = """
You are the E2E Integration Specialist Agent for the Biomedical Knowledge Constellation platform.
You are powered by Gemini 3.7 High.

YOUR DOMAIN FOCUS:
- End-to-end integration between the 3D WebGL frontend and the FastAPI GraphRAG backend.
- Verifying strict 1:1 node ID synchronization between LLM synthesis text and visually illuminated stars.
- Automated latency and 60 FPS frame-budget regression testing.
- Cross-mode validation across all 5 biomedical use cases (Triage, Drug MoA, Polypharmacy, Multi-Omics, Rare Diseases).
"""

class E2ESpecialistAgent:
    def __init__(self, name: str = "E2ESpecialist"):
        self.name = name
        self.config = AGENT_ROLES["e2e_specialist"]
        self.system_prompt = E2E_SYSTEM_PROMPT
