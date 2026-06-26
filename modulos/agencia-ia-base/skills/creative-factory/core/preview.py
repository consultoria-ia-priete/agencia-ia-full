"""
preview.py — gera preview.html mostrando os slides gerados, texto on-image,
captions e metadados.

Regra do ecossistema (memória feedback_preview_html_obrigatorio.md):
    SEMPRE mandar preview HTML antes de publicar peça visual.
"""
from __future__ import annotations

import html
import json
from datetime import datetime
from pathlib import Path
from typing import Any


HTML_TEMPLATE = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Preview — {title}</title>
<style>
  :root {{
    --bg: #0b0d11;
    --panel: #14171d;
    --border: #232934;
    --text: #e7e9ee;
    --muted: #8b95a5;
    --accent: #ffb547;
    --green: #4ade80;
    --red: #f87171;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 32px;
    background: var(--bg); color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Inter", sans-serif;
  }}
  h1 {{ margin: 0 0 8px; font-size: 24px; }}
  .meta {{ color: var(--muted); font-size: 13px; margin-bottom: 24px; }}
  .meta strong {{ color: var(--text); }}
  .slides {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; }}
  .slide {{
    background: var(--panel); border: 1px solid var(--border); border-radius: 12px;
    overflow: hidden; display: flex; flex-direction: column;
  }}
  .slide .img-wrap {{
    aspect-ratio: 1 / 1; background: #000; display: flex; align-items: center; justify-content: center;
    position: relative;
  }}
  .slide .img-wrap img {{ width: 100%; height: 100%; object-fit: cover; }}
  .slide .img-wrap .placeholder {{
    color: var(--muted); font-size: 13px; text-align: center; padding: 24px;
  }}
  .slide .img-wrap .badge {{
    position: absolute; top: 12px; left: 12px;
    padding: 4px 10px; border-radius: 999px;
    background: rgba(0,0,0,0.6); border: 1px solid rgba(255,255,255,0.15);
    font-size: 11px; letter-spacing: 0.05em; text-transform: uppercase;
  }}
  .slide .img-wrap .text-overlay {{
    position: absolute; bottom: 16px; left: 16px; right: 16px;
    background: rgba(0,0,0,0.55); color: #fff;
    padding: 8px 12px; border-radius: 6px; font-size: 14px; font-weight: 600;
  }}
  .slide .body {{ padding: 14px 16px; flex: 1; display: flex; flex-direction: column; gap: 8px; }}
  .slide .caption {{ font-size: 13px; line-height: 1.5; }}
  .slide .meta-row {{ display: flex; gap: 8px; flex-wrap: wrap; font-size: 11px; color: var(--muted); }}
  .slide .meta-row span {{
    border: 1px solid var(--border); padding: 2px 8px; border-radius: 999px;
  }}
  .slide.error {{ border-color: var(--red); }}
  .slide.error .img-wrap {{ background: #2a0e0e; }}
  .slide.error .err {{ color: var(--red); font-size: 12px; padding: 8px 12px; word-break: break-all; }}
  .footer {{ margin-top: 32px; padding-top: 16px; border-top: 1px solid var(--border); color: var(--muted); font-size: 12px; }}
  .footer details {{ margin-top: 8px; }}
  .footer pre {{
    background: var(--panel); border: 1px solid var(--border); padding: 12px; border-radius: 6px;
    overflow: auto; font-size: 11px;
  }}
</style>
</head>
<body>
<h1>{title}</h1>
<div class="meta">
  <strong>Cliente:</strong> {client_name} &nbsp;·&nbsp;
  <strong>Marca:</strong> {brand_main} &nbsp;·&nbsp;
  <strong>Idioma:</strong> {language} &nbsp;·&nbsp;
  <strong>Template:</strong> {template_name} &nbsp;·&nbsp;
  <strong>Gerado:</strong> {generated_at} &nbsp;·&nbsp;
  <strong>Custo estimado:</strong> ${cost_estimate:.3f}
</div>

<div class="slides">
{slides_html}
</div>

<div class="footer">
  <strong>Briefing:</strong> {brief}<br>
  <strong>Output dir:</strong> <code>{output_dir}</code>
  <details><summary>Metadata bruto (JSON)</summary><pre>{raw_meta}</pre></details>
</div>
</body>
</html>
"""

SLIDE_TEMPLATE = """  <div class="slide{error_class}">
    <div class="img-wrap">
      <span class="badge">Slide {slide_id} · {slide_type}</span>
      {image_or_placeholder}
      {text_overlay_html}
    </div>
    <div class="body">
      <div class="caption">{caption}</div>
      <div class="meta-row">
        <span>{model}</span>
        <span>{aspect}</span>
        <span>{elapsed}s</span>
        <span>${cost:.3f}</span>
      </div>
      {error_html}
    </div>
  </div>
"""


def render_preview(
    *,
    title: str,
    output_path: Path | str,
    client_name: str,
    brand_main: str,
    language: str,
    template_name: str,
    brief: str,
    output_dir: str,
    slides: list[dict[str, Any]],
) -> Path:
    """
    Gera preview.html no path indicado.

    `slides` é uma lista de dicts com:
        slide_id, slide_type, image_url (ou local path), text_overlay, caption,
        model, aspect, elapsed_s, cost_estimate_usd, error (opcional)
    """
    slides_html_parts = []
    total_cost = 0.0
    for s in slides:
        is_error = bool(s.get("error"))
        img_url = s.get("image_url") or ""
        if is_error:
            img_html = '<div class="placeholder">⚠️ Falha na geração</div>'
        elif img_url:
            img_html = f'<img src="{html.escape(img_url)}" alt="slide {s.get("slide_id")}">'
        else:
            img_html = '<div class="placeholder">(sem imagem)</div>'

        text_overlay = s.get("text_overlay") or ""
        text_overlay_html = (
            f'<div class="text-overlay">{html.escape(text_overlay)}</div>'
            if text_overlay else ""
        )

        cost = float(s.get("cost_estimate_usd", 0) or 0)
        total_cost += cost
        error_html = (
            f'<div class="err">{html.escape(s.get("error", ""))}</div>'
            if is_error else ""
        )

        slides_html_parts.append(SLIDE_TEMPLATE.format(
            error_class=" error" if is_error else "",
            slide_id=html.escape(str(s.get("slide_id", "?"))),
            slide_type=html.escape(str(s.get("slide_type", "content"))),
            image_or_placeholder=img_html,
            text_overlay_html=text_overlay_html,
            caption=html.escape(s.get("caption", "") or ""),
            model=html.escape(str(s.get("model", "?"))),
            aspect=html.escape(str(s.get("aspect", "?"))),
            elapsed=s.get("elapsed_s", 0),
            cost=cost,
            error_html=error_html,
        ))

    raw_meta = json.dumps(slides, indent=2, ensure_ascii=False, default=str)

    html_full = HTML_TEMPLATE.format(
        lang=("pt" if language.startswith("pt") else "en"),
        title=html.escape(title),
        client_name=html.escape(client_name),
        brand_main=html.escape(brand_main),
        language=html.escape(language),
        template_name=html.escape(template_name),
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        cost_estimate=total_cost,
        slides_html="".join(slides_html_parts),
        brief=html.escape(brief or ""),
        output_dir=html.escape(output_dir),
        raw_meta=html.escape(raw_meta),
    )

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_full, encoding="utf-8")
    return out
