# Bookify

[English](README.md) · **Español**

Convierte lo que investigaste con tu asistente de IA (o cualquier tema) en un **libro digital
ilustrado**, fácil de leer y de compartir. Una idea por página, dibujos simples, paso de página
animado y siempre el mismo diseño y el mismo tono.

Cada libro es **un solo archivo HTML**: se abre en cualquier navegador y se ve en el celular (una
página) y en la computadora (dos páginas). Lo puedes mandar por correo, WhatsApp o Drive.

Sirve para cualquier contenido: una guía, un manual, una historia, la explicación de una idea, el
resultado de una investigación o lo que haga falta. El libro sale en el idioma en que hablas con
el asistente.

## Herramientas compatibles

Es una *skill* con el formato estándar `SKILL.md`, así que funciona en:

| Herramienta | `--tool` | Se instala en (global) | Con `--project` |
|---|---|---|---|
| Claude Code | `claude` | `~/.claude/skills/bookify` | `.claude/skills/bookify` |
| Command Code CLI | `commandcode` | `~/.commandcode/skills/bookify` | `.commandcode/skills/bookify` |
| OpenCode | `opencode` | `~/.config/opencode/skills/bookify` | `.opencode/skills/bookify` |
| GitHub Copilot en VS Code | `copilot` | `~/.copilot/skills/bookify` | `.github/skills/bookify` |

**Requisito:** Python 3.9 o superior ([python.org](https://www.python.org/downloads/)). No se
instala ningún paquete.

## Instalar (un comando)

Cambia `claude` por la herramienta que uses (`commandcode`, `opencode`, `copilot`, varias
separadas por comas como `claude,opencode`, o `all`).

Windows (PowerShell):

```powershell
irm https://raw.githubusercontent.com/devjoi2018/bookify/main/bookify/install.py | python - --tool claude
```

macOS o Linux:

```bash
curl -fsSL https://raw.githubusercontent.com/devjoi2018/bookify/main/bookify/install.py | python3 - --tool claude
```

Descarga el último release de este repositorio y copia la skill en la carpeta de esa herramienta.
Para instalarla solo en un proyecto, añade `--project` (usa la carpeta actual). Después reinicia la
herramienta o abre una sesión nueva.

## Usar

Investiga lo que quieras con tu asistente y luego pide **"convierte esto en libro"**, o usa el
comando:

| Herramienta | Cómo |
|---|---|
| Claude Code, Command Code | `/bookify` (lo investigado en la conversación) o `/bookify <tema>` |
| GitHub Copilot | en el chat en modo agente: `/bookify <tema>` |
| OpenCode | pide "convierte esto en libro" o escribe `@bookify` |

Otros argumentos: `build [nombre|all]`, `list`, `version` y `update`.

Los libros se guardan en la carpeta donde trabajas:
- `books/<Name>/`: el contenido (`content.json`) y los dibujos (`images/`). Para cambiar un libro, pídeselo al asistente.
- `output/<Title>.html`: el libro terminado, listo para compartir. Para comprobar que todo cabe, ábrelo con `?check` al final de la dirección.

## Actualizar

Usa `update` como argumento (`/bookify update`) o, desde una terminal:

```powershell
python ~/.claude/skills/bookify/install.py --update
```

(Cambia la ruta por la de tu herramienta, según la tabla de arriba.) Compara tu versión con el
último release de GitHub y, si hay uno nuevo, actualiza la skill en **todas** las herramientas
donde la instalaste. Tus libros no se tocan.

Otras opciones del instalador: `--check` (solo mira si hay versión nueva), `--list` (dónde está
instalada), `--uninstall --tool X`, `--version 1.2.0` (un release concreto).

## Qué hay en este repositorio

- `bookify/`: la skill completa, que es lo que se instala.
  - `SKILL.md`: instrucciones para el asistente.
  - `style.md`, `structures.md`, `format.md`, `review.md`: tono, estructura por tipo de libro, formato del contenido y revisión.
  - `engine/build.py` y `engine/template/`: el constructor y el diseño (`DESIGN.md` documenta el sello visual).
  - `install.py`: instalador y actualizador.
  - `version.json`: versión y repositorio.
- `examples/`: un libro de muestra con sus dibujos.

## Sin asistente

```powershell
python bookify/engine/build.py --new "Mi libro" --type explainer --lang es
```

Después edita `books/Mi libro/content.json` (el formato está en `bookify/format.md`) y construye:

```powershell
python bookify/engine/build.py "Mi libro"
```

## Licencia

[MIT](LICENSE): libre y gratis para usar, copiar, modificar y distribuir, también con fines comerciales.
