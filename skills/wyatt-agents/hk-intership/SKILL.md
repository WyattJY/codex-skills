---
name: hk-intership
description: Use when working in the HK_intership workspace, routing research tasks to the correct local skill, or needing the G-drive runtime and repo helper tools used by that workspace
---

# HK Intership

Canonical implementation lives at:
`G:\Wyatt\HK_intership\.agent\skills\hk-intership`

Use this as the Codex entry skill for the HK_intership workspace.

1. Read the canonical skill at:
   `G:\Wyatt\HK_intership\.agent\skills\hk-intership\SKILL.md`
2. For end-to-end paper-to-report work, use:
   `G:\Wyatt\HK_intership\.agent\skills\research-workflow`
   Final PDF export can use:
   `G:\Wyatt\.agents\skills\lovstudio-md2pdf\scripts\md2pdf.py`
3. For expert-survey-style final reports, use:
   `G:\Wyatt\HK_intership\.agent\skills\expert-survey-report`
4. For single-paper analysis work, use:
   `G:\Wyatt\HK_intership\.agent\skills\research-analysis-subagent`
5. Before running the research workflow, verify the G-drive runtime with:
   `powershell -ExecutionPolicy Bypass -File "G:\Wyatt\HK_intership\.agent\tools\verify-research-runtime.ps1"`
6. Prefer `G:\` paths. Avoid saving to `C:\` unless the user explicitly requests it.
