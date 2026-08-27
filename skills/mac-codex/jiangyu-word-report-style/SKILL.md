---
name: jiangyu-word-report-style
description: Use when creating or editing Chinese Word/DOCX reports, technical manuals, implementation plans, or handover documents, especially when formulas, algorithms, workflows, theorems, experiment data, or system relationships need clear visual explanation and a concept overview figure.
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

## Visual Explanation and Concept Figures

When a report contains a hard-to-understand formula, algorithm, workflow, theorem, experiment result, or system relationship, assess whether a visual explanation will reduce the reader's cognitive load. For conceptual or explanatory artwork, **REQUIRED SUB-SKILL:** use `paint-with-code` and keep its editable source beside the rendered PNG.

1. At the start of a substantial report, consider an overview figure that maps the subject, inputs, main process, outputs, and evaluation or application context. Place it after the cover/basic-information page and before the first major body section, unless the user specifies another location.
2. For formulas, workflows, theorems, and experiment data, make the visual explain the exact symbols, stages, relationships, or trends used in the text. Never invent values, labels, or conclusions; use the supplied or locally verified data.
3. Follow the `paint-with-code` workflow: retain `index.html`, `sketch.js`, any local assets, and the final PNG. Render in a WebGL2-capable browser and check that the image is nonblank, legible, correctly framed, and free of accidental overlap.
4. Insert the verified PNG into the DOCX at the point where it helps comprehension, add a concise figure caption, and reference it from the surrounding text. Keep the source files with the report or in a clearly named companion directory.
5. Use a precise chart, SVG, Draw.io diagram, or Word equation when exact geometry, typography, or numerical plotting is required; `paint-with-code` may provide a conceptual companion figure, but must not replace exact formulas or quantitative evidence.

Pair this visual workflow with `documents:documents` when DOCX rendering or layout QA is available.

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
