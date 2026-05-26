---
name: dual-review
description: Use before merging or shipping code. Runs or prepares independent Claude Code and Codex review passes, then merges findings into a single actionable review report.
version: 0.1.0
author: WyattJY Hermes local workflow
---
# Dual Review

## Inputs
- Git diff or patch.
- Product spec, `AGENTS.md`, test results, screenshots, and release notes when available.
- The gate being reviewed: G5 frontend, G6 backend, G7 QA, or G9 release.

## Workflow
1. Collect diff, rules, product spec, and verification output into a review packet.
2. Run Claude Code review in a fresh context when available.
3. Run Codex review in a fresh context when available.
4. Merge findings by severity: blocker, major, minor, style.
5. Require reproduction steps or a test command for blocker/major findings.
6. Save representative bugs to `memory/bugs/` and SQLite `bug_cases`.

## Hard rules
- The agent that wrote the code must not be the only reviewer.
- Do not merge or ship if blocker findings remain.
- Do not paste secrets, `.env`, account files, private cookies, or company raw data into review packets.
- Review reports must separate observed evidence from inference.

