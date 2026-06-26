#!/usr/bin/env python3
"""
viral_short.py — pipeline E2E pra geração de vídeo viral curto.

Fluxo:
  1. Carrega brand-profile do cliente
  2. Carrega template (ex: before_after.yaml) com script segments + slides
  3. ElevenLabs TTS → MP3 do voiceover
  4. Whisper STT → SRT word-level
  5. creative-factory → 6 imagens dos slides
  6. Remotion render → MP4 1080x1920
  7. (Opcional) Auto-crop pra 1080x1080 (Feed/GMB) e 30s pro GMB

Uso:
  python3 viral_short.py \\
    --client /Users/.../FLOOR_TO_CEILING \\
    --template before_after \\
    --brief "Spring deep cleaning — pricing contrast story" \\
    --output-id "V001" \\
    [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
CREATIVE_FACTORY = Path.home() / ".claude" / "skills" / "creative-factory"

if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))
if str(CREATIVE_FACTORY) not in sys.path:
    sys.path.insert(0, str(CREATIVE_FACTORY))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--client", required=True)
    p.add_argument("--template", required=True, help="ex: before_after, dica_rapida, depoimento")
    p.add_argument("--brief", default="")
    p.add_argument("--output-id", default="")
    p.add_argument("--script-text", help="Roteiro completo (se já escrito); se vazio, pipeline pede")
    p.add_argument("--dry-run", action="store_true", help="não chama APIs externas — só monta plano")
    return p.parse_args()


def load_template(name: str) -> dict:
    import yaml
    candidates = list((SKILL_DIR / "templates").glob(f"*/{name}.yaml"))
    if not candidates:
        raise FileNotFoundError(f"Template '{name}' não encontrado em {SKILL_DIR / 'templates'}")
    return yaml.safe_load(candidates[0].read_text())


def main() -> int:
    args = parse_args()
    started = datetime.now()

    # Brand
    from core.brand_loader import load_brand  # creative-factory's brand_loader
    brand = load_brand(args.client, strict=False)
    print(f"📂 Cliente: {brand.client_name} ({brand.brand_main}, {brand.publication_language})")

    # Template
    tpl = load_template(args.template)
    print(f"📋 Template: {tpl['template']} v{tpl['version']} ({tpl['default_duration_s']}s, {tpl['slide_count']} slides)")

    # Output dir
    today = datetime.now().strftime("%Y-%m-%d")
    out_id = args.output_id or datetime.now().strftime("%H%M")
    out_dir = (
        Path(args.client).expanduser().resolve()
        / "squads" / "conteudo-viral" / "output" / "videos"
        / f"{today}_{out_id}"
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 Output: {out_dir}")

    # Plan
    plan = {
        "client": brand.client_name,
        "brand_main": brand.brand_main,
        "language": brand.publication_language,
        "template": tpl["template"],
        "brief": args.brief,
        "output_id": out_id,
        "date": today,
        "duration_s": tpl["default_duration_s"],
        "aspect": tpl["default_aspect"],
        "stages": [
            {"step": 1, "name": "TTS",            "tool": "elevenlabs (via fal.ai)", "estimated_cost_usd": 0.15, "estimated_time_s": 8},
            {"step": 2, "name": "STT/SRT",        "tool": "whisper (via fal.ai)",    "estimated_cost_usd": 0.01, "estimated_time_s": 5},
            {"step": 3, "name": "Image gen",      "tool": "flux-dev (creative-factory)", "estimated_cost_usd": tpl["slide_count"] * 0.025, "estimated_time_s": tpl["slide_count"] * 10},
            {"step": 4, "name": "Remotion render","tool": "remotion (local node)",   "estimated_cost_usd": 0,    "estimated_time_s": 60},
            {"step": 5, "name": "Crops",          "tool": "ffmpeg (local)",          "estimated_cost_usd": 0,    "estimated_time_s": 10},
        ],
    }
    plan["estimated_cost_total_usd"] = round(sum(s["estimated_cost_usd"] for s in plan["stages"]), 3)
    plan["estimated_time_total_s"] = sum(s["estimated_time_s"] for s in plan["stages"])

    # Save plan
    (out_dir / "plan.json").write_text(json.dumps(plan, indent=2, ensure_ascii=False))
    print(f"   ✓ plan.json salvo")
    print(f"   📊 Custo estimado: ${plan['estimated_cost_total_usd']}")
    print(f"   ⏱️  Tempo estimado: {plan['estimated_time_total_s']}s")

    if args.dry_run:
        print("\n🔬 DRY RUN — não vai chamar APIs externas")
        print("\nESTÁGIOS PLANEJADOS:")
        for s in plan["stages"]:
            print(f"   {s['step']}. {s['name']:<22} ({s['tool']}) — ${s['estimated_cost_usd']:.3f}, ~{s['estimated_time_s']}s")
        print(f"\n✅ Plano salvo em {out_dir / 'plan.json'}")
        print(f"   Pra rodar real: remover --dry-run e ter saldo na fal.ai")
        return 0

    # Real run — TODO: implementar quando saldo disponível
    print("\n⚠️  Run real ainda não implementado completamente.")
    print("    Próximas implementações:")
    print("    - core.elevenlabs_client.synthesize() → mp3")
    print("    - core.whisper_client.transcribe() → srt")
    print("    - creative-factory.pipelines.carousel_daily call por slide")
    print("    - core.remotion_runner.render() → mp4")
    return 0


if __name__ == "__main__":
    sys.exit(main())
