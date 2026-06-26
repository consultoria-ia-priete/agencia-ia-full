"""
brand_loader.py — carrega brand-profile.json + company.md do cliente atual.

Convenção: o cliente tem `<client_dir>/_opensquad/_memory/` com:
  - brand-profile.json  (estruturado, lido por scripts)
  - company.md          (narrativo, lido por agentes)

Valida placeholders não-substituídos pra evitar gerar criativo com `{{MARCA_PRINCIPAL}}`
literal no prompt.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Detecta placeholders {{X}} que sobraram (sinal de cliente não-provisionado)
PLACEHOLDER_RE = re.compile(r"\{\{[A-Z_]+\}\}")

# Campos do brand-profile.json que NÃO podem conter placeholder em produção
REQUIRED_RESOLVED_FIELDS = [
    ("client", "name"),
    ("brand", "main"),
    ("language", "publication"),
    ("publishing", "ghl_location_id"),
]


@dataclass
class BrandProfile:
    """Wrapper tipado em torno do brand-profile.json — campos planos pra acesso fácil."""
    raw: dict[str, Any] = field(default_factory=dict)
    company_md: str = ""
    client_dir: Path | None = None

    # ── Atalhos pra acesso comum ──────────────────────────
    @property
    def client_name(self) -> str:
        return self.raw.get("client", {}).get("name", "")

    @property
    def brand_main(self) -> str:
        return self.raw.get("brand", {}).get("main", "")

    @property
    def industry(self) -> str:
        return self.raw.get("brand", {}).get("industry", "")

    @property
    def publication_language(self) -> str:
        return self.raw.get("language", {}).get("publication", "pt-BR")

    @property
    def primary_color(self) -> str:
        return self.raw.get("visual_identity", {}).get("primary_color", "#000000")

    @property
    def secondary_color(self) -> str:
        return self.raw.get("visual_identity", {}).get("secondary_color", "#FFFFFF")

    @property
    def negative_visual_prompt(self) -> str:
        return self.raw.get("visual_identity", {}).get("negative_visual_prompt", "")

    @property
    def voice_tone(self) -> str:
        return self.raw.get("voice", {}).get("tone", "")

    @property
    def geo_country(self) -> str:
        return self.raw.get("geo", {}).get("country", "")

    @property
    def geo_state(self) -> str:
        return self.raw.get("geo", {}).get("state", "")

    @property
    def geo_cities(self) -> list[str]:
        return self.raw.get("geo", {}).get("cities_primary", [])

    @property
    def ghl_location_id(self) -> str:
        return self.raw.get("publishing", {}).get("ghl_location_id", "")

    @property
    def model_organic(self) -> str:
        return self.raw.get("creative_factory_defaults", {}).get("image_model_organic", "flux-dev")

    @property
    def model_ads(self) -> str:
        return self.raw.get("creative_factory_defaults", {}).get("image_model_ads", "flux-pro")

    @property
    def model_with_text(self) -> str:
        return self.raw.get("creative_factory_defaults", {}).get("image_model_with_text", "ideogram")

    @property
    def aspect_ratio_carousel(self) -> str:
        return self.raw.get("creative_factory_defaults", {}).get("aspect_ratio_carousel", "1:1")


def find_unresolved_placeholders(data: Any, path: str = "") -> list[tuple[str, str]]:
    """Anda recursivamente em dict/list/str e retorna [(json_path, placeholder)]."""
    findings: list[tuple[str, str]] = []
    if isinstance(data, dict):
        for k, v in data.items():
            findings.extend(find_unresolved_placeholders(v, f"{path}.{k}" if path else k))
    elif isinstance(data, list):
        for i, v in enumerate(data):
            findings.extend(find_unresolved_placeholders(v, f"{path}[{i}]"))
    elif isinstance(data, str):
        for match in PLACEHOLDER_RE.findall(data):
            findings.append((path, match))
    return findings


def load_brand(
    client_dir: str | Path,
    *,
    strict: bool = True,
) -> BrandProfile:
    """
    Carrega brand-profile.json + company.md de um cliente.

    Args:
        client_dir: path do cliente (ex: /Users/.../FLOOR_TO_CEILING)
        strict: se True, levanta exceção quando placeholders críticos não foram resolvidos.
                Em desenvolvimento, passe strict=False pra inspecionar.

    Returns:
        BrandProfile carregado.
    """
    client_path = Path(client_dir).expanduser().resolve()
    if not client_path.is_dir():
        raise FileNotFoundError(f"client_dir inválido: {client_path}")

    profile_path = client_path / "_opensquad" / "_memory" / "brand-profile.json"
    if not profile_path.is_file():
        raise FileNotFoundError(
            f"brand-profile.json não encontrado em {profile_path}. "
            "Provisione o cliente via sscia-sync ou copie o template."
        )

    with profile_path.open() as f:
        raw = json.load(f)

    company_path = client_path / "_opensquad" / "_memory" / "company.md"
    company_md = company_path.read_text() if company_path.is_file() else ""

    profile = BrandProfile(raw=raw, company_md=company_md, client_dir=client_path)

    # Validação: placeholders nos campos críticos
    if strict:
        critical_unresolved: list[str] = []
        for field_path in REQUIRED_RESOLVED_FIELDS:
            cur: Any = raw
            for k in field_path:
                cur = (cur or {}).get(k) if isinstance(cur, dict) else None
            if isinstance(cur, str) and PLACEHOLDER_RE.search(cur):
                critical_unresolved.append(f"{'.'.join(field_path)} = {cur!r}")

        if critical_unresolved:
            raise ValueError(
                "brand-profile.json tem placeholders críticos não substituídos:\n  - "
                + "\n  - ".join(critical_unresolved)
                + "\nProvisione o cliente corretamente antes de gerar criativos."
            )

    return profile


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python3 brand_loader.py <client_dir> [--strict|--lenient]")
        sys.exit(1)
    strict = "--lenient" not in sys.argv
    p = load_brand(sys.argv[1], strict=strict)
    print(f"✓ Cliente: {p.client_name}")
    print(f"  Marca:   {p.brand_main}")
    print(f"  Idioma:  {p.publication_language}")
    print(f"  Geo:     {p.geo_country} / {p.geo_state} / {p.geo_cities}")
    print(f"  Cores:   primary={p.primary_color} secondary={p.secondary_color}")
    print(f"  Modelos: organic={p.model_organic} ads={p.model_ads} text={p.model_with_text}")

    unresolved = find_unresolved_placeholders(p.raw)
    if unresolved:
        print(f"\n⚠️  {len(unresolved)} placeholders não-críticos restantes:")
        for path, ph in unresolved[:10]:
            print(f"  - {path}: {ph}")
