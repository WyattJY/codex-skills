# Jiangyu Word Report Style Contract

This is the user's preferred DOCX report format, derived from the internship handover report builders under `G:\实习\_handover_build`.

## Page

- Margins: top 2.5 cm, bottom 2.2 cm, left 2.7 cm, right 2.4 cm.
- Keep a formal Chinese technical-report layout.
- Prefer cover page + basic info table + page break.

## Fonts

- Body Chinese: 宋体 12 pt.
- Body ASCII / numbers: Times New Roman 12 pt.
- Main title: 黑体 22 pt bold, centered.
- Subtitle: 宋体 14 pt bold, centered.
- Heading 1: 黑体 16 pt bold.
- Heading 2: 黑体 14 pt bold.
- Caption: 宋体 10.5 pt bold, centered.

## Paragraphs

- Body: fixed 20 pt line spacing.
- Body: 0 pt before and after.
- Body: first-line indent 24 pt.
- Heading 1: fixed 20 pt line spacing, 12 pt before, 6 pt after.
- Heading 2: fixed 20 pt line spacing, 8 pt before, 4 pt after.

## Tables

- Use 三线表.
- Remove all borders first.
- Header row: thick top rule, thin bottom rule.
- Last row: thick bottom rule.
- Captions centered above tables.
- Keep cells vertically centered.
- Use 9-10.5 pt table text depending on density.
- Center compact columns such as stage, model, metric, status, date; left-align narrative columns.

## Verification

- Always check the DOCX zip structure.
- Load with `python-docx` to confirm paragraphs/tables/headings.
- Render through the documents skill when LibreOffice is available.
- On Windows, Word COM PDF export is an acceptable fallback if LibreOffice is missing.
- If visual QA cannot be completed, say so explicitly.
