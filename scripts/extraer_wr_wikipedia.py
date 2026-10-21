#!/usr/bin/env python3
"""
Extrae la progresión histórica del récord mundial de Any% de Super Mario Bros.
desde la tabla de la Wikipedia en inglés, y la normaliza a CSV.

Fuente: https://en.wikipedia.org/wiki/Super_Mario_Bros._speedrunning
        (sección "Any% world record progression"), texto wiki crudo.
Salida: datos/procesados/wr_progresion_any.csv
"""

import csv
import json
import os
import re
import subprocess

URL = ("https://en.wikipedia.org/w/index.php"
       "?title=Super_Mario_Bros._speedrunning&action=raw")
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRUDOS = os.path.join(BASE, "datos", "crudos")
PROCESADOS = os.path.join(BASE, "datos", "procesados")
os.makedirs(CRUDOS, exist_ok=True)
os.makedirs(PROCESADOS, exist_ok=True)

MESES = {m: i + 1 for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June",
     "July", "August", "September", "October", "November", "December"])}


def descargar():
    p = subprocess.run(["curl", "-sS", "--max-time", "60", "-A", "tesis-limite-humano", URL],
                       capture_output=True, text=True, check=True)
    return p.stdout


def limpiar_notas(s):
    s = re.sub(r"<ref[\s\S]*?</ref>", "", s)
    s = re.sub(r"<ref[^>]*/>", "", s)
    s = re.sub(r"\[\[([^\]|]*\|)?([^\]]*)\]\]", r"\2", s)
    s = re.sub(r"\{\{[^}]*\}\}", "", s)
    s = re.sub(r"<[^>]+>", "", s)
    return " ".join(s.split()).strip()


def parsear_fecha(txt):
    """Devuelve (año, mes) a partir de 'August 13, 2026' o 'August 2026'."""
    m = re.search(r"([A-Z][a-z]+)\s+(\d{1,2},\s*)?(\d{4})", txt)
    if not m:
        return None, None
    return int(m.group(3)), MESES.get(m.group(1))


def a_segundos(tiempo):
    """'4:54.332' -> 294.332"""
    if not tiempo:
        return None
    m = re.match(r"(\d+):(\d{2})(?:\.(\d+))?$", tiempo)
    if not m:
        return None
    min_, seg, frac = m.group(1), m.group(2), (m.group(3) or "0")
    return int(min_) * 60 + int(seg) + float("0." + frac)


def main():
    txt = descargar()
    open(os.path.join(CRUDOS, "wikipedia_smb_speedrunning.wiki"), "w", encoding="utf-8").write(txt)

    ini = txt.index("Any% world record progression")
    tabla = txt[ini: txt.index("|}", ini) + 2]

    filas = []
    for i, blk in enumerate(tabla.split("\n|-")[1:], start=1):
        celdas = [c.strip() for c in blk.split("\n|")[1:]]
        if len(celdas) < 3:
            continue
        fecha_txt, tiempo_txt, runner = celdas[0], celdas[1], celdas[2]
        notas = limpiar_notas(celdas[3]) if len(celdas) > 3 else ""
        visible = re.sub(r"<ref[\s\S]*?</ref>", "", tiempo_txt)
        m = re.search(r"(\d+:\d{2}(?:\.\d+)?)", visible)
        if not m:
            continue
        tiempo = m.group(1)
        anio, mes = parsear_fecha(fecha_txt)
        filas.append({
            "orden": i,
            "fecha_texto": fecha_txt,
            "anio": anio,
            "mes": mes,
            "tiempo": tiempo,
            "segundos": a_segundos(tiempo),
            "runner": limpiar_notas(runner),
            "notas": notas,
        })

    filas.sort(key=lambda r: (r["anio"] or 0, r["mes"] or 0))
    ruta = os.path.join(PROCESADOS, "wr_progresion_any.csv")
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)

    print(f"{len(filas)} registros -> {ruta}")
    print(f"  primero: {filas[0]['fecha_texto']} {filas[0]['tiempo']} ({filas[0]['runner']})")
    print(f"  último : {filas[-1]['fecha_texto']} {filas[-1]['tiempo']} ({filas[-1]['runner']})")

    meta = {
        "fuente": "Wikipedia, Super Mario Bros. speedrunning, tabla Any% world record progression",
        "url": URL,
        "n_registros": len(filas),
        "nota": "Solo incluye registros de récord mundial; no incluye todos los runs verificados.",
    }
    json.dump(meta, open(os.path.join(PROCESADOS, "wr_progresion_meta.json"), "w"), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
