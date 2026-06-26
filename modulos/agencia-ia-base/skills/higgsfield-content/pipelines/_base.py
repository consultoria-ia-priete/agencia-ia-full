"""
_base.py — helper compartilhado entre os 4 pipelines ativos.

Fluxo padrão:
1. Parse args + load brand-profile
2. Validar content_engine
3. Resolver template + montar prompt
4. Calcular squad alvo + output_dir + manifest_id
5. Construir Higgsfield payload + estimar créditos
6. Salvar prompt.json + manifest.json (status='draft')
7. Imprimir CLAUDE INSTRUCTION (qual MCP chamar com quais args)
8. Sair com exit 0

Quando Claude executar o MCP e tiver a URL/path, o pipeline pode ser invocado de novo
com `--finalize --output-url URL --output-dir DIR` pra atualizar manifest + push pro worker.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CORE_DIR = Path(__file__).resolve().parent.parent / "core"
sys.path.insert(0, str(CORE_DIR))

from brand_loader import BrandProfile, load_brand, BrandLoadError, validate  # type: ignore[import-not-found]  # noqa: E402
from prompt_builder import PromptBundle, PromptBuildError, build  # type: ignore[import-not-found]  # noqa: E402
from manifest import (  # type: ignore[import-not-found]  # noqa: E402
    Manifest,
    make_id,
    output_dir,
    save_manifest,
    save_prompt,
    sha256_text,
)
from higgsfield_helper import (  # type: ignore[import-not-found]  # noqa: E402
    HiggsfieldImagePayload,
    HiggsfieldVideoPayload,
    build_image_payload,
    build_video_payload,
    claude_call_instructions,
    estimate_credits,
    validate_video_request,
)


def parse_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--client", required=True, help="slug do cliente (ex: floor-to-ceiling)")
    parser.add_argument("--template", required=True, help="nome do template (sem .yaml)")
    parser.add_argument("--param", action="append", default=[], help="key=value (repete)")
    parser.add_argument("--squad", help="override do squad dir (default deduzido do playbook)")
    parser.add_argument("--seed", type=int, help="seed Higgsfield (opcional)")
    parser.add_argument("--dry-run", action="store_true", help="só monta payload, não salva arquivos")
    parser.add_argument("--print-json", action="store_true", help="output em JSON estruturado")


def parse_params(param_kvs: list[str]) -> dict[str, str]:
    params: dict[str, str] = {}
    for kv in param_kvs:
        if "=" not in kv:
            raise SystemExit(f"--param malformado: {kv!r} (use key=value)")
        k, v = kv.split("=", 1)
        params[k.strip()] = v.strip()
    return params


def deduce_squad(brand: BrandProfile, override: str | None = None) -> str:
    if override:
        return override
    playbook = brand.content_engine.playbook
    if playbook == "cinematic-content":
        return "cinematic-content"
    if playbook == "viral-reels-seo":
        return "viral-reels-seo"
    return "video-content"


def load_brand_safe(slug: str, expected_playbook: str | None = None) -> BrandProfile:
    try:
        brand = load_brand(slug)
    except BrandLoadError as e:
        print(f"[ERRO brand] {e}", file=sys.stderr)
        raise SystemExit(1)

    issues = validate(brand, expected_playbook=expected_playbook)
    if issues:
        print(f"[ERRO content_engine] {brand.slug} tem problemas:", file=sys.stderr)
        for i in issues:
            print(f"  ✗ {i}", file=sys.stderr)
        raise SystemExit(2)
    return brand


def build_prompt_safe(template: str, brand: BrandProfile, params: dict[str, str]) -> PromptBundle:
    try:
        return build(template, brand, params=params)
    except PromptBuildError as e:
        print(f"[ERRO prompt] {e}", file=sys.stderr)
        raise SystemExit(3)


def run_video_pipeline(
    args: argparse.Namespace,
    *,
    expected_playbook: str | None,
    default_model: str | None = None,
) -> int:
    """Fluxo padrão pra geração de VÍDEO."""
    brand = load_brand_safe(args.client, expected_playbook=expected_playbook)
    params = parse_params(args.param)
    bundle = build_prompt_safe(args.template, brand, params)

    model = bundle.model or default_model or brand.content_engine.higgsfield_default_video_model
    duration = bundle.duration or 7

    payload = build_video_payload(
        prompt=bundle.final_prompt,
        model=model,
        duration=duration,
        aspect_ratio=bundle.aspect_ratio,
        seed=args.seed,
    )
    issues = validate_video_request(payload)
    if issues:
        print(f"[ERRO payload] {issues}", file=sys.stderr)
        return 4

    credits = estimate_credits(model)

    return _emit(args, brand, bundle, payload, credits, kind="video")


def run_image_pipeline(
    args: argparse.Namespace,
    *,
    expected_playbook: str | None,
    default_model: str | None = None,
    num_images: int = 1,
) -> int:
    """Fluxo padrão pra geração de IMAGEM."""
    brand = load_brand_safe(args.client, expected_playbook=expected_playbook)
    params = parse_params(args.param)
    bundle = build_prompt_safe(args.template, brand, params)

    model = bundle.model or default_model or brand.content_engine.higgsfield_default_image_model

    payload = build_image_payload(
        prompt=bundle.final_prompt,
        model=model,
        aspect_ratio=bundle.aspect_ratio,
        seed=args.seed,
        num_images=num_images,
    )
    credits = estimate_credits(model, count=num_images)

    return _emit(args, brand, bundle, payload, credits, kind="image")


def _emit(
    args: argparse.Namespace,
    brand: BrandProfile,
    bundle: PromptBundle,
    payload: HiggsfieldVideoPayload | HiggsfieldImagePayload,
    credits: int,
    *,
    kind: str,
) -> int:
    squad = deduce_squad(brand, args.squad)
    manifest_id = make_id(args.id_prefix)
    date = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

    if args.dry_run:
        out_dir = None
        prompt_path = None
        manifest_path = None
    else:
        out_dir = output_dir(brand.client_dir, squad, date=date, manifest_id=manifest_id)
        prompt_path = save_prompt(out_dir, {
            "template_name": bundle.template_name,
            "template_path": str(bundle.template_path),
            "final_prompt": bundle.final_prompt,
            "params_used": bundle.params_used,
            "validations_applied": bundle.validations_applied,
            "duration": bundle.duration,
            "aspect_ratio": bundle.aspect_ratio,
            "model": bundle.model,
        })

        manifest = Manifest(
            id=manifest_id,
            slug=brand.slug,
            squad=squad,
            date=date,
            playbook=brand.content_engine.playbook,
            sub_playbook=brand.content_engine.sub_playbook,
            template_name=bundle.template_name,
            model=bundle.model,
            duration_s=bundle.duration,
            aspect_ratio=bundle.aspect_ratio,
            prompt_final=bundle.final_prompt,
            params_used=bundle.params_used,
            validations_applied=bundle.validations_applied,
            brand_profile_hash=sha256_text(json.dumps(brand.raw, sort_keys=True, ensure_ascii=False)),
            created_at=datetime.now(tz=timezone.utc).isoformat(),
            credits_estimate=credits,
            seed=args.seed,
            status="draft",
        )
        manifest_path = save_manifest(out_dir, manifest)

    instructions = claude_call_instructions(payload)

    if args.print_json:
        out: dict[str, Any] = {
            "manifest_id": manifest_id,
            "client": brand.slug,
            "client_dir": brand.client_dir,
            "squad": squad,
            "date": date,
            "kind": kind,
            "template": bundle.template_name,
            "model": payload.model,
            "aspect_ratio": payload.aspect_ratio,
            "credits_estimate": credits,
            "prompt_final": bundle.final_prompt,
            "mcp_call": {
                "tool": f"mcp__claude_ai_Higgsfield__generate_{kind}",
                "arguments": payload.to_mcp_args(),
            },
            "output_dir": str(out_dir) if out_dir else None,
            "prompt_path": str(prompt_path) if prompt_path else None,
            "manifest_path": str(manifest_path) if manifest_path else None,
        }
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print(f"=== higgsfield-content pipeline ({kind}) ===")
        print(f"Manifest ID:  {manifest_id}")
        print(f"Client:       {brand.slug} ({brand.client_dir})")
        print(f"Squad:        {squad}")
        print(f"Template:     {bundle.template_name}")
        print(f"Model:        higgsfield/{payload.model}")
        print(f"Aspect:       {payload.aspect_ratio}")
        print(f"Duration:     {bundle.duration}s" if bundle.duration else "Duration:     (image)")
        print(f"Validations:  {bundle.validations_applied}")
        print(f"Credits est.: {credits}")
        if out_dir:
            print(f"Output dir:   {out_dir}")
        print()
        print(instructions)

    return 0
