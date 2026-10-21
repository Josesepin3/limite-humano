#!/usr/bin/env python3
"""
Extrae todos los runs VERIFICADOS de la categoría Any% de Super Mario Bros. (NES)
en speedrun.com, y los exporta como JSONL crudo + CSV procesado.

Fuente: speedrun.com API v1
  - Juego:  om1m3625  (Super Mario Bros. NES)
  - Categoría: w20p0zkn (Any%)
  - Variable "Version": onvvdymn  -> 013zwgxq = NTSC, rqvj686q = PAL

Uso:  python3 extraer_runs.py
Salida:
  datos/crudos/runs_any_pcts.jsonl   (1 objeto JSON por línea, crudo)
  datos/procesados/runs_any_pcts.csv (campos aplanados, listo para análisis)
"""

import csv
import json
import os
import subprocess
import time

API = "https://www.speedrun.com/api/v1"
JUEGO = "om1m3625"
CATEGORIA = "w20p0zkn"
VAR_VERSION = "onvvdymn"
VAL_NTSC = "013zwgxq"
VAL_PAL = "rqvj686q"

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRUDOS = os.path.join(BASE, "datos", "crudos")
PROCESADOS = os.path.join(BASE, "datos", "procesados")
os.makedirs(CRUDOS, exist_ok=True)
os.makedirs(PROCESADOS, exist_ok=True)

USER_AGENT = "tesis-limite-humano (investigación académica)"


def get(url, intentos=5):
    """GET con reintentos. Usa curl como transporte (el endpoint rechaza urllib)."""
    for i in range(intentos):
        p = subprocess.run(
            ["curl", "-sS", "--max-time", "60", "-A", USER_AGENT, url],
            capture_output=True, text=True,
        )
        if p.returncode == 0 and p.stdout.strip().startswith(("{", "[")):
            return json.loads(p.stdout)
        print(f"   ! reintentando ({p.returncode} {p.stderr.strip()[:80]}) ...")
        time.sleep(2 ** i)
    raise RuntimeError(f"no se pudo obtener: {url}")


def extraer_todo():
    base = (f"{API}/runs?game={JUEGO}&category={CATEGORIA}"
            f"&status=verified&max=200&orderby=date&direction=asc&embed=players")
    todos = []
    offset = 0
    while True:
        j = get(f"{base}&offset={offset}")
        lote = j.get("data", [])
        if not lote:
            break
        todos.extend(lote)
        print(f"  offset={offset:6d}  +{len(lote):4d}  (total {len(todos)})")
        offset += 200
        time.sleep(0.35)  # cortesía hacia el servidor público
    return todos


def aplanar(r):
    vals = r.get("values", {}) or {}
    region = vals.get(VAR_VERSION)

    def _nombre(p):
        if isinstance(p, str):
            return p
        if p.get("rel") == "guest":
            return p.get("name") or "invitado"
        names = p.get("names") or {}
        return names.get("international") or names.get("en-gb") or p.get("name") or "?"

    pl = r.get("players")
    lista = pl.get("data", pl) if isinstance(pl, dict) else (pl or [])
    players = "+".join(_nombre(p) for p in lista)

    t = r.get("times", {}) or {}
    sys_ = r.get("system", {}) or {}
    return {
        "id": r.get("id"),
        "weblink": r.get("weblink"),
        "fecha": r.get("date") or "",
        "enviado": (r.get("submitted") or "")[:10],
        "tiempo_s": t.get("primary_t"),
        "rta_s": t.get("realtime_t"),
        "jugador": players,
        "emulado": 1 if sys_.get("emulated") else 0,
        "plataforma": sys_.get("platform") or "",
        "region_var": region or "",
        "region_txt": {VAL_NTSC: "NTSC", VAL_PAL: "PAL"}.get(region, "sin dato"),
        "verificado": (r.get("status") or {}).get("status", ""),
        "video": 1 if r.get("videos") else 0,
        "comentario": (r.get("comment") or "").replace("\n", " ")[:300],
    }


def main():
    print("Extrayendo runs verificados de Any% (Super Mario Bros. NES) ...")
    crudos = extraer_todo()
    print(f"TOTAL crudos: {len(crudos)}")

    with open(os.path.join(CRUDOS, "runs_any_pcts.jsonl"), "w", encoding="utf-8") as f:
        for r in crudos:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    filas = [aplanar(r) for r in crudos]
    nts = [r for r in filas if r["region_txt"] == "NTSC"]
    pals = [r for r in filas if r["region_txt"] == "PAL"]
    print(f"NTSC: {len(nts)}   PAL: {len(pals)}   sin dato: {len(filas) - len(nts) - len(pals)}")

    campos = list(filas[0].keys())
    for tag, sub in (("any_pcts_todos", filas), ("any_pcts_ntsc", nts)):
        ruta = os.path.join(PROCESADOS, f"runs_{tag}.csv")
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=campos)
            w.writeheader()
            w.writerows(sub)
        print(f"  -> {ruta}  ({len(sub)} filas)")


if __name__ == "__main__":
    main()
