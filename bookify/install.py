#!/usr/bin/env python3
"""
Bookify installer · a skill that turns research into illustrated digital books.

Uses only the Python standard library (3.9 or newer). Installs no packages.

Install (downloads the latest GitHub release):
    python install.py --tool claude           Claude Code (and profiles that share ~/.claude)
    python install.py --tool commandcode      Command Code CLI
    python install.py --tool opencode         OpenCode
    python install.py --tool copilot          GitHub Copilot in VS Code
    python install.py --tool claude,opencode  several at once (or: all)
    python install.py                         asks which one, when run in a terminal

Options:
    --project [DIR]   install for one project only (default: the current folder) instead of for the user
    --version X       install a specific release (for example 1.2.0)
    --branch NAME     install from a branch instead of a release (for example main)
    --from DIR        install from a local copy of the repository (for development)

Maintain:
    python install.py --update      look for a new release and update every installation
    python install.py --check       only report whether there is a new release
    python install.py --list        show where it is installed
    python install.py --uninstall --tool X [--project DIR]
"""
import io, json, os, re, shutil, sys, tempfile, urllib.error, urllib.request, zipfile
from datetime import date
from pathlib import Path

REPO = "devjoi2018/bookify"         # also change it in version.json if the repository moves
NAME = "bookify"                    # skill name: must match its folder
PLACEHOLDER = "{{SKILL_DIR}}"       # replaced in SKILL.md with the real path of the installed skill
REGISTRY = Path.home() / ".bookify" / "installs.json"
PLACEHOLDER_REPO_OWNER = "your-user/"

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def _xdg_config():
    return Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")


# tool: (display name, global skills folder, skills folder inside a project)
TOOLS = {
    "claude":      ("Claude Code",              lambda: Path.home() / ".claude" / "skills",       ".claude/skills"),
    "commandcode": ("Command Code",             lambda: Path.home() / ".commandcode" / "skills",  ".commandcode/skills"),
    "opencode":    ("OpenCode",                 lambda: _xdg_config() / "opencode" / "skills",   ".opencode/skills"),
    "copilot":     ("GitHub Copilot (VS Code)", lambda: Path.home() / ".copilot" / "skills",      ".github/skills"),
}
HOW_TO_USE = {
    "claude": "/bookify <topic>  (or ask: \"turn this into a book\")",
    "commandcode": "/bookify <topic>  (or ask: \"turn this into a book\")",
    "opencode": "ask: \"turn this into a book\"  (or type @bookify)",
    "copilot": "in agent mode chat: /bookify <topic>",
}
# Never copied into an installation
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", "output", "books", ".claude", ".git", ".DS_Store")


class Error(Exception):
    pass


# ---------- GitHub ----------
def current_repo():
    """The repo in version.json next to this file (installed copies), or REPO if not configured."""
    folder = Path(__file__).resolve().parent
    if not (folder / "engine" / "build.py").exists():   # run through a pipe: do not read unrelated files
        return REPO
    try:
        r = str(json.loads((folder / "version.json").read_text(encoding="utf-8")).get("repo", ""))
        if r and not r.startswith(PLACEHOLDER_REPO_OWNER):
            return r
    except (OSError, json.JSONDecodeError):
        pass
    return REPO


def _get(url, binary=False):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": NAME})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise Error(f"GitHub answered {e.code} to {url}")
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise Error(f"Could not reach GitHub ({e}). Check your internet connection.")
    return data if binary else json.loads(data.decode("utf-8"))


def latest_release(repo=None, version=None):
    repo = repo or current_repo()
    if repo.startswith(PLACEHOLDER_REPO_OWNER):
        raise Error("The GitHub repository is not configured yet (REPO in install.py).")
    path = f"tags/v{version.lstrip('vV')}" if version else "latest"
    rel = _get(f"https://api.github.com/repos/{repo}/releases/{path}")
    if rel is None and version:
        rel = _get(f"https://api.github.com/repos/{repo}/releases/tags/{version}")
    return rel


def _numbers(v):
    return tuple(int(x) for x in re.findall(r"\d+", str(v))[:3]) or (0,)


def download(repo, version=None, branch=None):
    """Return (temporary folder with the repo, version, release notes)."""
    if branch:
        url, ver, notes = f"https://codeload.github.com/{repo}/zip/refs/heads/{branch}", f"branch {branch}", ""
    else:
        rel = latest_release(repo, version)
        if rel is None:
            raise Error(f"{repo} has no such release (or none at all). Try --branch main.")
        url, ver, notes = rel["zipball_url"], str(rel.get("tag_name", "")).lstrip("vV"), rel.get("body") or ""
    data = _get(url, binary=True)
    if data is None:
        raise Error(f"Not found: {url}")
    tmp = Path(tempfile.mkdtemp(prefix="bookify-"))
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for m in z.infolist():                       # nothing outside the temporary folder
            target = (tmp / m.filename).resolve()
            if tmp.resolve() not in target.parents and target != tmp.resolve():
                raise Error(f"The download contains an invalid path: {m.filename}")
        z.extractall(tmp)
    return tmp, ver, notes


def find_skill(root):
    root = Path(root)
    for c in [root, root / NAME, *root.glob(f"*/{NAME}")]:
        if (c / "SKILL.md").exists() and (c / "engine" / "build.py").exists():
            return c
    raise Error(f"Skill folder {NAME}/ (with SKILL.md and engine/) not found in {root}")


# ---------- installation registry ----------
def read_registry():
    try:
        return json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []


def save_registry(items):
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")


def register(tool, target, version):
    items = [i for i in read_registry() if Path(i["path"]) != target]
    items.append({"tool": tool, "path": str(target), "version": version, "date": date.today().isoformat()})
    save_registry(items)


# ---------- install ----------
def target_dir(tool, project=None):
    _, global_dir, local = TOOLS[tool]
    base = (Path(project).resolve() / local) if project else global_dir()
    return base / NAME


def install_into(source, target, version):
    target = Path(target)
    if target.exists() and not (target / "version.json").exists() and not (target / "engine").exists():
        raise Error(f"{target} already exists and does not look like a {NAME} installation. Leaving it alone.")
    target.parent.mkdir(parents=True, exist_ok=True)
    new = target.with_name(NAME + ".new")
    old = target.with_name(NAME + ".old")
    for d in (new, old):
        if d.exists():
            shutil.rmtree(d)
    shutil.copytree(source, new, ignore=IGNORE)
    path = target.resolve().as_posix()
    for f in ("SKILL.md", "review.md"):
        p = new / f
        if p.exists():
            p.write_text(p.read_text(encoding="utf-8").replace(PLACEHOLDER, path), encoding="utf-8")
    vf = new / "version.json"
    meta = json.loads(vf.read_text(encoding="utf-8")) if vf.exists() else {}
    if version and not version.startswith("branch"):
        meta["version"] = version
    if not meta.get("repo") or str(meta["repo"]).startswith(PLACEHOLDER_REPO_OWNER):
        meta["repo"] = current_repo()
    vf.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if target.exists():
        target.rename(old)
    new.rename(target)
    if old.exists():
        shutil.rmtree(old, ignore_errors=True)
    return meta.get("version", version)


def choose_tools(value):
    if value:
        names = list(TOOLS) if value.strip().lower() == "all" else [v.strip().lower() for v in value.split(",") if v.strip()]
        bad = [n for n in names if n not in TOOLS]
        if bad:
            raise Error(f"Unknown tool: {', '.join(bad)}. Use: {', '.join(TOOLS)} or all")
        return names
    if not sys.stdin.isatty():
        raise Error("Name the tool: --tool " + "|".join(TOOLS) + "|all")
    print("Which tool should Bookify be installed for?")
    keys = list(TOOLS)
    for i, k in enumerate(keys, 1):
        print(f"  {i}. {TOOLS[k][0]}")
    print(f"  {len(keys) + 1}. All")
    answer = input("Type the numbers, separated by commas: ").replace(" ", "")
    chosen = []
    for r in answer.split(","):
        if r.isdigit() and 1 <= int(r) <= len(keys):
            chosen.append(keys[int(r) - 1])
        elif r == str(len(keys) + 1):
            return keys
    if not chosen:
        raise Error("No tool chosen.")
    return chosen


def install(tools, project=None, version=None, branch=None, from_dir=None):
    tmp = None
    try:
        if from_dir:
            source = find_skill(from_dir)
            ver = json.loads((source / "version.json").read_text(encoding="utf-8")).get("version", "local")
        else:
            tmp, ver, _ = download(current_repo(), version, branch)
            source = find_skill(tmp)
        for t in tools:
            target = target_dir(t, project)
            v = install_into(source, target, ver)
            register(t, target, v)
            print(f"✓ {TOOLS[t][0]}: {target}  (version {v})")
            print(f"    Use it: {HOW_TO_USE[t]}")
        print("\nRestart the tool (or open a new session) so it loads the skill.")
        print("It needs Python 3.9 or newer on this computer; nothing else is installed.")
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)


# ---------- update, list, uninstall ----------
def installed_version():
    """The oldest of the registered installations: if one is behind, it needs updating."""
    versions = [i.get("version", "0") for i in read_registry() if Path(i["path"]).exists()]
    if not versions:
        folder = Path(__file__).resolve().parent
        local = folder / "version.json"
        if (folder / "engine" / "build.py").exists() and local.exists():
            versions = [json.loads(local.read_text(encoding="utf-8")).get("version", "0")]
    return min(versions, key=_numbers) if versions else None


def check():
    """Print the status and end with a STATUS=new|up-to-date|no-releases line."""
    current = installed_version() or "0"
    rel = latest_release()
    if rel is None:
        print(f"Installed version: {current}. {current_repo()} does not exist or has no published releases yet.")
        print("STATUS=no-releases")
        return None
    latest = str(rel.get("tag_name", "")).lstrip("vV")
    print(f"Installed version: {current}")
    print(f"Latest release:    {latest}  ({rel.get('html_url', '')})")
    if _numbers(latest) > _numbers(current):
        notes = (rel.get("body") or "").strip()
        if notes:
            print("\nWhat's new:\n" + notes[:1500])
        print("STATUS=new")
        return latest
    print("STATUS=up-to-date")
    return None


def update(force=False):
    newer = check()
    if not newer and not force:
        return
    items = [i for i in read_registry() if Path(i["path"]).exists()]
    if not items:
        raise Error("No registered installations found. Install with --tool.")
    tmp, ver, _ = download(current_repo())
    try:
        source = find_skill(tmp)
        for i in items:
            v = install_into(source, Path(i["path"]), ver)
            register(i["tool"], Path(i["path"]), v)
            print(f"✓ Updated: {TOOLS.get(i['tool'], (i['tool'],))[0]}: {i['path']}  ({v})")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("\nRestart the tool (or open a new session) to use the new version.")


def list_installs():
    items = read_registry()
    if not items:
        print("No registered installations.")
    for i in items:
        state = "" if Path(i["path"]).exists() else "  (no longer exists)"
        print(f"  {TOOLS.get(i['tool'], (i['tool'],))[0]}: {i['path']}  version {i.get('version', '?')}{state}")


def uninstall(tools, project=None):
    for t in tools:
        target = target_dir(t, project)
        if target.exists():
            if not (target / "engine" / "build.py").exists():
                raise Error(f"{target} does not look like a {NAME} installation. Not deleting it.")
            shutil.rmtree(target)
            print(f"✓ Removed from {TOOLS[t][0]}: {target}")
        else:
            print(f"· {TOOLS[t][0]}: not installed in {target}")
        save_registry([i for i in read_registry() if Path(i["path"]) != target])
    print("Your books (books/ and output/ folders) are not touched.")


def _value(argv, option):
    if option in argv:
        i = argv.index(option)
        if i + 1 < len(argv) and not argv[i + 1].startswith("--"):
            return argv[i + 1]
        return ""
    return None


def main(argv):
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return
    if sys.version_info < (3, 9):
        raise Error("Python 3.9 or newer is required.")
    project = _value(argv, "--project")
    if project == "":
        project = os.getcwd()
    if "--check" in argv:
        check()
    elif "--update" in argv:
        update("--force" in argv)
    elif "--list" in argv:
        list_installs()
    elif "--uninstall" in argv:
        uninstall(choose_tools(_value(argv, "--tool")), project)
    else:
        install(choose_tools(_value(argv, "--tool")), project,
                _value(argv, "--version") or None, _value(argv, "--branch") or None, _value(argv, "--from") or None)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Error as e:
        print("Error:", e)
        sys.exit(2)
    except KeyboardInterrupt:
        sys.exit(130)
