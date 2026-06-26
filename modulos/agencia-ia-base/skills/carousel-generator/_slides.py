"""
_slides.py — Funções renderizadoras por tipo de slide.

Cada função recebe (slide_data, variant) e retorna o HTML completo do slide.
"""
from _styles import base_css, profile_badge_html, footer_html, render_inline_tags, PALETTE


def _wrap(extra_css: str, body_html: str, variant: str) -> str:
    """Wrap final: <html> + <head><style> + <body>."""
    css = base_css(variant) + "\n" + extra_css
    return f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><style>
{css}
</style></head><body>
<div class="slide">
{profile_badge_html()}
<div class="hero">
{body_html}
</div>
{{footer}}
</div></body></html>"""


def render_capa(s: dict, variant: str, slide_num: int) -> str:
    p = PALETTE[variant]
    extra = f"""
.hook{{font-family:'Poppins',sans-serif;font-weight:700;font-size:88px;color:{p['text']};line-height:1.02;letter-spacing:-2.5px}}
.subtitle{{font-family:'Inter',sans-serif;font-weight:400;font-size:28px;color:{p['muted']};line-height:1.5;max-width:780px;margin-top:48px}}
"""
    body = f"""<div class="eyebrow">{s.get('eyebrow', '')}</div>
<div class="hook">{render_inline_tags(s['hook'], variant)}</div>"""
    if s.get("subtitle"):
        body += f'\n<div class="subtitle">{render_inline_tags(s["subtitle"], variant)}</div>'
    return _wrap(extra, body, variant).replace("{footer}", footer_html(slide_num))


def render_body(s: dict, variant: str, slide_num: int) -> str:
    p = PALETTE[variant]
    extra = f"""
.hook{{font-family:'Poppins',sans-serif;font-weight:700;font-size:80px;color:{p['text']};line-height:1.05;letter-spacing:-2px;margin-bottom:36px}}
.body-text{{font-family:'Inter',sans-serif;font-weight:400;font-size:34px;color:{p['text']};line-height:1.5;max-width:880px}}
.body-text p{{margin-bottom:20px}}
.body-text p:last-child{{margin-bottom:0}}
"""
    body = f"""<div class="eyebrow">{s.get('eyebrow', '')}</div>
<div class="hook">{render_inline_tags(s['hook'], variant)}</div>
<div class="body-text">"""
    for para in s.get("paragraphs", []):
        body += f"\n  <p>{render_inline_tags(para, variant)}</p>"
    body += "\n</div>"
    return _wrap(extra, body, variant).replace("{footer}", footer_html(slide_num))


def render_lista(s: dict, variant: str, slide_num: int) -> str:
    p = PALETTE[variant]
    diamond_color = p['accent'] if variant != "GREEN" else "#000"
    item_color = p['text']
    extra = f"""
.hook{{font-family:'Poppins',sans-serif;font-weight:700;font-size:72px;color:{p['text']};line-height:1.05;letter-spacing:-2px;margin-bottom:44px}}
.item-list{{display:flex;flex-direction:column;gap:20px}}
.item{{display:flex;gap:22px;align-items:flex-start;font-family:'Inter',sans-serif;font-weight:400;font-size:30px;line-height:1.4;color:{item_color}}}
.item .diamond{{color:{diamond_color};flex-shrink:0;font-family:'JetBrains Mono',monospace;font-size:24px;line-height:1.5;padding-top:4px;font-weight:700}}
.closing{{font-family:'Poppins',sans-serif;font-weight:700;font-size:36px;color:{p['text']};line-height:1.3;margin-top:32px}}
"""
    body = f"""<div class="eyebrow">{s.get('eyebrow', '')}</div>
<div class="hook">{render_inline_tags(s['hook'], variant)}</div>
<div class="item-list">"""
    for item in s.get("items", []):
        body += f'\n  <div class="item"><span class="diamond">◆</span><span>{render_inline_tags(item, variant)}</span></div>'
    body += "\n</div>"
    if s.get("closing"):
        body += f'\n<div class="closing">{render_inline_tags(s["closing"], variant)}</div>'
    return _wrap(extra, body, variant).replace("{footer}", footer_html(slide_num))


def render_metrics(s: dict, variant: str, slide_num: int) -> str:
    p = PALETTE[variant]
    metric_border = "#000" if variant == "LIGHT" else "#222"
    label_color = "#666" if variant == "LIGHT" else p['muted']
    extra = f"""
.tag{{display:inline-block;background:#000;color:#8FDF65;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:22px;padding:8px 16px;border-radius:6px;letter-spacing:2px;margin-bottom:32px;width:fit-content}}
.hook{{font-family:'Poppins',sans-serif;font-weight:700;font-size:72px;color:{p['text']};line-height:1.05;letter-spacing:-2px;margin-bottom:36px}}
.desc{{font-family:'Inter',sans-serif;font-weight:400;font-size:30px;color:{label_color};line-height:1.45;max-width:880px;margin-bottom:48px}}
.metrics{{display:flex;flex-direction:column;gap:0;border:1.5px solid {metric_border};border-radius:12px;overflow:hidden}}
.metric{{display:flex;justify-content:space-between;padding:20px 28px;border-bottom:1px solid {metric_border};font-family:'JetBrains Mono',monospace;font-size:26px}}
.metric:last-child{{border-bottom:none}}
.metric .label{{color:{label_color};font-weight:500}}
.metric .val{{color:{p['text']};font-weight:700}}
.metric .val.hl{{background:#8FDF65;color:#000;padding:4px 12px;border-radius:6px}}
"""
    body = f'<div class="tag">{s.get("tag", "")}</div>\n'
    body += f'<div class="hook">{render_inline_tags(s["hook"], variant)}</div>\n'
    if s.get("desc"):
        body += f'<div class="desc">{render_inline_tags(s["desc"], variant)}</div>\n'
    body += '<div class="metrics">'
    for m in s.get("metrics", []):
        cls = "val hl" if m.get("highlight") else "val"
        body += f'\n  <div class="metric"><span class="label">{m["label"]}</span><span class="{cls}">{m["val"]}</span></div>'
    body += "\n</div>"
    return _wrap(extra, body, variant).replace("{footer}", footer_html(slide_num))


def render_dados(s: dict, variant: str, slide_num: int) -> str:
    p = PALETTE[variant]
    extra = f"""
.hook{{font-family:'Poppins',sans-serif;font-weight:700;font-size:64px;color:{p['text']};line-height:1.0;letter-spacing:-1.5px;margin-bottom:32px}}
.stats{{background:#000;color:#8FDF65;padding:32px 40px;border-radius:14px;font-family:'JetBrains Mono',monospace;display:flex;flex-direction:column;gap:18px}}
.stat-row{{display:flex;justify-content:space-between;align-items:center;font-size:28px;font-weight:500}}
.stat-row .num{{font-family:'Poppins',sans-serif;font-weight:700;color:#8FDF65;font-size:34px;letter-spacing:-0.5px}}
.stat-row .label{{color:#CCC;font-size:22px}}
.source{{font-family:'JetBrains Mono',monospace;font-size:16px;color:{p['dim']};margin-top:20px;font-weight:600}}
"""
    body = f"""<div class="eyebrow">{s.get('eyebrow', '')}</div>
<div class="hook">{render_inline_tags(s['hook'], variant)}</div>
<div class="stats">"""
    for r in s.get("rows", []):
        body += f'\n  <div class="stat-row"><span class="num">{r["num"]}</span><span class="label">{r["label"]}</span></div>'
    body += "\n</div>"
    if s.get("source"):
        body += f'\n<div class="source">{s["source"]}</div>'
    return _wrap(extra, body, variant).replace("{footer}", footer_html(slide_num))


def render_climax(s: dict, variant: str, slide_num: int) -> str:
    p = PALETTE[variant]
    extra = f"""
.equation{{display:flex;flex-direction:column;gap:12px;margin-bottom:32px}}
.eq-line{{font-family:'Poppins',sans-serif;font-weight:700;font-size:88px;line-height:1.0;color:{p['text']};letter-spacing:-2.5px}}
.subtitle{{font-family:'Inter',sans-serif;font-weight:500;font-size:30px;color:{p['muted']};line-height:1.5;max-width:800px;margin-top:24px}}
"""
    body = f'<div class="eyebrow">{s.get("eyebrow", "")}</div>\n<div class="equation">'
    for line in s.get("lines", []):
        body += f'\n  <div class="eq-line">{render_inline_tags(line, variant)}</div>'
    body += "\n</div>"
    if s.get("subtitle"):
        body += f'\n<div class="subtitle">{render_inline_tags(s["subtitle"], variant)}</div>'
    return _wrap(extra, body, variant).replace("{footer}", footer_html(slide_num))


def render_seeding(s: dict, variant: str, slide_num: int) -> str:
    """Igual a climax + box CRM Funnels (regra 1 em 3 da Diretiva NEXUS-001 §8)."""
    p = PALETTE[variant]
    extra = f"""
.equation{{display:flex;flex-direction:column;gap:12px;margin-bottom:24px}}
.eq-line{{font-family:'Poppins',sans-serif;font-weight:700;font-size:78px;line-height:1.0;color:{p['text']};letter-spacing:-2.5px}}
.subtitle{{font-family:'Inter',sans-serif;font-weight:500;font-size:28px;color:{p['muted']};line-height:1.5;max-width:800px;margin-top:16px;margin-bottom:28px}}
.proof{{padding:24px 30px;background:#000;border-radius:14px;font-family:'Inter',sans-serif;color:#FFF}}
.proof .top{{font-size:20px;font-weight:600;color:#A3A3A3;margin-bottom:10px;letter-spacing:2px;text-transform:uppercase}}
.proof .brand{{font-family:'Poppins',sans-serif;font-weight:700;font-size:38px;color:#8FDF65;letter-spacing:-1px;line-height:1.1;margin-bottom:8px}}
.proof .desc{{font-family:'Inter',sans-serif;font-weight:400;font-size:22px;color:#FFF;line-height:1.4}}
"""
    body = f'<div class="eyebrow">{s.get("eyebrow", "")}</div>\n<div class="equation">'
    for line in s.get("lines", []):
        body += f'\n  <div class="eq-line">{render_inline_tags(line, variant)}</div>'
    body += "\n</div>"
    if s.get("subtitle"):
        body += f'\n<div class="subtitle">{render_inline_tags(s["subtitle"], variant)}</div>'
    body += """
<div class="proof">
  <div class="top">— Meu SaaS</div>
  <div class="brand">CRM Funnels</div>
  <div class="desc">Toda minha entrega é vinculada a uma assinatura.</div>
</div>"""
    return _wrap(extra, body, variant).replace("{footer}", footer_html(slide_num))


def render_cta(s: dict, variant: str, slide_num: int) -> str:
    p = PALETTE[variant]
    # Cor da palavra grande + payoff highlight depende da variante
    if variant == "DARK":
        word_style = "color:#8FDF65"
        highlight_style = "color:#8FDF65;font-weight:700"
    elif variant == "LIGHT":
        word_style = "color:#000;background:#8FDF65;padding:0 24px;display:inline-block"
        highlight_style = "background:#8FDF65;padding:0 12px;display:inline-block"
    else:  # GREEN
        word_style = "color:#8FDF65;background:#000;padding:0 24px;display:inline-block"
        highlight_style = "background:#000;color:#8FDF65;padding:0 14px;display:inline-block"

    word = s["comenta_word"]
    n = len(word)
    if n <= 7:
        word_size = "200px"
    elif n <= 9:
        word_size = "160px"
    elif n <= 11:
        word_size = "130px"
    else:
        word_size = "110px"
    extra = f"""
.hero{{align-items:flex-start}}
.siga{{font-family:'Inter',sans-serif;font-weight:600;font-size:44px;color:{p['text']};margin-bottom:4px;letter-spacing:-0.5px}}
.comenta{{font-family:'Inter',sans-serif;font-weight:400;font-size:48px;color:{p['text']};margin-bottom:8px}}
.word{{font-family:'Poppins',sans-serif;font-weight:700;font-size:{word_size};line-height:0.9;letter-spacing:-6px;margin-bottom:64px;{word_style}}}
.payoff{{font-family:'Poppins',sans-serif;font-weight:600;font-size:42px;color:{p['text']};line-height:1.25;letter-spacing:-0.5px;max-width:920px}}
.payoff .hl{{{highlight_style}}}
"""
    body = f"""<div class="eyebrow">SUA VEZ</div>
<div class="siga">Siga o perfil e</div>
<div class="comenta">Comenta</div>
<div class="word">{word}</div>
<div class="payoff">{s.get('payoff_pre', 'e eu te mando o link do meu')}<br><span class="hl">{s.get('payoff_highlight', 'Treinamento Grátis')}</span> {s.get('payoff_post', 'de como criar sua ConsultorIA.')}</div>"""
    return _wrap(extra, body, variant).replace("{footer}", footer_html(slide_num))


# Dispatcher por tipo
RENDERERS = {
    "capa": render_capa,
    "body": render_body,
    "lista": render_lista,
    "metrics": render_metrics,
    "dados": render_dados,
    "climax": render_climax,
    "seeding": render_seeding,
    "cta": render_cta,
}


def render_slide(slide_data: dict, variant: str, slide_num: int) -> str:
    tipo = slide_data["tipo"]
    if tipo not in RENDERERS:
        raise ValueError(f"Tipo de slide desconhecido: {tipo}. Tipos válidos: {list(RENDERERS.keys())}")
    return RENDERERS[tipo](slide_data, variant, slide_num)
