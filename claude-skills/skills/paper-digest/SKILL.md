---
name: paper-digest
description: Use when Wyatt asks for a daily research idea, paper watchlist digest, reranker/multimodal model reading routine, or one-paper-to-experiment summary.
---


# Paper Digest
## Claude Code Adaptation

- This copy is prepared for Claude Code personal or project skills.
- Resolve bundled files relative to ${CLAUDE_SKILL_DIR} when Claude Code exposes it; otherwise use the local skill directory.
- Map old agent/tool wording to the closest Claude Code capability by intent.

## Workflow

1. Prefer local T7/HK research material before live web search.
2. Use the local research root from `--research-root`, `CLAUDE_WYATT_RESEARCH_ROOT or CODEX_WYATT_RESEARCH_ROOT`, or `H:/T7/Wyatt/HK_intership`.
3. Use the optional memory root from `--memory-root`, `CLAUDE_WYATT_MEMORY_HOME or CODEX_WYATT_MEMORY_HOME`, or `H:/T7/hermes/home/memory`.
4. Produce exactly one actionable research idea: why it matters, experiment, required data/code, expected signal, stop condition, and references.
5. For external searches, use available Claude Code web/search tools or Python `urllib.request`; respect rate limits and stop on 429 instead of retrying aggressively.
6. Write reports locally only when asked or when running the bundled script. Do not send Weixin/WeCom messages from this skill.

## Hard Rules

- Do not dump generic AI news or multiple papers.
- Do not request or export raw company data.
- Keep private summaries local and report exact saved paths.
- If live search fails, say it is inconclusive and synthesize only from available local files.
