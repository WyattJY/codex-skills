---
name: dataset-profiler
description: Use to generate safe aggregate-only profiles for CSV, JSONL, text, or image datasets without exporting company raw samples.
---

# Dataset Profiler
## Claude Code Adaptation

- This copy is prepared for Claude Code personal or project skills.
- Resolve bundled files relative to ${CLAUDE_SKILL_DIR} when Claude Code exposes it; otherwise use the local skill directory.
- Map old agent/tool wording to the closest Claude Code capability by intent.

## Inputs
- A local dataset path on a trusted machine.
- Allowed output folder for aggregate statistics.
- Optional task label: classification, retrieval, reranker, VLM, OCR, QA, or multimodal.

## Workflow
1. Inspect only aggregate metadata: row counts, columns, missing rates, label counts, length percentiles, file extensions, image dimensions when available.
2. Write a `DATA_CARD.md` with safe summaries.
3. Flag leakage risks, imbalance, duplicate IDs, missing modalities, and split mismatch.
4. For company server work, ask Wyatt to run the script there and paste only the generated aggregate card or screenshot.
5. Link the result to a `RUN_CARD` or `ERROR_CARD` when used in an experiment.

## Hard rules
- Never export raw examples, raw text, image pixels, private identifiers, cookies, tokens, or credentials.
- Default to aggregate counts and percentages only.
- If a field name itself is sensitive, redact it before writing the card.
- Keep profiler scripts dependency-light so they can run on locked-down servers.
