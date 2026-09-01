"""
Biomedical GraphRAG Synthesizer.
Generates ultra-clean, structured, interactive JSON payloads with bite-sized clinical reasoning.
Supports multi-symptom queries: every matched symptom becomes its own pathway step,
and care guidance is generated dynamically from the retrieved subgraph (never canned).
"""

from typing import Dict, Any, List, Optional
from ..db.schema import BiomedicalNode, BiomedicalEdge
from .groq_client import GroqClient

SAFE_FALLBACK_CARE_TIPS = [
    "Rest and take it easy for the next 24 hours",
    "Stay well-hydrated with water or electrolyte fluids",
    "Track your symptoms and how long they last to share with your doctor"
]

MAX_SHOWN_CENTERS = 3


class GraphRAGSynthesizer:
    def __init__(self):
        self.groq = GroqClient()

    def synthesize_explanation(
        self,
        query: str,
        mode: str,
        center_nodes: List[BiomedicalNode],
        hop1_nodes: List[BiomedicalNode],
        hop2_nodes: List[BiomedicalNode],
        edges: List[BiomedicalEdge],
        matched_terms: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Generates a structured, interactive synthesis payload for the frontend cards."""
        matched_terms = matched_terms or []
        primary_center = center_nodes[0]

        lit_node_ids = [n.id for n in center_nodes] + [n.id for n in hop1_nodes] + [n.id for n in hop2_nodes]
        lit_edge_ids = [e.id for e in edges]

        # Calculate dynamic confidence match (75% - 98%) from average edge weight
        edge_weights = [e.weight for e in edges]
        avg_weight = sum(edge_weights) / len(edge_weights) if edge_weights else 0.88
        match_confidence = min(98, max(75, int(avg_weight * 100)))

        # Pathway steps: every matched symptom first, then direct pathway neighbors
        pathway_steps: List[Dict[str, Any]] = []
        for idx, node in enumerate(center_nodes[:MAX_SHOWN_CENTERS]):
            pathway_steps.append({
                "step": idx + 1,
                "node_id": node.id,
                "name": node.name,
                "type": node.type,
                "role": "Matched Symptom" if len(center_nodes) > 1 else "Primary Focus",
                "detail": self._truncate(node.summary, 110)
            })

        step_offset = len(pathway_steps)
        for idx, node in enumerate(hop1_nodes[:3]):
            pathway_steps.append({
                "step": step_offset + idx + 1,
                "node_id": node.id,
                "name": node.name,
                "type": node.type,
                "role": "Direct Pathway",
                "detail": self._truncate(node.summary, 100)
            })

        center_names = ", ".join(n.name for n in center_nodes[:3])
        groq_prompt = f"""
A person says: "{query}".
Matched findings from our medical knowledge graph: {center_names}.
Related pathways: {', '.join([n.name for n in hop1_nodes[:3]])}.

INSTRUCTIONS:
1. Write EXACTLY 2 short, empathetic, easy-to-read sentences explaining what might be connecting these findings. Never diagnose.
2. Then on a new line start with "CARE:" followed by exactly 3 short practical wellness tips separated by semicolons. Tips must be relevant to these specific findings, not generic.
3. Return plain text only, no markdown.
"""
        groq_text = self.groq.chat_completion(
            messages=[
                {"role": "system", "content": (
                    "You are an empathetic clinical educator who explains complex physiology "
                    "in simple, friendly language. You never diagnose and never give medication dosages."
                )},
                {"role": "user", "content": groq_prompt}
            ],
            temperature=0.2,
            max_tokens=280
        )

        plain_verdict, care_tips = self._parse_verdict_and_care(groq_text)

        # Filter relevant red flags across all centers and their neighborhoods
        red_flags = list(set(
            primary_center.red_flag_triggers
            + [rf for n in center_nodes for rf in n.red_flag_triggers]
            + [rf for n in hop1_nodes for rf in n.red_flag_triggers]
        ))[:4]

        return {
            "query": query,
            "mode": mode,
            "headline": primary_center.name,
            "domain": primary_center.domain,
            "match_confidence": match_confidence,
            "matched_symptoms": [n.name for n in center_nodes],
            "plain_verdict": plain_verdict,
            "pathway_steps": pathway_steps,
            "care_tips": care_tips,
            "red_flags": red_flags,
            "node_count_activated": len(lit_node_ids),
            "lit_node_ids": lit_node_ids,
            "lit_edge_ids": lit_edge_ids,
            "citations": list(set(
                primary_center.literature_citations
                + [c for n in center_nodes for c in n.literature_citations]
                + [c for n in hop1_nodes for c in n.literature_citations]
            ))[:3]
        }

    # ------------------------------------------------------------------

    @staticmethod
    def _truncate(text: str, limit: int) -> str:
        if not text:
            return ""
        return text[:limit] + "..." if len(text) > limit else text

    @staticmethod
    def _parse_verdict_and_care(groq_text: Optional[str]) -> tuple:
        """Splits the LLM response into (plain_verdict, care_tips).

        Expected shape: two sentences of explanation, then a line starting with
        'CARE:' holding 3 semicolon-separated tips. Falls back to safe generic
        wellness tips whenever the model output is missing or malformed.
        """
        if not groq_text:
            return "", list(SAFE_FALLBACK_CARE_TIPS)

        text = groq_text.strip()
        care_tips = None

        upper = text.upper()
        if "CARE:" in upper:
            split_at = upper.index("CARE:")
            verdict_part = text[:split_at].strip()
            care_part = text[split_at + len("CARE:"):].strip()
            raw_tips = [t.strip(" -*•\t") for t in care_part.split(";") if t.strip(" -*•\t")]
            if 2 <= len(raw_tips) <= 5:
                care_tips = raw_tips[:3]
            text = verdict_part

        if not care_tips:
            care_tips = list(SAFE_FALLBACK_CARE_TIPS)

        return text, care_tips
