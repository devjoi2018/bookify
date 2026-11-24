# Sistema de diseño · Bookify

Este archivo es la referencia visual de todos los libros, sean del tema y del tipo que sean. Todo libro nuevo usa
esta paleta, estas tipografías y estos componentes. No se inventan colores ni
estilos por libro: el sello se reconoce porque es siempre el mismo.

Inspiración declarada: la claridad editorial de *Proceso creativo* (Eduardo
Salles): papel blanco, colores planos, dibujos de línea y una idea por página.
Es una inspiración, no una copia. Nuestro sello tiene **paleta propia (Faro)**,
**portada propia** (índigo con círculo coral, título serif a la izquierda) y
**marcas propias** (la chispa coral en las notas). No se reproducen sus textos,
ilustraciones, colores, portada ni maquetación.

---

## 1. Principios del sello

1. **Una idea por página.** Si una página necesita dos ideas, son dos páginas.
2. **El blanco es parte del diseño.** El papel vacío deja respirar la idea.
3. **Dibujo antes que adorno.** Cada ilustración explica algo; si no explica, sobra.
4. **Tres colores y tinta.** Índigo, coral y menta sobre papel blanco. Nada más.
5. **Color a sangre solo en momentos clave:** portada, aperturas de capítulo y contraportada.
6. **Leer en cualquier pantalla.** La página es fija (2:3) y se escala entera.

---

## 2. Paleta "Faro"

Un faro: una luz cálida (coral) sobre un mar profundo (índigo), con agua tranquila (menta).

| Nombre | Hex | Rol | Dónde se usa |
|---|---|---|---|
| Tinta Noche | `#1B1B2F` | Texto y trazo | Todo el texto, contornos de ilustraciones |
| Papel | `#FFFFFF` | Fondo de página | Todas las páginas interiores |
| Índigo Faro | `#3949D6` | Acento principal y color de marca | Portada, contraportada, folios, subrayados de definición, viñetas, índice, apertura índigo, relleno de dibujos |
| Coral Chispa | `#FF6B4F` | Acento cálido | Círculo de portada, segunda línea del título, chispa de las notas, resultados (píldora), apertura coral, relleno de dibujos |
| Menta Pausa | `#BFE6D5` | Calma | Aperturas reflexivas, rellenos suaves |
| Tinte Índigo | `#ECEEFD` | Fondo suave | Fondo de `código` |
| Gris Nota | `#5E5E70` | Texto secundario | Pies, aclaraciones |
| Filete | `#E5E6EE` | Líneas finas | Separadores de tabla |
| Mesa clara / oscura | `#E7E8EE` / `#17182A` | Fondo detrás del libro | Según el tema del sistema |

**Proporción aproximada por libro:** 70 % papel, 15 % tinta, 10 % índigo, 5 % coral.

**Reglas de color**
- Una página interior lleva como máximo **dos** acentos (índigo y coral) además de la tinta.
- Texto: blanco sobre índigo; tinta sobre coral y menta. El texto nunca va en coral sobre blanco salvo la chispa y el resalte de la portada.
- Las aperturas rotan en este orden: **menta → índigo → coral** y vuelven a empezar.
- Portada y contraportada: siempre índigo.
- Las páginas siempre son claras, también si el dispositivo está en modo oscuro (un libro es papel). Solo la mesa cambia.

**Lo que no se usa nunca** (para no copiar la inspiración): amarillo, azul cielo, durazno, títulos de portada en mayúsculas espaciadas, retícula de puntos en portada, el sol como icono de nota.

---

## 3. Tipografía

| Uso | Fuente | Peso | Tamaño (en página de 440 px) |
|---|---|---|---|
| Títulos de capítulo (apertura) | Merriweather | 900 | 46 px |
| Título de página | Merriweather | 900 | 34 px (nivel 1) · 25 px (nivel 2) |
| Pregunta grande | Merriweather | 400 + 900 | 33 px: primera línea normal, segunda negra |
| Texto | Source Serif 4 | 400 / 700 | 16.5 px, interlineado 1.6, justificado con guiones |
| Destacado | Source Serif 4 | 400 | 20 px |
| Notas "Por ejemplo:" | Patrick Hand | 400 | 19 px, frase normal, centradas; etiqueta en mayúsculas índigo con chispa coral |
| Título de portada | Merriweather | 900 | 52 px, alineado a la izquierda, 2.ª línea en coral |
| Etiqueta de portada, folios, etiquetas, código, teclas | Montserrat | 600 / 800 | 10–14 px |

Reglas:
- Títulos sin punto final. Se equilibran en 1–2 líneas.
- Negritas: de 1 a 3 por página, solo para conceptos clave.
- Subrayado índigo (`__así__`) solo para **definiciones**.
- Nada de texto en mayúsculas salvo la etiqueta de las notas y la de la portada.

---

## 4. La página

- Tamaño lógico fijo: **440 × 660 px** (2:3, como un libro de 15 × 23 cm).
- Márgenes: 58 px arriba, 46 px a los lados, 66 px abajo.
- Folio (número) centrado abajo, Montserrat 11 px, índigo. Lo pone el script.
- Contenido centrado verticalmente por defecto. Las páginas densas usan `"align": "top"`.
- Espacio útil: unos 348 × 536 px. Como guía: **máximo ~110 palabras** de texto corrido por página, o un diagrama + 40 palabras.

**Cómo se ve en cada pantalla** (lo decide `book.js`):

| Pantalla | Vista |
|---|---|
| PC / portátil | Dos páginas abiertas, con lomo, sombra y canto de hojas |
| Tableta horizontal | Dos páginas abiertas |
| Tableta vertical | Una página |
| Celular vertical | Una página |
| Celular horizontal | Una página a lo ancho, se lee deslizando hacia abajo |

Regla técnica: dos páginas si la pantalla es horizontal, ≥ 900 px de ancho y ≥ 500 px de alto.

---

## 5. Tipos de página

La portada de cada libro cambia solo su etiqueta, título, subtítulo, pie e ilustración: la composición es fija para que el sello se reconozca.


| Tipo | Para qué | Notas |
|---|---|---|
| `cover` | Primera página | Fondo índigo; círculo coral grande que sale por la esquina superior derecha con la ilustración dentro; arriba a la izquierda la etiqueta del tipo de libro ("Guía", "Historia"…); abajo el título en Merriweather blanco con la 2.ª línea en coral, subtítulo y un pie con fecha o autor. Sin colección ni numeración |
| `contents` | Índice automático | Lo arma el script con los capítulos y las páginas que llevan `"toc"` |
| `chapter` | Inicio de capítulo | Color a sangre, título grande, subtítulo opcional |
| `page` | Todo lo demás | Una lista de bloques |
| `back-cover` | Cierre | Índigo, ilustración pequeña y 1–2 frases en blanco |

El script agrega una página en blanco si hace falta para que la contraportada cierre el libro en vista doble (en celular no se muestra).

---

## 6. Bloques (componentes)

| Bloque | Uso | Campos |
|---|---|---|
| `illustration` | Dibujo al inicio de la página | `src`, `size`: `s` (84 px), `m` (120 px), `l` (ancho completo) |
| `heading` | Título de página | `text`, `level` 1 o 2 |
| `question` | Título en forma de pregunta | `light`, `bold` |
| `text` | Párrafos | `text` (párrafos separados por línea en blanco), `align` |
| `highlight` | Frase grande, la idea de la página | `text`, `align` |
| `note` | Nota manuscrita con chispa coral | `label` ("Por ejemplo:", "Ojo:", "Truco:", "Señal:"), `text` |
| `list` | Viñetas o pasos | `items`, `ordered`, `start` |
| `table` | Dos columnas cortas | `rows` |
| `levels` | Escala con código + explicación | `rows` |
| `facts` | Datos técnicos (etiqueta índigo + valor) | `rows` |
| `sizes` | Círculos de tamaño creciente | `items`: `name`, `size`, `opacity` |
| `combine` | Diagrama A + B → resultado | `icon`, `a`, `b`, `b_label`, `result` |
| `columns` | Comparar dos ideas | `columns`: `icon`, `title`, `text` |
| `myths` | Ideas tachadas + explicación | `items`: [tachado, explicación], `icon` |
| `sources` | Lista de enlaces | `items`: [título, url] |
| `footnote` | Aclaración pequeña en gris | `text` |
| `space` | Aire extra | `height` |
| `html` | Salida de emergencia | `html` (usar casi nunca) |

**Formato dentro del texto:** `**negrita**`, `__definición__` (subrayado índigo), `*cursiva*`, `` `código` ``, `[[Tecla]]`, `==resalte índigo==` (dentro de notas), `[texto](https://…)`.

---

## 7. Ilustraciones

Cada libro guarda sus dibujos en `books/<Name>/images/*.svg`. Los iconos comunes (`spark`, `cross`, `check`) y `cover-base` viven en `engine/template/icons/`.

Reglas de dibujo:
- **Trazo de tinta de 3 px**, puntas y uniones redondeadas. Formas planas, sin degradados ni sombras.
- **Rellenos solo con las clases de la paleta:** `indigo`, `coral`, `mint` (menta), `paper` (papel), `ink` (tinta).
- Clases de trazo: `line` (solo contorno), `outline` (contorno + relleno; se combina con una de color: `class="outline indigo"`).
- Uno o dos colores por dibujo, más la tinta.
- Formas simples y reconocibles: círculos, objetos cotidianos, flechas, personajes muy geométricos.
- `viewBox` de 120×120 para iconos, 300×N para dibujos anchos, 52×52 para los iconos dentro de diagramas.
- Sin `id` dentro de los SVG (se repiten en las páginas y chocarían).
- Nada de texto dentro del dibujo, salvo etiquetas muy cortas en Montserrat.
- Originales siempre: no se calcan ilustraciones de otros libros ni personajes con marca.
- Colores fijos dentro del SVG (si hacen falta): `#1B1B2F`, `#3949D6`, `#FF6B4F`, `#FFFFFF`.

---

## 8. Ritmo de un libro

1. Portada → Índice → Introducción (2–3 páginas).
2. Cada capítulo: **apertura** → página-pregunta o definición → páginas de desarrollo → (opcional) página de ejemplo con nota → cierre corto.
3. Alternar páginas con dibujo y páginas solo de texto. Nunca más de tres páginas seguidas sin dibujo ni diagrama.
4. Cerrar con epílogo, fuentes y contraportada.
