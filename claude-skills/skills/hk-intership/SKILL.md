---
name: hk-intership
description: Use when Wyatt mentions HK, HK_intership, internship literature survey, reranker papers, Megatron full fine-tuning research, or asks whether the HK literature-review workflow was used.
---


# HK Internship Router
## Claude Code Adaptation

- This copy is prepared for Claude Code personal or project skills.
- Resolve bundled files relative to ${CLAUDE_SKILL_DIR} when Claude Code exposes it; otherwise use the local skill directory.
- Map old agent/tool wording to the closest Claude Code capability by intent.

## Purpose

Route HK internship literature-review work through the correct local T7 corpus and paper-analysis stack. This is not a generic arXiv-news skill.

## Local Paths

- Preferred HK workspace: `H:/T7/Wyatt/HK_intership`
- Research corpus: `H:/T7/megatron_full_ft_hk_research`
- Optional memory root: `H:/T7/hermes/home/memory`
- Existing Claude Code paper skills usually live under the active Claude Code skill roots; use `/research-workflow` and `/research-analysis-subagent` when available.

## Workflow

1. Confirm the task is HK/internship literature work, not a generic daily paper scan.
2. Verify the local HK paths that exist before planning.
3. Prefer existing `paper.md`, `paper_artifacts`, `Analysis_Detail.md`, `hk_merged_report.md`, and `hk_merged_report.docx`.
4. If new paper processing is needed, process one paper directory at a time using the paper-analysis workflow.
5. Merge as a theme-organized expert survey, not a paper-by-paper abstract recap.
6. If external search is needed, use available Claude Code web/search tools or Python `urllib.request`; respect 429/rate limits and label failed scans as inconclusive.

## Hard Rules

- Do not claim "HK workflow used" unless this skill was loaded and at least one HK artifact was read.
- Do not send abstract-only summaries as HK literature research.
- Keep outputs on `H:/T7` unless Wyatt names another target.
- Do not include API keys, Weixin tokens, cookies, raw company data, or private samples.
