"""
Embedded Local Graph Database Engine (SQLite-backed indexed graph store).
Provides high-performance multi-hop graph traversals, spatial coordinate assignment, and JSON caching.
"""

import sqlite3
import json
import os
import math
import random
from typing import List, Dict, Any, Optional
from .schema import BiomedicalNode, BiomedicalEdge, SubgraphResult

DOMAIN_COLORS = {
    "Neurological": "#00f0ff",      # Electric Cyan
    "Gastrointestinal": "#ffaa00",  # Warm Amber
    "Cardiovascular": "#ff3366",    # Crimson / Ruby
    "Respiratory": "#00ffaa",       # Mint / Emerald
    "Pharmacology": "#ffcc00",      # Golden Yellow
    "Genetics/Oncology": "#b026ff", # Deep Violet
    "Immunology": "#3399ff",        # Cobalt Blue
    "General Medicine": "#e0e6ed"   # Starlight Silver
}

class EmbeddedGraphDB:
    def __init__(self, db_path: str = "biomed_graph.db"):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Initializes tables and high-performance indexes."""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS nodes (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    aliases TEXT,
                    summary TEXT,
                    x REAL,
                    y REAL,
                    z REAL,
                    base_color TEXT,
                    severity_level TEXT,
                    red_flags TEXT,
                    citations TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS edges (
                    id TEXT PRIMARY KEY,
                    source TEXT NOT NULL,
                    target TEXT NOT NULL,
                    predicate TEXT NOT NULL,
                    weight REAL,
                    evidence_count INTEGER,
                    mechanism TEXT,
                    citations TEXT,
                    FOREIGN KEY(source) REFERENCES nodes(id),
                    FOREIGN KEY(target) REFERENCES nodes(id)
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_edge_source ON edges(source)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_edge_target ON edges(target)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_node_name ON nodes(name)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_node_domain ON nodes(domain)")
            conn.commit()

    def batch_upsert_nodes(self, nodes: List[BiomedicalNode]):
        """Batch inserts or updates nodes within a single transaction for maximum throughput."""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            data = [
                (
                    node.id,
                    node.name,
                    node.type,
                    node.domain,
                    json.dumps(node.aliases),
                    node.summary,
                    node.coordinates_3d[0],
                    node.coordinates_3d[1],
                    node.coordinates_3d[2],
                    node.base_color or DOMAIN_COLORS.get(node.domain, "#00f0ff"),
                    node.severity_level,
                    json.dumps(node.red_flag_triggers),
                    json.dumps(node.literature_citations)
                )
                for node in nodes
            ]
            cursor.executemany("""
                INSERT OR REPLACE INTO nodes (
                    id, name, type, domain, aliases, summary, x, y, z, base_color, severity_level, red_flags, citations
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, data)
            conn.commit()

    def batch_upsert_edges(self, edges: List[BiomedicalEdge]):
        """Batch inserts or updates edges within a single transaction."""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            data = [
                (
                    edge.id,
                    edge.source,
                    edge.target,
                    edge.predicate,
                    edge.weight,
                    edge.evidence_count,
                    edge.mechanism,
                    json.dumps(edge.literature_citations)
                )
                for edge in edges
            ]
            cursor.executemany("""
                INSERT OR REPLACE INTO edges (
                    id, source, target, predicate, weight, evidence_count, mechanism, citations
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, data)
            conn.commit()

    def upsert_node(self, node: BiomedicalNode):
        self.batch_upsert_nodes([node])

    def upsert_edge(self, edge: BiomedicalEdge):
        self.batch_upsert_edges([edge])

    def get_node(self, node_id: str) -> Optional[BiomedicalNode]:
        """Retrieves a single node by ID."""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM nodes WHERE id = ?", (node_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return self._row_to_node(row)

    def _row_to_node(self, row: sqlite3.Row) -> BiomedicalNode:
        return BiomedicalNode(
            id=row["id"],
            name=row["name"],
            type=row["type"],
            domain=row["domain"],
            aliases=json.loads(row["aliases"] or "[]"),
            summary=row["summary"],
            coordinates_3d=[row["x"], row["y"], row["z"]],
            base_color=row["base_color"],
            severity_level=row["severity_level"],
            red_flag_triggers=json.loads(row["red_flags"] or "[]"),
            literature_citations=json.loads(row["citations"] or "[]")
        )

    def _row_to_edge(self, row: sqlite3.Row) -> BiomedicalEdge:
        return BiomedicalEdge(
            id=row["id"],
            source=row["source"],
            target=row["target"],
            predicate=row["predicate"],
            weight=row["weight"],
            evidence_count=row["evidence_count"],
            mechanism=row["mechanism"],
            literature_citations=json.loads(row["citations"] or "[]")
        )

    def get_subgraph(self, center_node_id: str, max_1hop: int = 10, max_2hop: int = 15) -> Optional[Dict[str, Any]]:
        """Retrieves 1-hop and 2-hop connected subgraphs with weights."""
        center = self.get_node(center_node_id)
        if not center:
            return None

        with self._get_conn() as conn:
            cursor = conn.cursor()
            # 1-hop edges
            cursor.execute("""
                SELECT * FROM edges 
                WHERE source = ? OR target = ?
                ORDER BY weight DESC LIMIT ?
            """, (center_node_id, center_node_id, max_1hop))
            hop1_edge_rows = cursor.fetchall()
            hop1_edges = [self._row_to_edge(r) for r in hop1_edge_rows]

            hop1_node_ids = set()
            for e in hop1_edges:
                hop1_node_ids.add(e.target if e.source == center_node_id else e.source)

            # Retrieve hop1 nodes
            hop1_nodes = []
            if hop1_node_ids:
                placeholders = ",".join("?" for _ in hop1_node_ids)
                cursor.execute(f"SELECT * FROM nodes WHERE id IN ({placeholders})", list(hop1_node_ids))
                hop1_nodes = [self._row_to_node(r) for r in cursor.fetchall()]

            # 2-hop edges
            hop2_nodes = []
            hop2_edges = []
            if hop1_node_ids:
                placeholders = ",".join("?" for _ in hop1_node_ids)
                cursor.execute(f"""
                    SELECT * FROM edges 
                    WHERE (source IN ({placeholders}) OR target IN ({placeholders}))
                      AND source != ? AND target != ?
                    ORDER BY weight DESC LIMIT ?
                """, (*list(hop1_node_ids), *list(hop1_node_ids), center_node_id, center_node_id, max_2hop))
                hop2_edge_rows = cursor.fetchall()
                hop2_edges = [self._row_to_edge(r) for r in hop2_edge_rows]

                hop2_node_ids = set()
                for e in hop2_edges:
                    for nid in [e.source, e.target]:
                        if nid != center_node_id and nid not in hop1_node_ids:
                            hop2_node_ids.add(nid)

                if hop2_node_ids:
                    p2 = ",".join("?" for _ in hop2_node_ids)
                    cursor.execute(f"SELECT * FROM nodes WHERE id IN ({p2})", list(hop2_node_ids))
                    hop2_nodes = [self._row_to_node(r) for r in cursor.fetchall()]

        return {
            "center_node": center.model_dump(),
            "one_hop_nodes": [n.model_dump() for n in hop1_nodes],
            "two_hop_nodes": [n.model_dump() for n in hop2_nodes],
            "active_edges": [e.model_dump() for e in (hop1_edges + hop2_edges)]
        }

    def export_full_graph_json(self, output_path: str = "network_data.json") -> Dict[str, Any]:
        """Exports full graph topology for Three.js WebGL canvas rendering."""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM nodes")
            nodes = [self._row_to_node(r).model_dump() for r in cursor.fetchall()]

            cursor.execute("SELECT * FROM edges")
            edges = [self._row_to_edge(r).model_dump() for r in cursor.fetchall()]

        payload = {
            "version": "1.0.0",
            "node_count": len(nodes),
            "edge_count": len(edges),
            "nodes": nodes,
            "edges": edges
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

        return payload

    def count_entities(self) -> Dict[str, int]:
        """Returns total counts of nodes and edges."""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM nodes")
            node_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM edges")
            edge_count = cursor.fetchone()[0]
            return {"node_count": node_count, "edge_count": edge_count}
