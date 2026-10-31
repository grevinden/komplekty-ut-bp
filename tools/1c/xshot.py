#!/usr/bin/env python3
"""Снимок X-экрана через Gdk + кроп по геометрии окна.

Запуск: xshot.py <файл.png> [XID]
Если задан XID (0x...), берётся геометрия окна из перебора детей root'а Gdk.
"""
import gi
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk
import sys


def grab_root():
    display = Gdk.Display.get_default()
    screen = display.get_default_screen()
    w, h = screen.get_width(), screen.get_height()
    root = screen.get_root_window()
    pb = Gdk.pixbuf_get_from_window(root, 0, 0, w, h)
    return pb


def find_geom(xid):
    """Геометрия окна по XID через дерево X (Gdk не даёт, читаем xwininfo)."""
    import subprocess, re
    out = subprocess.run(["xwininfo", "-root", "-tree"], capture_output=True,
                         text=True, env={"DISPLAY": ":0", "PATH": "/usr/bin:/bin"}).stdout
    for line in out.splitlines():
        if hex(xid) in line.split():
            m = re.search(r"(\d+)x(\d+)\+(-?\d+)\+(-?\d+)", line)
            if m:
                return tuple(int(v) for v in m.groups())
    return None


def main():
    out = sys.argv[1]
    pb = grab_root()
    if pb is None:
        print("не удалось получить снимок", file=sys.stderr)
        sys.exit(2)
    pb.savev(out, "png", [], [])
    print("snapshot", out, pb.get_width(), "x", pb.get_height())
    if len(sys.argv) > 2:
        xid = int(sys.argv[2], 16) if sys.argv[2].startswith("0x") else int(sys.argv[2])
        geom = find_geom(xid)
        if geom:
            w, h, x, y = geom
            from PIL import Image
            im = Image.open(out)
            x = max(x, 0); y = max(y, 0)
            crop = im.crop((x, y, min(x + w, im.width), min(y + h, im.height)))
            crop = crop.resize((crop.width * 2, crop.height * 2), Image.LANCZOS)
            crop.save(out.replace(".png", "_win.png"))
            print("window crop", out.replace(".png", "_win.png"), geom)
        else:
            print("окно не найдено", file=sys.stderr)


main()
