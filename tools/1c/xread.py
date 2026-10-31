#!/usr/bin/env python3
"""Чтение текста окон 1С через accessibility-слой (Atspi), без OCR.

Запуск: xread.py [имя приложения]   (по умолчанию ищем 1cv8)
Печатает дерево видимых элементов с текстом.
"""
import sys
import gi
gi.require_version('Atspi', '2.0')
from gi.repository import Atspi

target = sys.argv[1] if len(sys.argv) > 1 else '1cv8'
SKIP = ('filler', 'panel', 'filler')


def walk(node, depth=0, out=None, limit=400):
    if node is None or len(out) > limit:
        return
    try:
        role = node.get_role_name()
        name = (node.get_name() or '').strip()
        try:
            txt = ''
            ti = node.get_text_iface() if hasattr(node, 'get_text_iface') else None
        except Exception:
            txt = ''
        if name and role not in SKIP:
            out.append('  ' * depth + f'[{role}] {name[:200]}')
        for i in range(node.get_child_count()):
            walk(node.get_child_at_index(i), depth + 1, out, limit)
    except Exception:
        pass


desk = Atspi.get_desktop(0)
found = False
for i in range(desk.get_child_count()):
    try:
        app = desk.get_child_at_index(i)
        nm = app.get_name() or ''
    except Exception:
        continue
    if target.lower() not in nm.lower():
        continue
    found = True
    print(f'=== приложение: {nm} (окон: {app.get_child_count()}) ===')
    out = []
    for w in range(app.get_child_count()):
        walk(app.get_child_at_index(w), 0, out)
    print('\n'.join(out) if out else '(текста через Atspi нет)')

if not found:
    apps = []
    for i in range(desk.get_child_count()):
        try:
            apps.append(desk.get_child_at_index(i).get_name())
        except Exception:
            pass
    print(f'приложение «{target}» не найдено; в сессии:', apps)
