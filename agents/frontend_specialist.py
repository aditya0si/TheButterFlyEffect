"""
Frontend Specialist Agent (Gemini 3.7 High)
Expert in 3D WebGL / Three.js starfield graphics, dynamic node bloom shaders, and SaaS aesthetics.
"""

from typing import Dict, Any
from .config import AGENT_ROLES

FRONTEND_SYSTEM_PROMPT = """
You are the Frontend Specialist Agent for the Biomedical Knowledge Constellation platform.
You are powered by Gemini 3.7 High.

YOUR DOMAIN FOCUS:
- 3D WebGL Canvas built with Three.js / React Three Fiber utilizing InstancedMesh for 60 FPS performance.
- Bloom post-processing, glowing particle halos, and animated synaptic edge lightning.
- Smooth spring-based camera controls (GSAP / OrbitControls) for focus, pan, and zoom.
- Glassmorphic SaaS dashboard featuring multi-service mode switching, search HUD, and deep-dive node inspector.
"""

class FrontendSpecialistAgent:
    def __init__(self, name: str = "FrontendSpecialist"):
        self.name = name
        self.config = AGENT_ROLES["frontend_specialist"]
        self.system_prompt = FRONTEND_SYSTEM_PROMPT
