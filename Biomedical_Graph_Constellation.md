# Biomedical Symptom Constellation — Concept & Build Plan

A "Living Graph" web experience where a visitor describes how they feel in plain language, and a 3D constellation of medical knowledge lights up around their symptoms — showing related symptoms, possible conditions, and explanatory answers grounded in retrieved data (GraphRAG).

> Inspired by the "Living Literature Map" pattern: nodes = entities, edges = relatedness, LLM answers grounded only in retrieved nodes.

---

## 1. The User Experience (storyboard)

1. User opens the page → a slowly rotating 3D constellation of glowing nodes (symptoms, conditions, body systems) fills the screen. Ambient, calm, "starfield of medicine".
2. A search bar at the bottom: *"Describe what you're feeling..."*
3. User types: **"I have nausea and fever since yesterday"**
4. The AI interprets the input → matches it to symptom nodes → the constellation reacts:
   - **"Nausea"** and **"Fever"** nodes flare brightly (primary glow, large halo)
   - 1-hop neighbors light up dimmer: *vomiting, dehydration, headache, abdominal pain*
   - 2-hop neighbors (possible conditions) shimmer: *viral gastroenteritis, influenza, food poisoning, typhoid, dengue (if region-relevant)*
   - Edges connecting them animate like electricity traveling between stars
5. A side panel slides in:
   - Plain-language answer from the LLM (grounded in the lit nodes only)
   - "Related symptoms to watch for" list
   - "Possible causes (not a diagnosis)" cards with confidence-ish ordering
   - **Red-flag escalation**: "Seek immediate care if: stiff neck, confusion, difficulty breathing..."
   - Persistent disclaimer: *"This is educational information, not medical advice."*
6. User can click any lit node → the camera flies to it and it becomes the new center of the query.

---

## 2. The Knowledge Graph (node database)

### Node types

| Type | Examples | Data stored per node |
|---|---|---|
| **Symptom** | nausea, fever, rash | id, name, aliases ("feeling sick", "throwing up"), embedding, body system, red-flag flag |
| **Condition** | viral gastroenteritis, migraine | id, name, overview text, typical onset, urgency level, embedding |
| **Body system** | GI, neurological, respiratory | grouping/community for constellation coloring |
| **Risk factor / context** | travel, pregnancy, age group, season | used to re-rank retrieved conditions |
| **Care action** | hydration, OTC options, see a doctor | safe, generic guidance nodes |

### Edge types

- `SYMPTOM_OF` — nausea → gastroenteritis (weighted by typicality: common / occasional / rare)
- `CO_OCCURS_WITH` — fever ↔ chills
- `RED_FLAG_FOR` — stiff neck + fever → meningitis (high-priority edge, always lights up bright red)
- `WORSENED_BY` / `RELIEVED_BY` — contextual care hints
- `SIMILAR_TO` — semantic similarity edges for visual clustering

### Communities (constellation colors)

Respiratory · Gastrointestinal · Neurological · Cardiac · Dermatological · Musculoskeletal · Systemic/Infectious — exactly like the 9 "schools" in the literature-map site.

---

## 3. The RAG pipeline (query → lit constellation)

```
User text
   │
   ├─ 1. LLM extraction pass → structured symptoms
   │      "i feel like throwing up and im burning up" → [nausea, fever]
   │
   ├─ 2. Embed each extracted symptom → vector search top-k symptom nodes
   │
   ├─ 3. Graph expansion → 1-hop (related symptoms) + 2-hop (conditions)
   │      with edge weights as relevance scores
   │
   ├─ 4. Re-rank conditions by:
   │      # of matched symptoms × edge typicality weight
   │      (+ optional context: age/region/season if user provides)
   │
   ├─ 5. Red-flag check → any red-flag edge in the subgraph? Escalate visually + in text
   │
   └─ 6. LLM answer pass
          System: "You explain possible causes in calm plain language. ONLY use
                   the provided nodes. Never diagnose. Always include the disclaimer
                   and red-flag guidance."
          Context: retrieved node texts + edge weights
          Output: answer + the list of node IDs used → frontend lights exactly those
```

**The key detail:** the LLM returns the *node IDs it used*, so the visualization and the text are guaranteed to be in sync — the constellation literally shows the answer's sources.

---

## 4. Frontend (same architecture as the reference site)

- React + Three.js: `InstancedMesh` for nodes (one draw call), line segments for edges, glow via sprite textures + bloom post-processing
- Lighting states per node: `idle → related (dim) → primary (bright flare)` driven by the retrieved node ID list
- Force-directed layout computed once offline (community-clustered), shipped as static coordinates in `network_data.json`
- Click-to-refocus camera animation (GSAP or spring physics)

## 5. Data sources to build the graph

- Public medical ontologies: **UMLS / MeSH / SNOMED CT** subsets, **Human Disease Ontology**
- Symptom–condition mappings: open symptom-checker datasets, WHO fact sheets, MedlinePlus articles
- Curated, not crawled: start with **~200–400 nodes** covering the 30–50 most common complaint clusters (cold/flu, GI, headache, back pain, skin, allergies)

## 6. Safety & compliance (non-negotiable for this domain)

- Every answer carries "not medical advice" and red-flag escalation
- No diagnosis language — "possible causes", "commonly associated with"
- No personal data storage; if asking for age/region, keep it in-session only
- The graph is *educational triage*, positioned like an interactive WebMD — not a diagnostic tool

## 7. MVP scope

- 250 nodes, ~1,500 edges, 6 communities
- Symptom extraction + vector search + 2-hop expansion + answer pass
- Static JSON + serverless LLM endpoint
- Visual flare sequence + side panel
- Later: multi-symptom conversation ("it also hurts when I eat"), region-aware conditions, doctor-visit prep summary
