# Legal Case Constellation — Concept & Build Plan

A "Living Case Map" for lawyers, law students, and researchers: enter a case scenario in plain language, and a 3D constellation of legal knowledge lights up — relevant statutes, landmark precedents, similar past cases, and legal doctrines — presented as an explorable case-study tree with AI answers grounded only in retrieved nodes (GraphRAG).

> Same architecture as the biomedical version and the "Living Literature Map": nodes = legal entities, edges = legal relationships, LLM grounded in retrieved nodes only.

---

## 1. The User Experience (storyboard)

1. Lawyer opens the page → a 3D constellation of glowing nodes: landmark cases, statutes, doctrines, crime categories — organized into colored clusters (Criminal, Juvenile Justice, Constitutional, Property...).
2. A prompt bar: *"Describe the case or question..."*
3. Lawyer enters: **"Murder committed by a 14-year-old, in Maharashtra"**
4. The AI decomposes the scenario into legal facets:
   - Offense: *murder / homicide*
   - Offender: *juvenile (14)*
   - Jurisdiction: *Maharashtra, India*
5. The constellation reacts:
   - **Primary nodes flare**: *IPC §302 (murder)*, *Juvenile Justice Act 2015 — §15/§18 (heinous offenses, 16–18 vs under-16 rules)*, *Juvenile Justice Board*
   - **Precedent nodes light up**: *Pratap Singh v. State of Jharkhand (2005)*, *Salil Bali v. Union of India (2013)*, the Nirbhaya aftermath amendments, relevant Bombay HC / Maharashtra rulings
   - **Doctrine nodes shimmer**: *doli incapax* (presumption of incapacity under a certain age), *parens patriae*, "heinous offense" classification debate
   - Edges animate: `OVERRULED_BY` edges glow red, `UPHELD` glows green, `DISTINGUISHED` glows amber — the lawyer sees *which way the law flows* at a glance
6. Side panel presents the result as a **generated case study**:
   - Issue → Rule → Application → Conclusion (IRAC) summary
   - "Cases most similar to yours" with similarity reasoning
   - "Open questions" — e.g., whether the 14-year-old could be tried as an adult under JJ Act provisions
   - Jurisdiction filter chip: switch Maharashtra → all-India → another state
7. Clicking any precedent node flies the camera to it and shows its full case card: citation, holding, key paragraphs, how courts have treated it since.

---

## 2. The Knowledge Graph (node database)

### Node types

| Type | Examples | Data per node |
|---|---|---|
| **Statute / section** | IPC §302, JJ Act §15 | full text, jurisdiction, effective dates, amendments |
| **Case / precedent** | Salil Bali v. UoI | citation, court, year, holding, key paragraphs, outcome, embedding |
| **Doctrine / principle** | doli incapax, mens rea | plain-language explanation + authoritative definition |
| **Offense category** | murder, culpable homicide | links to statutes and sentencing ranges |
| **Jurisdiction** | India, Maharashtra, Bombay HC | hierarchy edges (SC → HC → District) |
| **Offender profile facet** | juvenile, adult, repeat offender | modifies which statutes apply |
| **Procedural stage** | FIR, charge sheet, bail, appeal | for procedural Q&A |

### Edge types (the "legal physics" of the graph)

- `CITES` / `RELIED_UPON` — case → case, case → statute
- `OVERRULED_BY` / `REVERSED` — **critical**: RAG must never surface a dead precedent as good law
- `UPHELD` / `DISTINGUISHED` / `QUESTIONED` — treatment edges (like Shepard's/KeyCite signals)
- `GOVERNS` — statute → offense category
- `AMENDED_BY` — statute version history
- `APPLIES_TO` — facet edges: JJ Act `APPLIES_TO` offenders < 18
- `SIMILAR_FACTS` — case ↔ case semantic similarity (computed from embeddings)

### Communities (constellation colors)

Criminal Law · Juvenile Justice · Constitutional · Civil / Tort · Property · Corporate · Procedural — each a colored cluster, exactly like the reference site's 9 schools.

---

## 3. The RAG pipeline (scenario → lit constellation)

```
Lawyer's scenario text
   │
   ├─ 1. LLM facet extraction
   │      "murder by 14yo in Maharashtra"
   │        → {offense: murder, offender_age: 14, jurisdiction: MH}
   │
   ├─ 2. Facet → node matching
   │      statutes (IPC §302, JJ Act), facet nodes (juvenile), jurisdiction node
   │
   ├─ 3. Graph traversal
   │      GOVERNS / APPLIES_TO edges → applicable law
   │      CITES/RELIED_UPON 2-hop → precedent subgraph
   │      treatment check → prune OVERRULED nodes (or show them marked dead)
   │
   ├─ 4. Similar-case retrieval
   │      embed scenario → vector search over case nodes
   │      filter by jurisdiction hierarchy + recency
   │
   ├─ 5. LLM case-study pass
   │      System: "You are a legal research assistant. Answer ONLY from the
   │               provided nodes. Cite the exact node IDs. Never invent citations.
   │               Note jurisdiction and currency of every source."
   │      Output: IRAC summary + node ID list → frontend lights those nodes
   │
   └─ 6. Treatment warning layer
          If any retrieved case is QUESTIONED/OVERRULED → visible amber/red badge
```

**Key detail (same as biomedical):** the model returns the node IDs it relied on, so the lit constellation is provably the answer's source set. No invisible hallucinations.

---

## 4. Why this beats plain vector RAG for law

- **Citation relationships are the law.** A flat embedding search retrieves "similar sounding" text; the graph retrieves *binding precedent* and its current validity.
- **Jurisdiction is structural, not semantic** — hierarchy edges make filtering exact.
- **Stare decisis visualization**: seeing a line of cases `CITES → CITES → CITES` from 1998 to 2025 tells a story no list can.
- **The "murder by 14yo" query is genuinely hard for plain RAG**: the answer lives at the *intersection* of IPC §302 and the JJ Act — graph traversal finds intersections; vectors don't.

## 5. Data sources

- **Indian Kanoon API** (Indian case law + statutes — the obvious fit for the India example)
- Court websites / eCourts, SCC/Manupatra (licensed, for a commercial version)
- US version: CourtListener (free, full opinion text + citation network — already a graph!)
- Statute texts from official gazettes
- Start curated: 1 jurisdiction + 1 domain (e.g., Indian criminal law, ~300 cases + ~80 statute sections) before scaling

## 6. Safety & trust requirements

- "Research assistance, not legal advice" disclaimer on every output
- Every claim must cite a node with a real citation string — the UI shows the source card on hover
- Currency stamps: "last verified treatment: <date>" per case node
- Never auto-assert outcomes ("the accused will be tried as adult") — present as "courts have held / open question"

## 7. MVP scope

- 350 nodes, ~2,000 edges, 5 communities (Indian criminal + juvenile justice focus)
- Facet extraction + traversal + similar-case retrieval + IRAC answer pass
- Constellation with treatment-colored edges + case-card side panel
- Jurisdiction filter
- Later: multi-jurisdiction compare mode, timeline view (doctrine evolution 1960→2026), brief-drafting export, citation-graph import from CourtListener/Indian Kanoon at scale
