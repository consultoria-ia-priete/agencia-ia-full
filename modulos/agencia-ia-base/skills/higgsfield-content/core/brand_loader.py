"""
brand_loader.py — carrega brand-profile.json de um cliente e valida content_engine.

Uso CLI:
    python brand_loader.py --client floor-to-ceiling --validate

Uso programático:
    from brand_loader import load_brand, BrandProfile
    brand = load_brand("floor-to-ceiling")
    print(brand.content_engine.group)  # "B"
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

PROJETOS_ROOT = Path.home() / "Documents" / "PROJETOS_CLAUDE_CODE"

SLUG_TO_DIR = {
    "ballarin-sou-viver-milao": "BALLARIN_SOU_VIVER_MILAO",
    "investbens-residencial-serraria": "INVESTBENS_RESIDENCIAL_SERRARIA",
    "floor-to-ceiling": "FLOOR_TO_CEILING",
    "mendes-flooring": "MENDES_FLOORING",
    "jrs-flooring": "JRS_FLOORING",
    "alex-sscia": "ALEX_SSCIA",
}

VALID_GROUPS = {"A", "B", "B-prime"}
VALID_PLAYBOOKS = {"cinematic-content", "viral-reels-seo"}


class BrandLoadError(RuntimeError):
    pass


@dataclass
class ContentEngine:
    group: str
    playbook: str
    sub_playbook: str
    video_cadence_per_week: int
    image_cadence_per_week: int
    higgsfield_default_video_model: str
    higgsfield_default_image_model: str
    use_soul_avatar: bool
    carousel_canon: bool
    editorial_line: str
    ads_enabled: bool
    ad_creative_aspect_ratios: list[str]
    ads_cadence_per_week: int
    video_editor_pipeline: str
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class BrandProfile:
    slug: str
    client_dir: str
    path: Path
    raw: dict[str, Any]
    content_engine: ContentEngine

    @property
    def language(self) -> str:
        return self.raw.get("language", {}).get("publication", "pt-BR")

    @property
    def ghl_location_id(self) -> str:
        return self.raw.get("publishing", {}).get("ghl_location_id", "")

    @property
    def default_platforms(self) -> list[str]:
        return self.raw.get("publishing", {}).get("default_platforms", [])

    @property
    def primary_keywords(self) -> list[str]:
        return self.raw.get("seo", {}).get("primary_keywords", [])

    @property
    def cities_primary(self) -> list[str]:
        return self.raw.get("geo", {}).get("cities_primary", [])

    @property
    def voice_tone(self) -> str:
        return self.raw.get("voice", {}).get("tone", "")

    @property
    def default_cta(self) -> str:
        return self.raw.get("publishing", {}).get("default_cta", "")

    @property
    def hashtags_default(self) -> list[str]:
        return self.raw.get("publishing", {}).get("hashtags_default", [])


def resolve_client_dir(slug: str) -> str:
    if slug in SLUG_TO_DIR:
        return SLUG_TO_DIR[slug]
    upper_slug = slug.upper().replace("-", "_")
    if (PROJETOS_ROOT / upper_slug).exists():
        return upper_slug
    raise BrandLoadError(f"Não consegui resolver slug → diretório: {slug!r}. Conhecidos: {sorted(SLUG_TO_DIR)}")


def load_brand(slug: str) -> BrandProfile:
    client_dir = resolve_client_dir(slug)
    path = PROJETOS_ROOT / client_dir / "_opensquad" / "_memory" / "brand-profile.json"
    if not path.exists():
        raise BrandLoadError(f"brand-profile.json não existe em {path}")

    raw = json.loads(path.read_text(encoding="utf-8"))
    ce_raw = raw.get("content_engine")
    if not ce_raw:
        raise BrandLoadError(
            f"{slug}: campo `content_engine` ausente no brand-profile. "
            "Rode a migração da Fase 1 antes de gerar conteúdo."
        )

    ce = ContentEngine(
        group=ce_raw.get("group", ""),
        playbook=ce_raw.get("playbook", ""),
        sub_playbook=ce_raw.get("sub_playbook", ""),
        video_cadence_per_week=int(ce_raw.get("video_cadence_per_week", 0) or 0),
        image_cadence_per_week=int(ce_raw.get("image_cadence_per_week", 0) or 0),
        higgsfield_default_video_model=ce_raw.get("higgsfield_default_video_model", "dop"),
        higgsfield_default_image_model=ce_raw.get("higgsfield_default_image_model", "nano-banana-2k"),
        use_soul_avatar=bool(ce_raw.get("use_soul_avatar", False)),
        carousel_canon=bool(ce_raw.get("carousel_canon", False)),
        editorial_line=ce_raw.get("editorial_line", "TBD"),
        ads_enabled=bool(ce_raw.get("ads_enabled", False)),
        ad_creative_aspect_ratios=list(ce_raw.get("ad_creative_aspect_ratios", ["9:16", "1:1", "4:5"])),
        ads_cadence_per_week=int(ce_raw.get("ads_cadence_per_week", 0) or 0),
        video_editor_pipeline=ce_raw.get("video_editor_pipeline", "default"),
        raw=ce_raw,
    )

    return BrandProfile(
        slug=slug,
        client_dir=client_dir,
        path=path,
        raw=raw,
        content_engine=ce,
    )


def validate(brand: BrandProfile, expected_playbook: str | None = None) -> list[str]:
    """Retorna lista de problemas. Lista vazia = ok pra gerar."""
    issues: list[str] = []
    ce = brand.content_engine

    if not ce.group:
        issues.append("content_engine.group vazio — cliente não tem grupo definido")
    elif ce.group not in VALID_GROUPS:
        issues.append(f"content_engine.group={ce.group!r} inválido. Esperado: {sorted(VALID_GROUPS)}")

    if not ce.playbook:
        issues.append("content_engine.playbook vazio")
    elif ce.playbook not in VALID_PLAYBOOKS:
        issues.append(f"content_engine.playbook={ce.playbook!r} inválido. Esperado: {sorted(VALID_PLAYBOOKS)}")

    if expected_playbook and ce.playbook != expected_playbook:
        issues.append(
            f"Playbook do brand-profile ({ce.playbook!r}) não casa com playbook esperado pelo pipeline ({expected_playbook!r})"
        )

    if not brand.ghl_location_id:
        issues.append("publishing.ghl_location_id vazio — precisa antes de publicar")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspeciona brand-profile + content_engine")
    parser.add_argument("--client", required=True, help="slug do cliente (ex: floor-to-ceiling)")
    parser.add_argument("--validate", action="store_true", help="rodar checks")
    parser.add_argument("--expected-playbook", help="comparar com playbook esperado")
    args = parser.parse_args()

    try:
        brand = load_brand(args.client)
    except BrandLoadError as e:
        print(f"[ERRO] {e}", file=sys.stderr)
        return 1

    ce = brand.content_engine
    print(f"Slug:       {brand.slug}")
    print(f"Dir:        {brand.client_dir}")
    print(f"Path:       {brand.path}")
    print(f"Language:   {brand.language}")
    print(f"CRM Funnels loc:    {brand.ghl_location_id or '(vazio)'}")
    print(f"Group:      {ce.group}")
    print(f"Playbook:   {ce.playbook}")
    print(f"Sub-play:   {ce.sub_playbook or '(nenhum)'}")
    print(f"Cad. vídeo: {ce.video_cadence_per_week}/sem")
    print(f"Cad. img:   {ce.image_cadence_per_week}/sem")
    print(f"Modelo vid: higgsfield/{ce.higgsfield_default_video_model}")
    print(f"Modelo img: higgsfield/{ce.higgsfield_default_image_model}")
    print(f"Ads:        {'on' if ce.ads_enabled else 'off'} ({ce.ads_cadence_per_week}/sem)")
    print(f"Carr canon: {'YES (não mexer)' if ce.carousel_canon else 'no'}")
    print(f"Soul avatar:{'on' if ce.use_soul_avatar else 'reservado'}")
    print(f"Edit line:  {ce.editorial_line}")

    if args.validate:
        issues = validate(brand, expected_playbook=args.expected_playbook)
        if issues:
            print("\n[VALIDAÇÃO] problemas:")
            for i in issues:
                print(f"  ✗ {i}")
            return 2
        print("\n[VALIDAÇÃO] ✓ ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
