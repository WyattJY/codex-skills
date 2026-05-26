---
name: case-archiver
description: Use when a project, task, or legacy local folder needs to be archived into Wyatt's Hermes memory. Captures raw requirement, solution path, references, user-attitude turning point, final delivery, representative bugs, and rewritten final prompt.
version: 0.1.0
author: WyattJY Hermes local workflow
---
# Case Archiver
## Workflow
1. Determine case id: case-{yyyymmdd}-{slug}.
2. Read README, AGENTS.md, CLAUDE.md, commits, docs, and visible artifacts.
3. Write PROJECT_CARD, TIMELINE, REFERENCES, USER_FEEDBACK, BUG_CASES, FINAL_PROMPT.
4. Preserve raw user wording where available; do not beautify it.
5. Update memory/cases/INDEX.md.
6. Trigger case-router re-embedding/FTS update.
## Hard rules
- Never store secrets, tokens, .env, cookies, or raw company data.
- Section 5 user-attitude turning point is mandatory when known.
- Section 7 final rewritten prompt is mandatory at project close.
