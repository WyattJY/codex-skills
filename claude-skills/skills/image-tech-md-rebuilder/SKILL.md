---
name: image-tech-md-rebuilder
description: Rebuild complete technical Markdown documents from screenshot image folders. Use when the user gives an image path or folder of screenshots from a non-copyable cloud document, especially Chinese/English technical notes, interview prep, architecture docs, code snippets, tables, diagrams, or asks to "复刻/还原/提取图片里的MD/技术文档" rather than produce per-image OCR.
---


# Image Tech MD Rebuilder
## Claude Code Adaptation

- This copy is prepared for Claude Code personal or project skills.
- Resolve bundled files relative to ${CLAUDE_SKILL_DIR} when Claude Code exposes it; otherwise use the local skill directory.
- Map old agent/tool wording to the closest Claude Code capability by intent.

## Goal

Convert ordered screenshots of a non-copyable technical document into one coherent Markdown document. The deliverable must read like the original source document, not like an OCR dump.

## Required Output Standard

- Produce a continuous technical `.md` file with the original document structure.
- Rebuild headings, paragraphs, numbered lists, tables, code blocks, and diagrams semantically.
- Use Mermaid for flowcharts, sequence diagrams, state flows, and architecture diagrams when the screenshot contains a diagram that can be faithfully represented.
- Preserve important screenshots as image references only when OCR/Markdown cannot represent the content reliably.
- Never deliver a final document organized as "screenshot 01 text, screenshot 02 text". That format is only allowed as an intermediate OCR scaffold.
- State the final absolute output path.

## Workflow

1. **Inventory images**
   - Accept a single image path or an image folder.
   - Sort screenshots by filename and timestamp unless the user gives a different order.
   - Count images and inspect formats/sizes.

2. **Run OCR into intermediate artifacts**
   - Prefer the bundled script:

```powershell
uv run --with rapidocr --with onnxruntime --with pillow python ${CLAUDE_SKILL_DIR}\scripts\ocr_image_folder.py --image-dir "<IMAGE_DIR>" --out-dir "<WORK_DIR>\ocr_output"
```

   - If `rapidocr` fails, try `rapidocr_onnxruntime`, PaddleOCR, Tesseract, or a vision model if available.
   - Keep raw OCR artifacts for audit: JSON, plain text dump, and scaffold Markdown.

3. **Rebuild the document, do not summarize**
   - Read the OCR dump in order.
   - Merge text that is split across screenshot boundaries.
   - Identify the source document hierarchy: title, intro, sections, Q&A headings, subheadings.
   - Reconstruct code from OCR into valid fenced code blocks.
   - Reconstruct tables as Markdown tables.
   - Reconstruct diagrams as Mermaid or compact ASCII if Mermaid would distort the content.
   - Remove screenshot artifacts: line numbers that are not part of code, duplicated repeated headers, OCR garbage, UI controls, cursor marks, and watermark clutter.

4. **Correct OCR systematically**
   - Fix common technical OCR errors:
     - `FastAPl` -> `FastAPI`
     - `JsoN` -> `JSON`
     - `LLA` / `1lm` -> `LLM` / `llm` by context
     - `MCPServer` -> `MCP Server`
     - `MCPClient` -> `MCP Client`
     - `StreamableHTTP` -> `Streamable HTTP`
     - `Server-SentEvents` -> `Server-Sent Events`
     - `检素` -> `检索`
     - `攻路` -> `攻略`
     - `Agont`, `Agint`, `Agein`, `Aget` -> `Agent`
   - Correct obvious punctuation and numbering errors from OCR, such as `1。` to `1.` in numbered lists.
   - Preserve domain terms, variable names, and code identifiers exactly when visible.
   - If a line is uncertain, compare against the original image before inventing missing content.

5. **Validate before final**
   - Confirm the final Markdown has no screenshot-section structure unless the original source was actually screenshot-indexed.
   - Confirm code fences are balanced.
   - Confirm image references, if any, resolve.
   - Search for obvious OCR garbage patterns: `????`, `1111`, `1I1I`, `uouua`, `Japeps`, `FastAPl`, `Agont`, `检素`.
   - Report residual uncertainty only if specific sections remain ambiguous after checking the image.

## Output Naming

Use a clear final name near the image folder, for example:

- `technical_document_rebuilt.md`
- `<project>_technical_document.md`
- `<source-folder-name>_rebuilt.md`

Keep OCR intermediates in an `ocr_output` folder beside the final document.

## Practical Notes

- Terminal display of Chinese can be mojibake on Windows. Verify file contents with Python `Path.read_text(encoding="utf-8")` rather than trusting `Get-Content` rendering.
- For code screenshots, prefer reconstructing likely valid code over preserving OCR line-by-line noise, but do not change the intended logic.
- For interview-prep documents, keep both "short answer" and "detailed answer" sections if present.
- For architecture/flow documents, Mermaid is usually better than embedding screenshots because it makes the result editable and searchable.
