---
name: paper-digest
description: Daily research routine for Wyatt. Selects one paper, technical doc, video, or repository relevant to the current multimodal/model-training watchlist and produces a 500-word idea with links and a concrete experiment.
version: 0.1.0
author: WyattJY Hermes local workflow
---
# Paper Digest
## Morning workflow
1. Read the internship context index at `/Volumes/T7 Shield/hermes/home/memory/research/INTERNSHIP_CONTEXT/internship_context_index.md` (this is the canonical path; do NOT look for it under `~/.hermes-wyatt/INTERNSHIP_CONTEXT/`). Also check `research-watchlist.md` if it exists (it may not — skip if absent).
2. Query the dedupe database at `/Volumes/T7 Shield/hermes/home/memory/research/research_dedupe.sqlite` to see what was already covered by previous runs. See `references/dedupe-db-schema.md` for the schema.
3. Scan the local internship research folder before trusted external sources.
4. Rank by relevance to `/Volumes/T7 Shield/02_Research_Papers_Reports/实习`, not generic popularity.
5. Produce one 500-word idea only.
6. Include why it matters, experiment, required data/code, expected signal, stop condition, references.
7. Write the report to `/Volumes/T7 Shield/hermes/home/memory/research/REPORTS/daily-past-week-YYYYMMDD.md` and update the dedupe DB.
8. Push through configured Weixin/WeCom channel only after isolated gateway is configured.
9. Record Wyatt feedback: 有用 / 无用 / 深读.
## Deep-read workflow
If Wyatt replies 深读, write PAPER_CARD and link it to active cases.

## External search patterns
### Preferred approach: Python in execute_code
Do NOT use terminal `curl | python3` pipes — the security scanner rejects them and arXiv rate-limits quickly.
Instead use `execute_code` with Python `urllib`:

- **Semantic Scholar**: JSON API, 1 req/sec limit. Good for initial discovery. Add `time.sleep(2)` between queries.
- **arXiv**: Atom XML, ~1 req / 3 sec limit. Use after Semantic Scholar for missing topics. Parse with `xml.etree.ElementTree`.
- **429 handling**: If either API returns 429, stop and report "external scan inconclusive" rather than retrying. Base report on available results + HK corpus.

### Dedupe DB
Path: `/Volumes/T7 Shield/hermes/home/memory/research/research_dedupe.sqlite`
Schema: `sources(stable_id, source_type, title, url, published_at, summary, topic, content_hash, first_seen_at, last_seen_at)`, `runs(run_id, kind, window_start, window_end, created_at, status, source_count, report_path)`, `run_sources(run_id, source_id, rank)`. Always `.schema` before inserting — column names differ from naive expectations.

### Report location
Write report to `/Volumes/T7 Shield/hermes/home/memory/research/REPORTS/daily-past-week-YYYYMMDD.md`.

## Hard rules
- Produce exactly one research idea per run; do not dump generic AI news or multiple papers.
- For Weixin/WeCom pushes to Wyatt, write the delivered digest in Chinese and translate paper/source content into Chinese; keep original paper titles and key technical terms in parentheses when useful.
- Bind the idea to the active watchlist, a historical case, and one concrete file/directory under the T7 internship research folder when possible.
- Include a concrete experiment, required data/code, expected signal, stop condition, and references.
- Never request or export raw company data; use screenshots, logs, RUN_CARD, DATA_CARD, or aggregate statistics.
- Push through Weixin/WeCom only after an isolated gateway/HERMES_HOME is configured and token double-running is ruled out.

## External API queries: pitfalls
- **Do NOT use `terminal` (`curl`) for arXiv or Semantic Scholar API queries.** `curl | python3` gets blocked by the security scanner (pipe-to-interpreter), and standalone `curl` to arXiv frequently times out or returns 429.
- **Use `execute_code` with Python `urllib.request` instead.** It has a 120s timeout and avoids the pipe-to-interpreter block. Space queries ≥3s apart to respect rate limits.
- Semantic Scholar returns JSON (preferred when arXiv is 429). arXiv returns Atom XML — parse with `xml.etree.ElementTree`.
- Both APIs can rate-limit (429). If all live queries fail, **do not conclude “no candidates”**. First query the dedupe DB for sources whose `published_at` falls in the requested window, then synthesize from those archived sources + HK/local corpus. Label the live scan as inconclusive/rate-limited. See `references/month-window-fallback.md`.
- The dedupe database lives at `/Volumes/T7 Shield/hermes/home/memory/research/research_dedupe.sqlite`. Schema is documented in `references/dedupe-db-schema.md`.
