# Claude Skills

Claude Code-compatible migration of Jiangyu's local Codex skill set.

## Layout

- `skills/` - migrated Claude Code skills. Copy or symlink these directories to `~/.claude/skills`, or use this folder as a Claude Code plugin root.
- `agents/` - Claude-native Wyatt/Hermes role agents that complement the skills, including product-manager routing.
- `.claude-plugin/plugin.json` - minimal plugin metadata for Claude Code plugin-style installation.
- `manifests/` - source mapping, review status, and count parity evidence.
- `MIGRATION_REVIEW.md` - human review of format conversion and runtime dependencies.
- `windows-mirror-reference/` - reference-only preservation of the older Windows mirror scripts and manifests; it is not part of the active Claude Code skill count.

## Current Count

See `manifests/summary.json`. The migration is generated from the current local Codex skill roots and keeps the Codex source count equal to its Claude target count.

Current installed parity on this Mac:

- `69/69` migrated Codex skills are present in this package and installed under `~/.claude/skills`.
- `14/14` Hermes local skills are also installed for Claude Code.
- `1` Claude-native `wyatt-product-team` entrypoint is installed for Hermes product-manager and product-team routing.

Active Claude Code skills under `~/.claude/skills`: `84`.

The Claude Code route and Wyatt/Hermes Claude agents are configured for Xiaomi MiMo's official Anthropic-compatible direct endpoint with model `mimo-v2.5-pro`.

## Dependency Bootstrap

The skill format is Claude Code-ready, but several workflows need local tools before they can run end to end:

- Lark daily and meeting workflows: install `lark-cli`, then authenticate calendar/task and vc/drive/docs scopes with `lark-cli auth login`.
- Word/DOCX render verification: install `pandoc` plus LibreOffice or another `soffice` provider on `PATH`; the style script itself uses `python-docx`.
- Audio and screenshot course notes: keep the ASR environment on T7, for example `/Volumes/T7 Shield/codex_cache/course_note_asr/.venv`, and install the ASR/image packages required by that skill.

## Hermes Product Team

Claude Code can use the Hermes product-manager workflow through `$wyatt-product-team`, backed by `claude-skills/agents/wyatt-product-manager.md`, `PRODUCT_TEAM_ROUTING.md`, and the local `/Users/jiangyu/.hermes-wyatt` wrappers.

## Safety

Do not commit API keys, `.env`, `settings.json*`, cookies, session files, or local auth material. Secrets belong in Keychain, environment variables, or authenticated CLIs.
