#!/usr/bin/env python3
"""
Per-paper preflight for Step 3 of research-workflow.

1. Verifies paper.md and paper_artifacts/ exist.
2. Reads analysis_prompt.md and prints its SHA + all hard constraints to stdout
   — this forces the active prompt rules into the agent's current context
   so the agent does not rely on memory from earlier in the session.

Exit 0 = OK to proceed.
Exit 1 = precondition failed; skip this paper and log the error.
"""
import argparse
import hashlib
import sys
from pathlib import Path

SKILL_DIR   = Path(__file__).resolve().parent.parent
PROMPT_FILE = (SKILL_DIR / ".." / "research-analysis-subagent" / "assets" / "analysis_prompt.md").resolve()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-dir", required=True, help="Absolute path to one paper directory")
    args = parser.parse_args()

    paper_dir = Path(args.paper_dir).resolve()
    errors: list[str] = []

    if not paper_dir.is_dir():
        errors.append(f"paper_dir not found: {paper_dir}")
    elif not (paper_dir / "paper.md").is_file():
        errors.append(f"paper.md missing in: {paper_dir}")
    elif not (paper_dir / "paper_artifacts").is_dir():
        errors.append(f"paper_artifacts/ missing in: {paper_dir}")

    if not PROMPT_FILE.is_file():
        errors.append(f"analysis_prompt.md not found: {PROMPT_FILE}")

    if errors:
        for e in errors:
            print(f"[preflight] ERROR: {e}", flush=True)
        sys.exit(1)

    prompt_text = PROMPT_FILE.read_text(encoding="utf-8")
    sha = hashlib.sha256(prompt_text.encode()).hexdigest()[:12]

    print(f"[preflight] paper  : {paper_dir}", flush=True)
    print(f"[preflight] prompt : {PROMPT_FILE}  sha256:{sha}", flush=True)
    print(f"[preflight] ── active constraints (apply verbatim to this paper) ──", flush=True)
    for line in prompt_text.splitlines():
        s = line.strip()
        if s and ("禁止" in s or "严禁" in s or "必须" in s or s.startswith("- **") or "不得" in s):
            print(f"[preflight]   {s}", flush=True)
    print(f"[preflight] ── end constraints ──", flush=True)
    print(f"[preflight] OK — ready to analyze", flush=True)


if __name__ == "__main__":
    main()
