---
name: case-archiver
description: Use only when Wyatt explicitly asks to archive a completed project, task, or local folder into reusable T7 case notes for future Claude Code workflows.
---


# Case Archiver
## Claude Code Adaptation

- This copy is prepared for Claude Code personal or project skills.
- Resolve bundled files relative to ${CLAUDE_SKILL_DIR} when Claude Code exposes it; otherwise use the local skill directory.
- Map old agent/tool wording to the closest Claude Code capability by intent.

## Workflow

1. Confirm Wyatt asked to write or update durable case memory.
2. Determine case id: `case-{yyyymmdd}-{slug}`.
3. Read only relevant README, AGENTS.md, CLAUDE.md, commits, docs, and visible artifacts.
4. Capture raw requirement, baseline interpretation, actual path, references, turning point, final delivery, final prompt, and representative bugs.
5. Write to a local memory root only after confirmation. Preferred root order:
   - `--memory-root`
   - `CLAUDE_WYATT_MEMORY_HOME or CODEX_WYATT_MEMORY_HOME`
   - `H:/T7/hermes/home/memory`

## Hard Rules

- Do not archive secrets, `.env`, tokens, cookies, sessions, private samples, or raw company data.
- Preserve raw user wording separately from rewritten prompts.
- Do not update long-term memory unless the user explicitly asked for it.
