---
name: prompt-rewriter
description: Use at project close or after a major correction to rewrite the final prompt that would have solved the task cleanly from the start.
---

# Prompt Rewriter
## Claude Code Adaptation

- This copy is prepared for Claude Code personal or project skills.
- Resolve bundled files relative to ${CLAUDE_SKILL_DIR} when Claude Code exposes it; otherwise use the local skill directory.
- Map old agent/tool wording to the closest Claude Code capability by intent.
## Workflow
1. Read raw requirement, baseline interpretation, actual path, user feedback, final deliverable, and representative bugs.
2. Identify where the first prompt under-specified constraints, taste, evidence, file paths, or success criteria.
3. Write a concise final prompt with scope, artifacts, constraints, checks, and stop conditions.
4. Save to a local output file. Update case memory only if Wyatt explicitly asks.
## Hard rules
- Do not rewrite history; preserve raw wording separately.
- Include verification commands or acceptance criteria when relevant.
