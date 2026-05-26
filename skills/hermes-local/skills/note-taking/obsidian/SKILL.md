---
name: obsidian
description: Read, search, create, and edit notes in the Obsidian vault.
platforms: [linux, macos, windows]
---

# Obsidian Vault

Use this skill for filesystem-first Obsidian vault work: reading notes, listing notes, searching note files, creating notes, appending content, and adding wikilinks.

## Vault path

Use a known or resolved vault path before calling file tools.

The documented vault-path convention is the `OBSIDIAN_VAULT_PATH` environment variable, for example from `~/.hermes/.env`. If it is unset, use `~/Documents/Obsidian Vault`.

File tools do not expand shell variables. Do not pass paths containing `$OBSIDIAN_VAULT_PATH` to `read_file`, `write_file`, `patch`, or `search_files`; resolve the vault path first and pass a concrete absolute path. Vault paths may contain spaces, which is another reason to prefer file tools over shell commands.

If the vault path is unknown, `terminal` is acceptable for resolving `OBSIDIAN_VAULT_PATH` or checking whether the fallback path exists. Once the path is known, switch back to file tools.

## Read a note

Use `read_file` with the resolved absolute path to the note. Prefer this over `cat` because it provides line numbers and pagination.

## List notes

Use `search_files` with `target: "files"` and the resolved vault path. Prefer this over `find` or `ls`.

- To list all markdown notes, use `pattern: "*.md"` under the vault path.
- To list a subfolder, search under that subfolder's absolute path.

## Search

Use `search_files` for both filename and content searches. Prefer this over `grep`, `find`, or `ls`.

- For filenames, use `search_files` with `target: "files"` and a filename `pattern`.
- For note contents, use `search_files` with `target: "content"`, the content regex as `pattern`, and `file_glob: "*.md"` when you want to restrict matches to markdown notes.

## Create a note

Use `write_file` with the resolved absolute path and the full markdown content. Prefer this over shell heredocs or `echo` because it avoids shell quoting issues and returns structured results.

## Append to a note

Prefer a native file-tool workflow when it is not awkward:

- Read the target note with `read_file`.
- Use `patch` for an anchored append when there is stable context, such as adding a section after an existing heading or appending before a known trailing block.
- Use `write_file` when rewriting the whole note is clearer than constructing a fragile patch.

For an anchored append with `patch`, replace the anchor with the anchor plus the new content.

For a simple append with no stable context, `terminal` is acceptable if it is the clearest safe option.

## Targeted edits

Use `patch` for focused note changes when the current content gives you stable context. Prefer this over shell text rewriting.

## Scheduled change monitoring

When Wyatt asks to "watch" or "keep an eye on" an Obsidian vault/folder, prefer a script-only Hermes cron watchdog rather than an always-running process. Create a baseline snapshot first, then run on the requested schedule and record only newly added files into durable memory. Keep the job silent when there are no new files, and alert only for new files or an unavailable vault path. See `references/nightly-vault-change-monitoring.md` for the proven WyattJY pattern.

## Summarizing recent Obsidian learning / notes for Wyatt

When Wyatt asks what he learned or what notes were made "yesterday" / "today" / recently, treat this as an Obsidian-vault recall task, not a generic chat-memory question.

1. Resolve the date from the live clock, then inspect the vault and the watcher outputs for that date.
2. Prefer the daily memory check report when present: `/Volumes/T7 Shield/hermes/home/memory/reports/daily_memory_checks/memory-check-YYYYMMDD.md`, and the linked Obsidian daily note under `0.计划/YYYY-MM-DD.md`.
3. Also inspect the watcher record under `/Volumes/T7 Shield/hermes/home/memory/obsidian-watch/daily/YYYY-MM-DD.md`, but be aware it may include macOS AppleDouble `._*` files and can be detected as binary because previews contain NUL bytes. Decode as UTF-8 with errors ignored if needed; ignore `._*` metadata files in the user-facing summary.
4. For the actual learning summary, read the top-level topic notes created/modified that day (usually the non-`assets/` `.md` files), especially their `## 先给结论` and `## 学习地图` sections. Do not summarize only file names when the note contents are available.
5. Return a compact Chinese summary grouped by learning thread, core takeaways, and created/updated note paths. Mention automation/memory changes separately from study notes.

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax. When creating notes, use these to link related content.
