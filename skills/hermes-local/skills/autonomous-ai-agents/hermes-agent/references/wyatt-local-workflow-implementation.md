# WyattJY Local Hermes Workflow Implementation Pattern

Use this reference when asked to configure a local Hermes installation from a written implementation plan, especially the WyattJY multi-agent / local-memory workflow.

## Durable pattern

1. Load the implementation document and extract the exact requirements before editing config.
   - For DOCX, prefer structured extraction (python-docx if available; zip/XML fallback is acceptable for plain paragraphs/tables).
   - Save an extracted text copy next to the workflow artifacts for traceability.
2. Inspect the live Hermes install before changing anything:
   - `hermes --version`
   - `hermes config path`
   - `hermes config env-path`
   - `hermes profile list`
   - `hermes config check`
   - `hermes doctor`
3. For WyattJY's workflow, keep the local workflow home and external-drive memory separate:
   - workflow home: `~/.hermes-wyatt`
   - memory root: `/Volumes/T7 Shield/hermes/home/memory`
   - `~/.hermes-wyatt/memory` may symlink to the external-drive memory root.
4. Configure only a small set of long-lived profiles:
   - `orchestrator`
   - `memory-curator`
   - `research-analyst`
   - `product-builder`
   - `reviewer-ops`
   Use temporary subagents for product-team roles rather than creating many permanent profiles.
5. Add the workflow skill directory to each relevant profile:
   - `skills.external_dirs` should include `~/.hermes-wyatt/skills`.
6. Enable secret hygiene:
   - `security.redact_secrets: true` in every local profile.
   - Do not copy `WEIXIN_TOKEN`, `.env`, cookies, sessions, or API keys into memory/docs/skills.
   - Avoid double-running the same Weixin token across local and server homes.
7. For `memory-curator`, disable network/media/messaging style toolsets unless explicitly needed. Typical disabled list:
   - `web`, `browser`, `image_gen`, `video`, `video_gen`, `messaging`, `spotify`, `homeassistant`, `yuanbao`.
8. Implement the memory archive as Markdown plus SQLite/FTS5, not only vector search. Required tables from the WyattJY plan:
   - `projects`
   - `project_events`
   - `feedback_turning_points`
   - `bug_cases`
   - `final_prompts`
   - a `cases` table and `case_fts` FTS5 index are useful local additions for routing.
9. First-pass P0 skills should be class-level and minimal but runnable:
   - `case-archiver`
   - `case-router`
   - `paper-digest`
   - `prompt-rewriter`
   - `server-observation-loop`
   Each SKILL.md should include `name`, `description`, `workflow`, and `hard rules`.
10. Verify after edits:
   - `hermes skills list` shows the external P0 skills enabled.
   - `python3 -m py_compile` passes for local skill scripts.
   - `case-router` returns 0–3 cases for a sample non-trivial request.
   - `paper-digest` can manually generate one idea into `research/IDEA_LOG`.
   - `hermes config check` passes for every configured profile.

## Pitfalls

- Do not treat the Word plan as a vague suggestion; extract it and map every required artifact to a path or config key.
- Do not store real secrets while satisfying `.env` examples in the document. Leave placeholders or require the user to provide secrets directly.
- Do not create a long flat set of permanent profiles for every product role. The plan explicitly favors few long-term profiles plus temporary subagents.
- If a validation command initially fails because `python` is unavailable, retry with `python3`; capture the retry pattern only, not a durable claim that `python` is broken.
