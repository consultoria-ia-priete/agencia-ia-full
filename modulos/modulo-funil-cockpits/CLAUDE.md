# Funil & Cockpits — âncora do Claude Code

## O que é este repositório

Os **funis de vendas** do método (quiz low-ticket, webinar, consultoria, LP) + os **cockpits**
de acompanhamento, no estilo Alex SSCIA. Os funis vêm como **templates sanitizados** (placeholders
no lugar dos dados reais); a skill ajuda o aluno a personalizar, buildar e fazer deploy.

> Os **escritórios dos agentes** já vêm na **Base** (`_opensquad/dashboard/office.html`).

O aluno **não programa**. Fale simples, um passo por vez, espere o "ok".

## Triage

| O aluno diz… | Você faz |
|---|---|
| "instalar", "subir meu funil", "publicar página", "criar quiz/webinar", "começar" | Invoca **`install-funil-cockpits`** |
| "gerar o cockpit" | Roda `cockpits/build-cockpit-*.py` |
| "lead não chega", "deploy falhou", "erro" | Lê `docs/troubleshooting.md` |

## Princípios

- **Nunca** subir com placeholder cru (`SEU-DOMINIO`, `{{...}}`) nem com Pixel/checkout de outro.
- O aluno usa o **Pixel dele** (módulo Meta Ads) e a **credencial CRM Funnels dele** (módulo CRM Funnels) no `/api/lead`.
- `.env` e backups fora do git. `scripts/scan-secrets.sh` antes de qualquer push.

## Mapa do repositório

| Caminho | Propósito |
|---|---|
| `.claude/skills/install-funil-cockpits/SKILL.md` | Instalador guiado (personaliza + deploy) |
| `funis/quiz/`, `funis/webinar/`, `funis/consultoria/`, `funis/lp/` | Funis (Vite/Astro), sanitizados |
| `cockpits/build-cockpit-*.py` + `*.template.html` | Geradores de dashboard |
| `aula/`, `docs/` | Aula + troubleshooting/windows |

## Plataforma
macOS por padrão; Windows: `docs/windows.md`.
