# Claude Skills

Claude Code-compatible migration of Jiangyu's local Codex skill set.

## Layout

- `skills/` - migrated Claude Code skills. Copy or symlink these directories to `~/.claude/skills`, or use this folder as a Claude Code plugin root.
- `agents/` - Claude-native Wyatt/Hermes role agents that complement the skills, including product-manager routing.
- `.claude-plugin/plugin.json` - minimal plugin metadata for Claude Code plugin-style installation.
- `manifests/` - source mapping, review status, and count parity evidence.
- `MIGRATION_REVIEW.md` - human review of format conversion and runtime dependencies.

## Current Count

See `manifests/summary.json`. The migration is generated from the current local Codex skill roots and keeps Codex source count equal to Claude target count.

Current installed parity on this Mac: `69` migrated Codex skills in this package and `69` installed Claude Code skills under `~/.claude/skills`.

The Claude Code route and Wyatt/Hermes Claude agents are configured for CPA-backed Xiaomi MiMo with model `mimo-v2.5-pro`.

## Safety

Do not commit API keys, `.env`, `settings.json*`, cookies, session files, or local auth material. Secrets belong in Keychain, environment variables, or authenticated CLIs.
