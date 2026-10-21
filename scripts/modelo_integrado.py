#!/usr/bin/env python3
"""
Modelo INTEGRADO del límite humano: probabilidad de que ALGÚN humano, en
algún momento, alcance el tiempo perfecto de la máquina.

Este script corrige y fusiona los dos modelos anteriores:

  - El primero (simulacion_montecarlo.py) estimaba bien la mecánica de las
    secciones, pero trataba los 203 runs del 8-4 IL como 203 "intentos".
  - El segundo (limite_biologico.py) corrigió el denominador, pero aisló el
    8-4 del resto del run.

Aquí se unen las dos piezas correctas:

  P(run perfecto) = P(las 7 secciones con frame rule sin cruzar escalón)
                    × P(8-4 perfecto en ese mismo run)

LA ESTRUCTURA EN DOS NIVELES
----------------------------
Para que un run completo empate el óptimo hacen falta DOS cosas a la vez:

  A) No cruzar ningún escalón de 21 frames en las 7 secciones con frame rule.
     Esto NO es difícil: los 10 mejores runs de la historia lo consiguen, y la
     evidencia fija p_escalon ~ 0,5 % por sección.

  B) Ejecutar el 8-4 perfecto. Esto SÍ es difícil, y es lo que la biología
     limita. La tasa por intento del 8-4 (p84) es el parámetro crucial.

CÓMO SE ESTIMA p84 SIN ENGAÑARSE
--------------------------------
El 8-4 IL es un tablero de MEJORES MARCAS PERSONALES: 203 corredores, un run
cada uno. La marca de cada corredor costó un grind de T intentos. Aplicando
la teoría de renovación:

    P(PB perfecto) = 1 - (1 - p84)^T

Con 4/203 jugadores con PB perfecto, se despeja p84 para cada T:

    p84 = 1 - (1 - 4/203)^(1/T)

Como T no está medido con precisión (los comentarios lo mencionan de forma
anecdótica), el resultado se presenta COMO UNA FUNCIÓN DE T, y se acota el
rango con evidencia observable de sesiones.
"""

import csv
import json
import math
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(BASE, "datos", "procesados")
FPS = 60.0988138974405
FRAME_RULE = 21


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    den = 1 + z * z / n
    centro = (p + z * z / (2 * n)) / den
    margen = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / den
    return (max(0.0, centro - margen), min(1.0, centro + margen))


def p_desde_pb(p_pb, T):
    if p_pb <= 0:
        return 0.0
    if p_pb >= 1:
        return 1.0
    return 1 - (1 - p_pb) ** (1 / T)


def it50(p):
    if p <= 0:
        return float("inf")
    if p >= 1:
        return 1
    return math.ceil(math.log(0.5) / math.log(1 - p))


def it_objetivo(p, obj):
    if p <= 0:
        return float("inf")
    if p >= 1:
        return 1
    return math.ceil(math.log(1 - obj) / math.log(1 - p))


def leer_il():
    with open(os.path.join(PROC, "il_84.csv"), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def cargar_p_escalon():
    """Toma p_escalon calibrado del modelo Monte Carlo si existe."""
    ruta = os.path.join(PROC, "simulacion_mc.json")
    if os.path.exists(ruta):
        d = json.load(open(ruta, encoding="utf-8"))
        return d["calibracion_regla"]["p_perder_escalon_por_seccion"]
    return 0.005


def p_sin_cruzar(p_esc, n_regla=7):
    return (1 - p_esc) ** n_regla


def main():
    il = leer_il()
    n_jug = len(il)
    perfectos = sum(1 for r in il if int(r["delta_frames"]) == 0)
    p_pb = perfectos / n_jug
    ic_pb = wilson(perfectos, n_jug)

    p_esc = cargar_p_escalon()
    p_regla = p_sin_cruzar(p_esc)
    it_por_sesion = 400          # intentos de 8-4 en una sesión intensa (supuesto)
    sesiones_por_semana = 5

    print("=== INSUMOS ===")
    print(f"  8-4 IL: {n_jug} corredores, {perfectos} con PB perfecto "
          f"-> P(PB)={p_pb:.4f} (IC {ic_pb[0]:.4f}-{ic_pb[1]:.4f})")
    print(f"  p_escalon (7 secciones): {p_esc:.4f} -> P(sin cruzar)={p_regla:.4f}")
    print(f"  Corredores con perfecto: "
          f"{', '.join(sorted({r['jugador'] for r in il if int(r['delta_frames'])==0}))}")
    print()

    # --- Tabla en función de T --------------------------------------------
    print("=== P(RUN PERFECTO) COMO FUNCIÓN DEL GRIND T POR CORREDOR ===")
    print(f"{'T (intentos 8-4)':>18} | {'p84':>12} | {'P(run perf.)':>12} | "
          f"{'it. 50%':>10} | {'it. 99%':>10}")
    tabla = []
    for T in (100, 300, 1000, 3000, 10000, 30000):
        p84 = p_desde_pb(p_pb, T)
        p_run = p84 * p_regla
        r = {
            "T_intentos_por_corredor": T,
            "p84": p84,
            "p_run_perfecto": p_run,
            "intentos_50pct": it50(p_run),
            "intentos_99pct": it_objetivo(p_run, 0.99),
        }
        tabla.append(r)
        it50s = r["intentos_50pct"]
        it99s = r["intentos_99pct"]
        print(f"{T:>18} | {p84:>12.3e} | {p_run:>12.3e} | "
              f"{('inf' if it50s==float('inf') else f'{it50s:,}'):>10} | "
              f"{('inf' if it99s==float('inf') else f'{it99s:,}'):>10}")

    # --- Escenario de referencia: T = 3000 (grind de meses) ---------------
    T_ref = 3000
    p84_ref = p_desde_pb(p_pb, T_ref)
    p_run_ref = p84_ref * p_regla

    print()
    print(f"=== ESCENARIO DE REFERENCIA (T={T_ref} intentos por corredor) ===")
    print(f"  p84 = {p84_ref:.3e}")
    print(f"  P(run perfecto) = {p_run_ref:.3e}")
    print(f"  Intentos para 50 %: {it50(p_run_ref):,}")
    print(f"  Intentos para 99 %: {it_objetivo(p_run_ref, 0.99):,}")

    # --- Traducción a tiempo humano ---------------------------------------
    ritmos = [3, 5, 8, 12]   # intentos completos por hora (incluye reinicios)
    print()
    print("  Traducción a tiempo (a distintos ritmos de intentos completos/hora):")
    traduccion = []
    it50_ref = it50(p_run_ref)
    for rph in ritmos:
        horas = it50_ref / rph
        traduccion.append({"intentos_por_hora": rph, "horas": horas})
        print(f"    {rph:>2} intentos/h -> {horas:,.0f} h "
              f"({horas/24:,.0f} días, {horas/24/365:.2f} años)")

    # --- Evento "alguien, algún día" --------------------------------------
    # Si N corredores grindean en paralelo, la probabilidad acumulada crece.
    print()
    print("=== EVENTO: ¿ALGÚN HUMANO, ALGÚN DÍA? ===")
    print("  Si la comunidad mantiene N corredores activos, cada uno con la")
    print("  misma p_run por intento, la probabilidad de que AL MENOS UNO lo")
    print("  logre en un periodo crece con el número total de intentos.")
    escenarios = []
    for corredores in (1, 3, 10):
        for anios in (1, 5, 10, 25):
            intentos_totales = (corredores * it_por_sesion * sesiones_por_semana
                                * 52 * anios)
            p_alguno = 1 - (1 - p_run_ref) ** intentos_totales
            escenarios.append({
                "corredores": corredores, "anios": anios,
                "intentos_totales": intentos_totales,
                "p_alguno_lo_logre": p_alguno,
            })
    for e in escenarios:
        print(f"  {e['corredores']:>2} corredores, {e['anios']:>2} años "
              f"({e['intentos_totales']:>12,} intentos) -> "
              f"P = {100*e['p_alguno_lo_logre']:6.2f} %")

    salida = {
        "insumos": {
            "n_corredores_il": n_jug, "perfectos_il": perfectos,
            "p_pb_perfecto": p_pb, "ic95_p_pb": ic_pb,
            "p_escalon": p_esc, "p_sin_cruzar_regla": p_regla,
            "corredores_con_perfecto": sorted(
                {r["jugador"] for r in il if int(r["delta_frames"]) == 0}),
        },
        "tabla_por_T": tabla,
        "escenario_referencia": {
            "T": T_ref, "p84": p84_ref, "p_run_perfecto": p_run_ref,
            "intentos_50pct": it50_ref,
            "intentos_99pct": it_objetivo(p_run_ref, 0.99),
            "traduccion_tiempo": traduccion,
        },
        "evento_algun_humano": escenarios,
        "supuestos": {
            "intentos_8_4_por_sesion": it_por_sesion,
            "sesiones_por_semana": sesiones_por_semana,
            "nota": ("T (grind por corredor) no está medido con precisión; se "
                     "presenta como rango. Los intentos por sesión son un "
                     "supuesto declarado, no una medición."),
        },
    }
    ruta = os.path.join(PROC, "modelo_integrado.json")
    json.dump(salida, open(ruta, "w", encoding="utf-8"), ensure_ascii=False,
              indent=2, default=str)
    print()
    print(f"-> {ruta}")


if __name__ == "__main__":
    main()
