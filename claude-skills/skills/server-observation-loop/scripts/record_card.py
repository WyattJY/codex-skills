#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import time
from pathlib import Path


DEFAULT_MEMORY_ROOT = Path(os.environ.get("CLAUDE_WYATT_MEMORY_HOME") or os.environ.get("CODEX_WYATT_MEMORY_HOME", "H:/T7/hermes/home/memory"))
CARD_DIRS = {
    "run": "datasets/RUN_CARDS",
    "data": "datasets/DATA_CARDS",
    "error": "datasets/ERROR_CARDS",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Record RUN_CARD, DATA_CARD, or ERROR_CARD without raw company data.")
    parser.add_argument("kind", choices=sorted(CARD_DIRS))
    parser.add_argument("--memory-root", default=str(DEFAULT_MEMORY_ROOT))
    parser.add_argument("--title", required=True)
    parser.add_argument("--goal", default="")
    parser.add_argument("--command", default="")
    parser.add_argument("--observed", default="")
    parser.add_argument("--inference", default="")
    parser.add_argument("--next-command", default="")
    parser.add_argument("--metrics", default="")
    args = parser.parse_args()

    date = time.strftime("%Y-%m-%d")
    stamp = time.strftime("%Y%m%d-%H%M%S")
    out_dir = Path(args.memory_root) / CARD_DIRS[args.kind]
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{args.kind}-card-{stamp}.md"
    body = f"""# {args.kind.upper()}_CARD - {args.title}

## Basic Info
- Date: {date}
- Goal: {args.goal or "UNKNOWN_NEEDS_WYATT"}
- Safety boundary: sanitized logs, screenshots, aggregate metrics, and commands only. No raw company data.

## Command
```bash
{args.command or "# UNKNOWN_NEEDS_WYATT"}
```

## Metrics
{args.metrics or "- UNKNOWN_NEEDS_WYATT"}

## Screenshot / Log Summary
{args.observed or "- UNKNOWN_NEEDS_WYATT"}

## Claude Code Analysis
- Observed: {args.observed or "UNKNOWN_NEEDS_WYATT"}
- Inference: {args.inference or "UNKNOWN_NEEDS_WYATT"}
- Next command:
```bash
{args.next_command or "# UNKNOWN_NEEDS_WYATT"}
```

## Safety Checklist
- No API key, token, cookie, or session recorded.
- No raw company data, raw samples, or private identifiers recorded.
"""
    out.write_text(body, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
