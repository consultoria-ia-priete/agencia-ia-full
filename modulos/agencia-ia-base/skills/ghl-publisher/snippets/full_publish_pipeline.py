"""
full_publish_pipeline.py — Pipeline completo end-to-end de publicação no CRM Funnels.

Faz tudo que um agente publicador precisa:
  1. Valida canais conectados (Instagram + LinkedIn ativos)
  2. Upload das imagens locais (JPEG) → URLs em assets.cdn.filesafe.space
  3. Cria posts (Instagram + LinkedIn) em paralelo, modo imediato
  4. Verifica resultado de cada post (~10s depois)
  5. Retorna relatório completo

Uso programático:
    from full_publish_pipeline import publish_carousel
    report = publish_carousel(
        slides_dir="/path/to/jpegs/",
        caption="Caption do post",
        platforms=["instagram", "linkedin"],
    )
"""
import os
import time
from datetime import datetime, timezone, timedelta
from _common import LOC, http_request
from upload_media import upload_directory
from create_post import create_immediate_post
from list_posts import list_posts, get_post


def validate_accounts() -> dict[str, bool]:
    """Verifica se Instagram e LinkedIn estão conectados e ativos."""
    res = http_request("GET", f"/social-media-posting/{LOC}/accounts")
    accounts = res.get("results", {}).get("accounts", [])
    status = {}
    for acc in accounts:
        plat = acc.get("platform")
        active = acc.get("status") == "active"
        if plat in ("instagram", "linkedin"):
            status[plat] = active
    return status


def find_just_created_post(platform: str, summary: str, account_id: str) -> dict | None:
    """Localiza o post recém-criado pelos primeiros chars do summary + accountId."""
    now = datetime.now(timezone.utc)
    since = (now - timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    until = (now + timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    posts = list_posts(since, until)
    summary_prefix = summary[:30]
    for p in posts:
        if (
            p.get("summary", "").startswith(summary_prefix)
            and account_id in p.get("accountIds", [])
        ):
            return p
    return None


def publish_carousel(
    slides_dir: str,
    caption: str,
    platforms: list[str] = None,
) -> dict:
    """Publica um carrossel completo.

    Args:
        slides_dir: diretório com JPEGs em ordem alfabética (slide-01.jpg, slide-02.jpg, ...)
        caption: caption (mesma para todos os platforms)
        platforms: lista de canais. Default: ["instagram", "linkedin"]

    Returns:
        dict com chaves 'uploads', 'posts', 'verification'
    """
    if platforms is None:
        platforms = ["instagram", "linkedin"]

    report = {"uploads": {}, "posts": {}, "verification": {}}

    # 1. Validar canais
    print("\n[1/5] Validando canais conectados...")
    status = validate_accounts()
    for p in platforms:
        if not status.get(p):
            raise RuntimeError(f"Canal {p} não está ativo. Pedir Alex para reconectar no CRM Funnels UI.")
        print(f"  ✅ {p}: active")

    # 2. Upload das imagens
    print(f"\n[2/5] Uploading slides em {slides_dir}...")
    urls_map = upload_directory(slides_dir, ".jpg")
    image_urls = [u for u in urls_map.values() if u]
    if not image_urls:
        raise RuntimeError("Nenhuma imagem foi uploaded com sucesso.")
    report["uploads"] = urls_map
    print(f"  ✅ {len(image_urls)} slides uploaded")

    # 3. Criar posts em cada canal
    print("\n[3/5] Criando posts...")
    for platform in platforms:
        try:
            res = create_immediate_post(platform, image_urls, caption)
            print(f"  ✅ {platform}: {res.get('message', 'created')}")
            report["posts"][platform] = res
        except Exception as e:
            print(f"  ❌ {platform}: {e}")
            report["posts"][platform] = {"error": str(e)}

    # 4. Aguardar e verificar
    print("\n[4/5] Aguardando 12s antes de verificar...")
    time.sleep(12)

    print("\n[5/5] Verificando resultados...")
    from create_post import PLATFORMS as ACCOUNT_MAP
    for platform in platforms:
        post = find_just_created_post(platform, caption, ACCOUNT_MAP[platform])
        if not post:
            report["verification"][platform] = {"found": False}
            print(f"  ⚠️ {platform}: post não localizado na listagem")
            continue
        details = get_post(post["_id"])
        v = {
            "found": True,
            "id": details.get("_id"),
            "platform": details.get("platform"),
            "status": details.get("status"),
            "media_count": len(details.get("media", [])),
            "error": details.get("error"),
        }
        report["verification"][platform] = v
        ok = (
            v["platform"] == platform  # não pode ser google
            and v["status"] in ("published", "in_progress")
            and v["media_count"] == len(image_urls)
            and not v["error"]
        )
        emoji = "✅" if ok else "⚠️"
        print(f"  {emoji} {platform}: id={v['id']} status={v['status']} media={v['media_count']} platform={v['platform']}")
        if v["error"]:
            print(f"     ERROR: {v['error']}")

    return report


if __name__ == "__main__":
    import sys
    import json
    if len(sys.argv) < 3:
        print("Uso: python full_publish_pipeline.py <slides_dir> '<caption>'")
        sys.exit(1)
    report = publish_carousel(sys.argv[1], sys.argv[2])
    print("\n━━━ RELATÓRIO FINAL ━━━")
    print(json.dumps(report, indent=2, default=str))
