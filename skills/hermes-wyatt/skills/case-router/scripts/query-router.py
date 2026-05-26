#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import sqlite3
from pathlib import Path


def classify(q: str) -> str:
    low = q.lower()
    if any(x in low for x in ['ui', 'prd', '前端', '后端', '产品', 'app', 'web']):
        return 'product'
    if any(x in low for x in ['论文', 'paper', 'research', '模型', '训练', 'multimodal', 'qwen', 'vl', 'reranker']):
        return 'research/training'
    if any(x in low for x in ['bug', '报错', 'error', 'review', 'test', 'ci']):
        return 'debugging/review'
    return 'misc'


def terms_for(q: str):
    terms = re.findall(r'[A-Za-z0-9_\-]+|[\u4e00-\u9fff]{2,}', q.lower())
    synonyms = []
    if '训练' in q or 'model' in q.lower():
        synonyms += ['training', 'train', '模型']
    if '多模态' in q or 'multimodal' in q.lower():
        synonyms += ['vl', 'vision', '视觉', 'multimodal']
    return list(dict.fromkeys(terms + synonyms))


def score_row(row, terms):
    text = ' '.join(str(row[k] or '') for k in row.keys()).lower()
    score = 0
    for t in terms:
        tl = t.lower()
        if tl in text:
            score += 3 if tl in str(row['title']).lower() or tl in str(row['project_dir']).lower() else 1
    if row['domain'] in ('training', 'research'):
        score += 1
    return score


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('query', nargs='*')
    parser.add_argument('--memory-root', default=os.environ.get('HERMES_MEMORY_HOME', '/Volumes/T7 Shield/hermes/home/memory'))
    parser.add_argument('--top-k', type=int, default=3)
    parser.add_argument('--write-context', default='')
    args = parser.parse_args()

    query = ' '.join(args.query).strip()
    if not query:
        raise SystemExit('Usage: query-router.py "new requirement text"')

    db = Path(args.memory_root) / 'cases' / 'embeddings.sqlite'
    explicit = re.findall(r'\[\[(case-[A-Za-z0-9_-]+)\]\]', query)
    rows = []

    if db.exists():
        conn = sqlite3.connect(str(db))
        conn.row_factory = sqlite3.Row
        if explicit:
            qmarks = ','.join('?' for _ in explicit)
            rows = conn.execute(f'SELECT * FROM cases WHERE case_id IN ({qmarks})', explicit).fetchall()
        else:
            all_rows = conn.execute('SELECT rowid, * FROM cases').fetchall()
            row_map = {r['case_id']: r for r in all_rows}
            terms = terms_for(query)
            fts_rows = []
            if terms:
                # FTS5 first, then Python term scoring as fallback/secondary ranker.
                quoted_terms = []
                for t in terms[:8]:
                    clean = t.replace('"', '""')
                    if clean:
                        quoted_terms.append(f'"{clean}"')
                fts_query = ' OR '.join(quoted_terms)
                if fts_query:
                    try:
                        fts_ids = [
                            r['case_id']
                            for r in conn.execute(
                                'SELECT case_id FROM case_fts WHERE case_fts MATCH ? ORDER BY bm25(case_fts) LIMIT ?',
                                (fts_query, args.top_k),
                            ).fetchall()
                        ]
                        fts_rows = [row_map[cid] for cid in fts_ids if cid in row_map]
                    except sqlite3.DatabaseError:
                        fts_rows = []
            fts_case_ids = {r['case_id'] for r in fts_rows}
            scored = [(score_row(r, terms) + (5 if r['case_id'] in fts_case_ids else 0), r) for r in all_rows]
            scored = [x for x in scored if x[0] > 0]
            scored.sort(key=lambda x: (x[0], x[1]['updated_at']), reverse=True)
            rows = []
            seen_ids = set()
            for r in fts_rows + [r for _s, r in scored]:
                if r['case_id'] in seen_ids:
                    continue
                rows.append(r)
                seen_ids.add(r['case_id'])
                if len(rows) >= args.top_k:
                    break
            if not rows:
                rows = conn.execute('SELECT rowid, * FROM cases ORDER BY updated_at DESC LIMIT ?', (args.top_k,)).fetchall()
        conn.close()

    out = [
        '# MEMORY_CONTEXT',
        '',
        f'- query: {query}',
        f'- classified_intent: {classify(query)}',
        f'- loaded_cases: {min(len(rows), args.top_k)} (max {args.top_k})',
        '',
    ]
    for r in rows[: args.top_k]:
        out += [
            f'## {r["case_id"]}: {r["title"]}',
            f'- domain: {r["domain"]}',
            f'- project_dir: {r["project_dir"]}',
            f'- case_path: {r["case_path"]}',
            '- why: term/explicit match; inspect linked case before reuse.',
            f'- summary: {r["summary"]}',
            '',
        ]
    if not rows:
        out.append('No matching historical case found. Proceed without forced memory reuse, but archive the outcome if non-trivial.')

    text = '\n'.join(out)
    if args.write_context:
        Path(args.write_context).write_text(text, encoding='utf-8')
    print(text)


if __name__ == '__main__':
    main()
