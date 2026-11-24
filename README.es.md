<div align="center">

<img src="docs/logo.svg" alt="Logo de Bookify" width="96">

# Bookify

**Convierte lo que investigas con tu IA en un libro ilustrado, claro y fácil de leer.**

[English](README.md) · **Español**

[![Licencia: MIT](https://img.shields.io/badge/Licencia-MIT-3949D6.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-3949D6.svg)](https://www.python.org/downloads/)
[![Última versión](https://img.shields.io/github/v/release/devjoi2018/bookify?color=FF6B4F&label=versi%C3%B3n)](https://github.com/devjoi2018/bookify/releases)
[![Sin dependencias](https://img.shields.io/badge/dependencias-ninguna-BFE6D5.svg)](#requisitos)

<a href="https://devjoi2018.github.io/bookify/es/"><img src="docs/demo.gif" alt="Pasando las páginas del libro de muestra, hecho con Bookify" width="760"></a>

**[Lee el libro de muestra en tu navegador](https://devjoi2018.github.io/bookify/es/)**

</div>

---

Bookify es una *skill* para tu asistente de IA. Toma lo que investigaste en una conversación y lo
convierte en un libro digital corto, ilustrado y bien explicado.

Sirve para dos cosas:

- **Entender mejor** lo que investigaste.
- **Compartirlo** de una forma que la gente sí quiera leer.

Funciona dentro de Claude Code, Command Code, OpenCode y GitHub Copilot.

## Contenido

- [El problema](#el-problema)
- [La solución de siempre](#la-solución-de-siempre)
- [Qué hace Bookify](#qué-hace-bookify)
- [Para qué puedes usarlo](#para-qué-puedes-usarlo)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Actualizar](#actualizar)
- [Desinstalar](#desinstalar)
- [Referencia de comandos](#referencia-de-comandos)
- [Usarlo sin asistente](#usarlo-sin-asistente)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Licencia](#licencia)

## El problema

Investigar con una IA es rápido. Leer lo que responde, no tanto.

- **Escribe mucho.** Respuestas largas, con párrafos que repiten lo mismo con otras palabras.
- **Las ideas se pierden.** Lo importante queda enterrado entre listas, matices y advertencias.
- **Suena genérico.** El texto tiene ese tono de relleno que se reconoce enseguida: el famoso *AI slop*.
- **Cuesta compartirlo.** Nadie quiere abrir un muro de texto copiado de un chat.

Al final tienes mucha información, pero no siempre la entiendes mejor que antes.

## La solución de siempre

Lo normal es pedirle a la IA que lo explique de nuevo:

> *"Explícamelo más simple."*
> *"Más corto."*
> *"Ahora sin tanto relleno."*
> *"Ponle un ejemplo."*

Funciona, pero lleva varias vueltas. Y cada vez que empiezas un tema nuevo, vuelves a empezar desde cero.

## Qué hace Bookify

Bookify le da a tu asistente unas reglas fijas para escribir y diseñar. Así, en lugar de iterar
tú a mano, el asistente ya sabe cómo debe quedar el resultado:

- **Una idea por página.** Nada de bloques eternos.
- **Frases cortas y lenguaje sencillo.** Sin relleno ni frases de cartón.
- **Ejemplos y dibujos** donde ayudan a entender.
- **Fuentes al final** para los datos que lo necesitan.
- **Una revisión antes de entregarlo** que comprueba cada página: una sola idea, nada de jerga sin explicar, nada de páginas demasiado largas.

El resultado es un libro con un diseño limpio y profesional, en un solo archivo `.html`:

- Se abre en cualquier navegador, sin instalar nada.
- Se lee bien en el celular (una página) y en la computadora (dos páginas).
- Pasas las páginas como en un libro de verdad.
- Lo compartes por correo, chat o una nube.
- Se escribe en el idioma en que hablas con tu asistente.

> [!NOTE]
> Bookify no inventa información: trabaja con lo que investigaste. Si la conversación tiene datos
> dudosos, el libro también los tendrá. Revisa siempre las fuentes de lo importante.

## Para qué puedes usarlo

Algunas ideas:

- **Tu biblioteca personal.** Guarda cada investigación como un libro y vuelve a ella cuando la necesites.
- **Explicarle algo a tu equipo.** Una guía corta en vez de un documento largo.
- **Aprender un tema nuevo.** Pide el libro para repasar lo que acabas de investigar.
- **Compartir con quien no usa IA.** Un archivo que cualquiera puede abrir y entender.

Sirve para guías, manuales, historias, explicaciones, resúmenes de investigación o lo que necesites.

## Requisitos

- [Python 3.9 o superior](https://www.python.org/downloads/)
- Una de estas herramientas: [Claude Code](https://claude.com/claude-code), [Command Code CLI](https://commandcode.ai), [OpenCode](https://opencode.ai) o [GitHub Copilot en VS Code](https://github.com/features/copilot)

## Instalación

1. **Abre una terminal.**
   - Windows: abre **PowerShell**.
   - macOS o Linux: abre la **Terminal**.

2. **Ejecuta el comando de tu sistema.** Este ejemplo instala Bookify para **Claude Code**.

   Windows (PowerShell):

   ```powershell
   irm https://raw.githubusercontent.com/devjoi2018/bookify/main/bookify/install.py | python - --tool claude
   ```

   macOS o Linux:

   ```bash
   curl -fsSL https://raw.githubusercontent.com/devjoi2018/bookify/main/bookify/install.py | python3 - --tool claude
   ```

3. **Si usas otra herramienta, cambia `claude`** al final del comando:

   | Herramienta | Valor de `--tool` |
   |---|---|
   | Claude Code | `claude` |
   | Command Code CLI | `commandcode` |
   | OpenCode | `opencode` |
   | GitHub Copilot en VS Code | `copilot` |
   | Varias a la vez | `claude,copilot` |
   | Todas | `all` |

4. **Reinicia tu herramienta** o abre una sesión nueva, para que encuentre la skill.

Listo.

<details>
<summary><b>Instalar solo en un proyecto</b></summary>

Por defecto, Bookify se instala para tu usuario y funciona en todos tus proyectos. Para instalarlo
solo en la carpeta actual, añade `--project` al final del comando:

```powershell
irm https://raw.githubusercontent.com/devjoi2018/bookify/main/bookify/install.py | python - --tool claude --project
```

</details>

<details>
<summary><b>Dónde se guardan los archivos</b></summary>

| Herramienta | Para tu usuario | Para un proyecto (`--project`) |
|---|---|---|
| Claude Code | `~/.claude/skills/bookify` | `.claude/skills/bookify` |
| Command Code CLI | `~/.commandcode/skills/bookify` | `.commandcode/skills/bookify` |
| OpenCode | `~/.config/opencode/skills/bookify` | `.opencode/skills/bookify` |
| GitHub Copilot en VS Code | `~/.copilot/skills/bookify` | `.github/skills/bookify` |

</details>

## Uso

1. **Investiga tu tema.** Habla con tu asistente como siempre: pregunta, compara, busca.

2. **Pide el libro.** Escribe *"convierte esto en libro"* o usa el comando de tu herramienta:

   | Herramienta | Comando |
   |---|---|
   | Claude Code, Command Code | `/bookify` |
   | GitHub Copilot | `/bookify` (en el chat, en modo **Agent**) |
   | OpenCode | `@bookify` |

   También puedes empezar directo con un tema:

   ```text
   /bookify cómo funciona el pan de masa madre
   ```

3. **Espera a que termine.** El asistente escribe el libro, hace los dibujos, lo construye y lo revisa.

4. **Abre tu libro.** Lo encuentras en la carpeta donde trabajas. Haz doble clic en el `.html`:

   ```text
   output/
   └── <Título de tu libro>.html   ← el libro terminado, listo para compartir
   books/
   └── <Nombre>/
       ├── content.json            ← el texto del libro
       └── images/                 ← los dibujos
   ```

5. **Ajusta lo que quieras.** Pídeselo a tu asistente, por ejemplo: *"haz más corto el capítulo 2"*
   o *"añade una página sobre los costos"*. Él actualiza el libro y lo vuelve a construir.

## Actualizar

1. Escribe en tu asistente:

   ```text
   /bookify update
   ```

2. Bookify busca en GitHub si hay una versión nueva.
3. Si la hay, la instala en **todas** las herramientas donde lo tienes. Tus libros no se tocan.

<details>
<summary><b>Actualizar desde la terminal</b></summary>

Ejecuta el instalador que viene con la skill. La ruta depende de tu herramienta (mira
[Dónde se guardan los archivos](#instalación)). Para Claude Code:

```bash
python ~/.claude/skills/bookify/install.py --update
```

Para solo comprobar si hay una versión nueva, sin instalarla, usa `--check`.

</details>

## Desinstalar

Ejecuta esto en una terminal, cambiando `claude` por tu herramienta:

```bash
python ~/.claude/skills/bookify/install.py --uninstall --tool claude
```

Tus libros se quedan donde están.

## Referencia de comandos

### Comandos de la skill

Úsalos dentro de tu asistente (`/bookify …` o `@bookify …`):

| Comando | Qué hace |
|---|---|
| `/bookify` | Convierte la conversación actual en un libro |
| `/bookify <tema>` | Escribe un libro sobre un tema |
| `/bookify build <nombre>` | Vuelve a construir un libro después de editarlo |
| `/bookify build all` | Vuelve a construir todos los libros de la carpeta |
| `/bookify list` | Muestra tus libros |
| `/bookify version` | Muestra la versión instalada |
| `/bookify update` | Actualiza Bookify a la última versión |

### Opciones del instalador

Úsalas con `install.py`:

| Opción | Qué hace |
|---|---|
| `--tool <nombre>` | Herramienta donde instalar: `claude`, `commandcode`, `opencode`, `copilot`, varias separadas por comas, o `all` |
| `--project [carpeta]` | Instala en un proyecto en lugar de para tu usuario (por defecto, la carpeta actual) |
| `--update` | Actualiza todas las instalaciones a la última versión |
| `--check` | Solo comprueba si hay una versión nueva |
| `--list` | Muestra dónde está instalado Bookify |
| `--uninstall` | Quita Bookify de la herramienta indicada con `--tool` |
| `--version <x.y.z>` | Instala una versión concreta |
| `--force` | Reinstala aunque la versión sea la misma |

## Usarlo sin asistente

También puedes escribir el contenido tú y construir el libro desde la terminal.

1. Crea un libro nuevo:

   ```bash
   python bookify/engine/build.py --new "Mi libro" --type explainer --lang es
   ```

   Tipos de libro: `guide`, `manual`, `story`, `explainer`, `research`, `other`.

2. Edita `books/Mi libro/content.json`. El formato se explica en [`bookify/format.md`](bookify/format.md).

3. Constrúyelo:

   ```bash
   python bookify/engine/build.py "Mi libro"
   ```

4. Abre `output/Mi libro.html`. Para comprobar que todas las páginas caben, añade `?check` al final
   de la dirección en el navegador.

## Estructura del proyecto

```text
bookify/                 ← la skill (es lo que se instala)
├── SKILL.md             ← instrucciones para el asistente
├── style.md             ← tono de escritura
├── structures.md        ← estructura de cada tipo de libro
├── format.md            ← formato del contenido (content.json)
├── review.md            ← lista de revisión
├── install.py           ← instalador y actualizador
├── version.json         ← versión actual
└── engine/
    ├── build.py         ← convierte content.json en un libro HTML
    └── template/        ← diseño: HTML, CSS, JS e iconos (ver DESIGN.md)
examples/                ← un libro de muestra que explica Bookify, en inglés y en español
docs/demo.gif            ← la animación del principio de esta página
docs/logo.svg            ← el logo del proyecto
```

## Licencia

Publicado bajo la [licencia MIT](LICENSE). Puedes usarlo, copiarlo, cambiarlo y compartirlo gratis,
también con fines comerciales.
