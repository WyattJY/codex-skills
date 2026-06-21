---
name: audio-screenshot-course-notes
description: Use when the user provides lecture or course audio plus screenshots/images and asks for accurate transcription, Chinese course notes, semantic screenshot placement, Obsidian Markdown output, or an assets-backed study note.
---

# Audio Screenshot Course Notes

## Overview

Create a durable Markdown course note from a recording and related screenshots. Preserve a faithful transcript in a separate file, then write a source-grounded teaching note where screenshots and code links actively explain the lesson. MiMo is only an ASR provider in this workflow; Codex writes the final notes, performs source-code analysis, places screenshots, and synthesizes the teaching narrative.

## Workflow

1. Locate inputs and output target.
   - Resolve every audio and image path from the user message and attachment list.
   - Create the output folder and an `assets/` subfolder unless the user names another asset path.
   - Prefer T7 paths for caches, intermediate files, and final artifacts when available.

2. Inspect screenshots before writing.
   - Use image perception for each screenshot, not filename order alone.
   - Record slide title, visible annotations, key diagram areas, and the likely lecture topic.
   - Inspect handwriting, highlights, arrows, and progressive PPT reveals as teaching signals. Integrate their meaning into normal explanatory prose; do not write mechanical labels such as `音频依据：` or `涂鸦识别：` in the final note.
   - Preserve original screenshot filenames by default and keep links stable. If copying is required, copy into `assets/` without renaming; only add a short suffix when a filename collision would overwrite a file.
   - For this user's manually captured lesson screenshots, default to using every non-hidden image in the lesson asset folder. Do not drop screenshots merely because they look progressive or partially overlapping; the act of screenshotting is a priority marker.
   - If an image is corrupt, unreadable, or truly duplicate with no additional teaching value, leave it out only with an explicit `未使用截图说明` entry in the note explaining the filename and reason.
   - Treat screenshots as teaching evidence. Do not dump them in a gallery; each inserted image must support the exact paragraph or mechanism immediately around it.
   - When several screenshots show a progressive reveal, include the sequence as a teaching progression with concise captions. Use the most complete frame for summary, but keep intermediate frames when they show how the explanation builds.

3. Transcribe audio faithfully.
   - Reuse an existing transcript/cache only when it matches the source audio duration and segment count.
   - For Chinese technical lectures, prefer MiMo ASR when `MIMO_ASR_API_KEY` or an approved Keychain secret is available: use `scripts/transcribe_mimo_asr.py` with `mimo-v2.5-asr`, `language=zh`, and the Token Plan/OpenAI-compatible base URL. Never hardcode or print the key.
   - MiMo ASR currently accepts wav/mp3 data URLs through `chat/completions`; base64 audio must stay under 10MB per request. For long `.m4a`/course recordings, let the script transcode with `ffmpeg` and use note-grade short chunks: default silence-aware segmentation, target 25 seconds, minimum 10 seconds, maximum 30 seconds. If silence detection cannot find reliable cut points, the script falls back to fixed short chunks.
   - The MiMo transcript script must preserve chunk start/end timestamps and write both a short auxiliary summary and the transcript text for each chunk. The summary is for note drafting only; the transcript remains the source of truth.
   - Do not use MiMo to write, polish, structure, or synthesize the final course note. MiMo's role ends at speech-to-text output and lightweight transcript-side chunk summaries; Codex must do the note writing, screenshot integration, source-code reading, and pedagogical restructuring.
   - After MiMo returns text, run deterministic course cleanup: normalize common technical ASR errors such as `RPE/LP/LPE -> RoPE` and `西塔/奇塔 -> theta`, and mark non-course system prompts such as verification-code prompts, notification sounds, and player UI messages as `（非课程提示音：...）`.
   - For formula-dense technical courses, treat MiMo as a short-segment ASR source only. Before writing the main note, run a two-step correction pass:
     1. Apply a term dictionary cleanup for high-risk tokens, especially `RoPE`, `theta`, `cos/sin`, `Q/K/V`, `mask`, `view_as_complex`, model names, function names, tensor-shape terms, and other course-specific English/code tokens.
     2. Reverse-check key claims against screenshots, formulas, notebooks, and real source code before they enter the main note. Do not let ASR surface errors become final explanations.
   - When accurate word/segment timestamps matter more than raw transcript text, keep or rerun local `faster-whisper` because MiMo ASR returns chunk-level text rather than reliable word timestamps in this workflow.
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

5. Build a teaching evidence matrix before writing.
   - Before drafting, create a working matrix with one row per major teaching claim. This can be a scratch note or in-memory outline, but the final note must reflect it.
   - Each row should answer: `Why is this concept introduced?`, `What problem does it solve?`, `Which screenshot proves or clarifies it?`, `Which transcript segment supports it?`, `Which source line or notebook cell verifies it?`, and `What breaks if implemented or understood incorrectly?`
   - Every user-provided screenshot/image in the lesson asset folder must map to a teaching row, or to the explicit `未使用截图说明` exception list. Missing images without explanation mean the note is incomplete.
   - Use the matrix to decide note order. Do not follow screenshot order or transcript order when that would weaken the teaching chain.
   - For technical DSX notes, separate toy explanation from real-model evidence. If a hand-written notebook demonstrates the idea and a LLaMA/Qwen/project notebook shows the production path, include both levels when available.
   - If the draft feels like parallel concept summaries, rewrite it into a problem chain: previous lesson or limitation -> new concept motivation -> mechanism -> screenshot evidence -> source-code evidence -> failure mode -> takeaway.
   - Treat the user's accepted RoPE-style notes as the quality bar: the note should read like an experienced teacher guiding a reader through why each idea follows from the previous one.

6. Build the Markdown note.
   - Use a clear Chinese title, source metadata, and a short summary.
   - Put source metadata in an Obsidian callout at the top, not as a plain bullet block. Use this exact shape:
     `> [!info] 资料来源`, followed by audio, transcript, screenshot folder, project/source root, ASR provider, and correction notes.
   - Link to the separate transcript file in metadata, usually under `assets/<lesson>/<lesson>_逐字稿.md`.
   - Add a clickable Obsidian table of contents near the top when the note has multiple major sections. Prefer `[[#完整标题|显示名]]` links and verify every target heading exists.
   - Add a `课程笔记` section with coherent headings, explanations, action items, terminology, source anchors, and semantically placed screenshots.
   - For normal DSX technical course notes, include these structural anchors unless the user explicitly asks for a shorter artifact: `先给结论`, `课程承接`, `学习地图`, main teaching chapters, `大模型算法工程师易错点` or `工程师易错点`, and `复盘动作与自测题`.
   - Reconstruct the teaching flow instead of dumping subtitles chronologically. For each major section, write in this order: motivation, core idea, mechanism, example or evidence, and takeaway. Be explicit about why the speaker introduces a concept, what problem it solves, and how the next idea follows.
   - Use content-based transitions in the main note. Do not write phrases like `老师在 09:52 之后引入 mask`; write the actual teaching transition, such as `在说明普通 Self-Attention 默认能看全句之后，老师引入 mask 这个约束`。
   - Keep technical depth, but introduce formal formulas only after plain-language intuition. When a section is dense, split it into smaller subsections that build understanding progressively.
   - End every major chapter-style section with `### 本章小结`.
   - For technical project courses, especially this user's Qwen3-VL/grounding notes, use a "大模型算法工程师视角" rather than a generic "学霸笔记" voice: keep `先给结论`, `学习地图`, `课程精讲`, `源码精读`, `工程师易错点`, `自测题`, and `复盘动作`, and make the note read like a reproducible engineering analysis.
   - A study-grade engineering note must be usable for review and reproduction: it should explain why each step exists, how it connects to the previous and next lessons, what would break if the step is wrong, and which exact source lines prove the claim.
   - Use Obsidian callouts as a required teaching device, not optional decoration. For a normal technical lesson note, include:
     - At least one `> [!info] 资料来源` callout near the top.
     - At least two `> [!important] ...` callouts for central claims, definitions, mechanism summaries, formulas, or dense section takeaways.
     - At least one `> [!warning] ...` callout for implementation traps, boundary conditions, notation confusions, or common misunderstandings.
     - Prefer placing each callout immediately after the paragraph, formula, screenshot, or code example that motivates it. Do not collect all callouts in one appendix.
     - Use concise, specific callout titles such as `本节核心`, `关键区别`, `shape 约束`, `实现陷阱`, or `面试表达`.
     - Do not put screenshots inside callouts. Figures should remain in normal prose beside the explanation they support.
   - Use this callout pattern for dense lessons:
     ```markdown
     > [!important] 本节核心
     > 用 2-4 句话压缩读者必须带走的定义、机制或结论。

     > [!warning] 实现陷阱
     > 明确指出会写错的代码、shape、边界、公式符号或因果关系，并给出正确做法。
     ```
   - Insert screenshots near the point where the audio discusses that concept. Use relative Obsidian links:
     `![说明](assets/<原始截图文件名>.jpg)`
   - Add concise captions explaining why each screenshot belongs there, what problem it clarifies, and what the reader should take away. Captions should not merely restate the filename or list OCR-like observations.
   - Every included screenshot needs nearby prose that explains its teaching value. Good captions use language like `这张图证明...`, `图中...说明...`, `这张白板解决...`, or equivalent natural prose. Do not place an image between headings without an explanatory paragraph.
   - When a screenshot shows code, pair it with the actual local source file and line anchor when available. When the note itself quotes code, the clickable script link must appear directly below the quoted code block.
   - When quoting code from a notebook or script, write the role of the code before the listing and the expected behavior or failure mode after it. The source link immediately below the code block is mandatory.
   - For concepts that remain hard to explain with only screenshots and prose, add accurate teaching visualizations. Prefer script-generated vector figures such as SVG for Markdown display and PDF for later LaTeX/PDF export. Use Python tools such as matplotlib or seaborn when they are the clearest way to draw process flows, masks, shape contracts, distributions, curves, comparisons, or summary diagrams. Do not add decorative graphics.
   - When generated figures are added, inspect them visually before insertion, place them immediately beside the explanation they support, and mention the matching PDF asset if one was generated.

7. Run a deep synthesis review before finalizing.
   - Do not accept a note only because callout counts and image links pass. Ask whether it has a continuous problem chain like: `old limitation -> new concept -> mechanism -> visual evidence -> code evidence -> engineering pitfall -> takeaway`.
   - Check that each major screenshot is used as evidence, not decoration. If a figure does not help explain the surrounding paragraph, remove it or move it.
   - Check that source links are not just collected in metadata. Important code snippets need adjacent `源码位置：` links, and the prose must explain inputs, outputs, shape, failure mode, and why that line matters.
   - Check that `课程承接` explains how this lesson follows from previous lessons and prepares later lessons.
   - Check that `学习地图` maps concepts to problems and evidence, not just a table of topics.
   - Check that `复盘动作与自测题` forces the reader to reopen the real source files or notebooks and verify the shapes/logic.

8. Verify before completion.
   - Run `scripts/check_markdown_assets.py <note.md>` to confirm all local image links resolve.
   - Run `scripts/check_course_note_quality.py <note.md> --asset-dir <lesson-asset-dir>` for synthesized course notes whenever a lesson asset folder exists. This must pass before claiming the note follows this skill. The checker enforces callouts, RoPE-grade teaching structure, screenshot captions, source anchors, code-source adjacency, TOC targets, chapter summaries, pedagogical signals, and full coverage of non-hidden lesson images.
   - Use `--no-deep-structure` only for legitimate short notes or non-course artifacts, and explicitly state that the note was intentionally checked with relaxed structure. Do not use this flag to pass a shallow technical course note.
   - Check that the main note exists in the requested output directory, the transcript note exists next to the audio under `assets/<lesson>/`, images exist in `assets/`, and no source files were modified.
   - Skim the main note to ensure the transcript has been removed from the body and that screenshots are interleaved with explanatory prose.
   - Verify clickable table-of-contents links resolve to existing headings when a TOC is present.
   - Verify no mechanical labels such as `音频依据：` or `涂鸦识别：` remain in the main note, and avoid timestamp-like lecture narration outside metadata/transcript links.
   - Verify the note uses Obsidian callouts for high-signal teaching points: `> [!info]` for provenance, `> [!important]` for core concepts, and `> [!warning]` for mistakes or failure modes. A note that only has ordinary paragraphs and an `工程师易错点` heading is incomplete.
   - Verify no important teaching content was dropped during condensation or restructuring, and check that text and figures are aligned: each inserted frame supports the surrounding explanation and shows the fullest relevant information rather than a transitional or incomplete state.
   - Check visual richness before delivery: decide whether more high-information screenshots or generated teaching visualizations would materially improve clarity; add only figures that teach something.
   - Summarize the saved paths and any uncertainty in the final response.

## ASR Notes

Use MiMo ASR first when the audio is allowed to leave the Mac and a credential is available. Store the key in macOS Keychain once:

```bash
/Users/jiangyu/.codex/skills/audio-screenshot-course-notes/scripts/install_mimo_asr_keychain.sh
```

Then run transcription without putting the key in the command line:

```bash
/Users/jiangyu/.codex/skills/audio-screenshot-course-notes/scripts/transcribe_mimo_asr.py \
  /path/to/lesson.m4a \
  --language zh \
  --segment-mode silence \
  --segment-seconds 25 \
  --min-segment-seconds 10 \
  --max-segment-seconds 30 \
  --summary-chars 180 \
  --output-md /path/to/assets/lesson/lesson_逐字稿.md \
  --segments-json /path/to/assets/lesson/lesson_transcript_segments.json
```

The script reads credentials from `MIMO_ASR_API_KEY` first, then from macOS Keychain service `wyatt-mimo-asr-api-key`. It must not be called with a literal key in a committed script, Markdown note, shell profile, or log. It uses `https://token-plan-cn.xiaomimimo.com/v1/chat/completions` by default via the base URL plus `/chat/completions`.

MiMo output files are designed for later note synthesis:
- The Markdown transcript starts with `辅助摘要`, then `短分段逐字稿`.
- Each transcript chunk uses `[HH:MM:SS --> HH:MM:SS]` so screenshots and explanations can be aligned to the closest spoken segment.
- The segments JSON stores `start_seconds`, `end_seconds`, `text`, `summary`, source chunk path, and usage metadata.
- The auxiliary summaries are generated from MiMo transcript text after deterministic cleanup. Do not treat them as a replacement for reviewing the transcript around important formulas, code, ratios, model names, or implementation details.
- MiMo must not be used as the authoring model for the main note. Codex reads the transcript, screenshots, and source code, then writes the final Markdown note.

Use a local workflow like this when MiMo is unavailable, the audio is confidential, timestamps must be finer, or no better project-specific ASR exists:

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
- High-signal ideas must be visually scannable in Obsidian callouts. Use `[!important]` for central concepts and mechanism summaries, `[!warning]` for traps and failure modes, and `[!info]` for source metadata. Do not rely on plain headings alone for these teaching signals.
- Use generated SVG/PDF teaching figures when they clarify relationships better than screenshots alone, especially for pipelines, attention masks, tensor shape flows, architecture summaries, plots, and compact mechanism diagrams.
- Keep source provenance: audio path, screenshot paths, output path, ASR model/tool, and date.
- For long lectures, create section timestamps and a compact "重点复习" section.

## Common Mistakes

- Renaming screenshots unnecessarily, overwriting same-name screenshots, or copying images without updating Markdown links.
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
- Omitting Obsidian callouts such as `> [!important]` and `> [!warning]`; a note can read polished but still fail this skill if high-signal concepts and implementation traps are not visually marked.
- Producing a shallow summary for a technical course when the user expects study notes that can support later implementation.
- Letting MiMo write or restructure the course note. In this workflow MiMo is ASR-only; Codex is responsible for the final note.
- Mentioning source files without explaining inputs, outputs, core logic, failure modes, and why those lines matter for the lecture point.
- Putting all script links in a distant source list while quoted code blocks have no adjacent clickable script link. Every important quoted code block should be followed by its own `vscode://file` source link.
- Saving large caches or generated assets on the system disk when T7 is the intended workspace.
