# Claude Skills Repository Design

## Goal

Create a separate `WyattJY/claude-skills` repository that Claude Code can use
directly, without copying the full `WyattJY/codex-skills` backup export.

## Design

Use `H:\T7\codex_downloads\repos\WyattJY-claude-skills` as the local checkout.
Generate installable skills into `skills/<skill-name>/SKILL.md`, with scripts,
references, and assets preserved when they are part of the skill.

The source set is intentionally curated:

- Active H-drive Wyatt skills from `H:\T7\codex_skills\skills`.
- Local Codex personal skills from `C:\Users\18357\.codex\skills`.
- Existing Claude-oriented skills from `WyattJY/codex-skills/skills/wyatt-claude`.

The full `codex-skills` export stays as backup and provenance. It is not a
runtime install target because it contains duplicate roots, old snapshots, and
environment-specific copies.

## Adaptation

Generated `SKILL.md` files receive a short Claude Code adaptation section. The
text keeps H-drive workspace paths where they are part of Wyatt's actual
workflow, but changes Codex-facing phrasing to Claude Code-facing phrasing.

Bundled files are copied except for generated or unsafe paths such as `.git`,
top-level `agents`, `node_modules`, `__pycache__`, `.env`, and likely
credential/session files. Nested role/reference folders named `agents` are kept.

## Install

Install with directory junctions from `C:\Users\18357\.claude\skills` to the
repository's generated `skills` directory. This keeps the H drive as the source
of truth and avoids duplicating real skill contents into the Claude profile.
`C:\Users\18357\.claude\skills` remains the personal-skill discovery entrypoint
that Claude Code expects on this Windows machine.

## Verification

Verification has three levels:

1. Static validation: every skill has frontmatter, `name`, and `description`.
2. Local install validation: `~/.claude/skills/<skill-name>` resolves.
3. Claude CLI validation: invoke `claude -p` with `/skill-name` for each skill.
4. Storage audit: installed generated skills are junctions targeting the H-drive
   repository.

## GitHub

The local repository can be committed immediately. Publishing depends on the
availability of an authenticated GitHub path. On this machine `gh` is currently
not installed and SSH to GitHub may be blocked by the network, so GitHub push is
best attempted after local generation and Claude verification are complete.
