"""
prompt_builder.py — combina template YAML + brand profile + brief → prompts finais.

Templates ficam em ~/.claude/skills/creative-factory/templates/<categoria>/<nome>.yaml
Estrutura padrão:

    template: cleaning_before_after
    version: 1.0
    niche: residential cleaning
    purpose: organic_carousel       # organic_carousel | ad | gmb_post
    default_model: flux-dev
    default_aspect: "1:1"
    slides:
      - id: 1
        type: hook
        visual_prompt: |
          ...{{brand.tone}}...{{brief}}...{{geo_hint}}...
        text_overlay: "..."
        caption: "..."

Vars suportadas no `visual_prompt`:
    {{brand.main}}                  → nome da marca
    {{brand.industry}}              → ex: 'residential cleaning'
    {{brand.tone}}                  → tom da marca
    {{brand.color_primary}}         → hex
    {{brand.color_secondary}}       → hex
    {{brand.negative}}              → negative_visual_prompt
    {{geo_hint}}                    → ex: "in a New Jersey suburban home"
    {{language}}                    → 'pt-BR' ou 'en-US'
    {{brief}}                       → tema livre que o operador passou
    {{brief.tema}} {{brief.cidade}} → quando brief é dict
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .brand_loader import BrandProfile

VAR_RE = re.compile(r"\{\{([\w.]+)\}\}")
TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


@dataclass
class SlidePrompt:
    """Prompt pronto pra um slide."""
    slide_id: str
    slide_type: str
    visual_prompt: str
    text_overlay: str = ""
    caption: str = ""
    model: str = "flux-dev"
    aspect: str = "1:1"
    image_size: str = "square_hd"
    image_refs: list[str] | None = None


def _resolve_var(path: str, brand: BrandProfile, brief: Any, extra: dict) -> str:
    """Resolve {{x.y.z}} buscando em ordem: extra → brief → brand."""
    parts = path.split(".")
    head = parts[0]
    rest = parts[1:] if len(parts) > 1 else []

    # 1) extras (geo_hint, language, brief, etc.)
    if head in extra and not rest:
        return str(extra[head])

    # 2) brief (dict ou str)
    if head == "brief":
        if isinstance(brief, str):
            return brief if not rest else ""
        if isinstance(brief, dict):
            cur: Any = brief
            for k in rest:
                cur = (cur or {}).get(k)
            return str(cur) if cur is not None else ""
        return ""

    # 3) brand.* (mapeamento manual pra evitar reflection)
    if head == "brand":
        mapping = {
            "main": brand.brand_main,
            "industry": brand.industry,
            "tone": brand.voice_tone,
            "color_primary": brand.primary_color,
            "color_secondary": brand.secondary_color,
            "negative": brand.negative_visual_prompt,
            "language": brand.publication_language,
        }
        if rest and rest[0] in mapping:
            return str(mapping[rest[0]])
        return ""

    return ""


def _substitute(text: str, brand: BrandProfile, brief: Any, extra: dict) -> str:
    def repl(m: re.Match[str]) -> str:
        return _resolve_var(m.group(1), brand, brief, extra)
    return VAR_RE.sub(repl, text)


def _build_geo_hint(brand: BrandProfile) -> str:
    """Constrói pista geográfica do brand-profile pra ajudar o modelo a contextualizar."""
    parts = []
    if brand.geo_state and brand.geo_country == "US":
        parts.append(f"American {brand.geo_state} suburban setting")
    elif brand.geo_country == "BR":
        parts.append("Brazilian setting")
    if brand.geo_cities:
        parts.append(f"({brand.geo_cities[0]} area)")
    return ", ".join(parts) if parts else ""


def load_template(template_name: str, *, category: str = "carousel") -> dict[str, Any]:
    """Carrega template YAML por nome curto. category ∈ {carousel, ads, single}."""
    path = TEMPLATES_DIR / category / f"{template_name}.yaml"
    if not path.is_file():
        # fallback: procura em qualquer category
        candidates = list(TEMPLATES_DIR.glob(f"*/{template_name}.yaml"))
        if not candidates:
            raise FileNotFoundError(
                f"Template '{template_name}' não encontrado em {TEMPLATES_DIR}"
            )
        path = candidates[0]
    with path.open() as f:
        return yaml.safe_load(f)


def build_carousel_prompts(
    template_name: str,
    brand: BrandProfile,
    brief: Any = "",
    *,
    category: str = "carousel",
) -> tuple[dict[str, Any], list[SlidePrompt]]:
    """
    Carrega template, resolve variáveis, retorna (template_meta, list[SlidePrompt]).
    """
    tpl = load_template(template_name, category=category)

    extra = {
        "geo_hint": _build_geo_hint(brand),
        "language": brand.publication_language,
    }

    default_model = tpl.get("default_model") or brand.model_organic
    default_aspect = tpl.get("default_aspect") or brand.aspect_ratio_carousel
    image_size = "square_hd" if default_aspect in ("1:1", "square") else "portrait_16_9" if default_aspect == "9:16" else "square_hd"

    prompts: list[SlidePrompt] = []
    for s in tpl.get("slides", []):
        visual = _substitute(s.get("visual_prompt", ""), brand, brief, extra).strip()
        # Adiciona negative ao final se houver
        if brand.negative_visual_prompt and "negative" not in visual.lower():
            visual = f"{visual}\nAvoid: {brand.negative_visual_prompt}"

        prompts.append(SlidePrompt(
            slide_id=str(s.get("id", f"s{len(prompts)+1}")),
            slide_type=s.get("type", "content"),
            visual_prompt=visual,
            text_overlay=_substitute(s.get("text_overlay", "") or "", brand, brief, extra),
            caption=_substitute(s.get("caption", "") or "", brand, brief, extra),
            model=s.get("model") or default_model,
            aspect=s.get("aspect") or default_aspect,
            image_size=image_size,
        ))

    return tpl, prompts


if __name__ == "__main__":
    import sys
    from .brand_loader import load_brand
    if len(sys.argv) < 3:
        print("Uso: python3 -m core.prompt_builder <client_dir> <template_name> [brief]")
        sys.exit(1)
    brand = load_brand(sys.argv[1], strict=False)
    brief = sys.argv[3] if len(sys.argv) > 3 else "demonstração"
    meta, prompts = build_carousel_prompts(sys.argv[2], brand, brief)
    print(f"Template: {meta.get('template')} v{meta.get('version')}")
    for p in prompts:
        print(f"\n── Slide {p.slide_id} ({p.slide_type}) — model={p.model} ──")
        print(p.visual_prompt)
        if p.text_overlay:
            print(f"[TEXT OVERLAY: {p.text_overlay}]")
