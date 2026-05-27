#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time
from pathlib import Path


DEFAULT_TRENDS = [
    ("Dense operator dashboard", "Use restrained typography, clear tables, compact filters, status chips, and persistent actions for repeated use."),
    ("Model demo page", "Show sample defaults, input/output evidence, run metadata, and report-ready statistics without marketing hero sections."),
    ("Research workflow view", "Prefer timeline, paper cards, RUN_CARD links, and decision logs over decorative cards."),
    ("Admin/key console", "Use account status, quota windows, add-key flow, audit trail, and error recovery states."),
    ("Word/report handoff", "Keep charts and screenshots report-friendly, with exact file paths and reproducible commands."),
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Write Wyatt UI trend notes.")
    parser.add_argument("--memory-root", default="H:/T7/hermes/home/memory")
    parser.add_argument("--extra", action="append", default=[])
    args = parser.parse_args()

    out_dir = Path(args.memory_root) / "ui"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "ui-trends.md"
    now = time.strftime("%Y-%m-%d")
    lines = [
        "# UI Trends for WyattJY",
        "",
        f"Updated: {now}",
        "",
        "These notes are implementation-oriented. They are not mood-board slogans.",
        "",
        "| Direction | Reusable Guidance |",
        "|---|---|",
    ]
    for title, body in DEFAULT_TRENDS:
        lines.append(f"| {title} | {body} |")
    for item in args.extra:
        lines.append(f"| Manual note | {item} |")
    lines += [
        "",
        "## Hard Constraints",
        "- Build the actual tool/app surface first, not a landing page, unless the user asks for a landing page.",
        "- Avoid one-note palettes and decorative-only visuals.",
        "- Preserve sample/default data on model pages.",
        "- Verify text fit, responsive states, and screenshot evidence before claiming UI completion.",
    ]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
