---
name: case-router
description: Use at the start of a new Hermes request to retrieve the top relevant historical cases from memory/cases before dispatching work. Supports explicit [[case-...]] references and hybrid FTS/vector retrieval.
version: 0.1.0
author: WyattJY Hermes local workflow
---
# Case Router
## Workflow
1. Parse explicit [[case-...]] references first.
2. Classify intent: product, research, training, intranet, document, misc.
3. Query FTS5 and vector index for top-3 cases.
4. Load only frontmatter, section 5 turning point, section 7 final prompt, and key bug notes.
5. Tell Wyatt which cases were loaded and why.
6. Dispatch only after the route is clear.
## Hard rules
- Load at most 3 cases and state the reuse/non-reuse reason for each.
- Always tell Wyatt which cases were loaded before dispatching work.
- Do not store or print secrets, tokens, .env content, cookies, sessions, or raw company data.
- If no case is relevant, say so explicitly and proceed without forced memory reuse.

## Anti-patterns
- Do not load more than 3 cases.
- Do not silently load context.
- Do not retrieve memory for pure small talk.
