#!/usr/bin/env python3
"""Check local image links in a Markdown note.

Usage:
    check_markdown_assets.py /path/to/note.md
"""

from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import unquote


SKIP_PREFIXES = ("http://", "https://", "data:", "app://")


def clean_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        return unquote(target[1:-1])
    if '"' in target:
        target = target.split('"', 1)[0].strip()
    elif "'" in target:
        target = target.split("'", 1)[0].strip()
    return unquote(target)


def clean_obsidian_target(raw: str) -> str:
    target = raw.split("|", 1)[0].strip()
    return unquote(target)


def scan_markdown_image_targets(text: str) -> list[str]:
    targets: list[str] = []
    cursor = 0
    while True:
        start = text.find("![", cursor)
        if start == -1:
            break
        if text.startswith("![[", start):
            cursor = start + 3
            continue

        alt_end = text.find("]", start + 2)
        if alt_end == -1:
            break
        open_paren = alt_end + 1
        if open_paren >= len(text) or text[open_paren] != "(":
            cursor = alt_end + 1
            continue

        pos = open_paren + 1
        if pos < len(text) and text[pos] == "<":
            close_angle = text.find(">", pos + 1)
            close_paren = text.find(")", close_angle + 1) if close_angle != -1 else -1
            if close_angle != -1 and close_paren != -1:
                targets.append(clean_target(text[pos : close_angle + 1]))
                cursor = close_paren + 1
                continue

        depth = 0
        chars: list[str] = []
        while pos < len(text):
            char = text[pos]
            if char == "\\" and pos + 1 < len(text):
                chars.append(text[pos + 1])
                pos += 2
                continue
            if char == "(":
                depth += 1
            elif char == ")":
                if depth == 0:
                    break
                depth -= 1
            chars.append(char)
            pos += 1
        if pos < len(text) and text[pos] == ")":
            targets.append(clean_target("".join(chars)))
            cursor = pos + 1
        else:
            cursor = open_paren + 1
    return targets


def scan_obsidian_image_targets(text: str) -> list[str]:
    targets: list[str] = []
    cursor = 0
    while True:
        start = text.find("![[", cursor)
        if start == -1:
            break
        end = text.find("]]", start + 3)
        if end == -1:
            break
        targets.append(clean_obsidian_target(text[start + 3 : end]))
        cursor = end + 2
    return targets


def iter_local_image_targets(text: str) -> list[str]:
    targets = scan_markdown_image_targets(text) + scan_obsidian_image_targets(text)
    return [target for target in targets if target and not target.startswith(SKIP_PREFIXES)]


def check_markdown_assets(md_path: Path) -> tuple[int, list[str]]:
    text = md_path.read_text(encoding="utf-8")
    missing: list[str] = []
    checked = 0

    for target in iter_local_image_targets(text):
        path = Path(target)
        if not path.is_absolute():
            path = md_path.parent / path
        checked += 1
        if not path.exists():
            missing.append(str(path))
    return checked, missing


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_markdown_assets.py /path/to/note.md", file=sys.stderr)
        return 2

    md_path = Path(sys.argv[1]).expanduser().resolve()
    if not md_path.exists():
        print(f"missing markdown: {md_path}", file=sys.stderr)
        return 2

    checked, missing = check_markdown_assets(md_path)

    print(f"markdown={md_path}")
    print(f"local_image_links={checked}")
    print(f"missing={len(missing)}")
    for path in missing:
        print(f"MISSING {path}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
