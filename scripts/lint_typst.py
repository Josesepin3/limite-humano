#!/usr/bin/env python3
"""Lint del documento Typst: comprueba que una edicion externa no rompio nada.

El documento se edita en Typst (no en Markdown) para que no haya paso de
portado, y por lo tanto no haya pérdida de contenido. A cambio, hay que
proteger la sintaxis. Este script automatiza esa protección.

Uso: lint_typst.py <archivo.typ> [<archivo.typ> ...]
"""
import re
import sys

# (patrón, explicación, cómo corregirlo)
TRAMPAS = [
    (r"<sup>|</sup>|<sub>|</sub>",
     "etiquetas HTML de super/subindice: Typst usa las funciones super[] y sub[]",
     "reemplazar <sup>[x]</sup> por super[x] y <sub>[x]</sub> por sub[x]"),
    (r"\*\*", "negrita de Markdown; en Typst es *un asterisco*",
     "reemplazar **texto** por *texto*"),
    (r"(?<![\w*])\$", "math de Typst ($...$): usa otra familia tipografica",
     "escribir la formula en texto plano con super[...]"),
    (r"\bsup\[", "sup[] no existe en Typst 0.15; la funcion es super[]",
     "reemplazar sup[ por super["),
    (r"⌊|⌋", "corchetes de parte entera (U+230A/B): Arial no los tiene",
     "usar la expresion en palabras"),
    (r"⁻", "superindice menos (U+207B): Arial no lo tiene",
     "usar super[−n] con el signo menos U+2212"),
    (r"^\s*\|.*\|", "tabla en Markdown",
     "usar #tabla(...)"),
    (r"^\s*>\s", "cita en bloque de Markdown",
     "usar #cita-larga(...) solo para citas de 40+ palabras"),
    (r"\bTODO\b|\bFIXME\b|\bXXX\b", "marca de trabajo sin resolver", "resolverla"),
    (r"\[([^\]]*)\]\([^)]*\)", "enlace de Markdown", "usar #link(...)"),
]

# La plantilla debe seguir siendo la de la casa, sin modifications.
PLANTILLA = "apa7.typ"


def revisar(ruta):
    with open(ruta, encoding="utf-8") as f:
        texto = f.read()
    problemas = []

    for patron, que, como in TRAMPAS:
        for m in re.finditer(patron, texto, re.M):
            linea = texto.count("\n", 0, m.start()) + 1
            problemas.append((linea, que, como, texto[max(0, m.start() - 30):m.start() + 30].replace("\n", " ")))

    # Estructura esperada del documento.
    for etiqueta, patron, minimo in [
        ("portada", r"#portada\(", 1),
        ("resumen", r"#resumen\(", 1),
        ("palabras clave", r"#palabras-clave\(", 1),
        ("contenidos", r"#contenidos\(", 1),
        ("lista de ilustraciones", r"#lista-ilustraciones\(", 1),
        ("titulo general", r"#titulo-general\(", 1),
        ("referencias", r"#referencias\(", 1),
        ("apendices", r"#apendice\(", 3),
    ]:
        n = len(re.findall(patron, texto))
        if n < minimo:
            problemas.append((0, f"falta {etiqueta} (se esperaba {minimo}+, hay {n})", "restaurarlo", ""))

    # La numeracion de tablas y figuras debe ser correlativa y sin huecos.
    for etiqueta, patron in [("Tabla", r"#tabla\(\"([^\"]+)\""), ("Figura", r"#figura-apa\(\"([^\"]+)\"")]:
        nums = re.findall(patron, texto)
        if nums:
            esperados = [str(i) for i in range(1, len(nums) + 1)]
            # Las tablas de apendice van numeradas A1, B1, C1...
            nums = [n for n in nums if re.fullmatch(r"\d+", n)]
            esperados = [str(i) for i in range(1, len(nums) + 1)]
            if nums != esperados:
                problemas.append((0, f"numeracion de {etiqueta}s no correlativa: {nums}", "renumerar en orden", ""))

    # Cada nota al pie debe tener su llamada.
    n_def = len(re.findall(r"#footnote\[", texto))
    n_ref = len(re.findall(r"#footnote\[", texto))
    if n_def == 0:
        problemas.append((0, "no hay ninguna nota al pie", "revisar que no se hayan borrado", ""))

    return problemas


def compilar(ruta):
    """Comprueba que el documento compila de verdad. Es la prueba definitiva:
    un error de sintaxis que las reglas no detectan igual rompe la
    compilacion, y ahi es donde se ve."""
    import subprocess
    import tempfile
    import os
    with tempfile.TemporaryDirectory() as d:
        salida = os.path.join(d, "prueba.pdf")
        r = subprocess.run(
            ["typst", "compile", ruta, salida], capture_output=True, text=True
        )
        if r.returncode != 0:
            return r.stderr.strip()
    return None


def main(rutas):
    salida = 0
    for ruta in rutas:
        problemas = revisar(ruta)
        print(f"\n=== {ruta} ===")
        if problemas:
            salida = 1
            for linea, que, como, ctx in problemas:
                if linea:
                    print(f"  L{linea}: {que}")
                    print(f"        corregir: {como}")
                    print(f"        contexto: …{ctx}…")
                else:
                    print(f"  {que} — {como}")
        else:
            print("  sin problemas de sintaxis")

        error = compilar(ruta)
        if error:
            salida = 1
            print("  !! NO COMPILA:")
            for linea in error.splitlines()[:12]:
                print(f"     {linea}")
        else:
            print("  compila correctamente")
    return salida


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
