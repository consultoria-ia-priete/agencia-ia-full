#!/usr/bin/env python3
"""build-cockpit-webinar.py — Cockpit de INFOPRODUTO/WEBINAR (Alex SSCIA / ConsultorIA).

Nicho próprio (não-imobiliário). Lê cockpit-webinar.json (coletado por
collect-webinar.py) + brand-profile.json e gera um cockpit DECISÓRIO:
- Painel "Exige sua decisão" no topo, com o alerta-rei: CAMPANHA ATIVA SEM ENTREGA
  (gasto ontem/3d zerado = parou por verba/billing — diretiva do Alex).
- Funil webinar (Lead→Grupo→Comunidade→High Ticket→Fechado).
- Campanhas ativas + quem aplicou pro high ticket.
- Geração de instrução (copia pro clipboard, igual ao cockpit imobiliário).

Saída: ALEX_SSCIA/_opensquad/dashboard/cockpit-webinar.html (file://).
"""
import json
import re
import importlib.util
from datetime import datetime, timezone, timedelta
from pathlib import Path

BRT = timezone(timedelta(hours=-3))
PROJECTS = Path("$PROJECTS_ROOT")

# barra de navegação compartilhada entre cockpits (← Central · chips · setas)
_nav_spec = importlib.util.spec_from_file_location("cockpit_nav", Path(__file__).resolve().parent / "cockpit_nav.py")
cockpit_nav = importlib.util.module_from_spec(_nav_spec)
_nav_spec.loader.exec_module(cockpit_nav)
SRC = PROJECTS / "ALEX_SSCIA" / "_opensquad" / "_memory" / "analises" / "cockpit-webinar.json"
BRAND = PROJECTS / "ALEX_SSCIA" / "_opensquad" / "_memory" / "brand-profile.json"
OUT = PROJECTS / "ALEX_SSCIA" / "_opensquad" / "dashboard" / "cockpit-webinar.html"
TEMPLATE = (Path(__file__).resolve().parent / "cockpit-webinar.template.html").read_text(encoding="utf-8")


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def money(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _hex2rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def _mix(h, f, target=0):
    r, g, b = _hex2rgb(h)
    return "#%02x%02x%02x" % tuple(int(c + (target - c) * f) for c in (r, g, b))


def load_brand():
    p, s = "#8FDF65", "#1a1a1a"
    if BRAND.is_file():
        vi = json.loads(BRAND.read_text()).get("visual_identity", {})
        p = vi.get("primary_color", p); s = vi.get("secondary_color", s)
    return {"primary": p, "secondary": s, "pdark": _mix(p, .35), "pdarker": _mix(p, .60),
            "areia": _mix(p, .90, 255), "linha": _mix(p, .80, 255)}


def build():
    d = json.loads(SRC.read_text(encoding="utf-8"))
    brand = load_brand()
    sp = d.get("spend", {})
    camps = d.get("campanhas_ativas", [])
    funil = d.get("funil", {})
    perto = d.get("perto_de_fechar", [])

    # ── MOTOR DE DECISÃO (webinar) ──
    alertas = []
    n_ativas = len(camps)
    gasto_total_ativas = sum(c["gasto"] for c in camps)
    # ALERTA-REI: campanhas ativas mas sem entrega (parou por verba)
    if n_ativas > 0 and sp.get("ontem", 0) == 0 and sp.get("d3", 0) == 0:
        alertas.append({
            "sev": "red", "titulo": f"{n_ativas} campanhas ativas SEM entrega",
            "porque": "gasto ontem R$0 e 3 dias R$0 — campanhas ligadas mas não rodam",
            "impacto": "provável falta de verba/billing — webinar sem captação parada",
            "acao": "Repor verba / revisar billing Meta", "detalhe": "conta act_478633523083228"})
    # leads zerados com campanha ativa
    total_leads = sum(c["leads"] for c in camps)
    if n_ativas > 0 and total_leads == 0 and gasto_total_ativas > 0:
        alertas.append({
            "sev": "yellow", "titulo": "Campanhas gastaram sem gerar lead",
            "porque": f"{money(gasto_total_ativas)} em 14d, 0 leads atribuídos",
            "impacto": "criativo ou segmentação não está convertendo",
            "acao": "Revisar criativos do webinar", "detalhe": "C1/C3/C4/C5"})
    # high ticket quente
    if perto:
        p0 = perto[0]
        alertas.append({
            "sev": "yellow", "titulo": f'Acompanhar {p0["nome"]}',
            "porque": f'{p0.get("prob",0)}% · {p0.get("estagio","")}',
            "impacto": "aplicou pro high ticket — não deixar esfriar",
            "acao": "Follow-up high ticket", "detalhe": p0["nome"]})

    sev_ord = {"red": 0, "yellow": 1, "green": 2}
    alertas.sort(key=lambda a: sev_ord.get(a["sev"], 9))
    n_red = sum(1 for a in alertas if a["sev"] == "red")
    n_yellow = sum(1 for a in alertas if a["sev"] == "yellow")
    sev_emoji = {"red": "🔴", "yellow": "🟡", "green": "🟢"}

    if alertas:
        cards = ""
        for a in alertas:
            cards += (f'<div class="decision-card {a["sev"]}"><div class="dc-head">'
                      f'{sev_emoji[a["sev"]]} <strong>{esc(a["titulo"])}</strong></div>'
                      f'<div class="dc-why">{esc(a["porque"])}</div>'
                      f'<div class="dc-impact">{esc(a["impacto"])}</div>'
                      f'<button class="dc-btn" data-acao="{esc(a["acao"])}" data-det="{esc(a["detalhe"])}">Gerar instrução</button></div>')
        resumo = []
        if n_red: resumo.append(f'<b style="color:var(--marca)">{n_red} exige decisão agora</b>')
        if n_yellow: resumo.append(f'{n_yellow} para atenção')
        painel = ('<div class="decision-panel"><div class="dp-title">⚡ Exige sua decisão '
                  f'<span class="dp-resumo">{" · ".join(resumo)}</span></div>'
                  f'<div class="decision-grid">{cards}</div></div>')
    else:
        painel = ('<div class="decision-panel ok"><div class="dp-title">✅ Tudo sob controle '
                  '<span class="dp-resumo">nenhuma decisão pendente</span></div></div>')

    # ── Painel de tráfego (métricas de mídia + cruzamento CRM) ──
    t = d.get("trafego", {})
    cr = d.get("cruzamento_crm", {})
    def _m(v, prefix="", suffix="", dash="—"):
        return f"{prefix}{v}{suffix}" if v not in (None, "", 0) or v == 0 and prefix == "" else dash
    def _val(v, fmt):
        return fmt.format(v) if v is not None else "—"
    def _int(v):
        return f"{int(v):,}".replace(",", ".") if v not in (None, "") else "—"
    metricas = [
        ("Impressões", _int(t.get("impressions")), "vezes que o anúncio apareceu", "meta"),
        ("Cliques", _int(t.get("clicks")), f'no link: {t.get("link_clicks",0)}', "meta"),
        ("CTR", _val(t.get("ctr"), "{:.2f}%"), "cliques ÷ impressões", "meta"),
        ("CPM", _val(t.get("cpm"), "R$ {:.2f}"), "custo por mil impressões", "meta"),
        ("CPC", _val(t.get("cpc"), "R$ {:.2f}"), "custo por clique", "meta"),
        ("Connect rate", _val(t.get("connect_rate"), "{:.1f}%"),
         f'LP view ({t.get("lp_views",0)}) ÷ clique ({t.get("link_clicks",0)})', "meta"),
        ("CPL", _val(t.get("cpl_meta"), "R$ {:.2f}"),
         f'gasto ÷ leads Meta ({t.get("leads_meta",0)})', "meta"),
        ("Custo/lead no grupo", _val(cr.get("custo_lead_grupo"), "R$ {:.2f}"),
         f'gasto ÷ entraram no grupo ({cr.get("no_grupo",0)}) · CRM', "crm"),
        ("CPV (custo/venda)", _val(cr.get("cpv"), "R$ {:.2f}"),
         f'gasto ÷ vendas fechadas ({cr.get("vendas",0)}) · CRM', "crm"),
    ]
    metr_cards = ""
    for nome, val, sub, fonte in metricas:
        badge = '<span class="m-badge crm">CRM</span>' if fonte == "crm" else ''
        metr_cards += (f'<div class="metric {fonte}"><div class="m-label">{esc(nome)}{badge}</div>'
                       f'<div class="m-value">{esc(val)}</div>'
                       f'<div class="m-sub">{esc(sub)}</div></div>')
    trafego_html = (
        '<h2><span class="accent"></span>Tráfego — métricas de mídia</h2>'
        '<p class="sub-h2">Performance dos criativos (14 dias). '
        'Os 2 últimos cruzam o gasto do Meta com o funil real do CRM.</p>'
        f'<div class="metrics-grid">{metr_cards}</div>')

    # ── Campanhas ativas (tabela) ──
    camp_rows = ""
    for c in sorted(camps, key=lambda x: -x["gasto"]):
        camp_rows += (f'<tr><td><strong>{esc(c["nome"])}</strong></td>'
                      f'<td class="num">{money(c["gasto"])}</td>'
                      f'<td class="num">{c["leads"]}</td>'
                      f'<td class="status-on">● ativa</td></tr>')

    # ── Funil webinar ──
    funil_html = ""
    if funil.get("stages"):
        stages = ""
        for s in funil["stages"]:
            win = " win" if s.get("win") else ""
            stages += (f'<div class="stage{win}"><div class="n">{s["count"]}</div>'
                       f'<div class="lbl">{esc(s["label"])}</div></div>')
        # funil é a 1ª seção (topo absoluto) → margin-top menor que o padrão 48px
        funil_html = (f'<h2 style="margin-top:30px"><span class="accent"></span>Funil do Webinar → High Ticket</h2>'
                      f'<p class="sub-h2">Visão ao vivo do CRM · {funil.get("total",0)} oportunidades no funil "{esc(funil.get("nome",""))}".</p>'
                      f'<div class="funnel">{stages}</div>')

    repl = {
        "__CLIENTE__": esc(d.get("cliente", "ConsultorIA")),
        "__C_PRIMARY__": brand["primary"], "__C_SECONDARY__": brand["secondary"],
        "__C_PDARK__": brand["pdark"], "__C_PDARKER__": brand["pdarker"],
        "__C_AREIA__": brand["areia"], "__C_LINHA__": brand["linha"],
        "__DATA_HOJE__": datetime.now(BRT).strftime("%d / %m / %Y"),
        "__PAINEL_HTML__": painel,
        "__KPI_GASTO14__": money(sp.get("d14", 0)),
        "__KPI_ONTEM__": money(sp.get("ontem", 0)),
        "__KPI_ATIVAS__": str(n_ativas),
        "__KPI_FUNIL__": str(funil.get("total", 0)),
        "__CAMP_ROWS__": camp_rows,
        "__TRAFEGO_HTML__": trafego_html,
        "__FUNIL_HTML__": funil_html,
        "__GERADO__": datetime.now(BRT).strftime("%d/%m/%Y %H:%M"),
        "__GERADO_ISO__": datetime.now(BRT).isoformat(),
        "__NAV_HTML__": cockpit_nav.nav_bar_for("ALEX_SSCIA/_opensquad/dashboard/cockpit-webinar.html"),
        "__NAV_CSS__": cockpit_nav.NAV_CSS,
    }
    html = TEMPLATE
    for k, v in repl.items():
        html = html.replace(k, v)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"✓ cockpit-webinar.html · cor {brand['primary']} · {n_red} alertas vermelhos · {OUT}")


if __name__ == "__main__":
    build()
