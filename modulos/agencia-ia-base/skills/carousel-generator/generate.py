"""
generate.py — Lê um JSON de carrossel e produz os 8 HTMLs em uma pasta.

Uso:
    python3 generate.py <input.json> <output_dir>
    python3 generate.py examples/C09.json /tmp/carousel-c09/

Também aceita stdin:
    cat carousel.json | python3 generate.py - <output_dir>
"""
import sys
import json
import os
from pathlib import Path

# Permite import dos arquivos vizinhos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _slides import render_slide


def validate(data: dict) -> list[str]:
    """Retorna lista de erros (vazia se OK)."""
    errs = []
    required_root = ["id", "data_publicacao", "slot_brt", "tema", "pilar",
                     "variant", "palavra_gatilho", "tem_seeding_crm_funnels",
                     "caption", "slides"]
    for k in required_root:
        if k not in data:
            errs.append(f"Falta campo obrigatório na raiz: '{k}'")

    if data.get("variant") not in ("DARK", "LIGHT", "GREEN"):
        errs.append(f"variant deve ser DARK|LIGHT|GREEN, recebido: {data.get('variant')}")

    slides = data.get("slides", [])
    if len(slides) != 8:
        errs.append(f"Deve ter exatamente 8 slides, recebido: {len(slides)}")

    if slides:
        if slides[0].get("tipo") != "capa":
            errs.append(f"Slide 1 deve ser tipo 'capa', recebido: {slides[0].get('tipo')}")
        if slides[-1].get("tipo") != "cta":
            errs.append(f"Slide 8 deve ser tipo 'cta', recebido: {slides[-1].get('tipo')}")

        if data.get("tem_seeding_crm_funnels") and slides[6].get("tipo") != "seeding":
            errs.append("tem_seeding_crm_funnels=true mas slide 7 não é tipo 'seeding'")
        if not data.get("tem_seeding_crm_funnels") and slides[6].get("tipo") == "seeding":
            errs.append("slide 7 é 'seeding' mas tem_seeding_crm_funnels=false")

        # Validar palavra-gatilho aparece no CTA
        cta = slides[-1]
        if data.get("palavra_gatilho") and cta.get("comenta_word") != data["palavra_gatilho"]:
            errs.append(f"palavra_gatilho ({data.get('palavra_gatilho')}) != cta.comenta_word ({cta.get('comenta_word')})")

    return errs


def generate(data: dict, output_dir: str):
    """Gera os 8 HTMLs no output_dir."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    variant = data["variant"]
    cid = data["id"]

    for i, slide in enumerate(data["slides"], 1):
        html = render_slide(slide, variant, i)
        fname = output_path / f"{cid}-slide-{i:02d}.html"
        fname.write_text(html, encoding="utf-8")
        print(f"  ✓ {fname}")

    print(f"\n✓ {len(data['slides'])} HTMLs gerados em {output_path}")


def main():
    if len(sys.argv) < 3:
        print("Uso: python3 generate.py <input.json|-> <output_dir>")
        sys.exit(1)

    src = sys.argv[1]
    out = sys.argv[2]

    if src == "-":
        data = json.load(sys.stdin)
    else:
        data = json.load(open(src))

    errs = validate(data)
    if errs:
        print("❌ Erros de validação:")
        for e in errs:
            print(f"  · {e}")
        sys.exit(2)

    generate(data, out)


if __name__ == "__main__":
    main()
