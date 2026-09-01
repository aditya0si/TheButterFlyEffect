/**
 * Application Orchestrator & UI Controller.
 * Manages mode switching with live 3D sector refocusing and interactive pathway navigation.
 */

const API_BASE = window.location.origin.includes("localhost") || window.location.origin.includes("127.0.0.1")
  ? "" 
  : "http://localhost:8000";

let engine = null;
let currentMode = "triage";
let activeSelectedNode = null;
const PRO_MODE_KEY = "auramed_pro_mode";

const PRESETS = {
  triage: [
    { query: "I have high fever and severe body pain since yesterday", label: "⚡ Fever & Body Aches" },
    { query: "Throbbing unilateral headache with nausea and flashing lights", label: "⚡ Classic Migraine Attack" },
    { query: "Severe epigastric burning pain and acid reflux after eating", label: "⚡ Acid Reflux & GERD" },
    { query: "Retrosternal chest tightness and exertional shortness of breath", label: "⚡ Angina Ischemia Pattern" }
  ],
  drug_moa: [
    { query: "Sumatriptan 5-HT1D agonism and trigeminal vasodilation", label: "⚡ Sumatriptan 5-HT1D MoA" },
    { query: "Osimertinib EGFR tyrosine kinase inhibition in NSCLC", label: "⚡ Osimertinib Kinase MoA" },
    { query: "Omeprazole covalent inhibition of gastric proton pump", label: "⚡ PPI Proton Pump Target" },
    { query: "Erenumab CGRP receptor monoclonal antibody blockade", label: "⚡ CGRP Target Pathway" }
  ],
  polypharmacy: [
    { query: "Dangerous interaction between Warfarin and Fluconazole", label: "⚡ Warfarin + Fluconazole CYP2C9" },
    { query: "Ciprofloxacin co-administration with Warfarin bleeding risk", label: "⚡ Ciprofloxacin + Warfarin Hazard" },
    { query: "Fluconazole CYP3A4 inhibition increasing Atorvastatin levels", label: "⚡ Statin Toxicity Risk" }
  ],
  multi_omics: [
    { query: "EGFR activating mutations and downstream oncogenic cascades in lung cancer", label: "⚡ EGFR L858R Cascade" },
    { query: "TNF-alpha master cytokine signaling in rheumatoid synovitis", label: "⚡ TNF-α Inflammatory Axis" },
    { query: "TLR9 endosomal nucleic acid sensing in systemic lupus", label: "⚡ TLR9 Autoimmune Axis" }
  ],
  rare_disease: [
    { query: "Joint hypermobility with skin elasticity and COL3A1 mutation", label: "⚡ Ehlers-Danlos Vascular Defect" },
    { query: "FBN1 fibrillin deficiency with aortic root enlargement", label: "⚡ Marfan Syndromic Cluster" }
  ]
};

document.addEventListener("DOMContentLoaded", async () => {
  // 1. Initialize 3D Cosmic Constellation Engine
  engine = new ConstellationEngine("constellationCanvas");

  // 2. Load Dense Star Graph
  await loadGraphData();

  // 3. Bind UI Handlers
  bindEvents();

  // 4. Restore consumer/pro preference (consumer-first by default)
  applyProModeVisibility();
});

async function loadGraphData() {
  try {
    const res = await fetch(`${API_BASE}/api/graph/full`);
    if (res.ok) {
      const data = await res.json();
      engine.loadGraphData(data);
      updateTelemetry(`Sky loaded · ${data.node_count} stars`);
    } else {
      throw new Error("Failed to fetch graph topology");
    }
  } catch (err) {
    console.warn("Using fallback local network_data.json:", err);
    try {
      const localRes = await fetch("network_data.json");
      const localData = await localRes.json();
      engine.loadGraphData(localData);
      updateTelemetry(`Cosmos Loaded (${localData.node_count} Stars)`);
    } catch (e) {
      console.error("Critical: Unable to load graph topology", e);
    }
  }
}

function bindEvents() {
  // Mode Navigation with Immediate 3D Sector Refresh
  const modeButtons = document.querySelectorAll(".mode-btn");
  modeButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      modeButtons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      currentMode = btn.dataset.mode;
      renderQuickPrompts();

      // Refresh and fly 3D canvas to this sector!
      if (engine) {
        engine.focusSector(currentMode);
        updateTelemetry(`Pivoting to ${btn.textContent.trim()} Sector...`);
      }
    });
  });

  renderQuickPrompts();

  // Search Form Submit
  const searchForm = document.getElementById("searchForm");
  const queryInput = document.getElementById("queryInput");

  searchForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const query = queryInput.value.trim();
    if (!query) return;

    await executeGraphRAGQuery(query);
  });

  // Reset Camera Button
  document.getElementById("resetCamBtn").addEventListener("click", () => {
    engine.resetCamera();
  });

  // Pro Mode Toggle (consumer-first: expert modes hidden by default)
  document.getElementById("proModeBtn").addEventListener("click", () => {
    const enabling = !isProModeEnabled();
    localStorage.setItem(PRO_MODE_KEY, enabling ? "1" : "0");
    applyProModeVisibility();
    updateTelemetry(enabling ? "Pro modes unlocked" : "Simple mode");
  });

  // Close Side Synthesis Panel
  document.getElementById("closePanelBtn").addEventListener("click", () => {
    document.getElementById("synthesisPanel").classList.remove("open");
  });

  // Node Click in Canvas -> Open Deep Dive Inspector
  engine.onNodeClickCallback = (node) => {
    openNodeInspector(node);
  };

  // Close Node Inspector Drawer
  document.getElementById("closeInspectorBtn").addEventListener("click", closeNodeInspector);
  document.getElementById("inspectorBackdrop").addEventListener("click", closeNodeInspector);

  // Inspector Tab Switching
  const tabButtons = document.querySelectorAll(".inspector-tabs .tab-btn");
  tabButtons.forEach((tab) => {
    tab.addEventListener("click", () => {
      tabButtons.forEach((t) => t.classList.remove("active"));
      document.querySelectorAll(".tab-pane").forEach((p) => p.classList.remove("active"));
      tab.classList.add("active");
      const targetPane = document.getElementById(`tab${capitalize(tab.dataset.tab)}`);
      if (targetPane) targetPane.classList.add("active");
    });
  });

  // Inspector Action Buttons
  document.getElementById("focusNodeBtn").addEventListener("click", () => {
    if (activeSelectedNode) {
      engine.focusCameraOnNode(activeSelectedNode.id);
      closeNodeInspector();
    }
  });

  document.getElementById("triggerQueryFromNodeBtn").addEventListener("click", () => {
    if (activeSelectedNode) {
      document.getElementById("queryInput").value = activeSelectedNode.name;
      executeGraphRAGQuery(activeSelectedNode.name);
      closeNodeInspector();
    }
  });
}

function isProModeEnabled() {
  return localStorage.getItem(PRO_MODE_KEY) === "1";
}

function applyProModeVisibility() {
  const proEnabled = isProModeEnabled();
  document.querySelectorAll(".mode-btn.pro-mode").forEach((btn) => {
    btn.classList.toggle("hidden-mode", !proEnabled);
  });
  const toggleBtn = document.getElementById("proModeBtn");
  if (toggleBtn) {
    toggleBtn.classList.toggle("enabled", proEnabled);
    toggleBtn.textContent = proEnabled ? "Pro ✓" : "Pro";
    toggleBtn.title = proEnabled
      ? "Hide research & clinical modes"
      : "Show research & clinical modes";
  }

  // If pro mode was just disabled while sitting in an expert mode, fall back to triage
  if (!proEnabled && currentMode !== "triage") {
    const triageBtn = document.querySelector('.mode-btn[data-mode="triage"]');
    if (triageBtn) triageBtn.click();
  }
}

function renderQuickPrompts() {
  const container = document.getElementById("quickPrompts");
  container.innerHTML = "";
  const prompts = PRESETS[currentMode] || PRESETS.triage;

  prompts.forEach((p) => {
    const chip = document.createElement("span");
    chip.className = "prompt-chip";
    chip.textContent = p.label;
    chip.addEventListener("click", () => {
      document.getElementById("queryInput").value = p.query;
      executeGraphRAGQuery(p.query);
    });
    container.appendChild(chip);
  });
}

async function executeGraphRAGQuery(query) {
  updateTelemetry("Tracing your starpath...");
  const submitBtn = document.getElementById("submitBtn");
  submitBtn.disabled = true;

  try {
    const res = await fetch(`${API_BASE}/api/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, mode: currentMode })
    });

    if (!res.ok) throw new Error("API Query Failed");
    const data = await res.json();

    // 1. Highlight 3D Constellation
    const litNodes = data.synthesis.lit_node_ids || [data.center_node_id];
    const litEdges = data.synthesis.lit_edge_ids || [];
    engine.highlightPath(litNodes, litEdges);
    engine.focusCameraOnNode(data.center_node_id);

    // 2. Populate Synthesis Side Panel
    renderSynthesisPanel(data);

    updateTelemetry(`Found ${litNodes.length} connected stars`);
  } catch (err) {
    console.error("Query Error:", err);
    updateTelemetry("Query Failed");
  } finally {
    submitBtn.disabled = false;
  }
}

function renderSynthesisPanel(data) {
  const synth = data.synthesis;
  const panel = document.getElementById("synthesisPanel");

  document.getElementById("panelHeadline").textContent = synth.headline;
  
  // Match Confidence Meter
  const conf = synth.match_confidence || 90;
  document.getElementById("meterValue").textContent = `${conf}%`;
  document.getElementById("meterFill").style.width = `${conf}%`;

  // 1. Plain Words Verdict
  document.getElementById("plainVerdictText").textContent = synth.plain_verdict;

  // 2. Interactive Pathway Steps (Clicking step highlights & zooms to that star in 3D!)
  const stepsContainer = document.getElementById("pathwayStepsContainer");
  stepsContainer.innerHTML = "";

  if (synth.pathway_steps && synth.pathway_steps.length > 0) {
    synth.pathway_steps.forEach((st) => {
      const stepItem = document.createElement("div");
      stepItem.className = "pathway-step-card";
      stepItem.innerHTML = `
        <div class="step-num">${st.step}</div>
        <div class="step-info">
          <div class="step-header">
            <span class="step-name">${st.name}</span>
            <span class="step-role">${st.role}</span>
          </div>
          <p class="step-detail">${st.detail}</p>
        </div>
      `;
      stepItem.addEventListener("click", () => {
        document.querySelectorAll(".pathway-step-card").forEach(c => c.classList.remove("selected"));
        stepItem.classList.add("selected");
        engine.focusCameraOnNode(st.node_id);
      });
      stepsContainer.appendChild(stepItem);
    });
  }

  // 3. Red Flag Alert Pill
  const redFlagCard = document.getElementById("redFlagCard");
  if (synth.red_flags && synth.red_flags.length > 0) {
    redFlagCard.style.display = "flex";
    document.getElementById("redFlagContent").innerHTML = `<strong>Critical Signs to Watch:</strong> ${synth.red_flags.join(', ')}`;
  } else {
    redFlagCard.style.display = "none";
  }

  // 4. Care Tips
  const careList = document.getElementById("careTipsList");
  careList.innerHTML = "";
  (synth.care_tips || ["Rest in a dim room", "Hydrate with electrolytes"]).forEach((tip) => {
    const li = document.createElement("li");
    li.textContent = tip;
    careList.appendChild(li);
  });

  panel.classList.add("open");
}

async function openNodeInspector(node) {
  activeSelectedNode = node;
  const drawer = document.getElementById("nodeInspector");
  const backdrop = document.getElementById("inspectorBackdrop");

  document.getElementById("inspectorType").textContent = node.type || "Biomedical Entity";
  document.getElementById("inspectorTitle").textContent = node.name;
  document.getElementById("propDomain").textContent = node.domain || "General Medicine";
  document.getElementById("propSeverity").textContent = node.severity_level || "Normal";
  document.getElementById("propAliases").textContent = node.aliases && node.aliases.length > 0 ? node.aliases.join(", ") : "None";
  document.getElementById("inspectorSummary").textContent = node.summary || "No description available.";

  try {
    const res = await fetch(`${API_BASE}/api/nodes/${node.id}`);
    if (res.ok) {
      const detail = await res.json();
      renderInspectorConnections(detail.subgraph);
    }
  } catch (e) {
    console.warn("Could not fetch node deep detail:", e);
  }

  drawer.classList.add("open");
  backdrop.classList.add("open");
}

function renderInspectorConnections(subgraph) {
  const container = document.getElementById("inspectorConnections");
  container.innerHTML = "";

  if (!subgraph || !subgraph.one_hop_nodes || subgraph.one_hop_nodes.length === 0) {
    container.innerHTML = "<p style='color:var(--text-muted)'>No direct 1-hop connections found.</p>";
    return;
  }

  subgraph.one_hop_nodes.forEach((conn) => {
    const item = document.createElement("div");
    item.style.cssText = "background:var(--bg-card); padding:12px 16px; border-radius:12px; margin-bottom:10px; border:1px solid var(--border-subtle); display:flex; justify-content:space-between; align-items:center;";
    item.innerHTML = `
      <div>
        <strong style="color:#fff; font-size:0.92rem;">${conn.name}</strong>
        <div style="font-size:0.78rem; color:var(--text-muted);">${conn.type} • ${conn.domain}</div>
      </div>
      <button style="background:rgba(0,223,216,0.15); border:1px solid var(--cosmic-cyan); color:#00dfd8; padding:5px 14px; border-radius:14px; font-size:0.78rem; cursor:pointer;">Inspect</button>
    `;
    item.querySelector("button").addEventListener("click", () => {
      openNodeInspector(conn);
      engine.focusCameraOnNode(conn.id);
    });
    container.appendChild(item);
  });
}

function closeNodeInspector() {
  document.getElementById("nodeInspector").classList.remove("open");
  document.getElementById("inspectorBackdrop").classList.remove("open");
}

function updateTelemetry(text) {
  const el = document.getElementById("telemetryStatus");
  if (el) el.textContent = text;
}

function capitalize(s) {
  if (!s) return "";
  return s.charAt(0).toUpperCase() + s.slice(1);
}
