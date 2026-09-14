---
comments: false
tags: [about]
---

I am a **Data Science & AI leader** focused on turning AI into practical, scalable business solutions. Over my career at **Cardinal Health, Nestlé, Novartis, and ZS**, I have worked across AI, data science, analytics, and strategy, primarily in Healthcare, Life Sciences, Retail, and Consumer Products.

My focus is on **AI strategy, GenAI, agentic systems, machine learning, and AI product development**—from identifying high-value opportunities to designing architectures and building solutions that move from prototype to production.

I remain deeply hands-on with **Python and R** and enjoy working at the intersection of business, technology, and AI. I believe strong AI leadership requires both **strategic thinking and technical depth**: knowing where AI can create value, how to build it, and how to scale it responsibly.

## Core Competencies

* **AI Strategy & Transformation** — AI roadmaps, use-case prioritization, and scaling AI capabilities
* **Generative AI & Agents** — LLM applications, agentic workflows, orchestration, RAG, and evaluation
* **Data Science & ML** — predictive modeling, statistical analysis, feature engineering, and decision science
* **AI Product & Architecture** — translating business problems into scalable AI products and systems
* **Executive Communication** — simplifying complex technology into clear business narratives
* **Healthcare & Life Sciences** — deep experience applying analytics and AI to complex business problems

## Education

Master’s in **Data Science & Project Management**, University of Connecticut School of Business.

**My goal is simple: build AI systems that are useful, scalable, and grounded in real business problems—not hype.**



About The Site
=========
This site is powered by [Jekyll](http://jekyllrb.com/) using the [Minimal Mistakes](http://mademistakes.com/minimal-mistakes/) theme.

<!-- 3D backdrop: same Three.js CDN pin as the homepage constellation, canvas fixed behind the content -->
<div class="about3d" aria-hidden="true"><canvas id="about3d-canvas"></canvas></div>
<style>
.about3d canvas{position:fixed;inset:0;width:100vw;height:100vh;z-index:0;pointer-events:none;opacity:.85}
#main{position:relative;z-index:1}
.page__footer{position:relative;z-index:1}
@media (prefers-reduced-motion:reduce){.about3d canvas{opacity:.45}}
</style>
<script type="importmap">
{"imports": {"three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js"}}
</script>
<script type="module">
import * as THREE from 'three';

const canvas = document.getElementById('about3d-canvas');
if (!canvas) { throw new Error('about3d canvas missing'); }

let renderer;
try {
  renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
} catch (e) {
  canvas.remove();
  throw e;
}

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 100);
camera.position.set(0, 0, 14);

function themeAccent(fallbackColor) {
  const v = getComputedStyle(document.documentElement).getPropertyValue('--acc-1');
  return (v && v.trim()) || fallbackColor;
}

const group = new THREE.Group();
scene.add(group);

const wire = new THREE.Mesh(
  new THREE.IcosahedronGeometry(3.2, 1),
  new THREE.MeshBasicMaterial({ color: new THREE.Color(themeAccent('#38bdf8')), wireframe: true, transparent: true, opacity: 0.32 })
);
group.add(wire);

const core = new THREE.Mesh(
  new THREE.IcosahedronGeometry(3.2, 1),
  new THREE.MeshBasicMaterial({ color: new THREE.Color(themeAccent('#38bdf8')), transparent: true, opacity: 0.05 })
);
group.add(core);

const ring = new THREE.Mesh(
  new THREE.TorusGeometry(4.6, 0.015, 8, 128),
  new THREE.MeshBasicMaterial({ color: new THREE.Color(themeAccent('#38bdf8')), transparent: true, opacity: 0.4 })
);
ring.rotation.x = Math.PI / 2.6;
group.add(ring);

const STAR_N = 450;
const starPos = new Float32Array(STAR_N * 3);
for (let i = 0; i < STAR_N; i++) {
  starPos[i * 3] = (Math.random() - 0.5) * 40;
  starPos[i * 3 + 1] = (Math.random() - 0.5) * 24;
  starPos[i * 3 + 2] = -Math.random() * 20 - 2;
}
const starGeo = new THREE.BufferGeometry();
starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
const stars = new THREE.Points(
  starGeo,
  new THREE.PointsMaterial({ color: new THREE.Color(themeAccent('#38bdf8')), size: 0.05, transparent: true, opacity: 0.7 })
);
scene.add(stars);

function applyTheme() {
  const c = new THREE.Color(themeAccent('#38bdf8'));
  wire.material.color.copy(c);
  core.material.color.copy(c);
  ring.material.color.copy(c);
  stars.material.color.copy(c);
}
const themeBtn = document.getElementById('theme-toggle');
if (themeBtn) { themeBtn.addEventListener('click', () => setTimeout(applyTheme, 50)); }

let tx = 0, ty = 0, mx = 0, my = 0;
window.addEventListener('pointermove', (e) => {
  tx = (e.clientX / window.innerWidth - 0.5) * 2;
  ty = (e.clientY / window.innerHeight - 0.5) * 2;
}, { passive: true });

function fit() {
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setSize(window.innerWidth, window.innerHeight, false);
  camera.aspect = window.innerWidth / window.innerHeight;
  group.position.x = camera.aspect > 1.2 ? 4.2 : 0;
  camera.updateProjectionMatrix();
}
window.addEventListener('resize', fit);
fit();

function render() {
  renderer.render(scene, camera);
}
render();

const reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (!reduceMotion) {
  const clock = new THREE.Clock();
  let running = true;
  document.addEventListener('visibilitychange', () => {
    running = !document.hidden;
    if (running) { loop(); }
  });
  (function loop() {
    if (!running) { return; }
    requestAnimationFrame(loop);
    const t = clock.getElapsedTime();
    mx += (tx - mx) * 0.03;
    my += (ty - my) * 0.03;
    group.rotation.y = t * 0.12 + mx * 0.4;
    group.rotation.x = Math.sin(t * 0.2) * 0.15 + my * 0.25;
    ring.rotation.z = t * 0.05;
    stars.rotation.y = t * 0.005;
    render();
  })();
}
</script>
