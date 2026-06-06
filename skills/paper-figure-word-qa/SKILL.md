---
name: paper-figure-word-qa
description: >-
  Use when Wyatt asks to QA or fix paper figures, tables, formulas, charts, or screenshots in Word/DOCX/PDF research reports, especially complaints like 图里夹正文, 图中夹正文, 图表中夹杂正文, caption混进图片, PDF整个截图, 整页PDF截图, 截图偷懒, 表格没有展示完全, 表格下面结果没有展示完全, 表格底部结果没截到, 最后一行没截到, 最后一列没截到, 图表不干净, whole-page PDF screenshots, incomplete tables, or body/caption text inside report images.
---

# Paper Figure Word QA

## Core Purpose

Use this skill as the strict visual, content, and render QA gate for Chinese technical Word/DOCX/PDF reports that use paper-derived figures, tables, equations, algorithms, screenshots, generated plots, or benchmark visuals. The goal is to prevent polished reports with lazy page screenshots, original paper body text inside images, clipped tables, unreadable final-scale labels, shallow paper summaries, or unsupported trend claims.

A clean crop alone is not sufficient. Every accepted visual must have source lineage, final rendered-page evidence, and nearby Chinese explanation that states what claim the visual supports, what the reader should notice, and what the visual does not prove.

## Pairing

- Use `jiangyu-word-report-style` as the style layer for Wyatt's Chinese Word reports. Do not change cover, margins, heading fonts, body fonts, caption style, or three-line table styling unless the user explicitly asks.
- Use `documents:documents` for DOCX/PDF rendering, page PNG inspection, and final artifact verification.
- Use `hk-intership` first when the task is an HK/intership literature workflow or the corpus lives under `H:\T7\Wyatt\HK_intership`.
- Use `research-workflow` when papers must be downloaded, PDFs converted, paper artifacts extracted, or non-HK report exports are needed.
- For broad survey prompts such as `2026年的多模态、llm、检索技术发展情况`, use the research/corpus workflow before this skill. This skill then audits the evidence, visuals, formulas, tables, citations, and final render quality.

Do not use this skill for ordinary UI screenshots, product mockups, or charts that are not part of a report-quality paper evidence workflow.

## Non-Negotiable Rules

- Write report notes in Chinese unless Wyatt explicitly requests another language.
- Do not infer a visual's semantic content from filenames, captions, surrounding paper prose, OCR, subtitles, or timestamps without inspecting the image itself.
- Do not use OCR tools as a substitute for visual understanding.
- Do not insert or keep a paper visual unless the source candidate and final rendered report page have both been visually inspected.
- Do not call a report fixed when PDF export failed. Mark it `partial-with-limitation` unless rendered DOCX pages were inspected as an explicit substitute and the limitation is disclosed.
- Do not accept final visuals that are readable only as standalone assets. They must be readable at final PDF page scale.
- If source lineage cannot be established, omit the visual, rebuild it natively, replace it with a cleaner official equivalent, or disclose the limitation. Do not fill the gap with a plausible screenshot.
- Keep paper captions and body paragraphs out of images. Rewrite their meaning as report prose, captions, or source notes.
- Keep style changes separate from visual QA. If the existing Word format is approved, only change asset paths, crops, figure widths, captions, nearby explanation, and QA evidence.

## New Research Report Gate

When the task is a new research report rather than a narrow crop fix, run these gates before final writing:

1. Recency gate: verify every included paper/project is actually from the requested year or range, for example 2026. Record title, venue/status, date, DOI/arXiv/GitHub URL, and why it is in scope.
2. Inclusion/exclusion gate: maintain a small table of candidate works, selected works, rejected works, and rejection reasons such as not 2026, no multimodal relevance, no agent/HPO relevance, or no retrievable source.
3. Claim-evidence matrix: every major claim must map to at least one source paper, figure, table, formula, benchmark, or generated analysis chart.
4. Theme-first synthesis: organize by problem chain and technical mechanism, not by one shallow paragraph per paper. For `多模态、LLM、检索技术发展情况`, cover problem, route, mechanism, evidence, limitation, and trend judgment across multimodal models, LLM agents/optimization, retrieval/reranking, and evaluation.
5. No hallucinated references: references must have auditable identifiers. A paper without a verified PDF/abstract page/project page is not a confirmed source.
6. Visual completeness: important figures, tables, formulas, and result curves from the papers should be extracted, rebuilt, or redrawn when they materially improve teaching clarity. Do not use one token figure to represent an entire paper.

## Source Acquisition

Before cropping or rebuilding a visual:

1. Search the project artifacts first: existing paper PDFs, extracted page images, `paper_artifacts`, figures, tables, markdown conversions, and previous report assets.
2. If the original paper is missing, locate the official PDF or accepted source, then appendix, supplementary PDF, arXiv ancillary files, author project pages, code repositories, and official figure/table assets.
3. Render source PDFs at 240 DPI or higher for crop work. Use vector extraction when available and better than raster rendering.
4. For dense figures/tables, build source-page contact sheets or tiled candidate sheets across adjacent pages and supplement pages for recall. Contact sheets help search, but final keep/reject decisions require inspecting the actual candidate image.
5. Record missing source as `source_missing` and set the affected visual/report verdict to `partial-with-limitation`; do not silently accept a dirty report screenshot.

Evidence syntax:

- `source_inspected=view_image path=<absolute_path> page=<pdf_page> observation=<clean/dirty and why>`
- `render_inspected=view_image path=<rendered_png> report_page=<page> dpi=<dpi> observation=<readable/clipped/dirty>`
- `verdict=<pass|recrop|rebuild-native|omit|partial-with-limitation>`

## Visual Manifest

Maintain a manifest for every inserted or changed paper visual. Copy `assets/visual-manifest-template.md` when useful.

Required fields:

| Field | Meaning |
| --- | --- |
| `paper` | Paper title or short key. |
| `source_pdf` | Original PDF, supplement, official asset, or source page image. |
| `source_page` | PDF page, supplement page, or source asset path inspected. |
| `source_id` | Figure/Table/Equation/Algorithm identifier when available. |
| `visual_type` | figure, table, algorithm, formula, multi-panel, page-spanning-table, generated-native, rebuilt-native, or vector-asset. |
| `expected_objects` | Expected logical object count, for example `1 table`, `3 grouped subtables`, `Fig. 6(a-c)`, or `2-page continued table`. |
| `panel_map` | For multi-panel figures: panel labels, shared axes, shared legend/colorbar, global scale, and panels referenced by report prose. |
| `crop_provenance` | Crop box in PDF points or image pixels, source render DPI, source image path/hash, crop tool/command, final dimensions, and per-fragment coordinates for stitched visuals. |
| `generated_provenance` | For rebuilt/generated plots: script path, input source/table, parameters/seed, output format, and source comparison notes. |
| `clean_asset` | Final image/vector path or native report object location. |
| `report_page` | Final rendered DOCX/PDF page inspected. |
| `source_inspected` | `view_image` evidence for the source candidate. |
| `render_inspected` | `view_image` evidence for the final rendered page. |
| `claim_supported` | Exact report claim this visual supports. |
| `content_role` | Evidence, mechanism explanation, benchmark result, formula definition, pipeline overview, ablation, or cautionary limitation. |
| `reader_takeaway` | What the reader should learn from this visual. |
| `source_fact_vs_inference` | Separate source facts from report synthesis/inference. |
| `content_explained` | Whether nearby prose explains axes/rows/columns/formula symbols/baselines/key comparison/limitation. |
| `verdict` | pass, recrop, rebuild-native, omit, or partial-with-limitation. |

Narrative statements like "I checked the figures" are not enough. The manifest is the audit trail.

## Crop Acceptance Checklist

Reject the candidate and continue searching or recropping if any item fails:

- Original paper body paragraphs, section headings, headers, footers, page numbers, or unrelated neighboring objects remain.
- Original Figure/Table caption text is inside the image, unless it is a short label visually inside the figure/table body.
- The crop is a whole PDF page or near-full-page screenshot when the report needs one figure, table, formula, algorithm, or chart.
- A table header, final row, bottom rule, highlighted row, delta row, average column, final metric column, grouped subtable, or table-internal note is missing.
- A figure axis, tick label, legend, colorbar, subfigure label, in-figure annotation, baseline, or panel marker is clipped.
- A formula is surrounded by explanatory prose that should be retyped in the report.
- Text, formulas, labels, table cells, legends, or panel markers are unreadable at final PDF page scale.
- It captures an intermediate slide, animation, whiteboard, or dashboard build-up while the final complete state exists nearby.
- It has black padding, excessive blank canvas, blurred text, bad aspect ratio, or report-scaling artifacts.

Keep only visual-body content. Move explanatory meaning into the report's own Chinese prose, captions, and source notes.

## Special Visual Rules

### Multi-Panel Figures

- Inventory all panels, shared axes, shared legends/colorbars, global scales, and cross-panel labels before splitting.
- Keep the full multi-panel figure only when the shared context is necessary and readable.
- Split panels only if shared context is preserved or recreated in captions/prose.
- If report prose references panel `(a)` or `(c)`, that panel and its labels must be readable in the final PDF.

### Page-Spanning Tables

- Detect `continued` tables across pages, supplements, or appendix fragments.
- Record first, middle, and final fragments; repeated headers; bottom rule; final row; and per-fragment coordinates.
- Prefer native rebuild or a stitched output with provenance when a raster crop would be unreadable.
- Do not accept a table until the final row and final column are visible.

### Equations

- For equations embedded in prose, crop should fail. Retype the equation natively.
- Preserve equation number, multi-line alignment, symbol definitions, and nearby explanation.
- Explain in Chinese why the formula appears, then render the formula, then list every symbol.
- Inspect the final rendered page for clipping, line overflow, and missing equation numbers.

### Generated Or Rebuilt Visualizations

- Prefer vector PDF/SVG/EMF for generated plots, diagrams, and extracted vector figures when the Word/PDF pipeline preserves them.
- Use high-DPI PNG only with a recorded reason. Reject JPG for text-heavy visuals.
- Record script path, input data/source table, parameters/seed, output format, and source comparison.
- Spot-check axes, units, legends, scales, baselines, labels, and values against the source.
- Use generated charts for paper counts by topic/month, method taxonomies, pipeline comparisons, benchmark trends, ablations, distributions, and section summary diagrams when they teach something.

### Naming

- Keep raw candidates neutral before inspection: `paper_p12_crop_003.png`, `candidate_table_02.png`.
- Accepted assets should encode paper key, source id, panel/table range, page range, and mode: `xmas_table5_supp_p12-13_rebuilt_native`, `foo_fig3a-c_vector_clean`.
- Do not use `complete` in a filename until the manifest verifies completeness.

## Content Rigor Gate

Every dense plot, benchmark table, multi-panel figure, generated chart, formula, or algorithm must have nearby "read the figure" prose in Chinese. Captions cannot replace this explanation.

For each affected section, answer:

- What problem or route is this section explaining?
- What exact claim does the visual/formula/table support?
- Which source fact supports that claim?
- What technical meaning should the reader take away?
- What limitation, hidden assumption, or non-proven conclusion should be stated?
- How does this support the report's trend synthesis?

Required gates:

- `claim_evidence_traceability`: major claims map to source evidence or generated analysis with provenance.
- `formula_pedagogy_gate`: formulas have plain Chinese explanation before, native formula rendering, symbol list after, and no prose screenshots.
- `result_interpretation_gate`: result tables explain rows, columns, metrics, baselines, best/second-best, deltas, and limitations.
- `figure_purpose_gate`: figures explain axes, legends, panels, first comparison target, key trend/anomaly, and what the figure does not prove.
- `trend_synthesis_gate`: trend judgments are labeled as synthesis and grounded in multiple sources, not stated as source facts.

## Workflow

1. Identify deliverables and builder: final DOCX/PDF paths, report generation script, image asset folder, source PDFs, extracted page images, and style helpers.
2. Locate high-risk visuals: search builder scripts for image filenames, inspect complaint pages, list old dirty crop names, and prioritize dense screenshots, tables, formulas, multi-panel figures, and benchmark pages.
3. Acquire sources: locate original PDFs, supplements, official assets, appendix pages, and prior extraction artifacts. Render source pages at 240 DPI or higher.
4. Recall candidates: inspect adjacent pages and supplement fragments. Use contact sheets for recall, then inspect final candidates directly.
5. Classify each object: single figure, table, page-spanning table, algorithm, equation, multi-panel figure, composite screenshot, project-generated chart, or rebuilt-native object.
6. Crop, split, rebuild, or omit: never screen-capture a PDF viewer, browser, Word page, or existing dirty report page as the final asset.
7. Update report generation: replace paths, rewrite captions/source notes, add nearby explanatory prose, and preserve approved Word style.
8. Remove stale references: search builder scripts and DOCX embedded media for rejected asset names/hashes.
9. Rebuild DOCX, validate DOCX as zip, export PDF, render changed pages and neighbors, and inspect final pages.
10. Iterate until the manifest, content gates, source inspection, and rendered-page inspection pass.

For large reports with more than 10 affected visuals, more than 3 source papers, or more than 20 pages, split the QA by paper key or page range. Maintain one shared manifest and inspect affected pages plus neighbors. Render all pages to a contact sheet, then inspect suspicious pages full-size.

## Commands And Checks

Use resolved paths. Do not run literal placeholders such as `<builder.py>`.

```powershell
$py = 'C:\Users\18357\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$builder = Resolve-Path -LiteralPath '<builder.py>'
$docx = Resolve-Path -LiteralPath '<final.docx>'
& $py -m py_compile $builder
& $py $builder
& $py -m zipfile -t $docx
```

For source rendering, use `scripts/render_pdf_pages.ps1` or the same pattern manually. Render at 240 DPI by default.

```powershell
Get-Command pdfinfo, pdftoppm | Out-Null
$pdf = Resolve-Path -LiteralPath '<final.pdf>'
$inspectDir = '<fresh-inspection-dir>'
$renderDpi = 240
$pdfInfo = pdfinfo $pdf
pdftoppm -png -r $renderDpi -- $pdf (Join-Path $inspectDir 'page')
Get-ChildItem -LiteralPath $inspectDir -Filter 'page-*.png' |
  Where-Object { $_.LastWriteTime -gt (Get-Item -LiteralPath $pdf).LastWriteTime } |
  Sort-Object Name
```

If Poppler fails on Chinese paths, copy only the PDF/rendering input to a short ASCII temp path for inspection and keep final deliverables in the requested workspace.

For Word PDF export on Windows, use an isolated `powershell.exe -NoProfile -STA` subprocess with explicit timeout when possible. Capture the task-created Word PID, release `$doc` before `$word`, call finalizers, and clean only the task-created PID. If the PID cannot be proven, disclose the limitation and do not kill all Word processes.

The following COM snippet is illustrative only; production export still needs STA, timeout, PID mapping, and task-local cleanup:

```powershell
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
  $doc = $word.Documents.OpenNoRepairDialog($inputDocx, $false, $true, $false)
  $doc.SaveAs2($outputPdf, 17)
  $doc.Close($false)
} finally {
  if ($doc) { [System.Runtime.InteropServices.Marshal]::ReleaseComObject($doc) | Out-Null }
  $word.Quit()
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
  [GC]::Collect()
  [GC]::WaitForPendingFinalizers()
}
```

Search for rejected references:

```powershell
rg -n "dirty_asset_name|old_crop_name|whole_page_name|screenshot|caption|mixed|full|whole" <builder-or-report-dir>
```

Also inspect DOCX embedded media and relationships by listing `word/media/*` and `word/_rels/document.xml.rels`. Confirm rejected filenames or old media hashes are absent, or record why they are archival and unused.

If PowerShell output garbles Chinese, use UTF-8 Python reads or ASCII-only diagnostics. Do not assume terminal mojibake means the file itself is corrupt.

## Git And GitHub Verification

When the task includes committing, pushing, publishing, or updating GitHub:

- Verify `git status --short` before and after; disclose unrelated changes rather than hiding them.
- Confirm final artifacts are tracked or explicitly local-only.
- Use `git log -1 --name-status` to verify the expected skill files/artifacts are in the commit.
- Confirm local HEAD matches the pushed remote branch with `git ls-remote` or `gh pr view`.
- Verify the remote content exists through GitHub API or raw file fetch when possible.
- Final response should include branch, commit SHA, GitHub URL, and any artifact not uploaded.

## Final Acceptance Gate

Before final response, be able to state:

- DOCX rebuilt successfully and DOCX zip test passed, when a report was built.
- PDF export succeeded, or the render limitation is explicitly disclosed.
- Final PDF pages were rendered to PNG and inspected. If impossible, rendered DOCX pages were inspected as a substitute and marked as a limitation.
- Changed pages plus neighboring pages were inspected; for large edits, all pages were contact-sheet scanned and suspicious pages opened full-size.
- Every affected visual has a manifest row with source lineage, crop provenance, source `view_image` evidence, final render `view_image` evidence, claim supported, content role, and verdict.
- No original paper body text, paper captions, page headers/footers, whole-page screenshots, clipped rows/columns, or unreadable final-scale labels remain.
- Equations embedded in prose were retyped natively, not kept as prose screenshots.
- Generated charts have provenance and source comparison.
- References/citations are auditable and no hallucinated or out-of-scope papers are presented as confirmed sources.
- Old dirty image filenames or hashes are no longer referenced by the final builder/DOCX media relationships.
- No Word COM process created by the task remains running.

## Final Response

Keep the final answer concise. Include:

- final DOCX/PDF paths or skill/GitHub artifact paths;
- classes of problems fixed, such as dirty paper captions, incomplete tables, whole-page screenshots, formula prose screenshots, shallow evidence, or citation gaps;
- verification summary: zip test, PDF page count/render, pages inspected, stale references removed, GitHub commit/remote check if applicable;
- source/render evidence at a concise level;
- any remaining limitation.
