"""
Grunt Team Development Loop Engine
Coordinates the continuous, automated development cycle between Orchestrator (3.7), Coder (3.1), and Reviewer (3.6).
"""

from typing import Dict, Any, List, Callable
from .orchestrator import OrchestratorAgent
from .coder import CoderAgent
from .reviewer import ReviewerAgent

class GruntDevelopmentLoop:
    def __init__(self):
        self.orchestrator = OrchestratorAgent()
        self.coder = CoderAgent()
        self.reviewer = ReviewerAgent()
        self.history: List[Dict[str, Any]] = []

    async def execute_task_cycle(
        self,
        session_name: str,
        objective: str,
        deliverables: List[str],
        review_metrics: List[str],
        coder_execution_fn: Callable[[Dict[str, Any]], Dict[str, Any]],
        test_suite_fn: Callable[[], Dict[str, bool]],
        max_iterations: int = 3
    ) -> Dict[str, Any]:
        """Runs the iterative Orchestrator -> Coder -> Reviewer loop until approval or max iterations."""
        manifest = self.orchestrator.create_task_manifest(session_name, objective, deliverables, review_metrics)
        
        for iteration in range(1, max_iterations + 1):
            # 1. Coder executes
            submission = coder_execution_fn(manifest)
            
            # 2. Automated tests run
            test_results = test_suite_fn()
            
            # 3. Reviewer evaluates
            review_verdict = self.reviewer.evaluate_submission(manifest, submission, test_results)
            
            cycle_record = {
                "iteration": iteration,
                "manifest": manifest,
                "submission": submission,
                "review": review_verdict
            }
            self.history.append(cycle_record)
            
            if review_verdict["verdict"] == "APPROVED":
                return {
                    "status": "SUCCESS",
                    "iterations": iteration,
                    "session_name": session_name,
                    "final_review": review_verdict
                }
            else:
                # Orchestrator refines instructions for the next pass
                manifest["objective"] += f" [Refinement Required: {review_verdict['feedback']}]"

        return {
            "status": "NEEDS_MANUAL_TRIAGE",
            "iterations": max_iterations,
            "session_name": session_name,
            "history": self.history
        }
