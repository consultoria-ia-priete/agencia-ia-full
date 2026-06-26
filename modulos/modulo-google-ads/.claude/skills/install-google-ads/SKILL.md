---
name: install-google-ads
description: "Cria o MCC e o acesso de API do Google Ads (OAuth + developer token + refresh token) pra operar campanhas pelo Claude Code (Esquadrão Google Ads). Use quando o aluno disser 'instalar', 'conectar Google Ads', 'criar MCC', 'gerar token Google', 'começar'. Guia os passos manuais e roda o smoke test."
---

# Skill: install-google-ads — Seu acesso de API ao Google Ads

Você está dando ao aluno **acesso de API ao Google Ads**. São **4 credenciais** que se
encaixam: Developer Token (do MCC), Client ID + Client Secret (OAuth do Google Cloud) e
Refresh Token. O aluno **não programa** — fale simples, um passo por vez.

> ⚠️ **Item que trava o cronograma:** o **Basic Access** do Developer Token leva ~3 dias de
> aprovação do Google. A **leitura** (smoke test) já funciona no nível "Acesso às Análises"
> antes disso; a **escrita** (criar/editar campanha) só depois do Basic aprovado. Avise o aluno
> no começo pra ele não travar esperando.

## Passo 0 — Pré-requisitos

- Uma conta **Google Ads MCC** (Manager Account) — ou criar uma.
- Acesso ao **Google Cloud Console** (mesma conta Google).
- `python3` + libs: `pip install google-ads google-auth-oauthlib`.

## Fase 1 — Developer Token + Basic Access (começa AGORA, demora ~3 dias)

> No MCC: **Admin → API Center → gerar Developer Token**.
> Depois solicite **Basic Access** pelo formulário (precisa de um "design doc" descrevendo o uso).

Salve o token no vault:
```bash
mkdir -p ~/.claude/secrets && chmod 700 ~/.claude/secrets
printf %s '<DEVELOPER_TOKEN>' > ~/.claude/secrets/google-ads-developer-token.txt
printf %s '<MCC_ID_sem_traços>' > ~/.claude/secrets/google-ads-mcc.txt
chmod 600 ~/.claude/secrets/google-ads-*.txt
```
> Há um modelo de design doc em `docs/design-doc-modelo.md` pra preencher e anexar no formulário.

## Fase 2 — OAuth no Google Cloud

> **console.cloud.google.com** → criar/escolher um projeto → **Enable** a "Google Ads API".
> → **APIs & Services → OAuth consent screen** (External, publique em **Produção**).
> → **Credentials → Create Credentials → OAuth client ID → Desktop app** → **Download JSON**.

Salve o client OAuth no vault:
```bash
mv ~/Downloads/client_secret_*.json ~/.claude/secrets/google-ads-oauth-client.json
chmod 600 ~/.claude/secrets/google-ads-oauth-client.json
```

## Passo 3 — Refresh Token (navegador)

```bash
python3 .claude/skills/install-google-ads/get_refresh_token.py
```
Abre o navegador → logar com a **conta dona do MCC** → autorizar. O token é salvo no vault
(não aparece no terminal). Se vier vazio: o app OAuth ainda está em "Testing" → publique em Produção.

## Passo 4 — Smoke test (READ-ONLY) — VALIDA tudo junto

```bash
python3 .claude/skills/install-google-ads/smoke_test.py
```
Lista as contas acessíveis + as contas-filhas do MCC. Termina com `SMOKE_OK`.
- Erro de autenticação → confira as 4 credenciais no vault.
- `SMOKE_OK` mas sem contas-filhas → o MCC ainda não tem contas vinculadas (normal se for novo).

## Passo 5 — Escrita (depois do Basic Access aprovado)

Quando o Google aprovar o Basic Access (email, ~3 dias), reexecute o smoke test e o aluno já
pode criar/editar campanhas via API. Antes disso, só leitura.

## Validação final

- [ ] Developer Token + MCC ID salvos no vault
- [ ] OAuth client (Desktop) baixado e salvo no vault
- [ ] `get_refresh_token.py` salvou o refresh token
- [ ] `smoke_test.py` terminou com `SMOKE_OK`
- [ ] `scripts/scan-secrets.sh .` = 0 hits (tudo no vault, fora do repo)

Marque com o aluno cada item de `aula/checklist.md`.

## Troubleshooting

`docs/troubleshooting.md`. Comuns: refresh_token vazio (app em Testing), `DEVELOPER_TOKEN_NOT_APPROVED`
(Basic ainda pendente — leitura funciona, escrita não), `login_customer_id` errado (MCC com traços).
