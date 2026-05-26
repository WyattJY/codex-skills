# Dedupe Database Schema

Location: `/Volumes/T7 Shield/hermes/home/memory/research/research_dedupe.sqlite`

## Tables

### sources
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Auto-increment PK |
| stable_id | TEXT | Unique ID (e.g. `arxiv:2601.04720`, `hk-intership:1909.08053`) |
| source_type | TEXT | `arxiv`, `hk-intership`, etc. |
| title | TEXT | Paper title |
| url | TEXT | Link to paper |
| published_at | TEXT | ISO timestamp |
| summary | TEXT | Abstract or snippet |
| topic | TEXT | Research topic tag |
| content_hash | TEXT | SHA-256 of title+summary |
| first_seen_at | TEXT | ISO timestamp |
| last_seen_at | TEXT | ISO timestamp |
| delivered_at | TEXT | When pushed to user (nullable) |

### runs
| Column | Type | Description |
|--------|------|-------------|
| run_id | TEXT | Unique run ID (e.g. `daily-past-week-20260517`) |
| kind | TEXT | `daily-past-week`, `deep-read`, etc. |
| window_start | TEXT | ISO timestamp |
| window_end | TEXT | ISO timestamp |
| created_at | TEXT | ISO timestamp |
| status | TEXT | `active`, `superseded` |
| source_count | INTEGER | Number of sources in this run |
| report_path | TEXT | Path to the generated report |
| delivered_at | TEXT | When pushed to user (nullable) |

### run_sources
| Column | Type | Description |
|--------|------|-------------|
| run_id | TEXT | FK to runs |
| source_id | INTEGER | FK to sources.id |
| rank | INTEGER | Ordinal position in the run |

## Insert pattern

```python
# Insert a new source
conn.execute("""
    INSERT OR IGNORE INTO sources
    (stable_id, source_type, title, url, published_at, summary, topic, content_hash, first_seen_at, last_seen_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (stable_id, stype, title, url, pub_at, summary, topic, content_hash, now, now))

# Create a new run
conn.execute("""
    INSERT OR REPLACE INTO runs
    (run_id, kind, window_start, window_end, created_at, status, source_count, report_path)
    VALUES (?, 'daily-past-week', ?, ?, ?, 'active', ?, ?)
""", (run_id, window_start, window_end, now, source_count, report_path))

# Link source to run (use sources.id NOT stable_id)
cur = conn.execute("SELECT id FROM sources WHERE stable_id = ?", (stable_id,))
row = cur.fetchone()
if row:
    conn.execute("INSERT OR IGNORE INTO run_sources (run_id, source_id, rank) VALUES (?, ?, ?)",
                (run_id, row[0], rank))
```

## Notes
- `sources` primary key is `id` (integer), not `stable_id`. Use `stable_id` for lookups, `id` for joins.
- `runs` uses `kind` not `run_type`.
- The schema used `first_seen_at`/`last_seen_at`, not `created_at`/`updated_at`.
- The schema uses `published_at` (not `pub_date`) and `summary` (not `snippet`).
