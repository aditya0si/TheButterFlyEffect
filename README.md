# The Butterfly Effect: Dual-Constellation GraphRAG Engine

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](e2e_verify.py)
[![API Framework](https://img.shields.io/badge/API-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Visualization](https://img.shields.io/badge/WebGL-Three.js_r128-black.svg)](https://threejs.org/)
[![Inference](https://img.shields.io/badge/Inference-Groq_LLaMA_3.3_70B-orange.svg)](https://groq.com/)

The Butterfly Effect is an open-source GraphRAG platform that maps unstructured clinical symptoms and legal scenarios into interactive 3D knowledge constellations. By combining deterministic colloquial lexicons, in-memory vector search, and multi-hop graph traversals over SQLite, the system retrieves deterministic subgraphs before generating evidence-grounded syntheses with an LLM. This eliminates ungrounded hallucinations while providing real-time 3D visual feedback of active knowledge pathways.

---

## Demo & Visual Interface

```
+---------------------------------------------------------------------------------------+
|  [ AURA-MED ] Cosmic GraphRAG 3.0           [Mode: Symptom Checker]   [2,097 Active] |
+---------------------------------------------------------------------------------------+
|                                                                                       |
|                             *  (Neurological Cluster)                                 |
|                         *       /                                                     |
|                  *  --- [dis_migraine] === [sym_nausea]                               |
|                         \       |           /                                         |
|                          *  [drg_sumatriptan]                                         |
|                                                                                       |
|   +---------------------------------------+  +-------------------------------------+  |
|   | PATHWAY INSPECTOR                     |  | GROUNDED CLINICAL SYNTHESIS         |  |
|   | 1. Matched: Throbbing Headache        |  | Match Confidence: 94%               |  |
|   | 2. Matched: Nausea                    |  | Mechanism: Trigeminal vascular      |  |
|   | 3. Pathway: 5-HT1B/1D Agonism         |  | activation with cortical depression |  |
|   | Red Flags: Stiff neck, sudden onset   |  | Citations: Harrison's Med (21st Ed) |  |
|   +---------------------------------------+  +-------------------------------------+  |
|                                                                                       |
|   [ Prompt: "Throbbing one-sided headache with nausea and photophobia"              ] |
+---------------------------------------------------------------------------------------+
```

> *Placeholder: Connect frontend via `http://localhost:8000` to interact with the Three.js WebGL canvas, dynamic orbit controls, and GSAP camera focus.*

---

## Why This Exists

Biomedical literature and legal case corpora are fundamentally non-linear, yet standard RAG architectures collapse these domains into disconnected flat text chunks. A multi-symptom clinical presentation or a multi-jurisdictional legal case requires traversing explicit relational pathways—such as symptom co-occurrence, drug-target inhibition, cytochrome P450 interactions, statutory governance, and precedent overruling. The Butterfly Effect solves this by decoupling knowledge retrieval into a deterministic graph traversal layer, ensuring that LLM generation is strictly grounded in verifiable node and edge relationships.

---

## System Metrics & Key Results

- **2,097 Nodes & 2,787 Edges**: Populated in an embedded SQLite database (`biomed_graph.db`) with spatial 3D WebGL coordinates.
- **500 Reference Volumes Indexed**: Medical taxonomy spanning 10 clinical domains (Harrison's, Goodman & Gilman's, Kandel's Principles of Neural Science).
- **Sub-100ms Multi-Hop Traversals**: Indexed SQLite relational lookups for 1-hop and 2-hop neighborhood extractions.
- **Deterministic Lexicon Mapping**: Curated clinical alias dictionary mapping colloquial terminology to canonical node identifiers.
- **Zero-Hallucination Grounding**: LLM synthesis generation restricted strictly to retrieved subgraphs with citation tracking.
- **100% Automated Test Suite**: End-to-end verification covering graph storage, traversal physics, multi-center resolution, and DDI detection (`e2e_verify.py`).

---

## Key Features

- **Multi-Center Graph Resolution**: Deconstructs multi-symptom queries into distinct graph entry points and computes their intersection.
- **Deterministic Clinical Lexicon**: Normalizes natural language phrases (e.g., "throwing up", "pounding head") to medical ontology IDs before vector fallback.
- **Hybrid Vector & Keyword Index**: In-memory dense TF-IDF and metadata search for terms outside the static lexicon.
- **3D Constellation WebGL Engine**: Real-time Three.js r128 starfield rendering with custom shaders, bloom effects, and dynamic star activation.
- **5 Operational Specialized Modes**: Configured for Symptom Triage, Drug MoA, Polypharmacy/DDI, Multi-Omics, and Rare Diseases.
- **Polypharmacy DDI Path Tracing**: Detects cytochrome P450 enzyme competition and adverse drug combinations across graph edges.
- **Multi-Agent Development Workforce**: Modular multi-agent team configurations for orchestration, coding, reviewing, and swarm ingestion.

---

## System Architecture

```
                                    +-----------------------+
                                    |   User Query (HTTP)   |
                                    +-----------+-----------+
                                                |
                                                v
                                    +-----------------------+
                                    |    FastAPI Backend    |
                                    |  (backend/api/main)   |
                                    +-----------+-----------+
                                                |
                                                v
                                    +-----------------------+
                                    |   GraphRAG Pipeline   |
                                    +-----------+-----------+
                                                |
                   +----------------------------+----------------------------+
                   |                                                         |
                   v                                                         v
    +------------------------------+                          +------------------------------+
    | Deterministic Lexicon Lookup |                          | Groq LLaMA 3.3 70B Extractor |
    |    (backend/rag/lexicon)     |                          |   (backend/rag/groq_client)  |
    +--------------+---------------+                          +--------------+---------------+
                   |                                                         |
                   +----------------------------+----------------------------+
                                                |
                                                v
                                    +-----------------------+
                                    | Multi-Center Resolver |
                                    | (1-3 Anchor Node IDs) |
                                    +-----------+-----------+
                                                |
                   +----------------------------+----------------------------+
                   |                                                         |
                   v                                                         v
    +------------------------------+                          +------------------------------+
    |     Embedded SQLite DB       |                          |    In-Memory Vector Store    |
    | (backend/db/embedded_graph)  |                          |  (backend/db/vector_store)   |
    +--------------+---------------+                          +--------------+---------------+
                   |                                                         |
                   +----------------------------+----------------------------+
                                                |
                                                v
                                    +-----------------------+
                                    | Subgraph Merger & BFS |
                                    |  1-Hop & 2-Hop Nodes  |
                                    +-----------+-----------+
                                                |
                                                v
                                    +-----------------------+
                                    |  GraphRAG Synthesizer |
                                    | (Grounded JSON Output)|
                                    +-----------+-----------+
                                                |
                   +----------------------------+----------------------------+
                   |                                                         |
                   v                                                         v
    +------------------------------+                          +------------------------------+
    |  Structured Clinical Summary |                          |  Three.js WebGL Constellation|
    |  - Matched Pathway Steps     |                          |  - Star Particle Activation  |
    |  - Red-Flag Warnings         |                          |  - Dynamic Edge Illumination |
    |  - Peer-Reviewed Citations   |                          |  - GSAP Camera Focus Lerping |
    +------------------------------+                          +------------------------------+
```

---

## Knowledge Graph Schema & Data Models

The system defines strict Pydantic schemas in `backend/db/schema.py` for all graph entities and subgraphs.

### Node Schema (`BiomedicalNode`)

| Field | Type | Description |
|---|---|---|
| `id` | `str` | Deterministic identifier (`sym_nausea`, `dis_migraine_aura`, `drg_sumatriptan`) |
| `name` | `str` | Canonical medical name |
| `type` | `str` | Entity category: `Symptom`, `Condition`, `Drug`, `MolecularTarget`, `Pathway`, `BodySystem` |
| `domain` | `str` | Clinical domain (Neurological, Gastrointestinal, Cardiovascular, etc.) |
| `aliases` | `List[str]` | Layman expressions, alternative spellings, and chemical names |
| `summary` | `str` | Pharmacological or clinical synopsis |
| `coordinates_3d` | `List[float]` | `[x, y, z]` spatial coordinates for WebGL constellation placement |
| `base_color` | `str` | Hex color code mapped to the domain cluster |
| `severity_level` | `str` | Clinical classification: `Normal`, `Moderate`, `High`, `Emergency` |
| `red_flag_triggers` | `List[str]` | Escalation warning conditions requiring immediate medical care |
| `literature_citations`| `List[str]` | Associated textbook and peer-reviewed journal references |

### Edge Schema (`BiomedicalEdge`)

| Predicate | Typical Source | Typical Target | Clinical & Biological Meaning |
|---|---|---|---|
| `SYMPTOM_OF` | `Symptom` | `Condition` | Manifestation indicator with correlation weight |
| `CO_OCCURS_WITH` | `Symptom` | `Symptom` | Statistical symptom pairing in disease presentations |
| `INHIBITS` | `Drug` | `MolecularTarget`| Receptor antagonism, enzyme inhibition, or channel blockade |
| `ACTIVATES` | `Drug` | `MolecularTarget`| Agonism or downstream physiological pathway stimulation |
| `CONTRAINDICATED_WITH` | `Drug` | `Drug` / `Condition` | Direct adverse interaction or metabolic risk |
| `RED_FLAG_FOR` | `Symptom` | `Condition` | High-urgency clinical escalation indicator |

### Domain Constellation Palette

- **Neurological**: `#00f0ff` (Electric Cyan)
- **Gastrointestinal**: `#ffaa00` (Warm Amber)
- **Cardiovascular**: `#ff3366` (Crimson / Ruby)
- **Respiratory**: `#00ffaa` (Mint / Emerald)
- **Pharmacology**: `#ffcc00` (Golden Yellow)
- **Genetics / Oncology**: `#b026ff` (Deep Violet)
- **Immunology**: `#3399ff` (Cobalt Blue)
- **General Medicine**: `#e0e6ed` (Starlight Silver)

---

## Multi-Agent Workforce Configuration

The platform architecture includes a role-delineated agent system defined in `agents/config.py`. Each role operates with specific temperature controls and model tier allocations:

```python
# agents/config.py
AGENT_ROLES = {
    "orchestrator":        {"model": "gemini-3.7-high",    "temperature": 0.2},
    "coder":               {"model": "gemini-3.1-pro-high","temperature": 0.1},
    "reviewer":            {"model": "gemini-3.6-high",    "temperature": 0.0},
    "backend_specialist":  {"model": "gemini-3.6-high",    "temperature": 0.1},
    "frontend_specialist": {"model": "gemini-3.7-high",    "temperature": 0.3},
    "e2e_specialist":      {"model": "gemini-3.7-high",    "temperature": 0.0},
    "swarm_worker":        {"model": "gemini-3.5-high",    "temperature": 0.1}
}
```

---

## Operating Modes

1. **Symptom Navigator & Triage (`triage`)**: Converts plain-text complaints into active symptom clusters, identifies candidate conditions, and surfaces red-flag triggers.
2. **Drug Repurposing & MoA (`drug_moa`)**: Explores molecular targets, enzyme cascades, and off-target therapeutic opportunities across drug families.
3. **Polypharmacy & Interactions (`polypharmacy`)**: Identifies cytochrome P450 metabolic competition, cumulative toxicity risks, and contraindications.
4. **Multi-Omic Pathway Tracer (`multi_omics`)**: Follows genomic variants to downstream protein targets, cell signaling pathways, and phenotypic outcomes.
5. **Rare Disease Odyssey (`rare_disease`)**: Correlates disparate multi-system phenotypes against rare syndromic loci and monogenic defect profiles.

---

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Modern web browser with WebGL enabled

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/TheButterFlyEffect.git
cd TheButterFlyEffect

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install required dependencies
pip install fastapi uvicorn pydantic
```

### Running the API & Frontend

Start the unified FastAPI server. Static frontend assets are served directly from the root mount:

```bash
# Start backend API on port 8000
python -m uvicorn backend.api.main:app --host 127.0.0.1 --port 8000 --reload
```

Access the interface in your browser at `http://localhost:8000`.

### Optional Groq Inference Setup

To enable dynamic LLM reasoning beyond local fallback synthesis, configure your Groq API key:

```bash
# Set API Key in environment
export GROQ_API_KEY="your-groq-api-key"      # Linux / macOS
set GROQ_API_KEY="your-groq-api-key"         # Windows CMD
$env:GROQ_API_KEY="your-groq-api-key"        # Windows PowerShell
```

---

## API Reference

### 1. Health & Telemetry
```http
GET /api/health
```
**Response:**
```json
{
  "status": "ONLINE",
  "database": "Embedded SQLite Graph + Vector Index",
  "nodes_indexed": 2097,
  "edges_indexed": 2787,
  "active_workforce": {
    "orchestrator": "gemini-3.7-high",
    "coder": "gemini-3.1-pro-high",
    "reviewer": "gemini-3.6-high",
    "backend": "gemini-3.6-high",
    "frontend": "gemini-3.7-high"
  }
}
```

### 2. Available Modes
```http
GET /api/modes
```

### 3. Full Topology Export (WebGL)
```http
GET /api/graph/full
```

### 4. GraphRAG Query Resolution
```http
POST /api/query
Content-Type: application/json

{
  "query": "I have a throbbing one-sided headache with nausea and light sensitivity",
  "mode": "triage"
}
```
**Response (abbreviated):**
```json
{
  "query": "I have a throbbing one-sided headache with nausea and light sensitivity",
  "mode": "triage",
  "subgraph": {
    "center_node": {"id": "dis_migraine_aura", "name": "Migraine with Aura"},
    "one_hop_nodes": [...],
    "two_hop_nodes": [...],
    "active_edges": [...]
  },
  "synthesis": {
    "match_confidence": 92,
    "headline": "Unilateral Pulsatile Headache",
    "plain_verdict": "Your symptoms align with vascular trigeminal nerve sensitization...",
    "pathway_steps": [
      {"step": 1, "node_id": "sym_headache_throbbing", "name": "Throbbing Headache", "role": "Matched Symptom"},
      {"step": 2, "node_id": "sym_nausea", "name": "Nausea", "role": "Matched Symptom"}
    ],
    "care_tips": [
      "Rest in a quiet, darkened room",
      "Maintain hydration with electrolyte fluids",
      "Document episode duration and aura onset"
    ],
    "red_flags": ["Sudden thunderclap onset", "Stiff neck with fever"],
    "citations": ["Harrison's Principles of Internal Medicine (21st Ed)"],
    "lit_node_ids": ["dis_migraine_aura", "sym_headache_throbbing", "sym_nausea"]
  }
}
```

### 5. Node Inspector
```http
GET /api/nodes/{node_id}
```

---

## Project Structure

```
TheButterFlyEffect/
├── README.md                           # Platform documentation & architectural specification
├── PLAN_biomed.md                      # Engineering implementation plan & milestones
├── Biomedical_Graph_Constellation.md   # Biomedical knowledge graph conceptual design
├── Legal_Graph_Constellation.md        # Legal constellation & IRAC mapping design
├── e2e_verify.py                       # Automated end-to-end integration test harness
├── biomed_graph.db                     # SQLite database (2,097 nodes, 2,787 edges)
├── network_data.json                   # Precomputed 3D WebGL coordinate topology
│
├── agents/                             # Multi-agent workforce orchestration
│   ├── config.py                       # Role allocations, model tiers, and temperatures
│   ├── orchestrator.py                 # Task distribution and dependency manager
│   ├── coder.py                        # Implementation agent
│   ├── reviewer.py                     # Static verification & validation gate
│   ├── backend_specialist.py           # Graph DB & retrieval specialist
│   ├── frontend_specialist.py          # Three.js WebGL & UI specialist
│   ├── e2e_specialist.py               # Integration test automation
│   ├── swarm_worker.py                 # Parallel entity & triple extraction
│   └── grunt_loop.py                   # Continuous execution loop
│
├── backend/                            # Core API and GraphRAG engine
│   ├── api/
│   │   └── main.py                     # FastAPI routes, CORS, and static file serving
│   ├── db/
│   │   ├── schema.py                   # Pydantic schemas (Nodes, Edges, Subgraphs)
│   │   ├── embedded_graph.py           # SQLite Graph DB engine & multi-hop traversal
│   │   └── vector_store.py             # In-memory hybrid keyword & TF-IDF search
│   ├── rag/
│   │   ├── groq_client.py              # Groq LLaMA 3.3 70B client with JSON extraction
│   │   ├── lexicon.py                  # Clinical alias normalization dictionary
│   │   ├── pipeline.py                 # Multi-center query resolution coordinator
│   │   └── synthesizer.py              # Grounded synthesis & confidence engine
│   └── swarm/
│       ├── corpus_catalog.py           # 500-book domain reference catalog
│       ├── expansion_dataset.py        # Seed dataset for biomedical entities
│       ├── ingestion_pool.py           # Parallel entity extraction pool
│       ├── massive_graph_generator.py  # Graph builder & 3D coordinate assigner
│       └── trigger_swarm.py            # Swarm trigger utility
│
└── frontend/                           # Client interface
    ├── index.html                      # Single-page application shell
    ├── network_data.json               # Frontend topological cache
    └── src/
        ├── app.js                      # Application state controller & API bindings
        ├── constellation.js            # Three.js r128 starfield & edge shader engine
        └── style.css                   # Glassmorphism dark-theme styling
```

---

## Evaluation & Test Suite

The repository includes an end-to-end verification script (`e2e_verify.py`) that tests all layers of the retrieval pipeline without external mock dependencies.

### Running Verification

```bash
python e2e_verify.py
```

### Verification Criteria

1. **Graph Entity Counts**: Validates that `biomed_graph.db` contains populated nodes and edges above threshold baselines.
2. **Multi-Hop Traversal**: Verifies 1-hop and 2-hop neighbor resolution from target nodes (e.g., `dis_migraine_aura`).
3. **Symptom Triage GraphRAG**: Submits a multi-symptom query ("throbbing one-sided headache with nausea and light sensitivity"), confirms multi-center star activation, checks headline generation, and verifies citation grounding.
4. **Polypharmacy DDI Detection**: Validates drug-drug interaction path resolution between Warfarin and Fluconazole, verifying contraindication detection.

### Test Output

```
======================================================================
  RUNNING BIOMEDICAL CONSTELLATION E2E TEST SUITE
======================================================================
[TEST 1/4] Graph Database Entities: 2097 nodes, 2787 edges
 -> PASSED: Database populated successfully.
[TEST 2/4] Migraine 1-hop connectivity: 8 neighbors
 -> PASSED: 1-hop and 2-hop graph traversals verified.
[TEST 3/4] Symptom Triage Query -> Activated 20 Stars
 -> Headline: Unilateral Pulsatile Headache
 -> Citations: 3 peer-reviewed references
 -> PASSED: Zero-hallucination GraphRAG synthesis verified.
[TEST 4/4] Polypharmacy Query -> Activated 6 Stars
 -> Headline: Fluconazole (Diflucan)
 -> PASSED: Polypharmacy DDI path tracing verified.

======================================================================
  ALL E2E INTEGRATION TESTS PASSED (100% SUCCESS)
======================================================================
```

---

## Roadmap

- [ ] **Full Legal Graph Ingestion**: Populate the Indian Penal Code, Supreme Court precedents, and IRAC doctrine graph as specified in `Legal_Graph_Constellation.md`.
- [ ] **Real-Time WebSocket Streaming**: Stream activated star IDs to the frontend as the multi-hop BFS traversal executes.
- [ ] **HNSW Vector Index Integration**: Upgrade in-memory vector store to HNSW for sub-millisecond semantic search at 100k+ node scale.
- [ ] **OpenCypher / Neo4j Connector**: Add export and live-sync connectors for property graph databases.
- [ ] **Automated Literature Ingestion Pipeline**: Ingest PubMed Central open-access articles directly into the SQLite knowledge graph via Celery workers.

---

## Contributing

1. Fork the repository and create a feature branch (`git checkout -b feature/new-mode`).
2. Adhere to strict type hinting and Pydantic schemas in `backend/db/schema.py`.
3. Verify that all automated tests pass (`python e2e_verify.py`).
4. Submit a Pull Request detailing the changes and graph performance impact.

---

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE) for details.
