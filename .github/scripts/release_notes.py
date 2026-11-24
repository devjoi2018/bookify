"""Print the CHANGELOG.md section of one version, for the GitHub release notes.

usage: python release_notes.py 1.2.0
"""
import re
import sys
from pathlib import Path

version = sys.argv[1].lstrip("vV")
text = Path(__file__).resolve().parents[2].joinpath("CHANGELOG.md").read_text(encoding="utf-8")
match = re.search(rf"^## v?{re.escape(version)}\b[^\n]*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
if not match:
    sys.exit(f"CHANGELOG.md has no section for {version} (add a '## {version}' heading).")
print(match.group(1).strip())
