---
name: wyatt-product-team
description: Use when Wyatt asks for product-manager, technical-team, architecture, UI, frontend, backend, QA, reviewer, release, research, paper-reading, memory-archiving, or multi-role product workflow help in Claude Code.
---


# Wyatt Product Team
## Claude Code Adaptation

- This copy is prepared for Claude Code personal or project skills.
- Resolve bundled files relative to ${CLAUDE_SKILL_DIR} when Claude Code exposes it; otherwise use the local skill directory.
- Map old agent/tool wording to the closest Claude Code capability by intent.

## Purpose

Use this skill as the Claude Code entrypoint for Wyatt's Hermes-style product team workflow. It does not create long-lived Hermes profiles. It maps the original role-agent documents into Claude Code-readable role guidance and routes work through the smallest useful set of roles.

## Core Flow

1. Start with scope control: identify the user's goal, target user, non-goals, acceptance criteria, and likely gate.
2. Load at most the references needed for the current gate:
   - G0 and closeout: `references/agents/wyatt-memory-archivist.md`
   - G1/G2 product clarity: `references/agents/wyatt-product-manager.md`
   - G2/G6 architecture and backend shape: `references/agents/wyatt-system-architect.md`
   - G3/G4 UI direction: `references/agents/wyatt-ui-designer.md`
   - G5 frontend implementation: `references/agents/wyatt-frontend-engineer.md`
   - G6 backend implementation: `references/agents/wyatt-backend-engineer.md`
   - G7/G8 QA and review: `references/agents/wyatt-qa-engineer.md` and `references/agents/wyatt-reviewer-bot.md`
   - G9 release/package: `references/agents/wyatt-devops-release.md`
   - Research and papers: `references/agents/wyatt-research-analyst.md` or `references/agents/wyatt-scholar.md`
   - Hikvision codec stage work: `references/agents/wyatt-hikvision-codec-stage1.md`
3. For multi-role work, state the role split briefly, then execute. Use Claude Code subagents only when the user asks for parallel agents or when independent workstreams can run safely in parallel.
4. Keep outputs concrete: update repo files, write specs, create task slices, run verification, and report exact paths.

## Routing Notes

Use the Claude Code routing reference at `references/product-team-routing.md`. It is the canonical routing file for this migrated T7 skill.

Use the migrated Wyatt skills when they match the task:

- `$case-router` before large, history-sensitive work.
- `$backend-blueprint` before backend implementation.
- `$dual-review` for two-pass review.
- `$ship-package` before packaging or release.
- `$prompt-rewriter` for improving prompts.
- `$paper-digest` for paper tracking and research routines.
- `$ui-trends-watcher` for UI direction and trend review.

## Guardrails

- Do not invent requirements when local docs or the user's wording are available.
- Do not write secrets, tokens, cookies, `.env` contents, session files, Weixin identifiers, or private company data into skills, memory, docs, or reports.
- Do not turn every role into a permanent profile. Roles are task guidance, not persistent identities.
- If a task touches UI, product, backend, and release at once, slice it into gates instead of letting all roles edit the same files.
