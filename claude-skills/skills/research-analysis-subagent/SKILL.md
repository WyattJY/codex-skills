---
name: research-analysis-subagent
description: Use when processing one paper directory for the research workflow and writing Analysis_Detail.md from paper.md plus paper_artifacts
---

# Research Analysis Subagent

## Claude Code Adaptation

- This copy is prepared for Claude Code personal or project skills.
- Resolve bundled files relative to `${CLAUDE_SKILL_DIR}` when Claude Code exposes it; otherwise use this skill directory.

Use this skill only for a single paper directory at a time.

Required steps:

1. Read `assets/analysis_prompt.md` in full from this skill directory.
2. Read `${paper_dir}\paper.md`.
3. Read all images under `${paper_dir}\paper_artifacts`.
4. Write `${paper_dir}\Analysis_Detail.md` following the prompt specification exactly.
5. Remind the user to verify formula and image rendering.

Do not batch multiple papers in one invocation.
