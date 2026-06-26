---
name: install-funil-cockpits
description: "Sobe os funis do método (quiz, webinar, consultoria, LP) e os cockpits de acompanhamento. Use quando o aluno disser 'instalar', 'subir meu funil', 'publicar a página', 'criar o quiz/webinar', 'cockpit', 'começar'. Guia a personalização (preencher placeholders), build e deploy no Cloudflare Pages."
---

# Skill: install-funil-cockpits — Os funis + os cockpits

Você está subindo os **funis de vendas** do método (no estilo Alex SSCIA) e os **cockpits**
de acompanhamento, na conta do aluno. Ele **não programa** — fale simples, um passo por vez.

Os funis vêm em `funis/` como **templates já sanitizados** (com placeholders no lugar dos
dados do Alex). Seu trabalho: ajudar o aluno a **preencher os placeholders dele**, fazer o
build e o deploy. **Nunca** suba com os placeholders crus nem com dados de outro.

Funis incluídos:
| Pasta | O que é |
|---|---|
| `funis/quiz/` | Quiz low-ticket (Vite+React) — captura + qualificação |
| `funis/webinar/` | Página de webinar (inscrição + sala) |
| `funis/consultoria/` | Página da oferta de consultoria (high ticket) |
| `funis/lp/` | Landing page de oferta |
Cockpits: `cockpits/build-cockpit-webinar.py`, `cockpits/build-cockpit-servico.py` (+ templates).

> Os **escritórios dos agentes** já vêm na **Base** (`_opensquad/dashboard/office.html`).

## Passo 0 — Pré-requisitos

- A **Base** instalada; idealmente **CRM Funnels** e **Tracking** já conectados (os funis capturam lead
  no CRM Funnels e disparam Pixel/CAPI). Se ainda não, dá pra subir e plugar depois.
- **Node** + `npx wrangler` + conta **Cloudflare** (+ `gh`).

## Passo 1 — Escolher o funil e personalizar

Pergunte qual funil subir primeiro (recomendado: o **quiz**, porta de entrada low-ticket).
Abra a pasta e troque os placeholders pelos dados do aluno. Principais:
- `{{META_PIXEL_ID}}` → o Pixel da Meta DELE (vem do módulo Meta Ads, ou Events Manager).
- `SEU-DOMINIO.com` → o domínio do funil dele.
- `{{LASTLINK_PRODUTO_LOW}}` / `{{LASTLINK_PRODUTO_ALT}}` → os códigos de checkout dos produtos dele.
- `@{{SEU_INSTAGRAM}}` → o @ dele.
- `wrangler.toml`: `account_id`, domínio, e (se usar D1) o `database_id`.
- `functions/api/lead.ts`: o destino do lead (CRM Funnels) — usar a credencial do módulo CRM Funnels.

> Dica: peça ao aluno os valores um a um e faça as substituições com ele vendo.

## Passo 2 — Build + deploy (Cloudflare Pages)

```bash
cd funis/<funil>
npm install
npm run build          # Vite/Astro geram o dist/
npx wrangler pages deploy dist --project-name <nome-do-funil>
```
(Se o funil usa Cloudflare **Functions** pra `/api/lead`, o deploy do Pages já as inclui.)
Configure o domínio custom no painel da Cloudflare apontando pro projeto Pages.

## Passo 3 — Cockpits de acompanhamento

Os cockpits são geradores Python que leem um readout e produzem um HTML de dashboard.
```bash
python3 cockpits/build-cockpit-webinar.py   # gera o cockpit do funil de webinar
python3 cockpits/build-cockpit-servico.py   # gera o cockpit de serviço/consultoria
```
Abra o HTML gerado pra mostrar ao aluno o cockpit do funil de vendas (métricas + CRM Funnels).

## Passo 4 — Repetir pros outros funis

Repita os Passos 1–2 pra webinar, consultoria e LP conforme o aluno for ativando.
Cada um é independente; suba na ordem que fizer sentido pro lançamento dele.

## Validação final

- [ ] Pelo menos 1 funil (o quiz) com placeholders preenchidos, sem `SEU-DOMINIO`/`{{...}}` crus
- [ ] `npm run build` ok + `wrangler pages deploy` no ar
- [ ] Lead de teste capturado (chega no CRM Funnels) + Pixel disparando
- [ ] Cockpit gerado e abrindo
- [ ] `scripts/scan-secrets.sh .` = 0 hits

Marque com o aluno cada item de `aula/checklist.md`.

## Troubleshooting

`docs/troubleshooting.md`. Comuns: placeholder não preenchido (lead vai pro lugar errado /
pixel do Alex), `wrangler pages deploy` sem account_id, domínio custom não apontado,
`/api/lead` falhando (credencial CRM Funnels não configurada).
