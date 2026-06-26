#!/usr/bin/env bash
# sync-modules.sh — (INTERNO do Alex) Regenera modulos/ a partir do kit.
#
# O pacote completo BUNDLA cópias dos módulos. Em vez de editar à mão dentro de
# modulos/, edite cada módulo no kit (../<modulo>) e rode isto pra recopiar.
# Assim o full fica sempre igual aos módulos individuais.
#
# Uso (de dentro do agencia-ia-full/): scripts/sync-modules.sh /caminho/para/agencia-ia-kit
set -euo pipefail

KIT="${1:?uso: sync-modules.sh /caminho/para/agencia-ia-kit}"
HERE="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$HERE/modulos"

MODULES=(agencia-ia-base modulo-seo-content modulo-tracking modulo-crm-funnels
         modulo-meta-ads modulo-google-ads modulo-windsor-gmb modulo-funil-cockpits)

for m in "${MODULES[@]}"; do
  [[ -d "$KIT/$m" ]] || { echo "✗ não achei $KIT/$m"; exit 1; }
  rm -rf "$DEST/$m"
  rsync -a --exclude '.git' --exclude 'node_modules' --exclude '*.bak' --exclude 'dist' \
        "$KIT/$m" "$DEST/"
  echo "✓ sincronizado: $m"
done

echo ""
echo "Agora rode a varredura antes de commitar:"
echo "  scripts/scan-secrets.sh ."
