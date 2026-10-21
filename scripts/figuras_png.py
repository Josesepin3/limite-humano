#!/usr/bin/env python3
"""
Convierte las figuras SVG a PNG para incrustarlas en el documento.

Las figuras se generan primero con figuras.py (SVG, vectorial). Este script
produce la versión rasterizada que Markdown y Word pueden mostrar.

Requiere: rsvg-convert (paquete librsvg) o ImageMagick (convert).

Uso:
    python3 scripts/figuras_png.py
"""

import os
import shutil
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(BASE, "documento", "figuras")

# Escala 2x para que el PNG se vea nítido en pantallas de alta densidad
ESCALA = 2


def conversor():
    """Devuelve (nombre, función) del primer conversor disponible."""
    if shutil.which("rsvg-convert"):
        return "rsvg-convert", lambda src, dst: [
            "rsvg-convert", "-z", str(ESCALA), src, "-o", dst]
    if shutil.which("convert"):
        return "convert", lambda src, dst: [
            "convert", "-density", "180", src, dst]
    if shutil.which("magick"):
        return "magick", lambda src, dst: [
            "magick", "-density", "180", src, dst]
    return None, None


def main():
    nombre, conv = conversor()
    if not conv:
        print("ERROR: se necesita rsvg-convert o ImageMagick para generar los PNG.")
        print("  Arch:   sudo pacman -S librsvg")
        print("  Debian: sudo apt install librsvg2-bin")
        sys.exit(1)

    svgs = sorted(f for f in os.listdir(FIG) if f.endswith(".svg"))
    if not svgs:
        print("No hay SVG en", FIG, "- ejecuta primero figuras.py")
        sys.exit(1)

    print(f"Convirtiendo {len(svgs)} figuras con {nombre} "
          f"(escala {ESCALA}x)...")
    for f in svgs:
        src = os.path.join(FIG, f)
        dst = os.path.join(FIG, f[:-4] + ".png")
        subprocess.run(conv(src, dst), check=True)
        print(f"  OK {os.path.basename(dst)}  "
              f"({os.path.getsize(dst) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
