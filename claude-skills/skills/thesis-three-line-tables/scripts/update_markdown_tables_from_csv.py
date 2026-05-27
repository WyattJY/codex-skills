#!/usr/bin/env python3
"""
Update Markdown thesis drafts by regenerating aligned "三线表" text tables from CSVs.

Assumptions:
- Each table caption is a standalone line like: "表5-2 ...".
- Under each caption, there is a ```text code block holding a plain-text three-line table.
- CSVs are named like: table5_2_*.csv (or table5_2.csv).
"""

from __future__ import annotations

import argparse
import csv
import re
import unicodedata
from pathlib import Path


TABLE_CAPTION_RE = re.compile(r"^表(?P<chapter>\d+)-(?P<index>\d+)\s+(?P<title>.+?)\s*$")


def char_width(ch: str) -> int:
    if unicodedata.combining(ch):
        return 0
    return 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1


def display_width(s: str) -> int:
    return sum(char_width(ch) for ch in s)


def pad(s: str, width: int, align: str) -> str:
    w = display_width(s)
    if w >= width:
        return s
    pad_len = width - w
    if align == "right":
        return " " * pad_len + s
    if align == "center":
        left = pad_len // 2
        right = pad_len - left
        return " " * left + s + " " * right
    return s + " " * pad_len


def is_number(value: str) -> bool:
    try:
        float(value)
        return True
    except Exception:
        return False


def read_csv(path: Path) -> list[list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.reader(f))


def find_csv_for_table(csv_dir: Path, chapter: int, index: int) -> Path:
    patterns = [f"table{chapter}_{index}_*.csv", f"table{chapter}_{index}.csv"]
    matches: list[Path] = []
    for pat in patterns:
        matches.extend(csv_dir.glob(pat))
    matches = sorted(set(matches))
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise FileNotFoundError(f"No CSV found for 表{chapter}-{index} in {csv_dir} (expected {patterns}).")
    raise FileExistsError(f"Multiple CSVs found for 表{chapter}-{index}: {[m.name for m in matches]}")


def format_three_line_table(csv_path: Path) -> str:
    rows = read_csv(csv_path)
    header = rows[0]
    data = rows[1:]

    col_align: list[str] = []
    for col_idx, _ in enumerate(header):
        values = [r[col_idx] for r in data if col_idx < len(r) and r[col_idx] != ""]
        numeric_ratio = sum(is_number(v) for v in values) / max(len(values), 1)
        col_align.append("right" if numeric_ratio >= 0.8 else "left")

    widths: list[int] = []
    for col_idx, col_name in enumerate(header):
        max_w = display_width(col_name)
        for r in data:
            if col_idx < len(r):
                max_w = max(max_w, display_width(r[col_idx]))
        widths.append(max_w)

    def make_row(cells: list[str], is_header: bool) -> str:
        parts: list[str] = []
        for i, cell in enumerate(cells):
            align = "center" if is_header else col_align[i]
            parts.append(pad(cell, widths[i], align=align))
        return " | ".join(parts)

    header_row = make_row(header, is_header=True)
    data_rows = [make_row(r, is_header=False) for r in data]

    total_w = display_width(header_row)
    top = "=" * total_w
    mid = "-" * total_w
    bottom = "=" * total_w
    return "\n".join([top, header_row, mid, *data_rows, bottom])


def replace_next_text_codeblock(md: str, marker: str, new_block: str) -> str:
    idx = md.find(marker)
    if idx == -1:
        raise ValueError(f"marker not found: {marker}")

    code_start = md.find("```text", idx)
    if code_start == -1:
        raise ValueError(f"```text not found after marker: {marker}")

    after_fence = md.find("\n", code_start)
    if after_fence == -1:
        raise ValueError(f"newline missing after ```text for marker: {marker}")
    content_start = after_fence + 1

    closing = md.find("\n```", content_start)
    if closing == -1:
        raise ValueError(f"closing ``` not found for marker: {marker}")

    return md[:content_start] + new_block + md[closing:]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv-dir", type=Path, required=True, help="Folder containing per-table CSV files.")
    parser.add_argument("--md", type=Path, required=True, help="Markdown file to update in-place.")
    parser.add_argument("--dry-run", action="store_true", help="Print what would change; do not write.")
    args = parser.parse_args()

    md_text = args.md.read_text(encoding="utf-8")

    # Find captions in order of appearance
    captions: list[tuple[str, int, int]] = []
    for line in md_text.splitlines():
        m = TABLE_CAPTION_RE.match(line.strip())
        if not m:
            continue
        captions.append((line.strip(), int(m.group("chapter")), int(m.group("index"))))

    if not captions:
        raise SystemExit(f"No captions like '表5-2 ...' found in {args.md}")

    for caption, chapter, index in captions:
        csv_path = find_csv_for_table(args.csv_dir, chapter=chapter, index=index)
        new_block = format_three_line_table(csv_path)
        md_text = replace_next_text_codeblock(md_text, caption, new_block)

    if args.dry_run:
        print(md_text)
        return

    args.md.write_text(md_text, encoding="utf-8")
    print(f"Updated Markdown tables from CSVs: {args.md}")


if __name__ == "__main__":
    main()
