#!/bin/bash
# Запуск 1С с технологическим журналом платформы.
# Запуск: run1c.sh <ENTERPRISE|DESIGNER> <путь к базе> <выходной техжурнал> [доп. аргументы...]
BIN=/opt/1cv8/x86_64/8.3.27.2342/1cv8
MODE=$1; BASE=$2; TL=$3; shift 3
export DISPLAY=:0
export XAUTHORITY=/run/user/1000/.mutter-Xwaylandauth.TPGBY3
rm -f "$TL"
# имя переменной начинается с цифры — только через env
timeout 120 env "1C_TECH_LOG=$TL" "$BIN" "$MODE" "/F$BASE" /N"Администратор" \
  /DisableStartupDialogs /DisableStartupMessages "$@"
echo "exit=$?"
