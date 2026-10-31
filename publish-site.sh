#!/usr/bin/env bash
# Публикация учебника: docs/ этого проекта -> https://github.com/grevinden/komplekty-ut-bp
# Правки всегда в docs/ (здесь мастер-копия), этот скрипт только переносит и пушит.
set -euo pipefail
SRC="$(cd "$(dirname "$0")/docs" && pwd)"
SITE="$(cd "$(dirname "$0")/../komplekty-ut-bp" && pwd)"
rsync -a --delete --exclude 'README.md' --exclude '.git' "$SRC/" "$SITE/"
cd "$SITE"
git add -A
git commit -m "${1:-Обновление учебника $(date +%Y-%m-%d)}"
git push
echo "Опубликовано: $SITE"
