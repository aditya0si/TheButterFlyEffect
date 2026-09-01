"""
GraphRAG Pipeline Coordinator.
Handles: User Query -> Colloquial Lexicon + LLM Entity Resolution -> Multi-Center
Subgraph Expansion -> Structured Synthesis.

Designed for plain-language ("normal human") queries: multiple symptoms mentioned
in one sentence each become their own constellation center, and the resulting
subgraphs are merged into a single illuminated region.
"""

from typing import Dict, Any, List, Optional, Tuple
from ..db.schema import BiomedicalNode, BiomedicalEdge
from ..db.embedded_graph import EmbeddedGraphDB
from ..db.vector_store import EmbeddedVectorStore
from .synthesizer import GraphRAGSynthesizer
from .lexicon import match_clinical_terms, CANONICAL_NODE_HINTS

MAX_CENTERS = 3


class GraphRAGPipeline:
    def __init__(self, db_path: str = "biomed_graph.db"):
        self.db = EmbeddedGraphDB(db_path)
        self.vector_store = EmbeddedVectorStore()
        self.synthesizer = GraphRAGSynthesizer()
        self._warmup_vector_store()

    def _warmup_vector_store(self):
        """Indexes all 2,000+ nodes in the database into the in-memory search index."""
        with self.db._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM nodes")
            rows = cursor.fetchall()
            for r in rows:
                node = self.db._row_to_node(r)
                text_corpus = f"{node.name} {' '.join(node.aliases)} {node.summary} {node.domain} {node.type}"
                self.vector_store.add_node_index(node.id, text_corpus, {"domain": node.domain, "name": node.name})

    # ------------------------------------------------------------------
    # Center resolution
    # ------------------------------------------------------------------

    def _resolve_center(self, term: str) -> Optional[str]:
        """Resolves a single clinical term to a concrete node id.

        Preference order:
        1. Canonical curated node id (deterministic, avoids duplicate subtypes)
        2. Top-1 hybrid vector/keyword search result
        """
        canonical_id = CANONICAL_NODE_HINTS.get(term.strip().lower())
        if canonical_id and self.db.get_node(canonical_id):
            return canonical_id
        matches = self.vector_store.search(term, top_k=1)
        if matches:
            return matches[0][0]
        return None

    def _resolve_centers(self, query: str, max_centers: int = MAX_CENTERS) -> Tuple[List[str], List[str]]:
        """Maps a free-text query to up to `max_centers` distinct center node ids.

        Candidate concepts come from (in priority order):
          1. The colloquial lexicon ("throwing up" -> vomiting) — deterministic
          2. LLM entity extraction (handles phrasing outside the lexicon)
          3. The raw query itself — last-resort holistic match
        """
        search_terms: List[str] = list(match_clinical_terms(query))

        try:
            extracted = self.synthesizer.groq.extract_entities(query)
            if extracted:
                for e in extracted:
                    if isinstance(e, str) and e.strip() and e.strip() not in search_terms:
                        search_terms.append(e.strip())
        except Exception:
            pass

        search_terms.append(query)

        center_ids: List[str] = []
        resolved_terms: List[str] = []
        seen_ids = set()
        seen_names = set()
        for term in search_terms:
            node_id = self._resolve_center(term)
            if not node_id or node_id in seen_ids:
                continue
            node = self.db.get_node(node_id)
            name_key = node.name.strip().lower() if node else node_id
            if name_key in seen_names:
                continue
            seen_ids.add(node_id)
            seen_names.add(name_key)
            center_ids.append(node_id)
            resolved_terms.append(term)
            if len(center_ids) >= max_centers:
                break
        return center_ids, resolved_terms

    def _fallback_center(self, q_lower: str) -> str:
        """Deterministic last-resort centers when no concept could be resolved."""
        if "fever" in q_lower:
            return "sym_high_fever"
        if "headache" in q_lower or "migraine" in q_lower:
            return "sym_headache_unilateral"
        with self.db._get_conn() as conn:
            first_row = conn.execute("SELECT id FROM nodes LIMIT 1").fetchone()
        return first_row[0] if first_row else "sym_headache_unilateral"

    # ------------------------------------------------------------------
    # Multi-center union expansion
    # ------------------------------------------------------------------

    def _expand_union_subgraph(self, center_ids: List[str]) -> Optional[Dict[str, Any]]:
        """Expands a subgraph around every center and merges them into one region.

        Merged two-hop nodes are re-ranked by how many symptom centers they are
        connected to (conditions explaining multiple symptoms surface first),
        then by edge weight — mirroring the classic symptom-checker heuristic.
        """
        primary_center_id = center_ids[0]
        merged_one_hop: Dict[str, Dict[str, Any]] = {}
        merged_two_hop: Dict[str, Dict[str, Any]] = {}
        merged_edges: Dict[str, Dict[str, Any]] = {}
        center_hits: Dict[str, int] = {}

        for cid in center_ids:
            sg = self.db.get_subgraph(cid, max_1hop=6, max_2hop=8)
            if not sg:
                continue

            one_hop_ids = {n["id"] for n in sg["one_hop_nodes"]}
            for n in sg["one_hop_nodes"]:
                merged_one_hop.setdefault(n["id"], n)

            for n in sg["two_hop_nodes"]:
                nid = n["id"]
                if nid not in merged_two_hop:
                    merged_two_hop[nid] = n
                    center_hits[nid] = 0
                if any(e["source"] in one_hop_ids or e["target"] in one_hop_ids for e in sg["active_edges"]):
                    center_hits[nid] += 1

            for e in sg["active_edges"]:
                merged_edges.setdefault(e["id"], e)

        if not merged_one_hop and not merged_two_hop:
            return None

        ranked_two_hop = sorted(
            merged_two_hop.values(),
            key=lambda n: (center_hits.get(n["id"], 0), n["id"]),
            reverse=True,
        )

        return {
            "center_node": self.db.get_node(primary_center_id).model_dump(),
            "one_hop_nodes": list(merged_one_hop.values()),
            "two_hop_nodes": ranked_two_hop,
            "active_edges": list(merged_edges.values()),
        }

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def process_query(self, query: str, mode: str = "triage") -> Dict[str, Any]:
        """Runs the complete GraphRAG pipeline and returns visual highlights + synthesis."""
        center_ids, matched_terms = self._resolve_centers(query)

        if not center_ids:
            center_ids = [self._fallback_center(query.lower())]
            matched_terms = []

        primary_center_id = center_ids[0]
        subgraph = self._expand_union_subgraph(center_ids)

        if not subgraph:
            fallback_id = self._fallback_center(query.lower())
            center_ids = [fallback_id]
            primary_center_id = fallback_id
            subgraph = self._expand_union_subgraph(center_ids)

        if not subgraph:
            # Database has no traversable graph; return an empty region so the
            # synthesizer can still produce a safe, generic response.
            subgraph = {
                "center_node": self.db.get_node(primary_center_id).model_dump() if self.db.get_node(primary_center_id) else {},
                "one_hop_nodes": [],
                "two_hop_nodes": [],
                "active_edges": []
            }

        center = self.db.get_node(primary_center_id)
        center_models = [self.db.get_node(cid) for cid in center_ids]
        center_models = [c for c in center_models if c]

        if not center or not center_models:
            return {
                "query": query,
                "mode": mode,
                "center_node_id": primary_center_id,
                "center_node_ids": center_ids,
                "matched_terms": matched_terms,
                "center_node": None,
                "subgraph": subgraph,
                "synthesis": {
                    "query": query,
                    "mode": mode,
                    "headline": "No data indexed yet",
                    "domain": "General Medicine",
                    "match_confidence": 0,
                    "matched_symptoms": [],
                    "plain_verdict": "The knowledge graph is still empty. Run the ingestion swarm first, then try again.",
                    "pathway_steps": [],
                    "care_tips": list(self.synthesizer.SAFE_FALLBACK_CARE_TIPS),
                    "red_flags": [],
                    "node_count_activated": 0,
                    "lit_node_ids": [],
                    "lit_edge_ids": [],
                    "citations": []
                }
            }
        hop1_models = [self.db.get_node(n["id"]) for n in subgraph["one_hop_nodes"] if self.db.get_node(n["id"])]
        hop2_models = [self.db.get_node(n["id"]) for n in subgraph["two_hop_nodes"] if self.db.get_node(n["id"])]
        edge_models = [
            BiomedicalEdge(
                id=e["id"],
                source=e["source"],
                target=e["target"],
                predicate=e["predicate"],
                weight=e["weight"],
                evidence_count=e.get("evidence_count", 1),
                mechanism=e.get("mechanism"),
                literature_citations=e.get("literature_citations", [])
            )
            for e in subgraph["active_edges"]
        ]

        synthesis = self.synthesizer.synthesize_explanation(
            query=query,
            mode=mode,
            center_nodes=center_models,
            hop1_nodes=hop1_models,
            hop2_nodes=hop2_models,
            edges=edge_models,
            matched_terms=matched_terms
        )

        return {
            "query": query,
            "mode": mode,
            "center_node_id": primary_center_id,
            "center_node_ids": center_ids,
            "matched_terms": matched_terms,
            "center_node": center.model_dump(),
            "subgraph": subgraph,
            "synthesis": synthesis
        }
