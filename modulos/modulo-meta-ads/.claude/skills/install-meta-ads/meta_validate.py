#!/usr/bin/env python3
"""meta_validate.py — Valida um token Meta lendo-o do vault local e listando os ad accounts.

Uso:
    python3 meta_validate.py --slug minha-bm
    python3 meta_validate.py --token "EAA..."        # alternativa: passar o token direto

Lê de ~/.claude/secrets/meta-token-bm-<slug>.txt quando --slug é usado.
Exit 0 = token válido e enxerga ao menos 1 ad account.
"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

GRAPH = "https://graph.facebook.com/v21.0"


def read_token(slug=None, token=None):
    if token:
        return token.strip()
    p = Path.home() / ".claude" / "secrets" / f"meta-token-bm-{slug}.txt"
    if not p.exists():
        print(f"✗ Vault não encontrado: {p}", file=sys.stderr)
        sys.exit(2)
    return p.read_text().strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug")
    ap.add_argument("--token")
    args = ap.parse_args()
    if not args.slug and not args.token:
        print("✗ Use --slug <bm> ou --token <valor>.", file=sys.stderr)
        return 2

    tok = read_token(args.slug, args.token)
    qs = urllib.parse.urlencode({"fields": "name,account_status,currency", "access_token": tok})
    url = f"{GRAPH}/me/adaccounts?{qs}"
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "ignore")
        print(f"✗ Token rejeitado ({e.code}). Detalhe: {body[:200]}", file=sys.stderr)
        return 3
    except Exception as e:
        print(f"✗ Erro de rede: {e}", file=sys.stderr)
        return 3

    accounts = data.get("data", [])
    if not accounts:
        print("✗ Token válido, mas NÃO enxerga nenhum ad account.\n"
              "  Provável: faltou 'Add Assets' (ad accounts) ao System User.", file=sys.stderr)
        return 4

    print(f"✓ Token OK — enxerga {len(accounts)} ad account(s):")
    for a in accounts:
        status = "ativa" if a.get("account_status") == 1 else f"status={a.get('account_status')}"
        print(f"  - {a.get('name','?'):28} | {a.get('id','?'):20} | {a.get('currency','?')} | {status}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
