#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import sqlite3
from pathlib import Path


DEFAULT_MEMORY_ROOT = Path(os.environ.get("CLAUDE_WYATT_MEMORY_HOME") or os.environ.get("CODEX_WYATT_MEMORY_HOME", "H:/T7/hermes/home/memory"))


def classify(query: str) -> str:
    low = query.lower()
    if any(x in low for x in ["ui", "prd", "product", "frontend", "backend", "app", "web"]):
        return "product"
    if any(x in low for x in ["paper", "research", "model", "training", "multimodal", "qwen", "vl", "reranker"]):
        return "research/training"
    if any(x in low for x in ["bug", "error", "review", "test", "ci", "debug"]):
        return "debugging/review"
    return "misc"


def terms_for(query: str) -> list[str]:
    terms = re.findall(r"[A-Za-z0-9_\-]+|[\u4e00-\u9fff]{2,}", query.lower())
    return list(dict.fromkeys(terms))


def score_row(row: sqlite3.Row, terms: list[str]) -> int:
    text = " ".join(str(row[k] or "") for k in row.keys()).lower()
    score = 0
    for term in terms:
        if term in text:
            title_hit = term in str(row["title"] or "").lower() or term in str(row["project_dir"] or "").lower()
            score += 3 if title_hit else 1
    return score


def main() -> None:
    parser = argparse.ArgumentParser(description="Query Wyatt local case index if it exists.")
    parser.add_argument("query", nargs="*")
    parser.add_argument("--memory-root", default=str(DEFAULT_MEMORY_ROOT))
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--write-context", default="")
    args = parser.parse_args()

    query = " ".join(args.query).strip()
    if not query:
        raise SystemExit('Usage: query-router.py "new requirement text"')

    db = Path(args.memory_root) / "cases" / "embeddings.sqlite"
    explicit = re.findall(r"\[\[(case-[A-Za-z0-9_-]+)\]\]", query)
    rows: list[sqlite3.Row] = []

    if db.exists():
        conn = sqlite3.connect(str(db))
        conn.row_factory = sqlite3.Row
        if explicit:
            qmarks = ",".join("?" for _ in explicit)
            rows = conn.execute(f"SELECT * FROM cases WHERE case_id IN ({qmarks})", explicit).fetchall()
        else:
            all_rows = conn.execute("SELECT rowid, * FROM cases").fetchall()
            terms = terms_for(query)
            scored = [(score_row(row, terms), row) for row in all_rows]
            scored = [item for item in scored if item[0] > 0]
            scored.sort(key=lambda item: (item[0], item[1]["updated_at"]), reverse=True)
            rows = [row for _score, row in scored[: args.top_k]]
        conn.close()

    out = [
        "# MEMORY_CONTEXT",
        "",
        f"- query: {query}",
        f"- classified_intent: {classify(query)}",
        f"- memory_root: {Path(args.memory_root)}",
        f"- loaded_cases: {min(len(rows), args.top_k)} (max {args.top_k})",
        "",
    ]
    for row in rows[: args.top_k]:
        out += [
            f'## {row["case_id"]}: {row["title"]}',
            f'- domain: {row["domain"]}',
            f'- project_dir: {row["project_dir"]}',
            f'- case_path: {row["case_path"]}',
            "- why: term or explicit match; inspect linked case before reuse.",
            f'- summary: {row["summary"]}',
            "",
        ]
    if not rows:
        out.append("No matching historical case found, or no case index exists. Proceed without forced memory reuse.")

    text = "\n".join(out)
    if args.write_context:
        Path(args.write_context).write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
