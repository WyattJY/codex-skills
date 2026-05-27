---
name: hermes-wyatt-workflow
description: "Use when Wyatt mentions Hermes, WyattJY local multi-agent workflow, Codex/Claude Code routing, product-team subagents, local memory, Weixin research reports, internship literature review, or Hikvision codec onboarding."
---


## Claude Code Migration Notes

This skill was migrated from the local Codex skill registry for Claude Code. Use it as a Claude Code `SKILL.md` skill. Some source text may name Codex-only tools or channels; in Claude Code, use the closest available Claude Code tool, shell command, MCP/plugin integration, or local helper script. Keep secrets in Keychain, environment variables, or authenticated CLIs only.

Compatibility note: This skill remains intentionally Wyatt-local. It depends on /Users/jiangyu/.hermes-wyatt, /Users/jiangyu/.claude/agents, Hermes memory on T7, and wrapper commands documented in the skill.

# Hermes Wyatt Workflow

## Overview

This is the Codex-side entrypoint for WyattJY's local Hermes workflow. Use it to route work into the existing Hermes/Claude Code agents, memory store, research scheduler, and G0-G9 delivery gates without duplicating or weakening the Hermes rules.

## First Checks

1. Read `/Users/jiangyu/.hermes-wyatt/AGENTS.md` before non-trivial product, research, company, document, training, debug, or delivery work.
2. For product/team work, read `/Users/jiangyu/.hermes-wyatt/agents/PRODUCT_TEAM_ROUTING.md`.
3. When `/Volumes/T7 Shield/hermes-agent-system` exists, run `UV_LINK_MODE=copy uv run python -m hermes_agent_system agents route "<user request>"` from that project before implementation. This is the Codex-side memory-first technical-team router.
4. For literature research, read `/Volumes/T7 Shield/hermes/home/memory/research/INTERNSHIP_CONTEXT/internship_context_index.md` before external search when present.
5. Verify live state before claiming provider, cron, Weixin, Claude Code, or Codex subprocess success.

## Memory Roots

| Purpose | Path |
| --- | --- |
| Workflow home | `/Users/jiangyu/.hermes-wyatt` |
| Hermes memory root | `/Volumes/T7 Shield/hermes/home/memory` |
| Memory symlink | `/Users/jiangyu/.hermes-wyatt/memory` |
| Case SQLite/FTS | `/Volumes/T7 Shield/hermes/home/memory/cases/embeddings.sqlite` |
| Research dedupe SQLite | `/Volumes/T7 Shield/hermes/home/memory/research/research_dedupe.sqlite` |
| Research reports | `/Volumes/T7 Shield/hermes/home/memory/research/REPORTS` |
| Weixin outbox | `/Volumes/T7 Shield/hermes/home/memory/research/WEIXIN_OUTBOX` |
| Research send markers | `/Volumes/T7 Shield/hermes/home/memory/research/.state` |

At the start of non-trivial work, route memory through Hermes `case-router` and load at most 0-3 relevant cases. At closeout, preserve final prompts, turning points, bugs, and reusable cases through `case-archiver` or the memory archivist agent.

## Team Agent Roster

These role agents live under `/Users/jiangyu/.claude/agents/` and are invoked by Hermes/Claude Code, not shown as native Codex UI agents:

| Role | Agent file | Main use |
| --- | --- | --- |
| System architect | `wyatt-system-architect.md` | architecture, data contracts, module boundaries |
| Product manager | `wyatt-product-manager.md` | requirements, PRD, task slicing, UAT routing |
| UI designer | `wyatt-ui-designer.md` | UI concepts, design tokens, component specs, image prompts |
| Frontend engineer | `wyatt-frontend-engineer.md` | approved frontend slices and browser verification |
| Backend engineer | `wyatt-backend-engineer.md` | APIs, DB schema, services, integration |
| QA engineer | `wyatt-qa-engineer.md` | acceptance checks, regression checks, gap reports |
| Reviewer bot | `wyatt-reviewer-bot.md` | independent code and risk review |
| DevOps release | `wyatt-devops-release.md` | packaging, launch, rollback, reproducible release |
| Research analyst | `wyatt-research-analyst.md` | weekly scans, dedupe, summaries |
| Scholar | `wyatt-scholar.md` | paper cards and deep research |
| Memory archivist | `wyatt-memory-archivist.md` | case, bug, final-prompt, FTS updates |
| Hikvision stage one | `wyatt-hikvision-codec-stage1.md` | C/video codec onboarding, latency, safe reporting |

## Model Routing

Do not expose keys or `.env` contents. Use these routing rules only as task intent:

| Work type | Model |
| --- | --- |
| Architecture, product strategy, UI system design | `claude-opus-4-7-think` through AIHubMix |
| Small implementation, tests, docs, ops | `deepseek-v4-pro` through AIHubMix |
| Codex default and Hermes default provider | `openai-codex` / `gpt-5.5` unless explicitly overridden |
| UI draft image generation | `gpt-image-2` through CPA Lobewyatt |

Claude Code's interactive `/model` menu is not the source of truth for custom AIHubMix model IDs. For standalone sessions, prefer the wrapper commands documented in `/Users/jiangyu/.hermes-wyatt/AGENTS.md`.

## Product Work Flow

For product, app, dashboard, engineering, or UI work:

1. Run or inspect `/Users/jiangyu/.hermes-wyatt/bin/wyatt-product-team-flow` to create the G0-G9 project workspace when a new Hermes project is needed.
2. Follow G0-G9 from `/Users/jiangyu/.hermes-wyatt/AGENTS.md`.
3. Use architecture/product/UI roles before implementation when the task is not a small isolated fix.
4. Use frontend/backend/QA/reviewer/devops roles only after the matching gate artifacts exist.
5. Keep each diff bounded and verify with available lint, type, test, browser, or runtime checks before claiming completion.

## Research Flow

For internship, HK, reranker, Megatron full fine-tuning, Qwen/Qwen-VL/Navit, vLLM, or literature-review work:

1. Load Hermes `hk-intership` first when the task mentions HK, internship literature review, or the user asks whether the HK research skill was used.
2. Use the Codex `research-workflow` and `research-analysis-subagent` skills when generating paper reports, processing paper directories, or exporting Word research reports.
3. Check `/Volumes/T7 Shield/hermes/home/memory/research/research_dedupe.sqlite` before repeating literature.
4. Prefer `/Volumes/T7 Shield/02_Research_Papers_Reports/实习` as the local context root.
5. Before claiming Weixin delivery, check Hermes cron, `.state/morning-send-YYYYMMDD.done`, `WEIXIN_OUTBOX/*.pending.weixin.md`, and report `delivered_at` state.

## Hikvision Stage-One Flow

When Wyatt mentions Hikvision, 海康威视, intelligent algorithm department, C video codec, encode/decode, RTSP, H264/H265, FFmpeg, latency, response, or stage-one reporting:

1. Load `/Users/jiangyu/.hermes-wyatt/skills/hikvision-codec-stage1/SKILL.md`.
2. Use `/Users/jiangyu/.claude/agents/wyatt-hikvision-codec-stage1.md` for architecture, learning plan, debugging strategy, and report synthesis.
3. Store only sanitized task cards, aggregate metrics, screenshot descriptions, and lessons. Never store company source code, raw video, streams, credentials, private docs, or customer data.

## Useful Verification Commands

```bash
python3 /Users/jiangyu/.hermes-wyatt/bin/validate_wyatt_workflow.py
python3 /Users/jiangyu/.hermes-wyatt/tests/test_wyatt_workflow.py -v
hermes --profile default cron list --all
```

For Claude Code subprocess calls, use `/Users/jiangyu/.hermes-wyatt/bin/wyatt-claude-code`. For Codex subprocess calls, use `/Users/jiangyu/.hermes-wyatt/bin/wyatt-codex-exec`.

## Hard Rules

- Never write API keys, Weixin tokens, `.env` contents, cookies, session files, or raw company data into Codex memory, Hermes memory, reports, or chat.
- Do not infer that Weixin delivered a report from report existence alone.
- Do not repeat research items already recorded in the dedupe database.
- Do not make every role a long-lived Hermes profile; the technical-team roster is a task-role layer.
- When local state matters, inspect the real file, cron, wrapper, or runtime result before answering.
