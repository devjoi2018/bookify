#!/usr/bin/env python3
"""
Bookify book builder.

Uses only the Python standard library (3.9 or newer). Installs nothing.

Works on the current folder (or the one given with --dir DIR), which holds
books/<Name>/content.json and receives the result in output/<Title>.html:
    python build.py "Name"                  build books/Name -> output/<Title>.html
    python build.py --all                   build every book
    python build.py --new "Name" [--type TYPE] [--lang es]
                                            TYPE: guide, manual, story, explainer, research, other
    python build.py --list                  list the books
    python build.py --version               installed version
    (to look for new versions: python ../install.py --update)

While building, it estimates which pages might overflow (a rough, cautious guess).
For the exact check, open the book in a browser with ?check at the end of the
address (for example: output/My book.html?check).
"""
import html, json, re, sys
from pathlib import Path

# The Windows console does not always use UTF-8: avoid errors with accents and symbols
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ENGINE = Path(__file__).resolve().parent
TEMPLATE = ENGINE / "template"
VERSION_FILE = ENGINE.parent / "version.json"   # installed version and GitHub repository
# Working folder: the one of the person writing books, not the skill's (see use_dir)
ROOT = Path.cwd()
BOOKS = ROOT / "books"
OUTPUT = ROOT / "output"
TOC_ENTRIES_PER_PAGE = 14
COLORS = {"indigo", "coral", "mint"}


def use_dir(path):
    global ROOT, BOOKS, OUTPUT
    ROOT = Path(path).resolve()
    BOOKS, OUTPUT = ROOT / "books", ROOT / "output"


def relative(p):
    try:
        return p.relative_to(ROOT)
    except ValueError:
        return p


class Error(Exception):
    pass


# ---------- reader interface strings, by book language ----------
UI = {
    "es": {"cover": "Portada", "end": "Fin", "contents": "Índice", "go_contents": "Ir al índice",
           "previous": "Página anterior", "next": "Página siguiente", "navigation": "Navegación del libro",
           "example": "Por ejemplo:", "check": "Revisión:", "all_fit": "todas las páginas caben.",
           "one_overflows": "No cabe 1 página:", "n_overflow": "No caben {n} páginas:", "page_abbr": "p."},
    "en": {"cover": "Cover", "end": "End", "contents": "Contents", "go_contents": "Go to contents",
           "previous": "Previous page", "next": "Next page", "navigation": "Book navigation",
           "example": "For example:", "check": "Check:", "all_fit": "every page fits.",
           "one_overflows": "1 page does not fit:", "n_overflow": "{n} pages do not fit:", "page_abbr": "p."},
    "pt": {"cover": "Capa", "end": "Fim", "contents": "Índice", "go_contents": "Ir para o índice",
           "previous": "Página anterior", "next": "Próxima página", "navigation": "Navegação do livro",
           "example": "Por exemplo:", "check": "Revisão:", "all_fit": "todas as páginas cabem.",
           "one_overflows": "1 página não cabe:", "n_overflow": "{n} páginas não cabem:", "page_abbr": "p."},
}


def ui_strings(data):
    """Reader strings in the book's language; the JSON's "ui" covers other languages."""
    lang = str(data.get("language", "en")).lower()
    base = dict(UI.get(lang.split("-")[0], UI["en"]))
    base.update(data.get("ui", {}))
    return lang, base


# ---------- light inline formatting ----------
def md(s):
    """**bold**  __underlined term__  *italic*  `code`  [[Key]]  ==highlight==  [text](url)"""
    if s is None:
        return ""
    s = html.escape(str(s), quote=False)
    guard = []
    def keep(x):
        guard.append(x)
        return f"\x00{len(guard)-1}\x00"
    s = re.sub(r"`([^`]+)`", lambda m: keep(f"<code>{m.group(1)}</code>"), s)
    s = re.sub(r"\[\[([^\]]+)\]\]", lambda m: keep(f"<kbd>{m.group(1)}</kbd>"), s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", lambda m: keep(f'<a href="{m.group(2)}" target="_blank" rel="noopener">{m.group(1)}</a>'), s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"__(.+?)__", r"<u>\1</u>", s)
    s = re.sub(r"==(.+?)==", r"<em>\1</em>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
    s = s.replace("\n", "<br>")
    return re.sub(r"\x00(\d+)\x00", lambda m: guard[int(m.group(1))], s)


def paragraphs(s, cls=""):
    c = f' class="{cls}"' if cls else ""
    return "".join(f"<p{c}>{md(p.strip())}</p>" for p in re.split(r"\n\s*\n", str(s)) if p.strip())


# ---------- illustrations ----------
class Art:
    def __init__(self, book):
        self.dirs = [book / "images", TEMPLATE / "icons"]

    def svg(self, name, cls="art"):
        if not name:
            return ""
        if not name.endswith(".svg"):
            name += ".svg"
        for d in self.dirs:
            f = d / name
            if f.exists():
                t = f.read_text(encoding="utf-8")
                t = re.sub(r"<\?xml.*?\?>|<!DOCTYPE.*?>|<!--.*?-->", "", t, flags=re.S).strip()
                if not t.startswith("<svg"):
                    raise Error(f"{name} does not start with <svg>")
                return t.replace("<svg", f'<svg class="{cls}" aria-hidden="true"', 1)
        raise Error(f"Illustration '{name}' not found in images/ or in the template icons")


# ---------- blocks ----------
def block(b, art, ui):
    t = b.get("type")
    if t == "illustration":
        return art.svg(b["src"], f"art illus {b.get('size', 'm')}")
    if t == "heading":
        return f'<h2 class="h-{b.get("level", 1)}">{md(b["text"])}</h2>'
    if t == "question":
        return f'<p class="question"><span>{md(b["light"])}</span><strong>{md(b["bold"])}</strong></p>'
    if t == "text":
        return f'<div class="{"center" if b.get("align") == "center" else ""}">{paragraphs(b["text"])}</div>'
    if t == "highlight":
        return paragraphs(b["text"], "highlight" + (" center" if b.get("align") == "center" else ""))
    if t == "footnote":
        return paragraphs(b["text"], "footnote")
    if t == "note":
        label = b.get("label", ui["example"])
        return f'<div class="note"><div class="label"><svg><use href="#spark"/></svg>{md(label)}</div>{md(b["text"])}</div>'
    if t == "list":
        tag = "ol" if b.get("ordered") else "ul"
        start = f' start="{int(b["start"])}"' if b.get("start") else ""
        return f'<{tag} class="list"{start}>' + "".join(f"<li>{md(i)}</li>" for i in b["items"]) + f"</{tag}>"
    if t == "table":
        return '<table class="table"><tbody>' + "".join("<tr>" + "".join(f"<td>{md(c)}</td>" for c in r) + "</tr>" for r in b["rows"]) + "</tbody></table>"
    if t == "levels":
        return '<div class="levels">' + "".join(f"<code>{html.escape(a)}</code><span>{md(c)}</span>" for a, c in b["rows"]) + "</div>"
    if t == "facts":
        return '<dl class="facts">' + "".join(f"<dt>{md(a)}</dt><dd>{md(c)}</dd>" for a, c in b["rows"]) + "</dl>"
    if t == "sizes":
        return '<div class="sizes" aria-hidden="true">' + "".join(
            f'<div><i style="width:{i["size"]}px;height:{i["size"]}px;opacity:{i.get("opacity", 1)}"></i>{md(i["name"])}</div>' for i in b["items"]) + "</div>"
    if t == "combine":
        return ('<div class="combine">'
                f'<div class="node"><div class="circle">{art.svg(b["icon"])}</div>{md(b.get("a", ""))}</div>'
                f'<div class="node"><div class="circle accent">{md(b.get("b", ""))}</div>{md(b.get("b_label", ""))}</div>'
                f'<div class="result">{md(b["result"])}</div></div>')
    if t == "columns":
        return '<div class="columns">' + "".join(
            f'<div>{art.svg(c["icon"])}<h4>{md(c["title"])}</h4><p>{md(c["text"])}</p></div>' for c in b["columns"]) + "</div>"
    if t == "myths":
        icon = b.get("icon", "cross")
        return "".join(f'<div class="myth"><svg><use href="#{icon}"/></svg><s>{md(a)}</s><span>{md(c)}</span></div>' for a, c in b["items"])
    if t == "sources":
        return '<ul class="sources">' + "".join(f'<li><a href="{html.escape(u)}" target="_blank" rel="noopener">{md(n)}</a></li>' for n, u in b["items"]) + "</ul>"
    if t == "space":
        return f'<div style="height:{int(b.get("height", 16))}px"></div>'
    if t == "html":
        return b["html"]  # escape hatch: raw HTML
    raise Error(f"Unknown block type: '{t}'")


# ---------- height estimate (no browser) ----------
# Logical page size (see template/book.css). The character-width constants are calibrated
# with a wider font than the real one, so the estimate errs on the safe side.
USABLE_HEIGHT = 660 - 58 - 66   # height available for content
WIDTH = 440 - 46 * 2            # text column width
WARN = 0.97                     # "check": might just fit
ALERT = 1.15                    # "overflows": almost surely too long (the estimate usually runs 5-30 % high)


def _plain(s):
    s = re.sub(r"\[\[([^\]]+)\]\]", r" \1 ", str(s or ""))
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    return re.sub(r"[*_=`]", "", s)


def _lines(text, char_width, width=WIDTH):
    per_line = max(1, int(width / char_width))
    total = 0
    for part in str(text).split("\n"):
        words, line, n = _plain(part).split(), 0, 1
        for w in words:
            l = len(w) + (1 if line else 0)
            if line + l > per_line:
                n, line = n + 1, len(w)
            else:
                line += l
        total += n
    return total


def _ratio(art, name):
    try:
        t = art.svg(name)
        m = re.search(r'viewBox="\s*[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)', t)
        return float(m.group(2)) / float(m.group(1)) if m else 1.0
    except Error:
        return 1.0


def estimate_block(b, art):
    t = b.get("type")
    if t == "illustration":
        width = {"s": 84, "m": 120}.get(b.get("size", "m"), 330)
        return width * _ratio(art, b["src"]) + 22
    if t == "heading":
        if b.get("level", 1) == 1:
            return _lines(b["text"], 20.5) * 37.4 + 25.5
        return _lines(b["text"], 15.2) * 27.5 + 18.8
    if t == "question":
        return (_lines(b["light"], 17) + _lines(b["bold"], 20)) * 38 + 26.4
    if t in ("text", "footnote", "highlight"):
        cfg = {"text": (8.4, 26.4, 15.7), "footnote": (7.0, 21.6, 12.8), "highlight": (10.2, 29, 18)}[t]
        paras = [x for x in re.split(r"\n\s*\n", str(b["text"])) if x.strip()]
        return sum(_lines(x, cfg[0]) * cfg[1] + cfg[2] for x in paras)
    if t == "note":
        return 22 + 31 + _lines(b["text"], 9.2, 330) * 24.7
    if t == "list":
        return sum(_lines(i, 8.4, WIDTH - 19) * 26.4 + 8.3 for i in b["items"]) + 15
    if t == "table":
        return sum(max(_lines(r[-1], 7.6, WIDTH * 0.62), _lines(r[0], 7.6, WIDTH * 0.38)) * 21 + 17 for r in b["rows"]) + 12
    if t == "levels":
        return sum(_lines(c, 8.0, WIDTH - 70) * 21.7 + 10 for _, c in b["rows"])
    if t == "facts":
        return 18 + sum(_lines(v, 7.6, WIDTH - 100) * 21 + 5 for _, v in b["rows"])
    if t == "sizes":
        return max(i["size"] for i in b["items"]) + 11 + 21 + 26
    if t == "combine":
        return 80 + 8 + max(_lines(b.get("a", ""), 7.6, 150), 1) * 17 + 78 + 28
    if t == "columns":
        return 28 + 44 + 8 + 30 + max(_lines(c["text"], 7.4, 135) for c in b["columns"]) * 19.6 + 8
    if t == "myths":
        return sum(2 + _lines(a, 9.0, WIDTH - 38) * 22 + _lines(c, 7.6, WIDTH - 38) * 21 + 15 for a, c in b["items"])
    if t == "sources":
        return sum(_lines(n, 7.6, WIDTH - 16) * 21 + 8.7 for n, _ in b["items"])
    if t == "space":
        return int(b.get("height", 16))
    return 0


def estimate_page(p, art):
    return sum(estimate_block(b, art) for b in p.get("blocks", []))


# ---------- pages ----------
def book_dir(name):
    path = Path(name)
    if path.is_absolute():
        return path
    for c in (BOOKS / name, ROOT / name):
        if (c / "content.json").exists():
            return c
    return BOOKS / name


def build(book_name):
    book = book_dir(book_name)
    source = book / "content.json"
    if not source.exists():
        raise Error(f"{source} does not exist")
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise Error(f"content.json is not valid JSON (line {e.lineno}, column {e.colno}): {e.msg}")
    art = Art(book)
    title = data.get("title", book.name)
    lang, ui = ui_strings(data)

    # 1) Expand: the table of contents takes as many pages as it needs
    raw = data["pages"]
    entries = []
    for p in raw:
        if p["type"] == "chapter" and p.get("toc", True):
            entries.append(("", p["title"], p))
        elif p["type"] == "page" and p.get("toc"):
            entries.append(("" if p.get("toc_main") else "sub", p["toc"], p))
    pages = []
    for p in raw:
        if p["type"] == "contents":
            chunks = [entries[i:i + TOC_ENTRIES_PER_PAGE] for i in range(0, len(entries), TOC_ENTRIES_PER_PAGE)] or [[]]
            for k, ch in enumerate(chunks):
                pages.append({"type": "_contents", "title": p.get("title", ui["contents"]) if k == 0 else "", "entries": ch,
                              "illustration": p.get("illustration") if k == 0 else None, "id": "contents" if k == 0 else ""})
        else:
            pages.append(p)
    # 2) Even page count so the back cover closes the book
    if len(pages) % 2 == 1:
        pos = len(pages) - 1 if pages[-1]["type"] == "back-cover" else len(pages)
        pages.insert(pos, {"type": "_blank"})
    # 3) Ids and numbers
    ids, refs = {}, [e[2] for e in entries]
    for n, p in enumerate(pages):
        p["_n"] = n
        if p.get("type") in ("chapter", "page") and not p.get("id") and any(p is r for r in refs):
            p["id"] = "s" + str(n)
        if p.get("id"):
            if p["id"] in ids:
                raise Error(f"Duplicate id: {p['id']}")
            ids[p["id"]] = n

    # 4) Render and estimate
    out, warnings = [], []
    for p in pages:
        n, t = p["_n"], p["type"]
        pid = f' id="{p["id"]}"' if p.get("id") else ""
        folio = f'<div class="folio">{n}</div>'
        if t == "cover":
            lines = p["title"] if isinstance(p["title"], list) else [p["title"]]
            footer = p.get("footer", [])
            footer = footer if isinstance(footer, list) else [footer]
            # Top left: what kind of book it is ("Guide", "Story"…). No series or numbering.
            label = p.get("label") or type_label(data.get("type"), lang)
            label = f'<p class="cover-label">{md(label)}</p>' if label else ""
            out.append(f'<section class="page bleed cover"{pid} data-n="">'
                       f'<div class="disc">{art.svg(p.get("illustration") or "cover-base", "art illus")}</div>'
                       f'{label}'
                       f'<div class="cover-block">{"".join(f"<h1 class=cover-title>{md(x)}</h1>" for x in lines)}'
                       f'<p class="cover-subtitle">{md(p.get("subtitle", ""))}</p>'
                       f'<p class="cover-footer">{"".join(f"<span>{md(x)}</span>" for x in footer)}</p></div></section>')
        elif t == "_contents":
            items = [f'<li class="{cls}"><a href="#{ref["id"]}">{md(txt)}<span class="num">{ref["_n"]}</span></a></li>'
                     for cls, txt, ref in p["entries"]]
            head = (art.svg(p["illustration"], "art illus s") if p.get("illustration") else "") + (f'<h2 class="toc-title">{md(p["title"])}</h2>' if p["title"] else "")
            out.append(f'<section class="page top contents"{pid} data-n="{n}">{head}<ul class="toc">{"".join(items)}</ul>{folio}</section>')
        elif t == "chapter":
            c = p.get("color", "mint")
            if c not in COLORS:
                raise Error(f"Invalid chapter color: {c} (use {', '.join(sorted(COLORS))})")
            sub = f'<p class="chapter-subtitle">{md(p["subtitle"])}</p>' if p.get("subtitle") else ""
            ill = art.svg(p["illustration"], "art illus m") if p.get("illustration") else ""
            out.append(f'<section class="page bleed c-{c}"{pid} data-n="{n}">{ill}<h2 class="chapter-title">{md(p["title"])}</h2>{sub}{folio}</section>')
        elif t == "page":
            cls = "page top" if p.get("align") == "top" else "page"
            body = "".join(block(b, art, ui) for b in p.get("blocks", []))
            out.append(f'<section class="{cls}"{pid} data-n="{n}">{body}{folio}</section>')
            height = estimate_page(p, art)
            if height > USABLE_HEIGHT * WARN:
                hint = next((b.get("text") or b.get("light") for b in p.get("blocks", []) if b.get("text") or b.get("light")), "")
                warnings.append((n, round(100 * height / USABLE_HEIGHT), _plain(hint)[:50]))
        elif t == "back-cover":
            ill = art.svg(p.get("illustration"), "art illus") if p.get("illustration") else ""
            out.append(f'<section class="page bleed back-cover"{pid} data-n="">{ill}{paragraphs(p.get("text", ""))}</section>')
        elif t == "_blank":
            out.append('<section class="page blank" data-n=""></section>')
        else:
            raise Error(f"Unknown page type: '{t}'")

    icons = re.sub(r"<\?xml.*?\?>", "", (TEMPLATE / "icons" / "symbols.svg").read_text(encoding="utf-8"))
    base = (TEMPLATE / "book.html").read_text(encoding="utf-8")
    final = (base.replace("{{CSS}}", (TEMPLATE / "book.css").read_text(encoding="utf-8"))
                 .replace("{{JS}}", "const UI = " + json.dumps(ui, ensure_ascii=False) + ";\n"
                          + (TEMPLATE / "book.js").read_text(encoding="utf-8"))
                 .replace("{{ICONS}}", icons)
                 .replace("{{PAGES}}", "\n".join(out))
                 .replace("{{LANG}}", html.escape(lang))
                 .replace("{{DESCRIPTION}}", html.escape(data.get("description", "")))
                 .replace("{{TITLE}}", html.escape(title)))
    final = re.sub(r"\{\{UI\.(\w+)\}\}", lambda m: html.escape(ui.get(m.group(1), "")), final)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    result = OUTPUT / (re.sub(r'[\\/:*?"<>|]', "", title) + ".html")
    result.write_text(final, encoding="utf-8")
    print(f"Done: {relative(result)}  ({len(pages)} pages)")
    if warnings:
        print("Space estimate (cautious; for the exact check open the book with ?check):")
        for n, pct, hint in warnings:
            mark = "⚠ overflows" if pct >= ALERT * 100 else "· check    "
            print(f"  {mark}  page {n}: ~{pct}% of the available height · \"{hint}…\"")
    else:
        print("Estimate: every page fits. Exact check: open the book with ?check.")
    return result


# ---------- new book ----------
# Cover label and starter subtitle by type and language. The type only guides the structure
# (see structures.md): a book can be about anything.
TYPES = {
    "guide":     {"es": ("Guía", "Para entender algo y saber decidir."), "en": ("Guide", "To understand something and decide well."), "pt": ("Guia", "Para entender algo e saber decidir.")},
    "manual":    {"es": ("Manual", "Cómo hacer algo, de principio a fin."), "en": ("Manual", "How to do something, start to finish."), "pt": ("Manual", "Como fazer algo, do início ao fim.")},
    "story":     {"es": ("Historia", "Una historia contada con claridad."), "en": ("Story", "A story told clearly."), "pt": ("História", "Uma história contada com clareza.")},
    "explainer": {"es": ("Explicación", "Una idea compleja, explicada fácil."), "en": ("Explainer", "A complex idea, made simple."), "pt": ("Explicação", "Uma ideia complexa, explicada com simplicidade.")},
    "research":  {"es": ("Investigación", "Lo que se sabe, contado fácil."), "en": ("Research", "What is known, made easy to read."), "pt": ("Pesquisa", "O que se sabe, contado com simplicidade.")},
    "other":     {"es": ("", "De qué va este libro, en una frase."), "en": ("", "What this book is about, in one line."), "pt": ("", "Do que trata este livro, em uma frase.")},
}


def type_label(book_type, lang="en"):
    t = TYPES.get(book_type or "other", TYPES["other"])
    return t.get(str(lang).split("-")[0], t["en"])[0]


def existing_books():
    if not BOOKS.exists():
        return []
    return sorted(d for d in BOOKS.iterdir() if d.is_dir() and (d / "content.json").exists())


def new_book(name, book_type="other", lang="en"):
    """Create books/<name>/ with a starter content.json."""
    if book_type not in TYPES:
        raise Error(f"Unknown type: {book_type} (use {', '.join(TYPES)})")
    book = BOOKS / name
    if (book / "content.json").exists():
        raise Error(f"{book / 'content.json'} already exists")
    (book / "images").mkdir(parents=True, exist_ok=True)
    short = lang.split("-")[0]
    label, subtitle = TYPES[book_type].get(short, TYPES[book_type]["en"])
    ui = UI.get(short, UI["en"])
    sources = {"es": "Fuentes", "pt": "Fontes"}.get(short, "Sources")
    base = {
        "title": name,
        "type": book_type,
        "language": lang,
        "description": "",
        "pages": [
            {"type": "cover", "label": label, "title": [name, "…"], "illustration": "cover-base",
             "subtitle": subtitle, "footer": [""]},
            {"type": "contents", "title": ui["contents"]},
            {"type": "page", "id": "intro", "toc": "Intro", "toc_main": True, "blocks": [
                {"type": "heading", "text": "Intro"},
                {"type": "text", "text": "…"}]},
            {"type": "chapter", "title": "1", "color": "mint"},
            {"type": "page", "blocks": [{"type": "text", "text": "…"}]},
            {"type": "page", "id": "sources", "toc": sources, "toc_main": True, "blocks": [
                {"type": "heading", "level": 2, "text": sources},
                {"type": "sources", "items": [["…", "https://example.com"]]}]},
            {"type": "back-cover", "illustration": "cover-base", "text": "…"}]}
    (book / "content.json").write_text(json.dumps(base, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Created: {relative(book)} ({book_type}, {lang}). Write content.json, then build.")


def list_books():
    books = existing_books()
    if not books:
        print(f"No books in {BOOKS}")
    for d in books:
        try:
            data = json.loads((d / "content.json").read_text(encoding="utf-8"))
            print(f"  {d.name}  ({data.get('type', 'other')}, {data.get('language', 'en')}, {len(data.get('pages', []))} pages in the JSON)")
        except Exception as e:
            print(f"  {d.name}  (could not read it: {e})")


# ---------- version ----------
def version_info():
    try:
        return json.loads(VERSION_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise Error(f"Cannot read {VERSION_FILE}: {e}")


def _value(argv, option, default=None):
    if option in argv and argv.index(option) + 1 < len(argv):
        return argv[argv.index(option) + 1]
    return default


if __name__ == "__main__":
    argv = sys.argv[1:]
    with_value = {"--type", "--lang", "--dir"}
    args = [a for i, a in enumerate(argv) if not a.startswith("--") and (i == 0 or argv[i - 1] not in with_value)]
    try:
        if _value(argv, "--dir"):
            use_dir(_value(argv, "--dir"))
        if "--version" in argv:
            print(version_info().get("version", "unknown"))
        elif "--list" in argv:
            list_books()
        elif "--new" in argv and args:
            new_book(args[0], _value(argv, "--type", "other"), _value(argv, "--lang", "en"))
        elif "--all" in argv:
            books = existing_books()
            if not books:
                print(f"No books in {BOOKS}")
            for d in books:
                build(d.name)
        elif args:
            build(args[0])
        else:
            print(__doc__)
            sys.exit(1)
    except Error as e:
        print("Error:", e)
        sys.exit(2)
