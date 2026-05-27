---
name: server-observation-loop
description: Use when Claude Code cannot directly access a server, training job, private dataset, or intranet system and Wyatt must run commands manually then return sanitized logs, screenshots, metrics, or summaries.
---


# Server Observation Loop
## Claude Code Adaptation

- This copy is prepared for Claude Code personal or project skills.
- Resolve bundled files relative to ${CLAUDE_SKILL_DIR} when Claude Code exposes it; otherwise use the local skill directory.
- Map old agent/tool wording to the closest Claude Code capability by intent.

## Workflow

1. Ask for the current goal and the safest available evidence.
2. Produce one minimal command or script for Wyatt to run.
3. Tell Wyatt exactly what output, screenshot, or metric to paste back.
4. Analyze returned evidence as observed facts, likely causes, and next actions.
5. If Wyatt asks to preserve the run, write a RUN_CARD, DATA_CARD, or ERROR_CARD using the bundled script.

## Hard Rules

- Give one minimal command or script at a time.
- Never request raw confidential/company data, credentials, cookies, tokens, or full private datasets.
- Base analysis only on returned evidence and separate observation from inference.
- Prefer sanitized logs, aggregate metrics, screenshots, and summaries.
