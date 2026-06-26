#!/usr/bin/env python3
"""
generate-assets.py — Gera 4 assets visuais pra LP ConsultorIA.

1. cockpit-mestre.png  → via HTML+Playwright (Chrome headless) → texto perfeito
2. lapide-afiliado.png → via fal.ai (Ideogram V3) → texto on-image legível
3. lapide-drop.png     → via fal.ai (Ideogram V3)
4. lapide-info.png     → via fal.ai (Ideogram V3)

Brand: ALEX_SSCIA / ConsultorIA
- primary: #D97757 (verde)
- bg: #0a0a0a
- fonts: Poppins (display) + Inter (body) + JetBrains Mono (code)

Como rodar:
    cd "$PROJECTS_ROOT/ALEX_SSCIA/Funis de Vendas/Funil ConsultorIA"
    python3 scripts/generate-assets.py

Pré-reqs:
- ~/.claude/.env com FAL_KEY
- pip install playwright fal-client python-dotenv requests
- playwright install chromium  (1x setup)
"""
from __future__ import annotations

import asyncio
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

# === Setup ===
ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / "public" / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

load_dotenv(Path.home() / ".claude" / ".env")

if not os.getenv("FAL_KEY"):
    print("[X] FAL_KEY não encontrada em ~/.claude/.env")
    sys.exit(1)

# === ASSET 1 — Cockpit MESTRE via HTML/Playwright ===

COCKPIT_HTML = r"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Inter:wght@400;500;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

  * { box-sizing: border-box; margin: 0; padding: 0; }

  html, body {
    width: 1600px; height: 900px;
    font-family: 'Inter', sans-serif;
    background: #0a0a0a;
    color: #ffffff;
    overflow: hidden;
  }

  body {
    background:
      radial-gradient(ellipse at top right, rgba(143, 223, 101, 0.08), transparent 50%),
      radial-gradient(ellipse at bottom left, rgba(143, 223, 101, 0.04), transparent 60%),
      linear-gradient(180deg, #0a0a0a 0%, #050505 100%);
    padding: 32px 40px;
    position: relative;
  }

  /* Subtle grid overlay */
  body::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
      linear-gradient(rgba(143, 223, 101, 0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(143, 223, 101, 0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
  }

  .layout { position: relative; z-index: 1; display: grid; grid-template-rows: auto auto 1fr; gap: 18px; height: 100%; }

  /* HEADER */
  .header { display: flex; justify-content: space-between; align-items: flex-start; }

  .brand-block { display: flex; align-items: center; gap: 18px; }

  .crown {
    width: 56px; height: 56px;
    background: linear-gradient(135deg, #D97757, #C25E3F);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 32px;
    box-shadow: 0 0 32px rgba(143, 223, 101, 0.35);
  }

  .title-block h1 {
    font-family: 'Poppins', sans-serif;
    font-weight: 700;
    font-size: 32px;
    letter-spacing: -0.5px;
    line-height: 1.1;
  }
  .title-block h1 .accent { color: #D97757; }
  .title-block .tagline {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: #A3A3A3;
    margin-top: 6px;
    letter-spacing: 0.5px;
  }

  .live-badge {
    display: flex; align-items: center; gap: 10px;
    background: rgba(143, 223, 101, 0.08);
    border: 1px solid rgba(143, 223, 101, 0.35);
    padding: 10px 18px;
    border-radius: 100px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    font-weight: 700;
    color: #D97757;
    letter-spacing: 1px;
  }
  .live-dot {
    width: 9px; height: 9px;
    background: #D97757;
    border-radius: 50%;
    box-shadow: 0 0 12px #D97757;
  }

  /* KPIs */
  .kpis { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
  .kpi {
    background: linear-gradient(135deg, rgba(143, 223, 101, 0.06), rgba(143, 223, 101, 0.02));
    border: 1px solid rgba(143, 223, 101, 0.18);
    border-radius: 14px;
    padding: 18px 22px;
    position: relative;
    overflow: hidden;
  }
  .kpi::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: #D97757;
  }
  .kpi .label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: #D97757;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 6px;
  }
  .kpi .value {
    font-family: 'Poppins', sans-serif;
    font-weight: 700;
    font-size: 38px;
    line-height: 1;
    letter-spacing: -1px;
  }
  .kpi .value .unit {
    font-size: 13px;
    color: #A3A3A3;
    font-weight: 400;
    margin-left: 6px;
  }

  /* MAIN GRID */
  .main { display: grid; grid-template-columns: 1.15fr 1fr; gap: 16px; min-height: 0; }

  .panel {
    background: rgba(17, 17, 17, 0.6);
    border: 1px solid #222222;
    border-radius: 14px;
    padding: 16px 18px;
    display: flex;
    flex-direction: column;
    min-height: 0;
  }
  .panel-header {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 12px;
    padding-bottom: 10px;
    border-bottom: 1px solid #222222;
  }
  .panel-header h2 {
    font-family: 'Poppins', sans-serif;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 0.5px;
  }
  .panel-header .meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: #D97757;
    letter-spacing: 1px;
  }

  /* SQUADS META */
  .meta-squads { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
  .meta-card {
    background: #0d0d0d;
    border: 1px solid #1f1f1f;
    border-radius: 10px;
    padding: 12px 14px;
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .meta-card .icon {
    width: 36px; height: 36px;
    background: rgba(143, 223, 101, 0.1);
    border: 1px solid rgba(143, 223, 101, 0.3);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
  }
  .meta-card .title {
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    font-size: 12px;
    color: #ffffff;
  }
  .meta-card .role {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: #A3A3A3;
    margin-top: 2px;
    letter-spacing: 0.5px;
  }

  /* CLIENTS */
  .clients-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
  .client-card {
    background: #0d0d0d;
    border: 1px solid #1f1f1f;
    border-radius: 8px;
    padding: 10px 12px;
    position: relative;
  }
  .client-card.flagship { border-color: rgba(143, 223, 101, 0.45); background: rgba(143, 223, 101, 0.05); }
  .client-name {
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    font-size: 11px;
    color: #ffffff;
    line-height: 1.2;
  }
  .client-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8px;
    color: #D97757;
    letter-spacing: 1px;
    margin-top: 4px;
    text-transform: uppercase;
  }
  .client-card.flagship .client-badge { color: #D97757; }
  .client-card.adoption .client-badge { color: #ffa336; }

  /* OPS SQUADS */
  .ops-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; }
  .ops-card {
    background: #0d0d0d;
    border: 1px solid #1f1f1f;
    border-radius: 8px;
    padding: 10px 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .ops-card .ops-name {
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    font-size: 11px;
  }
  .ops-card .ops-agents {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: #D97757;
    background: rgba(143, 223, 101, 0.08);
    padding: 3px 8px;
    border-radius: 100px;
    border: 1px solid rgba(143, 223, 101, 0.2);
  }
  .ops-card .ops-icon { font-size: 13px; margin-right: 6px; }

  /* FOOTER STATUS BAR */
  .status-bar {
    position: absolute;
    bottom: 18px; left: 40px; right: 40px;
    display: flex; justify-content: space-between; align-items: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: #555555;
    letter-spacing: 1px;
    padding-top: 10px;
    border-top: 1px solid #1a1a1a;
    z-index: 2;
  }
  .status-bar .left { display: flex; gap: 18px; }
  .status-bar .right { color: #D97757; }
</style>
</head>
<body>
  <div class="layout">
    <!-- HEADER -->
    <header class="header">
      <div class="brand-block">
        <div class="crown">👑</div>
        <div class="title-block">
          <h1>ConsultorIA <span class="accent">— Hub MESTRE</span></h1>
          <div class="tagline">// META-ORQUESTRADOR DA AGÊNCIA · ACIMA DOS NEXUS DE CADA CLIENTE</div>
        </div>
      </div>
      <div class="live-badge">
        <span class="live-dot"></span>
        <span>● LIVE</span>
      </div>
    </header>

    <!-- KPIs -->
    <section class="kpis">
      <div class="kpi"><div class="label">CLIENTES</div><div class="value">10<span class="unit">ativos</span></div></div>
      <div class="kpi"><div class="label">AGENTES</div><div class="value">598<span class="unit">orquestrados</span></div></div>
      <div class="kpi"><div class="label">SQUADS</div><div class="value">7<span class="unit">operacionais</span></div></div>
      <div class="kpi"><div class="label">UPTIME</div><div class="value">99.8<span class="unit">%</span></div></div>
    </section>

    <!-- MAIN -->
    <section class="main">
      <!-- LEFT: Squads META -->
      <div class="panel">
        <div class="panel-header">
          <h2>SQUADS META · execução cross-cliente</h2>
          <span class="meta">04 / 04 ATIVOS</span>
        </div>
        <div class="meta-squads">
          <div class="meta-card">
            <div class="icon">🚀</div>
            <div><div class="title">Onboarding</div><div class="role">// PROVISIONA NOVO CLIENTE</div></div>
          </div>
          <div class="meta-card">
            <div class="icon">🩺</div>
            <div><div class="title">Doctor</div><div class="role">// DIAGNÓSTICO + CURA</div></div>
          </div>
          <div class="meta-card">
            <div class="icon">📡</div>
            <div><div class="title">Propagate</div><div class="role">// SYNC SKILLS CROSS-CLIENTE</div></div>
          </div>
          <div class="meta-card">
            <div class="icon">🔀</div>
            <div><div class="title">Switchboard</div><div class="role">// ROTEAMENTO ENTRE NEXUS</div></div>
          </div>
        </div>

        <div class="panel-header" style="margin-top:18px;">
          <h2>CLIENTES · operação ativa</h2>
          <span class="meta">10 / 10 ONLINE</span>
        </div>
        <div class="clients-grid">
          <div class="client-card flagship">
            <div class="client-name">Alex Priete</div>
            <div class="client-badge">◆ FLAGSHIP</div>
          </div>
          <div class="client-card">
            <div class="client-name">Allan Priete</div>
            <div class="client-badge">ATIVO</div>
          </div>
          <div class="client-card">
            <div class="client-name">Ballarin</div>
            <div class="client-badge">ATIVO</div>
          </div>
          <div class="client-card adoption">
            <div class="client-name">Floor to Ceiling</div>
            <div class="client-badge">ADOPTION</div>
          </div>
          <div class="client-card">
            <div class="client-name">Mendes Wood Floor</div>
            <div class="client-badge">ATIVO</div>
          </div>
          <div class="client-card">
            <div class="client-name">OdontoConnect</div>
            <div class="client-badge">ATIVO</div>
          </div>
        </div>
      </div>

      <!-- RIGHT: Squads operacionais -->
      <div class="panel">
        <div class="panel-header">
          <h2>SQUADS OPERACIONAIS · execução por cliente</h2>
          <span class="meta">07 / 07 ATIVOS</span>
        </div>
        <div class="ops-grid">
          <div class="ops-card"><span><span class="ops-icon">🧠</span><span class="ops-name">NEXUS</span></span><span class="ops-agents">142 agts</span></div>
          <div class="ops-card"><span><span class="ops-icon">🎨</span><span class="ops-name">Branding</span></span><span class="ops-agents">86 agts</span></div>
          <div class="ops-card"><span><span class="ops-icon">🔥</span><span class="ops-name">Conteúdo Viral</span></span><span class="ops-agents">94 agts</span></div>
          <div class="ops-card"><span><span class="ops-icon">📝</span><span class="ops-name">Meta Ads Copy</span></span><span class="ops-agents">71 agts</span></div>
          <div class="ops-card"><span><span class="ops-icon">⚙️</span><span class="ops-name">Infraestrutura</span></span><span class="ops-agents">68 agts</span></div>
          <div class="ops-card"><span><span class="ops-icon">🌐</span><span class="ops-name">Landing Pages</span></span><span class="ops-agents">79 agts</span></div>
          <div class="ops-card" style="grid-column: span 2;"><span><span class="ops-icon">🎯</span><span class="ops-name">Tráfego Pago</span></span><span class="ops-agents">58 agts</span></div>
        </div>

        <div class="panel-header" style="margin-top:18px;">
          <h2>EXECUTION LOG · live</h2>
          <span class="meta">STREAMING</span>
        </div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #A3A3A3; line-height: 1.7; letter-spacing: 0.2px;">
          <div><span style="color:#D97757;">[14:32]</span> nexus.allan-priete  → carrossel C47 publicado IG ✓</div>
          <div><span style="color:#D97757;">[14:30]</span> branding.ballarin   → 3 variantes geradas ✓</div>
          <div><span style="color:#D97757;">[14:27]</span> ads.floor-to-ceiling→ campanha pausada (CPL OK)</div>
          <div><span style="color:#D97757;">[14:25]</span> conteudo.mendes     → reel 14h agendado ✓</div>
          <div><span style="color:#ffa336;">[14:21]</span> doctor.odontoconnect→ alert: token CRM Funnels renovar</div>
          <div><span style="color:#D97757;">[14:18]</span> propagate           → skill sync FTC→JRS ✓</div>
        </div>
      </div>
    </section>
  </div>

  <div class="status-bar">
    <div class="left">
      <span>// CRM_FUNNELS_INFRA</span>
      <span>v2.1.0</span>
      <span>ROUTING: ENABLED</span>
    </div>
    <div class="right">➜ ALL_SYSTEMS_GO</div>
  </div>
</body>
</html>
"""


def render_cockpit():
    """Renderiza o HTML do cockpit via Playwright (Chrome headless) → PNG."""
    out = ASSETS_DIR / "cockpit-mestre.png"
    print(f"\n[1/4] Rendering cockpit-mestre.png via Playwright...")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("    [X] playwright não instalado. Rode: pip install playwright && playwright install chromium")
        return None

    # Salva HTML temporário pra debug se precisar
    tmp_html = ASSETS_DIR / "_cockpit-mestre.html"
    tmp_html.write_text(COCKPIT_HTML, encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1600, "height": 900}, device_scale_factor=1)
        page = context.new_page()
        page.goto(f"file://{tmp_html}")
        # Aguarda fontes do Google
        page.wait_for_load_state("networkidle")
        time.sleep(1.5)  # extra pra fonts renderizarem
        page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": 1600, "height": 900})
        browser.close()

    print(f"    [OK] {out}  (1600x900)")
    return out


# === ASSET 2-4 — Lápides via fal.ai Ideogram V3 ===

LAPIDES = [
    {
        "filename": "lapide-afiliado.png",
        "title": "AFILIADO",
        "epitaph": "R.I.P. Margem fina, sem ativo",
        "symbol_hint": "with a faint percent sign '%' carved subtly into the tombstone, as if eroded",
    },
    {
        "filename": "lapide-drop.png",
        "title": "DROPSHIPPING",
        "epitaph": "R.I.P. Logística que você não controla",
        "symbol_hint": "with a tiny overturned cardboard delivery box at the base of the tombstone, sad and broken",
    },
    {
        "filename": "lapide-info.png",
        "title": "INFOPRODUTO",
        "epitaph": "R.I.P. Audiência que não cresce",
        "symbol_hint": "with a cracked computer screen icon carved subtly into the tombstone center, as if shattered",
    },
]


def build_lapide_prompt(title: str, epitaph: str, symbol_hint: str) -> str:
    return (
        f"A single gray tombstone graveyard headstone, flat 2D minimalist illustration, "
        f"centered composition on a pure transparent background. "
        f"The tombstone has a rounded arch top and a cross-like silhouette engraved at the very top. "
        f"Large bold engraved text on the upper portion of the stone reads exactly: \"{title}\". "
        f"Below the title, smaller engraved text in two lines reads exactly: \"{epitaph}\". "
        f"{symbol_hint}. "
        f"Color palette: medium cool gray stone (#7a7a7a) with subtle highlight (#a3a3a3) and dark shadow (#3a3a3a). "
        f"Text color: off-white engraved letters with subtle inner shadow giving depth, very legible Poppins-like bold sans-serif typography. "
        f"Subtle grain and weathered concrete texture. "
        f"Tiny dry grass tufts and a small mound of dirt at the base. "
        f"Style: editorial flat illustration, sharp edges, no painterly brushstrokes, high contrast, suitable for dark UI background. "
        f"No colorful elements except very muted gray tones. "
        f"NEGATIVE: no cartoon goofy face, no rainbow colors, no creepy horror gore, no spider webs, no skulls, "
        f"no bright background, no white background, no realistic photography, no people, no extra text beyond what is specified."
    )


def generate_lapide(idx: int, total: int, spec: dict) -> Path | None:
    """Gera 1 lápide via Ideogram V3 (texto on-image)."""
    import fal_client

    out = ASSETS_DIR / spec["filename"]
    print(f"\n[{idx + 1}/{total}] Gerando {spec['filename']} via Ideogram V3...")

    prompt = build_lapide_prompt(spec["title"], spec["epitaph"], spec["symbol_hint"])

    start = time.time()
    try:
        response = fal_client.subscribe(
            "fal-ai/ideogram/v3",
            arguments={
                "prompt": prompt,
                "aspect_ratio": "3:4",
                "rendering_speed": "QUALITY",
                "style": "DESIGN",
                "expand_prompt": False,
                "num_images": 1,
            },
            with_logs=False,
        )
        elapsed = round(time.time() - start, 1)
        images = response.get("images") or []
        if not images:
            print(f"    [X] resposta sem imagens: {response}")
            return None
        url = images[0]["url"]
        # baixa
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        out.write_bytes(r.content)
        print(f"    [OK] {out}  (~600x800, {elapsed}s, ~$0.08)")
        return out
    except Exception as exc:
        print(f"    [X] erro: {type(exc).__name__}: {exc}")
        return None


# === Main ===

def main():
    print("=" * 60)
    print("ConsultorIA LP — Asset Generator")
    print("=" * 60)
    print(f"Output: {ASSETS_DIR}")

    results = {}

    # 1. Cockpit
    results["cockpit-mestre.png"] = render_cockpit()

    # 2-4. Lápides em sequência (não parallel — Ideogram é rápido)
    for idx, spec in enumerate(LAPIDES):
        results[spec["filename"]] = generate_lapide(idx + 1, len(LAPIDES) + 1, spec)

    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO")
    print("=" * 60)
    for name, path in results.items():
        if path and path.exists():
            size_kb = path.stat().st_size // 1024
            print(f"  ✓ {path}  ({size_kb} KB)")
        else:
            print(f"  ✗ {name}  — FALHOU")

    fails = [k for k, v in results.items() if v is None]
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
