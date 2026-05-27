#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import sqlite3
import time
from pathlib import Path


DEFAULT_MEMORY_ROOT = Path(os.environ.get("CLAUDE_WYATT_MEMORY_HOME") or os.environ.get("CODEX_WYATT_MEMORY_HOME", "H:/T7/hermes/home/memory"))


def slugify(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9\u4e00-\u9fff]+", "-", text).strip("-").lower()
    return slug[:64] or "case"


def md_section(title: str, body: str) -> str:
    return f"## {title}\n{body.strip() or 'UNKNOWN_NEEDS_WYATT'}\n"


def init_db(db: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db))
    conn.execute("CREATE TABLE IF NOT EXISTS cases (case_id TEXT PRIMARY KEY,title TEXT,domain TEXT,project_dir TEXT,summary TEXT,case_path TEXT,status TEXT,tags TEXT,updated_at TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS final_prompts (id TEXT PRIMARY KEY,project_id TEXT,prompt_text TEXT,use_case TEXT,version TEXT)")
    return conn


def rebuild_index(memory: Path, conn: sqlite3.Connection) -> None:
    rows = conn.execute("SELECT case_id,title,domain,project_dir,status,tags,updated_at FROM cases ORDER BY updated_at DESC, title").fetchall()
    index = memory / "cases" / "INDEX.md"
    index.write_text(
        "# Case Index\n\n| case_id | title | domain | project_dir | status | tags | updated_at |\n|---|---|---|---|---|---|---|\n"
        + "\n".join(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} |" for r in rows)
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Archive a project/task as a Wyatt local case note.")
    parser.add_argument("--memory-root", default=str(DEFAULT_MEMORY_ROOT))
    parser.add_argument("--title", required=True)
    parser.add_argument("--domain", default="misc")
    parser.add_argument("--project-dir", default="")
    parser.add_argument("--raw-requirement", default="")
    parser.add_argument("--baseline", default="")
    parser.add_argument("--path-taken", default="")
    parser.add_argument("--references", default="")
    parser.add_argument("--turning-point", default="")
    parser.add_argument("--final-delivery", default="")
    parser.add_argument("--final-prompt", default="")
    parser.add_argument("--bug", default="")
    parser.add_argument("--tags", default="manual-archive")
    args = parser.parse_args()

    memory = Path(args.memory_root)
    cases_dir = memory / "cases"
    cases_dir.mkdir(parents=True, exist_ok=True)
    today = time.strftime("%Y%m%d")
    now = time.strftime("%Y-%m-%d")
    case_id = f"case-{today}-{slugify(args.title)}"
    project_id = "project-" + slugify(args.title)
    case_path = cases_dir / f"{case_id}.md"

    content = "\n".join([
        "---",
        f"case_id: {case_id}",
        f'title: "{args.title}"',
        f'domain: "{args.domain}"',
        f'project_dir: "{args.project_dir}"',
        'status: "archived"',
        f"tags: [{args.tags}]",
        f'created_at: "{now}"',
        f'updated_at: "{now}"',
        "---",
        "",
        f"# Case: {args.title}",
        "",
        md_section("1. Raw Requirement", args.raw_requirement),
        md_section("2. Baseline Interpretation", args.baseline),
        md_section("3. Actual Path Taken", args.path_taken),
        md_section("4. References", args.references),
        md_section("5. User Turning Point", args.turning_point),
        md_section("6. Final Delivery", args.final_delivery),
        md_section("7. Rewritten Final Prompt", args.final_prompt),
        md_section("8. Representative Bugs", args.bug),
    ])
    case_path.write_text(content, encoding="utf-8")

    conn = init_db(cases_dir / "embeddings.sqlite")
    summary = f"{args.title}; domain={args.domain}; delivery={args.final_delivery[:160]}"
    conn.execute("INSERT OR REPLACE INTO cases VALUES (?,?,?,?,?,?,?,?,?)", (case_id, args.title, args.domain, args.project_dir, summary, str(case_path), "archived", args.tags, now))
    if args.final_prompt:
        conn.execute("INSERT OR REPLACE INTO final_prompts VALUES (?,?,?,?,?)", (f"prompt-{case_id}", project_id, args.final_prompt, args.domain, today))
    rebuild_index(memory, conn)
    conn.commit()
    conn.close()
    print(case_path)


if __name__ == "__main__":
    main()
