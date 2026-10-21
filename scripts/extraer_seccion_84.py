#!/usr/bin/env python3
"""
Extrae la distribución de tiempos del 8-4 IL (categoría extensions de SMB),
RESOLVIENDO los nombres de los jugadores.

El 8-4 es la ÚNICA sección del recorrido Any% sin frame rule. Por eso es la
sección donde el error humano no se redondea y donde se concentra toda la
brecha residual. Su distribución de tiempos es, por tanto, la mejor medición
empírica disponible de la precisión humana en la parte crítica del recorrido.

Fuentes:
  - Juego "smbce" (Super Mario Bros. Category Extensions): y658506e
  - Categoría "8-4 IL": rklezor2

Salida:
  datos/crudos/il_84.jsonl
  datos/procesados/il_84.csv
"""

import csv
import json
import os
import subprocess
import time

API = "https://www.speedrun.com/api/v1"
JUEGO = "y658506e"
CATEGORIA = "rklezor2"
FPS = 60.0988138974405
USER_AGENT = "tesis-limite-humano (investigacion academica)"

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRUDOS = os.path.join(BASE, "datos", "crudos")
PROC = os.path.join(BASE, "datos", "procesados")

_cache_usuarios = {}


def get(url, intentos=5):
    for i in range(intentos):
        p = subprocess.run(["curl", "-sS", "--max-time", "60", "-A", USER_AGENT, url],
                           capture_output=True, text=True)
        if p.returncode == 0 and p.stdout.strip().startswith(("{", "[")):
            return json.loads(p.stdout)
        time.sleep(2 ** i)
    raise RuntimeError(f"no se pudo obtener: {url}")


def nombre_usuario(uid):
    """Resuelve un id de usuario a su nombre internacional."""
    if uid in _cache_usuarios:
        return _cache_usuarios[uid]
    nombre = uid
    try:
        j = get(f"{API}/users/{uid}")
        n = (j.get("data") or {}).get("names") or {}
        nombre = n.get("international") or n.get("en-gb") or uid
    except Exception:  # noqa: BLE001
        pass
    _cache_usuarios[uid] = nombre
    return nombre


def resolver_jugadores(players):
    partes = []
    for p in players or []:
        if isinstance(p, str):
            partes.append(p)
        elif p.get("rel") == "user" and p.get("id"):
            partes.append(nombre_usuario(p["id"]))
        else:
            partes.append(p.get("name") or "invitado")
    return "+".join(partes)


def main():
    j = get(f"{API}/leaderboards/{JUEGO}/category/{CATEGORIA}?top=200")
    runs = j["data"]["runs"]

    crudos = []
    for x in runs:
        run = x["run"]
        crudos.append({
            "id": run["id"],
            "place": x.get("place"),
            "tiempo_s": run["times"]["primary_t"],
            "frames": round(run["times"]["primary_t"] * FPS),
            "jugador": resolver_jugadores(run.get("players")),
            "fecha": run.get("date"),
            "emulado": 1 if (run.get("system") or {}).get("emulated") else 0,
            "comentario": (run.get("comment") or "").replace("\n", " ")[:400],
        })

    os.makedirs(CRUDOS, exist_ok=True)
    os.makedirs(PROC, exist_ok=True)
    with open(os.path.join(CRUDOS, "il_84.jsonl"), "w", encoding="utf-8") as f:
        for r in crudos:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    mejor = min(r["frames"] for r in crudos)
    for r in crudos:
        r["delta_frames"] = r["frames"] - mejor

    campos = ["id", "place", "tiempo_s", "frames", "delta_frames",
              "jugador", "fecha", "emulado", "comentario"]
    with open(os.path.join(PROC, "il_84.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(crudos)

    empatan = [r for r in crudos if r["delta_frames"] == 0]
    print(f"8-4 IL: {len(crudos)} runs")
    print(f"  mejor: {mejor} frames ({mejor/FPS:.3f} s)")
    print(f"  empatan el óptimo: {len(empatan)} ({100*len(empatan)/len(crudos):.2f} %)")
    for r in empatan:
        print(f"    - {r['jugador']} ({r['fecha']})")
    print(f"  delta medio: {sum(r['delta_frames'] for r in crudos)/len(crudos):.2f} frames")
    print(f"  -> {os.path.join(PROC, 'il_84.csv')}")


if __name__ == "__main__":
    main()
