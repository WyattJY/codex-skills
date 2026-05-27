# WyattJY Claude Skills

Claude Code-ready mirror of Wyatt's user-managed Codex skills.

## Scope

This repository is a runtime set for Claude Code. It mirrors the user-managed
Codex skill roots on this machine, not Codex/Claude built-in or plugin-owned
skills:

- `skills/` contains installable Claude Code skills.
- `scripts/build-claude-skills.ps1` regenerates `skills/` from the source roots.
- `scripts/install-windows.ps1` installs these skills into `~/.claude/skills`.
- `scripts/review-claude-skills.ps1` checks the Codex-to-Claude conversion.
- `scripts/test-with-claude.ps1` invokes Claude Code against each generated skill.
- `manifests/` records source paths, generated files, and validation results.

## Source Roots

The generated skills come from:

- `H:\T7\codex_skills\skills` for active Wyatt skills.
- `C:\Users\18357\.codex\skills` for local Codex personal skills that have a
  `SKILL.md`.
- `C:\Users\18357\.agents\skills` for local shared agent skills, including Lark.

Source priority is in that order. Duplicate skill names keep the first source
and are recorded in `manifests/skipped_sources.tsv`.

The expected invariant is:

```text
unique user-managed Codex skills == generated Claude skills == installed Claude skills
```

## Windows Install

From this repository:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-windows.ps1
```

The installer creates directory junctions from:

```text
C:\Users\18357\.claude\skills\<skill-name>
```

to:

```text
H:\T7\codex_downloads\repos\WyattJY-claude-skills\skills\<skill-name>
```

Existing same-name skills are backed up before replacement. To make the Claude
personal skill directory exactly match this repository, pass `-PruneUnmanaged`:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-windows.ps1 -PruneUnmanaged
```

## Storage Model

The H drive is the source of truth. By default, real skill contents stay under:

```text
H:\T7\codex_downloads\repos\WyattJY-claude-skills\skills
```

Claude Code still discovers personal skills through:

```text
C:\Users\18357\.claude\skills
```

The installer therefore places junctions there. Those entries are pointers, not
real copies of the skill contents.

To audit that installed generated skills still point back to H:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\audit-storage.ps1
```

## Regenerate

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-claude-skills.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\validate-claude-skills.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\review-claude-skills.ps1
```

## Claude CLI Test

Install first, then run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\test-with-claude.ps1
```

The test asks Claude Code to load each skill via `/skill-name` and produce a
single-line acknowledgement. Skills with explicit license gates, such as
`mean-reviewer`, are treated as loaded but requiring manual acceptance. Results
are written under `test-results/`.

## Safety

Do not commit API keys, cookies, session files, account settings, `.env` files,
or credential-bearing outputs. The build script excludes common generated and
credential-like files, but source review is still required before publishing.
