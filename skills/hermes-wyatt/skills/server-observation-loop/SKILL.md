---
name: server-observation-loop
description: Use when Hermes cannot access the company server or training data directly and Wyatt must manually run commands, then return screenshots, logs, or aggregate statistics through phone/Weixin.
version: 0.1.0
author: WyattJY Hermes local workflow
---
# Server Observation Loop
## Workflow
1. Ask for current goal and available context.
2. Produce one minimal command or script for Wyatt to run.
3. Tell Wyatt exactly what output, screenshot, or metric to paste back.
4. Analyze returned evidence: observed facts, likely causes, next actions.
5. Update RUN_CARD, DATA_CARD, ERROR_CARD.
6. Never request raw confidential data.
## Hard rules
- Give one minimal command or script at a time, with exact output/screenshot/log evidence to paste back.
- Never request raw confidential/company data, credentials, cookies, tokens, or full private datasets.
- Base analysis only on returned evidence; separate observed facts from inference.
- Update RUN_CARD, DATA_CARD, or ERROR_CARD for every non-trivial training/debug loop.

## Output style
- What I see
- What I infer
- What you should run next
- What to paste back
