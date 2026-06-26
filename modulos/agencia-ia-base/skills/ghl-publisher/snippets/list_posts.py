"""
list_posts.py — Listar e detalhar posts no CRM Funnels.

Uso:
    from list_posts import list_posts, get_post, find_recent_post_by_summary
    posts = list_posts("2026-04-24T00:00:00.000Z", "2026-04-25T00:00:00.000Z")
    details = get_post("69ebfc91a7472002b07827d2")
"""
from _common import LOC, http_request


def list_posts(from_date: str, to_date: str, skip: int = 0, limit: int = 50) -> list[dict]:
    """Lista posts num intervalo de datas.

    Args:
        from_date: ISO 8601 (ex: "2026-04-24T00:00:00.000Z")
        to_date: ISO 8601
        skip, limit: paginação. Note que a API aceita SOMENTE como string.

    Returns:
        Lista de posts (campo result['results']['posts']).
    """
    body = {
        "fromDate": from_date,
        "toDate": to_date,
        "skip": str(skip),  # OBRIGATÓRIO como string
        "limit": str(limit),  # OBRIGATÓRIO como string
    }
    res = http_request("POST", f"/social-media-posting/{LOC}/posts/list", body)
    return res.get("results", {}).get("posts", [])


def get_post(post_id: str) -> dict:
    """Detalha um post específico. Retorna o objeto post diretamente."""
    res = http_request("GET", f"/social-media-posting/{LOC}/posts/{post_id}")
    return res.get("results", {}).get("post", {})


def find_recent_post_by_summary(summary_prefix: str, since_iso: str, until_iso: str) -> dict | None:
    """Localiza um post recém-criado pelo prefixo do summary.

    Útil porque a resposta de criação NÃO inclui o post ID.
    """
    posts = list_posts(since_iso, until_iso)
    for p in posts:
        if p.get("summary", "").startswith(summary_prefix):
            return p
    return None


def diagnose_post(post_id: str) -> None:
    """Imprime diagnóstico legível de um post (para debug)."""
    p = get_post(post_id)
    print(f"━━━ Post {post_id} ━━━")
    print(f"  platform:    {p.get('platform')}")
    print(f"  status:      {p.get('status')}")
    print(f"  scheduleDate: {p.get('scheduleDate')}")
    print(f"  publishedAt: {p.get('publishedAt')}")
    print(f"  accountIds:  {p.get('accountIds')}")
    print(f"  media count: {len(p.get('media', []))}")
    print(f"  deleted:     {p.get('deleted')}")
    if p.get("error"):
        print(f"  ⚠️ ERROR:    {p['error']}")
    for i, m in enumerate(p.get("media", [])[:3]):
        print(f"    [{i}] {m.get('url', '')[:80]}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2:
        diagnose_post(sys.argv[1])
    else:
        print("Uso: python list_posts.py <postId>")
