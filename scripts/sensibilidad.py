#!/usr/bin/env python3
"""
Análisis de sensibilidad del modelo Monte Carlo.

PREGUNTA QUE RESPONDE
---------------------
El resultado central depende de dos parámetros calibrados con más o menos
certeza:
  - p84 : probabilidad de 8-4 perfecto. MEDIDA directamente (4/203 = 1.97 %).
  - p_escalon : probabilidad de cruzar un escalón en cada una de las 7
    secciones con frame rule. ESTIMADA (2 %), no medida.

La medida de p84 es sólida porque el 8-4 IL es una medición directa. Pero
p_escalon es una inferencia. Este análisis recorre un rango amplio de
p_escalon y de p84 para ver si la conclusión cualitativa ("alcanzable en un
número finito y moderado de intentos") se sostiene o se rompe.

También se hace la pregunta inversa: ¿qué p84 tendría que alcanzar la
comunidad para que el óptimo sea alcanzable al 50 % en N intentos?

Salida: datos/procesados/sensibilidad.json
"""

import csv
import json
import math
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(BASE, "datos", "procesados")
FRAME_RULE = 21


def intentos_50(p):
    if p <= 0:
        return float("inf")
    if p >= 1:
        return 1
    return math.ceil(math.log(0.5) / math.log(1 - p))


def p_run(p84, p_esc, n_regla=7):
    return p84 * (1 - p_esc) ** n_regla


def medir_p84():
    ruta = os.path.join(PROC, "il_84.csv")
    if not os.path.exists(ruta):
        return 4 / 203
    with open(ruta, encoding="utf-8") as f:
        deltas = [int(r["delta_frames"]) for r in csv.DictReader(f)
                  if r["delta_frames"] not in (None, "")]
    return sum(1 for d in deltas if d == 0) / len(deltas)


def intervalo_confianza_wilson(k, n, z=1.96):
    """IC 95 % para una proporción (Wilson), robusto con n pequeño."""
    if n == 0:
        return (0, 0)
    p = k / n
    den = 1 + z * z / n
    centro = (p + z * z / (2 * n)) / den
    margen = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / den
    return (max(0, centro - margen), min(1, centro + margen))


def main():
    p84_obs = medir_p84()
    n84 = 203
    k84 = round(p84_obs * n84)
    ic = intervalo_confianza_wilson(k84, n84)

    print("=== INCERTIDUMBRE EN LA MEDICIÓN DE p84 ===")
    print(f"  Observado: {k84}/{n84} = {p84_obs:.4f}")
    print(f"  IC 95 % (Wilson): [{ic[0]:.4f}, {ic[1]:.4f}]")
    print()

    # --- Rejilla de sensibilidad -------------------------------------------
    p_escs = [0.0, 0.002, 0.005, 0.01, 0.02, 0.05, 0.10, 0.20]
    p84s = [ic[0], p84_obs, ic[1], 0.05, 0.10, 0.20]

    rejilla = []
    for pe in p_escs:
        for p8 in p84s:
            p = p_run(p8, pe)
            rejilla.append({
                "p_escalon": pe, "p84": round(p8, 5),
                "p_run_perfecto": p, "intentos_50pct": intentos_50(p),
            })

    print("=== REJILLA: intentos para 50 % de probabilidad ===")
    print(f"{'p84 \\ p_esc':>12} | " + " | ".join(f"{pe:>10.3f}" for pe in p_escs))
    for p8 in p84s:
        fila = [r for r in rejilla if abs(r["p84"] - round(p8, 5)) < 1e-9]
        fila.sort(key=lambda r: r["p_escalon"])
        print(f"{p8:>12.4f} | " + " | ".join(
            f"{('inf' if r['intentos_50pct']==float('inf') else r['intentos_50pct']):>10}"
            for r in fila))

    # --- Pregunta inversa: p84 necesaria para lograrlo en N intentos --------
    print()
    print("=== PREGUNTA INVERSA: ¿qué p84 hace falta para N intentos (50 %)? ===")
    inversa = []
    for N in (10, 25, 50, 100, 500, 1000, 5000, 10000):
        # p_run = 1 - 0.5^(1/N); y p_run = p84*(1-pe)^7
        p_run_nec = 1 - 0.5 ** (1 / N)
        for pe in (0.0, 0.005, 0.02):
            p84_nec = p_run_nec / (1 - pe) ** 7
            inversa.append({
                "N_objetivo": N, "p_escalon": pe,
                "p_run_necesario": p_run_nec,
                "p84_necesario": min(1.0, p84_nec),
                "mejora_vs_actual": (min(1.0, p84_nec) / p84_obs) if p84_obs else None,
            })

    for row in inversa:
        if row["p_escalon"] == 0.02:
            print(f"  N={row['N_objetivo']:>6} intentos -> p84 necesario "
                  f"= {row['p84_necesario']:.4f} "
                  f"({row['mejora_vs_actual']:.1f}x el actual)")

    salida = {
        "p84_observado": p84_obs,
        "p84_ic95": ic,
        "n_intentos_il": n84,
        "perfectos_il": k84,
        "rejilla": rejilla,
        "pregunta_inversa": inversa,
        "nota": ("p84 está medido (4/203); p_escalon está estimado. La rejilla "
                 "muestra cómo cambia el resultado al variar ambos."),
    }
    ruta = os.path.join(PROC, "sensibilidad.json")
    json.dump(salida, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print()
    print("=== CONCLUSIÓN DE ROBUSTEZ ===")
    p_mejor = p_run(ic[1], 0.0)
    p_peor = p_run(ic[0], 0.20)
    print(f"  Escenario MÁS favorable: P(perfecto)={p_mejor:.4f} "
          f"-> {intentos_50(p_mejor)} intentos")
    print(f"  Escenario MÁS adverso  : P(perfecto)={p_peor:.6f} "
          f"-> {intentos_50(p_peor)} intentos")
    print(f"\n-> {ruta}")


if __name__ == "__main__":
    main()
