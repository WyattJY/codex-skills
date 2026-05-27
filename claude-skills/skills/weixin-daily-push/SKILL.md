---
name: weixin-daily-push
description: Use when Wyatt asks Claude Code to prepare a safe Weixin/WeCom-ready daily research idea or workflow notification without sending it or exposing token-bearing gateway state.
---


# Weixin Daily Push
## Claude Code Adaptation

- This copy is prepared for Claude Code personal or project skills.
- Resolve bundled files relative to ${CLAUDE_SKILL_DIR} when Claude Code exposes it; otherwise use the local skill directory.
- Map old agent/tool wording to the closest Claude Code capability by intent.

## Workflow

1. Read the chosen daily idea, RUN_CARD, ERROR_CARD, release summary, or explicit source file.
2. Compress it into a concise private-message payload.
3. Write a pending outbox file and report its exact path.
4. Do not send a message, start a gateway, restart a token-bearing service, or mark delivery complete unless Wyatt explicitly asks and the channel is verified in the current environment.

## Hard Rules

- Never print or store `WEIXIN_TOKEN`, account JSON, cookies, sessions, pairing files, or `.env` contents.
- Do not run the same token from multiple runtimes.
- A generated outbox file is not proof of delivery.
- If delivery cannot be verified, say the message was prepared but not sent.
