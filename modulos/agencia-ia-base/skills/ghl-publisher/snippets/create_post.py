"""
create_post.py — Criar/agendar post social no CRM Funnels.

Suporta:
  • Carrossel (múltiplas imagens) ou single image
  • Publicação imediata (status="published") — RECOMENDADO
  • Agendamento (status="scheduled" + scheduleDate)

Uso programático:
    from create_post import create_immediate_post, create_scheduled_post
    res = create_immediate_post("instagram", urls, caption)
"""
from datetime import datetime, timedelta, timezone
from _common import LOC, USER_ID, IG_ID, LI_ID, http_request


PLATFORMS = {
    "instagram": IG_ID,
    "linkedin": LI_ID,
}


def create_immediate_post(platform: str, image_urls: list[str], caption: str) -> dict:
    """Publica imediatamente. RECOMENDADO sobre scheduled (evita bug platform=google).

    Args:
        platform: "instagram" ou "linkedin"
        image_urls: lista de URLs públicas (preferir CRM Funnels CDN — assets.cdn.filesafe.space)
        caption: texto do post (até ~2200 chars)

    Returns:
        dict com response da API. Atenção: NÃO inclui o ID do post.
        Use list_posts() depois para localizar o post recém-criado.
    """
    account_id = PLATFORMS.get(platform)
    if not account_id:
        raise ValueError(f"Platform inválida: {platform}. Use 'instagram' ou 'linkedin'.")

    payload = {
        "type": "post",
        "userId": USER_ID,
        "accountIds": [account_id],
        "media": [{"url": u, "type": "image/jpeg"} for u in image_urls],
        "summary": caption,
        "status": "published",
    }
    return http_request("POST", f"/social-media-posting/{LOC}/posts", payload)


def create_scheduled_post(
    platform: str,
    image_urls: list[str],
    caption: str,
    schedule_date_iso: str,
) -> dict:
    """Agenda um post para uma data futura.

    ⚠️ CUIDADO: Agendamentos com >5 minutos de antecedência podem disparar o bug
    'platform=google'. Sempre validar com get_post() após criação.

    Args:
        schedule_date_iso: ISO 8601 UTC (ex: "2026-04-25T13:00:00.000Z")
    """
    account_id = PLATFORMS.get(platform)
    if not account_id:
        raise ValueError(f"Platform inválida: {platform}")

    payload = {
        "type": "post",
        "userId": USER_ID,
        "accountIds": [account_id],
        "media": [{"url": u, "type": "image/jpeg"} for u in image_urls],
        "summary": caption,
        "status": "scheduled",
        "scheduleDate": schedule_date_iso,
    }
    return http_request("POST", f"/social-media-posting/{LOC}/posts", payload)


def schedule_in_minutes(platform: str, image_urls: list[str], caption: str, minutes: int = 2) -> dict:
    """Atalho: agenda para N minutos no futuro (default 2min para evitar bug)."""
    target = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    iso = target.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    return create_scheduled_post(platform, image_urls, caption, iso)


if __name__ == "__main__":
    # Exemplo demonstrativo (não executa sem URLs reais)
    print("Este módulo deve ser importado, não executado diretamente.")
    print("Exemplo:")
    print('  from create_post import create_immediate_post')
    print('  res = create_immediate_post("instagram", ["https://...jpg"], "caption")')
