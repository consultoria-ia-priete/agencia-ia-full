"""
multi_platform_post.py — Publicação multi-plataforma (IG + FB + GMB) via CRM Funnels.

Diferente do create_post.py legado (que aceita 1 plataforma por vez e usa
credenciais hardcoded do Alex), este snippet:

  1. Lê credenciais do .mcp.json e accountIds do brand-profile.json do CLIENTE
  2. Aceita lista de plataformas em 1 chamada
  3. Splita automaticamente Instagram/Facebook (carrossel ok) vs GMB (1 imagem + CTA button)
  4. Trata caption-truncation pra GMB (limite ~1500 chars)
  5. Adiciona callToAction button pro GMB se brand-profile fornecer
  6. Suporta --dry-run via parâmetro pra inspecionar payload sem publicar

Uso programático:
    from multi_platform_post import publish_multi
    res = publish_multi(
        client_dir="/Users/.../FLOOR_TO_CEILING",
        platforms=["instagram", "facebook", "google_business_profile"],
        image_urls=["https://...slide-01.jpg", "https://...slide-02.jpg", ...],
        caption="...",
        gmb_cta={"action": "BOOK", "url": "https://floortoceilingcleanings.com/book"},
        dry_run=False,
    )
"""
from __future__ import annotations

import json
import ssl
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

BASE_URL = "https://services.leadconnectorhq.com"

# Limite de caption por plataforma (validado em produção)
PLATFORM_CAPTION_LIMITS = {
    "instagram": 2200,
    "facebook": 63206,
    "google_business_profile": 1500,
    "linkedin": 3000,
}

# Plataformas que aceitam carrossel (>1 imagem em 1 post)
CAROUSEL_PLATFORMS = {"instagram", "facebook", "linkedin"}

# Plataformas que SEMPRE precisam de 1 imagem só
SINGLE_IMAGE_PLATFORMS = {"google_business_profile"}

# Action types válidos pro GMB callToAction
GMB_VALID_ACTIONS = {"BOOK", "ORDER", "SHOP", "LEARN_MORE", "SIGN_UP", "CALL"}


# ════════════════════════════════════════════════════════════════════════════
# Modelo
# ════════════════════════════════════════════════════════════════════════════

@dataclass
class PostResult:
    request_payload: dict
    response: dict | None = None
    error: str | None = None
    dry_run: bool = False
    platforms_in_request: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        if self.dry_run:
            return self.error is None
        return self.error is None and self.response is not None


@dataclass
class MultiPostResult:
    results: list[PostResult]
    client_name: str = ""
    platforms_requested: list[str] = field(default_factory=list)
    platforms_published: list[str] = field(default_factory=list)
    platforms_skipped: list[str] = field(default_factory=list)
    total_requests: int = 0

    @property
    def all_ok(self) -> bool:
        return all(r.ok for r in self.results)


# ════════════════════════════════════════════════════════════════════════════
# Credentials loader (lê do cliente, não hardcoded)
# ════════════════════════════════════════════════════════════════════════════

def load_client_creds(client_dir: str | Path) -> dict[str, Any]:
    """
    Lê credenciais e accountIds do cliente.

    Returns dict com:
        api_key:   CRM Funnels pit-... (de .mcp.json)
        location_id: CRM Funnels location (de .mcp.json E brand-profile.json devem coincidir)
        user_id:   CRM Funnels user_id (de _opensquad/_memory/ghl-credentials.md ou inferido)
        account_ids: dict {platform: id} (de brand-profile.json)
        default_cta: dict ou string (de brand-profile.json)
    """
    cdir = Path(client_dir).expanduser().resolve()

    # .mcp.json — CRM Funnels key + location
    mcp_path = cdir / ".mcp.json"
    if not mcp_path.is_file():
        raise FileNotFoundError(f"{mcp_path} não existe — provisionar cliente antes de publicar.")
    mcp = json.loads(mcp_path.read_text())
    ghl_env = mcp.get("mcpServers", {}).get("gohighlevel", {}).get("env", {})
    api_key = ghl_env.get("GHL_API_KEY", "")
    location_id = ghl_env.get("GHL_LOCATION_ID", "")
    if not api_key or not location_id:
        raise ValueError(f"GHL_API_KEY ou GHL_LOCATION_ID faltando em {mcp_path}")

    # brand-profile.json — accountIds e defaults
    bp_path = cdir / "_opensquad" / "_memory" / "brand-profile.json"
    if not bp_path.is_file():
        raise FileNotFoundError(f"{bp_path} não existe.")
    bp = json.loads(bp_path.read_text())

    pub = bp.get("publishing", {}) or {}
    account_ids = pub.get("ghl_account_ids", {}) or {}

    # user_id: tentar buscar em ghl-credentials.md (legacy) — senão deixa vazio
    user_id = ""
    ghl_md = cdir / "_opensquad" / "_memory" / "ghl-credentials.md"
    if ghl_md.is_file():
        for line in ghl_md.read_text().splitlines():
            if "user_id" in line.lower() or "userid" in line.lower() or "USER_ID" in line:
                # pega próximo token grande alfanumérico
                import re
                m = re.search(r"\b[a-zA-Z0-9]{15,}\b", line)
                if m:
                    user_id = m.group(0)
                    break

    return {
        "client_dir": cdir,
        "client_name": bp.get("client", {}).get("name", cdir.name),
        "api_key": api_key,
        "location_id": location_id,
        "user_id": user_id,
        "account_ids": account_ids,
        "default_cta": pub.get("default_cta", ""),
        "post_signature": pub.get("post_signature", ""),
        "websites_primary": (bp.get("websites", {}) or {}).get("primary", ""),
        "language": (bp.get("language", {}) or {}).get("publication", "en-US"),
    }


# ════════════════════════════════════════════════════════════════════════════
# HTTP helper
# ════════════════════════════════════════════════════════════════════════════

def _http_post(api_key: str, path: str, payload: dict) -> dict:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Version": "2021-07-28",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
    }
    url = BASE_URL + path
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method="POST", headers=headers)
    ctx = ssl._create_unverified_context()
    try:
        r = urllib.request.urlopen(req, context=ctx, timeout=60)
        raw = r.read().decode()
        return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {body}") from e


# ════════════════════════════════════════════════════════════════════════════
# Caption helpers
# ════════════════════════════════════════════════════════════════════════════

def truncate_caption(caption: str, limit: int) -> str:
    """Trunca preservando palavra inteira e adiciona reticências."""
    if len(caption) <= limit:
        return caption
    cut = caption[:limit - 3]
    last_space = cut.rfind(" ")
    if last_space > limit * 0.7:
        cut = cut[:last_space]
    return cut + "..."


def append_signature(caption: str, signature: str) -> str:
    if not signature:
        return caption
    if signature in caption:
        return caption
    return f"{caption}\n\n{signature}"


# ════════════════════════════════════════════════════════════════════════════
# Payload builders por platform-group
# ════════════════════════════════════════════════════════════════════════════

def build_carousel_payload(
    *,
    user_id: str,
    account_ids: list[str],
    image_urls: list[str],
    caption: str,
) -> dict:
    """Payload pra IG + FB + LinkedIn (aceitam carrossel)."""
    return {
        "type": "post",
        **({"userId": user_id} if user_id else {}),
        "accountIds": account_ids,
        "media": [{"url": u, "type": "image/jpeg"} for u in image_urls],
        "summary": caption,
        "status": "published",
    }


def build_gmb_payload(
    *,
    user_id: str,
    gmb_account_id: str,
    image_url: str,
    caption: str,
    cta: dict | None = None,
) -> dict:
    """
    Payload pra Google Business Profile.

    GMB difere de IG/FB:
      - Aceita SOMENTE 1 imagem (passamos a primeira/hero)
      - Suporta callToAction com action button
      - Caption limit 1500 chars
    """
    payload: dict[str, Any] = {
        "type": "post",
        **({"userId": user_id} if user_id else {}),
        "accountIds": [gmb_account_id],
        "media": [{"url": image_url, "type": "image/jpeg"}],
        "summary": caption,
        "status": "published",
    }
    if cta:
        action = cta.get("action", "").upper()
        if action not in GMB_VALID_ACTIONS:
            raise ValueError(
                f"GMB CTA action inválido: {action!r}. "
                f"Use um de: {sorted(GMB_VALID_ACTIONS)}"
            )
        url = cta.get("url", "")
        if not url and action != "CALL":
            raise ValueError("GMB CTA precisa de 'url' (exceto CALL).")
        payload["googleMyBusiness"] = {
            "callToAction": {"actionType": action, "url": url},
        }
    return payload


# ════════════════════════════════════════════════════════════════════════════
# Função principal
# ════════════════════════════════════════════════════════════════════════════

def publish_multi(
    *,
    client_dir: str | Path,
    platforms: list[str],
    image_urls: list[str],
    caption: str,
    gmb_cta: dict | None = None,
    append_brand_signature: bool = True,
    dry_run: bool = False,
) -> MultiPostResult:
    """
    Publica em múltiplas plataformas simultaneamente, splittando automaticamente
    quando GMB está envolvido.

    Args:
        client_dir: path raiz do cliente (lê .mcp.json e brand-profile.json)
        platforms:  lista de plataformas (chaves do brand-profile.publishing.ghl_account_ids)
                    Ex: ["instagram", "facebook", "google_business_profile"]
        image_urls: lista de URLs públicas (preferir CRM Funnels CDN). Carrossel se >1; GMB usa só a 1ª.
        caption:    texto base do post
        gmb_cta:    dict opcional {"action": "BOOK"|..., "url": "..."} pra botão GMB
        append_brand_signature: se True, adiciona post_signature do brand-profile no final
        dry_run:    se True, só monta payloads e retorna — não chama API

    Returns:
        MultiPostResult com .results (1 ou 2 PostResult dependendo se GMB tá envolvido)
    """
    creds = load_client_creds(client_dir)

    # Resolve accountIds + filtra plataformas habilitadas
    requested = list(platforms)
    resolved: dict[str, str] = {}
    skipped: list[str] = []
    for p in requested:
        aid = creds["account_ids"].get(p, "")
        if aid:
            resolved[p] = aid
        else:
            skipped.append(p)

    if not resolved:
        raise ValueError(
            f"Nenhuma plataforma resolvida. Solicitadas: {requested}. "
            f"Verifique brand-profile.json → publishing.ghl_account_ids."
        )

    # Caption final
    final_caption = append_signature(caption, creds["post_signature"]) if append_brand_signature else caption

    # Split: GMB precisa de request separado
    gmb_id = resolved.pop("google_business_profile", None)
    carousel_ids = list(resolved.values())

    results: list[PostResult] = []
    published_platforms: list[str] = []

    # ── Request 1: IG + FB + LinkedIn (carrossel) ─────────────────
    if carousel_ids:
        plat_in_req = [p for p in resolved.keys()]
        # Truncar caption pra menor limit das plataformas
        limit = min(PLATFORM_CAPTION_LIMITS.get(p, 2200) for p in plat_in_req)
        cap = truncate_caption(final_caption, limit)
        payload = build_carousel_payload(
            user_id=creds["user_id"],
            account_ids=carousel_ids,
            image_urls=image_urls,
            caption=cap,
        )
        res = PostResult(
            request_payload=payload,
            dry_run=dry_run,
            platforms_in_request=plat_in_req,
        )
        if not dry_run:
            try:
                res.response = _http_post(
                    creds["api_key"],
                    f"/social-media-posting/{creds['location_id']}/posts",
                    payload,
                )
                published_platforms.extend(plat_in_req)
            except Exception as exc:
                res.error = str(exc)
        else:
            published_platforms.extend(plat_in_req)
        results.append(res)

    # ── Request 2: GMB (1 imagem + opcional CTA) ──────────────────
    if gmb_id:
        if not image_urls:
            raise ValueError("GMB precisa de pelo menos 1 image_url.")
        cap_gmb = truncate_caption(final_caption, PLATFORM_CAPTION_LIMITS["google_business_profile"])
        # Se CTA não passou explícito, tenta inferir do brand-profile
        cta = gmb_cta
        if cta is None and creds.get("default_cta"):
            primary_url = creds.get("websites_primary", "")
            if primary_url:
                cta = {"action": "BOOK", "url": primary_url}
        payload = build_gmb_payload(
            user_id=creds["user_id"],
            gmb_account_id=gmb_id,
            image_url=image_urls[0],
            caption=cap_gmb,
            cta=cta,
        )
        res = PostResult(
            request_payload=payload,
            dry_run=dry_run,
            platforms_in_request=["google_business_profile"],
        )
        if not dry_run:
            try:
                res.response = _http_post(
                    creds["api_key"],
                    f"/social-media-posting/{creds['location_id']}/posts",
                    payload,
                )
                published_platforms.append("google_business_profile")
            except Exception as exc:
                res.error = str(exc)
        else:
            published_platforms.append("google_business_profile")
        results.append(res)

    return MultiPostResult(
        results=results,
        client_name=creds["client_name"],
        platforms_requested=requested,
        platforms_published=published_platforms,
        platforms_skipped=skipped,
        total_requests=len(results),
    )


# ════════════════════════════════════════════════════════════════════════════
# CLI mínimo (smoke test)
# ════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--client", required=True, help="path do cliente")
    p.add_argument("--platforms", required=True, help="vírgula-separado (ex: instagram,facebook,google_business_profile)")
    p.add_argument("--image-url", action="append", required=True, help="URL pública (use múltiplas vezes)")
    p.add_argument("--caption", required=True)
    p.add_argument("--gmb-action", help="GMB CTA action (BOOK, LEARN_MORE, ...)")
    p.add_argument("--gmb-url", help="GMB CTA url")
    p.add_argument("--dry-run", action="store_true", default=True, help="default True pra evitar publicação acidental")
    p.add_argument("--no-dry-run", action="store_true", help="explicitamente publica de verdade")
    args = p.parse_args()

    dry = not args.no_dry_run

    cta = None
    if args.gmb_action:
        cta = {"action": args.gmb_action, "url": args.gmb_url or ""}

    out = publish_multi(
        client_dir=args.client,
        platforms=[p.strip() for p in args.platforms.split(",")],
        image_urls=args.image_url,
        caption=args.caption,
        gmb_cta=cta,
        dry_run=dry,
    )

    print(f"Cliente: {out.client_name}")
    print(f"Solicitadas: {out.platforms_requested}")
    print(f"Publicadas:  {out.platforms_published}")
    print(f"Puladas:     {out.platforms_skipped}")
    print(f"Requests:    {out.total_requests} ({'DRY RUN' if dry else 'REAL'})")
    for i, r in enumerate(out.results, 1):
        print(f"\n── Request {i} (platforms: {r.platforms_in_request}) ──")
        if r.error:
            print(f"  ✗ ERROR: {r.error}")
        else:
            print(f"  ✓ {'(payload mounted)' if dry else 'OK'}")
        print("  Payload:")
        print(json.dumps(r.request_payload, indent=2, ensure_ascii=False)[:500] + "...")

    sys.exit(0 if out.all_ok else 1)
