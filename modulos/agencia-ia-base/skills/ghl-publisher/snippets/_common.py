"""
_common.py — Utilitários compartilhados pelos snippets da skill ghl-publisher.

Importe nos demais snippets com:
    from _common import LOC, API_KEY, USER_ID, IG_ID, LI_ID, HEADERS, ctx, http_request
"""
import urllib.request
import urllib.error
import ssl
import json
from typing import Any

# ── Credenciais (ver references/credentials.md) ─────────────────────
LOC = "{{GHL_LOCATION_ID}}"
API_KEY = "{{GHL_API_KEY}}"
USER_ID = "{{GHL_USER_ID}}"
IG_ID = "{{GHL_COMPANY_ID}}_{{GHL_LOCATION_ID}}_{{IG_NATIVE_ID}}"
LI_ID = "{{LI_ACCOUNT_ID}}"

BASE_URL = "https://services.leadconnectorhq.com"

# Headers padrão (User-Agent é obrigatório — sem ele Cloudflare WAF retorna 403)
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Version": "2021-07-28",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
}

# SSL context (necessário em macOS Python 3.14 sem certifi configurado)
ctx = ssl._create_unverified_context()


def http_request(method: str, path: str, body: Any = None, extra_headers: dict | None = None) -> dict:
    """Wrapper simples para chamadas à API CRM Funnels.

    Args:
        method: GET, POST, PUT, DELETE
        path: caminho relativo (ex: "/social-media-posting/{LOC}/posts")
        body: dict que será serializado como JSON, ou bytes (para multipart)
        extra_headers: headers extras (ex: Content-Type customizado para multipart)

    Returns:
        dict da resposta JSON

    Raises:
        urllib.error.HTTPError com .code e .read() para diagnosticar 4xx/5xx
    """
    url = BASE_URL + path
    headers = dict(HEADERS)
    if extra_headers:
        headers.update(extra_headers)

    if isinstance(body, (dict, list)):
        data = json.dumps(body).encode()
    elif isinstance(body, (bytes, bytearray)):
        data = body
    else:
        data = None

    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    r = urllib.request.urlopen(req, context=ctx)
    raw = r.read().decode()
    return json.loads(raw) if raw else {}
