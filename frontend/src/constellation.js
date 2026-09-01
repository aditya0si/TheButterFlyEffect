/**
 * Cosmic 3D Starfield Constellation Engine (Three.js WebGL).
 * Features:
 * - Dynamic Sector Focusing on SaaS Mode Switching
 * - Step-by-Step Interactive Pathway Navigation
 * - Floating 3D Hover Tooltip HUD
 * - Procedural Star Diffraction Flare Spikes & Volumetric Nebulae
 * - Animated Laser Filaments with Synaptic Pulses
 */

class ConstellationEngine {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.nodes = [];
    this.edges = [];
    this.nodeMap = new Map();
    this.litNodeIds = new Set();
    this.litEdgeIds = new Set();
    
    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.controls = null;
    this.raycaster = new THREE.Raycaster();
    this.mouse = new THREE.Vector2();
    
    this.starTexture = null;
    this.nebulaGroup = null;
    this.nodeMesh = null;
    this.haloGroup = null;
    this.edgeLines = null;
    this.hoveredNode = null;
    this.onNodeClickCallback = null;
    this.clock = new THREE.Clock();

    this.tooltipEl = this.createTooltipElement();
    this.initScene();
    this.animate();
  }

  createTooltipElement() {
    let el = document.getElementById("canvasHoverTooltip");
    if (!el) {
      el = document.createElement("div");
      el.id = "canvasHoverTooltip";
      el.style.cssText = `
        position: absolute;
        display: none;
        pointer-events: none;
        background: rgba(10, 12, 28, 0.92);
        border: 1px solid #00dfd8;
        border-radius: 12px;
        padding: 8px 14px;
        color: #fff;
        font-family: 'Outfit', sans-serif;
        font-size: 0.82rem;
        z-index: 1000;
        backdrop-filter: blur(16px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.8), 0 0 15px rgba(0, 223, 216, 0.3);
        transform: translate(15px, -50%);
        transition: opacity 0.15s ease;
      `;
      document.body.appendChild(el);
    }
    return el;
  }

  createProceduralStarTexture() {
    const size = 128;
    const canvas = document.createElement("canvas");
    canvas.width = size;
    canvas.height = size;
    const ctx = canvas.getContext("2d");
    const center = size / 2;

    const gradient = ctx.createRadialGradient(center, center, 0, center, center, center);
    gradient.addColorStop(0.0, "rgba(255, 255, 255, 1.0)");
    gradient.addColorStop(0.18, "rgba(230, 245, 255, 0.85)");
    gradient.addColorStop(0.45, "rgba(0, 223, 216, 0.35)");
    gradient.addColorStop(0.75, "rgba(180, 40, 255, 0.12)");
    gradient.addColorStop(1.0, "rgba(0, 0, 0, 0)");

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, size, size);

    // 4-Point Astronomical Diffraction Spikes
    ctx.strokeStyle = "rgba(255, 255, 255, 0.85)";
    ctx.lineWidth = 1.4;
    ctx.beginPath();
    ctx.moveTo(center, 4);
    ctx.lineTo(center, size - 4);
    ctx.moveTo(4, center);
    ctx.lineTo(size - 4, center);
    ctx.stroke();

    return new THREE.CanvasTexture(canvas);
  }

  initScene() {
    this.starTexture = this.createProceduralStarTexture();

    this.scene = new THREE.Scene();
    this.scene.fog = new THREE.FogExp2(0x02040a, 0.0012);

    const aspect = window.innerWidth / window.innerHeight;
    this.camera = new THREE.PerspectiveCamera(50, aspect, 1, 3500);
    this.camera.position.set(0, 45, 380);

    this.renderer = new THREE.WebGLRenderer({
      canvas: this.canvas,
      antialias: true,
      alpha: true,
      powerPreference: "high-performance"
    });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.05;
    this.controls.maxDistance = 900;
    this.controls.minDistance = 15;
    this.controls.autoRotate = true;
    this.controls.autoRotateSpeed = 0.22;

    this.createVolumetricNebula();

    window.addEventListener("resize", () => this.onResize());
    this.canvas.addEventListener("mousemove", (e) => this.onMouseMove(e));
    this.canvas.addEventListener("click", (e) => this.onClick(e));
  }

  createVolumetricNebula() {
    this.nebulaGroup = new THREE.Group();
    const particleCount = 2800;
    const geo = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    const cosmicPalette = [
      new THREE.Color(0x7928ca), // Purple
      new THREE.Color(0xff0080), // Magenta
      new THREE.Color(0x00dfd8), // Cyan
      new THREE.Color(0x0070f3), // Blue
      new THREE.Color(0xffffff)  // White
    ];

    for (let i = 0; i < particleCount; i++) {
      const radius = 90 + Math.random() * 950;
      const theta = Math.random() * Math.PI * 2;
      const phi = (Math.random() - 0.5) * Math.PI * 0.7;

      positions[i * 3] = radius * Math.cos(theta) * Math.cos(phi);
      positions[i * 3 + 1] = radius * Math.sin(phi) * 0.5 + (Math.random() - 0.5) * 90;
      positions[i * 3 + 2] = radius * Math.sin(theta) * Math.cos(phi);

      const color = cosmicPalette[Math.floor(Math.random() * cosmicPalette.length)];
      colors[i * 3] = color.r;
      colors[i * 3 + 1] = color.g;
      colors[i * 3 + 2] = color.b;
    }

    geo.setAttribute("position", new THREE.BufferAttribute(positions, 3));
    geo.setAttribute("color", new THREE.BufferAttribute(colors, 3));

    const mat = new THREE.PointsMaterial({
      size: 4.5,
      map: this.starTexture,
      vertexColors: true,
      transparent: true,
      opacity: 0.4,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    });

    const nebula = new THREE.Points(geo, mat);
    this.nebulaGroup.add(nebula);
    this.scene.add(this.nebulaGroup);
  }

  loadGraphData(graphData) {
    this.nodes = graphData.nodes || [];
    this.edges = graphData.edges || [];
    this.nodeMap.clear();

    this.nodes.forEach((n, idx) => {
      this.nodeMap.set(n.id, { ...n, index: idx });
    });

    this.buildGraphMeshes();
  }

  buildGraphMeshes() {
    if (this.nodeMesh) this.scene.remove(this.nodeMesh);
    if (this.haloGroup) this.scene.remove(this.haloGroup);
    if (this.edgeLines) this.scene.remove(this.edgeLines);

    const nodeCount = this.nodes.length;
    const geometry = new THREE.SphereGeometry(1.6, 16, 16);
    const material = new THREE.MeshBasicMaterial({ color: 0xffffff });
    
    this.nodeMesh = new THREE.InstancedMesh(geometry, material, nodeCount);
    const dummy = new THREE.Object3D();
    const color = new THREE.Color();

    this.haloGroup = new THREE.Group();

    this.nodes.forEach((node, i) => {
      const [x, y, z] = node.coordinates_3d || [0, 0, 0];
      dummy.position.set(x, y, z);
      dummy.scale.set(1.0, 1.0, 1.0);
      dummy.updateMatrix();
      this.nodeMesh.setMatrixAt(i, dummy.matrix);

      color.set(node.base_color || "#00dfd8");
      this.nodeMesh.setColorAt(i, color);

      const spriteMat = new THREE.SpriteMaterial({
        map: this.starTexture,
        color: node.base_color || "#00dfd8",
        transparent: true,
        opacity: 0.45,
        blending: THREE.AdditiveBlending,
        depthWrite: false
      });
      const sprite = new THREE.Sprite(spriteMat);
      sprite.position.set(x, y, z);
      sprite.scale.set(14, 14, 1);
      this.haloGroup.add(sprite);
    });

    this.nodeMesh.instanceMatrix.needsUpdate = true;
    if (this.nodeMesh.instanceColor) this.nodeMesh.instanceColor.needsUpdate = true;

    this.scene.add(this.nodeMesh);
    this.scene.add(this.haloGroup);

    this.buildEdgeSegments();
  }

  buildEdgeSegments() {
    const linePositions = [];
    const lineColors = [];
    const colorA = new THREE.Color();
    const colorB = new THREE.Color();

    this.edges.forEach((edge) => {
      const src = this.nodeMap.get(edge.source);
      const tgt = this.nodeMap.get(edge.target);

      if (src && tgt) {
        linePositions.push(src.coordinates_3d[0], src.coordinates_3d[1], src.coordinates_3d[2]);
        linePositions.push(tgt.coordinates_3d[0], tgt.coordinates_3d[1], tgt.coordinates_3d[2]);

        const isLit = this.litEdgeIds.has(edge.id);
        if (isLit) {
          colorA.set(0xff0080); // Pink
          colorB.set(0x00dfd8); // Cyan
        } else {
          colorA.set(0x1a1236); // Dim purple
          colorB.set(0x0f1c3a); // Dim blue
        }

        lineColors.push(colorA.r, colorA.g, colorA.b);
        lineColors.push(colorB.r, colorB.g, colorB.b);
      }
    });

    const edgeGeo = new THREE.BufferGeometry();
    edgeGeo.setAttribute("position", new THREE.Float32BufferAttribute(linePositions, 3));
    edgeGeo.setAttribute("color", new THREE.Float32BufferAttribute(lineColors, 3));

    const edgeMat = new THREE.LineBasicMaterial({
      vertexColors: true,
      transparent: true,
      opacity: 0.55,
      blending: THREE.AdditiveBlending
    });

    this.edgeLines = new THREE.LineSegments(edgeGeo, edgeMat);
    this.scene.add(this.edgeLines);
  }

  /**
   * Mode Switching: Refreshes the constellation and pivots to that sector's flagship galaxy
   */
  focusSector(mode) {
    const modeTargets = {
      triage: { keyword: "Neurology", x: 120, y: 35, z: 220, targetX: 60, targetY: 0, targetZ: 0 },
      drug_moa: { keyword: "Pharmacology", x: -90, y: 50, z: 240, targetX: -40, targetY: 0, targetZ: 0 },
      polypharmacy: { keyword: "Pharmacology", x: 0, y: -80, z: 250, targetX: 0, targetY: -20, targetZ: 0 },
      multi_omics: { keyword: "Oncology", x: -140, y: 60, z: 200, targetX: -80, targetY: 20, targetZ: 0 },
      rare_disease: { keyword: "Genetics", x: 140, y: -60, z: 210, targetX: 70, targetY: -20, targetZ: 0 }
    };

    const targetConfig = modeTargets[mode] || modeTargets.triage;
    
    // Find sector representative nodes
    const sectorNodes = this.nodes.filter(n => n.domain.toLowerCase().includes(targetConfig.keyword.toLowerCase()));
    const previewLitNodes = sectorNodes.slice(0, 12).map(n => n.id);
    const previewLitEdges = this.edges.filter(e => previewLitNodes.includes(e.source) || previewLitNodes.includes(e.target)).slice(0, 18).map(e => e.id);

    this.highlightPath(previewLitNodes, previewLitEdges);

    this.controls.autoRotate = false;
    gsap.to(this.camera.position, {
      x: targetConfig.x,
      y: targetConfig.y,
      z: targetConfig.z,
      duration: 1.8,
      ease: "power2.inOut",
      onComplete: () => {
        this.controls.autoRotate = true;
      }
    });

    gsap.to(this.controls.target, {
      x: targetConfig.targetX,
      y: targetConfig.targetY,
      z: targetConfig.targetZ,
      duration: 1.8,
      ease: "power2.inOut"
    });
  }

  highlightPath(litNodeIds, litEdgeIds) {
    this.litNodeIds = new Set(litNodeIds);
    this.litEdgeIds = new Set(litEdgeIds);

    const dummy = new THREE.Object3D();
    const color = new THREE.Color();

    this.nodes.forEach((node, i) => {
      const [x, y, z] = node.coordinates_3d;
      dummy.position.set(x, y, z);
      
      const isLit = this.litNodeIds.has(node.id);
      const scale = isLit ? 3.2 : 0.65;
      dummy.scale.set(scale, scale, scale);
      dummy.updateMatrix();
      this.nodeMesh.setMatrixAt(i, dummy.matrix);

      if (isLit) {
        color.set(0xffffff);
      } else {
        color.set(node.base_color || "#00dfd8").multiplyScalar(0.18);
      }
      this.nodeMesh.setColorAt(i, color);

      const halo = this.haloGroup.children[i];
      if (halo) {
        const haloSize = isLit ? 42 : 6;
        halo.scale.set(haloSize, haloSize, 1);
        halo.material.opacity = isLit ? 1.0 : 0.1;
      }
    });

    this.nodeMesh.instanceMatrix.needsUpdate = true;
    if (this.nodeMesh.instanceColor) this.nodeMesh.instanceColor.needsUpdate = true;

    if (this.edgeLines) this.scene.remove(this.edgeLines);
    this.buildEdgeSegments();
  }

  focusCameraOnNode(nodeId) {
    const node = this.nodeMap.get(nodeId);
    if (!node) return;

    const [x, y, z] = node.coordinates_3d;
    this.controls.autoRotate = false;

    gsap.to(this.camera.position, {
      x: x + 20,
      y: y + 14,
      z: z + 50,
      duration: 1.8,
      ease: "power3.inOut"
    });

    gsap.to(this.controls.target, {
      x: x,
      y: y,
      z: z,
      duration: 1.8,
      ease: "power3.inOut"
    });
  }

  resetCamera() {
    this.controls.autoRotate = true;
    gsap.to(this.camera.position, {
      x: 0,
      y: 45,
      z: 380,
      duration: 1.6,
      ease: "power2.out"
    });
    gsap.to(this.controls.target, {
      x: 0,
      y: 0,
      z: 0,
      duration: 1.6,
      ease: "power2.out"
    });
  }

  onMouseMove(event) {
    const rect = this.canvas.getBoundingClientRect();
    this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    this.mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

    this.raycaster.setFromCamera(this.mouse, this.camera);
    if (this.nodeMesh) {
      const intersects = this.raycaster.intersectObject(this.nodeMesh);
      if (intersects.length > 0) {
        const instanceId = intersects[0].instanceId;
        this.canvas.style.cursor = "pointer";
        this.hoveredNode = this.nodes[instanceId];

        // Update floating 3D hover tooltip
        if (this.hoveredNode) {
          this.tooltipEl.style.display = "block";
          this.tooltipEl.style.left = `${event.clientX}px`;
          this.tooltipEl.style.top = `${event.clientY}px`;
          this.tooltipEl.innerHTML = `
            <div style="font-weight:700; color:#fff; margin-bottom:2px;">✨ ${this.hoveredNode.name}</div>
            <div style="font-size:0.72rem; color:#00dfd8;">${this.hoveredNode.type} • ${this.hoveredNode.domain.split(',')[0]}</div>
          `;
        }
      } else {
        this.canvas.style.cursor = "default";
        this.hoveredNode = null;
        this.tooltipEl.style.display = "none";
      }
    }
  }

  onClick(event) {
    if (this.hoveredNode && this.onNodeClickCallback) {
      this.onNodeClickCallback(this.hoveredNode);
    }
  }

  onResize() {
    this.camera.aspect = window.innerWidth / window.innerHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(window.innerWidth, window.innerHeight);
  }

  animate() {
    requestAnimationFrame(() => this.animate());
    const elapsedTime = this.clock.getElapsedTime();

    if (this.nebulaGroup) {
      this.nebulaGroup.rotation.y = elapsedTime * 0.015;
    }

    this.controls.update();
    this.renderer.render(this.scene, this.camera);
  }
}
