#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import sqlite3
import time
from pathlib import Path


DEFAULT_MEMORY_ROOT = Path(os.environ.get("CLAUDE_WYATT_MEMORY_HOME") or os.environ.get("CODEX_WYATT_MEMORY_HOME", "H:/T7/hermes/home/memory"))


def extract_section(text: str, title_fragment: str) -> str:
    pattern = re.compile(rf"^##\s+.*{re.escape(title_fragment)}.*?\n(.*?)(?=^##\s+|\Z)", re.M | re.S)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def case_id_from_text(text: str, path: Path) -> str:
    match = re.search(r"^case_id:\s*(\S+)", text, re.M)
    return match.group(1) if match else path.stem


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a final rewritten prompt from a case markdown file.")
    parser.add_argument("case_file")
    parser.add_argument("--memory-root", default=str(DEFAULT_MEMORY_ROOT))
    parser.add_argument("--out", default="")
    parser.add_argument("--update-db", action="store_true")
    args = parser.parse_args()

    case_path = Path(args.case_file)
    text = case_path.read_text(encoding="utf-8", errors="ignore")
    case_id = case_id_from_text(text, case_path)
    raw = extract_section(text, "Raw Requirement") or extract_section(text, "Requirement")
    path_taken = extract_section(text, "Actual Path") or extract_section(text, "Path Taken")
    delivery = extract_section(text, "Final Delivery")
    bug = extract_section(text, "Representative Bugs")

    prompt = f"""Please handle this task in Claude Code using Wyatt's local workflow.

Requirements:
1. Preserve the user's original goal and exact path constraints.
2. Before implementation, check relevant local docs and prior cases only when useful.
3. For product/code/research/training work, split the work into scoped artifacts, implementation steps, and verification steps.
4. Deliver exact file paths, verification commands, known risks, and next steps.
5. Do not write or display .env files, API keys, WEIXIN_TOKEN, cookies, sessions, or raw company data.

Original requirement:
{raw or "UNKNOWN_NEEDS_WYATT"}

Validated path:
{path_taken or "UNKNOWN_NEEDS_WYATT"}

Final delivery reference:
{delivery or "UNKNOWN_NEEDS_WYATT"}

Bugs or review risks to avoid:
{bug or "UNKNOWN_NEEDS_WYATT"}
"""
    out = Path(args.out) if args.out else case_path.with_suffix(".final-prompt.md")
    out.write_text(prompt, encoding="utf-8")

    if args.update_db:
        db = Path(args.memory_root) / "cases" / "embeddings.sqlite"
        db.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(db))
        project_id = "project-" + re.sub(r"^case-\d+-", "", case_id)
        conn.execute("CREATE TABLE IF NOT EXISTS final_prompts (id TEXT PRIMARY KEY,project_id TEXT,prompt_text TEXT,use_case TEXT,version TEXT)")
        conn.execute("INSERT OR REPLACE INTO final_prompts VALUES (?,?,?,?,?)", (f"prompt-{case_id}", project_id, prompt, "case-final", time.strftime("%Y%m%d")))
        conn.commit()
        conn.close()
    print(out)


if __name__ == "__main__":
    main()
