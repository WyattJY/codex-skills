---
name: hk-intership
description: Use when Wyatt mentions HK, HK_intership, internship literature survey, reranker papers, Megatron full fine-tuning research, or asks whether the HK literature-review skill was used.
---

# HK Intership Router

## Overview

This is a router skill for Wyatt's HK/intership literature-review workflow. It does not replace the canonical paper skills; it forces the run to use the HK research corpus and the correct paper-to-report stack.

## Canonical Skill Stack

- `research-workflow`: batch paper list, PDF/Markdown corpus, report merge, Word export.
- `research-analysis-subagent`: one paper directory at a time; reads `paper.md` and `paper_artifacts`, then writes `Analysis_Detail.md`.
- `paper-digest`: Weixin-safe daily idea distilled from the HK workflow output.
- `weixin-daily-push`: push only the final safe summary, never credentials.

## External search (rate-limit aware)

When searching arXiv or Semantic Scholar for new papers:
- Use `execute_code` with Python `urllib`, NOT terminal `curl | python3` pipes (security scanner rejects, higher timeout risk).
- Semantic Scholar (JSON, 1 req/sec) for discovery; arXiv (XML, ~1 req/3 sec) to fill gaps.
- If 429 rate-limit hits, stop and mark scan as "inconclusive" — base report on HK corpus evidence.
- Do NOT retry repeatedly; it wastes turns and the cooldown is server-side.
- See paper-digest skill for dedupe DB schema and report paths.

## Mac Paths

- Codex workflow skill: `/Users/jiangyu/.codex/skills/research-workflow/SKILL.md`
- Codex one-paper skill: `/Users/jiangyu/.codex/skills/research-analysis-subagent/SKILL.md`
- HK corpus: `/Volumes/T7 Shield/02_Research_Papers_Reports/megatron_full_ft_hk_research`
- Internship mirror: `/Volumes/T7 Shield/02_Research_Papers_Reports/实习/02_Reranker训练重训微调/megatron_full_ft_hk_research`
- Internship context index: `/Volumes/T7 Shield/hermes/home/memory/research/INTERNSHIP_CONTEXT/internship_context_index.md` (canonical; do NOT look under `~/.hermes-wyatt/INTERNSHIP_CONTEXT/`)
- Dedupe database: `/Volumes/T7 Shield/hermes/home/memory/research/research_dedupe.sqlite` (schema: see `paper-digest` skill reference `references/dedupe-db-schema.md`)
- Report anchors: `paper_list.txt`, `downloads/*/paper.md`, `downloads/*/Analysis_Detail.md`, `hk_merged_report.md`, `hk_merged_report.docx`
- `research-watchlist.md` may not exist yet; skip if absent.

## Workflow

1. Confirm the task is HK/intership literature work rather than a generic daily arXiv scan.
2. Read this skill, then read `research-workflow` and `research-analysis-subagent` if new paper processing or report synthesis is needed.
3. Verify the HK corpus exists and list available paper directories.
4. For each selected paper, prefer existing `Analysis_Detail.md`; if missing, process one paper directory at a time with `research-analysis-subagent`.
5. Merge as a theme-organized expert survey, not a paper-by-paper abstract recap.
6. For Weixin, distill one actionable 500-word idea and link/path to the full HK report.
7. When refreshing external sources, distinguish `no new sources found` from `external scan failed/rate-limited`. If arXiv or another source returns 429/timeout, say the external scan was inconclusive and base the push on HK corpus evidence rather than implying the week had no new papers.
8. Write the generated report into Hermes memory and update dedupe state before scheduling push.

## Hard Rules

- Do not claim "HK skill used" unless this skill was loaded and at least one HK `Analysis_Detail.md` or HK report artifact was read.
- Do not send abstract-only summaries as HK literature research.
- Do not store outputs on `C:` or assume the old Windows `G:\` path exists on Mac; use T7 paths above.
- Do not include API keys, Weixin tokens, cookies, raw company data, or private samples.
- If the output is only a daily Weixin summary, include a full local report path for later deep reading.
- For external API queries (arXiv, Semantic Scholar), use `execute_code` with Python `urllib.request`, not `terminal` (`curl`). See `paper-digest` skill for details on avoiding 429/timeout/security-blocker issues.
