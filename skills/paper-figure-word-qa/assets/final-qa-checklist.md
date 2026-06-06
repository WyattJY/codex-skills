# Final QA Checklist

## Source And Scope

- [ ] Requested year/range verified for every included paper/project.
- [ ] Candidate inclusion/exclusion table exists for new research reports.
- [ ] Original PDF, supplement, appendix, official asset, or source page image exists for every accepted paper visual.
- [ ] Source pages rendered at 240 DPI or vector assets used when better.
- [ ] Contact sheets or tiled candidates used for dense visuals, with final decisions based on direct image inspection.

## Visual Manifest

- [ ] Every inserted/changed/rebuilt/omitted visual has a manifest row.
- [ ] Source lineage, source page, source id, source inspection, final render inspection, crop provenance, and verdict are recorded.
- [ ] Multi-panel figures include panel map and shared axes/legend/colorbar notes.
- [ ] Page-spanning tables include first/middle/final fragments and bottom-rule/final-row checks.
- [ ] Generated/rebuilt charts include script, input data/source, parameters, output format, and source comparison.

## Content Rigor

- [ ] Major claims map to source evidence or generated analysis.
- [ ] Dense plots/tables have nearby Chinese prose explaining axes/rows/columns/metrics/baselines/trends/limitations.
- [ ] Formulas are explained before rendering, typeset natively when embedded in prose, and followed by symbol definitions.
- [ ] Trend judgments are labeled as synthesis and separated from source facts.

## Build And Render

- [ ] DOCX rebuilt after the latest source changes.
- [ ] DOCX zip test passed.
- [ ] PDF exported after the latest DOCX timestamp, or limitation disclosed.
- [ ] Changed PDF pages plus neighbors rendered to PNG and inspected.
- [ ] For large edits, all pages rendered to a contact sheet and suspicious pages inspected full-size.
- [ ] Final page-scale labels, table cells, formula symbols, legends, and panel markers are readable.

## Stale Reference And Upload

- [ ] Builder scripts no longer reference rejected dirty assets.
- [ ] DOCX `word/media/*` and relationships no longer contain rejected filenames or old media hashes.
- [ ] Word COM task-created process cleaned up or limitation disclosed.
- [ ] If pushed to GitHub, `git status`, `git log -1 --name-status`, remote HEAD, and remote file content were verified.
