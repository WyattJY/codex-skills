---
name: ship-package
description: Use before local release or handoff to prepare reproducible Docker/release/GitHub packages with secret checks, rollback notes, and verification evidence.
---

# Ship Package
## Claude Code Adaptation

- This copy is prepared for Claude Code personal or project skills.
- Resolve bundled files relative to ${CLAUDE_SKILL_DIR} when Claude Code exposes it; otherwise use the local skill directory.
- Map old agent/tool wording to the closest Claude Code capability by intent.

## Workflow
1. Read product spec, release notes, Docker files, README, `.env.example`, and verification output.
2. Run release checks: secret scan, required docs, build/test hints, launch scripts, rollback notes.
3. Write `release_check_report.md` and report final delivery paths.
4. Package only source, docs, scripts, and safe sample data.
5. Exclude `.env`, tokens, sessions, account files, raw company data, caches, and generated secrets.

## Hard rules
- Never ship `.env`, API keys, Weixin tokens, cookies, sessions, or company raw data.
- Do not claim a package is runnable without a fresh verification command.
- Release notes must include exact paths, commands, and known gaps.
- Prefer reproducible scripts over manual Finder-only operations.
