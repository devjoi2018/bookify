<div align="center">

# 📖 Bookify

**Turn what you research with your AI into a clear, illustrated, easy-to-read book.**

**English** · [Español](README.es.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-3949D6.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-3949D6.svg)](https://www.python.org/downloads/)
[![Latest release](https://img.shields.io/github/v/release/devjoi2018/bookify?color=FF6B4F)](https://github.com/devjoi2018/bookify/releases)
[![No dependencies](https://img.shields.io/badge/dependencies-none-BFE6D5.svg)](#requirements)

<img src="docs/demo.gif" alt="Turning the pages of Bookify step by step, a sample book made with Bookify" width="760">

</div>

---

Bookify is a *skill* for your AI assistant. It takes what you researched in a conversation and
turns it into a short, illustrated, well-explained digital book.

It helps you do two things:

- **Understand** what you researched.
- **Share it** in a way people actually want to read.

It works inside Claude Code, Command Code, OpenCode and GitHub Copilot.

## Table of contents

- [The problem](#the-problem)
- [The usual fix](#the-usual-fix)
- [What Bookify does](#what-bookify-does)
- [What you can use it for](#what-you-can-use-it-for)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Updating](#updating)
- [Uninstalling](#uninstalling)
- [Command reference](#command-reference)
- [Using it without an assistant](#using-it-without-an-assistant)
- [Project structure](#project-structure)
- [License](#license)

## The problem

Researching with an AI is fast. Reading what it writes is not.

- **It writes a lot.** Long answers, with paragraphs that say the same thing in different words.
- **The ideas get lost.** The important part is buried under lists, caveats and side notes.
- **It sounds generic.** The text has that filler tone you spot right away: the famous *AI slop*.
- **It's hard to share.** Nobody wants to open a wall of text copied from a chat.

You end up with a lot of information, but you don't always understand it better than before.

## The usual fix

The usual move is to ask the AI to explain it again:

> *"Explain it more simply."*
> *"Shorter."*
> *"Now without the filler."*
> *"Give me an example."*

It works, but it takes several rounds. And every new topic, you start from scratch.

## What Bookify does

Bookify gives your assistant a fixed set of rules for writing and design. Instead of you iterating
by hand, the assistant already knows what the result should look like:

- **One idea per page.** No endless blocks of text.
- **Short sentences and plain language.** No filler, no stock phrases.
- **Examples and drawings** where they help you understand.
- **Sources at the end** for the facts that need them.
- **A review before it's delivered** that checks every page: one idea only, no unexplained jargon, no pages that run too long.

The result is a book with a clean, professional design, in a single `.html` file:

- Opens in any browser, nothing to install.
- Reads well on a phone (one page) and on a computer (two pages).
- You turn the pages like a real book.
- Share it by email, chat or cloud drive.
- Written in the language you use with your assistant.

> [!NOTE]
> Bookify doesn't make up information: it works with what you researched. If the conversation has
> doubtful facts, the book will too. Always check the sources for anything important.

## What you can use it for

A few ideas:

- **Your personal library.** Save each piece of research as a book and come back to it when you need it.
- **Explaining something to your team.** A short guide instead of a long document.
- **Learning a new topic.** Ask for the book to review what you just researched.
- **Sharing with people who don't use AI.** A file anyone can open and understand.

It works for guides, manuals, stories, explainers, research summaries, or anything else.

## Requirements

- [Python 3.9 or newer](https://www.python.org/downloads/)
- One of these tools: [Claude Code](https://claude.com/claude-code), [Command Code CLI](https://commandcode.ai), [OpenCode](https://opencode.ai) or [GitHub Copilot in VS Code](https://github.com/features/copilot)

## Installation

1. **Open a terminal.**
   - Windows: open **PowerShell**.
   - macOS or Linux: open **Terminal**.

2. **Run the command for your system.** This example installs Bookify for **Claude Code**.

   Windows (PowerShell):

   ```powershell
   irm https://raw.githubusercontent.com/devjoi2018/bookify/main/bookify/install.py | python - --tool claude
   ```

   macOS or Linux:

   ```bash
   curl -fsSL https://raw.githubusercontent.com/devjoi2018/bookify/main/bookify/install.py | python3 - --tool claude
   ```

3. **If you use a different tool, change `claude`** at the end of the command:

   | Tool | `--tool` value |
   |---|---|
   | Claude Code | `claude` |
   | Command Code CLI | `commandcode` |
   | OpenCode | `opencode` |
   | GitHub Copilot in VS Code | `copilot` |
   | Several at once | `claude,copilot` |
   | All of them | `all` |

4. **Restart your tool** or start a new session, so it finds the skill.

That's it. 🎉

<details>
<summary><b>Install for one project only</b></summary>

By default, Bookify is installed for your user, so it works in every project. To install it only
in the current folder, add `--project` at the end of the command:

```powershell
irm https://raw.githubusercontent.com/devjoi2018/bookify/main/bookify/install.py | python - --tool claude --project
```

</details>

<details>
<summary><b>Where the files go</b></summary>

| Tool | For your user | For one project (`--project`) |
|---|---|---|
| Claude Code | `~/.claude/skills/bookify` | `.claude/skills/bookify` |
| Command Code CLI | `~/.commandcode/skills/bookify` | `.commandcode/skills/bookify` |
| OpenCode | `~/.config/opencode/skills/bookify` | `.opencode/skills/bookify` |
| GitHub Copilot in VS Code | `~/.copilot/skills/bookify` | `.github/skills/bookify` |

</details>

## Usage

1. **Research your topic.** Talk with your assistant as usual: ask, compare, look things up.

2. **Ask for the book.** Write *"turn this into a book"*, or use the command for your tool:

   | Tool | Command |
   |---|---|
   | Claude Code, Command Code | `/bookify` |
   | GitHub Copilot | `/bookify` (in the chat, in **Agent** mode) |
   | OpenCode | `@bookify` |

   You can also start straight from a topic:

   ```text
   /bookify how sourdough bread works
   ```

3. **Wait for it to finish.** The assistant writes the book, draws the pictures, builds it and reviews it.

4. **Open your book.** You'll find it in the folder you're working in. Double-click the `.html` file:

   ```text
   output/
   └── <Your book title>.html   ← the finished book, ready to share
   books/
   └── <Name>/
       ├── content.json         ← the text of the book
       └── images/              ← the drawings
   ```

5. **Adjust anything you want.** Ask your assistant, for example: *"make chapter 2 shorter"* or
   *"add a page about costs"*. It updates the book and builds it again.

## Updating

1. Write in your assistant:

   ```text
   /bookify update
   ```

2. Bookify checks GitHub for a new version.
3. If there is one, it installs it in **every** tool where you have it. Your books are never changed.

<details>
<summary><b>Update from the terminal</b></summary>

Run the installer that came with the skill. The path depends on your tool (see
[Where the files go](#installation)). For Claude Code:

```bash
python ~/.claude/skills/bookify/install.py --update
```

To only check if there is a new version, without installing it, use `--check`.

</details>

## Uninstalling

Run this in a terminal, changing `claude` to your tool:

```bash
python ~/.claude/skills/bookify/install.py --uninstall --tool claude
```

Your books stay where they are.

## Command reference

### Skill commands

Use these inside your assistant (`/bookify …` or `@bookify …`):

| Command | What it does |
|---|---|
| `/bookify` | Turns the current conversation into a book |
| `/bookify <topic>` | Writes a book about a topic |
| `/bookify build <name>` | Rebuilds one book after you edit it |
| `/bookify build all` | Rebuilds every book in the folder |
| `/bookify list` | Lists your books |
| `/bookify version` | Shows the installed version |
| `/bookify update` | Updates Bookify to the latest release |

### Installer options

Use these with `install.py`:

| Option | What it does |
|---|---|
| `--tool <name>` | Tool to install for: `claude`, `commandcode`, `opencode`, `copilot`, several separated by commas, or `all` |
| `--project [folder]` | Installs in a project instead of for your user (current folder by default) |
| `--update` | Updates every install to the latest release |
| `--check` | Only checks whether a new version exists |
| `--list` | Shows where Bookify is installed |
| `--uninstall` | Removes Bookify from the tool given with `--tool` |
| `--version <x.y.z>` | Installs a specific release |
| `--force` | Reinstalls even if the version is the same |

## Using it without an assistant

You can also write the content yourself and build the book from the terminal.

1. Create a new book:

   ```bash
   python bookify/engine/build.py --new "My book" --type explainer --lang en
   ```

   Book types: `guide`, `manual`, `story`, `explainer`, `research`, `other`.

2. Edit `books/My book/content.json`. The format is explained in [`bookify/format.md`](bookify/format.md).

3. Build it:

   ```bash
   python bookify/engine/build.py "My book"
   ```

4. Open `output/My book.html`. To check that every page fits, add `?check` to the end of the
   address in your browser.

## Project structure

```text
bookify/                 ← the skill (this is what gets installed)
├── SKILL.md             ← instructions for the assistant
├── style.md             ← writing tone
├── structures.md        ← structure for each type of book
├── format.md            ← content format (content.json)
├── review.md            ← review checklist
├── install.py           ← installer and updater
├── version.json         ← current version
└── engine/
    ├── build.py         ← turns content.json into an HTML book
    └── template/        ← design: HTML, CSS, JS and icons (see DESIGN.md)
examples/                ← a sample book that explains Bookify, in English and Spanish
docs/demo.gif            ← the animation at the top of this page
```

> [!NOTE]
> The instructions for the assistant are written in Spanish. That doesn't affect you: the book is
> always written in your language.

## License

Released under the [MIT License](LICENSE). You can use, copy, change and share it for free, also for
commercial purposes.
