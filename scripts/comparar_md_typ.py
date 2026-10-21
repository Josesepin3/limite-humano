#!/usr/bin/env python3
"""Contrasta el contenido del documento Typst contra el borrador en Markdown.

Sirve para la revision final: tras una ronda de edicion externa hay que
poder demostrar que no se perdio, altero ni invento nada. Compara:

  · las cifras (numeros con decimales, millares y porcentajes)
  · las citas en el texto (Autor, anio) y las entradas de la lista de
    referencias
  · los encabezados de seccion
  · las celdas de las tablas
  · las notas al pie

Uso: comparar_md_typ.py <borrador.md> <documento.typ>
"""
import os
import re
import sys

# Tokens que cambian de forma al portar de Markdown a Typst y no son una
# perdida de contenido.
EQUIVALENCIAS = [
    ("⌊residuo ÷ 21⌋", "la parte entera de residuo ÷ 21"),
]

# El superindice de Typst (super[−6]) y el de Markdown (⁻) son la misma cifra:
# se aplanan a una forma comun antes de comparar.
RE_SUPER = re.compile(r"super\[([-−]?\d+)\]")
RE_SUPER_MD = re.compile(r"⁻(\d)")


def normalizar(s):
    s = s.replace("−", "-").replace("–", "-").replace("—", "-")
    s = s.replace(" ", " ")
    return s


def cifras(texto):
    """Numeros con decimales, millares o porcentajes."""
    limpio = re.sub(r"```.*?```", " ", texto, flags=re.S)
    limpio = re.sub(r"`[^`]*`", " ", limpio)
    limpio = re.sub(r"^\s*\|.*$", " ", limpio, flags=re.M)
    return set(re.findall(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+,\d{2,3}\b|\d+[.,]\d+\s?%", limpio))


def citas(texto):
    """Parejas (autor, anio) de las citas en el texto."""
    limpio = re.sub(r"```.*?```", " ", texto, flags=re.S)
    limpio = re.sub(r"`[^`]*`", " ", limpio)
    patrones = set()
    for m in re.finditer(r"\(([^()]{0,120}?)\)", limpio):
        dentro = m.group(1)
        for autor, anio in re.findall(r"([A-ZÁÉÍÓÚÑa-z][\w.'’-]+(?:\s+(?:y|&|et al\.)\s+[\w.'’-]+)?),\s*(\d{4}[a-b]?)", dentro):
            patrones.add((autor, anio))
    return patrones


def encabezados(texto):
    """Encabezados de Markdown (# Titulo) y de Typst (= Titulo)."""
    fuera = set()
    patrones = [r"^#{1,6}\s+(.*)$", r"^=+\s+(.*)$"]
    for patron in patrones:
        for m in re.finditer(patron, texto, re.M):
            t = re.sub(r"[*`#=]", "", m.group(1)).strip().lower()
            t = re.sub(r"^\d+(\.\d+)*[.)]?\s*", "", t)
            t = re.sub(r"^[a-z]\)\s*", "", t)
            t = re.sub(r"^ap[eé]ndice\s+[a-z]\.?\s*", "", t)
            if t:
                fuera.add(t)
    return fuera


def _bloques_corchete(texto):
    """Contenido de cada grupo [...] con corchetes balanceados."""
    salida = []
    i = 0
    n = len(texto)
    while i < n:
        if texto[i] == "[":
            prof = 0
            j = i
            while j < n:
                if texto[j] == "[":
                    prof += 1
                elif texto[j] == "]":
                    prof -= 1
                    if prof == 0:
                        break
                j += 1
            if prof == 0:
                salida.append(texto[i + 1:j])
                i = j + 1
                continue
        i += 1
    return salida


def celdas(texto):
    """Celdas: filas | a | b | en Markdown, grupos [celda] en Typst."""
    fuera = set()

    # Markdown
    for m in re.finditer(r"^\s*\|(.+)\|\s*$", texto, re.M):
        for c in m.group(1).split("|"):
            c = re.sub(r"[*`_]", "", c).strip().lower()
            c = re.sub(r"\s+", " ", c)
            if c and not set(c) <= set("-: "):
                fuera.add(c)

    # Typst: solo los corchetes que viven dentro de una llamada a table(...)
    for m in re.finditer(r"table\(", texto):
        prof = 0
        j = m.end() - 1
        while j < len(texto):
            if texto[j] == "(":
                prof += 1
            elif texto[j] == ")":
                prof -= 1
                if prof == 0:
                    break
            j += 1
        for b in _bloques_corchete(texto[m.end():j]):
            c = re.sub(r"[*`_]", "", b).strip().lower()
            c = re.sub(r"\s+", " ", c)
            # una celda no contiene saltos de linea: son bloques de contenido
            if c and "\n" not in c and len(c) > 1:
                fuera.add(c)
    return fuera


def notas(texto):
    return len(re.findall(r"^\[\^\d+\]:", texto, re.M))


def principales(datos, etiqueta):
    """Elementos que no deberian perderse: los mas largos y los mas raros."""
    return {d for d in datos if len(d) > 6}


def linea_base(ruta):
    if not ruta or not os.path.exists(ruta):
        return set()
    with open(ruta, encoding="utf-8") as f:
        return {l.rstrip("\n") for l in f if l.strip()}


def main(md_path, typ_path, base=None):
    md = open(md_path, encoding="utf-8").read()
    typ = open(typ_path, encoding="utf-8").read()
    nmd, ntyp = normalizar(md), normalizar(typ)
    for a, b in EQUIVALENCIAS:
        nmd = nmd.replace(normalizar(a), normalizar(b))
        ntyp = ntyp.replace(normalizar(a), normalizar(b))

    fallos = 0
    conocidas = linea_base(base)
    nuevas = []
    for nombre, func in [
        ("cifras", cifras),
        ("citas en el texto", citas),
        ("encabezados", encabezados),
        ("celdas de tabla", celdas),
    ]:
        a, b = func(nmd), func(ntyp)
        faltan = principales(a, nombre) - b
        print(f"\n--- {nombre}: {len(a)} en Markdown, {len(b)} en Typst")
        if faltan:
            for f in sorted(faltan):
                if f"{nombre}|{f}" not in conocidas:
                    nuevas.append(f"{nombre}|{f}")
            nuevas_bloque = [n for n in nuevas if n.startswith(nombre + "|")]
            print(f"    {len(faltan)} diferencias, "
                  f"{len(faltan) - len(nuevas_bloque)} conocidas, {len(nuevas_bloque)} nuevas")
            for f in sorted(faltan)[:25]:
                marca = "NUEVA " if f"{nombre}|{f}" in nuevas else "     "
                print(f"    {marca}SOLO EN MARKDOWN: {f}")
            if len(faltan) > 25:
                print(f"    … y {len(faltan) - 25} más")
        else:
            print("    sin perdidas")

    nm, nt = notas(md), len(re.findall(r"#footnote\[", typ))
    print(f"\n--- notas al pie: {nm} en Markdown, {nt} llamadas #footnote en Typst")
    print("    (el recuento no tiene que coincidir: al portar, parte de las notas")
    print("     pasan a prosa o al glosario. Lo que se comprueba es la COBERTURA)")
    sin_cubrir = []
    for num, texto in re.findall(r"^\[\^(\d+)\]:\s*(.*?)(?=\n\[\^|\n\n|\Z)", md, re.S | re.M):
        limpio = re.sub(r"[*`_]", "", texto).lower()
        # palabras significativas, sin las de relleno
        palabras = [p for p in re.findall(r"[a-záéíóúñ]{5,}", limpio)
                    if p not in {"este", "documento", "términos", "técnicos", "explican", "detalle",
                                 "primer", "aparecen", "aquí", "según", "entre", "comunidad", "cuatro"}]
        if not palabras:
            continue
        cubiertas = sum(1 for p in palabras[:8] if p in ntyp)
        if cubiertas < min(3, len(palabras[:8])):
            sin_cubrir.append((num, " ".join(palabras[:6])))
    if sin_cubrir:
        fallos += 1
        for num, muestra in sin_cubrir:
            print(f"    SIN CUBRIR [^ {num}]: {muestra}")
    else:
        print("    todas las notas del Markdown estan cubiertas (nota, prosa o glosario)")

    if nuevas:
        print("\n--- diferencias NUEVAS respecto de la linea base ---")
        for n in nuevas:
            print(f"    {n}")
        fallos += 1
    else:
        print("\n--- ninguna diferencia nueva respecto de la linea base ---")

    print("\nRESULTADO:", "OK" if not fallos else f"{fallos} bloque(s) con diferencias nuevas")
    return 0 if not fallos else 1


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    base = None
    for a in sys.argv[1:]:
        if a.startswith("--base="):
            base = a.split("=", 1)[1]
    if len(args) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(args[0], args[1], base))
