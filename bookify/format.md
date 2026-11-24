# Formato de content.json

Archivo: `books/<Name>/content.json`. Los dibujos van en `books/<Name>/images/*.svg` y se citan
por nombre sin extensión. Si un dibujo no está ahí, se busca en los iconos de la plantilla
(`engine/template/icons/`, por ejemplo `cover-base`).

Las claves y los valores fijos del JSON van en inglés; los textos del libro, en el idioma del libro.

```json
{
  "title": "Nombre del libro",
  "type": "research",
  "language": "es",
  "description": "Una línea para buscadores y vistas previas.",
  "pages": [
    {"type": "cover", "label": "Investigación",
     "title": ["Línea blanca", "línea coral"], "illustration": "cover",
     "subtitle": "Una frase que dice qué aprenderás.", "footer": ["Mes Año", "Autor (opcional)"]},
    {"type": "contents", "title": "Índice", "illustration": "icono"},
    {"type": "page", "id": "intro", "toc": "Introducción", "toc_main": true, "blocks": [ … ]},
    {"type": "chapter", "title": "Capítulo", "subtitle": "opcional", "color": "mint"},
    {"type": "page", "align": "top", "blocks": [ … ]},
    {"type": "back-cover", "illustration": "icono", "text": "Una o dos frases."}
  ]
}
```

- `type` del libro: `guide`, `manual`, `story`, `explainer`, `research` u `other`.
- `language`: código del idioma del libro (`es`, `en`, `pt`, `fr`…). Pone el idioma de la página y los textos del lector (botones, "Portada", "Fin"). El motor trae `es`, `en` y `pt`; para otro idioma, añade `"ui"` con las traducciones (claves: `cover`, `end`, `contents`, `go_contents`, `previous`, `next`, `navigation`, `example`, `check`, `all_fit`, `one_overflows`, `n_overflow`, `page_abbr`). Si falta alguna, se usa el inglés.
- Portada (`cover`): `label` es la palabra de arriba a la izquierda que dice qué clase de libro es ("Guía", "Historia", "Investigación"…), en el idioma del libro; si falta, se pone la del tipo. `footer` lleva fecha, autor o lo que quieras. Los libros no llevan colección ni número.
- Los capítulos (`chapter`) entran solos al índice (con `"toc": false` no entran). Una `page` entra si tiene `"toc": "Texto"` (subentrada; con `"toc_main": true`, entrada principal).
- Colores de capítulo: `mint`, `indigo`, `coral`, rotando en ese orden.
- `"align": "top"` para páginas densas; por defecto el contenido va centrado en vertical.
- Los números de página, el índice y la página en blanco final los pone el script.

## Bloques

```json
{"type": "illustration", "src": "nombre", "size": "s|m|l"}
{"type": "heading", "text": "Título", "level": 1}
{"type": "question", "light": "¿Qué es", "bold": "la idea?"}
{"type": "text", "text": "Párrafo.\n\nOtro párrafo.", "align": "center"}
{"type": "highlight", "text": "La frase que resume la página.", "align": "center"}
{"type": "note", "label": "Por ejemplo:", "text": "Caso breve con ==resalte índigo==."}
{"type": "list", "items": ["**Uno:** …", "**Dos:** …"], "ordered": true, "start": 1}
{"type": "table", "rows": [["Columna A", "Columna B"]]}
{"type": "levels", "rows": [["etiqueta", "Descripción corta"]]}
{"type": "facts", "rows": [["Etiqueta", "Valor"]]}
{"type": "sizes", "items": [{"name": "Chico", "size": 40, "opacity": 0.5}, {"name": "Grande", "size": 90}]}
{"type": "combine", "icon": "dibujo52", "a": "Elemento A", "b": "B", "b_label": "Qué es B", "result": "Resultado"}
{"type": "columns", "columns": [{"icon": "dibujo56", "title": "Idea A", "text": "…"}, {"icon": "dibujo56", "title": "Idea B", "text": "…"}]}
{"type": "myths", "items": [["Idea tachada", "Por qué no es así"]], "icon": "cross"}
{"type": "sources", "items": [["Título", "https://…"]]}
{"type": "footnote", "text": "Aclaración pequeña."}
{"type": "space", "height": 16}
```

| Bloque | Úsalo para |
|---|---|
| `illustration` | Dibujo al inicio de la página. `s` 84 px, `m` 120 px, `l` ancho completo. |
| `heading` | Título de página (nivel 1 grande, nivel 2 mediano). |
| `question` | Título en forma de pregunta: primera línea ligera, segunda negra. |
| `text` | Párrafos; línea en blanco separa párrafos. |
| `highlight` | La frase que resume la página. |
| `note` | Ejemplo, advertencia o truco, manuscrito con la chispa coral. Etiquetas, en el idioma del libro: "Por ejemplo:", "Ojo:", "Truco:", "Señal:", "Dato:". Sin `label`, se pone "Por ejemplo:" en el idioma del libro. |
| `list` | Viñetas o pasos; `start` continúa la numeración en otra página. |
| `table` | Dos columnas cortas (síntoma → arreglo, término → significado). |
| `levels` | Una escala: etiqueta corta + explicación. |
| `facts` | Datos clave de algo (etiqueta índigo + valor). |
| `sizes` | Círculos de tamaño creciente para comparar magnitudes. |
| `combine` | Diagrama A + B → resultado. |
| `columns` | Comparar dos ideas lado a lado. |
| `myths` | Creencias equivocadas tachadas, con la explicación. Icono: `cross` (por defecto) o `check`. |
| `sources` | Lista de enlaces a las fuentes. |
| `footnote` | Aclaración pequeña en gris. |
| `space` | Aire extra en px. |
| `html` | Salida de emergencia con HTML propio. Casi nunca. |

Formato en línea: `**negrita**` · `__definición__` (subrayado índigo) · `*cursiva*` · `` `código` `` · `[[Tecla]]` · `==resalte índigo==` · `[enlace](https://…)`.

## Cuánto cabe en una página (aproximado)
- Ilustración `s` + título nivel 2 + ~90 palabras.
- Ilustración `l` + título nivel 2 + ~60 palabras.
- Un `combine` + ~45 palabras, o dos `combine` solos.
- Tabla: hasta 8 filas cortas. Lista: hasta 5 elementos cortos.

Al construir, el script estima el espacio (sin navegador ni dependencias) y marca:
- `⚠ overflows`: divide la página o recorta.
- `· check`: puede que quepa justo; acorta un poco o confírmalo abriendo `output/<Title>.html?check` en el navegador, que mide de forma exacta y señala las páginas que se salen.

Nunca bajes el tamaño de letra para que algo quepa.
