#!/usr/bin/env python3
"""ghl_validate.py — Valida uma credencial CRM Funnels ANTES de gravá-la em qualquer lugar.

Faz uma chamada real à API do CRM Funnels e só retorna sucesso (exit 0) se a chave +
Location ID funcionam. De quebra, lista os canais sociais conectados (útil pra publicação).

Uso:
    python3 ghl_validate.py --api-key "pit-..." --location "LOCATION_ID"

Exit 0 = válido. Exit != 0 = inválido (NÃO grave a credencial).
"""
import argparse
import json
import ssl
import sys
import urllib.error
import urllib.request

BASE = "https://services.leadconnectorhq.com"
VERSION = "2021-07-28"


def _get(path, api_key):
    req = urllib.request.Request(
        f"{BASE}{path}",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Version": VERSION,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
        },
    )
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
        return json.loads(r.read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--api-key", required=True)
    ap.add_argument("--location", required=True)
    args = ap.parse_args()

    # 1) A Location existe / a chave tem acesso a ela?
    try:
        loc = _get(f"/locations/{args.location}", args.api_key)
        name = (loc.get("location") or {}).get("name") or loc.get("name") or "(sem nome)"
        print(f"✓ Location OK: {name}")
    except urllib.error.HTTPError as e:
        print(f"✗ FALHOU na Location ({e.code}). Chave errada, sem scope locations.readonly, "
              f"ou Location ID trocado.", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"✗ Erro de rede ao validar Location: {e}", file=sys.stderr)
        return 3

    # 2) Lista os canais sociais conectados (não bloqueia se vazio — só informa).
    try:
        data = _get(f"/social-media-posting/{args.location}/accounts", args.api_key)
        accounts = (data.get("results") or {}).get("accounts") or []
        if accounts:
            print("Canais sociais conectados:")
            for acc in accounts:
                print(f"  - {acc.get('platform','?'):10} | {acc.get('name','?'):24} | {acc.get('status','?')}")
        else:
            print("(nenhum canal social conectado ainda — opcional, dá pra conectar depois no CRM Funnels)")
    except urllib.error.HTTPError as e:
        print(f"(aviso: não listou canais sociais [{e.code}] — confira o scope "
              f"social-media-posting.readonly se for publicar)")

    print("\n✓ VÁLIDO — pode injetar no .mcp.json.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
