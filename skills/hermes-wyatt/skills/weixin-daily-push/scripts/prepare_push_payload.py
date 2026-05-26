#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import time
from pathlib import Path

SECRET_RE = re.compile(r"(?i)(api[_-]?key|token|secret|password|cookie|session)\s*[:=]\s*\S+")


def latest_file(root: Path, pattern: str) -> Path | None:
    files = [p for p in root.glob(pattern) if p.is_file() and not p.name.startswith("._")]
    if not files:
        return None
    return max(files, key=lambda p: p.stat().st_mtime)


def safe_excerpt(text: str, limit: int) -> str:
    text = SECRET_RE.sub(r"\1=<redacted>", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text[:limit].rstrip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare a safe Weixin daily push payload without sending it.")
    parser.add_argument("--memory-root", default="/Volumes/T7 Shield/hermes/home/memory")
    parser.add_argument("--source", default="", help="Optional markdown file. Defaults to latest research IDEA_LOG.")
    parser.add_argument("--out", default="")
    parser.add_argument("--limit", type=int, default=1800)
    args = parser.parse_args()

    memory = Path(args.memory_root)
    source = Path(args.source) if args.source else latest_file(memory / "research" / "IDEA_LOG", "idea-*.md")
    if not source or not source.exists():
        raise SystemExit("No source file found. Generate paper-digest first or pass --source.")
    text = safe_excerpt(source.read_text(encoding="utf-8", errors="ignore"), args.limit)
    payload = f"""【Hermes Wyatt 早报】
来源：{source}
生成时间：{time.strftime('%Y-%m-%d %H:%M:%S')}

{text}

回复：有用 / 无用 / 深读
"""
    out = Path(args.out) if args.out else memory / "server" / "latest-weixin-push-preview.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(payload, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()

