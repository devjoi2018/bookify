---
name: bookify
description: Convierte lo que se investigó en la conversación, o cualquier tema, en un libro digital ilustrado y fácil de leer y compartir (un solo archivo HTML con paso de página, para celular y PC), siempre con el mismo diseño y el mismo tono. Úsala cuando pidan pasar algo a libro o hacer un libro de algo, sea una guía, un manual, una historia, una explicación, el resultado de una investigación o cualquier otro contenido ("conviértelo en libro", "haz un libro con esto", "turn this into a book"). También construye y lista libros, y con el argumento update busca e instala una versión nueva de la skill.
license: MIT
argument-hint: "[tema | build [nombre|all] | list | version | update]"
allowed-tools: Bash(python *) Bash(python3 *) Bash(py *)
---

# Bookify

Pedido: $ARGUMENTS

La skill está instalada en `{{SKILL_DIR}}` (en adelante, **la carpeta de la skill**). Todas las
rutas de abajo son relativas a ella.

- **El motor:** `python "{{SKILL_DIR}}/engine/build.py"`. Si `python` no responde, usa `python3`; en Windows, `py`. Si ninguno existe, di al usuario que necesita Python 3.9 o superior (python.org) y para: no lo instales tú. Nunca instales paquetes: el motor no los necesita.
- **El instalador:** `python "{{SKILL_DIR}}/install.py"`.

Ejecuta el motor **desde la carpeta de trabajo del usuario** (la del proyecto abierto). Ahí crea
`books/<Name>/` (la fuente de cada libro) y `output/<Title>.html` (el libro terminado).

## Qué hacer según el pedido

Mira la primera palabra del pedido:

- **`update`**: sigue [Actualizar](#actualizar).
- **`version`**: ejecuta el motor con `--version` y di la versión.
- **`list`**: ejecuta el motor con `--list`.
- **`build`**: con `all` o sin nombre, el motor con `--all`; si no, el motor con `"Name"`. Luego sigue el paso 7 del flujo.
- **Cualquier otra cosa, o nada:** crea o cambia un libro con el [flujo](#flujo). Si el pedido está vacío, el contenido es lo que se ha investigado o hablado en esta conversación.

## Actualizar

1. Ejecuta el instalador con `--check`. La última línea dice `STATUS=…`.
2. `STATUS=up-to-date`: dilo en una línea con la versión. `STATUS=no-releases`: di que aún no hay versiones publicadas. Si sale `Error:`, explica la causa.
3. `STATUS=new`: muestra la versión nueva y resume las novedades en 2–4 líneas. Después ejecuta el instalador con `--update`: descarga el release y actualiza la skill en todas las herramientas donde esté instalada.
4. Termina diciendo que reinicie la herramienta (o abra una sesión nueva) para usar la versión nueva.

## Recursos (léelos antes de escribir)

- Tono y cómo adaptarlo a cada tipo de libro y a cada idioma: [style.md](style.md). Obligatorio.
- Estructura según el tipo de contenido: [structures.md](structures.md).
- Formato de `content.json`, bloques y cuánto cabe en una página: [format.md](format.md).
- Sello visual (paleta, tipografías, portada, reglas de dibujo): [engine/template/DESIGN.md](engine/template/DESIGN.md).
- Revisión antes de entregar: [review.md](review.md).
- Un libro terminado, para ver cómo queda el JSON: [example.json](example.json). Es solo una muestra del formato: no copies su tema, su estructura ni sus textos.

Solo se escribe **contenido**: `books/<Name>/content.json` y sus dibujos SVG. El motor pone el
diseño, la animación, los números de página y el índice. **Nunca escribas HTML, CSS ni JS para un
libro**, ni edites el `.html` de `output/`.

## Flujo

1. **Reúne el material.** Si en la conversación ya hay una investigación, respuestas o documentos, **esa es la fuente principal**: el libro cuenta eso, completo y fiel, sin inventar. Si solo hay un tema, investiga en fuentes primarias (documentación oficial, artículos científicos, instituciones, archivos). Guarda las URLs de todo lo que uses.
2. **Decide qué clase de libro pide el contenido**, no al revés: `guide`, `manual`, `story`, `explainer`, `research` u `other` ([structures.md](structures.md)). Decide también el **idioma**: el del usuario en esta conversación, salvo que pida otro. Si el propósito o el lector no están claros y el usuario está presente, pregunta una sola vez.
3. **Escaleta.** Capítulos y una idea por página. Muéstrala en 5–12 líneas y espera el visto bueno si el usuario está presente. Si pidió hacerlo sin preguntar, sigue.
4. **Crea la carpeta** (solo para un libro nuevo): el motor con `--new "Name" --type <type> --lang <código>` (`es`, `en`, `pt`, `fr`…). El nombre de la carpeta puede ir en el idioma del libro.
5. **Escribe** `books/<Name>/content.json` siguiendo [style.md](style.md) y [format.md](format.md). Claves en inglés; todo el texto, en el idioma elegido.
6. **Dibuja** los SVG que falten en `books/<Name>/images/` (reglas en `DESIGN.md`, sección 7). Cada portada lleva su propia ilustración. Puedes reutilizar dibujos de otros libros de la carpeta.
7. **Construye:** el motor con `"Name"`. Si marca `overflows`, divide o recorta esa página; si marca `check`, acórtala un poco o pide al usuario que lo confirme abriendo `output/<Title>.html?check`. **Nunca** bajes el tamaño de letra.
8. **Revisa** con [review.md](review.md). Si tu herramienta puede lanzar un subagente, encárgale la revisión con ese archivo y la carpeta del libro, para que lo lea con ojos nuevos; si no, hazla tú. Aplica solo lo que afecte a claridad, exactitud o al sello, y reconstruye.
9. **Entrega** la ruta de `output/<Title>.html`. Es un solo archivo: se abre en cualquier navegador y se comparte por correo o mensajería.

## Reglas que no cambian

- El diseño y la voz son los mismos en todos los libros: no inventes colores, tipografías ni estilos por libro.
- Nada copiado de otra obra: ni frases, ni ejemplos, ni ilustraciones.
- Los hechos llevan fuente en la página final. Si algo es opinión, ficción o simplificación, dilo.
- Sin colección ni numeración: la portada lleva título, subtítulo, una etiqueta del tipo de libro y, si quieres, fecha o autor en el pie.

## Lista de control

- [ ] El libro cuenta lo investigado sin dejar fuera lo importante ni añadir hechos sin fuente.
- [ ] Cada página tiene una sola idea y la construcción no marca `overflows`.
- [ ] La estructura corresponde al tipo de contenido ([structures.md](structures.md)).
- [ ] Todo el texto está en el idioma elegido, y `language` está bien puesto en el JSON.
- [ ] Cada capítulo empieza con un `chapter` y los colores rotan (`mint` → `indigo` → `coral`).
- [ ] Portada con ilustración propia. Hay un dibujo o diagrama al menos cada tres páginas.
- [ ] Fuentes al final.
