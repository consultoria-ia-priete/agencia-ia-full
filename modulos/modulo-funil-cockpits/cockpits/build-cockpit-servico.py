#!/usr/bin/env python3
"""build-cockpit-servico.py — Cockpit de SERVIÇO LOCAL (FTC / EUA, USD).

Lê cockpit-servico.json (collect-servico-local.py) + brand-profile.json e gera
cockpit decisório: painel "Exige sua decisão", funil de serviço no topo (orçamento
→ agendamento → job), tráfego Google Ads (USD), cruzamentos custo/orçamento e
custo/job. Saída: FLOOR_TO_CEILING/_opensquad/dashboard/cockpit-servico.html.
"""
import json
import importlib.util
from datetime import datetime, timezone, timedelta
from pathlib import Path

BRT = timezone(timedelta(hours=-3))
PROJECTS = Path("$PROJECTS_ROOT")
_nav_spec = importlib.util.spec_from_file_location("cockpit_nav", Path(__file__).resolve().parent / "cockpit_nav.py")
cockpit_nav = importlib.util.module_from_spec(_nav_spec)
_nav_spec.loader.exec_module(cockpit_nav)
SRC = PROJECTS / "FLOOR_TO_CEILING" / "_opensquad" / "_memory" / "analises" / "cockpit-servico.json"
BRAND = PROJECTS / "FLOOR_TO_CEILING" / "_opensquad" / "_memory" / "brand-profile.json"
OUT = PROJECTS / "FLOOR_TO_CEILING" / "_opensquad" / "dashboard" / "cockpit-servico.html"
TEMPLATE = (Path(__file__).resolve().parent / "cockpit-servico.template.html").read_text(encoding="utf-8")


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def usd(v):
    return f"$ {v:,.2f}" if v is not None else "—"


def _hex2rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def _mix(h, f, t=0):
    r, g, b = _hex2rgb(h); return "#%02x%02x%02x" % tuple(int(c + (t - c) * f) for c in (r, g, b))


def load_brand():
    p, s = "#1A8FE6", "#22C55E"
    if BRAND.is_file():
        vi = json.loads(BRAND.read_text()).get("visual_identity", {})
        p = vi.get("primary_color", p); s = vi.get("secondary_color", s)
    return {"primary": p, "secondary": s, "pdark": _mix(p, .35), "pdarker": _mix(p, .58),
            "areia": _mix(p, .92, 255), "linha": _mix(p, .82, 255)}


def build():
    d = json.loads(SRC.read_text(encoding="utf-8"))
    brand = load_brand()
    g = d.get("google", {})
    funil = d.get("funil", {})
    cz = d.get("cruzamento", {})

    # ── Decisão ──
    alertas = []
    ativas = g.get("campanhas_ativas", [])
    # campanha gastando com CPA alto
    cpa = g.get("cpa")
    if cpa and cpa > 80:
        alertas.append({"sev": "yellow", "titulo": "CPA do Google elevado",
                        "porque": f'CPA {usd(cpa)} por conversão (14d)',
                        "impacto": "custo de aquisição alto — revisar lances/keywords",
                        "acao": "Revisar campanha Google", "detalhe": ativas[0]["nome"] if ativas else "Google"})
    # orçamentos parados sem agendar
    est = cz.get("estimates", 0); sch = cz.get("scheduled", 0)
    if est >= 3 and sch == 0:
        alertas.append({"sev": "red", "titulo": "Orçamentos sem agendamento",
                        "porque": f'{est} orçamentos feitos, 0 agendados',
                        "impacto": "clientes orçados esfriando — follow-up urgente",
                        "acao": "Cobrar follow-up de orçamentos", "detalhe": f'{est} parados'})
    # fonte de mídia paga com fechamento fraco vs orgânicas
    ff = {x["fonte"]: x for x in d.get("fonte_fechamento", [])}
    gads = ff.get("Google Ads")
    lsa = ff.get("Google LSA")
    if gads and gads.get("opps", 0) >= 3 and gads["pct"] < 70 and lsa and lsa["pct"] >= 85:
        alertas.append({"sev": "yellow", "titulo": "Google Ads fecha menos que o orgânico",
                        "porque": f'Google Ads {gads["pct"]}% vs Google LSA {lsa["pct"]}% de fechamento',
                        "impacto": "mídia paga converte pior que LSA/indicação — revisar ou realocar verba",
                        "acao": "Revisar qualidade do Google Ads", "detalhe": f'{gads["pct"]}% fecha'})
    # sem Meta ainda (lembrete)
    if not d.get("_meta"):
        alertas.append({"sev": "yellow", "titulo": "Meta Ads ainda não ativo",
                        "porque": "só Google rodando; Meta a ativar",
                        "impacto": "canal de captação adicional parado",
                        "acao": "Ativar Meta Ads", "detalhe": "FTC"})
    sev_ord = {"red": 0, "yellow": 1, "green": 2}
    alertas.sort(key=lambda a: sev_ord.get(a["sev"], 9))
    n_red = sum(1 for a in alertas if a["sev"] == "red")
    n_yellow = sum(1 for a in alertas if a["sev"] == "yellow")
    se = {"red": "🔴", "yellow": "🟡", "green": "🟢"}
    if alertas:
        cards = "".join(
            f'<div class="decision-card {a["sev"]}"><div class="dc-head">{se[a["sev"]]} '
            f'<strong>{esc(a["titulo"])}</strong></div><div class="dc-why">{esc(a["porque"])}</div>'
            f'<div class="dc-impact">{esc(a["impacto"])}</div>'
            f'<button class="dc-btn" data-acao="{esc(a["acao"])}" data-det="{esc(a["detalhe"])}">Gerar instrução</button></div>'
            for a in alertas)
        resumo = []
        if n_red: resumo.append(f'<b style="color:#d9534f">{n_red} exige decisão agora</b>')
        if n_yellow: resumo.append(f'{n_yellow} para atenção')
        painel = ('<div class="decision-panel"><div class="dp-title">⚡ Exige sua decisão '
                  f'<span class="dp-resumo">{" · ".join(resumo)}</span></div>'
                  f'<div class="decision-grid">{cards}</div></div>')
    else:
        painel = ('<div class="decision-panel ok"><div class="dp-title">✅ Tudo sob controle</div></div>')

    # ── Funil de serviço ──
    funil_html = ""
    if funil.get("stages"):
        stages = "".join(
            f'<div class="stage{" win" if s.get("win") else ""}"><div class="n">{s["count"]}</div>'
            f'<div class="lbl">{esc(s["label"])}</div></div>' for s in funil["stages"])
        funil_html = (f'<h2 style="margin-top:30px"><span class="accent"></span>Funil de Serviço</h2>'
                      f'<p class="sub-h2">Visão ao vivo do CRM · {funil.get("total",0)} oportunidades vivas '
                      f'no funil "{esc(funil.get("nome",""))}" (orçamento → agendamento → serviço).</p>'
                      f'<div class="funnel">{stages}</div>')

    # ── VISÃO GERAL: leads por FONTE + % de FECHAMENTO (volume × qualidade) ──
    fontes = d.get("fontes", [])
    tot_contatos = d.get("total_contatos", 0)
    fech_by = {x["fonte"]: x for x in d.get("fonte_fechamento", [])}
    fontes_html = ""
    if fontes:
        tot_f = sum(f["leads"] for f in fontes) or 1
        rows = ""
        for f in fontes:
            pct = round(100 * f["leads"] / tot_f)
            is_paid = f["fonte"] in ("Google Ads",)
            fech = fech_by.get(f["fonte"], {})
            # selo de fechamento: verde forte ≥90%, ok ≥70%, alerta <70% (com ≥3 opps)
            fech_html = ""
            if fech.get("opps", 0) >= 3:
                fp = fech["pct"]
                cls = "fech-hot" if fp >= 90 else ("fech-ok" if fp >= 70 else "fech-low")
                fech_html = (f'<span class="fech {cls}">{fp}% fecha</span>'
                             f'<span class="fech-n">{fech["done"]}/{fech["opps"]} jobs</span>')
            rows += (
                f'<div class="fonte-row"><div class="fonte-nome">{f["icone"]} {esc(f["fonte"])}'
                f'{" <span class=fonte-tag>mídia paga</span>" if is_paid else ""}</div>'
                f'<div class="fonte-bar"><span style="width:{pct}%"></span></div>'
                f'<div class="fonte-val">{f["leads"]} <span class="fonte-pct">{pct}%</span></div>'
                f'<div class="fonte-fech">{fech_html}</div></div>')
        fontes_html = (
            '<h2><span class="accent"></span>De onde vêm os leads — e quais fecham</h2>'
            f'<p class="sub-h2">Visão geral do CRM · {tot_contatos} contatos · '
            f'barra = volume de leads · selo = % que vira job fechado (qualidade da fonte).</p>'
            f'<div class="fontes">{rows}</div>')

    # ── Tráfego Google (métricas) ──
    metricas = [
        ("Investido", usd(g.get("cost")), "Google Ads · 14 dias", "meta"),
        ("Conversões", str(int(g.get("conv", 0))), "leads do Google", "meta"),
        ("Impressões", f'{g.get("impr",0):,}'.replace(",", "."), "anúncio exibido", "meta"),
        ("Cliques", str(g.get("clicks", 0)), "no anúncio", "meta"),
        ("CTR", f'{g.get("ctr",0):.2f}%', "cliques ÷ impressões", "meta"),
        ("CPC", usd(g.get("cpc")), "custo por clique", "meta"),
        ("CPA", usd(g.get("cpa")), "custo por conversão", "meta"),
        ("Custo/orçamento", usd(cz.get("custo_por_estimate")),
         f'gasto ÷ orçamentos ({cz.get("estimates",0)}) · CRM', "crm"),
        ("Custo/job", usd(cz.get("custo_por_job")),
         f'gasto ÷ serviços feitos ({cz.get("done",0)}) · CRM', "crm"),
    ]
    metr = "".join(
        f'<div class="metric {f}"><div class="m-label">{esc(n)}'
        f'{"<span class=m-badge>CRM</span>" if f=="crm" else ""}</div>'
        f'<div class="m-value">{esc(v)}</div><div class="m-sub">{esc(sub)}</div></div>'
        for n, v, sub, f in metricas)
    trafego_html = ('<h2><span class="accent"></span>Google Ads — a fatia paga</h2>'
                    '<p class="sub-h2">Métricas da única fonte com custo controlável (14 dias, USD). '
                    'Os 2 últimos cruzam o gasto com o funil do CRM.</p>'
                    f'<div class="metrics-grid">{metr}</div>')

    # ── Campanhas ativas ──
    camp_rows = "".join(
        f'<tr><td><strong>{esc(c["nome"])}</strong></td><td class="num">{usd(c["cost"])}</td>'
        f'<td class="num">{int(c["conv"])}</td><td class="num">{c["clicks"]}</td>'
        f'<td class="status-on">● ativa</td></tr>' for c in ativas)
    if not camp_rows:
        camp_rows = '<tr><td colspan="5">Nenhuma campanha ativa no momento.</td></tr>'

    repl = {
        "__CLIENTE__": esc(d.get("cliente", "FTC")),
        "__C_PRIMARY__": brand["primary"], "__C_SECONDARY__": brand["secondary"],
        "__C_PDARK__": brand["pdark"], "__C_PDARKER__": brand["pdarker"],
        "__C_AREIA__": brand["areia"], "__C_LINHA__": brand["linha"],
        "__DATA_HOJE__": datetime.now(BRT).strftime("%d / %m / %Y"),
        "__FUNIL_HTML__": funil_html, "__PAINEL_HTML__": painel,
        "__FONTES_HTML__": fontes_html,
        "__TRAFEGO_HTML__": trafego_html, "__CAMP_ROWS__": camp_rows,
        "__GERADO__": datetime.now(BRT).strftime("%d/%m/%Y %H:%M"),
        "__NAV_HTML__": cockpit_nav.nav_bar_for("FLOOR_TO_CEILING/_opensquad/dashboard/cockpit-servico.html"),
        "__NAV_CSS__": cockpit_nav.NAV_CSS,
    }
    html = TEMPLATE
    for k, v in repl.items():
        html = html.replace(k, v)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"✓ cockpit-servico.html · cor {brand['primary']} · {n_red} alertas vermelhos · {OUT}")


if __name__ == "__main__":
    build()
