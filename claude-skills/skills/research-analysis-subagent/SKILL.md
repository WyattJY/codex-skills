---
name: research-analysis-subagent
description: "Use when processing one paper directory for the research workflow and writing Analysis_Detail.md from paper.md plus paper_artifacts"
---


## Claude Code Migration Notes

This skill was migrated from the local Codex skill registry for Claude Code. Use it as a Claude Code `SKILL.md` skill. Some source text may name Codex-only tools or channels; in Claude Code, use the closest available Claude Code tool, shell command, MCP/plugin integration, or local helper script. Keep secrets in Keychain, environment variables, or authenticated CLIs only.

# Research Analysis Subagent

Canonical implementation lives at:
`G:\Wyatt\HK_intership\.agent\skills\research-analysis-subagent`

Use this skill only for a single paper directory at a time.

Required steps:

1. Read the analysis prompt at:
   `G:\Wyatt\HK_intership\.agent\skills\research-analysis-subagent\assets\analysis_prompt.md`
2. Read `${paper_dir}\paper.md`.
3. Read all images under `${paper_dir}\paper_artifacts`.
4. Write `${paper_dir}\Analysis_Detail.md`.
5. Remind the user to verify formula and image rendering.

Do not batch multiple papers in one invocation.
