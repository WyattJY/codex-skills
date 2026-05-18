---
name: audio-screenshot-course-notes
description: Use when the user provides lecture or course audio plus screenshots/images and asks for accurate transcription, Chinese course notes, semantic screenshot placement, Obsidian Markdown output, or an assets-backed study note.
---

# Audio Screenshot Course Notes

## Overview

Create a durable Markdown course note from a recording and related screenshots. Preserve a faithful transcript, then write a structured study note that places screenshots where they support the spoken content.

## Workflow

1. Locate inputs and output target.
   - Resolve every audio and image path from the user message and attachment list.
   - Create the output folder and an `assets/` subfolder unless the user names another asset path.
   - Prefer T7 paths for caches, intermediate files, and final artifacts when available.

2. Inspect screenshots before writing.
   - Use image perception for each screenshot, not filename order alone.
   - Record slide title, visible annotations, key diagram areas, and the likely lecture topic.
   - Copy screenshots into `assets/` with stable numbered names such as `01_project_flow.jpg`.

3. Transcribe audio faithfully.
   - Use local ASR when possible. For Chinese technical lectures, prefer `faster-whisper` with `large-v3-turbo` or the strongest already-installed local model.
   - Keep caches and virtual environments under `/Volumes/T7 Shield/codex_cache/...` when installing tools.
   - Emit a raw transcript with timestamps before creating polished notes.
   - Preserve technical terms, code names, numbers, ratios, model names, and English tokens. Mark low-confidence fragments as `（待复核：...）` rather than silently inventing text.

4. Build the Markdown note.
   - Use a clear Chinese title, source metadata, and a short summary.
   - Include a `逐字稿` or `时间轴逐字稿` section when the user asks for precise extraction.
   - Add a `课程笔记` section with coherent headings, explanations, action items, and terminology.
   - Insert screenshots near the point where the audio discusses that concept. Use relative Obsidian links:
     `![说明](assets/01_project_flow.jpg)`
   - Add concise captions explaining why each screenshot belongs there.

5. Verify before completion.
   - Run `scripts/check_markdown_assets.py <note.md>` to confirm all local image links resolve.
   - Check that the note exists in the requested output directory, images exist in `assets/`, and no source files were modified.
   - Summarize the saved paths and any uncertainty in the final response.

## ASR Notes

Use a local workflow like this when no better project-specific ASR exists:

```bash
python3 -m venv "/Volumes/T7 Shield/codex_cache/course_note_asr/.venv"
"/Volumes/T7 Shield/codex_cache/course_note_asr/.venv/bin/pip" install faster-whisper
```

Then transcribe with word or segment timestamps. If GPU support is unavailable, use CPU int8/float32 settings that complete reliably. Do not claim the transcript is exact unless you reviewed the ASR output against the task-critical terms and timestamps.

## Note Quality Bar

- The final note should be useful without opening the audio.
- The transcript and synthesized notes should be separated so exact speech is not confused with interpretation.
- Screenshots must be semantically placed, not dumped at the end.
- Keep source provenance: audio path, screenshot paths, output path, ASR model/tool, and date.
- For long lectures, create section timestamps and a compact "重点复习" section.

## Common Mistakes

- Renaming/copying images but leaving broken Markdown links.
- Producing only a summary when the user asked for precise transcription.
- Over-polishing the transcript and losing spoken technical details.
- Assuming screenshot order equals lecture order without looking at image contents.
- Saving large caches or generated assets on the system disk when T7 is the intended workspace.
