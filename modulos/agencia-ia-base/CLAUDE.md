# Agência de IA — Base (Opensquad) — âncora do Claude Code

## O que é este repositório

A **NOSSA Base** da agência, instalada **por cima de um Opensquad que o aluno já tem**: adiciona
as **skills globais** (publicação, geração de imagem/vídeo, carrossel, sscia-sync) e **atualiza o
framework Opensquad** (NEXUS + squads-base + playbooks), **sem apagar a empresa/squads que o aluno
já criou**. É o alicerce de todos os outros módulos.

> Pré-requisito: o aluno **já instalou o Opensquad e criou a empresa dele** (aula anterior, fluxo
> nativo `/opensquad create`). Esta base é um **update aditivo e protegido** em cima disso.

O aluno **provavelmente não programa**. Fale simples, um passo por vez, comemore os marcos.

## Triage — o que fazer quando o aluno fala

| O aluno diz… | Você faz |
|---|---|
| "instalar a base", "puxar as skills", "atualizar", "começar" | Invoca **`install-base`** (update aditivo protegido) |
| "atualizar squads", "propagar" | `sscia-sync --propagate-all --skip-customized` |
| "criar cliente novo" (agência multi-cliente) | `sscia-sync --new-client` (avançado) |
| "não funcionou", "deu erro" | Lê `docs/troubleshooting.md` |
| Qualquer outra coisa | Faz UMA pergunta de esclarecimento antes de agir |

## Princípios (não viole)

- Um passo por vez; espere o "ok" do aluno.
- **Update aditivo e protegido:** NUNCA sobrescreva `_opensquad/_memory/*` (company.md,
  brand-profile, preferences), `squads/*/_memory/*`, `.mcp.json`, `.env`, nem as squads do aluno.
- Nunca invente credencial. CRM Funnels/Meta/Google/fal.ai/Higgsfield vêm dos módulos próprios.
- Segredo nunca vai pro git. `scripts/scan-secrets.sh` antes de qualquer push.

## O que esta base faz

| Ação | Onde | Protege |
|---|---|---|
| Adiciona as skills da agência | `~/.claude/skills/` | as skills que o aluno já tinha |
| Atualiza o framework (NEXUS + squads-base + playbooks) | projeto do aluno, via `sscia-sync --propagate` | a empresa + squads que o aluno criou |
| Disponibiliza o molde | `<PROJECTS_ROOT>/_TEMPLATE_SSCIA` | — |

## Mapa do repositório

| Caminho | Propósito |
|---|---|
| `.claude/skills/install-base/SKILL.md` | O instalador guiado |
| `skills/` | As 7 skills globais a copiar pra `~/.claude/skills/` |
| `template/_TEMPLATE_SSCIA/` | O molde de squads + NEXUS |
| `aula/` | Roteiro + checklist da aula |
| `docs/` | Referência + troubleshooting + windows |

## Plataforma

Passos assumem **macOS**. Windows: `docs/windows.md` primeiro. As skills do Claude Code
rodam igual nas duas plataformas.
