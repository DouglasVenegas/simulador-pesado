<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LabFinder — Inventario</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #f0f2f5; --surface: #ffffff; --border: #e2e6ea;
    --accent: #2563eb; --text: #111827; --muted: #6b7280;
    --active-glow: rgba(37,99,235,0.25);
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'DM Sans', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }

  header {
    background: var(--text); color: white; padding: 15px 24px;
    display: flex; align-items: center; gap: 14px;
    position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 12px rgba(0,0,0,0.3);
  }
  .logo { font-family: 'Space Mono', monospace; font-size: 1.1rem; font-weight: 700; }
  .logo span { color: #4ade80; }
  .search-wrap { flex: 1; max-width: 460px; margin-left: auto; position: relative; }
  .search-wrap input {
    width: 100%; padding: 9px 16px 9px 40px; border-radius: 99px;
    border: none; background: rgba(255,255,255,0.12); color: white;
    font-size: 0.92rem; font-family: 'DM Sans',sans-serif; outline: none; transition: background .2s;
  }
  .search-wrap input::placeholder { color: rgba(255,255,255,.45); }
  .search-wrap input:focus { background: rgba(255,255,255,.2); }
  .search-wrap svg { position: absolute; left: 13px; top: 50%; transform: translateY(-50%); opacity: .5; }

  main { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; padding: 24px; max-width: 1440px; margin: 0 auto; }
  @media (max-width: 960px) { main { grid-template-columns: 1fr; } }

  .panel { background: var(--surface); border-radius: 16px; border: 1px solid var(--border); overflow: hidden; }
  .panel-header { padding: 13px 20px; border-bottom: 1px solid var(--border); display: flex; align-items: center; justify-content: space-between; background: #fafafa; }
  .panel-title { font-family: 'Space Mono', monospace; font-size: .76rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }
  .badge { background: var(--accent); color: white; font-size: .68rem; font-weight: 600; border-radius: 99px; padding: 2px 10px; font-family: 'Space Mono', monospace; }

  .filters { padding: 10px 18px; display: flex; gap: 7px; flex-wrap: wrap; border-bottom: 1px solid var(--border); background: #fafafa; }
  .filter-btn { padding: 3px 11px; border-radius: 99px; border: 1.5px solid var(--border); background: white; font-size: .73rem; font-weight: 600; cursor: pointer; transition: all .15s; font-family: 'DM Sans',sans-serif; }
  .filter-btn:hover { border-color: var(--accent); color: var(--accent); }
  .filter-btn.active { background: var(--accent); color: white; border-color: var(--accent); }

  #results-list { max-height: 560px; overflow-y: auto; padding: 10px; display: flex; flex-direction: column; gap: 7px; }
  #results-list::-webkit-scrollbar { width: 5px; }
  #results-list::-webkit-scrollbar-thumb { background: var(--border); border-radius: 99px; }

  .result-card {
    border: 1.5px solid var(--border); border-radius: 11px; padding: 11px 13px;
    cursor: pointer; transition: all .17s; display: grid; grid-template-columns: auto 1fr auto; gap: 10px; align-items: center;
  }
  .result-card:hover { border-color: var(--accent); background: #eff6ff; transform: translateX(2px); }
  .result-card.active { border-color: var(--accent); background: #eff6ff; box-shadow: 0 0 0 3px var(--active-glow); }
  .zone-dot { width: 34px; height: 34px; border-radius: 7px; display: flex; align-items: center; justify-content: center; font-family: 'Space Mono', monospace; font-size: .62rem; font-weight: 700; flex-shrink: 0; }
  .card-info { min-width: 0; }
  .card-name { font-weight: 600; font-size: .88rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 2px; }
  .card-meta { font-size: .72rem; color: var(--muted); display: flex; gap: 7px; flex-wrap: wrap; }
  .card-qty { font-family: 'Space Mono', monospace; font-size: .77rem; font-weight: 700; color: var(--accent); white-space: nowrap; text-align: right; }
  .empty-state { text-align: center; padding: 44px 20px; color: var(--muted); font-size: .88rem; }

  .map-panel { display: flex; flex-direction: column; }
  #detail-panel { padding: 14px 18px; border-bottom: 1px solid var(--border); display: none; }
  #detail-panel.visible { display: block; }
  .detail-location { display: inline-flex; align-items: center; gap: 7px; background: var(--accent); color: white; border-radius: 9px; padding: 5px 14px; font-family: 'Space Mono', monospace; font-size: .83rem; font-weight: 700; margin-bottom: 10px; }
  .detail-name { font-size: 1.1rem; font-weight: 700; margin-bottom: 3px; }
  .detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 10px; }
  .detail-stat { background: var(--bg); border-radius: 9px; padding: 10px; }
  .detail-stat-label { font-size: .67rem; text-transform: uppercase; letter-spacing: .07em; color: var(--muted); font-weight: 600; margin-bottom: 3px; }
  .detail-stat-value { font-family: 'Space Mono', monospace; font-size: .93rem; font-weight: 700; }

  .map-container { padding: 12px; flex: 1; overflow: auto; }
  svg.lab-map { width: 100%; height: auto; }

  .map-zone { cursor: pointer; }
  .map-zone rect { transition: filter .18s, stroke .18s; }
  .map-zone:hover rect { filter: brightness(.86); }
  .map-zone.highlighted rect { stroke: #1d4ed8 !important; stroke-width: 2.5 !important; filter: brightness(.82) drop-shadow(0 0 5px rgba(37,99,235,.55)); }
</style>
</head>
<body>

<header>
  <div class="logo">Lab<span>Finder</span></div>
  <div class="search-wrap">
    <svg width="15" height="15" fill="none" viewBox="0 0 24 24" stroke="white" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
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
      <div class="empty-state">Escribe para buscar en el inventario</div>
    </div>
  </div>

  <div class="panel map-panel">
    <div class="panel-header">
      <span class="panel-title">Mapa del Laboratorio</span>
      <span style="font-size:.7rem;color:var(--muted)">Haz clic en una zona</span>
    </div>
    <div id="detail-panel">
      <div class="detail-location" id="detail-location">—</div>
      <div class="detail-name" id="detail-name">—</div>
      <div style="font-size:.8rem;color:var(--muted)" id="detail-type">—</div>
      <div class="detail-grid">
        <div class="detail-stat"><div class="detail-stat-label">Cantidad</div><div class="detail-stat-value" id="detail-qty">—</div></div>
        <div class="detail-stat"><div class="detail-stat-label">Zona</div><div class="detail-stat-value" id="detail-zone">—</div></div>
      </div>
    </div>
    <div class="map-container">
      <svg class="lab-map" viewBox="0 0 860 510" xmlns="http://www.w3.org/2000/svg">
        <!-- Room -->
        <rect x="1" y="1" width="858" height="508" fill="#eef0f4" rx="10" stroke="#bec3cc" stroke-width="2"/>
        <defs>
          <pattern id="g" x="0" y="0" width="24" height="24" patternUnits="userSpaceOnUse">
            <circle cx="12" cy="12" r="1" fill="#b8bec8" opacity=".55"/>
          </pattern>
        </defs>
        <rect x="1" y="1" width="858" height="508" fill="url(#g)" rx="10"/>

        <!-- Left AE/AG open area -->
        <polygon points="10,80 288,80 288,452 10,452 62,412 62,118" fill="#dbeafe" opacity=".5"/>
        <text x="145" y="258" text-anchor="middle" font-family="DM Sans,sans-serif" font-size="26" font-weight="700" fill="#1e3a8a" opacity=".3">AE /</text>
        <text x="145" y="290" text-anchor="middle" font-family="DM Sans,sans-serif" font-size="26" font-weight="700" fill="#1e3a8a" opacity=".3">AG</text>

        <!-- Vertical wall separator -->
        <rect x="290" y="58" width="9" height="410" fill="#c2ad92" rx="2"/>
        <g stroke="#9a8470" stroke-width="1.1">
          <line x1="292" y1="66" x2="299" y2="74"/><line x1="292" y1="88" x2="299" y2="96"/>
          <line x1="292" y1="110" x2="299" y2="118"/><line x1="292" y1="132" x2="299" y2="140"/>
          <line x1="292" y1="154" x2="299" y2="162"/><line x1="292" y1="176" x2="299" y2="184"/>
          <line x1="292" y1="198" x2="299" y2="206"/><line x1="292" y1="220" x2="299" y2="228"/>
          <line x1="292" y1="242" x2="299" y2="250"/><line x1="292" y1="264" x2="299" y2="272"/>
          <line x1="292" y1="286" x2="299" y2="294"/><line x1="292" y1="308" x2="299" y2="316"/>
          <line x1="292" y1="330" x2="299" y2="338"/><line x1="292" y1="352" x2="299" y2="360"/>
          <line x1="292" y1="374" x2="299" y2="382"/><line x1="292" y1="396" x2="299" y2="404"/>
          <line x1="292" y1="418" x2="299" y2="426"/><line x1="292" y1="440" x2="299" y2="448"/>
          <line x1="292" y1="458" x2="299" y2="466"/>
        </g>

        <!-- ===== F ZONES: F1-F18 across top ===== -->
        <!-- 18 zones, each 29px wide, 3px gap, starting x=302 -->
        <g class="map-zone" id="zone-F1"  onclick="filterByZone('F1')"> <rect x="302" y="8" width="29" height="36" fill="#4ade80" rx="4" opacity=".92" stroke="#22c55e" stroke-width="1"/><text x="316" y="30" text-anchor="middle" font-family="Space Mono,monospace" font-size="8" font-weight="700" fill="#14532d">F1</text></g>
        <g class="map-zone" id="zone-F2"  onclick="filterByZone('F2')"> <rect x="334" y="8" width="29" height="36" fill="#4ade80" rx="4" opacity=".92" stroke="#22c55e" stroke-width="1"/><text x="348" y="30" text-anchor="middle" font-family="Space Mono,monospace" font-size="8" font-weight="700" fill="#14532d">F2</text></g>
        <g class="map-zone" id="zone-F3"  onclick="filterByZone('F3')"> <rect x="366" y="8" width="29" height="36" fill="#4ade80" rx="4" opacity=".92" stroke="#22c55e" stroke-width="1"/><text x="380" y="30" text-anchor="middle" font-family="Space Mono,monospace" font-size="8" font-weight="700" fill="#14532d">F3</text></g>
        <g class="map-zone" id="zone-F4"  onclick="filterByZone('F4')"> <rect x="398" y="8" width="29" height="36" fill="#4ade80" rx="4" opacity=".92" stroke="#22c55e" stroke-width="1"/><text x="412" y="30" text-anchor="middle" font-family="Space Mono,monospace" font-size="8" font-weight="700" fill="#14532d">F4</text></g>
        <!-- slight gap -->
        <g class="map-zone" id="zone-F5"  onclick="filterByZone('F5')"> <rect x="432" y="8" width="29" height="36" fill="#4ade80" rx="4" opacity=".92" stroke="#22c55e" stroke-width="1"/><text x="446" y="30" text-anchor="middle" font-family="Space Mono,monospace" font-size="8" font-weight="700" fill="#14532d">F5</text></g>
        <g class="map-zone" id="zone-F6"  onclick="filterByZone('F6')"> <rect x="464" y="8" width="29" height="36" fill="#4ade80" rx="4" opacity=".92" stroke="#22c55e" stroke-width="1"/><text x="478" y="30" text-anchor="middle" font-family="Space Mono,monospace" font-size="8" font-weight="700" fill="#14532d">F6</text></g>
        <g class="map-zone" id="zone-F7"  onclick="filterByZone('F7')"> <rect x="496" y="8" width="29" height="36" fill="#4ade80" rx="4" opacity=".92" stroke="#22c55e" stroke-width="1"/><text x="510" y="30" text-anchor="middle" font-family="Space Mono,monospace" font-size="8" font-weight="700" fill="#14532d">F7</text></g>
        <g class="map-zone" id="zone-F8"  onclick="filterByZone('F8')"> <rect x="528" y="8" width="29" height="36" fill="#4ade80" rx="4" opacity=".92" stroke="#22c55e" stroke-width="1"/><text x="542" y="30" text-anchor="middle" font-family="Space Mono,monospace" font-size="8" font-weight="700" fill="#14532d">F8</text></g>
        <g class="map-zone" id="zone-F9"  onclick="filterByZone('F9')"> <rect x="560" y="8" width="29" height="36" fill="#4ade80" rx="4" opacity=".92" stroke="#22c55e" stroke-width="1.5"/><text x="574" y="30" text-anchor="middle" font-family="Space Mono,monospace" font-size="8" font-weight="700" fill="#14532d">F9</text></g>
        <g class="map-zone" id="zone-F10" onclick="filterByZone('F10')"><rect x="592" y="8" width="34" height="36" fill="#4ade80" rx="4" opacity=".92" stroke="#22c55e" stroke-width="1.5"/><text x="609" y="30" text-anchor="middle" font-family="Space Mono,monospace" font-size="8" font-weight="700" fill="#14532d">F10</text></g>
        <!-- gap then F11-F12 -->
        <g class="map-zone" id="zone-F11" onclick="filterByZone('F11')"><rect x="630" y="8" width="34" height="36" fill="#4ade80" rx="4" opacity=".92" stroke="#22c55e" stroke-width="1"/><text x="647" y="30" text-anchor="middle" font-family="Space Mono,monospace" font-size="8" font-weight="700" fill="#14532d">F11</text></g>
        <g class="map-zone" id="zone-F12" onclick="filterByZone('F12')"><rect x="667" y="8" width="34" height="36" fill="#4ade80" rx="4" opacity=".92" stroke="#22c55e" stroke-width="1"/><text x="684" y="30" text-anchor="middle" font-family="Space Mono,monospace" font-size="8" font-weight="700" fill="#14532d">F12</text></g>
        <!-- gap then F13-F14 -->
        <g class="map-zone" id="zone-F13" onclick="filterByZone('F13')"><rect x="705" y="8" width="34" height="36" fill="#4ade80" rx="4" opacity=".92" stroke="#22c55e" stroke-width="1"/><text x="722" y="30" text-anchor="middle" font-family="Space Mono,monospace" font-size="8" font-weight="700" fill="#14532d">F13</text></g>
        <g class="map-zone" id="zone-F14" onclick="filterByZone('F14')"><rect x="742" y="8" width="34" height="36" fill="#4ade80" rx="4" opacity=".92" stroke="#22c55e" stroke-width="1"/><text x="759" y="30" text-anchor="middle" font-family="Space Mono,monospace" font-size="8" font-weight="700" fill="#14532d">F14</text></g>
        <!-- gap then F15-F16 -->
        <g class="map-zone" id="zone-F15" onclick="filterByZone('F15')"><rect x="780" y="8" width="33" height="36" fill="#4ade80" rx="4" opacity=".92" stroke="#22c55e" stroke-width="1"/><text x="796" y="30" text-anchor="middle" font-family="Space Mono,monospace" font-size="8" font-weight="700" fill="#14532d">F15</text></g>
        <g class="map-zone" id="zone-F16" onclick="filterByZone('F16')"><rect x="816" y="8" width="33" height="36" fill="#4ade80" rx="4" opacity=".92" stroke="#22c55e" stroke-width="1"/><text x="832" y="30" text-anchor="middle" font-family="Space Mono,monospace" font-size="8" font-weight="700" fill="#14532d">F16</text></g>
        <!-- F17-F18 -->
        <g class="map-zone" id="zone-F17" onclick="filterByZone('F17')"><rect x="851" y="8" width="4" height="36" fill="#4ade80" rx="2" opacity=".92" stroke="#22c55e" stroke-width="1"/></g>
        <g class="map-zone" id="zone-F18" onclick="filterByZone('F18')"><rect x="856" y="8" width="3" height="36" fill="#4ade80" rx="2" opacity=".92" stroke="#22c55e" stroke-width="1"/></g>

        <!-- ===== A SHELVES (left curved) ===== -->
        <!-- A9 top horizontal -->
        <g class="map-zone" id="zone-A9" onclick="filterByZone('A9')">
          <rect x="195" y="82" width="82" height="30" fill="#fb923c" rx="5" opacity=".92" stroke="#ea580c" stroke-width="1"/>
          <text x="236" y="101" text-anchor="middle" font-family="Space Mono,monospace" font-size="10" font-weight="700" fill="white">A9</text>
        </g>
        <!-- A7-8 angled upper -->
        <g class="map-zone" id="zone-A7-8" onclick="filterByZone('A7-8')">
          <g transform="rotate(-20 152 130)">
            <rect x="98" y="116" width="108" height="28" fill="#fb923c" rx="5" opacity=".92" stroke="#ea580c" stroke-width="1"/>
            <text x="152" y="134" text-anchor="middle" font-family="Space Mono,monospace" font-size="9.5" font-weight="700" fill="white">A7-8</text>
          </g>
        </g>
        <!-- A5-6 left vertical -->
        <g class="map-zone" id="zone-A5-6" onclick="filterByZone('A5-6')">
          <rect x="10" y="178" width="28" height="92" fill="#fb923c" rx="5" opacity=".92" stroke="#ea580c" stroke-width="1"/>
          <text x="24" y="228" text-anchor="middle" font-family="Space Mono,monospace" font-size="9" font-weight="700" fill="white" transform="rotate(-90 24 228)">A5-6</text>
        </g>
        <!-- A3-4 left vertical -->
        <g class="map-zone" id="zone-A3-4" onclick="filterByZone('A3-4')">
          <rect x="10" y="278" width="28" height="92" fill="#fb923c" rx="5" opacity=".92" stroke="#ea580c" stroke-width="1"/>
          <text x="24" y="328" text-anchor="middle" font-family="Space Mono,monospace" font-size="9" font-weight="700" fill="white" transform="rotate(-90 24 328)">A3-4</text>
        </g>
        <!-- A1-2 angled lower -->
        <g class="map-zone" id="zone-A1-2" onclick="filterByZone('A1-2')">
          <g transform="rotate(20 150 392)">
            <rect x="96" y="378" width="108" height="28" fill="#fb923c" rx="5" opacity=".92" stroke="#ea580c" stroke-width="1"/>
            <text x="150" y="396" text-anchor="middle" font-family="Space Mono,monospace" font-size="9.5" font-weight="700" fill="white">A1-2</text>
          </g>
        </g>

        <!-- Entry door arc -->
        <path d="M 218,454 A 72,72 0 0,0 290,454" fill="none" stroke="#3b82f6" stroke-width="2.2"/>
        <text x="290" y="480" text-anchor="middle" font-family="DM Sans,sans-serif" font-size="10" fill="#6b7280">Entrada</text>

        <!-- ===== BENCH E ===== -->
        <rect x="318" y="134" width="130" height="16" fill="#d1d5db" rx="4" stroke="#9ca3af" stroke-width="1"/>
        <rect x="318" y="150" width="130" height="268" fill="#e2e6eb" stroke="#9ca3af" stroke-width="1"/>
        <line x1="383" y1="150" x2="383" y2="418" stroke="#5b9bd5" stroke-width="2"/>
        <g class="map-zone" id="zone-E2" onclick="filterByZone('E2')">
          <rect x="325" y="162" width="51" height="58" fill="#93c5fd" rx="5" stroke="#3b82f6" stroke-width="1.3"/>
          <text x="350" y="195" text-anchor="middle" font-family="Space Mono,monospace" font-size="12" font-weight="700" fill="#1e3a8a">E2</text>
        </g>
        <g class="map-zone" id="zone-E4" onclick="filterByZone('E4')">
          <rect x="390" y="162" width="51" height="58" fill="#93c5fd" rx="5" stroke="#3b82f6" stroke-width="1.3"/>
          <text x="415" y="195" text-anchor="middle" font-family="Space Mono,monospace" font-size="12" font-weight="700" fill="#1e3a8a">E4</text>
        </g>
        <g class="map-zone" id="zone-E1" onclick="filterByZone('E1')">
          <rect x="325" y="233" width="51" height="58" fill="#93c5fd" rx="5" stroke="#3b82f6" stroke-width="1.3"/>
          <text x="350" y="266" text-anchor="middle" font-family="Space Mono,monospace" font-size="12" font-weight="700" fill="#1e3a8a">E1</text>
        </g>
        <g class="map-zone" id="zone-E3" onclick="filterByZone('E3')">
          <rect x="390" y="233" width="51" height="58" fill="#93c5fd" rx="5" stroke="#3b82f6" stroke-width="1.3"/>
          <text x="415" y="266" text-anchor="middle" font-family="Space Mono,monospace" font-size="12" font-weight="700" fill="#1e3a8a">E3</text>
        </g>
        <rect x="325" y="306" width="51" height="44" fill="#93c5fd" rx="5" stroke="#3b82f6" stroke-width="1" opacity=".55"/>
        <rect x="390" y="306" width="51" height="44" fill="#93c5fd" rx="5" stroke="#3b82f6" stroke-width="1" opacity=".55"/>
        <rect x="318" y="402" width="130" height="16" fill="#d1d5db" rx="4" stroke="#9ca3af" stroke-width="1"/>

        <!-- ===== BENCH L ===== -->
        <rect x="464" y="134" width="130" height="16" fill="#d1d5db" rx="4" stroke="#9ca3af" stroke-width="1"/>
        <rect x="464" y="150" width="130" height="268" fill="#e2e6eb" stroke="#9ca3af" stroke-width="1"/>
        <line x1="529" y1="150" x2="529" y2="418" stroke="#5b9bd5" stroke-width="2"/>
        <g class="map-zone" id="zone-L2" onclick="filterByZone('L2')">
          <rect x="471" y="162" width="51" height="58" fill="#93c5fd" rx="5" stroke="#3b82f6" stroke-width="1.3"/>
          <text x="496" y="195" text-anchor="middle" font-family="Space Mono,monospace" font-size="12" font-weight="700" fill="#1e3a8a">L2</text>
        </g>
        <g class="map-zone" id="zone-L4" onclick="filterByZone('L4')">
          <rect x="536" y="162" width="51" height="58" fill="#93c5fd" rx="5" stroke="#3b82f6" stroke-width="1.3"/>
          <text x="561" y="195" text-anchor="middle" font-family="Space Mono,monospace" font-size="12" font-weight="700" fill="#1e3a8a">L4</text>
        </g>
        <g class="map-zone" id="zone-L1" onclick="filterByZone('L1')">
          <rect x="471" y="233" width="51" height="58" fill="#93c5fd" rx="5" stroke="#3b82f6" stroke-width="1.3"/>
          <text x="496" y="266" text-anchor="middle" font-family="Space Mono,monospace" font-size="12" font-weight="700" fill="#1e3a8a">L1</text>
        </g>
        <g class="map-zone" id="zone-L3" onclick="filterByZone('L3')">
          <rect x="536" y="233" width="51" height="58" fill="#93c5fd" rx="5" stroke="#3b82f6" stroke-width="1.3"/>
          <text x="561" y="266" text-anchor="middle" font-family="Space Mono,monospace" font-size="12" font-weight="700" fill="#1e3a8a">L3</text>
        </g>
        <rect x="471" y="306" width="51" height="44" fill="#93c5fd" rx="5" stroke="#3b82f6" stroke-width="1" opacity=".55"/>
        <rect x="536" y="306" width="51" height="44" fill="#93c5fd" rx="5" stroke="#3b82f6" stroke-width="1" opacity=".55"/>
        <rect x="464" y="402" width="130" height="16" fill="#d1d5db" rx="4" stroke="#9ca3af" stroke-width="1"/>

        <!-- ===== BENCH K ===== -->
        <rect x="610" y="134" width="120" height="16" fill="#d1d5db" rx="4" stroke="#9ca3af" stroke-width="1"/>
        <rect x="610" y="150" width="120" height="268" fill="#e2e6eb" stroke="#9ca3af" stroke-width="1"/>
        <line x1="670" y1="150" x2="670" y2="418" stroke="#5b9bd5" stroke-width="2"/>
        <g class="map-zone" id="zone-K2" onclick="filterByZone('K2')">
          <rect x="617" y="162" width="46" height="58" fill="#93c5fd" rx="5" stroke="#3b82f6" stroke-width="1.3"/>
          <text x="640" y="195" text-anchor="middle" font-family="Space Mono,monospace" font-size="12" font-weight="700" fill="#1e3a8a">K2</text>
        </g>
        <g class="map-zone" id="zone-K4" onclick="filterByZone('K4')">
          <rect x="677" y="162" width="46" height="58" fill="#93c5fd" rx="5" stroke="#3b82f6" stroke-width="1.3"/>
          <text x="700" y="195" text-anchor="middle" font-family="Space Mono,monospace" font-size="12" font-weight="700" fill="#1e3a8a">K4</text>
        </g>
        <g class="map-zone" id="zone-K1" onclick="filterByZone('K1')">
          <rect x="617" y="233" width="46" height="58" fill="#93c5fd" rx="5" stroke="#3b82f6" stroke-width="1.3"/>
          <text x="640" y="266" text-anchor="middle" font-family="Space Mono,monospace" font-size="12" font-weight="700" fill="#1e3a8a">K1</text>
        </g>
        <g class="map-zone" id="zone-K3" onclick="filterByZone('K3')">
          <rect x="677" y="233" width="46" height="58" fill="#93c5fd" rx="5" stroke="#3b82f6" stroke-width="1.3"/>
          <text x="700" y="266" text-anchor="middle" font-family="Space Mono,monospace" font-size="12" font-weight="700" fill="#1e3a8a">K3</text>
        </g>
        <rect x="617" y="306" width="46" height="44" fill="#93c5fd" rx="5" stroke="#3b82f6" stroke-width="1" opacity=".55"/>
        <rect x="677" y="306" width="46" height="44" fill="#93c5fd" rx="5" stroke="#3b82f6" stroke-width="1" opacity=".55"/>
        <rect x="610" y="402" width="120" height="16" fill="#d1d5db" rx="4" stroke="#9ca3af" stroke-width="1"/>

        <!-- ===== RIGHT SIDE: INV (top), INV (mid), CAP ===== -->
        <g class="map-zone" id="zone-INV-top" onclick="filterByZone('INV')">
          <rect x="742" y="56" width="32" height="98" fill="#e5e7eb" rx="6" stroke="#9ca3af" stroke-width="1.5"/>
          <text x="758" y="108" text-anchor="middle" font-family="Space Mono,monospace" font-size="9" font-weight="700" fill="#374151" transform="rotate(90,758,108)">INV</text>
        </g>
        <g class="map-zone" id="zone-INV-bot" onclick="filterByZone('INV')">
          <rect x="742" y="164" width="32" height="98" fill="#e5e7eb" rx="6" stroke="#9ca3af" stroke-width="1.5"/>
          <text x="758" y="216" text-anchor="middle" font-family="Space Mono,monospace" font-size="9" font-weight="700" fill="#374151" transform="rotate(90,758,216)">INV</text>
        </g>
        <g class="map-zone" id="zone-CAP" onclick="filterByZone('CAP')">
          <rect x="742" y="272" width="32" height="148" fill="#d8b4fe" rx="6" stroke="#9333ea" stroke-width="1.5"/>
          <text x="758" y="350" text-anchor="middle" font-family="Space Mono,monospace" font-size="9" font-weight="700" fill="#4c1d95" transform="rotate(90,758,350)">CAP</text>
        </g>

        <!-- ===== CONG + REFRI ===== -->
        <g class="map-zone" id="zone-CONG" onclick="filterByZone('CONG')">
          <rect x="512" y="432" width="118" height="46" fill="#f9a8d4" rx="7" stroke="#db2777" stroke-width="1.5"/>
          <text x="571" y="459" text-anchor="middle" font-family="Space Mono,monospace" font-size="11" font-weight="700" fill="#831843">CONG</text>
        </g>
        <g class="map-zone" id="zone-REFRI" onclick="filterByZone('REFRI')">
          <rect x="638" y="432" width="100" height="46" fill="#f9a8d4" rx="7" stroke="#db2777" stroke-width="1.5"/>
          <text x="688" y="459" text-anchor="middle" font-family="Space Mono,monospace" font-size="11" font-weight="700" fill="#831843">REFRI</text>
        </g>

      </svg>
    </div>
  </div>
</main>

<script>
const INVENTARIO = [
  {ubicacion:"F1",  descripcion:"Agar nutritivo",                cantidad:10, tipo:"Reactivo"},
  {ubicacion:"F2",  descripcion:"Tryptic Soy Broth (TSB)",       cantidad:5,  tipo:"Reactivo"},
  {ubicacion:"F3",  descripcion:"Agar MacConkey",                cantidad:4,  tipo:"Reactivo"},
  {ubicacion:"F4",  descripcion:"Agar sangre",                   cantidad:6,  tipo:"Reactivo"},
  {ubicacion:"F5",  descripcion:"Peptona bacteriológica",         cantidad:3,  tipo:"Reactivo"},
  {ubicacion:"F6",  descripcion:"Extracto de levadura",          cantidad:4,  tipo:"Reactivo"},
  {ubicacion:"F7",  descripcion:"NaCl 0.9%",                     cantidad:12, tipo:"Reactivo"},
  {ubicacion:"F8",  descripcion:"Glucosa D(+) anhidra",          cantidad:7,  tipo:"Reactivo"},
  {ubicacion:"F9",  descripcion:"Fosfato disódico Na₂HPO₄",      cantidad:5,  tipo:"Reactivo"},
  {ubicacion:"F10", descripcion:"Fosfato monopotásico KH₂PO₄",  cantidad:5,  tipo:"Reactivo"},
  {ubicacion:"F11", descripcion:"Hidróxido de sodio NaOH",       cantidad:8,  tipo:"Reactivo"},
  {ubicacion:"F12", descripcion:"Ácido acético glacial",         cantidad:4,  tipo:"Reactivo"},
  {ubicacion:"F13", descripcion:"Sulfato de amonio",             cantidad:6,  tipo:"Reactivo"},
  {ubicacion:"F14", descripcion:"Cloruro de calcio CaCl₂",      cantidad:4,  tipo:"Reactivo"},
  {ubicacion:"F15", descripcion:"EDTA disódico",                 cantidad:3,  tipo:"Reactivo"},
  {ubicacion:"F16", descripcion:"Tween 80",                      cantidad:2,  tipo:"Reactivo"},
  {ubicacion:"F17", descripcion:"Etanol 96°",                    cantidad:10, tipo:"Reactivo"},
  {ubicacion:"F18", descripcion:"Metanol grado HPLC",            cantidad:5,  tipo:"Reactivo"},
  {ubicacion:"A1-2",descripcion:"Vasos de precipitados 50 mL",   cantidad:20, tipo:"Cristalería"},
  {ubicacion:"A3-4",descripcion:"Matraces Erlenmeyer 250 mL",    cantidad:12, tipo:"Cristalería"},
  {ubicacion:"A5-6",descripcion:"Probetas 100 mL",              cantidad:8,  tipo:"Cristalería"},
  {ubicacion:"A7-8",descripcion:"Pipetas graduadas 10 mL",       cantidad:15, tipo:"Cristalería"},
  {ubicacion:"A9",  descripcion:"Embudos de separación 250 mL",  cantidad:6,  tipo:"Cristalería"},
  {ubicacion:"E1",  descripcion:"Ácido clorhídrico HCl 37%",     cantidad:3,  tipo:"Reactivo"},
  {ubicacion:"E2",  descripcion:"Ácido sulfúrico H₂SO₄ 98%",    cantidad:2,  tipo:"Reactivo"},
  {ubicacion:"E3",  descripcion:"Ácido nítrico HNO₃ 65%",       cantidad:2,  tipo:"Reactivo"},
  {ubicacion:"E4",  descripcion:"Amoníaco NH₃ 25%",             cantidad:3,  tipo:"Reactivo"},
  {ubicacion:"L1",  descripcion:"Buretas 50 mL",                cantidad:8,  tipo:"Cristalería"},
  {ubicacion:"L2",  descripcion:"Pipetas volumétricas 25 mL",    cantidad:10, tipo:"Cristalería"},
  {ubicacion:"L3",  descripcion:"Tubos de ensayo 16×150 mm",     cantidad:50, tipo:"Cristalería"},
  {ubicacion:"L4",  descripcion:"Frascos Schott 500 mL",        cantidad:14, tipo:"Cristalería"},
  {ubicacion:"K1",  descripcion:"Tinción Gram set completo",     cantidad:2,  tipo:"Reactivo"},
  {ubicacion:"K2",  descripcion:"Reactivo de Kovac's",          cantidad:3,  tipo:"Reactivo"},
  {ubicacion:"K3",  descripcion:"Azul de metileno",             cantidad:5,  tipo:"Reactivo"},
  {ubicacion:"K4",  descripcion:"Crystal Violet solución",       cantidad:4,  tipo:"Reactivo"},
  {ubicacion:"CONG",descripcion:"Muestras biológicas −20°C",     cantidad:15, tipo:"Muestra"},
  {ubicacion:"REFRI",descripcion:"Medios de cultivo preparados", cantidad:8,  tipo:"Reactivo"},
  {ubicacion:"CAP", descripcion:"Gafas de seguridad",            cantidad:8,  tipo:"Seguridad"},
  {ubicacion:"CAP", descripcion:"Guantes nitrilo talla M",       cantidad:100,tipo:"Seguridad"},
  {ubicacion:"CAP", descripcion:"Batas laboratorio talla L",     cantidad:12, tipo:"Seguridad"},
  {ubicacion:"INV", descripcion:"Stock tubos centrífuga 1.5 mL",cantidad:60, tipo:"Plástico"},
  {ubicacion:"INV", descripcion:"Puntas micropipeta 200 µL",    cantidad:500,tipo:"Plástico"},
  {ubicacion:"INV", descripcion:"Placas Petri desechables",     cantidad:80, tipo:"Plástico"},
];

const ZC = {
  F:    {bg:"#dcfce7",color:"#166534",border:"#4ade80"},
  A:    {bg:"#ffedd5",color:"#7c2d12",border:"#fb923c"},
  E:    {bg:"#dbeafe",color:"#1e3a8a",border:"#3b82f6"},
  L:    {bg:"#dbeafe",color:"#1e3a8a",border:"#3b82f6"},
  K:    {bg:"#dbeafe",color:"#1e3a8a",border:"#3b82f6"},
  CONG: {bg:"#fce7f3",color:"#831843",border:"#db2777"},
  REFRI:{bg:"#fce7f3",color:"#831843",border:"#db2777"},
  CAP:  {bg:"#f3e8ff",color:"#4c1d95",border:"#9333ea"},
  INV:  {bg:"#f3f4f6",color:"#374151",border:"#9ca3af"},
};
function gc(u) {
  const p = u.toUpperCase();
  if(p.startsWith('F')) return ZC.F;
  if(p.startsWith('A')) return ZC.A;
  if(p.startsWith('E')) return ZC.E;
  if(p.startsWith('L')) return ZC.L;
  if(p.startsWith('K')) return ZC.K;
  return ZC[p] || {bg:"#f3f4f6",color:"#374151",border:"#9ca3af"};
}

const types = [...new Set(INVENTARIO.map(i=>i.tipo))].sort();
const fb = document.getElementById('filter-bar');
types.forEach(t => {
  const b = document.createElement('button');
  b.className='filter-btn'; b.dataset.filter=t; b.textContent=t;
  b.onclick=()=>setFilter(t,b); fb.appendChild(b);
});

let activeFilter = 'all';
fb.querySelector('[data-filter="all"]').onclick = function(){ setFilter('all',this); };

function setFilter(f,btn) {
  activeFilter=f;
  document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  renderResults(document.getElementById('search-input').value.trim());
}

function renderResults(q) {
  const list = document.getElementById('results-list');
  let f = INVENTARIO;
  if(activeFilter !== 'all') f = f.filter(i=>i.tipo===activeFilter);
  if(q){ const ql=q.toLowerCase(); f=f.filter(i=>i.descripcion.toLowerCase().includes(ql)||i.ubicacion.toLowerCase().includes(ql)||i.tipo.toLowerCase().includes(ql)); }
  document.getElementById('count-badge').textContent = `${f.length} items`;
  if(!f.length){ list.innerHTML=`<div class="empty-state">Sin resultados</div>`; return; }
  list.innerHTML='';
  f.forEach(item => {
    const zc=gc(item.ubicacion);
    const c=document.createElement('div'); c.className='result-card';
    const s=item.ubicacion.length<=4?item.ubicacion:item.ubicacion.slice(0,4);
    c.innerHTML=`<div class="zone-dot" style="background:${zc.bg};color:${zc.color};border:1.5px solid ${zc.border}">${s}</div><div class="card-info"><div class="card-name">${item.descripcion}</div><div class="card-meta"><span>📍 ${item.ubicacion}</span><span>🏷️ ${item.tipo}</span></div></div><div class="card-qty">${item.cantidad}<br><span style="font-size:.6rem;color:#6b7280">uds</span></div>`;
    c.onclick=()=>showDetail(item,c); list.appendChild(c);
  });
}

function showDetail(item,cardEl) {
  document.querySelectorAll('.result-card').forEach(c=>c.classList.remove('active'));
  cardEl.classList.add('active');
  const dp=document.getElementById('detail-panel'); dp.classList.add('visible');
  document.getElementById('detail-location').textContent=`📍 ${item.ubicacion}`;
  document.getElementById('detail-name').textContent=item.descripcion;
  document.getElementById('detail-type').textContent=item.tipo;
  document.getElementById('detail-qty').textContent=item.cantidad;
  document.getElementById('detail-zone').textContent=item.ubicacion;
  highlightZone(item.ubicacion);
}

function highlightZone(ub) {
  document.querySelectorAll('.map-zone').forEach(z=>z.classList.remove('highlighted'));
  const u=ub.toUpperCase();
  if(u==='INV'){
    document.getElementById('zone-INV-top')?.classList.add('highlighted');
    document.getElementById('zone-INV-bot')?.classList.add('highlighted');
    return;
  }
  document.getElementById(`zone-${ub}`)?.classList.add('highlighted');
}

function filterByZone(prefix) {
  const input=document.getElementById('search-input');
  input.value=prefix;
  renderResults(prefix);
  document.querySelectorAll('.map-zone').forEach(z=>z.classList.remove('highlighted'));
  if(prefix==='INV'){
    document.getElementById('zone-INV-top')?.classList.add('highlighted');
    document.getElementById('zone-INV-bot')?.classList.add('highlighted');
  } else {
    document.querySelectorAll(`[id^="zone-${prefix}"]`).forEach(el=>el.classList.add('highlighted'));
  }
}

document.getElementById('search-input').addEventListener('input', e=>renderResults(e.target.value.trim()));
renderResults('');
</script>
</body>
</html>
