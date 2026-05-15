---
name: jiangyu-word-report-style
description: Generate or edit Word/DOCX reports in Jiangyu's internship handover report format. Use whenever this user asks for a Word document, Word report, docx deliverable, technical report, implementation plan, interview QA report, handover document, or asks to follow the 019dd837-de97-7cf2-8114-baf80bad0e1f handover Word style, including Chinese reports that need the same fonts, spacing, cover, tables, and verification workflow.
---

# Jiangyu Word Report Style

Use this skill as the style layer for the user's Word deliverables. Pair it with the `documents:documents` skill whenever possible for DOCX rendering and visual QA.

## Workflow

1. Identify the requested document topic, source files, output directory, and whether the user wants a new document or edits to an existing document.
2. If the task names a specific DOCX/template, inspect it first. Otherwise use the default style contract below, which matches the user's internship handover reports.
3. Build the report with `python-docx`, preferably by copying or adapting `scripts/jiangyu_docx_style.py` into the working project.
4. Save outputs under the user-named workspace, not a random temp folder. For this user, prefer the named `G:\...` project directory when one is in scope.
5. Verify the final DOCX:
   - run `python -m zipfile -t <docx>`;
   - load it with `python-docx` and report paragraph/table counts if useful;
   - run the documents skill renderer to PNG/PDF when LibreOffice is available;
   - on Windows, if LibreOffice is absent, try Microsoft Word COM export to PDF;
   - disclose clearly if visual render QA could not be completed.

## Style Contract

Use a formal Chinese technical-report style:

- Page margins: top 2.5 cm, bottom 2.2 cm, left 2.7 cm, right 2.4 cm.
- Chinese body font: 宋体 12 pt. English/number font: Times New Roman 12 pt.
- Main title: centered 黑体 22 pt bold.
- Subtitle: centered 宋体 14 pt bold.
- Heading 1: 黑体 16 pt bold, fixed 20 pt line spacing, 12 pt before, 6 pt after.
- Heading 2: 黑体 14 pt bold, fixed 20 pt line spacing, 8 pt before, 4 pt after.
- Body paragraphs: fixed 20 pt line spacing, 0 pt before/after, first-line indent 24 pt.
- Cover page: title, subtitle, then a “基本信息” table, then page break.
- Tables: use Chinese “三线表” style, not full grid tables. Center captions, use 宋体 10.5 pt bold captions, remove all table borders, then add thick top/bottom rules and a thin rule below the header row.
- Table text: 宋体 9-10.5 pt depending on density; keep cells vertically centered; use centered alignment for short labels/dates/status and left alignment for prose.
- Do not use colorful business templates, decorative blocks, emoji, or marketing-page styling.

## Content Pattern

For technical reports, prefer this structure unless the user specifies another:

1. Cover and basic information
2. Executive conclusion / conclusion first
3. Background and scope
4. Technical architecture or workflow
5. Data, training, evaluation, or implementation details
6. Comparison tables for key distinctions
7. Risks, boundaries, and interview/succession口径 if relevant
8. References or source links when current facts, papers, or model specs are used

For resume/interview reports, include dense Q&A tables and concise “面试口径” sections.

## Reusable Resources

- Use `scripts/jiangyu_docx_style.py` as the starter builder. It contains the font, heading, body, cover, caption, and three-line-table helpers.
- Use `references/style_contract.md` only when exact formatting details are needed without loading the script.

## Final Response

Return the final `.docx` path as a raw absolute path. Mention only the key verification result and any render limitation. Do not overwhelm the user with internal build artifacts unless asked.
