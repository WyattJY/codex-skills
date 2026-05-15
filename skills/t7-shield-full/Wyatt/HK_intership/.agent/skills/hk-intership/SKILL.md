---
name: hk-intership
description: Use when working in the HK_intership workspace, routing research tasks to the correct local skill, or needing the G-drive runtime and repo helper tools used by that workspace
---

# HK Intership Workspace Router

This skill is the entry point for the `G:\Wyatt\HK_intership` workspace.

Canonical local skills live at:
- `G:\Wyatt\HK_intership\.agent\skills\research-workflow`
- `G:\Wyatt\HK_intership\.agent\skills\research-analysis-subagent`
- `G:\Wyatt\HK_intership\.agent\skills\expert-survey-report`

Repo helper tools live at:
- `G:\Wyatt\HK_intership\.agent\tools\verify-research-runtime.ps1`
- `G:\Wyatt\HK_intership\.agent\tools\research-runtime.ps1`
- `G:\Wyatt\HK_intership\.agent\tools\install-research-runtime.ps1`

Use this skill to route work inside the HK_intership workspace:

1. If the user wants an end-to-end paper workflow, use `research-workflow`.
   Typical requests include:
   - generating a research report from paper links
   - batch-downloading papers
   - converting PDFs to Markdown
   - merging/exporting a report to Word
   - typesetting/exporting the final merged report to PDF via `lovstudio-md2pdf`
2. If the user wants an expert-survey-style final report that is theme-organized rather than paper-by-paper, use `expert-survey-report`.
   Typical requests include:
   - expert survey
   - consulting-grade review
   - 按主题归类，不要逐篇总结
   - 不要文献卡片感
   - 先立研究对象、主线和中心判断
3. If the user wants to process one paper directory and write `Analysis_Detail.md`, use `research-analysis-subagent`.
4. Before running the research pipeline, verify the runtime with:
   `powershell -ExecutionPolicy Bypass -File "G:\Wyatt\HK_intership\.agent\tools\verify-research-runtime.ps1"`
5. Keep `G:\Wyatt\HK_intership\.agent\skills\...` as the source of truth for scripts, prompts, and assets.
6. Prefer `G:\` paths for outputs and runtime artifacts. Avoid saving to `C:\` unless the user explicitly requests it.

Workspace landmarks:
- `downloads\` holds task outputs and paper batches.
- `docs\superpowers\specs\` and `docs\superpowers\plans\` hold prior design and implementation notes.
- `.agent\skills\` contains canonical skill instructions.
- `.agent\tools\` contains runtime bootstrap and verification scripts.
