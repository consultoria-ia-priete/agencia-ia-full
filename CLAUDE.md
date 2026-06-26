# Agência de IA — Pacote Completo — âncora do Claude Code

## O que é este repositório

A **Agência de IA completa**: todos os módulos num só lugar (`modulos/`), pra instalar numa
**sequência única**. É o pacote pra quem comprou tudo. Cada módulo tem a própria skill guiada;
a skill **`install-agencia`** orquestra a ordem.

O aluno **não programa**. Fale simples, comemore cada módulo, e faça **checkpoint entre eles**.

## Triage

| O aluno diz… | Você faz |
|---|---|
| "instalar", "instalar tudo", "montar a agência completa", "começar" | Invoca **`install-agencia`** |
| "instalar só o <módulo>" | Vai direto na skill daquele módulo em `modulos/<nome>/` |
| "deu erro no <módulo>" | Lê o `docs/troubleshooting.md` do módulo em questão |

## Ordem

Base → Meta Ads → Google Ads → Funil & Cockpits → CRM Funnels → Tracking → SEO Content → Windsor/GMB.
A Base é sempre primeiro. O aluno pode pular módulos que não vai usar agora.

## Princípios

- Um módulo por vez, checkpoint entre eles. Pré-requisito faltando não trava a sequência toda.
- Segredo nunca vai pro git. `scripts/scan-secrets.sh .` antes de qualquer push.

## Mapa do repositório

| Caminho | Propósito |
|---|---|
| `.claude/skills/install-agencia/SKILL.md` | O orquestrador da sequência |
| `modulos/<nome>/` | Cada módulo, self-contained (com a própria skill e aula) |
| `aula/`, `docs/` | Aula de visão geral + windows |
| `scripts/sync-modules.sh` | (interno do Alex) regenera `modulos/` a partir do kit |

## Plataforma
macOS por padrão; Windows: `docs/windows.md` (ou o repo `tutorial-windows`).
