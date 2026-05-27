---
name: research-workflow
description: Use when the user asks to generate a research report from paper links, batch-download papers, convert PDFs to Markdown, or export a research report to Word
---

# Research Workflow

## Claude Code Adaptation

- This copy is prepared for Claude Code personal or project skills.
- Resolve bundled files relative to `${CLAUDE_SKILL_DIR}` when Claude Code exposes it; otherwise use this skill directory.
- The bundled scripts and assets are the source of truth for Claude Code usage.

Use this workflow for a paper-to-report pipeline.

## Runtime

1. Verify the H-drive runtime:
   `powershell -ExecutionPolicy Bypass -File "${CLAUDE_SKILL_DIR}\scripts\verify-research-runtime.ps1"`
2. The helper sets `HF_HOME`, `HUGGINGFACE_HUB_CACHE`, `TEMP`, and `TMP` under `H:\T7\tools`.
3. Prefer the bundled scripts under `${CLAUDE_SKILL_DIR}\scripts`.

## Workflow

1. Batch download papers:
   `python "${CLAUDE_SKILL_DIR}\scripts\run.py" download_arxiv_papers.py --input "${paper_list_file}" --outdir "${topic_outdir}" --delay 0.5`
2. Convert PDFs to Markdown:
   `python "${CLAUDE_SKILL_DIR}\scripts\run.py" pdf_to_markdown.py --root "${pdf_root}"`
3. Use enhanced extraction for scanned PDFs or table-heavy layouts:
   `python "${CLAUDE_SKILL_DIR}\scripts\run.py" pdf_to_markdown.py --root "${pdf_root}" --mode enhanced`
4. Analyze one paper at a time with the paired `/research-analysis-subagent` skill.
5. Preflight one paper before analysis:
   `python "${CLAUDE_SKILL_DIR}\scripts\run.py" preflight.py --paper-dir "${paper_dir}"`
6. Merge the report:
   `python "${CLAUDE_SKILL_DIR}\scripts\run.py" merge_moe_report.py --base-dir "${topic_outdir}" --outline "${outline_md}" --output "${merged_report_md}"`
7. Export to Word with the bundled reference doc and Lua filter:
   `pandoc "${merged_report_md}" -o "${merged_report_docx}" --reference-doc="${CLAUDE_SKILL_DIR}\assets\reference.docx" --lua-filter="${CLAUDE_SKILL_DIR}\assets\figure_caption.lua" -f markdown-yaml_metadata_block`

## Utility

Relativize image paths only when sharing the Markdown file itself:

`python "${CLAUDE_SKILL_DIR}\scripts\run.py" convert_paths_to_relative.py --file "${merged_report_md}" --base-dir "<downloads root>"`
