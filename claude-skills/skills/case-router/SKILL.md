---
name: case-router
description: Use at the start of a non-trivial Wyatt task when relevant historical cases, prior project outcomes, or explicit [[case-...]] references may change scope, implementation, or verification.
---


# Case Router
## Claude Code Adaptation

- This copy is prepared for Claude Code personal or project skills.
- Resolve bundled files relative to ${CLAUDE_SKILL_DIR} when Claude Code exposes it; otherwise use the local skill directory.
- Map old agent/tool wording to the closest Claude Code capability by intent.

## Workflow

1. Parse explicit `[[case-...]]` references first.
2. If no explicit case is provided, decide whether history is likely useful. Skip this skill for pure small talk or tiny one-off commands.
3. Query a local case index only if it exists. Preferred root order:
   - `--memory-root`
   - `CLAUDE_WYATT_MEMORY_HOME or CODEX_WYATT_MEMORY_HOME`
   - `H:/T7/hermes/home/memory`
4. Load at most three cases and state why each is reusable, adjacent, or not useful.
5. If no usable case index exists, say so and proceed without forced memory reuse.

## Hard Rules

- Do not silently load context.
- Do not load more than three cases.
- Do not write memory from this skill.
- Do not print secrets, `.env` contents, tokens, cookies, sessions, or raw company data.
