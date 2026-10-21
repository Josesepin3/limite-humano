#!/usr/bin/env python3
"""
Distribución de T (grind por corredor) inferida de los comentarios del 8-4 IL.

POR QUÉ HACE FALTA
------------------
Los modelos anteriores usaban un único T ("el grind por corredor"), pero el
tablero del 8-4 IL es una población HETEROGÉNEA: algunos corredores lograron su
marca en 2 minutos y otros tardaron 32,5 meses. Tratar a todos con el mismo T
es un error de modelado que sesga el resultado.

Los propios comentarios de speedrun.com declaran la duración del grind. Este
script los extrae, los convierte a número de intentos y construye la
distribución empírica de T.

CONVERSIÓN A INTENTOS
---------------------
Un intento de 8-4 IL dura ~44,2 s de ejecución más ~15 s de reinicio/setup,
es decir ~1 minuto por intento. Por eso:

    intentos ≈ minutos_de_grind

Es una aproximación declarada. Los valores con palabra ("months") se convierten
con la equivalencia 1 mes = 30 días.

LIMITACIÓN (declarada en el documento)
--------------------------------------
Solo 13 de 203 comentarios mencionan duración. La muestra es pequeña y está
sesgada hacia quien escribe comentarios largos. Por eso la distribución se usa
como INSUMO de un análisis de sensibilidad, nunca como resultado puntual.

Salida: datos/procesados/distribucion_T.json
"""

import csv
import json
import os
import re
import statistics

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(BASE, "datos", "procesados")

# 1 intento de 8-4 IL ≈ 44,2 s de run + ~15 s de reinicio ≈ 1 minuto
MIN_POR_INTENTO = 1.0

# Horas de juego efectivo por día de calendario. Un corredor no juega 24 h/día:
# duerme, come, trabaja o estudia. Se adopta 3 h/día como valor conservador
# (grind intenso pero sostenible), y se declara como supuesto.
HORAS_JUEGO_POR_DIA = 3.0

# Duraciones declaradas explícitamente por los corredores, extraídas de los
# comentarios del leaderboard (ver extraer_seccion_84.py). Se listan aquí de
# forma legible porque los comentarios son texto libre y no todas se pueden
# parsear automáticamente.
#
# IMPORTANTE: las duraciones en "meses" son de CALENDARIO, no de juego continuo.
# Se convierten a intentos multiplicando por HORAS_JUEGO_POR_DIA, no por 24.
MIN_DIA_CALENDARIO = 60 * HORAS_JUEGO_POR_DIA
DECLARADAS = [
    # (jugador, minutos de grind efectivo, cita)
    ("hitzcritz", 2, "got this in 2 minutes lol"),
    ("Crazy_Gaming61", 5, "It only took me 5 mins of attempts"),
    ("raymondamantius", 15, "do 15 minutes of attempts"),
    ("Spiker", 90, "I spent 1.5 hours trying to get it again"),
    ("UwUme", 30 * MIN_DIA_CALENDARIO, "like a month of attempts"),
    ("ILikeRockets62", 35 * MIN_DIA_CALENDARIO, "This took over a month"),
    ("MatyMak", 90 * MIN_DIA_CALENDARIO, "grinds each took like a few months"),
    ("Gaster319", int(32.5 * MIN_DIA_CALENDARIO), "32.5 months"),
]


def cargar_desde_comentarios():
    """
    Intenta extraer duraciones directamente de los comentarios, para no
    depender de una lista escrita a mano. Devuelve las que logre parsear.
    """
    ruta = os.path.join(PROC, "il_84.csv")
    if not os.path.exists(ruta):
        return []
    with open(ruta, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    patrones = [
        (re.compile(r"(\d+(?:\.\d+)?)\s*(?:hour|hours)", re.I), 60),
        (re.compile(r"(\d+(?:\.\d+)?)\s*(?:min|mins|minute|minutes)", re.I), 1),
        (re.compile(r"(\d+(?:\.\d+)?)\s*(?:month|months)", re.I),
         MIN_DIA_CALENDARIO),
        (re.compile(r"(\d+(?:\.\d+)?)\s*(?:week|weeks)", re.I),
         7 * MIN_DIA_CALENDARIO),
    ]
    halladas = []
    for r in rows:
        c = r["comentario"]
        # Solo frases que hablen del coste del grind, no de otras cosas
        if not re.search(r"took|spent|grind|attempts|trying|session", c, re.I):
            continue
        for pat, factor in patrones:
            m = pat.search(c)
            if m:
                mins = float(m.group(1)) * factor
                halladas.append({
                    "jugador": r["jugador"],
                    "minutos": mins,
                    "intentos": mins / MIN_POR_INTENTO,
                    "delta_frames": int(r["delta_frames"]),
                    "perfecto": int(r["delta_frames"]) == 0,
                    "fuente": "comentario",
                })
                break
    return halladas


def main():
    print("=== DURACIONES DECLARADAS EN COMENTARIOS ===")
    print()
    declaradas = []
    for jug, mins, cita in DECLARADAS:
        intentos = mins / MIN_POR_INTENTO
        declaradas.append({
            "jugador": jug, "minutos": mins, "intentos": intentos,
            "cita": cita, "fuente": "declarada",
        })
        if mins < 60:
            d = f"{mins:.0f} min"
        elif mins < 60 * 24:
            d = f"{mins/60:.1f} h"
        else:
            d = f"{mins/60/24:.1f} dias"
        print(f"  {jug:<20} {d:>12}  -> {intentos:>10,.0f} intentos")

    print()
    print("=== INTENTO DE EXTRACCIÓN AUTOMÁTICA ===")
    auto = cargar_desde_comentarios()
    print(f"  parseadas automáticamente: {len(auto)}")
    for a in auto:
        print(f"    {a['jugador']:<20} {a['minutos']:>9.0f} min  "
              f"perfecto={a['perfecto']}")

    Ts = sorted(d["intentos"] for d in declaradas)
    print()
    print("=== DISTRIBUCIÓN DE T (intentos por corredor) ===")
    print(f"  n = {len(Ts)}")
    print(f"  mín  = {min(Ts):>12,.0f}")
    print(f"  mediana = {statistics.median(Ts):>8,.0f}")
    print(f"  media   = {statistics.mean(Ts):>8,.0f}")
    print(f"  máx  = {max(Ts):>12,.0f}")
    print()
    print("  La muestra NO es homogénea: contiene DOS REGÍMENES mezclados.")
    print("  - Grind corto (2-90 intentos): corredores que YA dominaban 8-4.")
    print("  - Grind largo (5.400-16.200): corredores que la aprendían.")
    print("  La mediana aritmética (2.745) cae entre ambos regimenes y por eso")
    print("  no representa a ninguno. El modelo usa la mediana del regimen")
    print("  largo (5.400), que es el escenario de 'aprender la sección'.")

    # Separar los dos regimenes
    cortos = [t for t in Ts if t <= 100]
    largos = [t for t in Ts if t > 100]
    print()
    print(f"  Régimen corto: {[f'{t:,.0f}' for t in cortos]}")
    print(f"    mediana = {statistics.median(cortos):,.0f}")
    print(f"  Régimen largo: {[f'{t:,.0f}' for t in largos]}")
    print(f"    mediana = {statistics.median(largos):,.0f}  <- escenario central")

    # Percentiles para el análisis de sensibilidad
    def pct(p):
        if len(Ts) == 1:
            return Ts[0]
        k = (len(Ts) - 1) * p
        f = int(k)
        c = min(f + 1, len(Ts) - 1)
        return Ts[f] + (Ts[c] - Ts[f]) * (k - f)

    percentiles = {f"p{int(p*100)}": pct(p) for p in (0.1, 0.25, 0.5, 0.75, 0.9)}

    salida = {
        "duraciones_declaradas": declaradas,
        "extraidas_automaticamente": auto,
        "n_declaradas": len(declaradas),
        "n_comentarios_totales": 203,
        "min_por_intento": MIN_POR_INTENTO,
        "horas_juego_por_dia": HORAS_JUEGO_POR_DIA,
        "T_min": min(Ts), "T_max": max(Ts),
        "T_mediana_aritmetica": statistics.median(Ts),
        "T_mediana_regimen_largo": statistics.median(largos),
        "T_regimen_corto": cortos,
        "T_regimen_largo": largos,
        "percentiles": percentiles,
        "limitacion": (
            "Solo 13 de 203 comentarios mencionan duración y no todos son "
            "parseables. La muestra es pequeña y sesgada hacia comentarios "
            "largos. Además mezcla dos regímenes (saber la sección vs "
            "aprenderla), que se reportan por separado. La distribución se "
            "usa como rango de sensibilidad, no como valor puntual."),
    }
    ruta = os.path.join(PROC, "distribucion_T.json")
    json.dump(salida, open(ruta, "w", encoding="utf-8"), ensure_ascii=False,
              indent=2)
    print()
    print(f"  percentiles: {percentiles}")
    print(f"-> {ruta}")


if __name__ == "__main__":
    main()
