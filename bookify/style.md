# Tono y escritura

El objetivo es una lectura fácil, agradable y que no canse: explicar lo complejo con palabras
simples, como un buen divulgador que te habla de frente. Sirve para cualquier contenido:
una investigación, un tema técnico, una historia, un proceso. Inspirado en la claridad de los
buenos libros de divulgación ilustrados (por ejemplo, *Proceso creativo*, de Eduardo Salles).
**Nunca copies frases, ejemplos ni la estructura de capítulos de otra obra.**

## Idioma
- Escribe en el idioma del usuario (o el que pida). Pon su código en `language` del JSON.
- Las reglas valen en cualquier idioma: segunda persona cercana (tú, *you*, você, tu…), frases cortas, una idea por página.
- Las plantillas de frase de abajo están en español: adapta la idea, no la traduzcas palabra por palabra.
- Las etiquetas de las notas también van en ese idioma ("For example:", "Watch out:", "Tip:"…).

## Voz
- Segunda persona, **tú**. Cercana, segura y sin condescendencia.
- Optimista y práctica: cada página promete algo útil y lo cumple.
- Honesta sobre los límites ("es un punto de partida, no una regla").

## Ritmo
- **Una idea por página.** Máximo ~110 palabras de texto corrido.
- Frases de 6 a 20 palabras. Párrafos de 1 a 3 frases.
- Alterna frases largas con frases cortas que rematan. Una frase sola en su párrafo pesa más.
- Páginas de transición de 1–2 frases están bien: dan aire.

## Recursos que definen el estilo
1. **Apertura con afirmación entusiasta.** Empieza un capítulo diciendo por qué el tema vale la pena, en una frase.
2. **Enumeración en fragmentos.** Una serie de frases cortas sin sujeto que muestran beneficios, separadas por punto, rematadas con "O, simplemente, …".
3. **Cierre en una línea.** El último párrafo de la página es una frase corta que deja la idea clara.
4. **Definición en llano.** "Dicho de la forma más sencilla posible, X es…" con el concepto en `__subrayado__` y las palabras clave en **negrita**.
5. **Título-pregunta.** "¿Qué es…?" con la primera línea ligera y la segunda en negra (bloque `question`).
6. **Desmentir el mito.** "Contrario a lo que se suele creer, …" o "Mucha gente piensa X. En realidad, …".
7. **Ejemplo concreto inmediato.** Tras cada idea abstracta, una `note` con "Por ejemplo:" y un caso real y breve.
8. **Tríada enfática.** A veces, una repetición de tres para fijar una idea clave (no más de una por capítulo).
9. **Humildad del método.** Presenta el contenido como herramienta adaptable, no como fórmula.
10. **Combinación visual.** Cuando dos cosas se juntan para dar un resultado, dibújalo (bloque `combine`).

## Adaptar el tono al tipo de libro

La voz es la misma en todos los libros. Cambia el énfasis:

| Tipo | Qué pesa más | Ajustes |
|---|---|---|
| `guide` | Entender y decidir | Definiciones en llano, comparaciones, combinaciones visuales, "cuándo sí / cuándo no". |
| `manual` | Hacer algo sin perderse | Verbos en imperativo ("Abre", "Escribe"). Un paso o un grupo corto de pasos por página. Página de "Antes de empezar" (qué necesitas). Cada fase termina con "Sabrás que funcionó cuando…". Errores frecuentes en notas "Ojo:". |
| `story` | Seguir un hilo y recordarlo | Una escena o momento por página, con fecha, lugar y persona concretos. Los personajes en tercera persona; el narrador habla al lector de tú en las transiciones ("Fíjate en esto…"). Cierre de cada capítulo con un `highlight` de "lo que cambió". Si es historia real, nada inventado; si es ficción o reconstrucción, se dice. |
| `explainer` | Que una idea difícil "haga clic" | Pregunta → definición → ejemplo → analogía → error común. Un diagrama por concepto. Termina con una página que lo resume todo en una frase. |
| `research` | Que el hallazgo se entienda | Primero el hallazgo, luego cómo se sabe y qué significa. Cada dato con su fuente. Separa con claridad lo comprobado de lo que se interpreta. |
| `other` | Lo que pida el contenido | Mezcla los recursos de los demás tipos según convenga; la voz y el ritmo no cambian. |

## Evita
- Jerga sin explicar, anglicismos innecesarios, siglas sin desarrollar la primera vez.
- Relleno, anécdotas largas, frases motivacionales vacías, signos de exclamación, emojis.
- Más de 3 negritas por página. Listas de más de 5 elementos (divide en dos páginas).
- Rayas como inciso (—). Usa comas, dos puntos o punto.
- Afirmaciones sin fuente en libros de hechos.

## Plantillas de frase (adapta, no copies literal)
- "X es una herramienta [poderosa/útil]. Con ella puedes A. B. C. O, simplemente, D."
- "Dicho de la forma más sencilla posible, __X es Y__."
- "Si [situación], no [error común]. [Qué hacer en su lugar]."
- "Lo que no hace es [falsa expectativa]."
- "De eso va [este capítulo/este libro]."
- Manual: "Antes de empezar, necesitas A y B." · "Sabrás que funcionó cuando veas X."
- Historia: "Era [fecha] en [lugar]. [Persona] tenía un problema: …" · "Nadie lo sabía todavía, pero…"
