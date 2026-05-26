# Month-window fallback when live paper APIs are rate-limited

Use this when Wyatt asks for “近一个月/近七天/本周文献” and Semantic Scholar or arXiv returns 429/timeout.

## Durable lesson
Do **not** report “no candidates” just because the live API query failed. That confuses API health with literature availability. Instead:

1. Mark the live external scan as `inconclusive` or `rate-limited`.
2. Query the local dedupe DB for sources already archived in the requested date window.
3. Synthesize from archived sources + HK/local corpus, clearly labeling coverage limits.
4. Save the report path and do not fabricate “new” papers beyond archived evidence.

## Dedupe DB query pattern

```python
import sqlite3
conn = sqlite3.connect('/Volumes/T7 Shield/hermes/home/memory/research/research_dedupe.sqlite')
conn.row_factory = sqlite3.Row
rows = [dict(r) for r in conn.execute('''
SELECT stable_id, source_type, title, url, published_at, summary, topic,
       first_seen_at, last_seen_at, delivered_at
FROM sources
WHERE substr(published_at,1,10) >= ? AND substr(published_at,1,10) <= ?
ORDER BY published_at DESC
LIMIT 80
''', (window_start_date, window_end_date))]
conn.close()
```

## Report wording

Use language like:

- “实时拉 Semantic Scholar / arXiv 时触发 429，因此这不是完整全网扫描。”
- “下面基于本地 dedupe DB 已归档且落在该时间窗内的来源 + HK/实习语境做可靠复盘。”
- “不要把 API 失败写成没有新文献。”

## Ranking heuristic
For Wyatt’s internship/reranker workflow, prioritize archived rows containing:

- reranker / reranking / retrieval / GenRetrieval
- vision-language / VLM / LVLM / multimodal / cross-modal
- fine-tuning / forgetting / continual / LoRA
- hard negative / pairwise / Recall@K / nDCG
- Qwen / Qwen-VL / Megatron / vLLM

Then map the month’s papers to one concrete experiment rather than dumping a bibliography.
