---
name: "research-workflow"
description: "Use when generating literature reports from paper links, batch-downloading papers, converting PDFs to Markdown, writing per-paper analysis, or exporting research reports to Word/PDF."
---

# Research Workflow

Canonical workflow for paper-to-report tasks in `G:\Wyatt\HK_intership`.

## Runtime

- `${SKILL_DIR}` is this skill directory.
- Prefer the G-drive runtime and avoid writing caches to `C:\`.
- Verify before running a workflow:

```powershell
powershell -ExecutionPolicy Bypass -File "G:\Wyatt\HK_intership\.agent\tools\verify-research-runtime.ps1"
```

The runtime helper sets `HF_HOME`, `HUGGINGFACE_HUB_CACHE`, `TEMP`, and `TMP` under `G:\tools`.

## Workflow

### 1. Batch Download Papers

```bash
python "${SKILL_DIR}/scripts/run.py" download_arxiv_papers.py \
  --input "${paper_list_file}" --outdir "${topic_outdir}" --delay 0.5
```

### 2. PDF To Markdown

Default mode is fast and best for born-digital arXiv PDFs:

```bash
python "${SKILL_DIR}/scripts/run.py" pdf_to_markdown.py --root "${pdf_root}"
```

Outputs per paper:

- `paper.md`
- `paper_artifacts/`

Fast mode uses Docling with page/picture image export enabled, but keeps OCR and table structure recognition off.

### 3. Enhanced PDF Extraction

Use enhanced mode for scanned PDFs, weak text layers, table-heavy papers, or messy multi-column layouts:

```bash
python "${SKILL_DIR}/scripts/run.py" pdf_to_markdown.py \
  --root "${pdf_root}" \
  --mode enhanced
```

Enhanced mode enables Docling OCR and Docling table structure recovery for the Markdown conversion.

Optional sidecar models can add visual diagnostics and structured artifacts:

```bash
python "${SKILL_DIR}/scripts/run.py" pdf_to_markdown.py \
  --root "${pdf_root}" \
  --mode enhanced \
  --layout-engine doclayout-yolo \
  --table-engine table-transformer
```

Sidecar outputs:

- `paper_artifacts/pages/page_0001.png`
- `paper_artifacts/layout_doclayout_yolo/*_layout.png`
- `paper_artifacts/tables_table_transformer/*_tables.png`
- `paper_artifacts/tables_table_transformer/*_table_*.png`
- `paper_artifacts/tables_table_transformer/*_structure.json`
- `paper_artifacts/enhanced_extraction_manifest.json`

DocLayout-YOLO is optional because it adds an AGPL-3.0 dependency. Install it only when needed:

```powershell
. "G:\Wyatt\HK_intership\.agent\tools\research-runtime.ps1"
& $env:RESEARCH_PYTHON -m pip install doclayout-yolo
```

Table Transformer runs through `transformers` and downloads Hugging Face models into the G-drive cache configured by the runtime helper.

### 4. Per-Paper Analysis

Repeat until `select_next_unread.py` returns an empty line. Each paper must be analyzed in a fresh subagent session with the paired `research-analysis-subagent` skill.

```bash
python "${SKILL_DIR}/scripts/run.py" select_next_unread.py \
  --base-dir "${topic_outdir}" --order name --require-paper-md
```

Then run:

```bash
python "${SKILL_DIR}/scripts/run.py" preflight.py --paper-dir "${paper_dir}"
```

Write and verify `${paper_dir}/Analysis_Detail.md`.

## 5. Merge Report

```bash
python "${SKILL_DIR}/scripts/run.py" merge_moe_report.py \
  --base-dir "${topic_outdir}" --outline "${outline_md}" --output "${merged_report_md}"
```

## 6. Export To Word

```bash
pandoc "${merged_report_md}" -o "${merged_report_docx}" \
  --reference-doc="${SKILL_DIR}/assets/reference.docx" \
  --lua-filter="${SKILL_DIR}/assets/figure_caption.lua" \
  -f markdown-yaml_metadata_block
```

## 7. Export To PDF

Use `lovstudio-md2pdf` for polished PDF output:

```powershell
& "G:\tools\research-workflow\venv\Scripts\python.exe" `
  "G:\Wyatt\.agents\skills\lovstudio-md2pdf\scripts\md2pdf.py" `
  --input "${merged_report_md}" `
  --output "${merged_report_pdf}" `
  --title "<report title>" `
  --author "<author>" `
  --theme github-light `
  --toc true
```

## Utility

Relativize image paths only when sharing the Markdown file itself:

```bash
python "${SKILL_DIR}/scripts/run.py" convert_paths_to_relative.py \
  --file "${merged_report_md}" --base-dir "<downloads root>"
```
