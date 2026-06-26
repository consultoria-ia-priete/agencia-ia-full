"""
ink.py — Recebe um roteiro completo (do SCRIPT) e gera a caption multilinha.

Atualiza o campo `caption` do JSON e retorna o JSON completo pronto pro generator.

Uso:
    python3 ink.py < roteiro.json > carousel-final.json
"""
import sys
import json
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _claude import call_claude_json, load_prompt_template


def run_ink(carousel: dict) -> dict:
    """Recebe carrossel JSON e atualiza o campo `caption`."""
    system_prompt = load_prompt_template("ink")
    user_input = {
        "tema": carousel.get("tema"),
        "pilar": carousel.get("pilar"),
        "palavra_gatilho": carousel.get("palavra_gatilho"),
        "slides": carousel.get("slides"),
    }

    full_prompt = (
        f"{system_prompt}\n\n"
        f"---\n\n"
        f"## Carrossel a captionar\n\n"
        f"```json\n{json.dumps(user_input, ensure_ascii=False, indent=2)}\n```"
    )

    print(f"[INK] Escrevendo caption para '{carousel.get('tema', '?')}'...", file=sys.stderr)
    result = call_claude_json(full_prompt)

    if "caption" not in result:
        raise ValueError(f"INK não retornou campo 'caption'")

    caption = result["caption"]
    palavra = carousel["palavra_gatilho"]
    expected = f"Comenta {palavra} aqui e eu te mando o link do meu Treinamento Grátis de como criar sua ConsultorIA"

    if expected not in caption:
        print(f"[INK] ⚠️ Caption não contém a fórmula CTA exata — verificar manualmente", file=sys.stderr)

    carousel["caption"] = caption
    return carousel


if __name__ == "__main__":
    carousel = json.load(sys.stdin)
    out = run_ink(carousel)
    print(json.dumps(out, ensure_ascii=False, indent=2))
