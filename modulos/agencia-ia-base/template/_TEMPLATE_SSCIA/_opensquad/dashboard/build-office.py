#!/usr/bin/env python3
"""
build-office.py — Cockpit de lançamento imobiliário (2 níveis).

Categoria PADRÃO: lancamento-imobiliario.

Gera office.html como uma ferramenta de decisão:
  Nível 1 (landing) — lista TODOS os clientes da categoria lancamento-imobiliario.
                      Auto-discovery varre PROJETOS_CLAUDE_CODE/ procurando quem tem
                      readout-imobiliario.json (categoria == lancamento-imobiliario).
  Nível 2 (cliente) — visão híbrida: KPIs, alertas, 3 tabelas (timeline, campanhas,
                      ranking) + escritório virtual dos agentes ao final.

Roda assim:

    python3 build-office.py

Ou (de qualquer pasta):

    python3 ~/.../INVESTBENS_RESIDENCIAL_SERRARIA/_opensquad/dashboard/build-office.py

Quando você atualiza squad-party.csv, agents/ ou os readout-imobiliario.json
dos clientes, é só rodar de novo.

Fonte de dados de performance: _opensquad/_memory/analises/readout-imobiliario.json
de CADA cliente (contrato canônico — não inventar campos).
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

# Resolve paths relativos ao próprio script
HERE = Path(__file__).parent.resolve()            # .../_opensquad/dashboard/
CLIENT_DIR = HERE.parent.parent                    # .../INVESTBENS_RESIDENCIAL_SERRARIA/
PROJECTS_ROOT = CLIENT_DIR.parent                  # .../PROJETOS_CLAUDE_CODE/
SQUADS_DIR = CLIENT_DIR / "squads"
TEMPLATE = HERE / "office.html"
DATA_MARKER_START = "// ============= AGENT DATA ============="
DATA_MARKER_END = "// ============= CHARACTER RENDER ============="

CATEGORIA = "lancamento-imobiliario"
READOUT_REL = Path("_opensquad") / "_memory" / "analises" / "readout-imobiliario.json"
BRAND_REL = Path("_opensquad") / "_memory" / "brand-profile.json"


# Heurísticas visuais do escritório
SHIRT_BY_ROLE = {
    "chief": "yellow", "orquestrador": "yellow", "router": "blue",
    "bridge": "teal", "auditor": "purple", "chronicler": "gray",
}
SHIRT_BY_TIER = {"chief": "yellow", "1a": "red", "1b": "blue"}
SHIRT_FALLBACK = ["orange", "blue", "green", "purple", "red", "teal", "gray"]
LOOK_CYCLE = [1, 2, 3, 4, 5, 6]

SQUAD_META = {
    "nexus":            ("🧭", "NEXUS"),
    "branding":         ("🏛️", "CORE"),
    "conteudo-viral":   ("🎬", "VECTOR"),
    "infraestrutura":   ("⚙️", "INFRA"),
    "meta-ads-copy":    ("📣", "COPY-CHIEF"),
    "landing-pages-seo":("🔍", "GATE"),
    "trafego-pago":     ("📊", "FLUX"),
}

ACTIVE_TASKS = {
    "nexus":            "Orquestrando squads · consolidando relatórios cross-squad",
    "branding":         "Validando consistência visual e tom de voz",
    "conteudo-viral":   "Próxima leva de carrosséis em produção",
    "infraestrutura":   "Pesquisa CRM Funnels Ads API + automações n8n",
    "meta-ads-copy":    "Lendários do copywriting prontos · COPY-CHIEF roteia por situação",
    "landing-pages-seo":"Aguardando primeiro briefing de LP",
    "trafego-pago":     "Monitorando campanhas Meta Ads · otimização diária",
}


# ────────────────────────────────────────────────────────────────────
# CSV / squads
# ────────────────────────────────────────────────────────────────────
def parse_csv(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    rows = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            clean = {}
            for k, v in r.items():
                if v is None:
                    clean[k] = ""
                elif isinstance(v, list):
                    clean[k] = ", ".join(str(x) for x in v if x).strip()
                else:
                    clean[k] = str(v).strip()
            rows.append(clean)
    return rows


def shirt_for(agent: dict, idx: int) -> str:
    tier = (agent.get("tier") or "").lower()
    if tier in SHIRT_BY_TIER:
        return SHIRT_BY_TIER[tier]
    role = (agent.get("id") or "").lower()
    for k, v in SHIRT_BY_ROLE.items():
        if k in role:
            return v
    return SHIRT_FALLBACK[idx % len(SHIRT_FALLBACK)]


def look_for(idx: int) -> int:
    return LOOK_CYCLE[idx % len(LOOK_CYCLE)]


def glasses_for(agent: dict, idx: int) -> bool:
    return idx % 3 != 0


def to_agent_obj(row: dict, idx: int) -> dict:
    code = row.get("codename") or row.get("id", "AGENT").upper()
    name = row.get("name", "")
    role = row.get("role", "")[:60]
    inspired = row.get("inspired_by") or row.get("expertise", "")
    inspired = (inspired[:42] + "…") if len(inspired) > 42 else inspired
    expertise = row.get("expertise", "")[:80]
    return {
        "code": code,
        "name": name,
        "role": role or "Especialista",
        "inspired": inspired,
        "look": look_for(idx),
        "shirt": shirt_for(row, idx),
        "glasses": glasses_for(row, idx),
        "working": idx == 0,
        "tip": expertise or role,
    }


def build_squad(squads_dir: Path, squad_id: str) -> dict | None:
    party = squads_dir / squad_id / "squad-party.csv"
    if not party.is_file():
        return None
    rows = parse_csv(party)
    if not rows:
        return None
    emoji, codename = SQUAD_META.get(squad_id, ("📦", squad_id.upper()))
    agents = [to_agent_obj(r, i) for i, r in enumerate(rows)]
    overflow = 0
    if squad_id == "meta-ads-copy" and len(agents) > 6:
        overflow = len(agents) - 6
        agents = agents[:6]
    return {
        "id": squad_id,
        "emoji": emoji,
        "name": squad_id.replace("-", " ").title(),
        "codename": codename,
        "active": True,
        "task": ACTIVE_TASKS.get(squad_id, "Em operação"),
        "agents": agents,
        "overflow": overflow,
        "totalAgents": len(rows),
    }


def build_squads(squads_dir: Path) -> list[dict]:
    order = ["nexus", "branding", "conteudo-viral", "meta-ads-copy",
             "infraestrutura", "landing-pages-seo", "trafego-pago"]
    out = []
    for sid in order:
        sq = build_squad(squads_dir, sid)
        if sq:
            out.append(sq)
    return out


# ────────────────────────────────────────────────────────────────────
# Auto-discovery de clientes da categoria
# ────────────────────────────────────────────────────────────────────
def kpi_status(client: dict) -> str:
    """Cor-resumo de qualidade do cliente p/ o card multi-cliente."""
    pct = client.get("kpis", {}).get("pct_qualidade")
    if pct is None:
        return "neutral"
    if pct >= 30:
        return "green"
    if pct >= 18:
        return "yellow"
    return "red"


def load_client(client_dir: Path) -> dict | None:
    """Carrega um cliente da categoria lancamento-imobiliario, se for um.

    Discovery: tem readout-imobiliario.json com categoria == lancamento-imobiliario.
    O brand-profile.json é opcional (enriquece cores / nome), mas o readout manda.
    """
    readout_path = client_dir / READOUT_REL
    if not readout_path.is_file():
        return None
    try:
        readout = json.loads(readout_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  ⚠ readout ilegível em {client_dir.name}: {e}")
        return None
    if (readout.get("categoria") or "").strip() != CATEGORIA:
        return None

    slug = readout.get("slug") or client_dir.name.lower()
    nome = readout.get("cliente") or client_dir.name

    # Brand profile (opcional) — cores e nome bonito
    colors = {"primary": "#E46A37", "secondary": "#00ACA8", "accent": "#B99362"}
    brand_path = client_dir / BRAND_REL
    if brand_path.is_file():
        try:
            bp = json.loads(brand_path.read_text(encoding="utf-8"))
            vi = bp.get("visual_identity", {}) or bp.get("brand", {}).get("visual_identity", {})
            if vi.get("primary_color"):
                colors["primary"] = vi["primary_color"]
            if vi.get("secondary_color"):
                colors["secondary"] = vi["secondary_color"]
            if vi.get("accent_color"):
                colors["accent"] = vi["accent_color"]
            bn = bp.get("brand", {}).get("main") or bp.get("client", {}).get("name")
            if bn:
                nome = bn
        except Exception:
            pass

    tt = readout.get("timeline_total", {}) or {}
    test_tot = readout.get("testes_total", {}) or {}
    kpis = {
        "gasto": tt.get("gasto"),
        "leads": tt.get("leads"),
        "pct_qualidade": tt.get("pct_qualidade"),
        "cpl": test_tot.get("cpl"),
        "ctr": test_tot.get("ctr"),
    }

    # Squads do cliente (escritório virtual)
    squads = build_squads(client_dir / "squads")

    client = {
        "slug": slug,
        "nome": nome,
        "dirname": client_dir.name,
        "categoria": CATEGORIA,
        "meta_account": readout.get("meta_account", ""),
        "atualizado_em": readout.get("atualizado_em", ""),
        "periodo": readout.get("periodo", {}),
        "colors": colors,
        "faixas_renda": readout.get("faixas_renda", []),
        "faixa_qualidade_min": readout.get("faixa_qualidade_min", ""),
        "timeline": readout.get("timeline", []),
        "timeline_total": tt,
        "campanhas": readout.get("campanhas", []),
        "testes": readout.get("testes", []),
        "testes_total": test_tot,
        "ranking": readout.get("ranking", []),
        "alertas": readout.get("alertas", []),
        "kpis": kpis,
        "squads": squads,
        "total_agents": sum(s["totalAgents"] for s in squads),
        "total_squads": len(squads),
        "is_current": client_dir.resolve() == CLIENT_DIR.resolve(),
    }
    client["status"] = kpi_status(client)
    return client


def discover_clients() -> list[dict]:
    """Varre PROJETOS_CLAUDE_CODE/ atrás de clientes da categoria."""
    found = []
    for child in sorted(PROJECTS_ROOT.iterdir()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        c = load_client(child)
        if c:
            found.append(c)
    # cliente atual primeiro, resto por nome
    found.sort(key=lambda c: (not c["is_current"], c["nome"].lower()))
    return found


# ────────────────────────────────────────────────────────────────────
# Build + render
# ────────────────────────────────────────────────────────────────────
def build_data() -> dict:
    clients = discover_clients()
    return {
        "categoria": CATEGORIA,
        "current_slug": next((c["slug"] for c in clients if c["is_current"]),
                             clients[0]["slug"] if clients else ""),
        "clients": clients,
    }


def render_html(data: dict, html: str) -> str:
    js_data = (
        f"const cockpitData = {json.dumps(data, ensure_ascii=False, indent=2)};\n"
    )
    pattern = re.compile(
        re.escape(DATA_MARKER_START) + r".*?" + re.escape(DATA_MARKER_END),
        re.DOTALL,
    )
    new_block = f"{DATA_MARKER_START}\n{js_data}\n{DATA_MARKER_END}"
    if not pattern.search(html):
        print("✗ Marcadores DATA não encontrados no template — verifica office.html")
        return html
    return pattern.sub(new_block, html)


def main() -> int:
    if not TEMPLATE.is_file():
        print(f"✗ Template não existe: {TEMPLATE}")
        return 1

    print(f"📁 Cliente atual: {CLIENT_DIR.name}")
    print(f"🔎 Varrendo {PROJECTS_ROOT} por categoria '{CATEGORIA}'...")
    data = build_data()
    if not data["clients"]:
        print("✗ Nenhum cliente da categoria encontrado (readout-imobiliario.json ausente?)")
        return 1
    for c in data["clients"]:
        k = c["kpis"]
        marker = " ◀ atual" if c["is_current"] else ""
        print(f"   • {c['nome']:30s} gasto R${k['gasto']} · {k['leads']} leads · "
              f"{k['pct_qualidade']}% ≥{c['faixa_qualidade_min']} · {c['total_agents']} agentes{marker}")

    html = TEMPLATE.read_text(encoding="utf-8")
    html = render_html(data, html)
    TEMPLATE.write_text(html, encoding="utf-8")
    print(f"\n✓ {TEMPLATE} atualizado ({len(data['clients'])} cliente(s) na categoria)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
