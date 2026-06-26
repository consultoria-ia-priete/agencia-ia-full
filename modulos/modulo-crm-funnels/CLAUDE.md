# Integração CRM Funnels — âncora do Claude Code

## O que é este repositório

Módulo que conecta o **CRM Funnels (CRM Funnels)** do aluno ao Claude Code por API. Depois disso,
o Claude lê e escreve no CRM dele (contatos, conversas, oportunidades, publicação social).
Requer a **Base** já instalada (existe uma pasta de agência com `.mcp.json`).

O aluno **provavelmente não programa**. Fale simples, um passo por vez, espere o "ok".
**Regra de ouro: nunca grave uma credencial sem validar antes.**

## Triage

| O aluno diz… | Você faz |
|---|---|
| "instalar", "conectar CRM Funnels", "integrar CRM Funnels", "configurar" | Invoca **`install-crm-funnels`** |
| "desconectar CRM Funnels", "remover" | Roda `ghl_inject.py --remove` |
| "não funcionou", "deu 401", "erro" | Lê `docs/troubleshooting.md` |
| Outra coisa | Pergunta de esclarecimento antes |

## Princípios

- Validar com `ghl_validate.py` (chamada real) ANTES de injetar.
- Injeção idempotente via `ghl_inject.py` (não duplica, faz backup, preserva outros MCPs).
- `.mcp.json` está no `.gitignore` — chave nunca vai pro git. `scripts/scan-secrets.sh` antes de push.

## Mapa do repositório

| Caminho | Propósito |
|---|---|
| `.claude/skills/install-crm-funnels/SKILL.md` | Instalador guiado |
| `.claude/skills/install-crm-funnels/ghl_validate.py` | Valida credencial (chamada real) |
| `.claude/skills/install-crm-funnels/ghl_inject.py` | Injeta/remove o bloco no `.mcp.json` |
| `aula/`, `docs/` | Aula + referência/troubleshooting/windows |

## Plataforma
macOS por padrão; Windows: `docs/windows.md`.
