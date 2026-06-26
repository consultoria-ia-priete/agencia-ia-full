# Windsor.ai + Google My Business — âncora do Claude Code

## O que é este repositório

Módulo que conecta o **Windsor.ai** ao Claude (via claude.ai) e puxa dados do **Google My
Business**: avaliações, posts, métricas. Alimenta SEO local, prova social e resposta a reviews.
**Não instala software** — Windsor é MCP remoto (OAuth no claude.ai).

O aluno **não programa**. Fale simples, um passo por vez, espere o "ok".

## Triage

| O aluno diz… | Você faz |
|---|---|
| "instalar", "conectar Windsor", "integrar GMB", "puxar reviews", "começar" | Invoca **`install-windsor-gmb`** |
| "responder avaliação", "postar no Google" | `list_actions` no conector + ação com confirmação |
| "deu erro", "não acha a ficha" | Lê `docs/troubleshooting.md` |

## Princípios

- Windsor conecta via **claude.ai** (OAuth) — sem chave em arquivo local.
- GMB usa `locations/XXXX` (NÃO `place_id`).
- Ação de escrita (responder review / postar) só com confirmação do aluno.

## Mapa do repositório

| Caminho | Propósito |
|---|---|
| `.claude/skills/install-windsor-gmb/SKILL.md` | Guia de conexão + primeiro pull |
| `docs/` | Referência (campos GMB), troubleshooting, windows |
| `aula/` | Roteiro + checklist |

## Plataforma
Independe de SO (é nuvem). `docs/windows.md` só pro ambiente Claude Code geral.
