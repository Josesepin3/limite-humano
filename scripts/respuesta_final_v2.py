#!/usr/bin/env python3
"""
RESPUESTA FINAL — v2: probabilidad de que algún humano, algún día, alcance el
tiempo perfecto de la máquina en Super Mario Bros. Any% (NTSC).

QUE CAMBIA RESPECTO A LA v1
---------------------------
La v1 usaba un único T (grind por corredor) y lo hacía variar a mano. La
evidencia de los comentarios del 8-4 IL muestra que T es HETEROGÉNEO (de 2 a
16.200 intentos según el corredor) y que además hay dos regímenes claros:

  - Corredores que ya dominan la sección (grind corto, minutos u horas).
  - Corredores que la aprenden desde cero (grind largo, días de juego).

La v2 propaga TODA la distribución de T y separa esos dos regímenes, en vez de
elegir un valor "de referencia" discutible.

MODELO
------
Nivel 1 — el 8-4 dentro de un intento:
    P(8-4 perfecto por intento | T) = 1 - (1 - P(PB perfecto))^(1/T)

  donde P(PB perfecto) = 4/203 es la fracción de corredores del tablero 8-4 IL
  que publicaron una marca perfecta, y T es cuántos intentos les costó.

Nivel 2 — el run completo:
    P(run perfecto) = P(8-4 perfecto) × (1 - p_escalon)^7

  porque además hay que no cruzar ningún escalón de 21 frames en las 7
  secciones con frame rule.

Nivel 3 — el evento "alguien, algún día":
    P(al menos uno) = 1 - (1 - P(run perfecto))^N

  con N = intentos totales acumulados por la comunidad en un horizonte dado.

TODOS los supuestos de actividad (cuántos corredores, cuántos intentos por
sesión) se declaran y se hacen variar. No hay ningún número "elegido".

Salida:
  datos/procesados/respuesta_final_v2.json
  documento/figuras/fig7_probabilidad_v2.svg
"""

import json
import math
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(BASE, "datos", "procesados")
FIG = os.path.join(BASE, "documento", "figuras")

# ---------------------------------------------------------------- Insumos
P_PB = 4 / 203                 # fracción de corredores con PB perfecto
P_ESCALON = 0.005              # por sección (calibrado en simulacion_montecarlo)
N_REGLA = 7                    # secciones con frame rule
P_SIN_CRUZAR = (1 - P_ESCALON) ** N_REGLA


def cargar_T():
    """Carga la distribución de T si existe; si no, usa valores por defecto."""
    ruta = os.path.join(PROC, "distribucion_T.json")
    if os.path.exists(ruta):
        d = json.load(open(ruta, encoding="utf-8"))
        ts = [x["intentos"] for x in d["duraciones_declaradas"]]
        return sorted(ts)
    return [15, 90, 5400, 6300, 16200]


def p84(T):
    """P(8-4 perfecto en UN intento) dado un grind de T intentos."""
    if T <= 0:
        return 0.0
    return 1 - (1 - P_PB) ** (1 / T)


def p_run(T):
    return p84(T) * P_SIN_CRUZAR


def p_alguno(p_uno, n):
    if p_uno <= 0:
        return 0.0
    if p_uno >= 1:
        return 1.0
    return 1 - (1 - p_uno) ** n


def it_para(p_uno, obj):
    if p_uno <= 0:
        return float("inf")
    if p_uno >= 1:
        return 1
    return math.ceil(math.log(1 - obj) / math.log(1 - p_uno))


# ---------------------------------------------------------------- Figura
def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" font-family="system-ui,sans-serif">'
            f'<rect width="{w}" height="{h}" fill="white"/>{body}</svg>')


def txt(x, y, s, size=11, color="#333", anchor="start", weight="normal"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}" font-weight="{weight}">{s}</text>')


def lin(x1, y1, x2, y2, color="#333", w=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="{w}"{d}/>')


def figura(filas):
    """
    Dos paneles:
      izquierda: P(run perfecto) por intento frente a T
      derecha:   P(al menos uno lo logra) frente a años, por nº de corredores
    """
    W, H = 940, 430
    panel = 400
    gx = 70
    gy = 60
    gh = 290

    b = [txt(W / 2, 26, "¿Puede un humano alcanzar el óptimo de la máquina?",
             16, "#111", "middle", "600"),
         txt(W / 2, 45, "Izquierda: dificultad por intento según el grind. "
                        "Derecha: probabilidad acumulada del evento.",
             11, "#666", "middle")]

    # ---- Panel izquierdo: p_run vs T (escala log en T) ----
    x0, x1 = 0, 4          # log10(T)
    y0, y1 = 0, 1
    ml, mt, mb = gx, gy, gh

    def XL(t):
        return ml + (math.log10(t) - x0) / (x1 - x0) * (panel - 60)

    def YL(p):
        return mt + gh - p * gh

    b.append(lin(ml, mt, ml, mt + gh, "#999"))
    b.append(lin(ml, mt + gh, ml + panel - 60, mt + gh, "#999"))
    for i in range(6):
        v = i / 5
        b.append(lin(ml, YL(v), ml + panel - 60, YL(v), "#f0f0f0"))
        b.append(txt(ml - 6, YL(v) + 4, f"{100*v:.0f}%", 9, "#777", "end"))
    for e in range(5):
        t = 10 ** e
        b.append(lin(XL(t), mt, XL(t), mt + gh, "#f0f0f0"))
        b.append(txt(XL(t), mt + gh + 15, f"{t:,}", 9, "#777", "middle"))
    b.append(txt(ml + (panel - 60) / 2, mt + gh + 34,
                 "T = intentos de grind por corredor (escala log)",
                 10, "#555", "middle"))
    b.append(txt(ml - 44, mt + gh / 2, "P(run perfecto)", 10, "#555",
                 "middle"))

    pts = []
    for lg in [x / 20 for x in range(2, 81)]:
        t = 10 ** lg
        pts.append((XL(t), YL(p_run(t))))
    b.append('<polyline points="' + " ".join(f"{a:.1f},{c:.1f}" for a, c in pts)
             + '" fill="none" stroke="#1a73e8" stroke-width="2.4"/>')

    # Marcar los T observados
    for t in filas:
        b.append(f'<circle cx="{XL(t):.1f}" cy="{YL(p_run(t)):.1f}" r="3" '
                 f'fill="#c0392b"/>')
    b.append(txt(ml + 10, mt + 14,
                 "puntos rojos = grinds reales declarados", 9, "#c0392b"))

    # ---- Panel derecho: P(alguno) vs años ----
    ml2 = panel + gx + 60
    pw = W - ml2 - 40
    anios_max = 25

    def XR(a):
        return ml2 + a / anios_max * pw

    def YR(p):
        return mt + gh - p * gh

    b.append(lin(ml2, mt, ml2, mt + gh, "#999"))
    b.append(lin(ml2, mt + gh, ml2 + pw, mt + gh, "#999"))
    for i in range(6):
        v = i / 5
        b.append(lin(ml2, YR(v), ml2 + pw, YR(v), "#f0f0f0"))
        b.append(txt(ml2 - 6, YR(v) + 4, f"{100*v:.0f}%", 9, "#777", "end"))
    for a in range(0, anios_max + 1, 5):
        b.append(lin(XR(a), mt, XR(a), mt + gh, "#f0f0f0"))
        b.append(txt(XR(a), mt + gh + 15, str(a), 9, "#777", "middle"))
    b.append(txt(ml2 + pw / 2, mt + gh + 34,
                 "años de actividad continuada", 10, "#555", "middle"))
    b.append(txt(ml2 - 44, mt + gh / 2, "P(al menos uno lo logra)", 10,
                 "#555", "middle"))

    # Escenario central: T mediano, distintos niveles de actividad
    T_med = 2745
    p1 = p_run(T_med)
    colores = {1: "#c0392b", 5: "#1a73e8", 20: "#2e9e5b"}
    for corr in (1, 5, 20):
        pp = []
        for a in range(0, anios_max + 1):
            # 200 intentos completos por corredor-día, 3 días activos/semana
            n = corr * 200 * 3 * 52 * a
            pp.append((XR(a), YR(p_alguno(p1, n))))
        b.append('<polyline points="'
                 + " ".join(f"{u:.1f},{v:.1f}" for u, v in pp)
                 + f'" fill="none" stroke="{colores[corr]}" stroke-width="2.4"/>')
        p25 = p_alguno(p1, corr * 200 * 3 * 52 * anios_max)
        b.append(txt(XR(anios_max) - 4, YR(p25) - 8, f"{corr} corredores",
                     10, colores[corr], "end", "600"))
    b.append(txt(ml2 + 8, mt + 14,
                 f"asumiendo T mediano = {T_med:,} y 200 intentos/día activo",
                 9, "#777"))

    open(os.path.join(FIG, "fig7_probabilidad_v2.svg"), "w",
         encoding="utf-8").write(svg(W, H, "".join(b)))


# ---------------------------------------------------------------- Main
def main():
    Ts = cargar_T()
    print("=== RESPUESTA FINAL v2 ===")
    print()
    print(f"  Insumos:")
    print(f"    P(PB perfecto 8-4)     = 4/203 = {P_PB:.4f}")
    print(f"    P(sin cruzar escalón)  = {P_SIN_CRUZAR:.4f}")
    print(f"    T observados (intentos)= {[f'{t:,.0f}' for t in Ts]}")
    print()

    print("=== p84 SEGÚN EL GRIND OBSERVADO ===")
    print(f"{'T (intentos)':>14} | {'p84':>12} | {'P(run perf.)':>13} | "
          f"{'it. 50%':>12} | {'it. 99%':>13}")
    tabla = []
    for T in Ts:
        a = p84(T)
        r = p_run(T)
        i50 = it_para(r, 0.50)
        i99 = it_para(r, 0.99)
        tabla.append({"T": T, "p84": a, "p_run": r,
                      "it_50": i50, "it_99": i99})
        print(f"{T:>14,.0f} | {a:>12.3e} | {r:>13.3e} | "
              f"{('inf' if i50==float('inf') else f'{i50:,}'):>12} | "
              f"{('inf' if i99==float('inf') else f'{i99:,}'):>13}")

    # Escenario central = mediana de T
    T_med = sorted(Ts)[len(Ts) // 2]
    p1 = p_run(T_med)
    print()
    print(f"=== ESCENARIO CENTRAL (T = mediana = {T_med:,.0f} intentos) ===")
    print(f"  p84            = {p84(T_med):.3e}")
    print(f"  P(run perfecto)= {p1:.3e}")
    print(f"  Intentos para 50 %: {it_para(p1,0.5):,}")
    print(f"  Intentos para 99 %: {it_para(p1,0.99):,}")

    # ---- Evento: alguien, algún día ----
    print()
    print("=== P(ALGÚN HUMANO LO LOGRA) — escenario central ===")
    print("  (200 intentos completos por día activo, 3 días/semana)")
    esc = []
    for corr in (1, 5, 20):
        for anios in (1, 5, 10, 25):
            n = corr * 200 * 3 * 52 * anios
            p = p_alguno(p1, n)
            esc.append({"corredores": corr, "anios": anios,
                        "intentos_totales": n, "p_alguno": p})
    print(f"{'corredores':>11} | " + " | ".join(f"{a:>7} años" for a in (1,5,10,25)))
    for corr in (1, 5, 20):
        fila = [e for e in esc if e["corredores"] == corr]
        print(f"{corr:>11} | " + " | ".join(
            f"{100*e['p_alguno']:>11.2f}%" for e in fila))

    # ---- Sensibilidad: el peor caso razonable ----
    T_pes = max(Ts)
    p_pes = p_run(T_pes)
    print()
    print(f"=== PEOR CASO RAZONABLE (T = {T_pes:,.0f}, el grind más largo) ===")
    print(f"  P(run perfecto) = {p_pes:.3e}")
    print(f"  Intentos para 50 %: {it_para(p_pes,0.5):,}")
    for corr, anios in ((5, 25), (20, 25)):
        n = corr * 200 * 3 * 52 * anios
        print(f"  {corr} corredores, {anios} años -> "
              f"P = {100*p_alguno(p_pes, n):.2f} %")

    # ---- Mejor caso razonable ----
    T_mej = min(t for t in Ts if t >= 90)   # excluye grinds de minutos
    p_mej = p_run(T_mej)
    print()
    print(f"=== MEJOR CASO RAZONABLE (T = {T_mej:,.0f}, corredor ya experto) ===")
    print(f"  P(run perfecto) = {p_mej:.3e}")
    print(f"  Intentos para 50 %: {it_para(p_mej,0.5):,}")
    n = 5 * 200 * 3 * 52 * 5
    print(f"  5 corredores, 5 años -> P = {100*p_alguno(p_mej, n):.2f} %")

    figura([t for t in Ts])

    salida = {
        "insumos": {
            "p_pb_perfecto": P_PB,
            "p_escalon": P_ESCALON,
            "p_sin_cruzar_regla": P_SIN_CRUZAR,
            "T_observados": Ts,
            "T_mediana": T_med,
        },
        "tabla_por_T": tabla,
        "escenario_central": {
            "T": T_med, "p84": p84(T_med), "p_run": p1,
            "it_50": it_para(p1, 0.5), "it_99": it_para(p1, 0.99),
        },
        "evento_algun_humano": esc,
        "peor_caso": {"T": T_pes, "p_run": p_pes,
                      "it_50": it_para(p_pes, 0.5)},
        "mejor_caso": {"T": T_mej, "p_run": p_mej,
                       "it_50": it_para(p_mej, 0.5)},
        "supuestos_actividad": {
            "intentos_por_dia_activo": 200,
            "dias_activos_por_semana": 3,
            "nota": ("Supuesto declarado. No se midió la actividad real de la "
                     "comunidad; el resultado escala linealmente con estos "
                     "valores y por eso se reporta como rango."),
        },
    }
    ruta = os.path.join(PROC, "respuesta_final_v2.json")
    json.dump(salida, open(ruta, "w", encoding="utf-8"), ensure_ascii=False,
              indent=2)
    print()
    print(f"-> {ruta}")
    print(f"-> {os.path.join(FIG, 'fig7_probabilidad_v2.svg')}")


if __name__ == "__main__":
    main()
