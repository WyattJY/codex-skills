---
name: nwafu-reference-list-md-docx
description: Format an NWAFU master's thesis reference list in a Markdown draft and export it to a thesis-style Word (.docx) list. Use when you need to remove numeric labels, group Chinese references before English references, sort the English references A-Z by first author, normalize one-entry-per-paragraph, and generate a Word copy with hanging indent (for pasting into the final thesis document).
---

# NWAFU Reference List (Markdown -> DOCX)

## Overview

Use `scripts/format_reference_list.py` to format the `参考文献/References` section in a Markdown file without touching other chapters, and optionally export the formatted list to a `.docx`.

## Quick Start

Format a Markdown reference list in-place and export a Word copy:
`python scripts/format_reference_list.py --md-in "<thesis.md>" --write-md --docx-out "<refs.docx>"`

Examples:
- `python scripts/format_reference_list.py --md-in "G:\\Wyatt\\master-paper\\毕业论文结构.md" --write-md --docx-out "G:\\Wyatt\\master-paper\\参考文献_毕业论文结构.docx"`
- `python scripts/format_reference_list.py --md-in "thesis.md" --md-out "thesis_formatted.md"`

## Formatting Rules

- Remove leading numbering like `1.` / `[12]`.
- Split entries by blank lines; reflow each entry to a single line.
- Detect Chinese vs English by presence of CJK characters; output Chinese entries first.
- Sort English entries by a normalized "starts with author" key (accent-stripped, case-insensitive).
- Keep everything outside the reference section unchanged.

## Notes

- This skill does not pinyin-sort Chinese references (keeps their original order).
- If `python-docx` is missing, install it with `python -m pip install python-docx`.

### scripts/
Automation:
- `scripts/format_reference_list.py`: format Markdown references + export `.docx`
