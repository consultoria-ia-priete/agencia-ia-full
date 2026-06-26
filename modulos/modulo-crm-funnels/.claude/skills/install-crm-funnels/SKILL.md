---
name: install-crm-funnels
description: "Conecta o CRM Funnels (CRM Funnels) ao Claude Code por API. Use quando o aluno disser 'instalar', 'conectar CRM Funnels', 'integrar CRM Funnels', 'configurar CRM Funnels', 'começar'. Guia a criação da Private Integration, VALIDA a credencial com chamada real e injeta no .mcp.json (idempotente, com rollback)."
---

# Skill: install-crm-funnels — Conecte seu CRM Funnels

Você está conectando o CRM Funnels do aluno ao Claude Code. Ele **provavelmente não programa**.
Fale simples, um passo por vez, espere o "ok". **Nunca grave uma credencial sem validar antes.**

Ao final, o `.mcp.json` da agência dele terá o bloco `gohighlevel` com chave + Location ID
**validados**, e o Claude poderá ler/escrever no CRM dele (contatos, conversas, oportunidades,
publicação social).

## Passo 0 — Pré-requisitos

- Base já instalada (skill `install-base` rodou) — existe uma pasta de agência com `.mcp.json`.
- Conta **CRM Funnels** com acesso à **Location** que ele quer conectar.
- `python3` disponível (pra validação).

Pergunte em qual pasta de agência vamos conectar (onde está o `.mcp.json`). Guarde como `CLIENT_DIR`.

## Passo 1 — Criar a Private Integration no CRM Funnels (manual, guiado)

Explique: "Vamos criar uma chave de API privada que dá ao Claude permissão no seu CRM."
Conduza no painel do CRM Funnels:

> **Settings → Private Integrations → Create new Integration**
> - Nome: `Claude Code` (ou o que preferir).
> - **Scopes (marque pelo menos):** `contacts.readonly`, `contacts.write`,
>   `conversations.readonly`, `conversations.write`, `conversations/message.write`,
>   `opportunities.readonly`, `opportunities.write`, `locations.readonly`,
>   `social-media-posting.readonly`, `social-media-posting.write`.
> - Criar → **copiar a API Key** (começa com `pit-`).

Depois pegue o **Location ID**: **Settings → Business Profile → Location ID** (copiar).

Peça pro aluno colar os dois aqui. Trate ambos como **secret** (não repita o valor em texto).

## Passo 2 — VALIDAR antes de gravar (obrigatório)

Rode o helper de validação — ele faz uma chamada real e só retorna OK se a credencial
funciona (e já lista os canais sociais conectados):
```bash
python3 .claude/skills/install-crm-funnels/ghl_validate.py --api-key "<pit-...>" --location "<LOCATION_ID>"
```
- Se falhar (401/403): a chave está errada, expirou, ou faltou scope. **NÃO grave.** Volte ao Passo 1.
- Se passar: siga. Mostre ao aluno os canais que apareceram ("Instagram conectado ✓").

## Passo 3 — Injetar no `.mcp.json` (idempotente + backup)

Com a credencial validada, injete o bloco `gohighlevel` no `.mcp.json` da agência:
```bash
python3 .claude/skills/install-crm-funnels/ghl_inject.py --client-dir "<CLIENT_DIR>" \
  --api-key "<pit-...>" --location "<LOCATION_ID>"
```
O script: faz backup `.mcp.json.bak`, cria/atualiza o bloco `gohighlevel` (não duplica),
preserva os outros MCPs (playwright, higgsfield). Confirme que escreveu.

> O `.mcp.json` está no `.gitignore` — a chave **nunca** vai pro GitHub.

## Passo 4 — Recarregar e testar

Peça pro aluno **reabrir o Claude Code** na pasta da agência (pra carregar o novo MCP).
Teste com uma leitura inofensiva: "lista meus últimos contatos do CRM Funnels" — deve responder
usando o MCP `gohighlevel`.

## Rollback (se precisar desconectar)

```bash
python3 .claude/skills/install-crm-funnels/ghl_inject.py --client-dir "<CLIENT_DIR>" --remove
```
Remove o bloco `gohighlevel` do `.mcp.json` (mantém o resto).

## Validação final

- [ ] `ghl_validate.py` retornou OK + listou os canais
- [ ] `.mcp.json` tem o bloco `gohighlevel` (e só um)
- [ ] Reabriu o Claude Code e uma leitura do CRM Funnels funcionou
- [ ] `scripts/scan-secrets.sh "<CLIENT_DIR>"` = 0 hits (a chave está no .mcp.json gitignored)

Marque com o aluno cada item de `aula/checklist.md`.

## Troubleshooting

`docs/troubleshooting.md`. Comuns: 401 (chave errada/sem scope), Location ID trocado,
MCP não recarregou (reabrir o Claude Code), `send_sms` dá sucesso falso (status real só
relendo a conversa com delay).
