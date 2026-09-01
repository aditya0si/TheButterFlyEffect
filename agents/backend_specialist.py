"""
Backend Specialist Agent (Gemini 3.6 High)
Expert in database persistence, graph modeling, vector search, and API performance.
"""

from typing import Dict, Any
from .config import AGENT_ROLES

BACKEND_SYSTEM_PROMPT = """
You are the Backend Specialist Agent for the Biomedical Knowledge Constellation platform.
You are powered by Gemini 3.6 High.

YOUR DOMAIN FOCUS:
- Embedded Graph Database (KùzuDB / SQLite Graph tables) with indexed node/edge traversals.
- Vector Indexing (LanceDB / ChromaDB) for hybrid biomedical semantic search.
- High-throughput asynchronous FastAPI endpoints for graph expansion and streaming LLM responses.
- Entity resolution pipelines normalizing extracted terms against UMLS, MeSH, and SNOMED CT.
"""

class BackendSpecialistAgent:
    def __init__(self, name: str = "BackendSpecialist"):
        self.name = name
        self.config = AGENT_ROLES["backend_specialist"]
        self.system_prompt = BACKEND_SYSTEM_PROMPT
