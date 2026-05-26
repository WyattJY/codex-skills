---
name: ship-package
description: Use at G9 Ops to prepare reproducible Docker/release/GitHub handoff packages with secret checks, rollback notes, and verification evidence.
version: 0.1.0
author: WyattJY Hermes local workflow
---
# Ship Package

## Workflow
1. Read product spec, release notes, Docker files, README, `.env.example`, and verification output.
2. Run release checks: secret scan, required docs, build/test hints, launch scripts, rollback notes.
3. Write `release_check_report.md` and update case final delivery paths.
4. Package only source, docs, scripts, and safe sample data.
5. Exclude `.env`, tokens, sessions, account files, raw company data, caches, and generated secrets.

## Hard rules
- Never ship `.env`, API keys, Weixin tokens, cookies, sessions, or company raw data.
- Do not claim a package is runnable without a fresh verification command.
- Release notes must include exact paths, commands, and known gaps.
- Prefer reproducible scripts over manual Finder-only operations.

