---
name: research-analysis-subagent
description: Use when processing one paper directory for the research workflow and writing Analysis_Detail.md from paper.md plus paper_artifacts
---

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
