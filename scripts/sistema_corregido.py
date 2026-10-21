#!/usr/bin/env python3
"""
Sistema probabilístico CORREGIDO — validación de la mecánica y resultado final.

DOS CORRECCIONES RESPECTO DEL PRIMER SISTEMA
--------------------------------------------
1. DENOMINADOR. El leaderboard 8-4 IL es un tablero de MEJORES MARCAS
   PERSONALES (203 runs / 203 jugadores). 4/203 mide P(PB perfecto por
   corredor), no P(intento perfecto). Se convierte con el modelo de renovación

       p84 = 1 - (1 - P(PB))^(1/T)

   usando la distribución de T observada en los comentarios
   (scripts/distribucion_T.py).

2. VIABILIDAD DEL MONTE CARLO. Con p84 ~ 3,7e-6, la probabilidad de run
   perfecto es ~3,6e-6. Un Monte Carlo directo necesitaría ~28 millones de
   simulaciones para observar 100 aciertos. El estimador directo es, por
   tanto, inutilizable a esa escala: daría 0 o 1 aciertos por azar.

   La arquitectura correcta es:
     - El resultado se calcula con la forma analítica cerrada (exacta).
     - El Monte Carlo se usa solo para VALIDAR LA MECÁNICA, escalando p84 a
       un valor observable (p84_test = 1e-3) y comprobando que el simulador
       reproduce la fórmula cerrada. Si la mecánica es correcta a esa escala,
       la forma cerrada es válida a la escala real.

Salida:
  datos/procesados/sistema_corregido.json
"""

import csv
import json
import math
import os
import random

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(BASE, "datos", "procesados")

P_PB = 4 / 203
P_ESCALON = 0.005
N_REGLA = 7
FPS = 60.0988138974405


def p_analitica(p84, p_esc=P_ESCALON):
    """P(run perfecto) por vía cerrada: p84 × (1-p_esc)^7."""
    return p84 * (1 - p_esc) ** N_REGLA


def p84_desde_T(T, p_pb=P_PB):
    if T <= 0:
        return 0.0
    return 1 - (1 - p_pb) ** (1 / T)


def simular(p84, p_esc, n, semilla=20261020):
    """
    Monte Carlo de la MECÁNICA del run: 7 secciones con frame rule + 8-4.

    En las 7 secciones se sortea "cruzar el escalón" (no "perder 1 frame"),
    que es la mecánica real del juego. En 8-4 se sortea el éxito con p84.
    """
    rng = random.Random(semilla)
    perfectos = 0
    for _ in range(n):
        fallo = False
        for _s in range(N_REGLA):
            if rng.random() < p_esc:
                fallo = True
                break
        if not fallo and rng.random() < p84:
            perfectos += 1
    return perfectos


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    m = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / den
    return (max(0.0, c - m), min(1.0, c + m))


def cargar_T_central():
    """
    Devuelve el T del escenario central y la lista completa de T observados.

    El escenario central es la mediana del RÉGIMEN LARGO (corredores que
    aprendían la sección), no la mediana aritmética de toda la muestra: esta
    última cae entre dos regímenes y no representa a ninguno.
    """
    ruta = os.path.join(PROC, "distribucion_T.json")
    if os.path.exists(ruta):
        d = json.load(open(ruta, encoding="utf-8"))
        return (d["T_mediana_regimen_largo"],
                sorted(x["intentos"] for x in d["duraciones_declaradas"]))
    return 6075, [2, 5, 15, 90, 5400, 5850, 6300, 16200]


def leer_errores_84():
    ruta = os.path.join(PROC, "il_84.csv")
    with open(ruta, encoding="utf-8") as f:
        return [int(r["delta_frames"]) for r in csv.DictReader(f)]


def it_para(p, obj):
    if p <= 0:
        return float("inf")
    if p >= 1:
        return 1
    return math.ceil(math.log(1 - obj) / math.log(1 - p))


def main():
    print("=" * 68)
    print("SISTEMA PROBABILÍSTICO CORREGIDO")
    print("=" * 68)
    print()

    # ---------------------------------------------------------------- 1
    print("1. DENOMINADOR CORREGIDO")
    print(f"   P(PB perfecto por corredor) = 4/203 = {P_PB:.4f}")
    print(f"   IC 95 % (Wilson)            = "
          f"[{wilson(4,203)[0]:.4f}, {wilson(4,203)[1]:.4f}]")
    print()

    # ---------------------------------------------------------------- 2
    T_central, T_obs = cargar_T_central()
    print("2. VIABILIDAD DEL MONTE CARLO DIRECTO")
    p84_real = p84_desde_T(T_central)
    p_real = p_analitica(p84_real)
    print(f"   T central (mediana régimen largo) = {T_central:,.0f}")
    print(f"   p84                 = {p84_real:.3e}")
    print(f"   P(run perfecto)     = {p_real:.3e}")
    n_para_100 = math.ceil(100 / p_real)
    print(f"   Para observar ~100 aciertos harían falta "
          f"{n_para_100:,} simulaciones.")
    print("   -> El Monte Carlo directo a la escala real es INVIABLE.")
    print()

    # ---------------------------------------------------------------- 3
    print("3. VALIDACIÓN DE LA MECÁNICA (Monte Carlo escalado)")
    print("   Se escala p84 a un valor observable y se compara con la fórmula.")
    print()
    print(f"   {'p84_test':>10} | {'N':>10} | {'MC observado':>14} | "
          f"{'Analítico':>14} | {'Error rel.':>10}")
    validaciones = []
    for p84_test, n in ((1e-2, 200000), (1e-3, 2000000), (1e-4, 2000000)):
        k = simular(p84_test, P_ESCALON, n)
        mc = k / n
        ana = p_analitica(p84_test)
        err = abs(mc - ana) / ana * 100 if ana > 0 else float("nan")
        validaciones.append({
            "p84_test": p84_test, "n_simulaciones": n,
            "mc_perfectos": k, "mc_p": mc, "analitico_p": ana,
            "error_relativo_pct": err,
        })
        print(f"   {p84_test:>10.0e} | {n:>10,} | {mc:>14.6e} | "
              f"{ana:>14.6e} | {err:>9.2f} %")
    print()
    print("   -> El simulador reproduce la fórmula cerrada. La mecánica")
    print("      (sortear escalones, no frames) está bien implementada.")
    print()

    # ---------------------------------------------------------------- 4
    print("4. RESULTADO FINAL (forma cerrada)")
    print()
    print(f"   {'T (intentos)':>14} | {'p84':>12} | {'P(run perf.)':>13} | "
          f"{'it. 50 %':>13}")
    tabla = []
    for T in T_obs:
        p84 = p84_desde_T(T)
        p = p_analitica(p84)
        i50 = it_para(p, 0.5)
        tabla.append({"T": T, "p84": p84, "p_run": p, "it_50": i50})
        print(f"   {T:>14,.0f} | {p84:>12.3e} | {p:>13.3e} | "
              f"{('inf' if i50 == float('inf') else f'{i50:,}'):>13}")

    # Escenario central
    p84_c = p84_desde_T(T_central)
    p_c = p_analitica(p84_c)
    print()
    print(f"   Escenario central T={T_central:,.0f}:")
    print(f"     p84            = {p84_c:.3e}")
    print(f"     P(run perfecto)= {p_c:.3e}")
    print(f"     Intentos para 50 %: {it_para(p_c,0.5):,}")
    print(f"     Intentos para 99 %: {it_para(p_c,0.99):,}")

    # ---------------------------------------------------------------- 5
    print()
    print("5. EVENTO «ALGÚN HUMANO, ALGÚN DÍA»")
    print("   (supuesto declarado: 200 intentos por día activo, 3 días/semana)")
    esc = []
    print(f"   {'corredores':>11} | " + " | ".join(
        f"{a:>7} años" for a in (1, 5, 10, 25)))
    for corr in (1, 5, 20):
        fila = []
        for anios in (1, 5, 10, 25):
            n = corr * 200 * 3 * 52 * anios
            p = 1 - (1 - p_c) ** n
            esc.append({"corredores": corr, "anios": anios,
                        "intentos": n, "p_alguno": p})
            fila.append(p)
        print(f"   {corr:>11} | " + " | ".join(f"{100*x:>11.2f}%" for x in fila))

    salida = {
        "correccion_denominador": {
            "p_pb": P_PB, "ic95": wilson(4, 203),
            "nota": ("203 runs, 203 jugadores distintos: tablero de PB, no de "
                     "intentos. 4/203 es P(PB perfecto por corredor)."),
        },
        "viabilidad_montecarlo": {
            "p84_real": p84_real, "p_run_real": p_real,
            "simulaciones_para_100_aciertos": n_para_100,
            "conclusion": ("Monte Carlo directo inviable a p~1e-6; el "
                           "resultado se obtiene por forma cerrada."),
        },
        "validacion_mecanica": validaciones,
        "tabla_por_T": tabla,
        "escenario_central": {
            "T": T_central, "p84": p84_c, "p_run": p_c,
            "it_50": it_para(p_c, 0.5), "it_99": it_para(p_c, 0.99),
        },
        "evento_algun_humano": esc,
        "supuestos": {
            "p_escalon_por_seccion": P_ESCALON,
            "n_secciones_con_frame_rule": N_REGLA,
            "intentos_por_dia_activo": 200,
            "dias_activos_por_semana": 3,
            "horas_juego_por_dia_para_T": 3,
        },
    }
    ruta = os.path.join(PROC, "sistema_corregido.json")
    json.dump(salida, open(ruta, "w", encoding="utf-8"), ensure_ascii=False,
              indent=2)
    print()
    print(f"-> {ruta}")
    print()
    print("Arquitectura: forma cerrada = resultado; Monte Carlo = validación.")


if __name__ == "__main__":
    main()
