---
name: audio-screenshot-course-notes
description: Use when the user provides lecture or course audio plus screenshots/images and asks for accurate transcription, Chinese course notes, semantic screenshot placement, Obsidian Markdown output, or an assets-backed study note.
---

# Audio Screenshot Course Notes

## Overview

Create a durable Markdown course note from a recording and related screenshots. Preserve a faithful transcript in a separate file, then write a source-grounded teaching note where screenshots and code links actively explain the lesson.

## Workflow

1. Locate inputs and output target.
   - Resolve every audio and image path from the user message and attachment list.
   - Create the output folder and an `assets/` subfolder unless the user names another asset path.
   - Prefer T7 paths for caches, intermediate files, and final artifacts when available.

2. Inspect screenshots before writing.
   - Use image perception for each screenshot, not filename order alone.
   - Record slide title, visible annotations, key diagram areas, and the likely lecture topic.
   - Inspect handwriting, highlights, arrows, and progressive PPT reveals as teaching signals. Integrate their meaning into normal explanatory prose; do not write mechanical labels such as `音频依据：` or `涂鸦识别：` in the final note.
   - Copy screenshots into `assets/` with stable numbered names such as `01_project_flow.jpg`.
   - Treat screenshots as teaching evidence. Do not dump them in a gallery; each inserted image must support the exact paragraph or mechanism immediately around it.
   - When several screenshots show a progressive reveal, prefer the most complete/readable one, and include intermediate screenshots only if they teach a distinct step.

3. Transcribe audio faithfully.
   - Use local ASR when possible. For Chinese technical lectures, prefer `faster-whisper` with `large-v3-turbo` or the strongest already-installed local model.
   - Keep caches and virtual environments under `/Volumes/T7/codex_cache/...` when installing tools.
   - Emit a raw transcript with timestamps before creating polished notes.
   - Preserve technical terms, code names, numbers, ratios, model names, and English tokens. Mark low-confidence fragments as `（待复核：...）` rather than silently inventing text.
   - For course-note deliverables, put the transcript Markdown in the same `assets/<lesson>/` folder as the audio by default, for example `assets/<lesson>/<lesson>_逐字稿.md`. The main note should link to it, not contain the full transcript inline, unless the user explicitly asks for a single-file note.
   - Strip or mark non-course system sounds such as verification-code prompts, notification sounds, and player UI messages as `（非课程提示音：...）`.

4. Ground the note in project/source context when available.
   - If the user gives a project root, inspect the real source files before writing the note.
   - Important spoken claims about scripts, configs, paths, metrics, data formats, training parameters, or outputs should be backed by clickable Markdown links to the relevant local files.
   - For Obsidian notes that should open local source files, prefer editor URI links over bare absolute paths. Use `vscode://file` links with URL-encoded paths and optional line anchors, for example:
     `[prepare_sft_dataset.py](<vscode://file/absolute/project/sft/prepare_sft_dataset.py:16>)`.
   - If no editor URI is appropriate, keep the line number outside the link target; do not put `:16` inside a bare filesystem path because Obsidian may treat it as part of the filename.
   - When quoting an important code block from a script, place the source script link immediately under that code block, not only elsewhere in the note. Use a short label like `脚本：` or `源码位置：`, and include the exact line anchor when possible, for example:
     `源码位置：[prepare_sft_dataset.py:16](<vscode://file/absolute/project/sft/prepare_sft_dataset.py:16>)`.
   - If a section includes multiple code snippets from different files, each snippet needs its own adjacent script link so the user can double-click from Obsidian without hunting through a separate source list.
   - Include concise code interpretation near the screenshot and explanation; do not merely list file paths at the top.

5. Build the Markdown note.
   - Use a clear Chinese title, source metadata, and a short summary.
   - Link to the separate transcript file in metadata, usually under `assets/<lesson>/<lesson>_逐字稿.md`.
   - Add a clickable Obsidian table of contents near the top when the note has multiple major sections. Prefer `[[#完整标题|显示名]]` links and verify every target heading exists.
   - Add a `课程笔记` section with coherent headings, explanations, action items, terminology, source anchors, and semantically placed screenshots.
   - Reconstruct the teaching flow instead of dumping subtitles chronologically. For each major section, write in this order: motivation, core idea, mechanism, example or evidence, and takeaway. Be explicit about why the speaker introduces a concept, what problem it solves, and how the next idea follows.
   - Use content-based transitions in the main note. Do not write phrases like `老师在 09:52 之后引入 mask`; write the actual teaching transition, such as `在说明普通 Self-Attention 默认能看全句之后，老师引入 mask 这个约束`。
   - Keep technical depth, but introduce formal formulas only after plain-language intuition. When a section is dense, split it into smaller subsections that build understanding progressively.
   - End every major chapter-style section with `### 本章小结`.
   - For technical project courses, especially this user's Qwen3-VL/grounding notes, use a "大模型算法工程师视角" rather than a generic "学霸笔记" voice: keep `先给结论`, `学习地图`, `课程精讲`, `源码精读`, `工程师易错点`, `自测题`, and `复盘动作`, and make the note read like a reproducible engineering analysis.
   - A study-grade engineering note must be usable for review and reproduction: it should explain why each step exists, how it connects to the previous and next lessons, what would break if the step is wrong, and which exact source lines prove the claim.
   - Insert screenshots near the point where the audio discusses that concept. Use relative Obsidian links:
     `![说明](assets/01_project_flow.jpg)`
   - Add concise captions explaining why each screenshot belongs there, what problem it clarifies, and what the reader should take away. Captions should not merely restate the filename or list OCR-like observations.
   - When a screenshot shows code, pair it with the actual local source file and line anchor when available. When the note itself quotes code, the clickable script link must appear directly below the quoted code block.
   - For concepts that remain hard to explain with only screenshots and prose, add accurate teaching visualizations. Prefer script-generated vector figures such as SVG for Markdown display and PDF for later LaTeX/PDF export. Use Python tools such as matplotlib or seaborn when they are the clearest way to draw process flows, masks, shape contracts, distributions, curves, comparisons, or summary diagrams. Do not add decorative graphics.
   - When generated figures are added, inspect them visually before insertion, place them immediately beside the explanation they support, and mention the matching PDF asset if one was generated.

6. Verify before completion.
   - Run `scripts/check_markdown_assets.py <note.md>` to confirm all local image links resolve.
   - Check that the main note exists in the requested output directory, the transcript note exists next to the audio under `assets/<lesson>/`, images exist in `assets/`, and no source files were modified.
   - Skim the main note to ensure the transcript has been removed from the body and that screenshots are interleaved with explanatory prose.
   - Verify clickable table-of-contents links resolve to existing headings when a TOC is present.
   - Verify no mechanical labels such as `音频依据：` or `涂鸦识别：` remain in the main note, and avoid timestamp-like lecture narration outside metadata/transcript links.
   - Verify no important teaching content was dropped during condensation or restructuring, and check that text and figures are aligned: each inserted frame supports the surrounding explanation and shows the fullest relevant information rather than a transitional or incomplete state.
   - Check visual richness before delivery: decide whether more high-information screenshots or generated teaching visualizations would materially improve clarity; add only figures that teach something.
   - Summarize the saved paths and any uncertainty in the final response.

## ASR Notes

Use a local workflow like this when no better project-specific ASR exists:

```bash
python3 -m venv "/Volumes/T7/codex_cache/course_note_asr/.venv"
"/Volumes/T7/codex_cache/course_note_asr/.venv/bin/pip" install faster-whisper
```

Then transcribe with word or segment timestamps. If GPU support is unavailable, use CPU int8/float32 settings that complete reliably. Do not claim the transcript is exact unless you reviewed the ASR output against the task-critical terms and timestamps.

## Note Quality Bar

- The final note should be useful without opening the audio.
- The transcript and synthesized notes should be separated so exact speech is not confused with interpretation.
- Screenshots must be semantically placed and explanatory, not dumped at the end or used as decoration.
- A good course note combines narration, screenshot evidence, and source-code anchors. If any one of those is available but missing from the explanation, the note is incomplete.
- For technical project courses, a good note should read like a large-model algorithm engineer's reproducible project analysis, not like meeting minutes: include mental models, data-flow or control-flow interpretation, code-level evidence, common mistakes, and self-check questions.
- A strong note reads like an experienced teacher guiding the reader: motivation first, then the central claim, mechanism, evidence, and takeaway. Figures should feel like part of the lesson, not attachments after the fact.
- Use generated SVG/PDF teaching figures when they clarify relationships better than screenshots alone, especially for pipelines, attention masks, tensor shape flows, architecture summaries, plots, and compact mechanism diagrams.
- Keep source provenance: audio path, screenshot paths, output path, ASR model/tool, and date.
- For long lectures, create section timestamps and a compact "重点复习" section.

## Common Mistakes

- Renaming/copying images but leaving broken Markdown links.
- Producing only a summary when the user asked for precise transcription.
- Over-polishing the transcript and losing spoken technical details.
- Assuming screenshot order equals lecture order without looking at image contents.
- Keeping the transcript inside the main note when it should be a separate reference document.
- Listing source files once but not using them where the explanation needs them.
- Writing captions that merely restate the image filename instead of explaining what the image proves.
- Writing final-note labels like `音频依据：` or `涂鸦识别：`; audio and doodle inspection should improve the explanation, not appear as raw audit notes.
- Describing the lesson with timestamps in the main narrative, such as `老师在 09:52 之后...`; use content-based transitions instead.
- Omitting a table of contents from long notes, or adding one without verifying that the links jump to real headings.
- Avoiding useful generated visualizations when a mask, shape contract, pipeline, or comparison would be much clearer as a simple vector diagram.
- Producing a shallow summary for a technical course when the user expects study notes that can support later implementation.
- Mentioning source files without explaining inputs, outputs, core logic, failure modes, and why those lines matter for the lecture point.
- Putting all script links in a distant source list while quoted code blocks have no adjacent clickable script link. Every important quoted code block should be followed by its own `vscode://file` source link.
- Saving large caches or generated assets on the system disk when T7 is the intended workspace.
