#!/usr/bin/env python3
"""
carousel_daily.py — pipeline ponta-a-ponta de geração de carrossel.

Recebe:
  --client <PATH>      pasta do cliente (lê brand-profile.json + company.md)
  --template <NAME>    nome do template (ex: cleaning_before_after)
  --brief "<TEMA>"     briefing livre do operador
  [--output-id <ID>]   ID amigável (ex: C01). default: timestamp
  [--dry-run]          não chama fal.ai — só monta prompts e gera preview com placeholders
  [--max-parallel N]   slides em flight ao mesmo tempo (default 5)

Saída:
  <client>/squads/conteudo-viral/output/criativos/<YYYY-MM-DD>_<output_id>/
    ├── prompts.json     prompts finais usados pra cada slide
    ├── slide-{id}.jpg   imagens baixadas (em produção)
    ├── manifest.json    metadados de geração (model, seed, custo, elapsed)
    └── preview.html     preview visual (regra do ecossistema)

Smoke test:
  python3 carousel_daily.py --client /Users/.../FLOOR_TO_CEILING \\
    --template cleaning_before_after --brief "deep cleaning before spring" --dry-run
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

# Permite rodar como script: python3 carousel_daily.py
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from core.brand_loader import load_brand  # noqa: E402
from core.prompt_builder import build_carousel_prompts  # noqa: E402
from core.preview import render_preview  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--client", required=True, help="path da pasta do cliente")
    p.add_argument("--template", required=True, help="nome do template (sem extensão)")
    p.add_argument("--brief", default="", help="briefing livre do operador")
    p.add_argument("--output-id", default="", help="ID curto pro output (ex: C01)")
    p.add_argument("--dry-run", action="store_true", help="não chama fal.ai — só prompts + preview")
    p.add_argument("--max-parallel", type=int, default=5)
    p.add_argument("--strict", action="store_true",
                   help="exige brand-profile sem placeholders críticos (default: False)")
    return p.parse_args()


def download(url: str, dest: Path) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=60) as r, dest.open("wb") as f:
            f.write(r.read())
        return True
    except Exception as exc:
        print(f"  ⚠️  falha ao baixar {url}: {exc}", file=sys.stderr)
        return False


def main() -> int:
    args = parse_args()
    started = time.time()

    print(f"📂 Carregando brand do cliente: {args.client}")
    brand = load_brand(args.client, strict=args.strict)
    print(f"   ✓ Cliente:  {brand.client_name}")
    print(f"   ✓ Marca:    {brand.brand_main}")
    print(f"   ✓ Idioma:   {brand.publication_language}")
    print(f"   ✓ Geo:      {brand.geo_country}/{brand.geo_state} {brand.geo_cities}")

    print(f"\n📋 Carregando template: {args.template}")
    meta, prompts = build_carousel_prompts(args.template, brand, args.brief)
    print(f"   ✓ Template: {meta.get('template')} v{meta.get('version')}")
    print(f"   ✓ Slides:   {len(prompts)}")

    # Pasta de output
    today = datetime.now().strftime("%Y-%m-%d")
    output_id = args.output_id or datetime.now().strftime("%H%M")
    out_dir = (
        Path(args.client).expanduser().resolve()
        / "squads" / "conteudo-viral" / "output" / "criativos"
        / f"{today}_{output_id}"
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n📁 Output: {out_dir}")

    # Salva prompts.json (auditável)
    prompts_dump = [
        {
            "slide_id": p.slide_id,
            "slide_type": p.slide_type,
            "model": p.model,
            "aspect": p.aspect,
            "image_size": p.image_size,
            "visual_prompt": p.visual_prompt,
            "text_overlay": p.text_overlay,
            "caption": p.caption,
        }
        for p in prompts
    ]
    (out_dir / "prompts.json").write_text(
        json.dumps(prompts_dump, indent=2, ensure_ascii=False)
    )
    print(f"   ✓ prompts.json salvo")

    # Geração (real ou dry-run)
    slides_meta: list[dict] = []
    if args.dry_run:
        print("\n🔬 DRY RUN — não vai chamar fal.ai")
        for p in prompts:
            slides_meta.append({
                "slide_id": p.slide_id,
                "slide_type": p.slide_type,
                "image_url": "",
                "text_overlay": p.text_overlay,
                "caption": p.caption,
                "model": p.model,
                "aspect": p.aspect,
                "elapsed_s": 0.0,
                "cost_estimate_usd": 0.0,
                "error": "DRY RUN",
            })
    else:
        # Import só agora pra dry-run não depender da FAL_KEY/SDK
        from core.fal_client import generate_batch  # noqa
        print(f"\n⏳ Gerando {len(prompts)} imagens via fal.ai (paralelo={args.max_parallel})...")
        requests = [
            {
                "slide_id": p.slide_id,
                "model": p.model,
                "prompt": p.visual_prompt,
                "image_size": p.image_size,
            }
            for p in prompts
        ]
        results = generate_batch(requests, max_parallel=args.max_parallel)
        for p, r in zip(prompts, results):
            local_path = ""
            if r.ok and r.image_url:
                local_path = str(out_dir / f"slide-{p.slide_id}.jpg")
                download(r.image_url, Path(local_path))
                status_icon = "✓"
            else:
                status_icon = "✗"
            print(f"   {status_icon} slide {p.slide_id} ({p.slide_type}) — {r.elapsed_s}s — {r.error or 'OK'}")
            slides_meta.append({
                "slide_id": p.slide_id,
                "slide_type": p.slide_type,
                "image_url": r.image_url or "",
                "local_path": local_path,
                "text_overlay": p.text_overlay,
                "caption": p.caption,
                "model": p.model,
                "aspect": p.aspect,
                "elapsed_s": r.elapsed_s,
                "cost_estimate_usd": r.cost_estimate_usd,
                "seed": r.seed,
                "error": r.error,
            })

    # Manifest
    manifest = {
        "client": brand.client_name,
        "brand_main": brand.brand_main,
        "language": brand.publication_language,
        "template": args.template,
        "brief": args.brief,
        "output_id": output_id,
        "date": today,
        "dry_run": args.dry_run,
        "total_elapsed_s": round(time.time() - started, 2),
        "total_cost_estimate_usd": sum(s.get("cost_estimate_usd", 0) for s in slides_meta),
        "slides": slides_meta,
    }
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False, default=str)
    )

    # Preview HTML
    preview_path = render_preview(
        title=f"{brand.brand_main} — {args.template} — {output_id}",
        output_path=out_dir / "preview.html",
        client_name=brand.client_name,
        brand_main=brand.brand_main,
        language=brand.publication_language,
        template_name=args.template,
        brief=args.brief or "(sem briefing)",
        output_dir=str(out_dir),
        slides=slides_meta,
    )

    print(f"\n✅ Concluído em {manifest['total_elapsed_s']}s")
    print(f"   Custo estimado: ${manifest['total_cost_estimate_usd']:.3f}")
    print(f"   Preview:        {preview_path}")
    print(f"   Abrir no Mac:   open '{preview_path}'")

    return 0


if __name__ == "__main__":
    sys.exit(main())
