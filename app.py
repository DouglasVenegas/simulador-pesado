import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Lab Finder", layout="wide")

html_code = r"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Lab Finder — Inventario de Laboratorio</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #f0f2f5;
    --surface: #ffffff;
    --border: #e2e6ea;
    --accent: #2563eb;
    --accent2: #16a34a;
    --text: #111827;
    --muted: #6b7280;
    --highlight: #fef08a;
    --zone-f: #4ade80;
    --zone-a: #fb923c;
    --zone-e: #93c5fd;
    --zone-l: #93c5fd;
    --zone-k: #93c5fd;
    --zone-cong: #f9a8d4;
    --zone-cap: #d8b4fe;
    --zone-inv: #e5e7eb;
    --active-glow: rgba(37,99,235,0.25);
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'DM Sans', sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
  }

  header {
    background: var(--text);
    color: white;
    padding: 18px 24px;
    display: flex;
    align-items: center;
    gap: 14px;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 2px 12px rgba(0,0,0,0.3);
  }

  header .logo {
    font-family: 'Space Mono', monospace;
    font-size: 1.15rem;
    letter-spacing: -0.5px;
    font-weight: 700;
    color: #fff;
  }

  header .logo span { color: #4ade80; }

  .search-wrap {
    flex: 1;
    max-width: 480px;
    margin-left: auto;
    position: relative;
  }

  .search-wrap input {
    width: 100%;
    padding: 10px 16px 10px 42px;
    border-radius: 99px;
    border: none;
    background: rgba(255,255,255,0.12);
    color: white;
    font-size: 0.95rem;
    font-family: 'DM Sans', sans-serif;
    outline: none;
    transition: background 0.2s;
  }

  .search-wrap input::placeholder { color: rgba(255,255,255,0.45); }
  .search-wrap input:focus { background: rgba(255,255,255,0.2); }

  .search-wrap svg {
    position: absolute;
    left: 14px;
    top: 50%;
    transform: translateY(-50%);
    opacity: 0.5;
  }

  main {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    padding: 24px;
    max-width: 1400px;
    margin: 0 auto;
  }

  @media (max-width: 900px) {
    main { grid-template-columns: 1fr; }
  }

  .panel {
    background: var(--surface);
    border-radius: 16px;
    border: 1px solid var(--border);
    overflow: hidden;
  }

  .panel-header {
    padding: 14px 20px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #fafafa;
  }

  .panel-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
  }

  .badge {
    background: var(--accent);
    color: white;
    font-size: 0.7rem;
    font-weight: 600;
    border-radius: 99px;
    padding: 2px 10px;
    font-family: 'Space Mono', monospace;
  }

  #results-list {
    max-height: 520px;
    overflow-y: auto;
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .result-card {
    border: 1.5px solid var(--border);
    border-radius: 12px;
    padding: 14px 16px;
    cursor: pointer;
    transition: all 0.18s;
    display: grid;
    grid-template-columns: auto 1fr auto;
    gap: 12px;
    align-items: center;
  }

  .result-card:hover {
    border-color: var(--accent);
    background: #eff6ff;
    transform: translateX(2px);
  }

  .result-card.active {
    border-color: var(--accent);
    background: #eff6ff;
    box-shadow: 0 0 0 3px var(--active-glow);
  }

  .zone-dot {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    font-weight: 700;
    flex-shrink: 0;
  }

  .card-info { min-width: 0; }

  .card-name {
    font-weight: 600;
    font-size: 0.92rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-bottom: 2px;
  }

  .card-meta {
    font-size: 0.75rem;
    color: var(--muted);
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }

  .card-qty {
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--accent);
    white-space: nowrap;
    text-align: right;
  }

  .empty-state {
    text-align: center;
    padding: 48px 20px;
    color: var(--muted);
  }

  .empty-state svg { margin-bottom: 12px; opacity: 0.3; }
  .empty-state p { font-size: 0.9rem; }

  .filters {
    padding: 12px 20px;
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    border-bottom: 1px solid var(--border);
    background: #fafafa;
  }

  .filter-btn {
    padding: 4px 12px;
    border-radius: 99px;
    border: 1.5px solid var(--border);
    background: white;
    font-size: 0.75rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s;
    font-family: 'DM Sans', sans-serif;
  }

  .filter-btn:hover { border-color: var(--accent); color: var(--accent); }
  .filter-btn.active { background: var(--accent); color: white; border-color: var(--accent); }

  .map-container {
    padding: 16px;
    overflow: auto;
  }

  svg.lab-map {
    width: 100%;
    height: auto;
    min-width: 420px;
  }

  .map-zone {
    cursor: pointer;
    transition: all 0.2s;
  }

  .map-zone rect, .map-zone polygon {
    transition: all 0.2s;
  }

  .map-zone:hover rect,
  .map-zone:hover polygon {
    filter: brightness(0.9);
  }

  .map-zone.highlighted rect,
  .map-zone.highlighted polygon {
    stroke: #1d4ed8;
    stroke-width: 3px;
    filter: brightness(0.85) drop-shadow(0 0 6px rgba(37,99,235,0.5));
  }

  #detail-panel {
    padding: 20px;
    display: none;
  }

  #detail-panel.visible { display: block; }

  .detail-location {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: var(--accent);
    color: white;
    border-radius: 10px;
    padding: 6px 16px;
    font-family: 'Space Mono', monospace;
    font-size: 0.9rem;
    font-weight: 700;
    margin-bottom: 14px;
  }

  .detail-name {
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 6px;
  }

  .detail-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-top: 14px;
  }

  .detail-stat {
    background: var(--bg);
    border-radius: 10px;
    padding: 12px;
  }

  .detail-stat-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: var(--muted);
    font-weight: 600;
    margin-bottom: 4px;
  }

  .detail-stat-value {
    font-family: 'Space Mono', monospace;
    font-size: 1rem;
    font-weight: 700;
    color: var(--text);
  }

  .zone-legend {
    padding: 12px 20px;
    border-top: 1px solid var(--border);
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 0.72rem;
    color: var(--muted);
  }

  .legend-dot {
    width: 10px;
    height: 10px;
    border-radius: 3px;
    flex-shrink: 0;
  }

  #results-list::-webkit-scrollbar { width: 6px; }
  #results-list::-webkit-scrollbar-track { background: transparent; }
  #results-list::-webkit-scrollbar-thumb { background: var(--border); border-radius: 99px; }

  .highlight-text {
    background: var(--highlight);
    border-radius: 3px;
    padding: 0 2px;
  }
</style>
</head>
<body>

<header>
  <div class="logo">Lab<span>Finder</span></div>
  <div class="search-wrap">
    <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="white" stroke-width="2.5">
      <circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>
    </svg>
    <input type="text" id="search-input" placeholder="Buscar material, cristalería…" autocomplete="off" autofocus>
  </div>
</header>

<main>
  <div class="panel">
    <div class="panel-header">
      <span class="panel-title">Inventario</span>
      <span class="badge" id="count-badge">0 items</span>
    </div>
    <div class="filters" id="filter-bar">
      <button class="filter-btn active" data-filter="all">Todos</button>
    </div>
    <div id="results-list">
      <div class="empty-state">
        <p>Escribe para buscar en el inventario</p>
      </div>
    </div>
  </div>

  <div class="panel" style="display:flex; flex-direction:column;">
    <div class="panel-header">
      <span class="panel-title">Mapa del Laboratorio</span>
      <span style="font-size:0.72rem; color:var(--muted);">Haz clic en una zona</span>
    </div>

    <div id="detail-panel">
      <div class="detail-location" id="detail-location">—</div>
      <div class="detail-name" id="detail-name">—</div>
      <div style="font-size:0.82rem; color:var(--muted);" id="detail-type">—</div>
      <div class="detail-grid">
        <div class="detail-stat">
          <div class="detail-stat-label">Cantidad</div>
          <div class="detail-stat-value" id="detail-qty">—</div>
        </div>
        <div class="detail-stat">
          <div class="detail-stat-label">Zona</div>
          <div class="detail-stat-value" id="detail-zone">—</div>
        </div>
      </div>
    </div>

    <div class="map-container" style="flex:1;">
      <svg class="lab-map" viewBox="0 0 760 460" xmlns="http://www.w3.org/2000/svg">
        <rect width="760" height="460" fill="#f8f9fa" rx="8"/>
        <g class="map-zone" id="zone-F" onclick="filterByZone('F')">
          <rect x="160" y="12" width="570" height="42" fill="#4ade80" rx="6" opacity="0.85"/>
          <text x="445" y="37" text-anchor="middle" font-family="Space Mono,monospace" font-size="11" font-weight="700" fill="#14532d">ZONA F — F1 a F18</text>
        </g>
        <g class="map-zone" id="zone-A1" onclick="filterByZone('A1')">
          <rect x="20" y="370" width="65" height="28" fill="#fb923c" rx="5" opacity="0.9"/>
          <text x="52" y="388" text-anchor="middle" font-family="Space Mono,monospace" font-size="9" font-weight="700" fill="white">A1-2</text>
        </g>
        <g class="map-zone" id="zone-E" onclick="filterByZone('E')">
          <rect x="270" y="170" width="120" height="220" fill="#93c5fd" rx="8" opacity="0.55"/>
        </g>
        <g class="map-zone" id="zone-L" onclick="filterByZone('L')">
          <rect x="420" y="170" width="120" height="220" fill="#93c5fd" rx="8" opacity="0.55"/>
        </g>
        <g class="map-zone" id="zone-K" onclick="filterByZone('K')">
          <rect x="570" y="170" width="120" height="220" fill="#93c5fd" rx="8" opacity="0.55"/>
        </g>
        <g class="map-zone" id="zone-INV" onclick="filterByZone('INV')">
          <rect x="700" y="90" width="50" height="100" fill="#e5e7eb" rx="6" stroke="#9ca3af" stroke-width="1.5"/>
          <text x="725" y="145" text-anchor="middle" font-family="Space Mono,monospace" font-size="9" font-weight="700" fill="#374151">INV</text>
        </g>
        <g class="map-zone" id="zone-CAP" onclick="filterByZone('CAP')">
          <rect x="700" y="220" width="50" height="140" fill="#d8b4fe" rx="6" stroke="#9333ea" stroke-width="1.5"/>
          <text x="725" y="295" text-anchor="middle" font-family="Space Mono,monospace" font-size="9" font-weight="700" fill="#4c1d95">CAP</text>
        </g>
        <g class="map-zone" id="zone-CONG" onclick="filterByZone('CONG')">
          <rect x="540" y="405" width="105" height="40" fill="#f9a8d4" rx="6" stroke="#db2777" stroke-width="1.5"/>
          <text x="592" y="429" text-anchor="middle" font-family="Space Mono,monospace" font-size="10" font-weight="700" fill="#831843">CONG</text>
        </g>
        <g class="map-zone" id="zone-REFRI" onclick="filterByZone('REFRI')">
          <rect x="655" y="405" width="95" height="40" fill="#f9a8d4" rx="6" stroke="#db2777" stroke-width="1.5"/>
          <text x="702" y="429" text-anchor="middle" font-family="Space Mono,monospace" font-size="10" font-weight="700" fill="#831843">REFRI</text>
        </g>
      </svg>
    </div>
  </div>
</main>

<script>
const INVENTARIO = [
  { ubicacion: "F1", descripcion: "Agar nutritivo", cantidad: 10, tipo: "Reactivo" },
  { ubicacion: "F2", descripcion: "Tryptic Soy Broth (TSB)", cantidad: 5, tipo: "Reactivo" },
  { ubicacion: "A1-2", descripcion: "Vasos de precipitados 50 mL", cantidad: 20, tipo: "Cristalería" },
  { ubicacion: "E1", descripcion: "Ácido clorhídrico HCl 37%", cantidad: 3, tipo: "Reactivo" },
  { ubicacion: "L1", descripcion: "Buretas 50 mL", cantidad: 8, tipo: "Cristalería" },
  { ubicacion: "K1", descripcion: "Tinción Gram set completo", cantidad: 2, tipo: "Reactivo" },
  { ubicacion: "CONG", descripcion: "Muestras biológicas −20°C", cantidad: 15, tipo: "Muestra" },
  { ubicacion: "REFRI", descripcion: "Medios de cultivo preparados", cantidad: 8, tipo: "Reactivo" },
  { ubicacion: "CAP", descripcion: "Gafas de seguridad", cantidad: 8, tipo: "Seguridad" },
  { ubicacion: "INV", descripcion: "Stock tubos centrífuga", cantidad: 60, tipo: "Plástico" }
];

const ZONE_COLORS = {
  F:     { bg: "#dcfce7", color: "#166534", border: "#4ade80" },
  A:     { bg: "#ffedd5", color: "#7c2d12", border: "#fb923c" },
  E:     { bg: "#dbeafe", color: "#1e3a8a", border: "#3b82f6" },
  L:     { bg: "#dbeafe", color: "#1e3a8a", border: "#3b82f6" },
  K:     { bg: "#dbeafe", color: "#1e3a8a", border: "#3b82f6" },
  CONG:  { bg: "#fce7f3", color: "#831843", border: "#db2777" },
  REFRI: { bg: "#fce7f3", color: "#831843", border: "#db2777" },
  CAP:   { bg: "#f3e8ff", color: "#4c1d95", border: "#9333ea" },
  INV:   { bg: "#f3f4f6", color: "#374151", border: "#9ca3af" },
};

function getZoneColor(ubicacion) {
  const u = ubicacion.toUpperCase();
  if (u.startsWith('F')) return ZONE_COLORS.F;
  if (u.startsWith('A')) return ZONE_COLORS.A;
  if (u.startsWith('E')) return ZONE_COLORS.E;
  if (u.startsWith('L')) return ZONE_COLORS.L;
  if (u.startsWith('K')) return ZONE_COLORS.K;
  if (u === 'CONG') return ZONE_COLORS.CONG;
  if (u === 'REFRI') return ZONE_COLORS.REFRI;
  if (u === 'CAP') return ZONE_COLORS.CAP;
  if (u === 'INV') return ZONE_COLORS.INV;
  return { bg: "#f3f4f6", color: "#374151", border: "#9ca3af" };
}

const types = [...new Set(INVENTARIO.map(i => i.tipo))].sort();
const filterBar = document.getElementById('filter-bar');
types.forEach(t => {
  const btn = document.createElement('button');
  btn.className = 'filter-btn';
  btn.dataset.filter = t;
  btn.textContent = t;
  btn.onclick = () => setFilter(t, btn);
  filterBar.appendChild(btn);
});

let activeFilter = 'all';
let activeItem = null;

function setFilter(f, btn) {
  activeFilter = f;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderResults(document.getElementById('search-input').value.trim());
}

document.getElementById('filter-bar').querySelector('[data-filter="all"]').onclick = function() {
  setFilter('all', this);
};

function renderResults(query) {
  const list = document.getElementById('results-list');
  let filtered = INVENTARIO;

  if (activeFilter !== 'all') {
    filtered = filtered.filter(i => i.tipo === activeFilter);
  }

  if (query.length > 0) {
    const q = query.toLowerCase();
    filtered = filtered.filter(i =>
      i.descripcion.toLowerCase().includes(q) ||
      i.ubicacion.toLowerCase().includes(q) ||
      i.tipo.toLowerCase().includes(q)
    );
  }

  document.getElementById('count-badge').textContent = `${filtered.length} items`;

  if (filtered.length === 0) {
    list.innerHTML = `<div class="empty-state"><p>Sin resultados</p></div>`;
    return;
  }

  list.innerHTML = '';
  filtered.forEach(item => {
    const zc = getZoneColor(item.ubicacion);
    const card = document.createElement('div');
    card.className = 'result-card';
    card.innerHTML = `
      <div class="zone-dot" style="background:${zc.bg}; color:${zc.color}; border:1.5px solid ${zc.border}">
        ${item.ubicacion.length <= 3 ? item.ubicacion : item.ubicacion.substring(0,3)}
      </div>
      <div class="card-info">
        <div class="card-name">${item.descripcion}</div>
        <div class="card-meta">
          <span>📍 ${item.ubicacion}</span>
          <span>🏷️ ${item.tipo}</span>
        </div>
      </div>
      <div class="card-qty">${item.cantidad}<br><span style="font-size:0.6rem;color:#6b7280">uds</span></div>
    `;
    card.onclick = () => showDetail(item, card);
    list.appendChild(card);
  });
}

function showDetail(item, cardEl) {
  document.querySelectorAll('.result-card').forEach(c => c.classList.remove('active'));
  cardEl.classList.add('active');
  activeItem = item;

  const panel = document.getElementById('detail-panel');
  panel.classList.add('visible');
  document.getElementById('detail-location').textContent = `📍 ${item.ubicacion}`;
  document.getElementById('detail-name').textContent = item.descripcion;
  document.getElementById('detail-type').textContent = item.tipo;
  document.getElementById('detail-qty').textContent = item.cantidad;
  document.getElementById('detail-zone').textContent = item.ubicacion;
}

function filterByZone(prefix) {
  const input = document.getElementById('search-input');
  input.value = prefix;
  renderResults(prefix);
}

document.getElementById('search-input').addEventListener('input', e => {
  renderResults(e.target.value.trim());
});

renderResults('');
</script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=True)