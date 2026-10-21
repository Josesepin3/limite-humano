#!/usr/bin/env python3
"""
Genera las figuras del documento a partir de los datos procesados.
Salida: documento/figuras/*.svg  (vectorial, sin dependencias externas)
"""

import csv
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(BASE, "datos", "procesados")
FIG = os.path.join(BASE, "documento", "figuras")
os.makedirs(FIG, exist_ok=True)

FPS = 60.0988138974405
OPT = 294.265


def svg(ancho, alto, contenido):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho} {alto}" '
            f'width="{ancho}" height="{alto}" font-family="system-ui,sans-serif">'
            f'<rect width="{ancho}" height="{alto}" fill="white"/>{contenido}</svg>')


def linea(x1, y1, x2, y2, color="#333", w=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="{w}"{d}/>')


def texto(x, y, s, size=11, color="#333", anchor="start", weight="normal"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}" font-weight="{weight}">{s}</text>')


# ---------------------------------------------------------------- Figura 1
def fig_convergencia():
    """Récord mundial vs. óptimo teórico a lo largo del tiempo."""
    with open(os.path.join(PROC, "wr_progresion_any.csv"), encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    pts = []
    for r in filas:
        anio, mes = int(r["anio"]), int(r["mes"])
        pts.append((anio + (mes - 1) / 12, float(r["segundos"])))

    W, H = 820, 450
    ml, mr, mt, mb = 78, 30, 40, 55
    x0, x1 = 2004.0, 2026.7
    y0, y1 = 293.5, 315.5

    def X(x):
        return ml + (x - x0) / (x1 - x0) * (W - ml - mr)

    def Y(y):
        return H - mb - (y - y0) / (y1 - y0) * (H - mt - mb)

    c = [texto(W / 2, 24, "Convergencia del récord mundial hacia el óptimo teórico (Any%)",
               15, "#111", "middle", "600")]
    for y in [294, 296, 298, 300, 302, 304, 306, 308, 310, 312, 314]:
        yy = Y(y)
        c.append(linea(ml, yy, W - mr, yy, "#eee", 1))
        m, s = divmod(y, 60)
        c.append(texto(ml - 8, yy + 4, f"{int(m)}:{int(s):02d}", 10, "#666", "end"))
    for x in range(2004, 2027, 2):
        xx = X(x)
        c.append(linea(xx, mt, xx, H - mb, "#f4f4f4", 1))
        c.append(texto(xx, H - mb + 18, str(x), 10, "#666", "middle"))

    # Área de brecha
    ruta_d = "M " + " L ".join(f"{X(a):.1f} {Y(t):.1f}" for a, t in pts)
    ruta_d += f" L {X(pts[-1][0]):.1f} {Y(OPT):.1f} L {X(pts[0][0]):.1f} {Y(OPT):.1f} Z"
    c.append(f'<path d="{ruta_d}" fill="#e8f0fe" opacity="0.85"/>')

    # Óptimo
    c.append(linea(ml, Y(OPT), W - mr, Y(OPT), "#c0392b", 2, "6,4"))
    c.append(texto(W - mr - 4, Y(OPT) - 7, "Óptimo teórico 4:54.265", 10, "#c0392b", "end", "600"))

    # Serie
    c.append('<polyline points="'
             + " ".join(f"{X(a):.1f},{Y(t):.1f}" for a, t in pts)
             + '" fill="none" stroke="#1a73e8" stroke-width="2.2"/>')
    for i, (a, t) in enumerate(pts):
        if i in (0, len(pts) - 1) or t in (300.355, 299.69, 294.631):
            c.append(f'<circle cx="{X(a):.1f}" cy="{Y(t):.1f}" r="3.4" fill="#1a73e8"/>')

    anotaciones = [
        (X(2004.2), Y(314) - 12, "5:14 — primer registro (2004)", "start", "#1a73e8"),
        (X(2011.0), Y(299.69) + 20, "4:59.690 — bajo 5 min (2010)", "middle", "#1a73e8"),
        (X(2019.5), Y(295.9) + 26, "4:55.913 (2018)", "middle", "#1a73e8"),
        (X(2026.6), Y(294.332) - 14, "4:54.332 — a 4 frames (2026)", "end", "#1a73e8"),
    ]
    for x, y, s, an, col in anotaciones:
        c.append(texto(x, y, s, 10.5, col, an, "600"))

    # Flecha de brecha final
    c.append(f'<path d="M {X(2026.2):.1f} {Y(OPT):.1f} L {X(2026.2):.1f} {Y(294.332):.1f}" '
             f'stroke="#c0392b" stroke-width="1.4" marker-end="url(#fl)"/>')
    c.append(texto(X(2022.0), Y(294.6) + 12, "brecha final: 4 frames (0,067 s)", 10.5, "#c0392b", "middle", "600"))

    c.append(texto(W / 2, H - 12, "Año", 11, "#555", "middle"))
    c.append(f'<defs><marker id="fl" markerWidth="8" markerHeight="8" refX="4" refY="4" '
             f'orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#c0392b"/></marker></defs>')
    open(os.path.join(FIG, "fig1_convergencia.svg"), "w", encoding="utf-8").write(svg(W, H, "".join(c)))


# ---------------------------------------------------------------- Figura 2
def fig_ritmo():
    """Frames ganados por año, por periodo."""
    with open(os.path.join(PROC, "resumen_estadistico.json"), encoding="utf-8") as f:
        wr = json.load(f)["record_mundial"]
    periodos = [p for p in wr["periodos"] if p]
    W, H = 780, 380
    ml, mr, mt, mb = 80, 30, 50, 70
    vals = [p["frames_por_anio"] for p in periodos]
    vmax = max(vals) * 1.15
    bw = (W - ml - mr) / len(periodos) * 0.55
    c = [texto(W / 2, 26, "Ritmo de mejora: frames ganados por año", 15, "#111", "middle", "600")]
    for i in range(6):
        v = vmax * i / 5
        yy = H - mb - (v / vmax) * (H - mt - mb)
        c.append(linea(ml, yy, W - mr, yy, "#eee"))
        c.append(texto(ml - 8, yy + 4, f"{v:.0f}", 10, "#666", "end"))
    for i, p in enumerate(periodos):
        cx = ml + (i + 0.5) * (W - ml - mr) / len(periodos)
        yy = H - mb - (p["frames_por_anio"] / vmax) * (H - mt - mb)
        c.append(f'<rect x="{cx-bw/2:.1f}" y="{yy:.1f}" width="{bw:.1f}" '
                 f'height="{H-mb-yy:.1f}" fill="#1a73e8" opacity="0.85" rx="3"/>')
        c.append(texto(cx, yy - 8, f"{p['frames_por_anio']:.1f}", 12, "#111", "middle", "700"))
        c.append(texto(cx, H - mb + 20, p["periodo"], 11, "#333", "middle", "600"))
        c.append(texto(cx, H - mb + 36, f"{p['n_records']} récords", 10, "#777", "middle"))
    c.append(texto(W / 2, H - 12, "La ganancia por año cae de 143 a 11,8 frames", 10.5, "#c0392b", "middle", "600"))
    open(os.path.join(FIG, "fig2_ritmo.svg"), "w", encoding="utf-8").write(svg(W, H, "".join(c)))


# ---------------------------------------------------------------- Figura 3
def fig_histograma():
    """Distribución de tiempos verificados (núcleo 4:54-5:30)."""
    with open(os.path.join(PROC, "runs_any_pcts_ntsc.csv"), encoding="utf-8") as f:
        ts = []
        for r in csv.DictReader(f):
            try:
                t = float(r["tiempo_s"])
            except (TypeError, ValueError):
                continue
            if 294 <= t <= 330:
                ts.append(t)
    bins = {}
    for t in ts:
        b = round(t, 1)
        bins[b] = bins.get(b, 0) + 1
    xs = sorted(bins)
    W, H = 880, 400
    ml, mr, mt, mb = 70, 25, 50, 60
    vmax = max(bins.values()) * 1.1
    n = len(xs)
    bw = (W - ml - mr) / n
    c = [texto(W / 2, 26, "Distribución de tiempos verificados (núcleo 4:54–5:30, N≈7k)", 15, "#111", "middle", "600")]
    for i in range(1, 6):
        v = vmax * i / 5
        yy = H - mb - (v / vmax) * (H - mt - mb)
        c.append(linea(ml, yy, W - mr, yy, "#eee"))
        c.append(texto(ml - 8, yy + 4, f"{v:.0f}", 10, "#666", "end"))
    for i, x in enumerate(xs):
        xx = ml + i * bw
        yy = H - mb - (bins[x] / vmax) * (H - mt - mb)
        m, s = divmod(x, 60)
        # Marcar la zona de élite
        col = "#c0392b" if x <= 296 else "#1a73e8"
        c.append(f'<rect x="{xx+0.4:.1f}" y="{yy:.1f}" width="{max(bw-0.8,0.7):.1f}" '
                 f'height="{H-mb-yy:.1f}" fill="{col}" opacity="0.8"/>')
    for x in [294.0, 296, 300, 305, 310, 315, 320, 325, 330]:
        if xs[0] <= x <= xs[-1]:
            xx = ml + (x - xs[0]) / (xs[-1] - xs[0]) * (W - ml - mr)
            m, s = divmod(int(x), 60)
            c.append(texto(xx, H - mb + 18, f"{m}:{s:02d}", 10, "#666", "middle"))
    c.append(texto(W / 2, H - 12,
                   "Rojo: runs a ≤4 frames del óptimo. La élite se separa del núcleo por ~1,5 s", 10.5, "#c0392b", "middle", "600"))
    open(os.path.join(FIG, "fig3_histograma.svg"), "w", encoding="utf-8").write(svg(W, H, "".join(c)))


def fig_sensibilidad():
    """Rejilla de intentos necesarios según p84 y p_escalon."""
    with open(os.path.join(PROC, "sensibilidad.json"), encoding="utf-8") as f:
        d = json.load(f)
    rej = d["rejilla"]
    p84s = sorted({r["p84"] for r in rej})
    pescs = sorted({r["p_escalon"] for r in rej})

    W, H = 880, 430
    ml, mr, mt, mb = 110, 40, 90, 70
    cw = (W - ml - mr) / len(pescs)
    ch = (H - mt - mb) / len(p84s)

    def color(n):
        # verde (pocos intentos) -> rojo (muchos)
        if n <= 20:
            return "#2e9e5b"
        if n <= 50:
            return "#8bc34a"
        if n <= 120:
            return "#f2c037"
        if n <= 300:
            return "#e67e22"
        return "#c0392b"

    c = [texto(W / 2, 28, "Intentos necesarios para 50 % de probabilidad", 15, "#111", "middle", "600"),
         texto(W / 2, 46, "Cada celda: nº de intentos según la calibración", 11, "#666", "middle")]

    for j, pe in enumerate(pescs):
        for i, p8 in enumerate(p84s):
            fila = [r for r in rej if abs(r["p84"] - p8) < 1e-9 and abs(r["p_escalon"] - pe) < 1e-9]
            if not fila:
                continue
            n = fila[0]["intentos_50pct"]
            x = ml + j * cw
            y = mt + i * ch
            txt = "∞" if n == float("inf") else str(int(n))
            c.append(f'<rect x="{x+2:.1f}" y="{y+2:.1f}" width="{cw-4:.1f}" height="{ch-4:.1f}" '
                     f'fill="{color(n)}" opacity="0.88" rx="3"/>')
            c.append(texto(x + cw / 2, y + ch / 2 + 5, txt, 13, "white", "middle", "700"))

    for j, pe in enumerate(pescs):
        c.append(texto(ml + (j + 0.5) * cw, H - mb + 20, f"{pe*100:.1f}%", 10.5, "#444", "middle", "600"))
    for i, p8 in enumerate(p84s):
        c.append(texto(ml - 10, mt + (i + 0.5) * ch + 4, f"{p8*100:.2f}%", 10.5, "#444", "end", "600"))

    c.append(texto(ml - 10, mt - 14, "P(8-4 perfecto)", 11, "#111", "start", "700"))
    c.append(texto(W - mr, H - mb + 42, "Tasa de cruce de escalón por sección", 11, "#111", "end", "700"))
    c.append(texto(W / 2, H - 14,
                   "Incluso en la celda más adversa (430) el óptimo es alcanzable en semanas, no décadas",
                   10.5, "#c0392b", "middle", "600"))
    open(os.path.join(FIG, "fig4_sensibilidad.svg"), "w", encoding="utf-8").write(svg(W, H, "".join(c)))


def fig_montecarlo():
    """Distribución del error de los runs simulados."""
    with open(os.path.join(PROC, "simulacion_mc.json"), encoding="utf-8") as f:
        d = json.load(f)
    esc = [e for e in d["escenarios"] if e["escenario"].startswith("calibrado")][0]
    hist = {int(k): v for k, v in esc["histograma_delta"].items()}
    xs = sorted(hist)
    W, H = 880, 420
    ml, mr, mt, mb = 70, 30, 60, 60
    vmax = max(hist.values()) * 1.1
    n = len(xs)
    bw = (W - ml - mr) / n
    c = [texto(W / 2, 28, "Distribución del error en 200.000 runs simulados", 15, "#111", "middle", "600"),
         texto(W / 2, 46, "0 frames perdidos = se empata el óptimo (4:54.265)", 11, "#666", "middle")]
    for i in range(1, 6):
        v = vmax * i / 5
        yy = H - mb - (v / vmax) * (H - mt - mb)
        c.append(linea(ml, yy, W - mr, yy, "#eee"))
        c.append(texto(ml - 8, yy + 4, f"{v/1000:.0f}k", 10, "#666", "end"))
    for i, x in enumerate(xs):
        xx = ml + i * bw
        yy = H - mb - (hist[x] / vmax) * (H - mt - mb)
        col = "#c0392b" if x == 0 else "#1a73e8"
        c.append(f'<rect x="{xx+0.5:.1f}" y="{yy:.1f}" width="{max(bw-1,0.8):.1f}" '
                 f'height="{H-mb-yy:.1f}" fill="{col}" opacity="0.85"/>')
    for i in range(0, n, 2):
        c.append(texto(ml + (i + 0.5) * bw, H - mb + 18, str(xs[i]), 9.5, "#666", "middle"))
    c.append(texto(ml + 0.5 * bw, H - mb - (hist[0] / vmax) * (H - mt - mb) - 10,
                   f"{100*esc['p_perfecto']:.2f}%", 12, "#c0392b", "start", "700"))
    c.append(texto(W / 2, H - 12,
                   "Rojo: runs perfectos. La masa se acumula en 1-3 frames: el humano casi siempre falla por poquísimo",
                   10.5, "#1a73e8", "middle", "600"))
    open(os.path.join(FIG, "fig5_montecarlo.svg"), "w", encoding="utf-8").write(svg(W, H, "".join(c)))


if __name__ == "__main__":
    fig_convergencia()
    fig_ritmo()
    fig_histograma()
    fig_sensibilidad()
    fig_montecarlo()
    print("Figuras generadas en", FIG)
    for f in sorted(os.listdir(FIG)):
        if f.endswith(".svg"):
            print("  ", f, os.path.getsize(os.path.join(FIG, f)), "bytes")
