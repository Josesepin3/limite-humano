#!/usr/bin/env python3
"""Comprueba la coherencia entre las citas del texto y la lista de referencias.

Reglas de APA 7 que verifica:

  · Toda cita en el texto (parentetica o narrativa) tiene una entrada
    correspondiente en la lista de referencias.        (sin "sostenes" huerfanos)
  · Toda entrada de la lista se cita al menos una vez en el texto.
                                                        (sin "referencias huerfanas")
  · Las notas al pie tambien citan: una nota que hace una afirmacion
    verificable debe apuntar a una fuente de la lista.

Detecta los dos formatos de cita:
  PARENTETICA  (Garcia y Perez, 2019)  /  (Garcia, 2019, p. 44)
  NARRATIVA    Garcia y Perez (2019) midieron...

Uso: verificar_citas.py <documento.typ>
"""
import re
import sys

# Palabras que aparecen en un nombre de autor y no son autores.
NO_AUTOR = {
    "el", "la", "los", "las", "un", "una", "este", "esta", "esto", "ver",
    "nivel", "seccion", "tabla", "figura", "apartado", "capitulo", "anexo",
    "nota", "speedrun", "leaderboard", "frame", "frames", "p", "pp",
}


def autor_raiz(autor):
    """Clave de comparacion: primer apellido del autor, en minusculas.

    "Bailey, D."      -> "bailey"
    "Orland, K."      -> "orland"
    "speedrun.com."  -> "speedrun.com"
    "averge11."       -> "averge11"
    """
    a = autor.strip().rstrip(".")
    # autor corporativo con punto final
    if re.fullmatch(r"(?:https?://)?[\w.-]+\.(?:com|org|net|io|es|co|uk)", a, re.I):
        return a.lower()
    # "Apellido, Iniciales" -> "Apellido"
    a = re.split(r",", a)[0].strip()
    # "Apellido y Apellido" -> el primero
    a = re.split(r"\s+(?:y|&|and)\s+", a)[0].strip()
    return a.rstrip(".").lower()


def referencias(texto):
    m = re.search(r"#referencias\(\((.*?)\n\)\)\n", texto, re.S)
    if not m:
        return []
    entradas = []
    for em in re.finditer(r"\[\n\s*(.*?)\n\s*\],", m.group(1), re.S):
        t = re.sub(r"[#*_]", "", em.group(1)).strip()
        t = re.sub(r"\s+", " ", t)
        am = re.match(r"(.+?)\.\s*\((\d{4}[a-z]?)", t)
        if am:
            entradas.append((am.group(1).strip(), am.group(2)))
    return entradas


def citas(texto, autores_conocidos):
    """Citas del texto, en los dos formatos de APA.

    `autores_conocidos` son las raíces de autor que ya están en la lista de
    referencias. Se usan para distinguir una cita narrativa real ("Maru
    (2023)") de un sintagma que solo parece una ("Nintendo (1985)").
    """
    cuerpo = re.sub(r"#referencias\(\(.*?\n\)\)\n", " ", texto, flags=re.S)
    cuerpo = re.sub(r"```.*?```", " ", cuerpo, flags=re.S)
    cuerpo = re.sub(r"`[^`]*`", " ", cuerpo)
    cuerpo = re.sub(r"#[a-zA-Z]+\[[^\]]*\]", " ", cuerpo)

    encontradas = set()

    # Narrativas: "Maru (2023)", "LeKukie (2022)"
    for m in re.finditer(
        r"([A-Za-zÁÉÍÓÚÑ][\w.’'&-]*(?:\s+(?:y|&)\s+[\w.’'&-]+)?)\s*\((\d{4}[a-z]?)", cuerpo
    ):
        autor, anio = m.group(1), m.group(2)
        if autor_raiz(autor) in autores_conocidos or autor.lower() in {
            "averge11", "yelia64", "speedrun.com"
        }:
            encontradas.add((autor, anio))

    # Parentheticas: "(Maru, 2023)", "(HappyLee, 2011; Orland, 2023)"
    for m in re.finditer(r"\(([^()]{0,160}?)\)", cuerpo):
        d = m.group(1)
        if re.search(r"https?://", d):
            continue
        for autor, anio in re.findall(
            r"([A-Za-zÁÉÍÓÚÑ][\w.’'&-]*(?:\s+(?:y|&|et al\.)\s+[\w.’'&-]+)?)\s*,\s*(\d{4}[a-z]?)",
            d,
        ):
            if autor_raiz(autor) in autores_conocidos or autor.lower() in {
                "averge11", "yelia64", "speedrun.com"
            }:
                encontradas.add((autor, anio))
    return encontradas


def notas_al_pie(texto):
    notas = []
    for m in re.finditer(r"#footnote\[", texto):
        k = m.end()
        prof = 1
        while k < len(texto) and prof:
            if texto[k] == "[":
                prof += 1
            elif texto[k] == "]":
                prof -= 1
            k += 1
        notas.append(re.sub(r"\s+", " ", texto[m.end():k - 1]).strip())
    return notas


def main(ruta):
    texto = open(ruta, encoding="utf-8").read()
    refs = referencias(texto)
    conocidos = {autor_raiz(a) for a, _ in refs}
    cits = citas(texto, conocidos)

    print(f"=== {ruta} ===")
    print(f"entradas en la lista de referencias: {len(refs)}")
    print(f"citas distintas en el texto:        {len(cits)}\n")

    huerfanas, sin_entrada = [], []

    # cita sin entrada: el autor no esta en la lista
    for autor, anio in sorted(cits):
        if autor_raiz(autor) not in conocidos:
            sin_entrada.append((autor, anio))

    # referencia sin cita: la entrada no aparece citada en el texto
    for autor, anio in refs:
        raiz = autor_raiz(autor)
        citado = any(
            autor_raiz(a) == raiz and (y == anio or a.split()[0].lower() == raiz)
            for a, y in cits
        )
        if not citado:
            huerfanas.append((autor, anio))

    print("REFERENCIAS QUE NO SE CITAN EN EL TEXTO:")
    if huerfanas:
        for a, y in huerfanas:
            print(f"    !! {a} ({y})")
    else:
        print("    ninguna")

    print("\nCITAS SIN ENTRADA EN LA LISTA:")
    if sin_entrada:
        for a, y in sin_entrada:
            print(f"    !! {a} ({y})")
    else:
        print("    ninguna")

    # notas al pie: cada una debe citar o no hacer afirmaciones
    notas = notas_al_pie(texto)
    sin_cita = []
    for n in notas:
        tiene = re.search(r"\(([^()]*\d{4}[a-z]?[^()]*)\)", n)
        if not tiene:
            sin_cita.append(n)
    print(f"\nNOTAS AL PIE: {len(notas)}")
    if sin_cita:
        for n in sin_cita:
            print(f"    !! sin cita: {n[:90]}")
    else:
        print("    todas citan una fuente de la lista")

    fallos = len(huerfanas) + len(sin_entrada) + len(sin_cita)
    print("\nRESULTADO:", "OK" if not fallos else f"{fallos} problema(s)")
    return 0 if not fallos else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
