#!/usr/bin/env python3
"""
Run any research-workflow script with the current Python interpreter.
The caller (agent) is responsible for ensuring required packages are installed.

Usage:
    python scripts/run.py download_arxiv_papers.py --input list.txt --outdir downloads/topic
    python scripts/run.py pdf_to_markdown.py --root downloads/MoE
    python scripts/run.py merge_moe_report.py --base-dir downloads/MoE --outline outline.md
"""
import sys
import subprocess
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python scripts/run.py <script.py> [args...]")
        print(f"Available: {', '.join(p.name for p in SCRIPTS_DIR.glob('*.py') if p.name != 'run.py')}")
        sys.exit(1)

    arg = Path(sys.argv[1])
    script = arg.resolve() if (arg.is_absolute() or arg.exists()) else SCRIPTS_DIR / arg.name

    if not script.exists():
        print(f"[run] ERROR: script not found: {script}")
        sys.exit(1)

    sys.exit(subprocess.run([sys.executable, str(script), *sys.argv[2:]]).returncode)


if __name__ == "__main__":
    main()
