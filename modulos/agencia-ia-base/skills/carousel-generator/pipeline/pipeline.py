"""
pipeline.py — Orquestrador da Fase 2: ORACLE → SCRIPT (×3) → INK (×3) → GENERATOR (×3).

Roda o pipeline diário completo: gera 3 pautas, 3 roteiros, 3 captions, 24 HTMLs.

Uso:
    python3 pipeline.py [YYYY-MM-DD]   # default: hoje

Output:
    squads/conteudo-viral/output/pipeline-daily/{YYYY-MM-DD}/
        ├── pautas.json                    (saída ORACLE)
        ├── C{N}.json, C{N+1}.json, C{N+2}.json   (saída SCRIPT+INK)
        └── design/C{N}/, C{N+1}/, C{N+2}/        (HTMLs do generator)
"""
import sys
import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oracle import run_oracle
from script import run_script
from ink import run_ink

# Generator vive uma pasta acima
sys.path.insert(0, str(Path(__file__).parent.parent))
from generate import generate as generate_html


# Pasta do cliente: definida por OPENSQUAD_CLIENT_DIR (a skill install-base exporta),
# com fallback pro diretório atual de trabalho.
PROJECT_ROOT = Path(os.environ.get("OPENSQUAD_CLIENT_DIR", os.getcwd()))
PIPELINE_OUTPUT_DIR = PROJECT_ROOT / "squads/conteudo-viral/output/pipeline-daily"


def _ensure_shared_symlink(day_dir: Path) -> None:
    """Garante que `{day_dir}/design/_shared` aponta pra `output/design/_shared`.

    HTMLs referenciam `../_shared/alex-profile.jpg` e `../_shared/fonts/*` —
    sem esse symlink, avatar e fontes não resolvem nos PNGs renderizados.
    """
    design_dir = day_dir / "design"
    design_dir.mkdir(parents=True, exist_ok=True)
    link = design_dir / "_shared"
    target = "../../../design/_shared"
    if link.is_symlink() or link.exists():
        link.unlink()
    link.symlink_to(target)


def run_pipeline(target_date: str) -> dict:
    """Roda o pipeline completo para a data alvo. Retorna dict de status."""
    day_dir = PIPELINE_OUTPUT_DIR / target_date
    day_dir.mkdir(parents=True, exist_ok=True)
    _ensure_shared_symlink(day_dir)

    print(f"\n{'='*60}", file=sys.stderr)
    print(f"PIPELINE DIÁRIO — {target_date}", file=sys.stderr)
    print(f"{'='*60}\n", file=sys.stderr)

    status = {"date": target_date, "carousels": []}

    # 1) ORACLE — 3 pautas
    print("[1/4] ORACLE — escolhendo 3 pautas...", file=sys.stderr)
    pautas_data = run_oracle(target_date, save_dir=day_dir)
    pautas = pautas_data["pautas"]
    print(f"      ✓ 3 pautas: {[p['id'] + ' ' + p['palavra_gatilho'] for p in pautas]}\n", file=sys.stderr)

    # 2-3) SCRIPT + INK por pauta
    for i, pauta in enumerate(pautas, 1):
        cid = pauta["id"]
        print(f"[2/4] SCRIPT — roteiro {cid} ({pauta['variant']})...", file=sys.stderr)
        roteiro = run_script(pauta)

        print(f"[3/4] INK — caption {cid}...", file=sys.stderr)
        carousel_final = run_ink(roteiro)

        carousel_path = day_dir / f"{cid}.json"
        carousel_path.write_text(
            json.dumps(carousel_final, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(f"      ✓ Salvo em {carousel_path}\n", file=sys.stderr)

        # 4) GENERATOR — 8 HTMLs
        design_dir = day_dir / "design" / cid
        print(f"[4/4] GENERATOR — 8 HTMLs de {cid}...", file=sys.stderr)
        generate_html(carousel_final, str(design_dir))
        print(file=sys.stderr)

        status["carousels"].append({
            "id": cid,
            "tema": pauta["tema"],
            "slot_brt": pauta["slot_brt"],
            "variant": pauta["variant"],
            "palavra_gatilho": pauta["palavra_gatilho"],
            "tem_seeding": pauta["tem_seeding_crm_funnels"],
            "json_path": str(carousel_path),
            "design_dir": str(design_dir),
        })

        # Pausa entre carrosséis pra não sobrecarregar API
        if i < len(pautas):
            time.sleep(2)

    # Salvar status do dia
    status_path = day_dir / "_status.json"
    status_path.write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n{'='*60}", file=sys.stderr)
    print(f"✅ PIPELINE COMPLETO — {len(status['carousels'])} carrosséis gerados", file=sys.stderr)
    print(f"   Output: {day_dir}", file=sys.stderr)
    print(f"{'='*60}\n", file=sys.stderr)

    return status


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y-%m-%d")
    out = run_pipeline(target)
    print(json.dumps(out, ensure_ascii=False, indent=2))
