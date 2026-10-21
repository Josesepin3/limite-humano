#!/usr/bin/env python3
"""Perfil estilometrico de la prosa del documento.

Mide los rasgos que hacen que un texto LEAse como generado por una maquina,
que es lo que un lector humano percibe (y no lo que persiguen los detectores
automaticos). Los marcadores son:

  1. BURSTINESS: dispersion de la longitud de las frases. La prosa humana
     alterna frases muy cortas y muy largas; la de maquina se mueve en una
     banda estrecha. Se mide como coeficiente de variacion y como proporcion
     de frases fuera de la banda media (las "outliers").

  2. APERTURAS REPETIDAS: cuantas veces arranca una frase con la misma
     palabra. La prosa de maquina tiende a repetir el mismo patron sintactico.

  3. TRANSICIONES VACIAS: conectores que Annaden sin decir nada
     ("es decir", "en efecto", "cabe destacar", "no solo... sino").

  4. ESTRUCTURA RIGIDA: proporcion de parrafos con la misma forma
     (oracion tematica + apoyo + cierre).

  5. HEDGING: muletillas de atenuacion ("conviene", "podria", "en principio").

  6. LONGITUD DE PARRAFO: dispersion.

Uso: estilometria.py <archivo.typ> [<archivo.typ> ...]
"""
import re
import statistics
import sys
from collections import Counter

CONECTORES_VACIOS = [
    "es decir", "en efecto", "cabe destacar", "cabe mencionar", "conviene "
    "destacar", "es importante recordar", "no solo", "sino que", "sin embargo",
    "por lo tanto", "en consecuencia", "en resumen", "en definitiva",
    "nótese que", "hay que", "por ende", "asimismo", "claro está",
    "evidentemente", "sin duda", "vale la pena", "lo interesante es que",
]

HEDGING = [
    "en principio", "podría", "conviene", "quizá", "quizás", "parece que",
    "se puede", "es posible", "tiende a", "habitualmente", "generalmente",
]


def _quitar_bloque(s, inicio):
    """Elimina desde `inicio` hasta el parentesis que cierra la llamada."""
    i = s.find(inicio)
    if i < 0:
        return s
    j = i + len(inicio) - 1
    prof = 0
    while j < len(s):
        if s[j] == "(":
            prof += 1
        elif s[j] == ")":
            prof -= 1
            if prof == 0:
                break
        j += 1
    return s[:i] + " " + s[j + 1:]


def texto_liso(ruta):
    with open(ruta, encoding="utf-8") as f:
        s = f.read()
    # fuera codigo, comentarios y marcado
    s = re.sub(r"```.*?```", " ", s, flags=re.S)
    s = re.sub(r"//.*", " ", s)
    # bloques de tabla, figura y referencia: su contenido NO es prosa
    for cab in ("#tabla(", "#figura-apa(", "#referencias(", "#apendice("):
        while cab in s:
            nuevo = _quitar_bloque(s, cab)
            if nuevo == s:
                break
            s = nuevo
    s = re.sub(r"\$[^$]*\$", " ", s)
    s = re.sub(r"#[a-zA-Z]+\[", " ", s)
    s = re.sub(r"[#*_`\[\]()]", " ", s)
    return s


def frases(texto):
    t = re.sub(r"\s+", " ", texto)
    partes = re.split(r"(?<=[.!?])\s+(?=[A-Z¿¡\"'(])", t)
    return [p.strip() for p in partes if len(p.split()) >= 3]


def parrafos(texto):
    bloques = re.split(r"\n\s*\n", texto)
    return [b.strip() for b in bloques if len(b.split()) >= 25]


def perfil(ruta):
    texto = texto_liso(ruta)
    fs = frases(texto)
    ps = parrafos(texto)
    longitudes = [len(f.split()) for f in fs]
    plongs = [len(p.split()) for p in ps]

    print(f"\n=== {ruta} ===")
    print(f"  frases: {len(fs)}   palabras: {sum(longitudes)}   parrafos: {len(ps)}")

    # 1. burstiness
    if longitudes:
        media = statistics.mean(longitudes)
        sd = statistics.pstdev(longitudes)
        cv = sd / media if media else 0
        cortas = sum(1 for l in longitudes if l <= 8)
        largas = sum(1 for l in longitudes if l >= 28)
        print(f"  1. BURSTINESS  longitud media {media:.1f} palabras, sd {sd:.1f}, CV {cv:.3f}")
        print(f"     frases cortas (<=8) {cortas} ({cortas/len(longitudes)*100:.1f} %)  |  "
              f"largas (>=28) {largas} ({largas/len(longitudes)*100:.1f} %)")
        print(f"     rango {min(longitudes)}-{max(longitudes)}   "
              f"distribucion: {Counter([l//5*5 for l in longitudes]).most_common()}")

    # 2. aperturas repetidas
    aperturas = [f.split()[0].lower().strip(",;:¿¡") for f in fs if f.split()]
    rep = Counter(aperturas).most_common(8)
    print(f"  2. APERTURAS DE FRASE (las mas repetidas): {rep}")
    distintas = len(set(aperturas))
    print(f"     aperturas distintas: {distintas} de {len(aperturas)} frases "
          f"({distintas/len(aperturas)*100:.0f} % de diversidad)")

    # 3. transiciones vacias
    total = 0
    detalles = []
    for c in CONECTORES_VACIOS:
        n = len(re.findall(re.escape(c), texto, re.I))
        if n:
            detalles.append((n, c))
            total += n
    detalles.sort(reverse=True)
    print(f"  3. TRANSICIONES VACIAS: {total} en total")
    for n, c in detalles:
        print(f"       {n:3d}  {c}")

    # 4. hedging
    th = 0
    for h in HEDGING:
        n = len(re.findall(re.escape(h), texto, re.I))
        if n:
            th += n
            print(f"       {n:3d}  {h}")
    print(f"     total hedging: {th}")

    # 5. longitud de parrafo
    if plongs:
        print(f"  5. PARRAFOS  media {statistics.mean(plongs):.1f} palabras, "
              f"sd {statistics.pstdev(plongs):.1f}, "
              f"rango {min(plongs)}-{max(plongs)}")


def main(rutas):
    for r in rutas:
        perfil(r)
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
