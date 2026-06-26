"""
script.py — Recebe 1 pauta e produz o JSON completo do roteiro de 8 slides.

Uso:
    python3 script.py < pauta.json > roteiro.json
"""
import sys
import json
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _claude import call_claude_json, load_prompt_template


def run_script(pauta: dict) -> dict:
    """Recebe 1 pauta (do ORACLE) e retorna o roteiro JSON completo."""
    system_prompt = load_prompt_template("script")
    full_prompt = (
        f"{system_prompt}\n\n"
        f"---\n\n"
        f"## Pauta a desenvolver\n\n"
        f"```json\n{json.dumps(pauta, ensure_ascii=False, indent=2)}\n```"
    )

    print(f"[SCRIPT] Roteirizando '{pauta.get('tema', '?')}'...", file=sys.stderr)
    result = call_claude_json(full_prompt)

    # Validações — Claude às vezes desvia (7 ou 9 slides). 2026-05-13: pipeline quebrou
    # com 9 slides. Estratégia: aceitar 7-9 e auto-ajustar pra 8 mantendo capa + cta.
    if "slides" not in result:
        raise ValueError(f"SCRIPT response sem campo 'slides': keys={list(result.keys())}")

    slides = result["slides"]
    n = len(slides)
    if n != 8:
        if n < 7 or n > 10:
            # Fora do envelope tolerável — não vale corrigir
            raise ValueError(f"SCRIPT retornou {n} slides — fora do envelope tolerado (7-10)")
        print(f"[SCRIPT] WARN: Claude retornou {n} slides, ajustando pra 8...", file=sys.stderr)
        # Estratégia: manter slide[0] (capa) + slide[-1] (cta). Do meio, trunca ou repete.
        capa = slides[0]
        cta = slides[-1]
        middle = slides[1:-1]
        target_middle = 6  # capa(1) + middle(6) + cta(1) = 8
        if len(middle) > target_middle:
            # Trunca os do meio (mantém os primeiros)
            middle = middle[:target_middle]
            print(f"[SCRIPT] truncou {n-8} slide(s) do meio", file=sys.stderr)
        elif len(middle) < target_middle:
            # Duplica o último do meio pra preencher (raro, fallback)
            while len(middle) < target_middle:
                middle.append(dict(middle[-1]))
            print(f"[SCRIPT] duplicou último slide do meio até preencher", file=sys.stderr)
        slides = [capa] + middle + [cta]
        result["slides"] = slides

    if result["slides"][0].get("tipo") != "capa":
        raise ValueError(f"Slide 1 deve ser 'capa', recebido: {result['slides'][0].get('tipo')}")

    if result["slides"][-1].get("tipo") != "cta":
        raise ValueError(f"Slide 8 deve ser 'cta', recebido: {result['slides'][-1].get('tipo')}")

    if pauta.get("tem_seeding_crm_funnels") and result["slides"][6].get("tipo") != "seeding":
        raise ValueError("tem_seeding=true mas slide 7 não é tipo 'seeding'")

    # Garante que campos da raiz batem com a pauta original
    result["id"] = pauta["id"]
    result["data_publicacao"] = pauta["data_publicacao"]
    result["slot_brt"] = pauta["slot_brt"]
    result["tema"] = pauta["tema"]
    result["pilar"] = pauta["pilar"]
    result["variant"] = pauta["variant"]
    result["palavra_gatilho"] = pauta["palavra_gatilho"]
    result["tem_seeding_crm_funnels"] = pauta["tem_seeding_crm_funnels"]

    # Garante que comenta_word do slide 8 = palavra_gatilho
    result["slides"][-1]["comenta_word"] = pauta["palavra_gatilho"]

    return result


if __name__ == "__main__":
    pauta = json.load(sys.stdin)
    out = run_script(pauta)
    print(json.dumps(out, ensure_ascii=False, indent=2))
