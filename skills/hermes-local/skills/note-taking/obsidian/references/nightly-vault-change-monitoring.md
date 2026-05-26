# Nightly Obsidian vault change monitoring

Use this pattern when Wyatt asks Hermes to keep an eye on an Obsidian vault or folder and remember new files.

## Recommended approach

1. Resolve and verify the concrete vault path first. Do not use `$OBSIDIAN_VAULT_PATH` literally in file tools.
2. Create a deterministic script under `~/.hermes/scripts/` that:
   - scans the vault recursively;
   - ignores noisy/editor-state directories such as `.obsidian/`, `.trash/`, `.git/`, `.cache/`, `node_modules/`;
   - stores a baseline snapshot on first run;
   - on later runs, detects newly added files by relative path;
   - writes sanitized metadata, hashes, titles, tags, and short previews to a durable memory folder;
   - prints output only when new files are found or when the vault is unavailable.
3. Bootstrap once immediately so the first scheduled run does not treat the whole vault as new.
4. Schedule with Hermes cron as a script-only job (`no_agent=true`) at the requested time.
5. Verify with `cronjob(action='list')` after creation.

## WyattJY implementation example

- Watched vault: `/Volumes/T7 Shield/obsidian/jiangyu`
- Script: `~/.hermes/scripts/obsidian_jiangyu_watch.py`
- Schedule: `30 20 * * *` (daily 20:30, local time)
- Memory/state root: `/Volumes/T7 Shield/hermes/home/memory/obsidian-watch/`
  - `obsidian_jiangyu_state.json` — latest snapshot/baseline
  - `obsidian_jiangyu_events.jsonl` — append-only event log
  - `daily/YYYY-MM-DD.md` — human-readable daily records
  - `obsidian_jiangyu_index.md` — index of event files

## Safety and noise rules

- Do not store secrets from note contents. For Markdown/text previews, skip or redact lines containing token/API-key/password/cookie/session-like strings.
- Store metadata and short previews, not full note dumps, unless the user explicitly asks for full content ingestion.
- If no new files are found, stay silent. This matches Wyatt's preference to avoid unnecessary WeChat status messages.
- If the external drive or vault path is unavailable, print a concise alert so the cron delivery notifies Wyatt.
- Treat `.obsidian/workspace.json` and similar editor-state files as noise unless the user explicitly wants vault-settings monitoring.

## Cron shape

Use a script-only cron job for watchdogs:

```python
cronjob(
    action="create",
    name="Wyatt Obsidian jiangyu nightly memory watcher",
    schedule="30 20 * * *",
    script="obsidian_jiangyu_watch.py",
    no_agent=True,
)
```

For script-only watchdogs, empty stdout means silent success; non-empty stdout is delivered to the origin/current channel.