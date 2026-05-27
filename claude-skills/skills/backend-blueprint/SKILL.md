---
name: backend-blueprint
description: Use when product-builder needs API, DB, auth, error model, caching, deployment, and backend task breakdown before implementation.
---

# Backend Blueprint
## Claude Code Adaptation

- This copy is prepared for Claude Code personal or project skills.
- Resolve bundled files relative to ${CLAUDE_SKILL_DIR} when Claude Code exposes it; otherwise use the local skill directory.
- Map old agent/tool wording to the closest Claude Code capability by intent.

## Workflow
1. Read `requirements.md`, `design.md`, frontend data states, and security constraints.
2. Produce `API_SPEC.md`, `DB_SCHEMA.md`, `ERROR_MODEL.md`, and backend task slices.
3. Define auth, permissions, rate limits, audit logs, concurrency assumptions, and rollback points.
4. Keep endpoint contracts stable before G6 backend implementation starts.
5. Link decisions back to `MEMORY_CONTEXT.md` and relevant cases when available.

## Hard rules
- Do not implement backend code before API contract and DB schema are clear.
- Do not store secrets in code, docs, screenshots, or memory.
- Prefer boring, maintainable infrastructure over new dependencies unless the project demands them.
- Every non-trivial error path needs a visible test or manual verification command.
