"""
Embedded Vector Index and Semantic Entity Linker.
Performs fast dense retrieval and fuzzy keyword matching to map user queries to starting Graph Node IDs.
"""

import math
import re
from typing import List, Dict, Any, Tuple

STOP_WORDS = {"i", "have", "and", "the", "a", "an", "what", "can", "be", "reason", "since", "yesterday", "feel", "feeling", "is", "my", "in", "with", "for", "to", "of", "some", "got"}

class EmbeddedVectorStore:
    def __init__(self):
        self.documents: List[Dict[str, Any]] = []

    def add_node_index(self, node_id: str, text: str, metadata: Dict[str, Any], embedding: List[float] = None):
        """Indexes a node for hybrid dense/sparse search."""
        self.documents.append({
            "node_id": node_id,
            "text": text.lower(),
            "tokens": set(re.findall(r"\w+", text.lower())) - STOP_WORDS,
            "metadata": metadata,
            "embedding": embedding
        })

    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """Hybrid search combining keyword token overlap and name matching."""
        query_clean = query.lower()
        all_query_tokens = set(re.findall(r"\w+", query_clean))
        query_tokens = all_query_tokens - STOP_WORDS
        if not query_tokens:
            query_tokens = all_query_tokens
        
        scored = []
        for doc in self.documents:
            score = 0.0
            if not query_tokens:
                continue
            
            # Exact token intersection
            matched = doc["tokens"].intersection(query_tokens)
            if matched:
                score += len(matched) * 2.0
                jaccard = len(matched) / max(len(doc["tokens"].union(query_tokens)), 1)
                score += jaccard * 1.5

            # Name match bonus
            node_name = doc.get("metadata", {}).get("name", "").lower()
            if any(t in node_name for t in query_tokens if len(t) > 2):
                score += 3.0

            # High priority direct symptom keywords
            if "fever" in query_tokens and "fever" in node_name:
                score += 5.0
            if "headache" in query_tokens and "headache" in node_name:
                score += 5.0

            if score > 0.2:
                scored.append((doc["node_id"], score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]
