#!/usr/bin/env bash
# install.sh — Instalador de 1 linha da NOSSA Base (sem git, sem Xcode).
#
# O ALUNO roda isto DE DENTRO da pasta do projeto dele no Opensquad:
#   curl -fsSL https://raw.githubusercontent.com/consultoria-ia-priete/agencia-ia-base/main/install.sh | bash
#
# Faz tudo: baixa a Base (zip via curl), instala as skills da agência em
# ~/.claude/skills, habilita o sscia-sync, e ADICIONA o NEXUS + as squads-base
# ao projeto atual — SEM apagar a empresa/squads/.mcp.json que o aluno já criou.
set -euo pipefail

REPO="consultoria-ia-priete/agencia-ia-base"
ZIP="https://github.com/${REPO}/archive/refs/heads/main.zip"
G=$'\033[0;32m'; Y=$'\033[1;33m'; R=$'\033[0;31m'; B=$'\033[1m'; N=$'\033[0m'

say(){ printf "%s\n" "$1"; }
PROJ="$(pwd)"
ROOT="$(dirname "$PROJ")"

say "${B}🏛️  Instalando a Base da Agência de IA${N}"
say "    projeto:  $PROJ"

# 0) Sanidade: está num projeto Opensquad?
if [[ ! -d "$PROJ/_opensquad" ]]; then
  say "${Y}⚠  Não achei _opensquad/ aqui. Rode este comando DENTRO da pasta do seu projeto"
  say "   (o que você criou na aula do Opensquad). Abortando por segurança.${N}"
  exit 1
fi

# 1) Ferramentas nativas (curl + unzip já vêm no macOS) — sem git.
command -v curl >/dev/null || { say "${R}✗ curl não encontrado.${N}"; exit 1; }
command -v unzip >/dev/null || { say "${R}✗ unzip não encontrado.${N}"; exit 1; }

# 2) Baixa a Base num temp e extrai.
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
say "⬇️  Baixando a Base…"
curl -fsSL "$ZIP" -o "$TMP/base.zip"
unzip -q "$TMP/base.zip" -d "$TMP"
SRC="$TMP/agencia-ia-base-main"
[[ -d "$SRC/skills" && -d "$SRC/template" ]] || { say "${R}✗ download inválido.${N}"; exit 1; }

# 3) Skills da agência → ~/.claude/skills (idempotente, não apaga as do aluno).
mkdir -p "$HOME/.claude/skills"
for s in opensquad sscia-sync ghl-publisher carousel-generator creative-factory higgsfield-content viral-video-factory; do
  [[ -d "$SRC/skills/$s" ]] && cp -R "$SRC/skills/$s" "$HOME/.claude/skills/"
done
say "${G}✓${N} skills da agência instaladas"

# 4) Wrapper do sscia-sync no PATH.
mkdir -p "$HOME/.local/bin"
cp "$HOME/.claude/skills/sscia-sync/sscia-sync" "$HOME/.local/bin/sscia-sync" 2>/dev/null || true
chmod +x "$HOME/.local/bin/sscia-sync" 2>/dev/null || true
case ":$PATH:" in
  *":$HOME/.local/bin:"*) ;;
  *) echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
     say "${Y}↺  adicionei ~/.local/bin ao PATH — reabra o terminal depois${N}" ;;
esac

# 5) ADICIONA NEXUS + squads-base ao projeto atual — PROTEGIDO.
#    O molde é lido do download TEMPORÁRIO (apagado no fim) — NÃO cria pasta
#    nenhuma na raiz de projetos do aluno. Nunca toca em _memory, .mcp.json,
#    .env, .claude, output; squads existentes do aluno são preservadas.
TPL="$SRC/template/_TEMPLATE_SSCIA"
# NEXUS (chief) — framework; adiciona se não existir.
if [[ -d "$TPL/_opensquad/chief" && ! -d "$PROJ/_opensquad/chief" ]]; then
  cp -R "$TPL/_opensquad/chief" "$PROJ/_opensquad/chief"
fi
# Dashboard de escritórios (cosmético) — adiciona se não existir.
if [[ -d "$TPL/_opensquad/dashboard" && ! -d "$PROJ/_opensquad/dashboard" ]]; then
  cp -R "$TPL/_opensquad/dashboard" "$PROJ/_opensquad/dashboard"
fi
# Squads-base — copia SÓ as que o aluno ainda não tem (preserva as dele).
if [[ -d "$TPL/squads" ]]; then
  mkdir -p "$PROJ/squads"
  for sq in "$TPL/squads"/*/; do
    name="$(basename "$sq")"
    [[ -e "$PROJ/squads/$name" ]] || cp -R "$sq" "$PROJ/squads/$name"
  done
fi
say "${G}✓${N} NEXUS + squads-base adicionados (suas squads e sua empresa: intactas)"

# 7) Higiene: garante .gitignore protegendo segredos (se for versionar).
GI="$PROJ/.gitignore"
if [[ ! -f "$GI" ]] || ! grep -q '_opensquad/_memory' "$GI" 2>/dev/null; then
  { echo ".mcp.json"; echo ".env"; echo ".env.*"; echo "_opensquad/_memory/"; echo "*.bak"; } >> "$GI"
fi

say ""
say "${G}${B}✅ Base instalada!${N}"
say "   • Skills da agência em ~/.claude/skills"
say "   • NEXUS + squads-base no seu projeto"
say "   • Sua empresa (_opensquad/_memory) e suas squads: preservadas"
say ""
say "${B}Próximo:${N} reabra o Claude Code nesta pasta e digite ${B}/opensquad${N} —"
say "seus agentes continuam lá, agora com as skills da agência. 🚀"
