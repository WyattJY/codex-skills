---
name: paper-figure-word-qa
description: Use when Wyatt asks to QA or fix paper figures/tables in Word/DOCX/PDF reports, including Chinese complaints like 图里夹正文, 表格没有展示完全, PDF整个截图, 截图偷懒, body/caption text in screenshots, whole-page PDF screenshots, or incomplete tables.
---

# Paper Figure Word QA

## Core Purpose

Use this skill as the strict visual QA gate for technical Word/DOCX/PDF reports that include paper figures, paper tables, formulas, screenshots, or benchmark result visuals. It is meant to prevent the exact failure mode where a report looks polished globally but individual paper figures are lazy page screenshots, include original paper body text, or miss critical rows/columns.

Pair it with:

- `jiangyu-word-report-style` when the deliverable is Wyatt's Chinese Word report style.
- `documents:documents` when DOCX rendering or page PNG verification is needed.
- The relevant research/corpus skill, such as `hk-intership` or `research-workflow`, when papers and extracted artifacts must be located first.

## Trigger Phrases

Use this skill when the user says or implies any of these:

- `Word报告`, `图文报告`, `论文精读`, `调研报告`, `literature report`, `paper survey` when the request involves paper figures/tables, formulas, screenshots, or visual QA.
- `paper figures`, `paper tables`, `figure extraction`, `table crop`, `result table`, `benchmark table`.
- `图里夹正文`, `图中夹正文`, `图表中夹杂正文`, `caption混进图片`, `表格没有展示完全`, `截图偷懒`, `PDF整个截图`, `图糊弄一下`, `图表不干净`.
- Need to keep the approved report format while only fixing figures, tables, captions, references, or visual QA.

Do not use this skill for ordinary app screenshots, UI mockups, or charts that are generated directly for the current project and are not part of a report-quality paper visual workflow.

## Non-Negotiable Rules

- Write report notes in Chinese unless Wyatt explicitly requests another language.
- Do not modify `jiangyu-word-report-style` when the problem is only figure/table selection, cropping, captions, or render QA.
- Do not insert or keep any paper figure/table unless the exact source crop has been visually inspected with `view_image`.
- Do not infer visual meaning from nearby prose, filenames, OCR text, subtitles, page numbers, or paper captions without checking the image itself.
- Do not use OCR as a substitute for visual understanding.
- Do not call a report "fixed" until the final DOCX has been rebuilt and the final PDF or rendered page PNGs have been inspected on the affected pages.
- Do not preserve a dirty screenshot because it is "good enough" if a cleaner crop can be made from the original paper page.
- Every final paper visual must have source lineage: source paper/key, original PDF path, source page number, Figure/Table/Equation/Algorithm identifier when available, final asset path, final rendered report page, visual type, expected logical object count, and source/render `view_image` inspection evidence.
- If clean lineage cannot be established, omit the visual, rebuild it natively, replace it with a cleaner equivalent visual, or disclose the limitation. Do not fill the gap with a plausible screenshot.
- If no clean crop can be produced, do not keep a dirty screenshot as fallback. Rebuild the table/formula natively, replace with a cleaner equivalent visual, omit it, or disclose the limitation.

## Two-Level Inspection

Always inspect both levels:

1. Source asset inspection: open the candidate crop/source image with `view_image` before deciding what it is and whether it is complete.
2. Rendered report inspection: after rebuilding/exporting, render the final PDF or DOCX pages and inspect the affected pages with `view_image`.

Passing only one level is not enough. A source crop can be clean but become unreadable, oversized, clipped, or badly placed in the Word report.

After export, verify the PDF exists, is nonzero bytes, has a modified time after the rebuilt DOCX, and has a readable page count via `pdfinfo` or an equivalent tool. If this cannot be proven, do not mark PDF verification as passed.

Rendered report inspection must confirm: the visual is readable at final page scale, no original paper caption/body text remains, no row/column/axis/legend is clipped, and every changed visual appears on the expected page without layout spillover.

## Visual Manifest

Maintain a lightweight manifest for every inserted or changed paper visual. It can be a Markdown table, CSV, JSON, or a section in the work notes. The manifest must contain:

| Field | Required Meaning |
| --- | --- |
| `paper` | Paper name or short key. |
| `source_pdf` | Original PDF or extracted page source. |
| `source_page` | PDF page or page image inspected. |
| `source_id` | Figure/Table/Equation/Algorithm identifier when available. |
| `visual_type` | figure, table, algorithm, formula, composite, generated-native, or rebuilt-native. |
| `expected_objects` | Expected logical object count, for example `1 table`, `3 grouped subtables`, or `2 plot panels`. |
| `clean_asset` | Final image path or native report object location. |
| `report_page` | Final rendered DOCX/PDF page inspected. |
| `source_inspected` | Evidence that the source crop/page was inspected with `view_image`. |
| `render_inspected` | Evidence that the final rendered page was inspected with `view_image`. |
| `verdict` | pass, recrop, rebuild-native, omit, or partial-with-limitation. |

Do not rely on narrative claims such as "I checked the figures." The manifest is the audit trail that prevents hidden dirty screenshots.

## Crop Acceptance Checklist

Reject the crop and continue searching or recropping if any item fails:

- It contains original paper body paragraphs.
- It contains original paper Figure/Table caption text outside the actual visual body.
- It contains page headers, footers, page numbers, unrelated neighboring figures, or section headings.
- It is a whole PDF page when the report only needs one figure, table, algorithm, formula, or chart.
- A table row, final row, highlighted row, metric column, final column, bottom rule, or grouped subtable is cut off.
- A figure axis title, tick labels, legend, subfigure label, colorbar, in-figure annotation, or required visual element is cut off.
- A formula is surrounded by explanatory prose that should instead be typeset in the report text.
- The visual has black padding, excessive blank canvas, blurred text, unreadable labels, or a bad aspect ratio caused by prior report scaling.
- It captures an intermediate slide/animation/build-up state while a final complete state exists nearby.
- It visually resembles a whole PDF page: page margins are visible, page headers/footers/page numbers remain, multiple sections are visible, or the aspect ratio is close to a full page.

Keep only visual-body content:

- For figures: axes, legends, colorbars, subfigure labels such as `(a)`, in-figure notes, arrows, labels, and plotted data.
- For tables: top/bottom rules, header rows, all result rows, grouped subtables, highlighted rows, table-internal notes if they are visually part of the table.
- For algorithms: the algorithm box/body, requirements, pseudocode lines, and return line.

Do not keep paper captions or surrounding prose just because they explain the figure. Rewrite that explanation as the report's own caption/source note.

## Pass/Fail Acceptance Tests

Every changed visual must pass these tests before delivery:

- `visual_manifest_required`: manifest row exists with source, clean asset, final report page, expected logical object count, and source/render inspection evidence.
- `source_vs_render_double_pass`: both source crop and final rendered page pass the cleanliness/completeness checklist.
- `one_logical_object_per_asset`: one asset contains one logical object unless the original paper figure is intentionally multi-panel and the report claim depends on the whole multi-panel visual.
- `no_original_prose_or_caption_inside_image`: no original paper body paragraphs, section headings, page headers/footers, page numbers, or original Figure/Table caption paragraphs remain inside the image.
- `table_completeness_sentinels`: before accepting a table, identify and check header row, final row, final metric column, bottom rule, highlighted/bold row, grouped subtable count, and table-internal notes.
- `whole_page_detector`: reject full-page or near-full-page PDF screenshots.
- `render_readability_gate`: reject rendered pages where table text, axis labels, legends, formula symbols, or subfigure labels are unreadable at normal report viewing size.
- `stale_dirty_reference_scan`: final builder must not reference rejected dirty assets or risky stale names such as `whole`, `full`, `screenshot`, `mixed`, `caption`, `dirty`, `old`, or prior dirty crop names unless they are clearly archival and unused.

## Workflow

1. Identify the final deliverables and builder:
   - final `.docx` and `.pdf` paths;
   - report generation script, usually a Python builder;
   - image asset folder;
   - original paper PDFs or page PNGs;
   - already-approved format/style helpers.

2. Locate high-risk visuals:
   - search builder scripts for image filenames;
   - inspect rendered report pages around the user's complaint;
   - list paper visual assets and old dirty crop names;
   - prioritize pages containing dense paper screenshots, tables, formulas, or multi-panel benchmark figures.

3. Classify each visual before cropping:
   - single figure/chart;
   - single table;
   - algorithm box;
   - formula/equation;
   - composite block containing multiple figures/tables;
   - paper page screenshot;
   - project-generated explanatory figure.

4. Inspect source candidates:
   - open current dirty crop with `view_image`;
   - open original paper page PNG/PDF render with `view_image`;
   - inspect neighboring pages or adjacent candidate crops if the figure/table may continue or if the current crop is incomplete;
   - use contact sheets or filenames only for recall, never for final keep/reject.

5. Crop or split:
   - recrop from the original paper page whenever possible;
   - when recropping from a PDF, render the source page at 200-300 DPI or use direct PDF image/vector extraction;
   - do not create final assets by screen-capturing a PDF viewer, browser, Word page, or existing dirty report page;
   - split composite blocks into separate report visuals;
   - keep crop names neutral until the image has been inspected;
   - after inspection, use semantic filenames such as `xmas_table5_complete_clean.png` or `scalselect_table2_budget_clean.png`;
   - use `clean`, `complete`, or specific table/figure numbers in filenames so future searches can distinguish them from rejected assets.

6. Update report generation:
   - replace dirty asset paths with clean assets;
   - update captions/source notes to describe what the clean visual shows;
   - move paper-caption meaning into the report's own prose;
   - keep the approved Word style functions unchanged unless the user explicitly asks to change formatting.

7. Remove stale references:
   - search builder scripts for rejected dirty filenames;
   - check old filenames are not referenced by the final builder;
   - keep dirty assets only as archival source if useful, but never referenced in final output.

8. Rebuild and render:
   - compile/check the builder;
   - rebuild DOCX;
   - validate DOCX as a zip;
   - export PDF;
   - render PDF pages to PNG;
   - inspect affected pages and at least one page before/after for layout spillover.

9. Iterate until clean:
   - if a table is clipped in the rendered report, adjust crop bounds or figure width;
   - if a visual becomes too small, split it further or allocate a separate page;
   - if an original caption/prose remains visible, recrop again;
   - if a formula screenshot includes prose, typeset the formula in the report instead.

## Handling Common Visual Types

### Paper Tables

Tables are accepted only when every relevant row and column is visible. For benchmark/result tables, the final row, highlighted method row, delta row, average column, and final metric column matter most.

Rules:

- Include table header, all compared methods/settings, all metric columns, and bottom rule.
- Do not crop away small grouped subtables, such as three mini-tables under one Table number.
- If Table 1 and Table 2 are stacked with captions between them, split them into `table1_clean` and `table2_clean`.
- If the paper caption touches the table, prefer the table body and recreate caption information in the report; do not keep a full paragraph caption just to avoid tight cropping.
- If a table is mostly text or numeric results and will be unreadable as an image at report scale, rebuild it as a report-native three-line table and cite the paper source. Use an image crop only when the visual layout itself is essential and remains readable after rendering.

### Paper Figures

Figures are accepted only when the graph or diagram can be understood without the original paper caption embedded in the image.

Rules:

- Include legends, axes, tick labels, colorbars, subfigure labels, and annotations that belong to the figure.
- Exclude original paper caption and paragraph text below the figure.
- If a multi-panel figure is too dense, split panels or use a wider figure width only if the rendered report remains readable.
- If the report text references a specific panel, ensure that panel is visible and readable.

### Algorithms

For algorithm boxes:

- Include title line if it is part of the algorithm box.
- Include inputs/requirements, all numbered steps, branches, and return statement.
- Exclude surrounding paragraphs explaining the algorithm.

### Formulas

Prefer report-native formulas when formulas are embedded in prose.

Use a crop only when the formula itself is a visual artifact and the crop contains no unrelated explanatory paragraphs. Otherwise:

- explain the formula in Chinese prose before the formula;
- typeset the formula in the report;
- list symbol meanings after it;
- avoid copying a paper paragraph screenshot.

### Composite Screenshots

If one crop contains multiple logical objects, split it unless the paper figure itself is intentionally a single multi-panel figure.

Keep multi-panel figures together only when they share one original figure number/caption and the report claim depends on the whole multi-panel visual. Otherwise split the panels or tables into separate report assets.

Examples:

- `Table 1 + Table 2 + captions` becomes two table crops.
- `Figure 3 + Figure 4 + Table 1 + body text` becomes three clean assets.
- `formula paragraph + result table` becomes report-native formula plus a table crop.

## Known Failure Examples To Prevent

- XMAS Figure 6 / Table 5: Figure 6 should show only the ARP bars and concept distribution; Table 5 must show all three grouped result tables completely. Do not include original paper caption or cut off the bottom results.
- XMAS Figure 3 / Figure 4 / Table 1: do not use a page chunk containing figure captions, body text, and table captions. Split into separate clean assets.
- ScalSelect Table 1 / Table 2: do not keep the original paper captions inside the image. Split the two result tables and preserve complete rows.
- ScalSelect Table 6 / Table 7 / Figure 2: keep Table 6, Table 7, and the importance-score plots as separate visuals. Do not mix them with surrounding prose.
- MLLM RFT formulas and results: formulas in prose should be report-native formulas; result tables should be table bodies only.
- HPO vs LLM: do not screenshot a whole PDF page. Crop each curve/table separately and explain stop-loss implications in report prose.
- MLIPilot: split scorecard, final result table, iteration history, convergence curve, and accept/reject matrix. Do not merge them into one unreadable chunk.

## Commands And Checks

Use repo-specific paths, but the standard pattern is:

```powershell
$py = 'C:\Users\18357\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $py -m py_compile <builder.py>
& $py <builder.py>
& $py -m zipfile -t <final.docx>
```

If `python-docx` fails on Chinese paths, copy the final DOCX to a short ASCII temp path for structural stats only. Do not move the final deliverable out of the project.

If `python-docx` has trouble reading images or writing DOCX files under Chinese paths, use file-like streams for image insertion or stage only the build/input copy under a short ASCII temp directory, then copy the successfully validated DOCX back to the requested project path. The final deliverable path must remain inside the user-named workspace.

For Word PDF export on Windows, prefer `SaveAs2(..., 17)` if `ExportAsFixedFormat` hangs:

Run Word COM export in an isolated Windows PowerShell STA subprocess when possible, with an explicit timeout. Capture the task-created Word instance PID, release `$doc` and `$word` in that order, call `[GC]::Collect()` and `[GC]::WaitForPendingFinalizers()`, and clean up only the task-created Word PID. Never blanket-kill all `WINWORD.EXE` processes because the user may have Word documents open.

```powershell
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
  $doc = $word.Documents.OpenNoRepairDialog($inputDocx, $false, $true, $false)
  $doc.SaveAs2($outputPdf, 17)
  $doc.Close($false)
} finally {
  $word.Quit()
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
```

Render and inspect final pages:

Render into a fresh inspection directory for this build, or delete prior `page-*.png` files before rendering. Use quoted absolute paths, verify `pdftoppm` exists, render dense table/figure pages at 200 DPI or higher, and confirm the expected PNG files were created after the current PDF timestamp. If Poppler fails on Chinese paths, copy the PDF to a short ASCII temp path for rendering only; keep the final PDF in the project.

```powershell
pdftoppm -png -r 144 <final.pdf> <inspect_dir>\page
```

Search for rejected references:

```powershell
rg -n "dirty_asset_name|old_crop_name|whole_page_name" <builder.py>
```

Also search for risky stale filename patterns such as `page`, `whole`, `full`, `screenshot`, `mixed`, `caption`, `dirty`, and `old`. A match is not automatically wrong, but each match must be explained as unused/archive or replaced.

If PowerShell output garbles Chinese, use UTF-8 Python reads or ASCII-only diagnostics. Do not assume garbled terminal output means the file itself is corrupt.

## Word Style Preservation

When Wyatt says the existing Word format is good:

- do not rewrite the cover, heading styles, page margins, three-line table helpers, body font, or caption style;
- do not replace the whole report generator unless necessary;
- make targeted changes to asset paths, crop files, figure widths, captions, and nearby explanatory text;
- keep the report's own Chinese captions/source notes, not original paper captions embedded in screenshots.

## Final Acceptance Gate

Before final response, verify and be able to state:

- DOCX rebuilt successfully.
- DOCX zip test passed.
- PDF was exported or a clear render limitation was disclosed.
- PDF/pages were rendered to PNG if possible.
- Affected pages were visually inspected with `view_image`.
- Old dirty image filenames are no longer referenced by the final builder.
- No Word COM background process created by the task remains running.
- Final DOCX/PDF paths are inside the user-named workspace unless the user asked otherwise.
- For every affected visual, the final notes can state the source crop inspected, rendered report page PNG inspected, page number, render DPI, and verdict.

## Final Response

Keep the final answer concise. Include:

- final DOCX/PDF paths;
- the classes of visual problems fixed, such as dirty paper captions, incomplete tables, whole-page screenshots, formula prose screenshots;
- verification summary: zip test, PDF page count/render, key pages inspected, stale references removed;
- source/render evidence for affected visuals at a concise level;
- any limitation that remains.
