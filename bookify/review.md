# Revisión de un libro

Revisa el libro como si no lo hubieras escrito tú. La carpeta del libro es `books/<Name>/`, en la carpeta de trabajo del usuario.

Lee primero:
- `{{SKILL_DIR}}/style.md` (tono y cómo adaptarlo al tipo de libro y al idioma)
- `{{SKILL_DIR}}/structures.md` (estructura según el tipo)
- `{{SKILL_DIR}}/format.md` (bloques y capacidad de página)
- `{{SKILL_DIR}}/engine/template/DESIGN.md` (paleta, portada, reglas de dibujo)

Después lee `books/<Name>/content.json` (sus campos `type` e `language` dicen qué clase de libro es y en qué idioma está) y los SVG de `books/<Name>/images/`.

Comprueba, página por página:
1. Una sola idea por página; texto corrido por debajo de ~110 palabras.
2. Voz cercana en segunda persona, frases cortas, cierre en una línea, definiciones en llano, ejemplos con `note`, con los ajustes del tipo de libro.
3. Todo el texto en el idioma de `language`, natural en ese idioma (no traducido palabra por palabra).
4. La estructura sigue la de su tipo en `structures.md` (o se aparta con un buen motivo).
5. Nada de jerga sin explicar, exclamaciones, emojis, rayas (—) ni más de 3 negritas por página.
6. Aperturas en cada capítulo y colores rotando menta → índigo → coral.
7. Dibujos con las clases `line`, `outline`, `indigo`, `coral`, `mint`, `paper`, `ink`; sin `id`; sin colores fuera de la paleta.
8. Afirmaciones de hechos con su fuente en la página final; la ficción o reconstrucción, declarada.
9. Ninguna frase que parezca copiada de otra obra.

Responde con una lista corta: número aproximado de página (por su posición en `pages`), el problema y el arreglo concreto. Incluye solo lo que afecte a claridad, exactitud o al sello. Omite gustos personales. Si todo está bien, dilo en una línea.
