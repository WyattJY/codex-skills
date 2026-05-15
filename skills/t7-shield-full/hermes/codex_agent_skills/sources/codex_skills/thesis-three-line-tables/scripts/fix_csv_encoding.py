#!/usr/bin/env python3
"""
Normalize CSV encoding for Excel/WPS:
- Read each *.csv using a small set of common encodings.
- Write back as UTF-8 with BOM (utf-8-sig) + requested newline style.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


DEFAULT_INPUT_ENCODINGS = ("utf-8-sig", "utf-8", "gb18030", "gbk")


@dataclass
class RewriteResult:
    path: Path
    detected_encoding: str
    changed: bool


def normalize_newlines(text: str, newline: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.rstrip("\n") + "\n"
    if newline.upper() == "CRLF":
        return text.replace("\n", "\r\n")
    return text


def read_with_fallback(path: Path, encodings: tuple[str, ...]) -> tuple[str, str]:
    raw = path.read_bytes()
    for encoding in encodings:
        try:
            return raw.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("unknown", raw, 0, 1, "unsupported encoding")


def rewrite_csv(path: Path, newline: str, dry_run: bool) -> RewriteResult:
    original = path.read_bytes()
    text, detected = read_with_fallback(path, DEFAULT_INPUT_ENCODINGS)
    normalized = normalize_newlines(text, newline=newline)

    if dry_run:
        return RewriteResult(path=path, detected_encoding=detected, changed=(normalized.encode("utf-8-sig") != original))

    with path.open("w", encoding="utf-8-sig", newline="") as f:
        f.write(normalized)
    return RewriteResult(path=path, detected_encoding=detected, changed=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv-dir", type=Path, required=True, help="Folder containing *.csv files.")
    parser.add_argument("--newline", choices=("CRLF", "LF"), default="CRLF", help="Output newline style.")
    parser.add_argument("--dry-run", action="store_true", help="Do not write files; only report.")
    args = parser.parse_args()

    csv_dir: Path = args.csv_dir
    paths = sorted(csv_dir.glob("*.csv"))
    if not paths:
        raise SystemExit(f"No CSV files found in: {csv_dir}")

    results: list[RewriteResult] = []
    for path in paths:
        results.append(rewrite_csv(path, newline=args.newline, dry_run=args.dry_run))

    changed = sum(1 for r in results if r.changed)
    print(f"Processed {len(results)} file(s); changed {changed}.")


if __name__ == "__main__":
    main()
