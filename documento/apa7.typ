// ============================================================================
//  PLANTILLA APA 7.ª EDICIÓN PARA TYPST
//  Archivo único y autocontenido: librería + contrato de uso.
//
//  ESTE ARCHIVO NO ES UN DOCUMENTO. No tiene contenido después de la librería.
//  Para usarlo hay que escribir el documento DEBAJO de la última línea, o
//  importarlo en otro archivo. Ver «CONTRATO DE USO» más abajo.
//
//  Verificado contra las fuentes oficiales de APA
//  (apastyle.apa.org — Publication Manual of the APA, 7th ed.).
//  Compilado y medido con Typst 0.15.1.
//
//  Fuentes de verdad y copias:
//    · Este archivo: ~/Documentos/apa7-typst/apa7.typ
//    · ~/Plantillas/apa7.typ → symlink a este archivo. Desde el escritorio,
//      click derecho ▸ Nuevo documento ▸ apa7.typ copia el contenido (no el
//      enlace), así que el documento que armás queda independiente.
//    · compilar.sh compila lo que le pases: `./compilar.sh miarchivo.typ`
//
//  ┌──────────────────────────────────────────────────────────────────────────┐
//  │ Si modificás este archivo, NO edites la copia de ~/Plantillas: es un    │
//  │ enlace simbólico y los cambios se pierden al escribir sobre él.        │
//  └──────────────────────────────────────────────────────────────────────────┘
// ============================================================================
//
// ─────────────────────────────────────────────────────────────────────────────
//  CONTRATO DE USO
// ─────────────────────────────────────────────────────────────────────────────
//
//  INSTRUCCIONES PARA AGENTES DE IA — leé esto antes de escribir una línea.
//  Seguí el orden de las secciones 3 y 4 exactamente. No inventes funciones,
//  no uses marcado de markdown, no apliques estilos a mano.
//
//  1. QUÉ HACE ESTO
//     `apa()` aplica TODAS las reglas de formato de APA 7 de una vez: papel,
//     márgenes, fuente, doble espacio, sangría, alineación, número de página,
//     niveles de título y espaciado. Si escribís tu propio `set text`, `set par`
//     o `set page`, lo estás pisando. No lo hagas: escribí contenido limpio y
//     dejá que la plantilla formatee.
//
//  2. CÓMO SE USA — hay dos modos, elegí uno
//
//     MODO A · Como plantilla (este archivo es el documento)
//         Escribí el documento al final de este archivo, a partir de la línea
//         `// ─── ACÁ EMPIEZA TU DOCUMENTO ───`. Tu documento tiene que empezar
//         sí o sí por la línea `#show: apa.with(...)`; sin ella no se aplica
//         ningún formato. Las funciones ya están definidas más arriba, no
//         hace falta importarlas.
//
//     MODO B · Como librería (tu documento está en otro archivo)
//         #import "apa7.typ": *
//         #show: apa.with(titulo-pdf: "Título", autor-pdf: "Nombre Apellido")
//         … tu documento acá …
//
//  3. ORDEN DEL DOCUMENTO (§ 1.16)
//     Cada bloque arranca en página nueva. Las funciones ya insertan el salto
//     de página: NO agregues `pagebreak()` a mano.
//
//         #portada(…)            → 1. portada            (página 1)
//         #resumen(…)            → 2. resumen            (página 2)
//         #palabras-clave(…)     → 3. palabras clave     (misma pág. 2)
//         #contenidos()          → 4. índice             (OPCIONAL, sección 5)
//         #lista-ilustraciones() → 5. lista de ilustra. (OPCIONAL, debajo de contenidos)
//         #titulo-general(…)     → 6. texto              (página nueva)
//         … cuerpo con títulos, citas, tablas y figuras …
//         #referencias((…))      → 7. referencias
//         #apendice(…)           → 8. apéndices
//
//  4. ESQUELETO MÍNIMO QUE RESPETA TODO LO ANTERIOR
//
//         #show: apa.with(
//           titulo-pdf: "Efecto de la cobertura sobre la homotermia del suelo",
//           autor-pdf: "María Gómez y Juan Pérez",
//         )
//
//         #portada(
//           "Efecto de la cobertura sobre la homotermia del suelo",
//           autores: ("María Gómez", "Juan Pérez"),
//           afiliacion: "Departamento de Biología, Universidad Nacional",
//           curso: "BIO 204: Ecología",
//           docente: "Dra. Ana Ruiz",
//           fecha: "5 de octubre de 2026",
//         )
//
//         #resumen([
//           Un único párrafo de no más de 250 palabras, sin sangría. Va entre
//           corchetes porque es contenido markup, no texto entre comillas.
//         ])
//
//         #palabras-clave("cubierta", "microclima", "bosque de montaña")
//
//         #contenidos()
//
//         #lista-ilustraciones()
//
//         La línea de arriba es lo que pediste: índice automático ya maquetado.
//         Mientras esté, la portada y el índice se regeneran solos y vos solo
//         tocás los datos. Si tu institución no lo pide, o preferís armarlo a
//         mano, borrá esta llamada y reemplazala por tu lista (sección 5).
//
//         #titulo-general("Efecto de la cobertura sobre la homotermia del suelo")
//
//         Primer párrafo del trabajo. Fijate que NO dice «Introducción»: APA
//         lo prohíbe, el comienzo del texto ya es la introducción (§ 1.11).
//
//         = Método
//
//         Párrafo normal. La sangría y el doble espacio los pone la plantilla.
//
//         = Resultados
//
//         #tabla("1", "Temperatura media por sitio", [ … ])
//         #figura("1", "Serie temporal", [ … ])
//         #cita-larga([ … ])
//
//         #referencias((
//           [García, M., & Ruiz, A. (2019). Título del artículo. #emph[Ecología Aplicada], #vol(14, 2), 210–219.],
//         ))
//
//         OJO con el «&»: en la LISTA DE REFERENCIAS va ampersand antes del
//         último autor, nunca «y». En el texto es al revés: parentética con «&»
//         y narrativa con «y». Ver «CÓMO CITAR», puntos 2 y 10.
//
//  5. LOS CINCO NIVELES DE TÍTULO (§ 2.27)
//
//         Nivel 1  =  centered, negrita        → `= Método`
//         Nivel 2  →  margen izq., negrita     → `== Instrumentos`
//         Nivel 3  →  margen izq., negrita cursiva → `=== Procedimiento`
//         Nivel 4  →  en línea, negrita       → `#nivel4("Título", [ … ])`
//         Nivel 5  →  en línea, negrita cursiva → `#nivel5("Título", [ … ])`
//
//     Los niveles 1 a 3 son elementos `heading` de Typst: escribilos con `=`,
//     `==`, `===`, uno por renglón, en minúsculas de `=` a mayor nivel.
//
//     Los niveles 4 y 5 NO son `heading`: van «en línea», o sea el título y el
//     párrafo comparten renglón y el título termina en punto. Por eso son
//     funciones y el texto del párrafo va DENTRO de la llamada, entre corchetes.
//
//     Reglas de estructura que importan:
//       · Cada sección principal arranca con nivel 1.
//       · No dejes una sola subsección dentro de una sección: dos o ninguna.
//       · No numeres ni letras los títulos: nunca `#set heading(numbering:)`.
//       · Títulos en title case. En español, title case con la primera palabra,
//         los nombres propios y los subtítulos con inicial mayúscula; el resto
//         en minúscula.
//
//     LIMITACIÓN CONOCIDA: los niveles 4 y 5 no aparecen en el índice
//     (`#outline()`) de Typst, porque son funciones y no elementos `heading`.
//     APA no pide índice en los trabajos de carrera, así que no es problema en
//     la práctica.
//
//  6. REGLAS QUE DEBES RESPETAR AL ESCRIBIR
//       · Nada de viñetas ni listas con viñeta en el cuerpo; si hace falta una
//         enumeración usá `1.` `2.` y la sangría la pone la plantilla.
//       · Nada de negritas para enfatizar texto corrido. La cursiva se usa
//         para títulos de fuente, palabras clave, estadísticos y símbolos.
//       · Las citas de 40 palabras o más van con `#cita-larga(…)`, sin comillas.
//       · Las citas de menos de 40 palabras van dentro del párrafo, entre comillas.
//       · Los rótulos de tabla y figura los pone `#tabla()` / `#figura()`. No
//         escribas «Tabla 1» a mano en el texto del párrafo.
//       · No uses `\n` ni espacios para maquetar. Los párrafos se separan con
//         una línea en blanco; el interlineado lo controla la plantilla.
//
//  7. CÓMO VERIFICAR QUE NO ROMPISTE NADA
//     Compilá y medí el PDF:
//
//         typst compile salida.typ
//         pdftotext -bbox salida.pdf - | head -40
//
//     Lo que tiene que dar (todo en puntos PDF, 1 in = 72 pt):
//       · Página 612 × 792 pt  =  21,59 × 27,94 cm
//       · x mínimo del texto = 72,0  (margen de 1 in)
//       · x máximo del texto ≤ 540,0 y VARIANTE entre renglones (no justificado)
//       · Primer renglón con sangría en x = 108,0 (= 72 + 36 = 0,5 in)
//       · Diferencia vertical entre renglones seguidos = 22,0 pt (= 2 × 11)
//       · Número de página en x = 534…540, en la franja de arriba
//
//     No des por buena una modificación sin correr esto.
//
// ─────────────────────────────────────────────────────────────────────────────
//  API — signatures exactas
// ─────────────────────────────────────────────────────────────────────────────
//
//  #show: apa.with(
//    fuente: "Arial",  // str o array de str (ver «FUENTE»)
//    tamano: 11pt,               // length
//    idioma: "es",               // str: reglas de separación silábica
//    comillas: "dobles",          // "dobles" → " " (§ 8.26) · "angulares" → « »
//    sangria: 1.27cm,            // 0,5 in
//    doble: true,                // doble espacio
//    justificar: false,          // APA exige false (§ 1.22)
//    titulo-pdf: none,           // str o none → metadato del PDF
//    autor-pdf: none,            // str o none → metadato del PDF
//  )
//
//  #portada(
//    titulo,                          // str obligatorio, en cursiva no: normal
//    autores: (),                     // str o tupla de str
//    afiliacion: none,                // str: «Departamento, Universidad»
//    curso: none,                     // str
//    docente: none,                   // str
//    fecha: none,                     // str, formato del país
//    lineas-arriba: 3,                // int: renglones en blanco antes del título
//  )
//
//  ─── LA PORTADA Y SUS ESPACIOS (§§ 2.3 a 2.6) ──────────────────────────────
//
//  La portada es el lugar donde más se cueven los errores de espaciado, porque
//  hay UNA sola excepción y es fácil pasarla por alto o inventarse otras:
//
//      «each element placed on a separate line, no extra lines added between
//       elements, EXCEPT after the paper title»
//      «place one double-spaced blank line between the paper title and the
//       author names»
//      «double-space the rest of the title page»
//
//  — APA, Student Title Page Guide, 7.ª ed.
//
//  Traducido a líneas, de arriba abajo:
//
//      línea 1-3   en blanco
//      TÍTULO      en negrita, centrado, en title case   (§ 2.4)
//      (blanco)    ← UN renglón vacío. Sólo aquí.        (§ 2.5)
//      AUTOR/AUTORES
//      afiliación
//      curso
//      docente
//      fecha
//
//  O sea: un solo renglón en blanco en toda la portada, y va justo después del
//  título. Todo lo demás va pegado, a 22,0 pt entre línea. Si le ponés un blanco
//  entre el autor y la afiliación, o entre el curso y el docente, ya no es APA.
//  Si le sacás el blanco al título, tampoco.
//
//  El título va de 3 a 4 renglones desde el borde superior, y en negrita. Nada
//  más en la portada va en negrita, cursiva, subrayado o con otro cuerpo de
//  letra: «not bold or italic, except for the paper title». Ojo con esto, que
//  es fácil de arruinar: si le ponés cursiva a la fecha o al nombre de la
//  materia, queda mal.
//
//  `lineas-arriba: 3` es ese offset. Subilo a 4 si tu institución pide la
//  variante «four lines down».
//
//  #titulo-general(titulo)                          → texto en página nueva
//  #resumen(cuerpo, etiqueta: "Resumen")            → «Resumen» o «Abstract»
//  #palabras-clave(..claves)                        → varargs de str
//  #contenidos(etiqueta: "Contenidos", profundidad: 3, sangria: 1.27cm)
//                                                  → índice automático, OPCIONAL
//  #lista-ilustraciones(etiqueta: "Lista de ilustraciones", profundidad: none)
//                                                  → figuras automáticas, abajo de contenidos
//  #nivel4(titulo, cuerpo, sangria: 1.27cm)
//  #nivel5(titulo, cuerpo, sangria: 1.27cm)
//  #cita-larga(cuerpo, sangria: 1.27cm)
//  #referencia(cuerpo, sangria: 1.27cm)             → una entrada, suelta
//  #referencias(entradas, etiqueta: "Referencias") → página de referencias
//  #tabla(numero, titulo, cuerpo, nota: none)
//  #figura(numero, titulo, imagen, nota: none)
//  #apendice(letra, titulo)
//  #vol(numero, edicion)                            → «14(2)» con 14 en cursiva
//  #sangria-parrafo(cuerpo) / #sin-sangria(cuerpo)
//  #nueva-pagina()
//
//  Argumentos de tipo `content` (los que van entre corchetes: `cuerpo`,
//  `titulo`, `nota`, `imagen`) admiten markup: `#emph[…]`, `#strong[…]`,
//  `#vol(…)`, `#sym.…`. Los que son `str` van entre comillas SIN corchetes.
//
// ─────────────────────────────────────────────────────────────────────────────
//  CÓMO SE IMPLEMENTÓ EL DOBLE ESPACIO — no lo toques sin leer esto
// ─────────────────────────────────────────────────────────────────────────────
//
//  En Typst, `par.leading` NO es la distancia entre bases: es el hueco entre el
//  borde inferior de una línea y el borde superior de la siguiente. Además
//  `par.spacing` no se le suma al `leading` entre párrafo y párrafo. Por eso
//  `leading: 2em` da casi el triple de espacio y `spacing: 0pt` deja el doble
//  espacio roto entre párrafos.
//
//  La plantilla arma una grilla de bases exacta:
//
//      top-edge 0,8em   │┐
//      leading    1em   ├─→ 2 em entre bases DENTRO de un párrafo
//      bottom-edge 0,2em ┘
//      spacing    1em   │→ 2 em también ENTRE párrafos y ENTRE bloques
//
//  Como `block(spacing: auto)` hereda el spacing de párrafo, los bloques (títulos,
//  tablas, figuras, notas) caen en la grilla sin tocar nada. Resultado: 22 pt
//  entre cualquier par de renglones consecutivos. Eso es lo que cumple «do not
//  add extra spacing before or after headings» (§ 1.20).
//
//  ─── ¿NO HAY UNA FORMA FÁCIL? NO. ESTO ES LO QUE HAY ────────────────────────
//
//  Typst no tiene `\doublespacing` ni `leading: "double"`: es un reclamo
//  abierto desde 2023 en el repo de Typst (issue 106, «Double line spacing»).
//  La receta de arriba es la oficial, la que dan los docs de `par` textualmente.
//  Y como `leading` NO es la distancia entre bases, los atajos que la gente
//  prueba dan números que no son 22.
//
//  Medido en este sistema, 11 pt, con `pdftotext -bbox` sobre renglones marcados
//  (objetivo: 22,0 pt = 2 x 11):
//
//      configuración                        dentro    entre    ¿22,0?
//      ──────────────────────────────────────────────────────────────────
//      sin tocar nada (por defecto)          14,7    14,7 / 20,8   no
//      par(leading: 2em)                     29,6    20,8 / 29,6   no  (+34 %)
//      par(leading: 1.3em)  «0,65em x 2»      21,9    20,8 / 21,9   no
//      par(leading: 1em)                     18,6    18,6 / 20,8   no
//      par(leading: 1em, spacing: 1em)       18,6    18,6          no
//      bordes 0,8/-0,2 + leading 1em         22,0    22,0 / 24,2   no
//      bordes 0,8/-0,2 + 1em + spacing 1em   22,0    22,0          SI  ← esta
//
//  Leer la tabla:
//    · `leading: 2em` da 29,6 pt, un 34 % más de doble espacio. Es el error
//      clásico: se lee «leading» como «distancia entre bases» y no lo es.
//    · `leading: 1.3em` (la receta que circula en foros, 0,65em x 2) da 21,9 pt
//      dentro del párrafo pero 20,8 entre párrafos: el doble espacio se rompe
//      justo en la unión, que es donde se nota.
//    · Falta el `spacing` y la unión entre párrafos queda a 24,2 pt mientras que
//      dentro del párrafo hay 22,0: dos ritmos distintos en el mismo documento.
//    · Sólo la última fila da 22,0 en los dos casos.
//
//  O sea: los tres valores (`top-edge`, `leading`, `spacing`) hacen falta, y
//  hacen falta los tres. No sobra ninguno.
//
//  Corollary: NUNCA cambies `leading`, `spacing`, `top-edge` o `bottom-edge` por
//  tu cuenta. Para cambiar el cuerpo de letra usá `tamano`, y la grilla se
//  recalcula sola.
//
//  Detalle de implementación: dentro del párrafo el ritmo lo dan `top-edge` +
//  `leading` + `bottom-edge`; entre párrafos y entre bloques lo dan `spacing` +
//  los bordes, y el valor que gana es el MÁXIMO de los dos lados. Por eso en la
//  regla de `heading` no se pone `spacing: 0pt` (ver trampa 8).
//
//  `first-line-indent` va como diccionario `(amount: sangria, all: true)` a
//  propósito: por omisión Typst no indenta el primer párrafo del documento ni
//  los que siguen a un elemento de bloque, y APA manda indentar *todos* los
//  párrafos (§ 1.23). Si lo pasás a length simple, se pierde la sangría en
//  justo los párrafos que APA quiere sangrados.
//
// ─────────────────────────────────────────────────────────────────────────────
//  MEDIDAS VERIFICADAS — extraídas del PDF generado, no estimadas
// ─────────────────────────────────────────────────────────────────────────────
//
//    Regla                        Medida real        Fuente
//    ─────────────────────────────────────────────────────────────────────────
//    Papel Carta                  612×792 pt        § 2.22
//                                 21,59×27,94 cm
//    Márgenes                     72 pt = 2,54 cm   § 1.21
//    Sangría de primera línea     36 pt = 1,27 cm   § 1.23
//    Doble espacio                22 pt = 2 × 11pt  § 1.20
//    Alineado                     borde derecho     § 1.22
//                                 irregular, no
//                                 justificado
//    Número de página             x 534…540, arriba  § 1.17
//    Título de la portada         4.ª línea          § 1.6
//    Niveles 1/2/3                ver sección 5     § 2.27
//    Rótulo de tabla              negrita + cursiva  § 7.10, § 7.24
//
// ─────────────────────────────────────────────────────────────────────────────
//  FUENTE
// ─────────────────────────────────────────────────────────────────────────────
//
//  APA acepta 11 pt Arial (§ 1.18). Arial es propietaria de Monotype, así que
//  hay que instalarla a mano. La ruta alternativa es Liberation Sans: libre y
//  métricamente idéntica a Arial.
//
//  ┌── LA COA ESTÁ EN QUE LA FAMILIA ESTÉ COMPLETA ──────────────────────────┐
//  │                                                                       │
//  │  Typst NO sintetiza negrita ni cursiva. La documentación lo dice:     │
//  │                                                                       │
//  │    weight: «When the desired weight is not available, Typst selects    │
//  │             the font from the family that is closest in weight.»      │
//  │    style:  «When neither an italic nor an oblique style is available, │
//  │             Typst selects the normal style.»                          │
//  │                                                                       │
//  │  O sea: si a la familia le falta el estilo, el emphasis no se nota.   │
//  │  Ni un aviso, ni una cursiva inclinada, ni una negrita engrosada:     │
//  │  el texto sale idéntico al normal. En un trabajo de APA eso           │
//  │  significa títulos que no parecen títulos.                            │
//  │                                                                       │
//  │  Hacen falta los CUATRO archivos de la familia. Con los nombres de    │
//  │  Microsoft, que es como vienen en los paquetes de corefonts:          │
//  │                                                                       │
//  │      ARIAL.TTF      peso 400  Regular     — el cuerpo del texto       │
//  │      ARIALBD.TTF    peso 700  Bold        — niveles 1 y 2, «Tabla 1», │
//  │                                          «Figura 1», «Nota.», «Apéndice»│
//  │      ARIALI.TTF     peso 400  Italic      — títulos de fuente,       │
//  │                                          «Palabras clave:», nivel 5   │
//  │      ARIALBI.TTF    peso 700  Bold Italic — niveles 3 y 5             │
//  │                                                                       │
//  │  Para verificar qué estilos tenés:                                    │
//  │                                                                       │
//  │      fc-list ":family=Arial:style=Bold" family                        │
//  │                                                                       │
//  │  Si no devuelve nada, ese estilo falta. `compilar.sh` avisa solo,      │
//  │  con un chequeo por familia antes de compilar y otro sobre el PDF      │
//  │  ya generado (si el PDF lleva una sola fuente, es que no se usó        │
//  │  negrita ni cursiva).                                                 │
//  └───────────────────────────────────────────────────────────────────────┘
//
//  ─── POR QUÉ NO SIRVE UNA CADENA DE RESPALDO ───────────────────────────────
//
//  tempting: `fuente: ("Arial", "Liberation Sans")` para que la negrita venga
//  de la segunda. NO funciona, y está medido: Typst elige la primera familia
//  que tenga los glifos y no reintenta por estilo. El PDF sigue saliendo con
//  una sola fuente embebida y la negrita sigue sin verse.
//
//  La lista de `font:` es para cobertura de glifos (por ejemplo, «Noto Sans
//  Arabic» para texto árabe), no para estilos.
//
//  ─── COMPATIBILIDAD MÉTRICA, COMPROBADA ────────────────────────────────────
//
//  Arial y Liberation Sans tienen exactamente los mismos anchos de glifo, así
//  que cambiar de una a la otra no mueve ni un renglón. Medido sobre el mismo
//  documento de prueba:
//
//      42 renglones en los dos casos
//      mismos cortes de línea, mismas páginas, mismas posiciones al milésimo
//
//  El valor por defecto de `fuente` es «Arial» y los cuatro estilos están
//  instalados en este sistema. Liberation Sans queda como alternativa: los otros
//  cuatro estilos también están instalados, y como las dos familias dan el mismo
//  maquetado al milésimo, cambiar de una a otra no mueve ni un renglón ni una
//  página. Si un día desaparece Arial, basta con cambiar ese argumento.
//
//  AVISO: ser metricamente compatibles no significa que la negrita de una sea
//  igual de «negrita» que la de la otra. La comparación de anchos NO sirve para
//  detectar que falte el estilo bold, porque justamente son iguales; y para la
//  cursiva nunca sirve, porque inclinar no cambia el avance. Por eso el
//  chequeo se hace con `fc-list` y no desde Typst.
//
//  ─── LA CURSIVA ROBADA POR UN ARCHIVO AJENO ────────────────────────────────
//
//  Con los cuatro archivos correctos Todo funciona. Pero si volcás una carpeta
//  entera de fuentes de Arial en `~/.local/share/fonts/` sin revisarla, hay un
//  archivo que rompe la cursiva sin decir nada: `ARIALBLACKITALIC.TTF`.
//
//  El problema es que ese archivo se llama Arial Black pero declara en su tabla
//  OS/2 un peso de 400, y Typst agrupa por peso: entra en la familia «Arial» como
//  una cursiva más y le gana a la cursiva verdadera. El PDF se sigue viendo
//  bien y compila sin avisos, sólo que donde debería ir cursiva va Arial Black
//  Italic, que es un peso display pesado y se nota muchísimo.
//
//  Lo que se ve, con `pdffonts` sobre el PDF generado:
//
//      correcto                con ARIALBLACKITALIC.TTF de más
//      ─────────────────────   ──────────────────────────────────────
//      ArialMT                 ArialMT
//      Arial-BoldMT            Arial-BoldMT
//      Arial-ItalicMT          Arial-BlackItalic      <-- ¡robada!
//      Arial-BoldItalicMT      Arial-BoldItalicMT
//
// Chequeo de una línea, que no lo detecta ni `compilar.sh` porque la fuente está
//  instalada y el PDF sí lleva cuatro fuentes:
//
//      pdffonts salida.pdf | tail -n +3 | awk '{print $1}'
//
//  Tiene que aparecer `Arial-ItalicMT`. Si aparece cualquier otra cosa con
//  «Italic» en el nombre, hay un archivo de más tapando el estilo.
//
//  Lo mismo vale para cualquier archivo suelto de una familia vecina: Arial
//  Narrow, Arial Light y Arial Medium declaran familia «Arial» y se cuelan en el
//  grupo. Con esos no hay problema (pesos 300, 400 y 500, que no compiten con
//  400 cursiva ni con 700 negrita), pero si alguna vez un renglón sale con una
//  tipografía rara, el primer sospechoso es un archivo de más.
//
//  Duplicados exactos del mismo archivo (`1ARIALI.TTF`, `ARIALI 1.TTF`) no
//  molestan: Typst los deduplica. Son basura, pero inofensiva.
//
// ─────────────────────────────────────────────────────────────────────────────
//  TRAMPAS DE TYPST — ninguna de estas compila si la escribís mal
// ─────────────────────────────────────────────────────────────────────────────
//
//  1. En markup, `#emph[14](2)` NO compila: no se puede encadenar un segundo
//     grupo de argumentos sobre un bloque de contenido. Para el «volumen(número)»
//     de una referencia usá el helper `#vol(14, 2)`.
//
//  2. Un `(` pegado a una `,` se interpreta como comilla tipográfica («smart
//     quote»), no como paréntesis. Para paréntesis literales en markup hay que
//     escribir `#"("` o usar `sym.lparen` / `sym.rparen`.
//
//  3. `par` NO tiene parámetro `left-indent`. Para sangrar un bloque completo
//     usá `pad` (como hace `cita-larga`); para sangría francesa usá
//     `par(hanging-indent: …)`.
//
//  4. `(x)` es una expresión entre paréntesis: devuelve el valor, no una
//     colección. `([a]),` colapsa a contenido y no a tupla de un elemento. Por
//     eso `referencias()` normaliza la entrada y acepta las dos formas.
//
//  5. Una función de plantilla tiene que llevar el contenido del documento como
//     ÚLTIMO parámetro posicional (`body`). Si no, `#show: apa.with(…)` le pasa
//     el documento como primer argumento y falla con «unexpected argument».
//
//  6. `document.author` y `document.title` NO aceptan `auto`: compilan con
//     «expected content or none, found auto». Sólo `content` o `none`. Como
//     `apa()` se suele llamar sin argumentos, el valor por defecto es `none` /
//     `""` y el PDF queda sin metadatos; se completan con `titulo-pdf` y
//     `autor-pdf`.
//
//  7. En Typst, dos renglones separados por `\` dentro del MISMO párrafo respetan
//     el `leading`; dos bloques independientes no. Paratitles centrados de
//     varias líneas hay que unirlos en un solo párrafo — de eso se encarga
//     `unir()`.
//
//  8. El espacio entre dos bloques contiguos es el MÁXIMO de sus `spacing`, no
//     la suma. Poner `spacing: 0pt` dentro de un `show heading` deja dos
//     títulos seguidos pegados (11 pt en vez de 22) mientras que título→párrafo
//     sigue en 22 pt, así que el error queda disimulado. Para el «sin espacio
//     extra» de § 1.20 hay que HEREDAR el spacing global, nunca ponerlo en 0.
//
// ─────────────────────────────────────────────────────────────────────────────
//  CÓMO CITAR — citas en el texto y lista de referencias
//  (APA 7.ª ed.: cap. 8 = citas en el texto, cap. 10 = lista de referencias)
// ─────────────────────────────────────────────────────────────────────────────
//
//  ─── 0. QUÉ HACE LA PLANTILLA Y QUÉ NO ──────────────────────────────────────
//
//  Ninguna de estas reglas es automática. La plantilla NO puede saber si lo que
//  escribiste es una cita textual o una paráfrasis: eso lo decidís vos, contando
//  las palabras y viendo si cambiaste el texto original. Lo que sí hace la
//  plantilla:
//
//    #cita-larga(…)   sangría completa de 0,5 in, doble espacio,
//                     SIN comillas y SIN renglón en blanco extra   (§ 8.27)
//    #referencia(…)   sangría francesa de 0,5 in, una entrada suelta (§ 9.43)
//    "…"              comillas dobles, solas                          (§ 8.26)
//    #vol(14, 2)      volumen en cursiva, número de issue en normal   (§ 10.1)
//
//  ─── 1. LOS DOS FORMATOS DE CITA EN EL TEXTO ─────────────────────────────────
//
//  Hay exactamente dos. Se distinguen por DÓNDE va el autor.
//
//      PARENTÉTICA    autor y fecha van dentro del paréntesis. El texto es tuyo.
//                     La homotermia del suelo disminuyó (García y Pérez, 2019).
//
//      NARRATIVA      el autor ES parte de la oración y sólo la fecha va entre
//                     paréntesis, pegada al apellido.
//                     García y Pérez (2019) midieron la homotermia del suelo.
//
//  · La parentética puede ir en medio de la oración o al final.         (§ 8.11)
//  · Si dentro del paréntesis va también texto tuyo, separalo con PUNTO Y
//    COMA, nunca con otro paréntesis: «(ver García y Pérez, 2019, p. 44)».
//  · Si la cita cierra la oración, la puntuación va FUERA del paréntesis:
//    «… disminuía (García y Pérez, 2019, p. 44).»                    (§ 8.25)
//
//  El conector que pedís —«Según García y Pérez (2019) […]»— es la forma
//  NARRATIVA con un verbo de reporte adelante. Aclaración honesta: APA no
//  obliga a que haya verbo; lo que pide es que el autor sea parte de la
//  oración. Si tu disciplina lo exige, usalo siempre: es lo más seguro.
//
//  ─── 2. CUÁNTOS AUTORES PONER ────────────────────────────────────────────────
//
//  · En la cita PARENTÉTICA y en la LISTA DE REFERENCIAS va «&» antes del
//    último autor. En la cita NARRATIVA va escrito entero («and», o «y» si el
//    texto es en español).
//  · «et al.» con punto: «(Martín et al., 2020)».
//  · Los sufijos no van en la cita del texto: nunca «Jr.» ni «III». (§ 8.19)
//  · Cada cita del texto tiene que corresponder a UNA sola entrada de la lista.
//    Si dos entradas arrancan igual, distinguilas en el texto con las
//    iniciales: «(García, M. A., 2019)» frente a «(García, M., 2019)».
//
//  ─── 3. CITA TEXTUAL CORTA — 39 palabras o menos ─────────────────────────────
//
//  «For quotations of fewer than 40 words, add quotation marks around the words
//  and incorporate the quote into your own text—there is no additional
//  formatting needed.» — APA, Quotations
//
//  O sea: va entre comillas dobles y PEGADA a tu propia frase. Sin comillas no
//  es una cita textual, es un texto tuyo.
//
//      Según García y Pérez (2019), la velocidad «cayó un 12 %» (p. 44).
//
//  · SIEMPRE cita completa (autor + año) en la MISMA oración, con su número de
//    página o de párrafo.
//  · El número va después de la comilla de cierre o al final de la oración,
//    nunca adentro de las comillas.
//  · No agregues puntos suspensivos ni al principio ni al final, salvo que el
//    original los tenga.
//
//  ─── 4. CITA TEXTUAL LARGA — 40 palabras o más ──────────────────────────────
//
//  «Do not use quotation marks to enclose a block quotation. Start a block
//  quotation on a new line and indent the whole block 0.5 in. from the left
//  margin. Double-space the entire block quotation. Do not add extra space
//  before or after it.» — APA, Block quotations
//
//  Las cuatro, una por línea, y la plantilla te da dos:
//
//      SIN comillas        ← ni una, ni una
//      sangría de 0,5 in   ← la pone #cita-larga
//      doble espacio       ← ya está
//      sin blanco extra    ← ni antes ni después
//
//      #cita-larga([
//        Texto de la cita, con el punto final adentro y la referencia pegada al
//        punto. Sin punto después del paréntesis.
//        (García y Pérez, 2019, p. 45)
//      ])
//
//  · El punto de la cita va ANTES del paréntesis de referencia.
//  · NO pongas punto después del paréntesis de cierre. Es el error más común.
//  · Si la cita ocupa más de un párrafo, cada uno va 0,5 in más adentro que el
//    anterior: `#cita-larga([ … ], sangria: 2.54cm)`.
//
//  ─── OJO CON EL CORTE DE LAS 40 PALABRAS ────────────────────────────────────
//
//  Tu regla decía «más de 40 palabras». APA corta en 40 EXACTAS: a las 39 va
//  cita corta y a las 40 ya va cita larga. O sea que tu regla deja sin cubrir
//  el caso de exactamente 40 palabras, que APA manda como larga.
//
//  ─── 5. PARAFRASEAR ─────────────────────────────────────────────────────────
//
//  Una paráfrasis NO lleva comillas (es tu redacción) y NO necesita número de
//  página: «Although it is not required to provide a page or paragraph number in
//  the citation, you may include one … when it would help interested readers
//  locate the relevant passage» — APA, Paraphrases.
//
//      La cobertura reduce la homotermia del suelo (García y Pérez, 2019).
//      García y Pérez (2019) observaron que la cobertura reduce la homotermia.
//
//  · Si la paráfrasis sigue varias oraciones, citá en la primera mención y
//    después no repitas, mientras quede claro que seguís con el mismo trabajo.
//  · Si pasa a otro párrafo, volvé a citar.
//  · Si mezclás fuentes o saltás de una a otra, repetí la cita.
//  · Si leíste una paráfrasis de la fuente primaria dentro de otro trabajo,
//    citá la fuente primaria directamente si podés; si no, citá como fuente
//    secundaria.                                                (§ 8.26, § 9.7)
//
//  ─── 6. NÚMEROS DE PÁGINA Y DE UBICACIÓN ────────────────────────────────────
//
//    una página        p. 25        →  (García y Pérez, 2019, p. 25)
//    un rango           pp. 34–36    →  rayita, NO guion: «pp. 34–36»
//    páginas sueltas    pp. 67, 72   →  coma, sin «y»
//
//  · En la LISTA DE REFERENCIAS nunca va «p.» ni «pp.»: ahí las páginas van
//    sueltas, con rayita si son un rango.
//  · Si la fuente NO tiene páginas (artículo web, mensaje, publicación en línea),
//    poné otra cosa: número de párrafo («para. 5»), nombre del apartado entre
//    comillas («"Conclusiones"»), o número de tabla o figura.        (§ 8.28)
//
//  ─── 7. LAS COMILLAS — el bug que ya está corregido ─────────────────────────
//
//  APA exige comillas DOBLES: “así”. Typst saca las comillas del `lang`, y con
//  `idioma: "es"` la tecla " daba «así», que es la convención del español y NO
//  la de APA. Medido sobre el mismo documento:
//
//      lang: "es"   →   «asi»    angulares, incorrecto en APA
//      lang: "en"   →   “asi”    dobles, correcto
//
//  Por eso `apa()` lleva el parámetro `comillas`, y por defecto va en "dobles":
//  escribís  "texto citado"  y sale “texto citado” sin hacer nada más. Si tu
//  institución pide comillas angulares: `apa.with(comillas: "angulares")`.
//
//  ─── 8. CITAR VARIAS OBRAS ──────────────────────────────────────────────────
//
//  · En la cita PARENTÉTICA, orden alfabético y separadas con PUNTO Y COMA:
//        (García, 2019; Salas & D’Agostino, 2020)
//  · Mismo autor y varios años: el apellido UNA sola vez y después sólo el año,
//    en orden cronológico, sin fecha primero y «in press» al final:
//        (García, n.d., 2019, 2022)
//  · Para destacar las más relevantes, esas van PRIMERO, después «véase también»
//    y el resto alfabético: (García, 2019; véase también Salas, 2020).  (§ 8.12)
//  · En la cita NARRATIVA el orden es libre:
//        García (2019), Salas y D’Agostino (2020) y Martín et al. (2021) midieron…
//
//  ─── 9. REPETIR, Y LOS CASOS RAROS ──────────────────────────────────────────
//
//  · APA NO usa «ibid.». Cada cita se escribe completa, siempre.
//  · En la parentética: autor y año siempre.
//  · En la narrativa: el año va sólo la primera vez del párrafo; en el párrafo
//    siguiente vuelve a ir.
//  · PERO si citás varias obras del mismo autor, el año va en TODAS, para que no
//    quede ambigua cuál es cuál.
//  · Sin fecha: «n.d.». Aceptado pero todavía sin publicar: «in press».
//  · Sin autor: en el texto va el título y el año, con abreviaturas del título
//    igual que con un autor corporativo: primera vez «(Guía de redacción [GdR],
//    s. f.)», después «(GdR, s. f.)».                            (§ 9.12)
//  · Autor corporativo con sigla: la sigla se define UNA sola vez en todo el
//    texto: «(Instituto Nacional de Salud [INS], 2020)», después «(INS, 2020)».
//  · Entrevista, comunicación personal o carta: NO van a la lista de referencias
//    y en el texto sólo se describen.                                (§ 8.16)
//
//  ─── 10. LA LISTA DE REFERENCIAS ────────────────────────────────────────────
//
//  Página propia: `#referencias(…)`. Reglas de formato:
//
//    · Cada entrada es un párrafo, justificado a la izquierda.
//    · Doble espacio DENTRO de cada entrada y ENTRE entradas.
//    · Sin renglón en blanco entre entradas.  ← el error típico
//    · Sangría francesa de 0,5 in.              ← la pone #referencia
//    · Orden alfabético por la primera palabra de la entrada, que suele ser el
//      apellido del primer autor. Sin autor, por el título.        (§ 9.44)
//    · «El», «La», «Un» y equivalentes NO cuentan para alfabetizar: «El campo…»
//      se ordena por «campo».
//    · Sin numerar las entradas.                                    (§ 9.44)
//
//  Toda entrada tiene los mismos cuatro elementos, en este orden, y cada uno
//  termina en punto:
//
//      autor · fecha · título · fuente
//
//      García, M., & Ruiz, A. (2019). Título del artículo.
//      #emph[Ecología Aplicada], #vol(14, 2), 210–219.
//
//    · Autor    Apellido, Iniciales. — nombre INVERTIDO; entre autores, «&» en el
//               último; con autor corporativo, punto al final del elemento.
//    · Fecha    (2019). En la cita del texto va sólo el año, aunque acá pongas
//               la fecha completa.
//    · Título   con cursiva si la obra existe sola (libro, informe, página web);
//               sin cursiva si es parte de algo más (artículo de revista,
//               capítulo de libro, entrada de diccionario).        (§ 10.2)
//    · Fuente   en cursiva el nombre de la revista y el VOLUMEN; en normal la
//               coma, el número de issue entre paréntesis pegado al volumen, y
//               las páginas. Nunca una coma entre volumen e issue.    (§ 10.1)
//
//  · DOI y URL van SIN punto final, para no romper el enlace.             (§ 10.4)
//  · La cursiva se pone sobre la palabra, no sobre el punto que la sigue.
//
//  ─── 11. ¿AUTOMÁTICA O A MANO? ───────────────────────────────────────────────
//
//  Typst trae un generador con estilo APA que ya resuelve el orden alfabético,
//  la cursiva del volumen, el DOI y el orden de las entradas:
//
//      #bibliography("fuentes.bib", style: "apa", title: none)
//
//  Conviven bien con la lista manual: usá `bibliography` para lo que tenés en el
//  .bib y `#referencias(…)` para las entradas que querés escribir a mano
//  (comunicaciones personales, legislación, fuentes sin metadatos). Lo único
//  que no podés hacer es GENERAR la misma obra con los dos.
//
//  ─── 12. FUENTES DE ESTA SECCIÓN ─────────────────────────────────────────────
//
//  Todas de APA Style, 7.ª ed. (apastyle.apa.org), capítulos 8 y 10:
//
//    · Quotations, y su subpágina de números de página
//      …/style-grammar-guidelines/citations/quotations
//      …/style-grammar-guidelines/citations/quotations/page-numbers
//    · Paraphrases
//      …/style-grammar-guidelines/citations/paraphrasing
//    · Parenthetical versus narrative in-text citations
//      …/style-grammar-guidelines/citations/basic-principles/parenthetical-versus-narrative
//    · Author–date citation system — la tabla del número de autores
//      …/style-grammar-guidelines/citations/basic-principles/author-date
//    · Citing multiple works
//      …/style-grammar-guidelines/citations/basic-principles/multiple-works
//    · Reference List Setup — sangría francesa, alfabeto, renglón en blanco
//      …/style-grammar-guidelines/paper-format/reference-list
//    · Basic Principles of Reference List Entries — los cuatro elementos
//      …/style-grammar-guidelines/references/basic-principles
//    · Creating an APA Style Reference List (PDF con los errores frecuentes)
//      apastyle.apa.org/instructional-aids/creating-reference-list.pdf
//
// ─────────────────────────────────────────────────────────────────────────────
//
//  ─── ACÁ EMPIEZA TU DOCUMENTO ───
//
//  (Si usás el MODO A, escribí tu documento a partir de acá, empezando por
//  `#show: apa.with(...)`. Si usás el MODO B, no escribas nada en este archivo.)
//
// ============================================================================


// ── Utilidades internas ─────────────────────────────────────────────────────

#let nueva-pagina() = pagebreak(weak: true)

// Junta varias líneas en un solo párrafo, separadas por saltos de línea.
// Necesario porque un salto de línea dentro de un párrafo respeta el
// `leading`, mientras que dos bloques independientes no.
#let unir(lineas) = (
  if type(lineas) == array { lineas } else { (lineas,) }
).join([#linebreak()])


// ── 1. Reglas globales ──────────────────────────────────────────────────────

#let apa(
  fuente: "Arial", // § 1.18. OJO: la familia tiene que estar COMPLETA (ver «FUENTE»)
  tamano: 11pt,
  idioma: "es",
  comillas: "dobles", // "dobles" → " " (§ 8.26) · "angulares" → « »
  sangria: 1.27cm, // 0,5 in
  doble: true, // doble espacio
  justificar: false, // alineado a la izquierda, margen derecho irregular
  titulo-pdf: none,
  autor-pdf: none,
  body, // el contenido del documento; `#show: apa.with(…)` lo inyecta acá
) = {
  // Geometría de la grilla de bases, en múltiplos de `tamano`.
  let alto = if doble { 2 * tamano } else { 1.2 * tamano }

  // Idioma real que se le pasa a `text`.
  //
  // En Typst el estilo de las comillas se SACA del `lang`, no de un parámetro
  // aparte. APA exige comillas dobles (" ") pero el español usa angulares (« »),
  // así que el `lang` que da comillas APA es el inglés, no `idioma`:
  //
  //     lang: "es"   →   «asi»     angulares, NO es APA
  //     lang: "en"   →   “asi”     dobles, sí es APA
  //
  // Perder el `lang` español no cuesta silabeo: medido en este sistema, Typst no
  // guiona palabras en español con ninguna combinación (ni `lang: "es"` con
  // `hyphenate: auto`, ni `lang: "en"`). Así que `idioma` se sigue honoring y
  // sólo decide el tema de las comillas. Ver «CÓMO CITAR», punto 7.
  let lang = if comillas == "angulares" { idioma } else { "en" }

  // Metadatos del PDF.
  //
  // `document.author` sólo acepta contenido o `none`, así que sin autor
  // explícito va cadena vacía. `document.title` es lo mismo: NO acepta `auto`
  // (compila con «expected content or none, found auto»), ni siquiera cuando
  // se llama a `apa()` sin argumentos, que es el uso más común. Sin título
  // explícito el PDF queda sin metadato de título, que es el comportamiento
  // por defecto de Typst.
  set document(
    title: if titulo-pdf == none { none } else { titulo-pdf },
    author: if autor-pdf == none { "" } else { autor-pdf },
  )

  // Página Carta 21,59 × 27,94 cm, márgenes de 2,54 cm (§ 1.21).
  set page(
    paper: "us-letter",
    margin: (top: 2.54cm, bottom: 2.54cm, left: 2.54cm, right: 2.54cm),
    // Número de página arriba a la derecha, incluida la portada (§ 1.17).
    // Se estila a mano porque queda declarado antes que `set text`.
    //
    // No se toca `header-ascent`: con su valor por defecto (30 % del margen
    // superior) Typst deja el número a ~0,56 in del borde superior, dentro de
    // la franja del encabezado. Fijarlo a un valor duro para perseguir 0,5 in
    // exactos no vale la pena: depende del cuerpo de letra, así que cualquier
    // número mágico se rompe en cuanto el usuario cambia `tamano`.
    header: context align(right)[
      #text(font: fuente, size: tamano, lang: lang)[#here().page()]
    ],
    footer: none,
  )

  set text(
    font: fuente,
    size: tamano,
    lang: lang,
    // Reparto de la grilla: 0,8em arriba + 0,2em abajo = 1em de «altura de
    // línea», y el resto va como leading. Ver el bloque explicativo arriba.
    top-edge: 0.8em,
    bottom-edge: -0.2em,
  )

  set par(
    leading: alto - 1em, // dentro del párrafo: 0,8 + leading + 0,2 = 2em
    spacing: alto - 1em, // entre párrafos y bloques: 0,8 + spacing + 0,2
    justify: justificar, // sin justificación completa (§ 1.22)
    first-line-indent: (amount: sangria, all: true), // CADA párrafo (§ 1.23)
  )

  // Listas y tablas también sobre la grilla.
  set list(indent: sangria, body-indent: sangria, spacing: 0pt)
  set enum(indent: sangria, body-indent: sangria, spacing: 0pt)
  set table(stroke: none) // APA: sin líneas verticales
  set block(spacing: auto) // los bloques heredan el spacing de párrafo

  // APA no numera los títulos (§ 2.27: «Do not label headings with numbers or
  // letters»).
  set heading(numbering: none)

  // ── Títulos niveles 1 a 3 (§ 2.27) ───────────────────────────────────────
  show heading: it => {
    // OJO: acá NO se pone `spacing`. En Typst el espacio entre dos bloques
    // contiguos es el MÁXIMO de los dos `spacing`, no la suma. Poner `0pt`
    // acá ponía dos títulos seguidos a 11 pt en vez de 22 (mitad de grilla),
    // mientras que título→párrafo seguía en 22 pt y disimulaba el problema.
    // Lo que APA § 1.20 pide es «no agregar espacio extra», y eso ya se
    // cumple dejando que el título herede el `spacing` global de 1em.
    set par(
      leading: alto - 1em,
      justify: justificar,
      first-line-indent: 0pt,
    )
    set text(font: fuente, size: tamano)
    if it.level == 1 {
      // Nivel 1: centrado, negrita.
      align(center)[#text(weight: "bold")[#it.body]]
    } else if it.level == 2 {
      // Nivel 2: al margen izquierdo, negrita.
      text(weight: "bold")[#it.body]
    } else {
      // Nivel 3: al margen izquierdo, negrita cursiva.
      text(style: "italic", weight: "bold")[#it.body]
    }
  }

  body
}


// ── 2. Portada (§ 1.6) ─────────────────────────────────────────────────────
//
// Todo centrado, sin sangría, y el título arranca en la 4.ª línea de la
// página (tres líneas en blanco antes).

#let portada(
  titulo,
  autores: (),
  afiliacion: none,
  curso: none,
  docente: none,
  fecha: none,
  lineas-arriba: 3,
) = {
  pagebreak(weak: true)
  set par(first-line-indent: 0pt, justify: false)
  set align(center)
  v(1fr)
  let autores = if type(autores) == str { (autores,) } else { autores }
  let datos = ()
  for a in autores {
    datos.push(a)
  }
  for d in (afiliacion, curso, docente, fecha) {
    if d != none {
      datos.push(d)
    }
  }
  let lineas = ()
  for _ in range(lineas-arriba) {
    lineas.push([])
  }
  lineas.push([#strong[#titulo]])
  // Un renglón en blanco entre el título y el nombre. Es la ÚNICA excepción que
  // APA permite en la portada: «each element placed on a separate line, no extra
  // lines added between elements, EXCEPT after the paper title» y «place one
  // double-spaced blank line between the paper title and the author names»
  // (APA, Student Title Page Guide, 7.ª ed.). Todo lo que sigue —afiliación,
  // curso, docente, fecha— va seguido, sin blancos: «double-space the rest of
  // the title page».
  lineas.push([])
  for d in datos {
    lineas.push(d)
  }
  align(center + horizon, unir(lineas))
  v(1fr)
}


// ── 3. Título del trabajo al comienzo del texto (§ 1.11) ────────────────────
//
// Empieza en una página nueva (§ 1.16: cada sección principal en su página).

#let titulo-general(titulo) = {
  nueva-pagina()
  set par(first-line-indent: 0pt, justify: false)
  align(center)[#strong[#titulo]]
}


// ── 4. Resumen (§ 2.9) y palabras clave (§ 2.10) ────────────────────────────

#let resumen(cuerpo, etiqueta: "Resumen") = {
  nueva-pagina()
  set par(first-line-indent: 0pt, justify: false)
  align(center)[#strong[#etiqueta]]
  cuerpo
}

#let palabras-clave(..claves) = {
  set par(justify: false)
  [_Palabras clave:_ #claves.pos().join(", ")]
}


// ── 5. Contenidos ───────────────────────────────────────────────────────────
//
//  ─── AVISO: ESTO NO ES APA ──────────────────────────────────────────────────
//
//  APA NO lo pide y APA NO lo gobierna. En el orden oficial de páginas (§ 2.17)
//  la tabla de contenidos ni siquiera aparece:
//
//      title page · abstract · text · references · footnotes · tables ·
//      figures · appendices
//
//  Y no hay una página de apastyle.apa.org que la regule. Varias bibliotecas lo
//  resumen así, citando a APA: «APA provides no guidance for creating a table of
//  contents. This is a technical/software issue; not an aspect of APA Style.»
//
//  O sea: esto está acá porque quizá tu institución la pida. NO es un requisito
//  de APA, y si tu docente te pide otra cosa, manda lo del docente (§ 1.10: las
//  instrucciones de la asignatura mandan sobre APA).
//
//  ─── QUÉ SÍ RESUELVE ESTA FUNCIÓN ───────────────────────────────────────────
//
//  Todo lo que sigue lo heredé de las reglas de títulos de APA (§ 2.27) y de la
//  convención general, porque APA no pone nada:
//
//    · Página propia, arranca después de donde estés.
//    · Rótulo centrado en negrita, con el MISMO estilo que un título de nivel 1.
//    · Una entrada por cada título `=` / `==` / `===` del documento.
//    · Página a la derecha con puntos guía, como todo índice del mundo.
//    · Nivel 1 pegado al margen izq., nivel 2 a +0,5 in, nivel 3 a +1,0 in.
//    · Doble espacio entre entradas: 22,0 pt, o sea la grilla. Medido.
//    · Sin sangría en la primera línea (las entradas no son párrafos).
//    · NO enumera los títulos (`set heading(numbering: none)` ya está global).
//
//  Lo que NO entra al índice, a propósito:
//
//    · la portada, la página de resumen y «Palabras clave» — son front matter,
//      y el rótulo de «Resumen» tampoco va (un índice no se indexa a sí mismo);
//    · «Contenidos» — el propio rótulo se excluye solo.
//
//  Lo que SÍ entra y por eso se cambió: «Referencias» y «Apéndice A». Hoy son
//  `heading` de nivel 1, así que aparecen solos. Antes eran `align(center)`
//  sueltos y no salían. El maquetado NO cambió, porque la regla `show heading`
//  del nivel 1 devuelve exactamente lo mismo que hacían a mano.
//
//  Si un título ocupa dos renglones (como «Apéndice A» + su título), la entrada
//  del índice sale en dos renglones también, con los puntos y la página al
//  final. Es espejo del título, no un defecto.
//
//  ─── DÓNDE VA ───────────────────────────────────────────────────────────────
//
//  APA no lo dice. La costumbre es después del resumen y antes del texto:
//
//      #portada(…)
//      #resumen([…])
//      #palabras-clave(…)
//      #contenidos()          ← acá
//      #titulo-general("…")   ← esto ya arranca página nueva
//      …
//
//  Y recuerda: el índice NO incluye la portada ni el resumen, así que las
//  entradas van a arrancar con los títulos del texto.
//
//  ─── SI LO QUERÉS A MANO ─────────────────────────────────────────────────────
//
//  Borrá la llamada y escribí la lista con `#sin-sangria(…)`, una línea por
//  entrada. La ventaja de hacerlo a mano es que podés reordenar, omitir o
//  inventar entradas; la desventaja es que los números de página los tenés que
//  perseguir a mano cada vez que se mueve el texto. Con `#contenidos()` eso lo
//  resuelve Typst solo.
//
//  `profundidad` es cuántos niveles muestra (1, 2 o 3). Los títulos de nivel 4
//  y 5 no son `heading`, así que nunca van a salir en el índice: van «en línea»
//  y no son secciones de verdad.
#let contenidos(
  etiqueta: "Contenidos",
  profundidad: 3,
  sangria: 1.27cm, // 0,5 in por nivel, lo mismo que la sangría de párrafo
) = {
  nueva-pagina()
  set par(first-line-indent: 0pt, justify: false)
  // El rótulo se pasa como contenido y Typst lo renderiza con la regla
  // `show heading` de nivel 1 → centrado en negrita, idéntico a «Método».
  outline(
    title: [#text(weight: "bold")[#etiqueta]],
    depth: profundidad,
    indent: n => n * sangria,
  )
}


// ── 5b. Lista de ilustraciones ────────────────────────────────────────────────
//
//  Debajo de la tabla de contenidos va la tabla/lista de ilustraciones
//  (figuras). APA no la exige siempre, pero si hay varias figuras conviene
//  presentarla. Se genera automáticamente a partir de `#figura()`.
//
//  Si una ilustración NO es de autoría propia (tomada, adaptada o reproducida
//  de otra fuente), DEBE aparecer también en la lista de referencias con su
//  fuente correspondiente (§ 7.12 / uso ético de figuras). La función solo
//  enumera las figuras del documento; la inclusión en referencias es tu
//  responsabilidad.
#let lista-ilustraciones(
  etiqueta: "Lista de ilustraciones",
  profundidad: none,
) = {
  nueva-pagina()
  set par(first-line-indent: 0pt, justify: false)
  outline(
    title: [#text(weight: "bold")[#etiqueta]],
    target: figure,
    depth: profundidad,
    indent: auto,
  )
}


// ── 6. Títulos niveles 4 y 5 (§ 2.27) ───────────────────────────────────────
//
// Son «en línea»: el título termina en punto y el párrafo sigue en la misma
// línea. Por eso son funciones y no elementos `heading`: el texto del párrafo
// tiene que ir dentro de la misma llamada.
//
//     #nivel4("Muestra", [La muestra quedó compuesta por 120 personas…])
//     #nivel5("Materiales", [Se usaron reactivos de grado analítico…])

#let nivel4(titulo, cuerpo, sangria: 1.27cm) = par(
  first-line-indent: sangria,
)[#strong[#titulo]. #cuerpo]

#let nivel5(titulo, cuerpo, sangria: 1.27cm) = par(
  first-line-indent: sangria,
)[#text(style: "italic", weight: "bold")[#titulo]. #cuerpo]


// ── 7. Cita larga: 40 palabras o más (§ 2.11) ───────────────────────────────
//
// `par` no tiene margen izquierdo, así que se aplica con `pad`. `par.spacing`
// sigue gobernando la separación con el bloque anterior.

#let cita-larga(cuerpo, sangria: 1.27cm) = pad(left: sangria)[
  #set par(first-line-indent: 0pt, justify: false)
  #cuerpo
]


// ── 8. Lista de referencias (§ 2.12) ────────────────────────────────────────
//
// `par.hanging-indent` = «el indent que deben tener todas las líneas menos la
// primera», o sea la sangría francesa de 0,5 in que pide APA.

#let referencia(cuerpo, sangria: 1.27cm) = par(
  hanging-indent: sangria,
  first-line-indent: 0pt,
  justify: false,
)[#cuerpo]

#let referencias(entradas, etiqueta: "Referencias") = {
  nueva-pagina()
  set par(first-line-indent: 0pt, justify: false)
  // `heading` y no `align(center)`: así «Referencias» entra en `#contenidos()`.
  // El maquetado no cambia, porque la regla `show heading` de nivel 1 devuelve
  // exactamente `align(center)[negrita]`, que es lo que había acá antes.
  heading(level: 1)[#etiqueta]
  // Acepta tanto un array de entradas como una sola entrada suelta: en Typst
  // `(x),` se colapsa a `x`, así que un array de un elemento es indistinguible
  // del contenido solo.
  let entradas = if type(entradas) == array { entradas } else { (entradas,) }
  for e in entradas {
    referencia(e)
  }
}


// ── 9. Tablas (§ 7.10) ──────────────────────────────────────────────────────
//
// El rótulo va en `block(sticky: true)` para que nunca quede huérfano al pie
// de una página, separado de la tabla que describe.

#let tabla(numero, titulo, cuerpo, nota: none) = {
  set par(first-line-indent: 0pt, justify: false)
  block(sticky: true, unir(([#strong[Tabla #numero]], [#emph[#titulo]])))
  cuerpo
  if nota != none {
    unir(([#strong[Nota.] #nota]))
  }
}


// ── 10. Figuras (§ 7.24) ─────────────────────────────────────────────────────

#let figura(numero, titulo, imagen, nota: none) = {
  set par(first-line-indent: 0pt, justify: false)
  // Una figura incrustada en el texto va separada del texto por un renglón en
  // blanco a doble espacio, arriba y abajo: «Also add one blank double-spaced line
  // between the figure and any text to improve the visual presentation» (APA,
  // Figure setup).
  //
  // OJO con el número: el hueco pedido son 44 pt de DISTANCIA ENTRE BASES, no de
  // `above`. El Delta medido es `bottom-edge + hueco + top-edge` = 2,2 + h + 8,8
  // = h + 11. Por eso h = 33 pt, no 44 pt (con 44 el Delta da 55 y la grilla se
  // rompe). Medido:
  //
  //     above/below   Δ(texto → «Figura 1»)
  //     auto              22,0
  //     22pt              33,0
  //     33pt              44,0   ← este
  //     44pt              55,0
  block(above: 33pt, below: 33pt, sticky: true, unir(([#strong[Figura #numero]], [#emph[#titulo]])))
  imagen
  if nota != none {
    unir(([#strong[Nota.] #nota]))
  }
}


// ── 11. Apéndices (§ 2.5) ───────────────────────────────────────────────────

#let apendice(letra, titulo) = {
  nueva-pagina()
  set par(first-line-indent: 0pt, justify: false)
  // Ídem `referencias`: `heading` de nivel 1 para que «Apéndice A» entre en el
  // índice. La regla `show heading` la centra y la pone en negrita igual que
  // el `align(center)` de antes.
  heading(level: 1)[#unir(([Apéndice #letra], [#titulo]))]
}


// ── 12. Utilidades ──────────────────────────────────────────────────────────

// Volumen de una revista en cursiva con el número de edición entre paréntesis:
//     #vol(14, 2)   →   14(2)
//
// Nota técnica: en Typst no se puede encadenar un segundo grupo de argumentos
// sobre un bloque de contenido, así que `#emph[14](2)` NO compila. Por eso los
// paréntesis se emiten como cadena de texto y no como agrupamiento de markup.
//
// Y el cuerpo va en UNA sola línea a propósito: si el `[` abre y el `]` cierra en
// renglones distintos, los saltos de línea se vuelven espacios y queda un
// espacio colgando al final. Salía `14(2) , 210-219` en vez de `14(2), 210-219`.
#let vol(numero, edicion) = [#text(style: "italic")[#numero]#"("#edicion#")"]

#let sangria-parrafo(cuerpo) = par(first-line-indent: 1.27cm)[#cuerpo]

#let sin-sangria(cuerpo) = par(first-line-indent: 0pt)[#cuerpo]
