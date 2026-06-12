#!/usr/bin/env python3
"""Check local image links in a Markdown note.

Usage:
    check_markdown_assets.py /path/to/note.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def clean_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        return unquote(target[1:-1])
    if '"' in target:
        target = target.split('"', 1)[0].strip()
    elif "'" in target:
        target = target.split("'", 1)[0].strip()
    return unquote(target)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_markdown_assets.py /path/to/note.md", file=sys.stderr)
        return 2

    md_path = Path(sys.argv[1]).expanduser().resolve()
    if not md_path.exists():
        print(f"missing markdown: {md_path}", file=sys.stderr)
        return 2

    text = md_path.read_text(encoding="utf-8")
    missing: list[str] = []
    checked = 0

    for match in IMAGE_RE.finditer(text):
        target = clean_target(match.group(1))
        if target.startswith(("http://", "https://", "data:", "app://")):
            continue
        path = Path(target)
        if not path.is_absolute():
            path = md_path.parent / path
        checked += 1
        if not path.exists():
            missing.append(str(path))

    print(f"markdown={md_path}")
    print(f"local_image_links={checked}")
    print(f"missing={len(missing)}")
    for path in missing:
        print(f"MISSING {path}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
