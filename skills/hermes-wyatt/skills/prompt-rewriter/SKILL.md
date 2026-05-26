---
name: prompt-rewriter
description: Use at project close or after a major correction to rewrite the final prompt that would have solved the task cleanly from the start.
version: 0.1.0
author: WyattJY Hermes local workflow
---
# Prompt Rewriter
## Workflow
1. Read raw requirement, baseline interpretation, actual path, user feedback, final deliverable, and representative bugs.
2. Identify where the first prompt under-specified constraints, taste, evidence, file paths, or success criteria.
3. Write a concise final prompt with scope, artifacts, constraints, checks, and stop conditions.
4. Save to the case FINAL_PROMPT section and SQLite final_prompts.
## Hard rules
- Do not rewrite history; preserve raw wording separately.
- Include verification commands or acceptance criteria when relevant.
