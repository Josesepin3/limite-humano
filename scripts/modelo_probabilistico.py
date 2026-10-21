#!/usr/bin/env python3
"""
Modelo probabilístico del límite humano en Any% de Super Mario Bros.

Idea central
------------
Un run completo exige encadenar K tramos críticos, cada uno con probabilidad de
ejecución perfecta q. Si los tramos son aproximadamente independientes:

        P(run perfecto) = q^K

Con eso se estima el número esperado de intentos hasta conseguir un run perfecto
y se discute qué valores de q son compatibles con la evidencia empírica.

Supuestos (declarados explícitamente, no ocultos):
  - Independencia entre tramos (aproximación; ver limitaciones del documento).
  - q constante por tramo.
  - "Perfecto" = igualar el óptimo teórico, no solo el récord vigente.

Salida: datos/procesados/modelo_probabilistico.json
"""

import json
import math
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(BASE, "datos", "procesados")

FPS = 60.0988138974405
OPTIMO_S = 4 * 60 + 54.265          # 4:54.265, óptimo teórico declarado
RECORD_S = 4 * 60 + 54.332          # récord vigente al cierre del corpus
FRAMES_RESTANTES = round((RECORD_S - OPTIMO_S) * FPS, 2)   # = 4 frames


def intentos_mediana(p):
    """Nº de intentos para alcanzar 50 % de probabilidad acumulada."""
    if p >= 1:
        return 1
    if p <= 1e-15:
        return float("inf")
    return math.ceil(math.log(0.5) / math.log(1 - p))


def tabla_por_tramos(tramos, qs):
    filas = []
    for K in tramos:
        fila = {"tramos_K": K}
        for q in qs:
            p = q ** K
            fila[f"q={q}"] = {"P_run": p, "intentos_50pct": intentos_mediana(p)}
        filas.append(fila)
    return filas


def analisis_8_4(margen_frames, precisiones):
    """
    La sección final (8-4) no tiene frame rule: no hay margen que 'redondee' el error.
    Modelo de ventana: para igualar el óptimo hay que acertar DENTRO de un margen de
    M frames, es decir, ninguna de las (restantes - margen) decisiones debe fallar.
    Si la probabilidad de acertar un frame exigido es r, entonces:

        P(no fallar ninguna de las N exigidas) = r^N   con N = exigidas

    Aquí modelamos dos cantidades distintas:
      - margen_frames: cuántos frames de holgura admite el tramo (M).
      - exigidas (N): decisiones donde el frame exacto es obligatorio.
    """
    filas = []
    for r in precisiones:
        for exigidas in (1, 2, 4, 8):
            p = r ** exigidas
            filas.append({
                "precision_por_decision_r": r,
                "decisiones_exigidas": exigidas,
                "P_seccion_por_intento": p,
                "intentos_50pct": intentos_mediana(p) if p < 1 else 1,
                "intentos_99pct": (math.ceil(math.log(0.01) / math.log(1 - p))
                                   if 0 < p < 1 else 1),
            })
    return filas


def main():
    tramos = [10, 20, 30, 40, 50, 60, 80, 100]
    qs = [0.99, 0.995, 0.999, 0.9995, 0.9999, 0.99995, 0.99999]

    precisiones = [0.5, 0.8, 0.9, 0.95, 0.99, 0.999]

    resultado = {
        "constantes": {
            "fps_ntsc": FPS,
            "optimo_teorico_s": OPTIMO_S,
            "record_s": RECORD_S,
            "frames_restantes_hasta_optimo": FRAMES_RESTANTES,
            "seg_restantes": RECORD_S - OPTIMO_S,
        },
        "modelo": "P(run perfecto) = q^K  (K tramos críticos independientes, precisión q)",
        "supuestos": [
            "Los tramos críticos se tratan como independientes.",
            "q es constante entre tramos y entre intentos.",
            "Perfecto = igualar el óptimo teórico, no el récord vigente.",
            "No se modela fatiga, aprendizaje intra-sesión ni varianza entre jugadores.",
        ],
        "tabla_tramos": tabla_por_tramos(tramos, qs),
        "analisis_8_4": {
            "descripcion": ("8-4 es el único tramo sin frame rule: el error no se "
                            "redondea, cada frame cuenta."),
            "margen_frames": FRAMES_RESTANTES,
            "escenarios": analisis_8_4(FRAMES_RESTANTES, precisiones),
        },
    }

    ruta = os.path.join(PROC, "modelo_probabilistico.json")
    json.dump(resultado, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print(f"Frames restantes hasta el óptimo: {FRAMES_RESTANTES:.0f} ({RECORD_S-OPTIMO_S:.3f} s)")
    print("\nP(run perfecto) = q^K")
    print(f"{'K':>4} | " + " | ".join(f"q={q:<8}" for q in qs))
    for fila in resultado["tabla_tramos"]:
        print(f"{fila['tramos_K']:>4} | " + " | ".join(
            f"{fila[f'q={q}']['P_run']:.2e}" for q in qs))
    print("\nEscenarios en 8-4 (margen 4 frames; N = decisiones exigidas):")
    for e in resultado["analisis_8_4"]["escenarios"]:
        print(f"  r={e['precision_por_decision_r']:<6} N={e['decisiones_exigidas']:<2} "
              f"P/sección={e['P_seccion_por_intento']:.6f} "
              f"intentos(50%)={e['intentos_50pct']:>7} intentos(99%)={e['intentos_99pct']}")
    print(f"\n-> {ruta}")


if __name__ == "__main__":
    main()
