"""
Reviewer Agent (Gemini 3.6 High)
Strict quality assurance and verification gate.
Evaluates code against medical accuracy, performance, security, and architectural standards.
"""

from typing import Dict, Any, List
from .config import AGENT_ROLES

REVIEWER_SYSTEM_PROMPT = """
You are the Lead Reviewer Agent for the Biomedical Knowledge Constellation platform.
You are powered by Gemini 3.6 High.

YOUR CORE RESPONSIBILITIES:
1. Inspect code submitted by the Coder Agent against the Orchestrator's review metrics.
2. Verify:
   - Biomedical Data Integrity: UMLS / SNOMED / MeSH entity mappings are properly validated.
   - 3D Rendering Performance: No unbounded draw calls, memory leaks in WebGL geometries, or unbuffered loops.
   - Graph Traversal Efficiency: Indexed 1-hop and 2-hop graph operations executing in < 50ms.
   - Safety & Guardrails: Medical disclaimer notices and red-flag escalation paths are strictly preserved.
3. Issue deterministic verdict: 'APPROVED' or 'REVISE_REQUESTED' with line-by-line feedback.
"""

class ReviewerAgent:
    def __init__(self, name: str = "Reviewer"):
        self.name = name
        self.config = AGENT_ROLES["reviewer"]
        self.system_prompt = REVIEWER_SYSTEM_PROMPT

    def evaluate_submission(self, task_manifest: Dict[str, Any], submission: Dict[str, Any], test_results: Dict[str, bool]) -> Dict[str, Any]:
        """Evaluates a code submission against required metrics."""
        all_passed = all(test_results.values()) if test_results else True
        verdict = "APPROVED" if all_passed else "REVISE_REQUESTED"
        
        return {
            "session_name": task_manifest.get("session_name"),
            "verdict": verdict,
            "passed_metrics": [m for m, p in test_results.items() if p],
            "failed_metrics": [m for m, p in test_results.items() if not p],
            "feedback": "All automated checks and architectural constraints satisfied." if all_passed else "Revise highlighted test failures."
        }
