#!/usr/bin/env python3
"""Smoke test READ-ONLY da Google Ads API.
Monta o client com os segredos do cofre, lista as contas acessíveis pelo MCC e
enumera as contas-filhas (clientes). Funciona já no nível 'Acesso às Análises'
(leitura), antes do Basic Access ser aprovado.

O MCC vem de (nesta ordem): --mcc, env GOOGLE_ADS_MCC, ou ~/.claude/secrets/google-ads-mcc.txt
"""
import argparse
import json
import os
import sys

S = os.path.expanduser("~/.claude/secrets")


def read_mcc(cli_value):
    if cli_value:
        return cli_value.replace("-", "")
    env = os.environ.get("GOOGLE_ADS_MCC")
    if env:
        return env.replace("-", "")
    p = os.path.join(S, "google-ads-mcc.txt")
    if os.path.exists(p):
        return open(p).read().strip().replace("-", "")
    sys.exit("ERRO: informe o MCC via --mcc, env GOOGLE_ADS_MCC, ou ~/.claude/secrets/google-ads-mcc.txt")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mcc", help="ID do MCC (com ou sem traços)")
    args = ap.parse_args()
    MCC = read_mcc(args.mcc)

    try:
        from google.ads.googleads.client import GoogleAdsClient
        from google.ads.googleads.errors import GoogleAdsException
    except ImportError:
        sys.exit("ERRO: falta a lib. Rode: pip install google-ads")

    oauth = json.load(open(os.path.join(S, "google-ads-oauth-client.json")))["installed"]
    refresh = open(os.path.join(S, "google-ads-refresh-token.txt")).read().strip()
    devtok = open(os.path.join(S, "google-ads-developer-token.txt")).read().strip()

    client = GoogleAdsClient.load_from_dict({
        "developer_token": devtok,
        "client_id": oauth["client_id"],
        "client_secret": oauth["client_secret"],
        "refresh_token": refresh,
        "login_customer_id": MCC,
        "use_proto_plus": True,
    })

    print("=== 1) Contas acessíveis (ListAccessibleCustomers) ===")
    cs = client.get_service("CustomerService")
    for rn in cs.list_accessible_customers().resource_names:
        print("  -", rn)

    print(f"\n=== 2) Contas-filhas sob o MCC {MCC} ===")
    ga = client.get_service("GoogleAdsService")
    query = """
        SELECT customer_client.id, customer_client.descriptive_name,
               customer_client.manager, customer_client.level,
               customer_client.currency_code, customer_client.status
        FROM customer_client
        WHERE customer_client.level <= 1
        ORDER BY customer_client.level
    """
    try:
        rows = 0
        for batch in ga.search_stream(customer_id=MCC, query=query):
            for r in batch.results:
                c = r.customer_client
                tag = "MCC " if c.manager else "    "
                print(f"  {tag} {c.id}  {c.descriptive_name or '(sem nome)'}  [{c.status.name}] {c.currency_code}")
                rows += 1
        print(f"\nTotal: {rows} contas visíveis.\nSMOKE_OK")
    except GoogleAdsException as ex:
        print("ERRO GoogleAdsException:")
        for e in ex.failure.errors:
            print("  ->", e.error_code, "|", e.message)
        sys.exit(1)


if __name__ == "__main__":
    main()
