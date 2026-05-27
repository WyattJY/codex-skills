#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from datetime import datetime
from pathlib import Path


EXTS = {".pdf", ".md", ".txt", ".docx", ".pptx", ".ipynb", ".html"}
EXCLUDES = {".git", "node_modules", ".cache", "__pycache__"}
DEFAULT_MEMORY_ROOT = Path(os.environ.get("CLAUDE_WYATT_MEMORY_HOME") or os.environ.get("CODEX_WYATT_MEMORY_HOME", "H:/T7/hermes/home/memory"))
DEFAULT_RESEARCH_ROOT = Path(os.environ.get("CLAUDE_WYATT_RESEARCH_ROOT") or os.environ.get("CODEX_WYATT_RESEARCH_ROOT", "H:/T7/Wyatt/HK_intership"))


def recent_files(root: Path, limit: int = 20) -> list[Path]:
    out: list[Path] = []
    if not root.exists():
        return out
    stack = [(root, 0)]
    while stack:
        path, depth = stack.pop()
        if depth > 4 or path.name in EXCLUDES:
            continue
        try:
            for child in path.iterdir():
                if child.is_dir():
                    stack.append((child, depth + 1))
                elif child.suffix.lower() in EXTS:
                    out.append(child)
        except OSError:
            pass
    out.sort(key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True)
    return out[:limit]


def main() -> None:
    parser = argparse.ArgumentParser(description="Create one local research idea from Wyatt's T7 research corpus.")
    parser.add_argument("--memory-root", default=str(DEFAULT_MEMORY_ROOT))
    parser.add_argument("--research-root", default=str(DEFAULT_RESEARCH_ROOT))
    parser.add_argument("--out", default="")
    args = parser.parse_args()

    memory = Path(args.memory_root)
    research_root = Path(args.research_root)
    files = recent_files(research_root, 10)
    today = datetime.now().strftime("%Y-%m-%d")
    chosen = files[0] if files else None
    refs = "\n".join(f"- {p}" for p in files[:5]) if files else "- No local files found; pass --research-root."

    text = f"""# Daily Research Idea - {today}

## Topic
Turn one local research artifact into a small, testable multimodal/reranker experiment.

## Idea
Use the newest relevant local artifact as the anchor:

`{chosen if chosen else "UNKNOWN"}`

Extract one hypothesis from it and map that hypothesis to a controllable experiment in the current training or evaluation workflow. Change one variable only: data filtering, hard-negative construction, reranker objective, visual-language input format, or preference sample construction.

## Experiment
- Control: current baseline configuration.
- Variant: one hypothesis-driven change from the selected artifact.
- Data: a small de-identified subset, aggregate metrics, logs, or screenshots only.
- Metric: Recall@K, nDCG, bad-case category count, latency, or training cost.
- Stop condition: no directional improvement on the small sample, or error categories remain unchanged.

## Expected Signal
One key metric improves directionally or one bad-case category becomes visibly smaller without a large cost increase.

## Local References
{refs}

## Feedback Options
Useful / Not useful / Deep read
"""

    if args.out:
        out = Path(args.out)
    else:
        out_dir = memory / "research" / "IDEA_LOG"
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / f"idea-{today}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(text)
    print(f"\nSaved: {out}")


if __name__ == "__main__":
    main()
