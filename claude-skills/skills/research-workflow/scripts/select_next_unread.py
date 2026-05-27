from __future__ import annotations

import argparse
import os
from pathlib import Path


def list_candidate_dirs(base_dir: Path, require_paper_md: bool) -> list[Path]:
    items = []
    for p in base_dir.iterdir():
        if not p.is_dir():
            continue
        if require_paper_md and not (p / "paper.md").is_file():
            continue
        items.append(p)
    return items


def sort_dirs(dirs: list[Path], order: str) -> list[Path]:
    if order == "mtime":
        def key(p: Path):
            t = p.stat().st_mtime
            pm = p / "paper.md"
            if pm.is_file():
                try:
                    t = pm.stat().st_mtime
                except Exception:
                    pass
            return (t, p.name)
        return sorted(dirs, key=key)
    return sorted(dirs, key=lambda p: p.name)


def select_next_unread(base_dir: Path, order: str, require_paper_md: bool) -> Path | None:
    candidates = sort_dirs(list_candidate_dirs(base_dir, require_paper_md), order)
    for p in candidates:
        if not (p / "Analysis_Detail.md").is_file():
            return p
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-dir", default="downloads/MoE")
    parser.add_argument("--order", choices=["name", "mtime"], default="name")
    parser.add_argument("--require-paper-md", action="store_true")
    args = parser.parse_args()

    base_dir = Path(args.base_dir).expanduser().resolve()
    if not base_dir.is_dir():
        raise SystemExit(f"Base dir not found: {base_dir}")

    nxt = select_next_unread(base_dir, args.order, args.require_paper_md)
    if nxt is None:
        print("")
        return
    print(str(nxt))


if __name__ == "__main__":
    main()
