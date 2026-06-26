#!/usr/bin/env python3
"""Gera o refresh token OAuth pra Google Ads API.
Abre o navegador, autoriza como o DONO do MCC, e salva o refresh token no cofre.
NÃO imprime o token no terminal — só confirma sucesso.

Pré-requisito: ter o client OAuth (Desktop) baixado em
~/.claude/secrets/google-ads-oauth-client.json
"""
import os
from google_auth_oauthlib.flow import InstalledAppFlow

SECRETS = os.path.expanduser("~/.claude/secrets")
CLIENT_FILE = os.path.join(SECRETS, "google-ads-oauth-client.json")
TOKEN_FILE = os.path.join(SECRETS, "google-ads-refresh-token.txt")
SCOPES = ["https://www.googleapis.com/auth/adwords"]

if not os.path.exists(CLIENT_FILE):
    raise SystemExit(f"ERRO: falta {CLIENT_FILE}. Baixe o client OAuth (Desktop) do Google Cloud primeiro.")

flow = InstalledAppFlow.from_client_secrets_file(CLIENT_FILE, scopes=SCOPES)
# access_type=offline + prompt=consent garante que o refresh_token venha sempre
creds = flow.run_local_server(
    port=0,
    access_type="offline",
    prompt="consent",
    authorization_prompt_message="Abrindo o navegador... faça login com a conta DONA do MCC.",
    success_message="Autorizado! Pode fechar esta aba e voltar pro terminal.",
    open_browser=True,
)

if not creds.refresh_token:
    raise SystemExit("ERRO: nenhum refresh_token retornado. Garanta que o app OAuth está em "
                     "Produção (não Testing) e tente de novo.")

with open(TOKEN_FILE, "w") as f:
    f.write(creds.refresh_token)
os.chmod(TOKEN_FILE, 0o600)

print("OK_REFRESH_TOKEN_SALVO")
print(f"arquivo: {TOKEN_FILE}")
print(f"token termina em: ...{creds.refresh_token[-6:]}")
