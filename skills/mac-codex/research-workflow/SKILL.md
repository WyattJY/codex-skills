---
name: research-workflow
description: Use when the user asks to generate a research report from paper links, batch-download papers, convert PDFs to Markdown, or export a research report to Word
---

# Research Workflow

Canonical implementation lives at:
`G:\Wyatt\HK_intership\.agent\skills\research-workflow`

Runtime helper lives at:
`G:\Wyatt\HK_intership\.agent\tools\verify-research-runtime.ps1`

Use this workflow for a paper-to-report pipeline:

1. Verify the G-drive runtime:
   `powershell -ExecutionPolicy Bypass -File "G:\Wyatt\HK_intership\.agent\tools\verify-research-runtime.ps1"`
2. Batch download papers with:
   `G:\Wyatt\HK_intership\.agent\skills\research-workflow\scripts\run.py`
3. Convert PDFs to Markdown with:
   `G:\Wyatt\HK_intership\.agent\skills\research-workflow\scripts\pdf_to_markdown.py`
4. Analyze one paper at a time with the paired `research-analysis-subagent` skill.
5. Merge the report with:
   `G:\Wyatt\HK_intership\.agent\skills\research-workflow\scripts\merge_moe_report.py`
6. Export to Word with the Pandoc runtime resolved by the G-drive helper.

Use the canonical skill directory on `G:\` as the source of truth for scripts and assets.
