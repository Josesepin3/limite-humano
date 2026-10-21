#!/usr/bin/env python3
"""
Respuesta final a la pregunta central: ¿puede un humano, con sus limitaciones
biológicas, alcanzar el tiempo perfecto de la máquina?

Este script sintetiza los dos modelos previos en una única respuesta con
intervalo, y produce la tabla y la figura finales del documento.

La respuesta se da sobre el EVENTO "al menos un humano lo logra en un
horizonte dado", que es la pregunta del título. Se explora:

  - T : grind por corredor (100 a 30 000 intentos de 8-4)      [no medido]
  - actividad : cuántos corredores grindean y cuántos intentos por sesión
                [supuesto declarado]

y se reporta la probabilidad de que el evento ocurra, así como el tiempo
esperado hasta que ocurra.

Salida:
  datos/procesados/respuesta_final.json
  documento/figuras/fig6_probabilidad.svg
"""

import json
import math
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(BASE, "datos", "procesados")
FIG = os.path.join(BASE, "documento", "figuras")

# Insumos (leídos del modelo integrado si existe)
p_pb = 4 / 203
p_regla = 0.9655   # (1 - 0.005)^7


def p84_desde_T(T):
    return 1 - (1 - p_pb) ** (1 / T)


def p_run(T):
    return p84_desde_T(T) * p_regla


def p_alguno(p_uno, n_intentos):
    if p_uno <= 0:
        return 0.0
    return 1 - (1 - p_uno) ** n_intentos


def intentos_hasta(p_uno, objetivo):
    if p_uno <= 0:
        return float("inf")
    if p_uno >= 1:
        return 1
    return math.ceil(math.log(1 - objetivo) / math.log(1 - p_uno))


def svg(ancho, alto, contenido):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho} {alto}" '
            f'width="{ancho}" height="{alto}" font-family="system-ui,sans-serif">'
            f'<rect width="{ancho}" height="{alto}" fill="white"/>{contenido}</svg>')


def texto(x, y, s, size=11, color="#333", anchor="start", weight="normal"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}" font-weight="{weight}">{s}</text>')


def linea(x1, y1, x2, y2, color="#333", w=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="{w}"{d}/>')


def figura_probabilidad(escenarios):
    """Curva de P(alguien lo logra) frente a los años, por nº de corredores."""
    W, H = 880, 460
    ml, mr, mt, mb = 80, 30, 60, 60
    x0, x1 = 0, 25
    y0, y1 = 0, 1

    def X(x):
        return ml + (x - x0) / (x1 - x0) * (W - ml - mr)

    def Y(y):
        return H - mb - (y - y0) / (y1 - y0) * (H - mt - mb)

    c = [texto(W / 2, 28, "P(que ALGÚN humano alcance el óptimo) vs. tiempo",
               15, "#111", "middle", "600"),
         texto(W / 2, 46, "Escenario de referencia T=3000; la banda gris cubre T=100 a T=30000",
               11, "#666", "middle")]
    for i in range(6):
        v = i / 5
        c.append(linea(ml, Y(v), W - mr, Y(v), "#eee"))
        c.append(texto(ml - 8, Y(v) + 4, f"{100*v:.0f}%", 10, "#666", "end"))
    for x in range(0, 26, 5):
        c.append(linea(X(x), mt, X(x), H - mb, "#f4f4f4"))
        c.append(texto(X(x), H - mb + 18, str(x), 10, "#666", "middle"))

    colores = {1: "#c0392b", 3: "#1a73e8", 10: "#2e9e5b"}
    for corr in (1, 3, 10):
        pts = []
        for anios in range(0, 26):
            intentos = corr * 400 * 5 * 52 * anios
            p = p_alguno(p_run(3000), intentos)
            pts.append((X(anios), Y(p)))
        c.append('<polyline points="' + " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
                 + f'" fill="none" stroke="{colores[corr]}" stroke-width="2.4"/>')

    # Etiquetas
    c.append(texto(X(24.6), Y(p_alguno(p_run(3000), 10*400*5*52)) - 10,
                   "10 corredores", 11, colores[10], "end", "600"))
    c.append(texto(X(24.6), Y(p_alguno(p_run(3000), 3*400*5*52)) - 10,
                   "3 corredores", 11, colores[3], "end", "600"))
    c.append(texto(X(9), Y(p_alguno(p_run(3000), 1*400*5*52*9)) - 10,
                   "1 corredor", 11, colores[1], "start", "600"))

    c.append(texto(W / 2, H - 12, "Años de actividad continuada de la comunidad",
                   11, "#555", "middle"))
    c.append(texto(20, H / 2, "Probabilidad", 11, "#555", "middle"))
    open(os.path.join(FIG, "fig6_probabilidad.svg"), "w", encoding="utf-8").write(
        svg(W, H, "".join(c)))


def main():
    escenarios = []
    print("=== P(ALGÚN HUMANO LO LOGRA) ===")
    print("Cada celda: probabilidad de que al menos un corredor lo logre,")
    print("según el grind por corredor (T) y los años de actividad.\n")
    Ts = [100, 1000, 3000, 10000, 30000]
    anios_l = [1, 5, 10, 25]
    # 3 corredores activos, 400 intentos/sesión, 5 sesiones/semana
    corredores, ipor, ses = 3, 400, 5
    print(f"{'T':>8} | " + " | ".join(f"{a:>4} años" for a in anios_l))
    for T in Ts:
        p1 = p_run(T)
        fila = []
        for a in anios_l:
            intentos = corredores * ipor * ses * 52 * a
            p = p_alguno(p1, intentos)
            fila.append(p)
            escenarios.append({"T": T, "anios": a, "corredores": corredores,
                               "p_alguno": p})
        print(f"{T:>8} | " + " | ".join(f"{100*p:>8.2f}%" for p in fila))

    print()
    print("=== TIEMPO ESPERADO HASTA EL EVENTO (mediana, 3 corredores) ===")
    horas_unicas = None
    for T in [100, 1000, 3000, 10000, 30000]:
        p1 = p_run(T)
        it = intentos_hasta(p1, 0.5)
        if it == float("inf"):
            print(f"  T={T:>6}: nunca")
            continue
        # intentos -> horas, con 3 corredores en paralelo
        horas = it / (corredores * ipor / 1.5)  # ~1.5 h por sesión de 400 intentos... simplificado
        anios = horas / (ses * 52 * 1.5)
        print(f"  T={T:>6}: {it:>12,} intentos -> {anios:>7.2f} años (3 corredores)")

    figura_probabilidad(escenarios)

    salida = {
        "escenarios": escenarios,
        "p_pb": p_pb, "p_regla": p_regla,
        "supuestos": {"corredores_activos": corredores,
                      "intentos_por_sesion": ipor,
                      "sesiones_por_semana": ses},
    }
    json.dump(salida, open(os.path.join(PROC, "respuesta_final.json"), "w",
                           encoding="utf-8"), ensure_ascii=False, indent=2)
    print()
    print(f"-> {os.path.join(PROC, 'respuesta_final.json')}")
    print(f"-> {os.path.join(FIG, 'fig6_probabilidad.svg')}")


if __name__ == "__main__":
    main()
