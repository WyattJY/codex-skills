#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sqlite3
import time
from pathlib import Path


def slugify(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9\u4e00-\u9fff]+", "-", text).strip("-").lower()
    return slug[:64] or "case"


def init_db(db: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db))
    conn.execute("CREATE TABLE IF NOT EXISTS projects (project_id TEXT PRIMARY KEY,title TEXT,domain TEXT,stack TEXT,status TEXT,project_dir TEXT,final_deliverable TEXT,github_url TEXT,created_at TEXT,updated_at TEXT,tags TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS project_events (event_id TEXT PRIMARY KEY,project_id TEXT,event_type TEXT,content TEXT,evidence_path TEXT,created_at TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS feedback_turning_points (id TEXT PRIMARY KEY,project_id TEXT,before_state TEXT,change_made TEXT,user_reaction TEXT,lesson TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS bug_cases (bug_id TEXT PRIMARY KEY,project_id TEXT,symptom TEXT,root_cause TEXT,fix TEXT,prevention TEXT,severity TEXT,created_at TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS final_prompts (id TEXT PRIMARY KEY,project_id TEXT,prompt_text TEXT,use_case TEXT,version TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS cases (case_id TEXT PRIMARY KEY,title TEXT,domain TEXT,project_dir TEXT,summary TEXT,case_path TEXT,status TEXT,tags TEXT,updated_at TEXT)")
    conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS case_fts USING fts5(case_id UNINDEXED,title,summary,tags,content='cases',content_rowid='rowid')")
    return conn


def md_section(title: str, body: str) -> str:
    return f"## {title}\n{body.strip() or 'UNKNOWN_NEEDS_WYATT'}\n"


def rebuild_indexes(conn: sqlite3.Connection, memory: Path) -> None:
    cases = conn.execute("SELECT case_id,title,domain,project_dir,status,tags,updated_at FROM cases ORDER BY updated_at DESC, title").fetchall()
    projects = conn.execute("SELECT project_id,title,domain,stack,status,project_dir,tags,updated_at FROM projects ORDER BY updated_at DESC, title").fetchall()
    (memory / "cases" / "INDEX.md").write_text(
        "# Case Index\n\n| case_id | title | domain | project_dir | status | tags | updated_at |\n|---|---|---|---|---|---|---|\n"
        + "\n".join(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} |" for r in cases)
        + "\n",
        encoding="utf-8",
    )
    (memory / "projects" / "PROJECT_INDEX.md").write_text(
        "# Project Index\n\n| project_id | title | domain | stack | status | project_dir | tags | updated_at |\n|---|---|---|---|---|---|---|---|\n"
        + "\n".join(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} | {r[7]} |" for r in projects)
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Archive a project/task as a Wyatt Hermes memory case.")
    parser.add_argument("--memory-root", default="/Volumes/T7 Shield/hermes/home/memory")
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
    slug = slugify(args.title)
    case_id = f"case-{today}-{slug}"
    project_id = f"project-{slug}"
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
        md_section("1. 最初需求 raw", args.raw_requirement),
        md_section("2. 最初理解 baseline", args.baseline),
        md_section("3. 实际走的路径", args.path_taken),
        md_section("4. 参考来源", args.references),
        md_section("5. 用户态度转折点", args.turning_point),
        md_section("6. 最终交付", args.final_delivery),
        md_section("7. 事后回写 prompt", args.final_prompt),
        md_section("8. 代表性 bug", args.bug),
    ])
    case_path.write_text(content, encoding="utf-8")

    db = cases_dir / "embeddings.sqlite"
    conn = init_db(db)
    summary = f"{args.title}; domain={args.domain}; delivery={args.final_delivery[:160]}"
    conn.execute("INSERT OR REPLACE INTO projects VALUES (?,?,?,?,?,?,?,?,?,?,?)", (project_id, args.title, args.domain, "", "archived", args.project_dir, args.final_delivery, "", now, now, args.tags))
    conn.execute("INSERT OR REPLACE INTO cases VALUES (?,?,?,?,?,?,?,?,?)", (case_id, args.title, args.domain, args.project_dir, summary, str(case_path), "archived", args.tags, now))
    conn.execute("INSERT OR REPLACE INTO project_events VALUES (?,?,?,?,?,?)", (f"event-{case_id}-requirement", project_id, "requirement", args.raw_requirement, str(case_path), now))
    conn.execute("INSERT OR REPLACE INTO project_events VALUES (?,?,?,?,?,?)", (f"event-{case_id}-delivery", project_id, "delivery", args.final_delivery, str(case_path), now))
    if args.turning_point:
        conn.execute("INSERT OR REPLACE INTO feedback_turning_points VALUES (?,?,?,?,?,?)", (f"turn-{case_id}", project_id, args.baseline, args.path_taken, args.turning_point, "Preserve this as routing evidence for future similar work."))
    if args.bug:
        conn.execute("INSERT OR REPLACE INTO bug_cases VALUES (?,?,?,?,?,?,?,?)", (f"bug-{case_id}", project_id, args.bug, "UNKNOWN_NEEDS_WYATT", "UNKNOWN_NEEDS_WYATT", "Route similar symptoms through reviewer-ops.", "unknown", now))
    if args.final_prompt:
        conn.execute("INSERT OR REPLACE INTO final_prompts VALUES (?,?,?,?,?)", (f"prompt-{case_id}", project_id, args.final_prompt, args.domain, "1"))
    try:
        conn.execute("INSERT INTO case_fts(case_fts) VALUES('rebuild')")
    except sqlite3.DatabaseError:
        pass
    rebuild_indexes(conn, memory)
    conn.commit()
    conn.close()
    print(case_path)


if __name__ == "__main__":
    main()
