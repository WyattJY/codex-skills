#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import os
import re
import sqlite3
from datetime import datetime
from pathlib import Path

EXCLUDES = {
    '.git', 'node_modules', 'Library', '.hermes', '.hermes-wyatt', '.cache', '.Trash',
    'venv', '.venv', '__pycache__', 'Applications', 'Pictures', 'Movies', 'Music',
    'Downloads', 'Desktop', 'Public', 'logs', 'sessions', 'weixin', '.pytest_cache', '.mypy_cache',
    '.ruff_cache', '.next', 'dist', 'build'
}
MARKERS = [
    'AGENTS.md', 'CLAUDE.md', 'README.md', 'readme.md', 'package.json',
    'pyproject.toml', 'requirements.txt', 'Cargo.toml', 'go.mod', 'pom.xml', '.git'
]
SECRET_PAT = re.compile(r'(\.env|token|secret|cookie|session|key)', re.I)


def slugify(s: str) -> str:
    s = re.sub(r'[^A-Za-z0-9\u4e00-\u9fff]+', '-', s).strip('-').lower()
    return s[:48] or hashlib.sha1(s.encode()).hexdigest()[:10]


def is_excluded(p: Path) -> bool:
    return p.name in EXCLUDES or SECRET_PAT.search(p.name) is not None


def detect_stack(p: Path) -> str:
    return ','.join([m for m in MARKERS if (p / m).exists()])


def iter_dirs(root: Path, max_depth: int):
    stack = [(root.expanduser(), 0)]
    while stack:
        p, depth = stack.pop()
        if depth > max_depth or is_excluded(p):
            continue
        yield p, depth
        if depth == max_depth:
            continue
        try:
            stack.extend((c, depth + 1) for c in p.iterdir() if c.is_dir() and not is_excluded(c))
        except Exception:
            pass


def classify(p: Path, stack: str) -> str:
    low = (p.name + ' ' + stack).lower()
    if any(x in low for x in ['paper', 'research', '论文', '报告']):
        return 'research'
    if any(x in low for x in ['train', 'model', 'dataset', 'ml', 'vision', 'qwen', 'vl']):
        return 'training'
    if any(x in low for x in ['app', 'web', 'frontend', 'backend', 'next', 'react', 'vue']):
        return 'product'
    return 'tooling' if stack else 'misc'


def init_db(db: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db))
    conn.execute('PRAGMA journal_mode=DELETE')
    # Required by the WyattJY implementation document, section 4.3.
    conn.execute('CREATE TABLE IF NOT EXISTS projects (project_id TEXT PRIMARY KEY,title TEXT,domain TEXT,stack TEXT,status TEXT,project_dir TEXT,final_deliverable TEXT,github_url TEXT,created_at TEXT,updated_at TEXT,tags TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS project_events (event_id TEXT PRIMARY KEY,project_id TEXT,event_type TEXT,content TEXT,evidence_path TEXT,created_at TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS feedback_turning_points (id TEXT PRIMARY KEY,project_id TEXT,before_state TEXT,change_made TEXT,user_reaction TEXT,lesson TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS bug_cases (bug_id TEXT PRIMARY KEY,project_id TEXT,symptom TEXT,root_cause TEXT,fix TEXT,prevention TEXT,severity TEXT,created_at TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS final_prompts (id TEXT PRIMARY KEY,project_id TEXT,prompt_text TEXT,use_case TEXT,version TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS cases (case_id TEXT PRIMARY KEY,title TEXT,domain TEXT,project_dir TEXT,summary TEXT,case_path TEXT,status TEXT,tags TEXT,updated_at TEXT)')
    conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS case_fts USING fts5(case_id UNINDEXED,title,summary,tags,content='cases',content_rowid='rowid')")
    return conn


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--memory-root', default=os.environ.get('HERMES_MEMORY_HOME', '/Volumes/T7 Shield/hermes/home/memory'))
    parser.add_argument('--roots', nargs='*', default=[str(Path.home())])
    parser.add_argument('--limit', type=int, default=5)
    parser.add_argument('--max-depth', type=int, default=3)
    args = parser.parse_args()

    memory = Path(args.memory_root)
    cases_dir = memory / 'cases'
    projects_dir = memory / 'projects'
    cases_dir.mkdir(parents=True, exist_ok=True)
    projects_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime('%Y-%m-%d')

    candidates = []
    for root_s in args.roots:
        root = Path(root_s).expanduser()
        if not root.exists():
            continue
        for p, _depth in iter_dirs(root, args.max_depth):
            stack = detect_stack(p)
            if not stack:
                continue
            try:
                marker_mtimes = [(p / m).stat().st_mtime for m in MARKERS if (p / m).exists()]
                mtime = max([p.stat().st_mtime] + marker_mtimes)
            except Exception:
                mtime = 0
            candidates.append((mtime, p, classify(p, stack), stack))

    seen = set()
    chosen = []
    for mtime, p, domain, stack in sorted(candidates, reverse=True):
        key = str(p.resolve()) if p.exists() else str(p)
        if key in seen:
            continue
        seen.add(key)
        chosen.append((mtime, p, domain, stack))
        if len(chosen) >= args.limit:
            break

    conn = init_db(cases_dir / 'embeddings.sqlite')
    project_rows = []
    case_rows = []
    for _mtime, p, domain, stack in chosen:
        slug = slugify(p.name)
        cid = f'case-{now.replace("-", "")}-{slug}'
        pid = f'project-{slug}'
        case_path = cases_dir / f'{cid}.md'
        summary = f'Auto-generated skeleton for {p}. Stack markers: {stack}. Wyatt must fill raw requirement, turning point, final delivery, and final prompt.'
        if not case_path.exists():
            lines = [
                '---',
                f'case_id: {cid}',
                f'title: "{p.name}"',
                f'domain: "{domain}"',
                f'project_dir: "{p}"',
                'status: "skeleton"',
                f'tags: [auto-scan, {domain}]',
                f'created_at: "{now}"',
                f'updated_at: "{now}"',
                '---',
                '',
                f'# Case: {p.name}',
                '',
                '## 1. 最初需求 raw',
                'UNKNOWN_NEEDS_WYATT',
                '',
                '## 2. 最初理解 baseline',
                'Auto-generated skeleton from local folder scan.',
                '',
                '## 3. 实际走的路径',
                'UNKNOWN_NEEDS_WYATT',
                '',
                '## 4. 参考来源',
                f'- project_dir: `{p}`',
                f'- stack markers: `{stack}`',
                '',
                '## 5. 用户态度转折点',
                'UNKNOWN_NEEDS_WYATT',
                '',
                '## 6. 最终交付',
                'UNKNOWN_NEEDS_WYATT',
                '',
                '## 7. 事后回写 prompt',
                'UNKNOWN_NEEDS_WYATT',
                '',
                '## 8. 代表性 bug',
                'UNKNOWN_NEEDS_WYATT',
            ]
            case_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
        conn.execute('INSERT OR REPLACE INTO projects VALUES (?,?,?,?,?,?,?,?,?,?,?)', (pid, p.name, domain, stack, 'skeleton', str(p), '', '', now, now, f'auto-scan,{domain}'))
        conn.execute('INSERT OR REPLACE INTO cases VALUES (?,?,?,?,?,?,?,?,?)', (cid, p.name, domain, str(p), summary, str(case_path), 'skeleton', f'auto-scan,{domain}', now))
        project_rows.append(f'| {pid} | {p.name} | {domain} | {stack} | skeleton | {p} | auto-scan,{domain} | {now} |')
        case_rows.append(f'| {cid} | {p.name} | {domain} | {p} | skeleton | auto-scan,{domain} | {now} |')
    # Keep external-content FTS5 index in sync for case-router.
    try:
        conn.execute("INSERT INTO case_fts(case_fts) VALUES('rebuild')")
    except sqlite3.DatabaseError:
        pass
    conn.commit()
    conn.close()

    (projects_dir / 'PROJECT_INDEX.md').write_text(
        '# Project Index\n\n| project_id | title | domain | stack | status | project_dir | tags | updated_at |\n|---|---|---|---|---|---|---|---|\n'
        + '\n'.join(project_rows) + '\n',
        encoding='utf-8',
    )
    (projects_dir / 'FILE_TREE_SUMMARY.md').write_text(
        '# File Tree Summary\n\nRoots scanned:\n'
        + ''.join(f'- {r}\n' for r in args.roots)
        + f'\nLimit: {args.limit}\nMax depth: {args.max_depth}\n\nChosen projects:\n'
        + ''.join(f'- {p} ({domain}; {stack})\n' for _m, p, domain, stack in chosen),
        encoding='utf-8',
    )
    (cases_dir / 'INDEX.md').write_text(
        '# Case Index\n\n| case_id | title | domain | project_dir | status | tags | updated_at |\n|---|---|---|---|---|---|---|\n'
        + '\n'.join(case_rows) + '\n',
        encoding='utf-8',
    )
    print(f'Created/updated {len(chosen)} case skeletons under {cases_dir}')
    for _m, p, domain, stack in chosen:
        print(f'- {p} [{domain}] {stack}')


if __name__ == '__main__':
    main()
