# Bookify

**English** · [Español](README.es.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-3949D6.svg)](LICENSE)

Turn whatever you researched with your AI assistant (or any topic) into an **illustrated digital
book** that is easy to read and share. One idea per page, simple drawings, animated page turns,
and always the same design and tone.

Each book is **a single HTML file**: it opens in any browser and shows one page on a phone and two
pages on a computer. You can send it by email, WhatsApp or Drive.

It works for any content: a guide, a manual, a story, an explainer, the results of some research,
or anything else. The book is written in the language you use with your assistant.

## Supported tools

Bookify is a standard `SKILL.md` skill, so it works in:

| Tool | `--tool` | Installed in (global) | With `--project` |
|---|---|---|---|
| Claude Code | `claude` | `~/.claude/skills/bookify` | `.claude/skills/bookify` |
| Command Code CLI | `commandcode` | `~/.commandcode/skills/bookify` | `.commandcode/skills/bookify` |
| OpenCode | `opencode` | `~/.config/opencode/skills/bookify` | `.opencode/skills/bookify` |
| GitHub Copilot in VS Code | `copilot` | `~/.copilot/skills/bookify` | `.github/skills/bookify` |

**Requirement:** Python 3.9 or newer ([python.org](https://www.python.org/downloads/)). No packages
are installed.

## Install (one command)

Replace `claude` with the tool you use (`commandcode`, `opencode`, `copilot`, several separated by
commas such as `claude,opencode`, or `all`).

Windows (PowerShell):

```powershell
irm https://raw.githubusercontent.com/devjoi2018/bookify/main/bookify/install.py | python - --tool claude
```

macOS or Linux:

```bash
curl -fsSL https://raw.githubusercontent.com/devjoi2018/bookify/main/bookify/install.py | python3 - --tool claude
```

It downloads the latest release of this repository and copies the skill into that tool's skills
folder. To install it for a single project, add `--project` (it uses the current folder). Then
restart the tool or open a new session.

## Use

Research whatever you want with your assistant, then ask it to **"turn this into a book"**, or use
the command:

| Tool | How |
|---|---|
| Claude Code, Command Code | `/bookify` (what was researched in the conversation) or `/bookify <topic>` |
| GitHub Copilot | in agent mode chat: `/bookify <topic>` |
| OpenCode | ask "turn this into a book" or type `@bookify` |

Other arguments: `build [name|all]`, `list`, `version` and `update`.

Books are saved in the folder you are working in:
- `books/<Name>/`: the content (`content.json`) and the drawings (`images/`). To change a book, ask your assistant.
- `output/<Title>.html`: the finished book, ready to share. To check that everything fits, open it with `?check` at the end of the address.

## Update

Use `update` as the argument (`/bookify update`) or, from a terminal:

```powershell
python ~/.claude/skills/bookify/install.py --update
```

(Change the path to your tool's, as in the table above.) It compares your version with the latest
GitHub release and, if there is a new one, updates the skill in **every** tool where you installed
it. Your books are not touched.

Other installer options: `--check` (only report whether there is a new version), `--list` (where
it is installed), `--uninstall --tool X`, `--version 1.2.0` (a specific release).

## What's in this repository

- `bookify/`: the complete skill, which is what gets installed.
  - `SKILL.md`: instructions for the assistant.
  - `style.md`, `structures.md`, `format.md`, `review.md`: tone, structure by book type, content format and review.
  - `engine/build.py` and `engine/template/`: the builder and the design (`DESIGN.md` documents the visual identity).
  - `install.py`: installer and updater.
  - `version.json`: version and repository.
- `examples/`: a sample book with its drawings.

The prompts (`SKILL.md` and the files it references) are written in Spanish; the assistant writes
each book in the user's language.

## Without an assistant

```powershell
python bookify/engine/build.py --new "My book" --type explainer --lang en
```

Then edit `books/My book/content.json` (the format is in `bookify/format.md`) and build:

```powershell
python bookify/engine/build.py "My book"
```

## License

[MIT](LICENSE): free to use, copy, modify and distribute, including for commercial purposes.
