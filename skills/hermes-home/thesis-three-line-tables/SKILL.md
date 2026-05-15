---
name: thesis-three-line-tables
description: "Generate and polish thesis “三线表” tables from per-table CSV files, export them into a Word (.docx) document, and optionally sync aligned three-line text tables back into a Markdown thesis draft. Use when you need: (1) one CSV per table (Excel-friendly UTF-8 BOM), (2) Word three-line table formatting (no vertical lines; thick top/bottom rules; thin header separator; header bold; numeric alignment), (3) special beautification for long-text tables (e.g., API endpoint lists), or (4) batch table export for direct copy/paste into a Chinese thesis/dissertation."
---

# Thesis Three Line Tables

## Overview

Turn your thesis tables into:
- **Per-table CSVs** (clean, Excel/WPS-friendly)
- A **Word document** containing fully styled **three-line tables** (顶/底线加粗、表头下细线、无竖线)
- Optional **Markdown sync**: keep a readable “three-line text table” in your `.md` draft that is generated from the CSVs (so the source of truth stays the CSV).

## Workflow

### 1) Prepare CSVs (one file per table)
Store each table as a standalone CSV:
- First row is the header row.
- Use quotes when a field contains commas or line breaks.
- Recommended filename pattern: `table<chapter>_<index>_<slug>.csv` (e.g., `table5_2_backend_api_endpoints.csv`).

### 2) Fix CSV encoding (avoid “Excel 乱码”)
Run:
`python scripts/fix_csv_encoding.py --csv-dir <your-csv-folder>`

This rewrites all `*.csv` as **UTF-8 BOM + CRLF** (best default for Excel/WPS on Windows).

### 3) Export Word three-line tables (.docx)
Install dependency once (if needed):
`python -m pip install python-docx`

Then run:
`python scripts/build_three_line_tables_docx.py --csv-dir <your-csv-folder> --output <out.docx> --md <optional-thesis.md>`

If you pass `--md`, the script extracts table captions like `表5-2 ...` and automatically matches CSVs by table number (e.g., `table5_2_*.csv`).

Built-in beautification:
- Thick top/bottom rules, thin header separator; **no vertical lines**
- Header bold & centered
- Numeric columns right-aligned (heuristic)
- Long-text table polish (API endpoints): line breaks in endpoint lists; tighter “业务域/方法” columns; landscape layout

### 4) (Optional) Sync nice three-line text tables into Markdown
If your thesis is in Markdown and you keep ` ```text ` blocks under each caption, run:
`python scripts/update_markdown_tables_from_csv.py --csv-dir <your-csv-folder> --md <thesis.md>`

This keeps the Markdown readable while the CSV remains the canonical data source.

## Resources

### scripts/
Automation scripts:
- `scripts/fix_csv_encoding.py`: rewrite CSVs as UTF-8 BOM + CRLF
- `scripts/build_three_line_tables_docx.py`: build `三线表汇总.docx` from CSVs (optionally reading captions from Markdown)
- `scripts/update_markdown_tables_from_csv.py`: regenerate aligned Markdown “三线表” blocks from CSVs

### references/
Concise standards and conventions for three-line tables and CSV organization.
