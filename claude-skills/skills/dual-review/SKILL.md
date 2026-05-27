---
name: dual-review
description: Use before merging, shipping, or handing off code when an independent Claude Code review packet or optional second reviewer pass is needed.
---

# Dual Review
## Claude Code Adaptation

- This copy is prepared for Claude Code personal or project skills.
- Resolve bundled files relative to ${CLAUDE_SKILL_DIR} when Claude Code exposes it; otherwise use the local skill directory.
- Map old agent/tool wording to the closest Claude Code capability by intent.

## Inputs
- Git diff or patch.
- Product spec, `AGENTS.md`, test results, screenshots, and release notes when available.
- The gate being reviewed: G5 frontend, G6 backend, G7 QA, or G9 release.

## Workflow
1. Collect diff, rules, product spec, and verification output into a review packet.
2. Run an independent Claude Code review in a fresh context when available.
3. Optionally run an external reviewer only if it is configured and the user asks for it.
4. Merge findings by severity: blocker, major, minor, style.
5. Require reproduction steps or a test command for blocker/major findings.
6. Save representative bugs only when Wyatt explicitly asks to archive them.

## Hard rules
- The agent that wrote the code must not be the only reviewer.
- Do not merge or ship if blocker findings remain.
- Do not paste secrets, `.env`, account files, private cookies, or company raw data into review packets.
- Review reports must separate observed evidence from inference.
