# El límite humano: ¿Puede el hombre alcanzar la perfección de la máquina?

**Estudio de caso:** la categoría Any% de *Super Mario Bros.* (NES, 1985)

Este repositorio contiene el documento de investigación, los datos y el código
que reproducen todos sus resultados. Se publica como anexo abierto del artículo:
el manuscrito no incluye archivos adjuntos, y este repositorio es el lugar donde
viven los datos y el código que lo respaldan.

- **Autor:** Jose Sebastian Pinto Rondon
- **Institución:** Institución Universitaria Pascual Bravo
- **Materia:** Lenguaje y Cultura
- **Docente:** Jhony Alexander Restrepo Tobon
- **Fecha de corte de los datos:** 19 de octubre de 2026
- **Manuscrito (APA 7):** [`documento/limite-humano.pdf`](documento/limite-humano.pdf)
  — fuente en [`documento/limite-humano.typ`](documento/limite-humano.typ)
- **Borrador de trabajo:** [`documento/borrador.md`](documento/borrador.md)

---

## Qué contiene

| Carpeta | Contenido |
|---|---|
| `documento/` | El manuscrito (Typst + PDF), el borrador en Markdown y las figuras (SVG y PNG) |
| `datos/crudos/` | Las respuestas originales de las fuentes (sin transformar) |
| `datos/procesados/` | Los datos limpios y los resultados del sistema |
| `scripts/` | El código que va de los datos crudos a los resultados |

### El manuscrito en APA 7

El documento publicado se compila con [Typst](https://typst.app) usando la
plantilla APA 7 de la casa (`documento/apa7.typ`, copia de
`~/Plantillas/apa7.typ`):

```bash
cd documento
typst compile limite-humano.typ limite-humano.pdf
```

Requiere Typst ≥ 0.15 y la familia Arial completa (regular, negrita, cursiva y
negrita cursiva). `scripts/verificar_apa.py` comprueba la maquetación sobre el
PDF generado, contra el contrato de la plantilla:

```bash
python3 scripts/verificar_apa.py documento/limite-humano.pdf
```

Verifica el papel Carta (612 × 792 pt), los márgenes de 1 in, la sangría de
0,5 in, el doble espacio de 22 pt entre renglones, el borde irregular derecho
(sin justificar) y la posición del número de página.

### Fuentes de datos

| Fuente | Registros | Para qué |
|---|---|---|
| API de speedrun.com — Any% | 6.916 runs (6.752 NTSC, 164 PAL) | El corpus completo de intentos humanos |
| API de speedrun.com — 8-4 IL | 203 runs | La calibración del modelo (4 marcas perfectas) |
| Wikipedia (inglés) | 46 récords | La progresión histórica del récord mundial |

---

## Cómo reproducir

Solo requiere **Python 3** (biblioteca estándar, sin dependencias externas) y
`curl`. La descarga desde speedrun.com se hace con `curl` porque la API
rechaza las peticiones de `urllib`.

```bash
# 1. Extracción de datos (requiere red; la primera tarda 10-15 min)
python3 scripts/extraer_runs.py           # corpus Any% completo
python3 scripts/extraer_wr_wikipedia.py   # progresión del récord mundial
python3 scripts/extraer_seccion_84.py     # 203 runs del 8-4 IL

# 2. Análisis descriptivo
python3 scripts/analizar.py               # estadística y series temporales

# 3. El sistema probabilístico
python3 scripts/distribucion_T.py         # infiere la distribución del grind T
python3 scripts/sistema_corregido.py      # SISTEMA FINAL: forma cerrada + validación
python3 scripts/sensibilidad.py           # robustez e intervalo de Wilson
python3 scripts/limite_biologico.py       # prueba de estacionariedad (el techo)
python3 scripts/simulacion_montecarlo.py  # validación Monte Carlo de la mecánica

# 4. Figuras
python3 scripts/figuras.py                # figuras vectoriales (SVG)
python3 scripts/figuras_png.py            # versión PNG para el documento
```

Las figuras se generan como SVG y se rasterizan a PNG con `figuras_png.py`
(requiere `rsvg-convert` de `librsvg`, o ImageMagick). El documento incrusta
los PNG porque Markdown y Word los muestran sin depender de rutas externas.

`figuras.py` lee sus datos de los resultados ya procesados
(`sistema_corregido.json`, `distribucion_T.json`, `resumen_estadistico.json`),
nunca de valores escritos a mano, de modo que una figura no pueda contradecir
al texto.

Si solo quieres **verificar las cifras sin volver a descargar**, omite el paso 1:
los datos ya descargados están en `datos/`.

### Del crudo al resultado

```
extraer_runs.py ────────► runs_any_pcts_ntsc.csv ──► analizar.py ──► resumen_estadistico.json
extraer_wr_wikipedia.py ► wr_progresion_any.csv
extraer_seccion_84.py ──► il_84.csv ──┐
                                       ├──► distribucion_T.py ──► distribucion_T.json ──┐
                                       │                                                 │
                                       └─────────────────────────────────────────────────┴──► sistema_corregido.py
                                                                                              │
                                                        sensibilidad.py ──────────────────────┤
                                                        limite_biologico.py ──────────────────┤
                                                                                              ▼
                                                                                  sistema_corregido.json
                                                                                  (resultado central)
```

---

## El sistema probabilístico, en breve

La pregunta es si un humano puede igualar el óptimo teórico de **4:54.265**
(el mejor tiempo alcanzable sin pulsar izquierda y derecha a la vez).

El hallazgo central es estructural: en **siete** de los ocho niveles del
recorrido, una regla de la consola (*frame rule*, múltiplos de 21 frames)
absorbe el error humano —perder hasta 20 frames no cuesta tiempo—. En el octavo,
**8-4**, no hay tal absorción: cada frame cuenta.

La calibración parte de un dato medido: de 203 corredores que registraron una
marca en el *leaderboard* de 8-4, **4 lograron la ejecución perfecta** (1,97 %).
Ese *leaderboard* es un tablero de mejores marcas personales, no un registro de
intentos, así que ese 1,97 % mide la probabilidad de lograr un PB perfecto **en
toda una campaña**. Convertirlo a probabilidad **por intento** requiere un
modelo de renovación:

```
p84 = 1 − (1 − P(PB))^(1/T)
```

donde `T` es el número de intentos que un corredor dedica a su marca, inferido
de las duraciones declaradas en los comentarios del *leaderboard*.

El resultado se obtiene por **forma cerrada** (no por simulación); el Monte
Carlo se usa solo para validar que la mecánica del modelo es correcta.

---

## Cifras centrales (al 19 de octubre de 2026)

| Magnitud | Valor |
|---|---|
| Récord humano | 4:54.332 (Niftski, 14 ago 2026) |
| Óptimo teórico | 4:54.265 |
| Brecha | 4 frames / 0,067 s |
| P(PB perfecto de 8-4) | 4/203 = 1,97 % (IC 95 %: 0,77–4,96 %) |
| Grind `T` (mediana del régimen largo) | 6.075 intentos |
| P(8-4 perfecto por intento) | 3,28 × 10⁻⁶ |
| Intentos para el 50 % | ~219.000 |
| Rango robusto | ~3.250 – ~584.000 intentos |
| P(al menos uno lo logra), 5 corredores / 5 años | ~92 % |

Todas las cifras se reportan como **rangos**, nunca como valores únicos, porque
descansan en solo 4 éxitos perfectos y en 8 declaraciones de duración.

---

## Cómo citar

```
Pinto Rondon, J. S. (2026). El límite humano: ¿Puede el hombre alcanzar la
perfección de la máquina? Estudio de caso de la categoría Any% de
Super Mario Bros. (NES, 1985). https://github.com/Josesepin3/limite-humano
```

---

## Licencia

- El **código** (`scripts/`) está bajo licencia MIT.
- Los **datos** (`datos/`) y el **documento** (`documento/`) están bajo
  licencia Creative Commons Atribución 4.0 (CC BY 4.0).

Ver [`LICENSE`](LICENSE) para el detalle.

---

## Notas de método

- **Bifurcación de `T`.** La distribución del grind tiene dos regímenes: los
  corredores que ya conocían 8-4 dedican entre 2 y 90 intentos; los que lo
  aprendieron, entre 5.400 y 16.200. El escenario central usa la mediana del
  segundo, porque la mediana global cae entre ambos y no representa a ninguno.
- **Fecha del récord.** La API registra el run `z142re9z` el 14 de agosto de
  2026; Wikipedia lo fecha el 13, por conversión de zona horaria. Se usa la
  fecha de la fuente primaria.
- **Techo biológico.** La tasa de ejecuciones perfectas no mejora entre las
  dos mitades cronológicas del *leaderboard* (2 perfectos en cada una, con
  error medio casi idéntico). Eso respalda la lectura de que la precisión en
  8-4 es estacionaria y no se gana con entrenamiento acumulado.
