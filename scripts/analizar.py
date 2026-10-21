#!/usr/bin/env python3
"""
Análisis estadístico del corpus de runs verificados (Any%, Super Mario Bros. NES)
y de la progresión histórica del récord mundial.

Salidas:
  datos/procesados/resumen_estadistico.json   (todas las cifras del documento)
  datos/procesados/serie_anual.csv            (récord y mediana por año)
"""

import csv
import json
import math
import os
import statistics as st
from collections import defaultdict, Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(BASE, "datos", "procesados")

# --- Constantes de plataforma (NES NTSC) -------------------------------------
FPS_NTSC = 60.0988138974405      # Hz, NTSC NES
FRAME_RULE = 21                  # la transición de nivel ocurre en múltiplos de 21 frames
SEG_POR_FRAME = 1.0 / FPS_NTSC
SEG_POR_FRAME_RULE = FRAME_RULE / FPS_NTSC

# Óptimo teórico humano declarado por la comunidad (TAS sin L+R, teoría humana)
OPTIMO_TEORICO_S = 4 * 60 + 54.265

# Inicio histórico: primer récord documentado en la tabla de Wikipedia
INICIO_S = 5 * 60 + 14  # 5:14, enero 2004


def fmt_tiempo(s):
    if s is None:
        return None
    m = int(s // 60)
    resto = s - m * 60
    return f"{m}:{resto:06.3f}"


def cuantiles(xs, qs=(0.10, 0.25, 0.50, 0.75, 0.90, 0.99)):
    xs = sorted(xs)
    n = len(xs)
    out = {}
    for q in qs:
        i = min(n - 1, max(0, int(round(q * (n - 1)))))
        out[f"p{int(q*100)}"] = xs[i]
    return out


def cargar_runs():
    ruta = os.path.join(PROC, "runs_any_pcts_ntsc.csv")
    with open(ruta, encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    limpias = []
    for r in filas:
        try:
            t = float(r["tiempo_s"])
        except (TypeError, ValueError):
            continue
        if t <= 0:
            continue
        r["t"] = t
        r["anio"] = int((r["fecha"] or r["enviado"] or "0")[:4] or 0)
        limpias.append(r)
    return limpias


def analizar_corpus(runs):
    tiempos = [r["t"] for r in runs]
    n = len(tiempos)
    media = st.mean(tiempos)
    sd = st.pstdev(tiempos) if n else None
    q = cuantiles(tiempos)
    mejor = min(tiempos)

    # La cola extrema (runs de práctica, minijuegos, datos corruptos) infla la
    # desviación. Se calcula además una medida robusta sobre el núcleo competitivo.
    nucleo = [t for t in tiempos if t <= 600]      # runs de menos de 10 minutos
    media_nucleo = st.mean(nucleo) if nucleo else None
    sd_nucleo = st.pstdev(nucleo) if nucleo else None
    iqr = q["p75"] - q["p25"]
    mad = st.median([abs(t - q["p50"]) for t in tiempos])

    # Descomposición por años
    por_anio = defaultdict(list)
    for r in runs:
        if r["anio"]:
            por_anio[r["anio"]].append(r["t"])

    serie = []
    for anio in sorted(por_anio):
        ts = por_anio[anio]
        serie.append({
            "anio": anio,
            "n": len(ts),
            "mejor": min(ts),
            "mediana": st.median(ts),
            "media": st.mean(ts),
        })

    # Runs que alcanzan el óptimo teórico / umbrales
    umbrales = [300, 299, 298, 297, 296, 295, OPTIMO_TEORICO_S]
    sup = {f"<{u:.0f}s": sum(1 for t in tiempos if t < u) for u in umbrales}

    # Distribución por décimas de segundo (histograma)
    hist = Counter(math.floor(t * 10) / 10 for t in tiempos)
    histograma = [{"bin_s": k, "n": hist[k]} for k in sorted(hist)]

    # Jugadores más prolíficos
    jugadores = Counter(r["jugador"] for r in runs if r["jugador"])
    top_jugadores = jugadores.most_common(15)

    # Top 10 mejores runs con metadatos
    mejores = sorted(runs, key=lambda r: r["t"])[:15]
    top10 = [{
        "tiempo_s": r["t"], "tiempo": fmt_tiempo(r["t"]),
        "frames_vs_optimo": round((r["t"] - OPTIMO_TEORICO_S) * FPS_NTSC, 1),
        "jugador": r["jugador"], "fecha": r["fecha"], "emulado": r["emulado"],
        "id": r["id"],
    } for r in mejores]

    # Década / época
    recientes = [t for t in tiempos if t < 295]

    return {
        "n_runs": n,
        "mejor_s": mejor,
        "mejor_fmt": fmt_tiempo(mejor),
        "media_s": media,
        "mediana_s": st.median(tiempos),
        "desv_est_s": sd,
        "coef_variacion_pct": 100 * sd / media,
        "n_nucleo_hasta_600s": len(nucleo),
        "media_nucleo_s": media_nucleo,
        "desv_est_nucleo_s": sd_nucleo,
        "coef_variacion_nucleo_pct": (100 * sd_nucleo / media_nucleo) if media_nucleo else None,
        "iqr_s": iqr,
        "mad_s": mad,
        "max_s": max(tiempos),
        "cuantiles_s": q,
        "rango_s": max(tiempos) - min(tiempos),
        "n_bajo_295s": len(recientes),
        "umbrales_acumulados": sup,
        "histograma_decimas": histograma,
        "top_jugadores": top_jugadores,
        "top15_runs": top10,
        "serie_anual": serie,
        "anio_min": min(r["anio"] for r in runs if r["anio"]),
        "anio_max": max(r["anio"] for r in runs if r["anio"]),
    }


def analizar_wr():
    ruta = os.path.join(PROC, "wr_progresion_any.csv")
    with open(ruta, encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    for r in filas:
        r["t"] = float(r["segundos"])
        r["anio"] = int(r["anio"])
        r["mes"] = int(r["mes"])

    hitos = []
    for i, r in enumerate(filas):
        prev = filas[i - 1] if i else None
        ganancia = (prev["t"] - r["t"]) if prev else None
        hitos.append({
            "fecha": r["fecha_texto"],
            "tiempo_s": r["t"],
            "tiempo": fmt_tiempo(r["t"]),
            "runner": r["runner"],
            "ganancia_s": ganancia,
            "ganancia_frames": round(ganancia * FPS_NTSC, 1) if ganancia is not None else None,
            "gap_optimo_s": r["t"] - OPTIMO_TEORICO_S,
            "gap_optimo_frames": round((r["t"] - OPTIMO_TEORICO_S) * FPS_NTSC, 1),
            "notas": r["notas"],
        })

    # Ritmo de mejora por periodo
    def mejora_por_periodo(desde, hasta):
        sub = [h for h in hitos if desde <= _anio(h["fecha"]) <= hasta]
        if len(sub) < 2:
            return None
        a, b = sub[0]["tiempo_s"], sub[-1]["tiempo_s"]
        anios = _anio(sub[-1]["fecha"]) - _anio(sub[0]["fecha"]) or 1
        return {
            "periodo": f"{desde}-{hasta}",
            "n_records": len(sub),
            "ganancia_total_s": a - b,
            "ganancia_por_anio_s": (a - b) / anios,
            "frames_por_anio": (a - b) * FPS_NTSC / anios,
        }

    return {
        "n_registros": len(filas),
        "primer": hitos[0],
        "ultimo": hitos[-1],
        "hitos": hitos,
        "periodos": [mejora_por_periodo(2004, 2010), mejora_por_periodo(2011, 2016),
                     mejora_por_periodo(2017, 2020), mejora_por_periodo(2021, 2026)],
        "gap_inicial_frames": round((hitos[0]["tiempo_s"] - OPTIMO_TEORICO_S) * FPS_NTSC, 1),
        "gap_final_frames": hitos[-1]["gap_optimo_frames"],
        "cierre_pct": 100 * (1 - hitos[-1]["gap_optimo_s"] / (hitos[0]["tiempo_s"] - OPTIMO_TEORICO_S)),
    }


def _anio(fecha_txt):
    return int(fecha_txt.strip()[-4:])


def main():
    runs = cargar_runs()
    corpus = analizar_corpus(runs)
    wr = analizar_wr()

    resumen = {
        "constantes": {
            "fps_ntsc": FPS_NTSC,
            "frame_rule_frames": FRAME_RULE,
            "seg_por_frame": SEG_POR_FRAME,
            "seg_por_frame_rule": SEG_POR_FRAME_RULE,
            "optimo_teorico_s": OPTIMO_TEORICO_S,
            "optimo_teorico_fmt": fmt_tiempo(OPTIMO_TEORICO_S),
            "inicio_historico_s": INICIO_S,
            "inicio_historico_fmt": fmt_tiempo(INICIO_S),
        },
        "corpus": corpus,
        "record_mundial": wr,
    }
    ruta = os.path.join(PROC, "resumen_estadistico.json")
    json.dump(resumen, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=2, default=str)

    # Serie anual a CSV
    with open(os.path.join(PROC, "serie_anual.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["anio", "n", "mejor", "mediana", "media"])
        w.writeheader()
        for row in corpus["serie_anual"]:
            w.writerow({**row, "mejor": fmt_tiempo(row["mejor"]),
                        "mediana": fmt_tiempo(row["mediana"]),
                        "media": fmt_tiempo(row["media"])})

    print(f"Corpus: {corpus['n_runs']} runs NTSC, mejor {corpus['mejor_fmt']}")
    print(f"  mediana {fmt_tiempo(corpus['mediana_s'])}, desv {corpus['desv_est_s']:.3f}s, CV {corpus['coef_variacion_pct']:.2f}%")
    print(f"  runs bajo 295s: {corpus['n_bajo_295s']}")
    print(f"Récord: {wr['n_registros']} hitos; gap inicial {wr['gap_inicial_frames']:.0f} frames -> final {wr['gap_final_frames']:.0f} frames")
    print(f"  cierre de la brecha: {wr['cierre_pct']:.2f}%")
    for p in wr["periodos"]:
        if p:
            print(f"  {p['periodo']}: {p['n_records']} récords, {p['ganancia_por_anio_s']:.3f} s/año ({p['frames_por_anio']:.1f} frames/año)")
    print(f"\nresumen -> {ruta}")


if __name__ == "__main__":
    main()
