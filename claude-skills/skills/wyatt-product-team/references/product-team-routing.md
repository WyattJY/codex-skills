# Wyatt Product Team Routing For Claude Code

Use these roles as lenses/checkpoints inside Claude Code. Do not create long-lived Hermes profiles for each role.

| Gate | Role Reference | Purpose |
| --- | --- | --- |
| G0 | `agents/wyatt-memory-archivist.md` | Load only relevant prior context; archive only when explicitly asked. |
| G1-G2 | `agents/wyatt-product-manager.md` | Requirements, target user, non-goals, acceptance criteria, task slicing. |
| G2-G6 | `agents/wyatt-system-architect.md` | Architecture, module boundaries, data contracts, risks. |
| G3-G4 | `agents/wyatt-ui-designer.md` | UI direction, design tokens, component specs. |
| G5 | `agents/wyatt-frontend-engineer.md` | Frontend implementation slices and states. |
| G6 | `agents/wyatt-backend-engineer.md` | API, DB, auth, errors, deployment. |
| G7-G8 | `agents/wyatt-qa-engineer.md`, `agents/wyatt-reviewer-bot.md` | Verification, review findings, feedback routing. |
| G9 | `agents/wyatt-devops-release.md` | Release package, launch checks, rollback notes. |

Use Claude Code subagents only when the user explicitly asks for parallel agents or when independent workstreams can safely run in parallel.
