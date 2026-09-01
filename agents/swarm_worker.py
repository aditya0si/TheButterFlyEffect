"""
Swarm Worker Subagent (Gemini 3.5 High)
High-throughput worker template instantiated across 20-30 parallel workers during literature ingestion.
Extracts biomedical entities, predicates, citations, and triples from chapters and papers.
"""

from typing import Dict, Any, List
from .config import AGENT_ROLES

SWARM_WORKER_SYSTEM_PROMPT = """
You are a Biomedical Knowledge Extraction Swarm Worker powered by Gemini 3.5 High.
Your objective is to ingest medical book chapters, literature papers, and ontologies, and produce
clean, structured knowledge graph triples (Subject -> Predicate -> Object) with verified citations.

OUTPUT SCHEMA REQUIRED:
- Entities: [ { "id": str, "name": str, "type": "Symptom|Disease|Drug|Target|Pathway", "domain": str, "summary": str } ]
- Relations: [ { "source": str, "predicate": str, "target": str, "weight": float, "citation": str } ]
"""

class SwarmWorkerSubagent:
    def __init__(self, worker_id: int, domain_specialty: str = "General Medicine"):
        self.worker_id = worker_id
        self.domain_specialty = domain_specialty
        self.config = AGENT_ROLES["swarm_worker"]
        self.system_prompt = SWARM_WORKER_SYSTEM_PROMPT

    def parse_chunk(self, book_title: str, chapter_text: str) -> Dict[str, Any]:
        """Extracts structured entities and triples from a medical text chunk."""
        return {
            "worker_id": self.worker_id,
            "book_title": book_title,
            "domain": self.domain_specialty,
            "entities_found": [],
            "triples_found": [],
            "status": "PARSED"
        }
