# Esquadrão Meta Ads — âncora do Claude Code

## O que é este repositório

Módulo que dá ao aluno **acesso de API à Meta Ads**: criar o app, um System User, gerar e
validar o token. É parte do curso **Esquadrão Meta Ads**. Os passos no Business Manager são
**manuais** (cliques no painel); o Claude guia com precisão e valida o resultado.

O aluno **não programa**. Fale simples, um passo por vez, espere o "ok".

## Triage

| O aluno diz… | Você faz |
|---|---|
| "instalar", "criar app Meta", "gerar token", "conectar Meta", "começar" | Invoca **`install-meta-ads`** |
| "validar token", "será que funciona" | Roda `meta_validate.py --slug <bm>` |
| "app bloqueado", "atividade incomum", "erro" | Lê `docs/troubleshooting.md` |

## Princípios

- **1 token por Business Manager** (nunca reaproveitar cross-BM — Meta bloqueia o app).
- Token sempre **validado** com chamada real antes de declarar pronto.
- Token vive no vault `~/.claude/secrets/` (chmod 600), **nunca** no repo. `scan-secrets.sh` antes de push.

## Mapa do repositório

| Caminho | Propósito |
|---|---|
| `.claude/skills/install-meta-ads/SKILL.md` | Instalador guiado |
| `.claude/skills/install-meta-ads/meta_validate.py` | Valida token (lista ad accounts) |
| `aula/`, `docs/` | Aula + referência/troubleshooting/windows |

## Plataforma
macOS por padrão; Windows: `docs/windows.md` (vault sem `chmod`, protegido pela conta).
