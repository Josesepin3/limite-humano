#!/usr/bin/env python3
"""Verifica la maquetacion APA 7 sobre el PDF generado.

Contrato de verificacion de la plantilla (apa7.typ, seccion 7), en puntos PDF
(1 in = 72 pt):

  - Pagina 612 x 792 pt
  - x minimo del texto = 72,0 (margen de 1 in)
  - x maximo <= 540,0 y VARIANTE entre renglones (no justificado)
  - Primer renglón con sangria en x = 108,0 (= 72 + 36)
  - Diferencia vertical entre renglones seguidos = 22,0 pt
  - Numero de pagina en el borde derecho de la franja superior (~540)

Deltas admitidos (tolerancia +/- 2,5 pt):
  22,0  grilla del cuerpo (doble espacio, APA 7 seccion 2.21)
  11,0  cuerpo de celda de tabla a espacio simple (APA 7 seccion 7.8: "the
        table body may be single-spaced")

Notas de la medicion:
  - Se FUSIONAN los renglones separados por menos de 6 pt: una misma linea
    visual que mezcla estilos (negrita, cursiva, codigo monoespaciado, matematica)
    reporta distinta linea base en cada fragmento, y pdftotext los separa.
  - Los bloques se separan donde el hueco supera 30 pt: ahi empieza la nota al
    pie, que va en cuerpo menor y no pertenece a la grilla del cuerpo.

Uso: verificar_apa.py <pdf>
"""
import re
import subprocess
import sys
from collections import Counter

MARGEN = 72.0
DER = 540.0
SANG = 108.0
TOL = 2.5
CORTE_BLOQUE = 30.0


def main(path):
    html = subprocess.run(
        ["pdftotext", "-bbox", path, "-"], capture_output=True, text=True, check=True
    ).stdout
    pages = re.findall(
        r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', html, re.S
    )
    print(f"paginas: {len(pages)}")
    ok = True
    n_celdas = 0
    n_notas = 0

    for i, (w, h, body) in enumerate(pages, 1):
        words = re.findall(
            r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>',
            body,
        )
        if not words:
            print(f"  p{i}: (vacia)")
            continue
        W, H = float(w), float(h)
        if abs(W - 612) > 0.5 or abs(H - 792) > 0.5:
            print(f"  p{i}: !! tamano {W}x{H}")
            ok = False

        # --- agrupar en renglones visuales -------------------------------------
        crudos = {}
        for xmin, ymin, xmax, ymax, txt in words:
            crudos.setdefault(round(float(ymin), 1), []).append(
                (float(xmin), float(xmax), float(ymax), float(ymax) - float(ymin), txt)
            )
        rows = {}
        for k in sorted(crudos):
            if rows:
                pk = max(rows)
                if k - pk < 6.0:  # misma linea visual
                    rows[pk].extend(crudos[k])
                    continue
            rows[k] = list(crudos[k])

        # --- encabezado / cuerpo / nota al pie ---------------------------------
        head = {k: v for k, v in rows.items() if k < 60}
        # Una nota al pie va en cuerpo menor: alto de glifo ~8,8 frente a ~10,3
        # del cuerpo de 11 pt. Se mide el alto de la PALABRA mas alta del
        # renglon, no el del renglon entero, porque un renglon fusionado puede
        # mezclar el marcador de la nota (6,7) con su texto (8,8).
        pie_rows = {
            k: v
            for k, v in rows.items()
            if k >= 60 and max(w[3] for w in v) < 9.5
        }
        body_rows = {k: v for k, v in rows.items() if k >= 60 and k not in pie_rows}
        n_notas += len(pie_rows)

        # --- numero de pagina -------------------------------------------------
        for v in head.values():
            for xmin, xmax, ymax, alto, txt in v:
                if txt.strip().isdigit() and not (539.0 <= xmax <= 540.6):
                    print(f"  p{i}: !! n. pag en xMax={xmax:.1f} (esperado ~540)")
                    ok = False

        if not body_rows:
            print(f"  p{i}: {W:.0f}x{H:.0f} (sin cuerpo)")
            continue

        ys = sorted(body_rows)
        allx = [w[0] for v in body_rows.values() for w in v]
        allxe = [w[1] for v in body_rows.values() for w in v]
        xmin_g, xmax_g = min(allx), max(allxe)
        linex = sorted(min(w[0] for w in body_rows[k]) for k in ys)
        indents = sum(1 for x in linex if abs(x - SANG) < 0.6)

        # --- ritmo: dentro de cada bloque, todos los huecos valen 22 o 11 -----
        bloques = [[ys[0]]]
        for j in range(len(ys) - 1):
            hueco = ys[j + 1] - ys[j]
            if hueco > CORTE_BLOQUE:
                bloques.append([])
            bloques[-1].append(ys[j + 1])
        # El ULTIMO bloque de la pagina es el de la nota al pie, que va en
        # cuerpo menor y a espacio simple: se excluye del control de grilla.
        if len(bloques) > 1 and any(k in pie_rows for k in bloques[-1]):
            bloques.pop()
        malos = []
        c = Counter()
        for b in bloques:
            for j in range(len(b) - 1):
                hueco = round(b[j + 1] - b[j], 1)
                c[hueco] += 1
                if abs(hueco - 22.0) <= TOL:
                    continue
                if abs(hueco - 11.0) <= TOL:
                    n_celdas += 1
                    continue
                malos.append((hueco, b[j], b[j + 1]))

        print(
            f"  p{i}: {W:.0f}x{H:.0f} filas={len(ys)} xMin={xmin_g:.1f} "
            f"xMax={xmax_g:.1f} sangr108={indents}/{len(linex)}"
            + (f" notas={len(pie_rows)}" if pie_rows else "")
        )
        print(f"       deltas={c.most_common(4)}")
        if xmin_g < MARGEN - 0.6:
            print(f"       !! xMin {xmin_g:.1f} < {MARGEN}")
            ok = False
        if xmax_g > DER + 0.6:
            print(f"       !! xMax {xmax_g:.1f} > {DER}")
            ok = False
        if malos:
            for hueco, ya, yb in malos:
                ta = " ".join(w[4] for w in body_rows[ya])[:48]
                tb = " ".join(w[4] for w in body_rows[yb])[:48]
                print(f"       !! hueco {hueco} entre y={ya} y y={yb}")
                print(f"          desde: {ta}")
                print(f"          hasta: {tb}")
            ok = False

    print(f"\nceldas de tabla a espacio simple: {n_celdas}")
    print(f"renglones de nota al pie: {n_notas}")
    print("RESULTADO:", "OK (grilla APA)" if ok else "REVISAR")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
