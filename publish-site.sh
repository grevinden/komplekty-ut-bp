#!/usr/bin/env bash
# Публикация учебника. Один репозиторий: книга лежит в docs/, GitHub Pages
# собирает сайт из папки /docs ветки main (Settings -> Pages -> /docs).
# Скрипт коммитит изменения, пушит и ждёт сборку Pages.
set -euo pipefail
cd "$(dirname "$0")"

MSG="${1:-Обновление учебника $(date +%Y-%m-%d)}"
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -q -m "$MSG"
  echo "Коммит: $(git log -1 --format='%h %s')"
else
  echo "Незакоммиченных изменений нет, публикую HEAD $(git rev-parse --short HEAD)"
fi

git push -q origin main
HEAD7="$(git rev-parse --short=7 HEAD)"
echo "Запушено в origin/main ($HEAD7) -> https://grevinden.github.io/komplekty-ut-bp/"

# Pages собирает 30-60 с. REST по имени репозитория иногда отдаёт 404 из-за
# кеша GitHub, поэтому есть запасной путь по числовому ID репозитория.
for _ in $(seq 1 30); do
  s="$(gh api "repos/grevinden/komplekty-ut-bp/pages/builds/latest" \
        --jq '.status + " " + .commit[0:7]' 2>/dev/null || true)"
  if [ -z "$s" ]; then
    s="$(gh api "repositories/1440639007/pages/builds/latest" \
          --jq '.status + " " + .commit[0:7]' 2>/dev/null || true)"
  fi
  case "$s" in
    "built $HEAD7") echo "Pages: собрано $HEAD7"; exit 0 ;;
    "") ;;
    *) echo "Pages: $s" ;;
  esac
  sleep 10
done
echo "Сборка Pages не подтвердилась за 5 минут — проверьте статус вручную"
