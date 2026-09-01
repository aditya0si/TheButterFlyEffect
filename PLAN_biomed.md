# Project Plan: Biomedical Knowledge Constellation SaaS Platform

---

## SECTION A — GOAL DEFINITION

### 1. What is being built?
An interactive, AI-powered **Biomedical Knowledge Constellation SaaS Web Application**. The platform renders a dynamic, 3D WebGL living starfield of interconnected medical entities (symptoms, diseases, genes, molecular targets, pharmacological compounds, and care pathways). Users submit plain-language or clinical inquiries, triggering a **Multi-Agent GraphRAG pipeline** that retrieves knowledge across medical textbooks, clinical ontologies, and research databases. The 3D graph dynamically illuminates relevant paths, clusters, and nodes with animated pulses, while an LLM delivers a grounded, plain-language or scientific synthesis with full node-level traceability.

### 2. What does "done" look like (Observable Outcome)?
- A responsive, high-performance 3D constellation interface that renders hundreds of clustered nodes and edges smoothly at 60 FPS.
- Interactive camera controls allowing users to zoom, orbit, and click any node to focus, open deep-dive detail inspector drawers, and explore 1-hop and 2-hop neighborhoods.
- Multi-Service SaaS switcher supporting at least 3 active biomedical modes:
  1. *Clinical Symptom Navigator & Educational Triage*
  2. *Drug Repurposing & MoA Discovery*
  3. *Polypharmacy & Drug-Drug Interaction Visualizer*
- An automated **Agent Swarm Ingestion Pipeline** (using a pool of 20–30 worker subagents) capable of extracting entities and triples from biomedical literature into a structured Graph + Vector database.
- A functional dev/runtime workforce loop featuring:
  - **Orchestrator Agent** (Gemini 3.7 High)
  - **Coder Agent** (Gemini 3.1 Pro)
  - **Reviewer Agent** (Gemini 3.6 High)
  - **Backend Specialist Agent** (Gemini 3.6 High)
  - **Frontend Specialist Agent** (Gemini 3.7 High)
  - **E2E Integration Agent** (Gemini 3.7 High)
- Zero hallucinations: The frontend lights up *only* the verified node IDs and edges returned by the RAG pipeline.

### 3. What is explicitly out of scope?
- Replacing certified medical diagnoses or acting as a licensed medical device (educational triage and research exploratory tool only).
- Live Electronic Health Record (EHR / Epic / Cerner) integrations requiring direct hospital HIPAA/HL7 FHIR clearance for MVP.
- Real-time molecular docking simulations (molecular structures and binding affinities are sourced via pre-calculated/queried knowledge bases).

---

## SECTION B — TECH STACK

| Layer | Technology | Decision Rationale |
|---|---|---|
| **Frontend Framework** | React / Vite + Vanilla CSS | Extreme flexibility, fast HMR, precise canvas control without heavy framework overhead. |
| **3D Graphics & Canvas** | Three.js + WebGL / Canvas API | High-performance `InstancedMesh` for rendering thousands of nodes in a single draw call with bloom/glow post-processing. |
| **Animation & Camera** | GSAP (GreenSock) | Smooth physics-based camera fly-to, easing transitions, and glowing pulse animations. |
| **Backend API** | FastAPI (Python) | High-throughput asynchronous REST/WebSocket endpoints for agent streaming and graph queries. |
| **Graph Database** | KùzuDB / SQLite Graph Tables | High-performance embedded graph database optimized for multi-hop graph traversal and rapid local development. |
| **Vector Database** | LanceDB / ChromaDB | Fast, serverless vector search for hybrid entity linking (dense embeddings + sparse keyword search). |
| **Agent Orchestration** | Google Antigravity SDK (`google-antigravity`) | Native support for multi-agent streaming, subagent spawning, and tool calling across Gemini models. |
| **Models** | Gemini 3.7 High (Orchestrator, Frontend, E2E), Gemini 3.1 Pro (Coder), Gemini 3.6 High (Reviewer, Backend), Gemini 3.5 High (Ingestion Swarm) | Optimized role-specific capability allocation as defined in the agent workforce architecture. |

---

## SECTION C — SESSION MODULARIZATION

### Session 1: Agent Workforce & Topology Configuration
- **Objective:** Establish the multi-agent framework, role definitions, prompt manifests, and inter-agent communication protocol for the Grunt Team and Specialists.
- **Scope:** `agents/orchestrator.py`, `agents/coder.py`, `agents/reviewer.py`, `agents/backend_specialist.py`, `agents/frontend_specialist.py`, `agents/e2e_specialist.py`, `agents/config.py`.
- **Output:** Fully configured agent classes and prompt definitions ready to coordinate, execute, and review code iteratively.
- **Connects To:** Session 2 depends on these agents to orchestrate and execute backend database modeling and swarm scripts.
- **Failure Surface:** Ambiguous prompt instructions causing circular loops between Orchestrator, Coder, and Reviewer.

### Session 2: Data Architecture, Database Setup & Ingestion Swarm
- **Objective:** Design the Graph + Vector data schema and implement the 20–30 subagent literature ingestion swarm to populate biomedical entities and relations.
- **Scope:** `backend/db/schema.py`, `backend/db/graph_store.py`, `backend/db/vector_store.py`, `backend/swarm/ingestion_pool.py`, `backend/data/seed_graph.json`.
- **Output:** Working graph database holding node/edge collections with embeddings, plus batch ingestion scripts for biomedical literature.
- **Connects To:** Session 3 requires the populated database and schema to build the real-time GraphRAG query engine.
- **Failure Surface:** Entity resolution conflicts (duplicate nodes with slightly different naming) and slow high-dimensional vector search.

### Session 3: Backend GraphRAG Query Engine & API Service
- **Objective:** Build the FastAPI service that parses user queries, extracts entities, expands multi-hop subgraphs, and synthesizes grounded LLM explanations with exact node-ID mappings.
- **Scope:** `backend/api/main.py`, `backend/rag/pipeline.py`, `backend/rag/entity_extractor.py`, `backend/rag/synthesizer.py`, `backend/tests/test_rag.py`.
- **Output:** Working REST/WebSocket API endpoints `/api/query`, `/api/nodes/{id}`, `/api/graph/subgraph`.
- **Connects To:** Session 4 relies on these endpoints to power the 3D visual constellation on the frontend.
- **Failure Surface:** High query latency during multi-hop graph expansion; LLM returning ungrounded node IDs.

### Session 4: 3D WebGL Constellation Engine & Visual Aesthetics
- **Objective:** Develop the Three.js 3D living constellation interface with orbital controls, glowing starfield background, bloom shaders, and synaptic edge pulsing.
- **Scope:** `frontend/src/canvas/ConstellationCanvas.jsx`, `frontend/src/canvas/NodeRenderer.js`, `frontend/src/canvas/EdgeRenderer.js`, `frontend/src/canvas/PostProcessing.js`, `frontend/src/styles/constellation.css`.
- **Output:** A 60 FPS interactive 3D universe of biomedical nodes with smooth camera orbit, pan, and zoom.
- **Connects To:** Session 5 integrates this visual engine into the complete SaaS application.
- **Failure Surface:** WebGL draw-call bottlenecks on low-power devices; shader compilation errors.

### Session 5: SaaS UI, Node Deep-Dive Inspector & Multi-Service Modes
- **Objective:** Build the SaaS shell with service mode switching (Triage, Drug Repurposing, Polypharmacy), search interface, glowing path visualization, and slide-in node detail inspector.
- **Scope:** `frontend/src/components/SaaSHeader.jsx`, `frontend/src/components/ModeSelector.jsx`, `frontend/src/components/SearchHUD.jsx`, `frontend/src/components/NodeInspectorModal.jsx`, `frontend/src/components/ExplanationCard.jsx`.
- **Output:** Fully functional web SaaS interface allowing node selection, detail inspection, and mode transitions.
- **Connects To:** Session 6 connects the UI to the live backend API.
- **Failure Surface:** UI state desynchronization between lit graph nodes and explanation sidebar cards.

### Session 6: E2E Integration, Review Loop & Performance Hardening
- **Objective:** Connect frontend to backend, validate full end-to-end user query flows, execute automated reviewer benchmarks, and optimize memory/rendering.
- **Scope:** `e2e/test_full_flow.py`, `backend/benchmarks/latency_test.py`, `frontend/src/utils/performance.js`.
- **Output:** Verified, robust end-to-end application with automated test coverage and optimized 60 FPS graph transitions.
- **Connects To:** Final project delivery and deployment readiness.
- **Failure Surface:** WebSocket disconnections during heavy streaming payloads; memory leaks during repeated camera fly-throughs.

---

## SECTION D — PROGRESS CHECKLIST

- [x] **Session 1: Agent Workforce & Topology Configuration**
  - [x] Define Orchestrator (Gemini 3.7 High) prompt and task delegation protocol
  - [x] Define Coder (Gemini 3.1 Pro) prompt and code generation harness
  - [x] Define Reviewer (Gemini 3.6 High) feedback and validation criteria
  - [x] Define Backend Specialist (Gemini 3.6 High) & Frontend Specialist (Gemini 3.7 High) roles
  - [x] Define E2E Specialist (Gemini 3.7 High) verification harness
  - [x] Implement Grunt Team continuous development loop (`agents/grunt_loop.py`)

- [x] **Session 2: Data Architecture, Database Setup & Ingestion Swarm**
  - [x] Define Graph schema (Nodes, Edges, Communities, Properties) in SQLite/Kùzu (`backend/db/schema.py`)
  - [x] Define Embedded Graph engine with indexed 1-hop & 2-hop traversals (`backend/db/embedded_graph.py`)
  - [x] Define Vector search schema in Embedded Store (`backend/db/vector_store.py`)
  - [x] Build 500-book biomedical corpus catalog across 10 domains (`backend/swarm/corpus_catalog.py`)
  - [x] Build 25–30 worker subagent ingestion pool (`backend/swarm/ingestion_pool.py`)
  - [x] Build one-click Swarm Trigger CLI runner ready for 'GO' command (`backend/swarm/trigger_swarm.py`)

- [x] **Session 3: Backend GraphRAG Query Engine & API Service**
  - [x] Implement FastAPI asynchronous backend server (`backend/api/main.py`)
  - [x] Build entity extraction pass converting user queries into seed node IDs (`backend/db/vector_store.py`)
  - [x] Build 1-hop & 2-hop graph expansion and re-ranking algorithms (`backend/db/embedded_graph.py`)
  - [x] Implement synthesis LLM prompt returning explanation + exact node ID trace (`backend/rag/synthesizer.py`)
  - [x] Verify API responses return < 1.5s with deterministic node IDs

- [x] **Phase 2 Enhancement: 1000-Node Dense Universe & Groq Neural Core**
  - [x] Implement live Groq API client with `llama-3.3-70b-versatile` (`backend/rag/groq_client.py`)
  - [x] Build 1,000+ Node & 2,500+ Edge Massive Graph Generator Swarm across 10 domains (`backend/swarm/massive_graph_generator.py`)
  - [x] Re-index SQLite embedded database (2,097 Nodes & 2,787 Edges) and export high-density `network_data.json`
  - [x] Upgrade 3D Constellation with procedural star diffraction textures, volumetric nebula particles, and cosmic color scheme (Black, Purple, Pink, Blue, White)
  - [x] Redesign SaaS synthesis panel with empathetic humanized card layout (Match Confidence Meter, "In Plain Words", "What's Happening", "Care Compass", High-Contrast Red Flags)
  - [x] Execute full E2E verification of 1000-node graph and Groq streaming query resolution
