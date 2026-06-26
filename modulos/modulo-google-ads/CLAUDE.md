# Esquadrão Google Ads — âncora do Claude Code

## O que é este repositório

Módulo que dá ao aluno **acesso de API ao Google Ads**: MCC + Developer Token + OAuth
(client + refresh token). Parte do curso **Esquadrão Google Ads**. Passos no Google Cloud /
MCC são **manuais**; o Claude guia e roda o smoke test de validação.

O aluno **não programa**. Fale simples, um passo por vez, espere o "ok".

## Triage

| O aluno diz… | Você faz |
|---|---|
| "instalar", "criar MCC", "conectar Google Ads", "gerar token Google", "começar" | Invoca **`install-google-ads`** |
| "testar", "validar acesso" | Roda `smoke_test.py` |
| "deu erro", "token não aprovado", "não veio refresh" | Lê `docs/troubleshooting.md` |

## Princípios

- São **4 credenciais** que se encaixam (dev token, client id, client secret, refresh token) + MCC.
- **Basic Access** demora ~3 dias: leitura funciona antes, escrita só depois. Avise no começo.
- Tudo vive no vault `~/.claude/secrets/`, **nunca** no repo. `scan-secrets.sh` antes de push.
- MCC parametrizado (`--mcc`/env/vault) — nunca hardcode.

## Mapa do repositório

| Caminho | Propósito |
|---|---|
| `.claude/skills/install-google-ads/SKILL.md` | Instalador guiado |
| `.claude/skills/install-google-ads/get_refresh_token.py` | OAuth no navegador → refresh token |
| `.claude/skills/install-google-ads/smoke_test.py` | Teste read-only (valida as 4 credenciais) |
| `docs/design-doc-modelo.md` | Modelo pro formulário de Basic Access |
| `aula/`, `docs/` | Aula + troubleshooting/windows |

## Plataforma
macOS por padrão; Windows: `docs/windows.md`.
